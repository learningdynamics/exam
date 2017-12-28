

.PHONY: main clean dist

main:	report.pdf


report.pdf:	report.tex alifexi.sty report.bbl
	pdflatex $<
	pdflatex $<

report.bbl:	report.tex bib.bib
	pdflatex $<
	bibtex report.aux

dist:
	tar cvzf report.tar.gz report.tex alifexi.sty bib.bib

clean:
	rm -rf report.pdf *.aux *.bbl *.log
