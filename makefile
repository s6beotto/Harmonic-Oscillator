# Copyright © 2015-2016 Martin Ueding <dev@martin-ueding.de>

build = _build

latexrun := python3 ../latexrun.py --bibtex-cmd biber


# prevent all intermediate files from being deleted
.SECONDARY:
.PRECIOUS:


tex := Report/report.tex
tex_ := $(build)/report.tex
out := $(build)/report.pdf

out_slides := $(build)/slides.pdf

plots = imgs/harmonic_oscillator_track/track_10001000_track_1.pdf imgs/harmonic_oscillator_track/track_10001000_gauss_1_fit.pdf \
		imgs/harmonic_oscillator_track/track_10001000_gauss_2_fit.pdf imgs/harmonic_oscillator_track/track_10001000_gauss_2_fit.pdf \
		imgs/harmonic_oscillator_track/track_10001000_qq_1.pdf imgs/harmonic_oscillator_track/track_10001000_qq_10.pdf \
		imgs/harmonic_oscillator_track/track_10001000_qq_20.pdf imgs/harmonic_oscillator_track/track_10001000_qq_40.pdf \
		imgs/harmonic_oscillator_track/track_10001000_qq_80.pdf imgs/harmonic_oscillator_track/track_10001000_qq_100.pdf \
		imgs/harmonic_oscillator_track/track_10010000_track_1.pdf imgs/harmonic_oscillator_track/track_10010000_gauss_1_fit.pdf \
		imgs/harmonic_oscillator_track/track_10010000_gauss_2_fit.pdf imgs/harmonic_oscillator_track/track_10010000_gauss_2_fit.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_1.pdf imgs/harmonic_oscillator_track/track_10010000_qq_10.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_20.pdf imgs/harmonic_oscillator_track/track_10010000_qq_40.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_80.pdf imgs/harmonic_oscillator_track/track_10010000_qq_100.pdf \
		imgs/harmonic_oscillator_track/track_10000100_track_shifted_1.pdf imgs/harmonic_oscillator_track/track_10000100_track_shifted_2.pdf \
		imgs/harmonic_oscillator_track/track_10000100_track_shifted_5.pdf imgs/harmonic_oscillator_track/track_10000100_track_shifted_double.pdf \
		imgs/anharmonic_oscillator_track/track_100100_track_1.pdf \
		imgs/harmonic_oscillator_track/track_100100_step_track_shifted_1.pdf \
		imgs/harmonic_oscillator_track/track_100100_step_track_shifted_2.pdf \
		imgs/harmonic_oscillator_track/track_100100_step_track_shifted_5.pdf \
		imgs/harmonic_oscillator_track/track_100100_step_track_shifted_double.pdf


all: $(out) $(out_slides)
	@echo $(out) $(out_slides)


imgs/%_track_1.pdf: data/%.csv
	@python3 src/create_plots_track.py data/$*.csv -i 1 10 20 40 80 100 -o $@


imgs/%_gauss_1.pdf: data/%.csv
	@python3 src/create_plots_gauss.py data/$*.csv -i 1 10 20 40 80 100 -o $@

imgs/%_gauss_1_fit.pdf: data/%.csv
	@python3 src/create_plots_gauss.py data/$*.csv -i 1 10 20 40 80 100 -f -o $@

imgs/%_gauss_2_fit.pdf: data/%.csv
	@python3 src/create_plots_gauss.py data/$*.csv -i 10 20 40 80 100 -f -o $@


imgs/%_qq_1.pdf: data/%.csv
	@python3 src/create_plots_qq.py data/$*.csv -i 1 -o $@

imgs/%_qq_10.pdf: data/%.csv
	@python3 src/create_plots_qq.py data/$*.csv -i 10 -o $@

imgs/%_qq_20.pdf: data/%.csv
	@python3 src/create_plots_qq.py data/$*.csv -i 20 -o $@

imgs/%_qq_40.pdf: data/%.csv
	@python3 src/create_plots_qq.py data/$*.csv -i 40 -o $@

imgs/%_qq_80.pdf: data/%.csv
	@python3 src/create_plots_qq.py data/$*.csv -i 80 -o $@

imgs/%_qq_100.pdf: data/%.csv
	@python3 src/create_plots_qq.py data/$*.csv -i 100 -o $@


imgs/%_track_shifted_double.pdf: data/%.csv
	@python3 src/create_plots_track_shifted.py data/$*.csv -i 1 10 20 40 80 100 -o $@

imgs/%_track_shifted_5.pdf: data/%.csv
	@python3 src/create_plots_track_shifted.py data/$*.csv -i 1 5 10 15 20 25 -o $@

imgs/%_track_shifted_1.pdf: data/%.csv
	@python3 src/create_plots_track_shifted.py data/$*.csv -i 1 2 3 4 5 6 7 8 9 10 -o $@

imgs/%_track_shifted_2.pdf: data/%.csv
	@python3 src/create_plots_track_shifted.py data/$*.csv -i 1 3 5 7 9 11 13 15 -o $@


# harmonic oscillator
PRE := data/harmonic_oscillator_track/
$(PRE)%rack_100100.csv:
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 100 -N 100 -o $@

$(PRE)%rack_10001000.csv:
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 1000 -N 1000 -o $@

$(PRE)%rack_10000100.csv:
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 10000 -N 100 -o $@

$(PRE)%rack_10010000.csv:
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 100 -N 10000 -o $@

# step function as initialisation
$(PRE)track_100100_step.csv:
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 100 -N 100 --step -o $@

# anharmonic oscillator
PRE := data/anharmonic_oscillator_track/
$(PRE)%rack_100100.csv:
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init 0 -ir 10 -i 100 -N 100 -o $@

$(PRE)%rack_100200.csv:
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init 0 -ir 10 -i 100 -N 200 -o $@

$(PRE)%rack_10001000.csv:
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init 0 -ir 10 -i 1000 -N 1000 -o $@

$(PRE)%rack_10000100.csv:
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init 0 -ir 10 -i 10000 -N 100 -o $@

$(PRE)%rack_10010000.csv:
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init 0 -ir 10 -i 100 -N 10000 -o $@

.PHONY: $(tex_) $(build)/packages.tex

$(tex_): $(build)
	cp $(tex) $(tex_)

$(build)/packages.tex:
	cp Report/packages.tex $(build)/packages.tex

$(out): $(tex_) $(build) $(plots) $(build)/packages.tex
	cd $$(dirname $@) && $(latexrun) $$(basename $<)


$(build)/%.tex: $(build)
	cp presentation/$*.tex $@

requirements = $(build)/slides.tex $(build)/packages_slides.tex $(build)/template.tex $(build)/tikz_settings.tex
$(build)/slides.pdf: $(requirements) $(plots)
	cd $$(dirname $@) && $(latexrun) $$(basename $<)

$(build):
	@echo "Creating build directory"
	mkdir -p $(build)


.PHONY: clean
clean:
	$(RM) -r *.o *.out
	$(RM) *.pyc *.pyo
	$(RM) *.orig
	$(RM) -r $(build)/
	$(RM) -r data/
	$(RM) -r imgs/

clean-bib:
	$(RM) -r $(build)/*.out