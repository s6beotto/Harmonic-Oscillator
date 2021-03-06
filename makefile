
build = build

latexrun := python3 ../latexrun.py --bibtex-cmd biber


# prevent all intermediate files from being deleted
.SECONDARY:
.PRECIOUS:


tex := report/report.tex
tex_ := $(build)/report.tex
out := $(build)/report.pdf

out_slides := $(build)/slides.pdf

plots = imgs/harmonic_oscillator_track/track_1000100_track_1.pdf \
		imgs/harmonic_oscillator_track/track_1000100_track_1000.pdf \
		imgs/harmonic_oscillator_track/track_1000100_heavy_track_1000.pdf \
		imgs/harmonic_oscillator_track/track_1000100_virial.pdf \
		imgs/harmonic_oscillator_track/track_1000100_light_virial.pdf \
		imgs/harmonic_oscillator_track/track_1000100_working_virial.pdf \
		imgs/harmonic_oscillator_track/track_1000100_heavy_virial.pdf \
		imgs/harmonic_oscillator_track/track_1000100_virial_log.pdf \
		imgs/harmonic_oscillator_track/track_1000100_light_virial_log.pdf \
		imgs/harmonic_oscillator_track/track_1000100_working_virial_log.pdf \
		imgs/harmonic_oscillator_track/track_1000100_heavy_virial_log.pdf \
		imgs/harmonic_oscillator_track/track_10001000_track_1.pdf \
		imgs/harmonic_oscillator_track/track_10001000_gauss_1_fit.pdf \
		imgs/harmonic_oscillator_track/track_10001000_gauss_2_fit.pdf \
		imgs/harmonic_oscillator_track/track_10001000_gauss_2_fit.pdf \
		imgs/harmonic_oscillator_track/track_10010000_track_1.pdf \
		imgs/harmonic_oscillator_track/track_10010000_gauss_1_fit.pdf \
		imgs/harmonic_oscillator_track/track_10010000_gauss_2_fit.pdf \
		imgs/harmonic_oscillator_track/track_10010000_gauss_2_fit.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_1.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_10.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_20.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_40.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_80.pdf \
		imgs/harmonic_oscillator_track/track_10010000_qq_100.pdf \
		imgs/harmonic_oscillator_track/track_10000100_track_shifted_1.pdf \
		imgs/harmonic_oscillator_track/track_10000100_track_shifted_2.pdf \
		imgs/harmonic_oscillator_track/track_10000100_track_shifted_5.pdf \
		imgs/harmonic_oscillator_track/track_10000100_track_shifted_double.pdf \
		imgs/anharmonic_oscillator_track/track_1001002_track_1.pdf \
		imgs/anharmonic_oscillator_track/track_100010005_track_1.pdf \
		imgs/anharmonic_oscillator_track/track_100010005_track_pretty_1.pdf \
		imgs/anharmonic_oscillator_track/track_100010005_track_pretty_100.pdf \
		imgs/anharmonic_oscillator_track/track_100010005_track_pretty_1000.pdf \
		imgs/anharmonic_oscillator_track/track_1001003_track_1.pdf \
		imgs/anharmonic_oscillator_track/track_1001005_track_1.pdf \
		imgs/anharmonic_oscillator_track/track_10010010_track_1.pdf \
		imgs/anharmonic_oscillator_track/track_1001002_track_100.pdf \
		imgs/anharmonic_oscillator_track/track_1001003_track_100.pdf \
		imgs/anharmonic_oscillator_track/track_1001005_track_100.pdf \
		imgs/anharmonic_oscillator_track/track_10010010_track_100.pdf \
		imgs/harmonic_oscillator_track/track_100100_step_track_shifted_1.pdf \
		imgs/harmonic_oscillator_track/track_100100_step_track_shifted_2.pdf \
		imgs/harmonic_oscillator_track/track_100100_step_track_shifted_5.pdf \
		imgs/harmonic_oscillator_track/track_100100_step_track_shifted_double.pdf \
		imgs/harmonic_oscillator_classical_limit/harmonic_oscillator_10_classical_limit.pdf \
		imgs/harmonic_oscillator_classical_limit/harmonic_oscillator_1_classical_limit.pdf \
		imgs/harmonic_oscillator_classical_limit/harmonic_oscillator_100_classical_limit.pdf \
		imgs/harmonic_oscillator_classical_limit_energy/harmonic_oscillator_10_classical_limit_energy.pdf \
		imgs/anharmonic_oscillator_classical_limit/anharmonic_oscillator_classical_limit.pdf \
		imgs/harmonic_oscillator_track/track_10001000_thermalisation.pdf \
		imgs/harmonic_oscillator_track/track_10001000_thermalisation_log.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_1001000_lambda_parameter.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_1001000_tunnelling_current.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_1001000_bad_lambda_parameter.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_1001000_bad_tunnelling_current.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_1001000_tunnelling_current.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_10010000_lambda_parameter.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_10010000_tunnelling_current.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_10001000_lambda_parameter.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_10001000_tunnelling_current.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_100001000_lambda_parameter.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_100001000_tunnelling_current.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_100001000_tunnelling_current_log.pdf \
		imgs/anharmonic_oscillator_lambda_parameter/track_100001000_tunnelling_current_log_fit.pdf \
		imgs/potential/harm_0_0.pdf \
		imgs/potential/anharm_1_0.pdf \
		imgs/potential/anharm_5_0.pdf \
		imgs/potential/anharm_10_0.pdf \


