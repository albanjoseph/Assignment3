import time

class Timer:
    def __init__(self):
        self._start_time = None
        self.sampleCount = 0

    def start(self):
        #Start a new timer
        self._start_time = time.perf_counter()

    def reset(self):
        #Stop the timer, reset the counter, start the timer.
        self._start_time = None
        self.sampleCount = 0
        self._start_time = time.perf_counter()

    def time(self):
        #returns time elapsed
        elapsed_time = time.perf_counter() - self._start_time
        return elapsed_time
    
    def frequency(self):
        #determines frequency from time elapsed
        frequency = 1/(time.perf_counter() - self._start_time)
        return frequency