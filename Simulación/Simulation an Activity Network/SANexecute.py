import networkx as nx
import random
import matplotlib.pyplot as plt
import seaborn as sns
import simpy
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

class SANglobal:
    F = nx.DiGraph()
    a = 0
    b = 1
    c = 2
    d = 3
    inTo = 0
    F.add_nodes_from([a,b,c,d])
    F.add_edges_from([(a,b), (a,c), (b,c), (b,d), (c,d)])
    finishtime = 0
    
# We will run 1000 realizations to study its stochasticity
finishtimes =[]
n = 10
for rep in range(n):
    SANglobal.finishtime = 0 #Global collector for finish time
    env = simpy.Environment() # Create simulation environment
    SANglobal.F.nodecomplete = [] # Set an empty list for nodes
    for i in range(len(SANglobal.F.nodes())): # Iterate through the nodes
        eventname = 'Complete %1d' % i 
        SANglobal.F.nodecomplete.append(CustomEvent(env,eventname)) # Add custom events to be triggered / Agregar eventos personalizados para que se activen
    
    activitynode = [] # set of activities
    for i in range(len(SANglobal.F.nodes())): 
        activityname = 'Activity %1d' # Add a name for a activity
        activitynode.append(ActivityProcess(env,activityname)) # Include the activity on a list

    for i in range(len(SANglobal.F.nodes())):
        if i is not SANglobal.inTo:
            prenodes = SANglobal.F.predecessors(i) # Save the predecessor nodes to node i
            preevents = [SANglobal.F.nodecomplete[j] for j in prenodes] # Select the preevents
            env.process(activitynode[i].waitup(i, preevents)) # Activate the waitup for the specific event

    startevent = CustomEvent(env, 'Start') # Create a start event
    sstart = StartSingaller(env, 'Signal', startevent).StartSingals() # set the event flag to succeed
    env.process(activitynode[SANglobal.inTo].waitup(SANglobal.inTo, [startevent]))
    
    env.run(until = 50)
    finishtimes.append(SANglobal.finishtime) # Append the project's completion time
    plot_results(finishtimes)
