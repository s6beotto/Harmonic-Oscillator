# Copyright © 2015-2016 Martin Ueding <dev@martin-ueding.de>

build = _build

latexrun := python3 ../latexrun.py --bibtex-cmd biber


.PRECIOUS: %.tex %.pdf build/page/%.pdf


tex := Report/report.tex
tex_ := "$(build)/report.tex"
out := "$(build)/report.pdf"

postscript_ps := $(wildcard Postscript/*.ps)
postscript_pdf := $(postscript_ps:Postscript/%.ps=$(build)/%.pdf)

all: $(out)

$(tex_):
	cp $(tex) $(tex_)

"$(build)/packages.tex":
	cp "Report/packages.tex" "$(build)/packages.tex"


$(out): $(tex_) "$(build)/packages.tex"
	cd $$(dirname $@) && $(latexrun) $$(basename $<)

$(build):
	@echo "$(on)Creating build directory$(off)"
	mkdir -p $(build)

$(build)/page:
	@echo "$(on)Creating directory for full pages$(off)"
	mkdir -p $(build)/page

$(build)/page-lualatex:
	@echo "$(on)Creating build directory for full pages (LuaLaTeX)$(off)"
	mkdir -p $(build)/page-lualatex

$(build)/xy:
	@echo "$(on)Creating directory for X-Y data$(off)"
	mkdir -p $(build)/xy

$(build)/to_crop:
	@echo "$(on)Creating directory for PDF to crop$(off)"
	mkdir -p $(build)/to_crop


.PHONY: clean
clean:
	$(RM) *.o *.out
	$(RM) *.pyc *.pyo
	$(RM) *.orig
	$(RM) -r $(build)/*

clean-bib:
	$(RM) -r $(build)/*.out