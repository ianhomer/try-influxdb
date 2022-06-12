import itertools
import time


class Timer:
    def __init__(self):
        self.startTime = round(time.time() * 1000)

        self.started = itertools.count()
        self.completed = itertools.count()
        self.outputCadence = 100
        self.lastStopTime = 0
        self.lastPrepTime = 0

    def getRate(self, current, previous):
        return (
            int(self.outputCadence * 1000 / (current - previous))
            if previous > 0 and previous != current
            else 0
        )

    def prep(self):
        i = next(self.started)
        if i % self.outputCadence == 0:
            prepTime = round(time.time() * 1000)
            rate = self.getRate(prepTime, self.lastPrepTime)
            print(f"     {i} : {prepTime - self.startTime}ms : rate {rate}/s")
            self.lastPrepTime = prepTime

    def stop(self):
        i = next(self.completed)
        if i % self.outputCadence == 0:
            stopTime = round(time.time() * 1000)
            rate = self.getRate(stopTime, self.lastStopTime)
            print(f"done {i} : {stopTime - self.startTime}ms : rate {rate}/s")
            self.lastStopTime = stopTime
