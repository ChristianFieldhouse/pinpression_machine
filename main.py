from machine import Pin
from time import sleep
import math

class Stepper():
    def __init__(self, pins):
        assert len(pins) == 4, "Must be 4 pins"
        self.pins = [
            Pin(p, Pin.OUT)
            for p in pins
        ]

    def step(self, n=1, tick=0.003):
        backwards = n > 0
        for _ in range(abs(n)):
            num_pins = len(self.pins)
            for step in range(num_pins):
                for i in range(num_pins):
                    self.pins[i].value(i == (num_pins-1)*(backwards)+step*(1 - 2*backwards))
                sleep(tick)

    def __neg__(self):
        self.pins = self.pins[::-1]
        return self

    def __add__(self, other):
        self.pins += other.pins
        return self

class Steppers():
    def __init__(self, steppers):
        self.steppers = steppers

    def step(self, n=1, tick=0.003):
        backwards = n > 0
        for _ in range(abs(n)):
            num_pins = len(self.steppers[0].pins)
            for step in range(num_pins):
                for i in range(num_pins):
                    for j in range(len(self.steppers)):
                        self.steppers[j].pins[i].value(
                            i == (num_pins-1)*(backwards)+step*(1 - 2*backwards)
                        )
                sleep(tick)

prod = Stepper([19, 18, 17, 16])
x = Stepper([0, 1, 2, 3])
y = Steppers([
    -Stepper([6, 7, 8, 9]),
    Stepper([12, 13, 14, 15]),
])
x, prod = -prod, -x

def prodinout(i):
    prod.step(-i)
    prod.step(i)

def test_loop():
    while True:
        steps = 20
        stride = 20
        for j in range(steps):
            for i in range(steps):
                x.step(stride)
                prodinout(80)
            x.step(-steps*stride)
            y.step(stride)
        y.step(-steps*stride)

def test_sin():
    while True:
        steps = 40
        stride = 20
        for j in range(steps):
            for i in range(steps):
                x.step(stride)
                prodinout(int(80 * (1.2 + 0.8*math.sin(math.pi * (i+j)/7))/2))
            x.step(-steps*stride)
            y.step(stride)
        y.step(-steps*stride)

#test_loop()
