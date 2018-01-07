PART1_PICKLE_GLOB="pickle/part1/*.pickle"

.PHONY: main clean dist plot

main:	report.pdf


report.pdf:	report.tex plot  alifexi.sty report.bbl
	pdflatex $<
	pdflatex $<

plot:	part1_plot.png part2_plot.png part3_plot.png


report.bbl:	report.tex bib.bib
	pdflatex $<
	bibtex report.aux

part1_plot.png:	src/*.py pickle/part1/*.pickle
	python3 src/plots.py --files 'pickle/part1/*.pickle'

part2_plot.png:	src/*.py pickle/part2/*.pickle
	python3 src/plots.py --files 'pickle/part2/*.pickle' --plot part2_plot.png --latex part2_table.tex

part3_plot.png:	src/*.py pickle/part3/*.pickle
	python3 src/plots.py --files 'pickle/part3/*.pickle' --plot part3_plot.png --latex part3_table.tex

dist:
	tar cvzf report.tar.gz report.tex alifexi.sty bib.bib

clean:
	rm -rf report.pdf *.aux *.bbl *.log
