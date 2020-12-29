import random
import matplotlib.pyplot as plt
import seaborn as sns
import simpy
import networkx as nx
sns.set(context='talk',style='whitegrid',font='serif')

def plot_results(L):
    plt.figure(figsize=(5,5))
    plt.hist(L, bins = 30, density = True, cumulative=True)  
    plt.hist(L, bins = 30, density = True, cumulative=False)  
    plt.xlabel('$Days$')
    plt.ylabel('$Probability$')
    plt.title('Completion Time')
    plt.show()

class ActivityProcess(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
    def waitup(self, node, myEvent, verbose = False):
        evnt = [e.event for e in myEvent]
        yield self.env.all_of(evnt)
        if verbose:
            print("The activating event(s) were %s" %([x.name for x in myEvent]))
        tis = random.expovariate(1.0)
        yield self.env.timeout(tis)
        finishtime = self.env.now
        if finishtime > SANglobal.finishtime:
            SANglobal.finishtime = finishtime
        SANglobal.F.nodecomplete[node].event.succeed()

class StartSingaller(object):
    def __init__(self, env, name, sEvent):
        self.env = env
        self.name = name
        self.sEvent = sEvent
        self.env.process(self.StartSingals())
    def StartSingals(self):
        yield self.env.timeout(0)
        self.sEvent.event.succeed()

class CustomEvent(object):
    def __init__(self, env, name):
        self.name = name
        self.env = env
        self.event = self.env.event()


