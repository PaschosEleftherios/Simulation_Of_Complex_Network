import ciw
from collections import Counter
import math


global nodelist
global sortedList
global finalSort
global d
global counter2
global total_avg_wait
global total_avg_service
global total_avg_util_node
global total_avg_util_all
global total_avg_util_node
global total_tput
global nodeUtil
global final_mean_wait
global Conf_Interval
global final_tput



nodelist=[]
sortedList=[]
finalSort=[]
total_avg_wait=[]
total_avg_service = []
total_avg_util_node = []
total_avg_util_all = []
total_avg_util_node = [[],[],[],[],[],[],[],[],[]]
total_tput = []
nodeUtil= [0,0,0,0,0,0,0,0]
counter2=0
tValues = [6.314,2.920,2.353,2.132,2.015,1.943,1.895,1.860,1.833,1.812,1.796,1.782,1.771,1.761,
           1.753,1.746,1.740,1.734,1.729,1.725]



class RoutingDecision1(ciw.Node):
    def next_node(self,ind):

        busyness = {n: self.simulation.nodes[n].number_of_individuals for n
                    in [2, 3, 4,5,6,7,8,9]}
        chosen_n = sorted(busyness.keys(), key=lambda x: busyness[x])[0]
        return self.simulation.nodes[chosen_n]

class RoutingDecision2(ciw.Node):
    def next_node(self,ind):
        global counter2

        busyness = {n: self.simulation.nodes[n].number_of_individuals for n
                    in [2, 3, 4, 5, 6, 7, 8, 9]}
        sortedList = sorted(busyness.keys(), key=lambda x: busyness[x])
        finalSort=[]
        finalSort2=[]

        for i in range(len(sortedList)):
            finalSort.append(self.simulation.nodes[sortedList[i]])
            finalSort2.append(self.simulation.nodes[sortedList[i]])
        for i in range(1,8):
            min=finalSort[0].number_of_individuals
            if min == finalSort[i].number_of_individuals and str(finalSort[i].id_number) in "789":
                finalSort2.insert(0,finalSort[i])
        res=[]
        for x in finalSort2:
            if x not in res:
                res.append(x)

        if res[0].id_number >6 :
            return self.simulation.nodes[res[0].id_number]
        else:
            for j in range(1,10):
                if res[j].id_number > 6:
                    if (int(res[j].number_of_individuals) -d) > int(res[0].number_of_individuals):
                        counter2+=1
                        return self.simulation.nodes[res[j].id_number]
                    else:
                        break
            return self.simulation.nodes[res[0].id_number]


N = ciw.create_network(
   arrival_distributions=[
       ciw.dists.Exponential(rate=0.25),ciw.dists.NoArrivals(),ciw.dists.NoArrivals(),ciw.dists.NoArrivals(),
       ciw.dists.NoArrivals(),ciw.dists.NoArrivals(),ciw.dists.NoArrivals(),ciw.dists.NoArrivals(),ciw.dists.NoArrivals()],
   service_distributions=[
       ciw.dists.Deterministic(value=0.0),ciw.dists.Exponential(rate=0.125),ciw.dists.Exponential(rate=0.125),ciw.dists.Exponential(rate=0.125),ciw.dists.Exponential(rate=0.125),
       ciw.dists.Exponential(rate=0.125),ciw.dists.Exponential(rate=0.2),ciw.dists.Exponential(rate=0.2),ciw.dists.Exponential(rate=0.2)],
    routing=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
    number_of_servers=[1,1,1,1,1,1,1,1,1],
    queue_capacities=[float('inf'),float('inf'),float('inf'),float('inf'),float('inf'),float('inf'),
                      float('inf'),float('inf'),float('inf')]
)





