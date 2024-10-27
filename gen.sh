#!/bin/bash

rm -r tex-tmp
if test -d tex-tmp; then
	echo "exited since tex-tmp exists"
	exit
fi
mkdir tex-tmp
cd src
python gen.py
cd ..
cp -r tex tex-tmp
cp -r tex-book tex-tmp
cd tex-tmp
mkdir log
cd tex-book
for f in *.tex; do
	echo
	echo ===== compiling $f =====
	echo X | time xelatex --halt-on-error $f > ../log/$f.log1
	if (( $? )); then
		echo error when compiling $f, exiting...
		exit
	fi
	echo X | time xelatex --halt-on-error $f > ../log/$f.log2
	if (( $? )); then
		echo error when compiling $f, exiting...
		exit
	fi
	echo X | time xelatex --halt-on-error $f > ../log/$f.log3
	if (( $? )); then
		echo error when compiling $f, exiting...
		exit
	fi
done
cd ../..
mkdir -p tex-result
cp tex-tmp/tex-book/*.pdf tex-result
echo "compile done"