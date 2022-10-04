ALL = $(wildcard *.sty *.tex)
PAPER := main
BUILD_DIR := ./build

ARTIFACT_DIR := ../artifacts

# Create the pdf in BUILD_DIR and clean build files
build: proposal.pdf move clean

artifacts: proposal.pdf
	mkdir $(ARTIFACT_DIR)
	mv $< $(ARTIFACT_DIR)

# Call with e.g. "make main.pdf"
%.pdf: %.tex 
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
