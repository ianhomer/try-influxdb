import itertools
import time


class Timer:
    def __init__(self):
        self.startTime = round(time.time() * 1000)

        self.started = itertools.count()
        self.completed = itertools.count()
        self.outputCadence = 100

    def start(self):
        i = next(self.started)
        if i % self.outputCadence == 0:
            print(
                f"     {i} : {round(time.time() * 1000) - self.startTime}ms"
            )

    def stop(self):
        i = next(self.completed)
        if i % self.outputCadence == 0:
            print(
                f"done {i} : {round(time.time() * 1000) - self.startTime}ms"
            )
