from os import listdir
from os.path import join, isdir
from pathlib import Path
import json

def __include(fnames = []):
    return ['\\input{' + fname + "}" for fname in fnames]

def __chapter(chapter):
    return ['\\chapter{' + chapter + '}']

IGNORE_DIR = {
    "pack_settings"
}
OUTPUT_DIR = "../tex-book"
CHAPTER_ORDER = [
    "intro",
    "opening",
    "overcall",
    "conventions",
    "principles",
    "cardplay"
]

def _gen(fnames = [], chapter = "tmp"):
    cname = chapter + ".tex"
    with open("../tex/template.tex", "r") as fd:
        template = [l.strip() for l in fd.readlines()]

    output = []
    for t in template:
        if t == "%%% include":
            output += __chapter(chapter)
            output += __include(fnames)
        else:
            output.append(t)

    with open(join(OUTPUT_DIR, cname), "w") as fd:
        fd.writelines(l + "\n" for l in output)

def _gen_main(fnames = {}, cname = "main"):
    cname = cname + ".tex"
    with open("../tex/template.tex", "r") as fd:
        template = [l.strip() for l in fd.readlines()]

    fnames = fnames.copy()
    output = []
    for t in template:
        if t == "%%% include":
            # if chapter is included
            for chapter in CHAPTER_ORDER:
                if chapter in fnames:
                    output += __chapter(chapter)
                    output += __include(fnames[chapter])
                    del fnames[chapter]
            # unincluded
            for chapter in fnames:
                output += __chapter(chapter)
                output += __include(fnames[chapter])
        else:
            output.append(t)

    with open(join(OUTPUT_DIR, cname), "w") as fd:
        fd.writelines(l + "\n" for l in output)


def get_subdir(tex_dir, instr_txt = None):
    order_path = Path(join(tex_dir, instr_txt))
    # discover sections (directories only)
    subdirs = [s for s in listdir(tex_dir) if isdir(join(tex_dir, s))]
    # read optional section_order.txt to control order/exclusions
    ordered_subdirs = []
    excluded = set()
    if order_path.exists():
        with open(order_path, "r") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("!"):
                    name = line[1:].strip()
                    if name not in subdirs:
                        raise ValueError(f"Unknown chapter in exclusion: {name}")
                    excluded.add(name)
                    continue
                if line not in subdirs:
                    raise ValueError(f"Unknown chapter in order: {line}")
                if line not in ordered_subdirs:
                    ordered_subdirs.append(line)
    # append remaining sections (not ordered and not excluded), sorted for determinism
    remaining = sorted([s for s in subdirs if s not in set(ordered_subdirs) and s not in excluded])
    final_subdirs = ordered_subdirs + remaining
    return final_subdirs

def gen(tex_dir = "../tex"):
    allFnames = {}
    chapters = get_subdir(tex_dir, "chapter_order.txt")

    for chapter in chapters:
        fnames = []
        chapter_dir = join(tex_dir, chapter)
        sections = get_subdir(chapter_dir, "section_order.txt")
        for section in sections:
            fnames.append(join(tex_dir, chapter, section, "main"))
        _gen(fnames, chapter)
        allFnames[chapter] = fnames
    _gen_main(allFnames)

if __name__ == "__main__":
    gen()