all: $(out) $(out_slides)

.PHONY: report
report: $(out)

.PHONY: slides
slides: $(out_slides)


# images showing the tracks
imgs/%_track_1.pdf: data/%.csv src/create_plot_track.py
	@python3 src/create_plot_track.py data/$*.csv -i 1 10 20 40 80 100 -o $@

imgs/%_track_100.pdf: data/%.csv src/create_plot_track.py
	@python3 src/create_plot_track.py data/$*.csv -i 100 -o $@

imgs/%_track_1000.pdf: data/%.csv src/create_plot_track.py
	@python3 src/create_plot_track.py data/$*.csv -i 1000 -o $@


# images showing the most interesting part of the track
imgs/%_track_pretty_1.pdf: data/%.csv src/create_plot_track_pretty.py
	@python3 src/create_plot_track_pretty.py data/$*.csv -i 1 10 20 40 80 100 -o $@

imgs/%_track_pretty_100.pdf: data/%.csv src/create_plot_track_pretty.py
	@python3 src/create_plot_track_pretty.py data/$*.csv -i 100 -o $@

imgs/%_track_pretty_1000.pdf: data/%.csv src/create_plot_track_pretty.py
	@python3 src/create_plot_track_pretty.py data/$*.csv -i 1000 -o $@


# images compairing the distribution with gaussian ones
imgs/%_gauss_1.pdf: data/%.csv src/create_plot_gauss.py
	@python3 src/create_plot_gauss.py data/$*.csv -i 1 10 20 40 80 100 -o $@

imgs/%_gauss_1_fit.pdf: data/%.csv src/create_plot_gauss.py
	@python3 src/create_plot_gauss.py data/$*.csv -i 1 10 20 40 80 100 -f -o $@

imgs/%_gauss_2_fit.pdf: data/%.csv src/create_plot_gauss.py
	@python3 src/create_plot_gauss.py data/$*.csv -i 10 20 40 80 100 -f -o $@


# images compairing the distribution with gaussian ones using qq-plots
imgs/%_qq_1.pdf: data/%.csv src/create_plot_qq.py
	@python3 src/create_plot_qq.py data/$*.csv -i 1 -o $@

imgs/%_qq_10.pdf: data/%.csv src/create_plot_qq.py
	@python3 src/create_plot_qq.py data/$*.csv -i 10 -o $@

