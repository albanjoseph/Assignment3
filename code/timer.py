import time

class Timer:
    def __init__(self):
        self._start_time = None
        self.sampleCount = 0

    def start(self):
        #Start a new timer
        self._start_time = time.perf_counter()

    def stop(self):
        #Stop the timer, and report the elapsed time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        self.sampleCount = 0
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")

    def time(self):
        elapsed_time = time.perf_counter() - self._start_time
        return elapsed_time
    
    def frequency(self):
        frequency = 1/(time.perf_counter() - self._start_time)
        return frequency


