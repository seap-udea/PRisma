# Kepler-51 manuscript (papers/kepler51)
#
#   make              → main-v1.pdf
#   make main-v1.pdf
#   make clean        → remove LaTeX intermediates (keeps the PDF)
#   make distclean    → clean + remove the PDF

MAIN          := main-v1
LATEXMK       ?= latexmk
LATEXMK_FLAGS ?= -pdf -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all clean distclean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex tab_ring_summary.tex tab_ppc_all.tex references.bib aastex701.cls aasjournalv7.bst
	$(LATEXMK) $(LATEXMK_FLAGS) $(MAIN).tex

clean:
	@echo "Cleaning LaTeX intermediates…"
	@$(LATEXMK) -c $(MAIN).tex >/dev/null 2>&1 || true
	@rm -f \
		$(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out \
		$(MAIN).toc $(MAIN).lof $(MAIN).lot $(MAIN).fls $(MAIN).fdb_latexmk \
		$(MAIN).synctex.gz $(MAIN).synctex\(busy\) $(MAIN).nav $(MAIN).snm \
		$(MAIN).vrb $(MAIN).bcf $(MAIN).run.xml $(MAIN).notes \
		tab_ring_summary.aux tab_ppc_all.aux \
		*.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk \
		*.synctex.gz *.bbl *.blg *.bcf *.run.xml \
		missfont.log
	@echo "Done (PDF kept)."

distclean: clean
	@rm -f $(MAIN).pdf
	@echo "Removed $(MAIN).pdf."
