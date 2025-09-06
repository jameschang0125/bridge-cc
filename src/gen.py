from os import listdir
from os.path import join
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
	chapters = listdir(dir)
	allFnames = {}

	for chapter in chapters:
		fnames = []
		if (chapter in IGNORE_DIR) or Path(join(dir, chapter)).is_file():
			continue
		for section in listdir(join(dir, chapter)):
			fnames.append(join(dir, chapter, section, "main"))
		_gen(fnames, chapter)
		allFnames[chapter] = fnames
	_gen_main(allFnames)

if __name__ == "__main__":
	gen()
