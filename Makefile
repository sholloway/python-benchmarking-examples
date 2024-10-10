#########################################################################################
# Set up the demo environment

.PHONY: env init tests shell
# Setup the environment. Installs Python, git, and make.
# Assumes DevBox is installed.
env:
	devbox shell

# Create a project specific Python virtual environment, 
# upgrade pip, and install dependencies in the venv.
init:
	@( \
	set -e ; \
	python -m venv ./.venv; \
	source .venv/bin/activate; \
	python -m ensurepip --upgrade; \
	python -m pip install --upgrade pip; \
	pip install -e .; \
	)

# Run all the tests
tests:
	@( \
	source .venv/bin/activate; \
	python -m pytest --capture=no; \
	)

# Launch a python shell in the context of the virtual environment.
shell:
	@( \
	source .venv/bin/activate; \
	bpython; \
	)


#########################################################################################
# pytest-benchmarks related targets.

# Create boxplots of a pytest-benchmark test.
plot_benchmarks:
	@( \
	source .venv/bin/activate; \
	python -m pytest tests/benchmarks_test.py --benchmark-histogram=./benchmark_histograms/$(shell date +%m_%d_%y@%H_%M)/Benchmark; \
	)

#########################################################################################
# cProfile related targets.

# Measure one run with cProfile and identify the 10 top functions. 
# Can sort by: ‘ncallls_recursion’, ‘ncalls’, ‘tottime’, ‘tottime_per’, ‘cumtime’, ‘cumtime_per’, ‘function_name’.
profile_benchmark:
	@( \
	source .venv/bin/activate; \
	python -m pytest tests/profile_with_benchmarks_test.py --benchmark-only --benchmark-cprofile=tottime_per ; \
	)

#########################################################################################
# line-profiler related targets.

# Use the line-profiler to profile a unit test.
profile_lines:
	@( \
	source .venv/bin/activate; \
	python -m kernprof \
		--line-by-line \
		--view \
		--rich \
		pytest  \
		./tests/profile_with_line_profiler_test.py::TestWithLineProfiler::test_line_profiler; \
	)

# View the output of the line-profiler after a run.
view_line_profiler_output:
	@( \
	source .venv/bin/activate; \
	python -m line_profiler --rich pytest.lprof;\
	)

#########################################################################################
# pyinstrument related targets.

# Profile a test with pyinstrument
profile_with_pyinstrument:
	@( \
	source .venv/bin/activate; \
	pyinstrument -m pytest ./tests/profile_with_line_profiler_test.py::TestWithLineProfiler::test_line_profiler; \
	)

# Profile a test with pyinstrument and generate an HTML report.
profile_with_pyinstrument_html:
	@( \
	source .venv/bin/activate; \
	pyinstrument --renderer=html -m pytest ./tests/profile_with_line_profiler_test.py::TestWithLineProfiler::test_line_profiler; \
	)


# Profile a test with pyinstrument and visualize a flamegraph with speedscope.
# https://www.speedscope.app/
profile_with_pyinstrument_speedscope:
	@( \
	source .venv/bin/activate; \
	pyinstrument --renderer=speedscope \
		-o example.speedscope.json \
		-m pytest ./tests/profile_with_line_profiler_test.py::TestWithLineProfiler::test_line_profiler; \
	)

#########################################################################################
# memray related targets.

# Profile the memory of a python module with memray, 
# generate a flamegraph HTML file, and open it in the browser.
profile_memory: 
	@( \
	set -e ; \
	source .venv/bin/activate; \
	memray run --output ./memray_output/memory_example.bin --force examples/memory_example.py; \
	memray flamegraph \
		--temporal \
		--output ./memray_output/flamegraph.html \
		--force \
		./memray_output/memory_example.bin; \
	open ./memray_output/flamegraph.html; \
	)

# Profile a test with memray. 
# Use the pytest.mark.limit_memory to identify regressions.
profile_memory_test:
	@( \
	source .venv/bin/activate; \
	python -m pytest --memray tests/memory_test.py; \
	)