imgs/%_qq_20.pdf: data/%.csv src/create_plot_qq.py
	@python3 src/create_plot_qq.py data/$*.csv -i 20 -o $@

imgs/%_qq_40.pdf: data/%.csv src/create_plot_qq.py
	@python3 src/create_plot_qq.py data/$*.csv -i 40 -o $@

imgs/%_qq_80.pdf: data/%.csv src/create_plot_qq.py
	@python3 src/create_plot_qq.py data/$*.csv -i 80 -o $@

imgs/%_qq_100.pdf: data/%.csv src/create_plot_qq.py
	@python3 src/create_plot_qq.py data/$*.csv -i 100 -o $@


# images showing the tracks but shifted to seperate them clearly
imgs/%_track_shifted_double.pdf: data/%.csv src/create_plot_track_shifted.py
	@python3 src/create_plot_track_shifted.py data/$*.csv -i 1 10 20 40 80 100 -o $@

imgs/%_track_shifted_5.pdf: data/%.csv src/create_plot_track_shifted.py
	@python3 src/create_plot_track_shifted.py data/$*.csv -i 1 5 10 15 20 25 -o $@

imgs/%_track_shifted_1.pdf: data/%.csv src/create_plot_track_shifted.py
	@python3 src/create_plot_track_shifted.py data/$*.csv -i 1 2 3 4 5 6 7 8 9 10 -o $@

imgs/%_track_shifted_2.pdf: data/%.csv src/create_plot_track_shifted.py
	@python3 src/create_plot_track_shifted.py data/$*.csv -i 1 3 5 7 9 11 13 15 -o $@


# images showing the classical limit probability distribution
imgs/%_classical_limit.pdf: data/%.csv src/create_plot_classical_limit.py
	@python3 src/create_plot_classical_limit.py data/$*.csv -o $@


# images showing the classical limit energy
imgs/%_classical_limit_energy.pdf: data/%.csv src/create_plot_classical_limit_energy.py
	@python3 src/create_plot_classical_limit_energy.py data/$*.csv -o $@


# images showing the thermalisation
imgs/%_thermalisation.pdf: data/%.csv src/create_plot_thermalisation.py
	@python3 src/create_plot_thermalisation.py data/$*.csv -o $@

imgs/%_thermalisation_log.pdf: data/%.csv src/create_plot_thermalisation.py
	@python3 src/create_plot_thermalisation.py data/$*.csv --log -o $@


# images showing the probability distribution depending on the lambda parameter
imgs/%_lambda_parameter.pdf: data/%.csv src/create_plot_lambda_parameter.py
	@python3 src/create_plot_lambda_parameter.py data/$*.csv -o $@


# images showing the tunnelling current depending on the lambda parameter
imgs/%_tunnelling_current.pdf: data/%.csv src/create_plot_tunnelling_current.py
	@python3 src/create_plot_tunnelling_current.py data/$*.csv -o $@

imgs/%_tunnelling_current_log.pdf: data/%.csv src/create_plot_tunnelling_current.py
	@python3 src/create_plot_tunnelling_current.py data/$*.csv --log -o $@

imgs/%_tunnelling_current_log_fit.pdf: data/%.csv src/create_plot_tunnelling_current.py
	@python3 src/create_plot_tunnelling_current.py data/$*.csv --log --fit 7.0 -o $@


# images showing the distribution of the energy into potential and kinetic part
imgs/%_virial.pdf: data/%.csv src/create_plot_virial.py
	@python3 src/create_plot_virial.py data/$*.csv -o $@

imgs/%_virial_log.pdf: data/%.csv src/create_plot_virial.py
	@python3 src/create_plot_virial.py data/$*.csv -l -o $@


# images showing the used potentials
imgs/potential/harm_0_0.pdf: src/create_potential.py
	@python3 src/create_potential.py -H

imgs/potential/anharm_1_0.pdf: src/create_potential.py
	@python3 src/create_potential.py -a -d 1.0

