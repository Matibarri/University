import importlib
import SAN_classes
importlib.reload(SAN_classes)

# We will run 1000 realizations to study its stochasticity
finishtime =[]
n = 1000
for rep in range(n):
    SANglobal.finishtime = 0 #Global collector for finish time
    env = simpy.Environment() # Create simulation environment
    SANglobal.F.nodecomplete = [] # Set an empty list for nodes
    for i in range(len(SANglobal.F.nodes())): # Iterate through the nodes
        eventname = 'Complete %1d' % i 
        SANglobal.F.nodecomplete.append(CostumEvent(env,eventname)) # Add custom events to be triggered / Agregar eventos personalizados para que se activen
    
    activitynode = [] # set of activities
    for i in range(len(SANglobal.F.nodes())): 
        eventname = 'Activity %1d' # Add a name for a activity
        activitynode.append(ActivityProcess(env,activityname)) # Include the activity on a list

    for i in range(len(SANglobal.F.nodes())):
        if i is not SANglobal.inTo:
            prenodes = SANglobal.F.predecessors(i) # Save the predecessor nodes to node i
            preevents = [SANglobal.F.nodecomplete[j] for j in preenodes] # Select the preevents
            env.process(activitynode[i].waitup(i, preevents)) # Activate the waitup for the specific event

startevent = CustomEvent(env, 'Start') # Create a start event
sstart = StartSingaller(env, 'Signal', startevent).StartSingals() # set the event flag to succeed
env.process(activitynode[SANglobal.inTo].waitup(SANglobal.inTo, [startevent]))

env.run(until = 50)
finishtimes.append(SANglobal.finishtime) # Append the project's completion time
plot_results(finishtimes)