# Profiling using cProfile
python3 -m cProfile -o ./data/profile.pstats app.py
# Visualise pstats file
# Ensure the root parameter is correctly defined or skipped
gprof2dot -f pstats --root=app:83:pipeline ./data/profile.pstats | dot -Tpng -o ./viz/gprof2dot.png

# Profiling Memory Usage
# mprof run --python python3 app.py
python3 -m memory_profiler app.py