imgs/potential/anharm_5_0.pdf: src/create_potential.py
	@python3 src/create_potential.py -a -d 5.0

imgs/potential/anharm_10_0.pdf: src/create_potential.py
	@python3 src/create_potential.py -a -d 10.0

# harmonic oscillator
PRE := data/harmonic_oscillator_track/
$(PRE)%rack_100100.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 100 -N 100 -o $@

$(PRE)%rack_1000100.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 1000 -N 100 -o $@

$(PRE)%rack_1000100_working.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 0.125 -init 0 -ir 1 -i 1000 -N 100 -o $@

$(PRE)%rack_1000100_heavy.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 10 -init 0 -ir 1 -i 1000 -N 100 -o $@

$(PRE)%rack_1000100_light.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 0.01 -init 0 -ir 1 -i 1000 -N 100 -o $@

$(PRE)%rack_10001000.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 1000 -N 1000 -o $@

$(PRE)%rack_10000100.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 10000 -N 100 -o $@

$(PRE)%rack_10010000.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 100 -N 10000 -o $@

# harmonic oscillator step function as initialisation
$(PRE)track_100100_step.csv: src/harmonic_oscillator.py
	@python3 src/harmonic_oscillator.py  -m 0.25 -init 5 -ir 1 -i 100 -N 100 --step -o $@


# harmonic oscillator classical limit
PRE := data/harmonic_oscillator_classical_limit/
$(PRE)harmonic_oscillator_10.csv: src/harmonic_oscillator_classical_limit.py
	@python3 src/harmonic_oscillator_classical_limit.py  -m 0.25 --mu 10 -init 0 -ir 5 -i 1000 -N 1000 -o $@

$(PRE)harmonic_oscillator_1.csv: src/harmonic_oscillator_classical_limit.py
	@python3 src/harmonic_oscillator_classical_limit.py  -m 0.25 --mu 1  -init 0 -ir 5 -i 1000 -N 1000 -o $@

$(PRE)harmonic_oscillator_100.csv: src/harmonic_oscillator_classical_limit.py
	@python3 src/harmonic_oscillator_classical_limit.py  -m 0.25 --mu 100 -init 0 -ir 5 -i 1000 -N 1000 -o $@


# harmonic oscillator classical limit energy
PRE := data/harmonic_oscillator_classical_limit_energy/
$(PRE)harmonic_oscillator_10.csv: src/harmonic_oscillator_classical_limit_energy.py
	@python3 src/harmonic_oscillator_classical_limit_energy.py  -m 0.25 --mu 10 -init 0 -ir 5 -i 1000 -N 1000 -o $@


# anharmonic oscillator
PRE := data/anharmonic_oscillator_track/
$(PRE)%rack_10010010.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -5 -ir 5 -i 100 -N 100 -d 10 -o $@

$(PRE)%rack_1001005.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -2.5 -ir 5 -i 100 -N 100 -d 5 -o $@

$(PRE)%rack_1001003.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -1.5 -ir 5 -i 100 -N 100 -d 3 -o $@

$(PRE)%rack_1001002.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -1 -ir 5 -i 100 -N 100 -d 2 -o $@

$(PRE)%rack_10020010.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -5 -ir 10 -i 100 -N 200 -d 10 -o $@

$(PRE)%rack_100010002.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -5 -ir 10 -i 1000 -N 1000 -d 2 -o $@

$(PRE)%rack_100010003.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -5 -ir 10 -i 1000 -N 1000 -d 3 -o $@

$(PRE)%rack_100010005.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -5 -ir 10 -i 1000 -N 1000 -d 5 -o $@

$(PRE)%rack_1000100010.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -5 -ir 10 -i 1000 -N 1000 -d 10 -o $@

$(PRE)%rack_1000010010.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -5 -ir 10 -i 10000 -N 100 -d 10 -o $@

