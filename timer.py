import itertools
import time
import threading

from rx import start


class Timer:
    def __init__(self):
        self.startTime = round(time.time() * 1000)

        self.started = itertools.count()
        self.completed = itertools.count()
        self.sent = itertools.count()
        self.outputCadence = 100
        self.lastStopTime = 0
        self.lastPrepTime = 0
        self.lastSentTime = 0

    def getRate(self, current, previous, count):

        return (
            int(count * 1000 / (current - previous))
            if previous > 0 and previous != current
            else 0
        )

    @property
    def threadName(self):
        return threading.currentThread().getName()

    def finish(self):
        finishTime = round(time.time() * 1000)
        total = next(self.completed)
        rate = self.getRate(finishTime, self.startTime, total)
        print(
            f"{self.threadName:12} : "
            + f" end  : {total} in {finishTime - self.startTime}ms : rate {rate}/s"
        )

    def prep(self):
        i = next(self.started)
        if i % self.outputCadence == 0:
            prepTime = round(time.time() * 1000)
            rate = self.getRate(prepTime, self.lastPrepTime, self.outputCadence)
            print(
                f"{self.threadName:12} : "
                + f"     {i} : {prepTime - self.startTime}ms : rate {rate}/s"
            )
            self.lastPrepTime = prepTime

    def stop(self):
        i = next(self.completed)
        if i % self.outputCadence == 0:
            stopTime = round(time.time() * 1000)
            rate = self.getRate(stopTime, self.lastStopTime, self.outputCadence)
            print(
                f"{self.threadName:12} : "
                + f"done {i} : {stopTime - self.startTime}ms : rate {rate}/s"
            )
            self.lastStopTime = stopTime

    def send(self):
        i = next(self.sent)
        if i % self.outputCadence == 0:
            sentTime = round(time.time() * 1000)
            rate = self.getRate(sentTime, self.lastSentTime, self.outputCadence)
            print(
                f"{self.threadName:12} : "
                + f"send {i} : {sentTime - self.startTime}ms : rate {rate}/s"
            )
            self.lastSentTime = sentTime
