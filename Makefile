PART1_N_SAMPLES=10

.PHONY: main clean dist

main:	report.pdf


report.pdf:	report.tex part1_plot.png alifexi.sty report.bbl
	pdflatex $<
	pdflatex $<

report.bbl:	report.tex bib.bib
	pdflatex $<
	bibtex report.aux

part1_plot.png:	src/*.py src/*.pyx src/Makefile
	$(MAKE) -C src/
	python3 src/part1.py -n $(PART1_N_SAMPLES)

dist:
	tar cvzf report.tar.gz report.tex alifexi.sty bib.bib

clean:
	rm -rf report.pdf *.aux *.bbl *.log