$(PRE)%rack_1001000010.csv: src/anharmonic_oscillator.py
	@python3 src/anharmonic_oscillator.py  -m 0.25 -init -5 -ir 10 -i 100 -N 10000 -d 10 -o $@


# anharmonic oscillator classical limit
PRE := data/anharmonic_oscillator_classical_limit/
$(PRE)%.csv: src/anharmonic_oscillator_classical_limit.py
	@python3 src/anharmonic_oscillator_classical_limit.py  -m 0.01 -init -5 -ir 2 -d 4 -i 200 -N 1000 -b " -5:5:0.05" -o $@

# anharmonic oscillator lambda parameter
PRE := data/anharmonic_oscillator_lambda_parameter/
$(PRE)%1001000.csv: src/anharmonic_oscillator_lambda_parameter.py
	@python3 src/anharmonic_oscillator_lambda_parameter.py -ir 2 -i 100 -N 1000 -o $@

$(PRE)%10001000.csv: src/anharmonic_oscillator_lambda_parameter.py
	@python3 src/anharmonic_oscillator_lambda_parameter.py -ir 2 -i 1000 -N 1000 -o $@

$(PRE)%10010000.csv: src/anharmonic_oscillator_lambda_parameter.py
	@python3 src/anharmonic_oscillator_lambda_parameter.py -ir 2 -i 100 -N 10000 -o $@

$(PRE)%100001000.csv: src/anharmonic_oscillator_lambda_parameter.py
	@python3 src/anharmonic_oscillator_lambda_parameter.py -ir 2 -i 10000 -N 1000 -o $@

$(PRE)%10020000.csv: src/anharmonic_oscillator_lambda_parameter.py
	@python3 src/anharmonic_oscillator_lambda_parameter.py -ir 2 -i 100 -N 20000 -d '0:7:0.1' -o $@

$(PRE)%1001000_bad.csv: src/anharmonic_oscillator_lambda_parameter.py
	@python3 src/anharmonic_oscillator_lambda_parameter.py -init 0 -ir 10 -i 100 -N 1000 -o $@

.PHONY: plots
plots: $(plots)

$(tex_): $(build) $(tex)
	cp $(tex) $(tex_)

$(build)/packages.tex: $(build) report/packages.tex
	cp report/packages.tex $(build)/packages.tex

$(out): $(tex_) $(build) $(plots) $(build)/packages.tex
	cd $$(dirname $@) && $(latexrun) $$(basename $<)


# files related to slide generation
$(build)/slides.tex: $(build) presentation/slides.tex
	cp presentation/slides.tex $@

$(build)/packages_slides.tex: $(build) presentation/packages_slides.tex
	cp presentation/packages_slides.tex $@

$(build)/template.tex: $(build) presentation/template.tex
	cp presentation/template.tex $@

$(build)/tikz_settings.tex: $(build) presentation/tikz_settings.tex
	cp presentation/tikz_settings.tex $@

requirements = $(build)/slides.tex $(build)/packages_slides.tex $(build)/template.tex $(build)/tikz_settings.tex
$(out_slides): $(requirements) $(plots) presentation/slides.tex
	cd $$(dirname $@) && $(latexrun) $$(basename $<)

$(build):
	@echo "Creating build directory"
	mkdir -p $(build)

# create bin directory
bin:
	mkdir -p bin

# compile c library
bin/libmetropolis.so: bin src/metropolis.cpp src/metropolis.h
	g++ -c -fPIC src/metropolis.cpp -o bin/metropolis.o
	g++ -shared -Wl,-soname,libmetropolis.so -o bin/libmetropolis.so bin/metropolis.o -lm

.PHONY: compile
compile: bin/libmetropolis.so

.PHONY: clean
clean:
	$(RM) -r *.o *.out
	$(RM) *.pyc *.pyo
	$(RM) *.orig
	$(RM) -r $(build)/
	$(RM) -r data/
	$(RM) -r imgs/
	$(RM) -r bin/