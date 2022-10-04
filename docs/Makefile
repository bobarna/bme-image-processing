ALL = $(wildcard *.sty *.tex)
PAPER := proposal
BUILD_DIR := ./build

ARTIFACT_DIR := ../artifacts

# Create the pdf in BUILD_DIR and clean build files
build: $(PAPER).pdf move clean

artifacts: $(PAPER).pdf
	mkdir $(ARTIFACT_DIR)
	mv $< $(ARTIFACT_DIR)

# Call with e.g. "make main.pdf"
%.pdf: %.tex $(wildcard sections/*.tex)
	pdflatex $<
	- bibtex $*
	pdflatex $<
	pdflatex $<

move:
	rm -rf $(BUILD_DIR)
	mkdir $(BUILD_DIR)
	mv *.pdf $(BUILD_DIR)/

.PHONY: clean
clean:
	rm -f comment.cut $(PAPER).{aux,bbl,blg,log,out,pdf}
	rm -f *-converted-to.pdf
