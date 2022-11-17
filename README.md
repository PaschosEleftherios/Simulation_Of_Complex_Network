# Simulation_Of_Complex_Network
Simulation of a Complex Network using ciw.

In this simulation we are cmputing metrics,using standard deviation,confidence interval...
Simulation end's after computing the 95% confidence interval of the chosen metric.
------------------------------Section 1 System-----------------------------


The following simulation tries to simulate the behavior of a complex network.
The system structure consists of nine nodes. 
Node 1 : Dispatcher of the system.
This node is responsible for routing requests to the other eight nodes.
The first five nodes are the slow nodes.
The other three nodes are the fast nodes.
Node 1 routes the requests to nodes depending on the value of the load_balancing parameter
Algorithm RoutingDecision1 : routes the request to the least busy node.
Algorithm RoutingDecision2 : routes the request to the least busy node, giving priority to fast nodes.
Considering a input parameter d (integer).
If a fast node has >d requests from a slow node so that :
Fast_Node_Requests[i] -d > Slow_Node_Least_Busy_Requests then Dispatcher routes the request to node 'i'.
Each simulation lasts one day.
Routing Algorithm can be, RoutingDecision1 or RoutingDecision2 depending on the parameter load_balancing.
------------------------------Section 2 Network Parameters-----------------------------


The following values were given during the creation of the network in the proper fields.
Arrival_Distributions: 
	Dispatcher (Node 1) receives a request in exponential  distribution, with rate of 0.25 seconds
	The other eight nodes are not receiving requests from the outer world(NoArrivals)
Service_Distributions: 
	Requests from Node 1 to the other nodes are being sent immediately(deterministic(0.0)).
	Nodes 2-6(slow) are serving requests, following exponential distribution with rate of 0.125 seconds.
	Nodes 7-9(fast) are serving requests, following exponential distribution with rate of 0.2 seconds.
Number_Of_Servers: 
	Each node consists of one server(number_of_servers=1).
Queue_Capacities: 
	Every queue on each node has infinite capacity,(Queue_Capacities=inf) 
Routing Table: 
	Each requests has 0% possibility to be routed to other node since routing,
	is being configured by the Dispatcher.

A brief analysis of the network and the results of the simulation(diagrams,explanationof the results)
is being provided in the "Simulation of heterogeneous server clusters.pdf"(For now in Greek only.)
