PART1_PICKLE_GLOB="pickle/part1/*.pickle"

.PHONY: main clean dist

main:	report.pdf


report.pdf:	report.tex part1_plot.png alifexi.sty report.bbl
	pdflatex $<
	pdflatex $<

report.bbl:	report.tex bib.bib
	pdflatex $<
	bibtex report.aux

part1_plot.png:	src/*.py
	python3 src/plots.py --files 'pickle/part1/*.pickle'

dist:
	tar cvzf report.tar.gz report.tex alifexi.sty bib.bib

clean:
	rm -rf report.pdf *.aux *.bbl *.log
