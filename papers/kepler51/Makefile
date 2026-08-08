# Kepler-51 manuscript (papers/kepler51)
#
#   make                 → main-v1r.pdf
#   make reference-runs  → copy preferred NS chains into reference_runs/
#   make notebooks       → execute all PRisma-*.ipynb (figures + tables)
#   make artifacts       → reference-runs + notebooks
#   make clean           → remove LaTeX intermediates (keeps the PDF)
#   make distclean       → clean + remove the PDF

MAIN          := main-v1re
LATEXMK       ?= latexmk
LATEXMK_FLAGS ?= -pdf -interaction=nonstopmode -halt-on-error -file-line-error

REPO_ROOT := $(abspath ../..)
PYTHON    := $(REPO_ROOT)/.venv/bin/python
ifeq ($(wildcard $(PYTHON)),)
PYTHON := python3
endif

# Preferred manuscript chains: all-free, L=(δ, T14, ρ★,obs)
RESULTS_EXORINGS := $(REPO_ROOT)/pipeline/kepler_51/results/exorings
REF_STEMS := \
	kepler_51_b_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE \
	kepler_51_d_NS_exorings_kde_delta-T14-rho_obs_nlive1200_dlogz0.01_NKDE5000_seed2026_rhoFREE_bFREE_tauFREE_pFREE

# Execution order: observables/contours first; tables from full results/;
# corner + PPC last (read reference_runs/).
NOTEBOOKS := \
	PRisma-Observables.ipynb \
	PRisma-ContoursPR.ipynb \
	PRisma-PRErrors.ipynb \
	PRisma-RingSummaryTable.ipynb \
	PRisma-CornerPlots.ipynb \
	PRisma-PPCs.ipynb

NBCONVERT_FLAGS := \
	--to notebook --execute --inplace \
	--ExecutePreprocessor.timeout=-1 \
	--ExecutePreprocessor.kernel_name=python3

.PHONY: all clean distclean reference-runs notebooks artifacts

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex tab_ring_summary.tex tab_ppc_all.tex references.bib aastex701.cls aasjournalv7.bst
	$(LATEXMK) $(LATEXMK_FLAGS) $(MAIN).tex

# Sync preferred chains from the latest parallel sweep into reference_runs/.
reference-runs:
	@mkdir -p reference_runs
	@for stem in $(REF_STEMS); do \
		npz="$(RESULTS_EXORINGS)/$${stem}.npz"; \
		meta="$(RESULTS_EXORINGS)/$${stem}_meta.json"; \
		if [ ! -f "$$npz" ] || [ ! -f "$$meta" ]; then \
			echo "ERROR: missing $$npz or $$meta" >&2; \
			exit 1; \
		fi; \
		cp -f "$$npz" "$$meta" reference_runs/; \
		echo "updated reference_runs/$${stem}.npz"; \
	done

# Regenerate figures/ and tab_*.tex by executing every manuscript notebook.
notebooks: reference-runs
	@echo "Using Python: $(PYTHON)"
	@for nb in $(NOTEBOOKS); do \
		echo ""; \
		echo "========== $$nb =========="; \
		$(PYTHON) -m nbconvert $(NBCONVERT_FLAGS) "$$nb" \
			|| { echo "ERROR: $$nb failed" >&2; exit 1; }; \
	done
	@echo ""
	@echo "Notebooks done. Figures in figures/; tables: tab_ring_summary.tex tab_ppc_all.tex"

artifacts: notebooks

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
