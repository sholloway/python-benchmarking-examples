# python-benchmarking-examples
A collection of Python benchmarking and profiling examples.

## Setting Up the Project
This project uses Python 3.12 and Pip. Both can be installed multiple ways. For convenience,
a devbox.json file is provided to bootstrap Python. This is not required though. You can 
manage Python however you prefer. A Makefile is used to orchestrate project setup and use.

**Step 1: Bootstrap Python (Optional)** 
1. If you choose to use Devbox to manage Python then first install Devbox following its 
   [instructions](https://www.jetify.com/devbox/docs/installing_devbox/).
2. Once Devbox is installed create a shell environment with the provided devbox.json file. 
   This can be done by running `make env`. The first time you do this Python, gnumake, 
   and git will be installed and then activated in the context of a Devbox shell.
   Once the dependencies are installed when you run `make env` it will simply activate 
   those dependencies for the terminal shell you're working in.

**Step 2: Install the Python Dependencies**  
Once you have Python setup, leverage pip to install the project dependencies into a virtual environment.
This is done by running `make init`. 

The `make init` target creates a virtual environment in the project directory. This is 
named _.venv_. It then installs the dependencies into the virtual environment.

If you ever want to do a clean install, just delete _.venv_ and run `make init` again.

## Working with the Examples
| File                                | Demonstrates                                                | Instructions                                                                   | 
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------------------------|
| simple_timings_test.py              | How to manually measure how long a piece of code runs.      | Run the tests one at a time with the IDE.                                      | 
| timeit_test.py                      | How to use timeit in benchmark tests and visualize results. | Run the tests one at a time with the IDE.                                      | 
| benchmarks_test.py                  | How to use pytest-benchmarks.                               | Run the tests one at a time with the IDE and use the plot_benchmarks target.   | 
| profile_with_benchmarks_test.py     | How to use cProfiler.                                       | Run the tests one at a time with the IDE and use the profile_benchmark target. | 
| profile_with_line_profiler_test.py  | How to use the line-profiler.                               | Run the targets profile_lines and view_line_profiler_output                    | 
| memory_test.py                      | How to use memray.                                          | Run the targets profile_memory and profile_memory_test                         | 