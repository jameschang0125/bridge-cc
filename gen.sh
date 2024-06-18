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
cd tex-book
for f in *.tex; do
	xelatex $f
	xelatex $f
done
cd ../..
mkdir tex-result
cp tex-tmp/tex-book/*.pdf tex-result