def make_simulation(sim_time_secs,load_balancing,d_sim):
    global counter,counter2, final_mean_wait, final_mean_service, final_mean_util_all, S, nodeUtil, Conf_Interval, final_tput,d
    d = d_sim
    counter=1
    total_avg_wait=[]
    total_avg_service=[]
    total_tput=[]
    total_avg_util_node = [[],[],[],[],[],[],[],[],[]]
    all_util=[]
    nodeUtil= [0,0,0,0,0,0,0,0]
    counter2=0
    total_avg_util_all=[]
    while True:
        ciw.seed(counter)
        Q=ciw.Simulation(N,
                         tracker=ciw.trackers.NodePopulation(),
                         node_class=[load_balancing,ciw.Node,ciw.Node,ciw.Node,ciw.Node,ciw.Node,ciw.Node,ciw.Node,ciw.Node])
        Q.simulate_until_max_time(sim_time_secs)
        waiting=[r.waiting_time for r in Q.get_all_records() if r.arrival_date > 3600]
        service = [r.service_time for r in Q.get_all_records()if r.arrival_date > 3600]
        meanWaiting= sum(waiting)/ len(waiting)#Average Waiting time for the exact run
        meanService= sum(service)/ len(service)#Average Service time for the exact run
        total_avg_wait.append(meanWaiting)#List with all average waiting times.
        total_avg_service.append(meanService)#List with all average service times.
        final_mean_service = sum(total_avg_service)/len(total_avg_service)#Average Service Time for all runs.Grafikh
        final_mean_wait=sum(total_avg_wait)/len(total_avg_wait)#Average Wait Time for all runs.Grafikh
        service_nodes = [r.node for r in Q.get_all_records()if r.arrival_date > 3600 and r.node != 1]
        print(Counter(service_nodes))
        requests_serviced=sum(service_nodes)
        Tput=requests_serviced/sim_time_secs
        total_tput.append(Tput)
        final_tput = sum(total_tput)/len(total_tput)
        all_util=[]
        for i in range(1,9):
            total_avg_util_node[i].append(Q.transitive_nodes[i].server_utilisation)#Mesh xrhsimopoihsh ana kombo
            all_util.append(Q.transitive_nodes[i].server_utilisation)
        for i in range(1,9):
            nodeUtil[i-1]=sum(total_avg_util_node[i]) / len(total_avg_util_node[i])
        final= sum(all_util) / len(all_util)#Mesh xrhsimopoihsh synolika
        total_avg_util_all.append(final)
        final_mean_util_all=sum(total_avg_util_all)/len(total_avg_util_all)#Average Node Util for all nodes.GRAFIKH
        sum_inside_S = 0
        if counter >= 3:
            for i in range(len(total_avg_wait)):
                sum_inside_S += pow((total_avg_wait[i] - final_mean_wait), 2)
            S = math.sqrt((1 / (counter - 1)) * sum_inside_S)
            Conf_Interval = (tValues[counter - 2] * (S / math.sqrt(counter))) / final_mean_wait
            print("I have confidence interval, ",Conf_Interval)
            if Conf_Interval < 0.05:
                print("Found conf interval")
                break
            if counter == 19:
                print("Made 20 simulations")
                break
        print("Finished the %d run."% counter)
        counter += 1
    f.write("------------------------------Section 3 Output Results-----------------------------\n\n\n")
    f.write(f"Parameters given : sim_time_secs={sim_time_secs},d={d},load_balancing={load_balancing}.\n")
    f.write(f"I have confidence interval,{Conf_Interval}\n")
    f.write(f"For d = {d} i changed to fast node, {counter2} times : \n")
    f.write(f"Total Mean Waiting :{final_mean_wait}\n")
    f.write(f"Total Mean Service :{final_mean_service}\n")
    f.write(f"Total Mean Throughput :{final_tput}\n")
    for i in range(1, 9):
        f.write(f"Total Mean node {i + 1} utilization {nodeUtil[i - 1]} \n")
    f.write(f"Total Mean 'all_node' utilization : {final_mean_util_all}\n")
    f.write(
        f"Confidence Interval for Mean Waiting = {final_mean_wait - (tValues[counter - 2] * (S / math.sqrt(counter)))},{final_mean_wait + (tValues[counter - 2] * (S / math.sqrt(counter)))}\n")


