#!/bin/bash

set -u

target="${1:-all}"

if [[ "$target" == "all" ]]; then
	targets=(main.tex opening.tex conventions.tex principles.tex defensive.tex summary.tex)
else
	target_file="${target%.tex}.tex"
	if [[ ! -f "tex-book/$target_file" ]]; then
		echo "unknown target: $target"
		echo "available targets: all, main, opening, conventions, principles, defensive, summary"
		exit 1
	fi
	targets=("$target_file")
fi

rm -rf tex-tmp
mkdir tex-tmp

cd src
python gen.py
cd ..

cp -r tex tex-tmp
cp -r tex-book tex-tmp

cd tex-tmp
mkdir log
cd tex-book

for f in "${targets[@]}"; do
	echo
	echo ===== compiling $f =====
	echo X | time xelatex --halt-on-error "$f" > "../log/$f.log1"
	if (( $? )); then
		echo "error when compiling $f, exiting..."
		cat "../log/$f.log1"
		exit 1
	fi
	echo X | time xelatex --halt-on-error "$f" > "../log/$f.log2"
	if (( $? )); then
		echo "error when compiling $f, exiting..."
		cat "../log/$f.log2"
		exit 1
	fi
	echo X | time xelatex --halt-on-error "$f" > "../log/$f.log3"
	if (( $? )); then
		echo "error when compiling $f, exiting..."
		cat "../log/$f.log3"
		exit 1
	fi
done

cd ../..
mkdir -p tex-result
cp tex-tmp/tex-book/*.pdf tex-result
echo "compile done"