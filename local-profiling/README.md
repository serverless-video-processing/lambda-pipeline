# Profiling the Video Processing Pipeline Python Application

### Installing Dependencies:

`conda create -n virt python=3.9`

`conda activate virt`

`pip install -r requirements.txt`

# Profiling Instructions
The following subsections describe the code for profilling cpu and memory. The code takes input the file "ElephantsDream.mp4" (which is hardcoded in app.py) and performs the video processing on it.

## Profiling CPU Usage
The tool cProfile is used to profile the CPU execution cycles of our code. The cProfiler creats an .pstats file which can be visuallized using the tool gprof2dot. The code for this process is:

``` 
# Profiling using cProfile
python3 -m cProfile -o ./data/profile.pstats app.py

# Visualise pstats file
gprof2dot -f pstats --root=app:83:pipeline ./data/profile.pstats | dot -Tpng -o ./viz/gprof2dot.png
``` 

### Visualizing CPU Execution Cycles using snakeviz
SnakeViz is a browser based graphical viewer for the output of Python’s cProfile module(Ref: [snakeviz](https://jiffyclub.github.io/snakeviz/)). Generate a plot as:

```snakeviz ./data/profile.pstats ```


## Profilling Memory Consumption
We use the tool `memory_profiler` to profile memory consumption of our pipeline. The documentation can be found at [PyPi](https://pypi.org/project/memory-profiler/).    

First add a `@profile` decorator to all the functions to be profiled:   
```
from memory_profiler import profile

@profile
def my_func():
    return _
```

Then run the program using `memory_profiler` as:   
```
# Profiling Memory Usage
python3 -m memory_profiler app.py 2>&1 | tee memory_profile.out
``` 
The above script will output a line by line memory usage for all functions with the `@profile` decorator. This output is piped to the file `memory_profile.out`