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


def gen(dir = "../tex"):
	chapters = sorted(listdir(dir))
	allFnames = {}

	for chapter in chapters:
		fnames = []
		chapter_dir = join(dir, chapter)
		if (chapter in IGNORE_DIR) or Path(chapter_dir).is_file():
			continue
		# discover sections (directories only)
		sections = [s for s in listdir(chapter_dir) if isdir(join(chapter_dir, s))]
		# read optional section_order.txt to control order/exclusions
		order_path = Path(join(chapter_dir, "section_order.txt"))
		ordered_sections = []
		excluded = set()
		if order_path.exists():
			with open(order_path, "r") as f:
				for raw in f:
					line = raw.strip()
					if not line or line.startswith("#"):
						continue
					if line.startswith("!"):
						name = line[1:].strip()
						if name not in sections:
							raise ValueError(f"Unknown section in exclusion: {chapter}/{name}")
						excluded.add(name)
						continue
					if line not in sections:
						raise ValueError(f"Unknown section in order: {chapter}/{line}")
					if line not in ordered_sections:
						ordered_sections.append(line)
		# append remaining sections (not ordered and not excluded), sorted for determinism
		remaining = sorted([s for s in sections if s not in set(ordered_sections) and s not in excluded])
		final_sections = ordered_sections + remaining
		for section in final_sections:
			fnames.append(join(dir, chapter, section, "main"))
		_gen(fnames, chapter)
		allFnames[chapter] = fnames
	_gen_main(allFnames)

if __name__ == "__main__":
	gen()
