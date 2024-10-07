.PHONY: env init tests shell

# Setup the environment. Installs Python, git, and make.
# Assumes DevBox is installed.
env:
	devbox shell

# Create a project specific Python virtual environment, upgrade pip, and install dependencies in the venv.
init:
	@( \
	set -e ; \
	python -m venv ./.venv; \
	source .venv/bin/activate; \
	python -m ensurepip --upgrade; \
	python -m pip install --upgrade pip; \
	pip install -e .; \
	)

tests:
	@( \
	source .venv/bin/activate; \
	python -m pytest --capture=no; \
	)

shell:
	@( \
	source .venv/bin/activate; \
	bpython; \
	)

plot_benchmarks:
	@( \
	source .venv/bin/activate; \
	python -m pytest tests/benchmarks_test.py --benchmark-histogram=./benchmark_histograms/$(shell date +%m_%d_%y@%H_%M)/Benchmark; \
	)


# Measure one run with cProfile and stores 10 top functions. 
# Can sort by: ‘ncallls_recursion’, ‘ncalls’, ‘tottime’, ‘tottime_per’, ‘cumtime’, ‘cumtime_per’, ‘function_name’.
profile_benchmark:
	@( \
	source .venv/bin/activate; \
	python -m pytest tests/profile_test.py --benchmark-cprofile=tottime_per ; \
	)

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
