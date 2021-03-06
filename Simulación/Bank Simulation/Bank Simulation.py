from abc import ABC, abstractmethod

class AbstractEvent(ABC):
    @abstractmethod
    def execute(simulator): #Abstract Simulator
        pass

class OrderedSet(ABC):
    @abstractmethod
    def insert(x):
        pass
    @abstractmethod
    def removeFirst():
        pass
    @abstractmethod
    def size():
        pass
    @abstractmethod
    def remove(x):
        pass

class ListQueue(OrderedSet):
    def __init__(self):
        self.elements = list()
    def insert(self, x):
        i = 0
        while i < len(self.elements) and self.elements[i] < x:
            i += 1
        self.elements.insert(i, x)
    def removeFirst(self):
        if len(self.elements) == 0:
            return None
        x = self.elements.pop(0)
        return x
    def remove(self, x):
        for i in range(len(self.elements)):
            if self.elements[i] == x:
                return self.elements.pop(i)
        return None
    def size(self):
        return len(self.elements)

class Event:
    def __init__(self):
        self.time = None
    def execute(self, simulator):
        pass

class AbstractSimulator(object):
    def __init__(self):
        self.events = None # Insert an abstract event
    def insert(self, e):
        self.events.insert(e) #AbstractEvent
    def cancel(self, e):
        raise NotImplementedError("Method not implemented")

class Event(AbstractSimulator, ABC):
    def __init__(self):
        self.time = None
    def __lt__(self, y):
        if isinstance(y, Event):
            return self.time < y.time
        else:
            raise ValueError('This is no an event')
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
        
class Simulator(AbstractSimulator):
    def __init__(self):
        super().__init__()
        self.time = None 
    def now(self):
        return self.time
    def doAllEvents(self):
        while self.events.size() > 0:
            e = self.events.removeFirst()
            self.time = e.time
            e.execute(self)

class BeepSimulator(Simulator):
    def __init__(self):
        super().__init__()
    def start(self):
        self.events = ListQueue()
        self.insert(Beep(4.0))
        self.insert(Beep(1.0))
        self.insert(Beep(1.5))
        self.insert(Beep(2.0))

        self.doAllEvents()

class Beep(Event):
    def __init__(self, time):
        super().__init__()
        self.time = time
    def execute(self, simulator):
        print('this is time ', simulator.time)

###

class Counter(Event):
    def __init__(self):
        self.time = time
    def execute(self, simulator):
        print('the time is', self.time)
        if self.time < 10:
            self.time += 2
            simulator.insert(self)

class CounterSimulator(Simulator):
    def __init__(self):
        super().__init__()
    def start(self):
        self.events = ListQueue
        self.insert(Counter(0))
        self.doAllEvents()

import numpy as np

class Random(object):
    def __init__(self):
        pass
    @staticmethod
    def exponential(mean):
        return -mean*np.log(np.random.rand())
    @staticmethod
    def bernoulli(p):
        return np.random.rand() < p

class RadioactiveParticle(Event):
    def __init__(self, time):
        self.time = time
    def execute(self, simulator):
        print('A particle desintegrates at time t ', self.time)

class ParticleSimulator(Simulator):
    def __init__(self):
        super().__init__()
    def start(self):
        self.events = ListQueue()
        self.insert(RadioactiveParticle(Random.exponential(4.0)))
        self.insert(RadioactiveParticle(Random.exponential(4.0)))
        self.insert(RadioactiveParticle(Random.exponential(4.0)))
        self.insert(RadioactiveParticle(Random.exponential(4.0)))
        self.insert(RadioactiveParticle(Random.exponential(4.0)))

        self.doAllEvents()

class Customer(object):
    count = 0
    def __init__(self):
        Customer.count +=1 # here
        self.id = Customer.count

np.random.seed(0) #fijamos la aleatoriedad
simulador = ParticleSimulator()
simulador.start()

