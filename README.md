# system note generator

This is the system notes used for the U26 event (2024). All rights reserved.

## usage

-   put your system into `tex` folder, look at the structures for example
-   run `gen.sh`, it should generate three folders: `sandbox`, `tex-book`, `tex-result`
-   usually the `tex-result` folder contains what you need

### Deterministic section ordering (section_order.txt)

For each chapter directory under `tex/` (e.g. `tex/opening`), you can create a file named `section_order.txt` to control the inclusion order of its subdirectories (sections):

-   One section directory name per line.
-   Lines starting with `#` are comments; blank lines are ignored.
-   Prefix a name with `!` to exclude that section from the chapter.
-   Any listed section that does not exist will cause an error.
-   Sections not listed (and not excluded) are appended in alphabetical order.

Example `tex/opening/section_order.txt`:

```
# explicit order first
1m
1M_
1N
!2X      # exclude this section

# remaining sections are appended in sorted order
```

## example output

```
===== compiling 1X.tex =====

real    0m1.234s
user    0m1.119s
sys     0m0.160s

real    0m1.242s
user    0m1.131s
sys     0m0.155s

===== compiling comp.tex =====

real    0m1.160s
user    0m1.062s
sys     0m0.156s

real    0m1.145s
user    0m1.020s
sys     0m0.166s

===== compiling main.tex =====

real    0m1.413s
user    0m1.355s
sys     0m0.134s

real    0m1.620s
user    0m1.480s
sys     0m0.160s

===== compiling pre.tex =====

real    0m1.188s
user    0m1.098s
sys     0m0.144s

real    0m1.134s
user    0m1.026s
sys     0m0.145s

===== compiling util.tex =====

real    0m1.225s
user    0m1.147s
sys     0m0.139s

real    0m1.249s
user    0m1.153s
sys     0m0.146s
compile done
```