f=open("results.txt","a")
f.write("------------------------------Section 1 System-----------------------------\n\n\n")
f.write("The following simulation tries to simulate the behavior a complex network.\n")
f.write("The system structure consists of nine nodes. \n")
f.write("Node 1 : Dispatcher of the system.\n")
f.write("This node is responsible for routing requests to the other eight nodes.\n")
f.write("The first five nodes are the slow nodes.\n")
f.write("The other three nodes are the fast nodes.\n")
f.write("Node 1 routes the requests to nodes depending on the value of the load_balancing parameter\n")
f.write("Algorithm RoutingDecision1 : routes the request to the least busy node.\n")
f.write("Algorithm RoutingDecision2 : routes the request to the least busy node, giving priority to fast nodes.\n")
f.write("Considering a input parameter d (integer).\n")
f.write("If a fast node has >d requests from a slow node so that :\n")
f.write("Fast_Node_Requests[i] -d > Slow_Node_Least_Busy_Requests then Dispatcher routes the request to node 'i'.\n")
f.write("Each simulation lasts one day.\n")
f.write("Routing Algorithm can be, RoutingDecision1 or RoutingDecision2 depending on the parameter load_balancing.\n")
f.write("------------------------------Section 2 Network Parameters-----------------------------\n\n\n")
f.write("The following values were given during the creation of the network in the proper fields.\n")
f.write("Arrival_Distributions: \n")
f.write("\tDispatcher (Node 1) receives a request in exponential  distribution, with rate of 0.25 seconds\n")
f.write("\tThe other eight nodes are not receiving requests from the outer world(NoArrivals)\n")
f.write("Service_Distributions: \n")
f.write("\tRequests from Node 1 to the other nodes are being sent immediately(deterministic(0.0)).\n")
f.write("\tNodes 2-6(slow) are serving requests, following exponential distribution with rate of 0.125 seconds.\n")
f.write("\tNodes 7-9(fast) are serving requests, following exponential distribution with rate of 0.2 seconds.\n")
f.write("Number_Of_Servers: \n")
f.write("\tEach node consists of one server(number_of_servers=1).\n")
f.write("Queue_Capacities: \n")
f.write("\tEvery queue on each node has infinite capacity,(Queue_Capacities=inf) \n")
f.write("Routing Table: \n")
f.write("\tEach requests has 0% possibility to be routed to other node since routing,\n")
f.write("\tis being configured by the Dispatcher.\n")


while True:
    print("Press 1 if you want to run many automated simulation \n")
    print("Press 0 if you want to run specific simulations of your choice \n")
    choice=int(input("Give the value of your choice "))
    if (choice==0):
        print("Give the simulation time,note 90000 seconds equal to 1 day + 1 hour warm up\n")
        print("sim_time_secs\n")
        sim_time_secs=int(input("Please give the simulation time in seconds :"))
        print("Choose the routing algorithm dispatcher is going to use.\n")
        print("load_balancing\n")
        load_balancing= int(input("Type 1 for RoutingDecision1 or 2 for RoutingDecision2"))
        if (load_balancing==1):
            make_simulation(sim_time_secs, RoutingDecision1, 0)
        else:
            print("Give a value for the 'd' parameter\n")
            d=int(input("Give a number for d :"))
            make_simulation(sim_time_secs, RoutingDecision2, d)
        x=int(input("If you want to make another simulation press 1 else press 0"))
        if (x==0):
            print("Finishing program\n")
            break
    else:
        sim_time_secs = 90000
        load_balancing = [RoutingDecision2, RoutingDecision2, RoutingDecision2, RoutingDecision2]
        make_simulation(sim_time_secs, RoutingDecision1, 0)
        for i in range(0, 4):
            make_simulation(sim_time_secs, load_balancing[i], i)
        break







