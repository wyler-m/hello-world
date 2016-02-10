import time

# ===========================================================================================================

def min_node(cost_so_far):
    best_node = None
    previous_flight = None
    best_cost = 1000000
    best_time = 24*60

    for v in cost_so_far:
      if cost_so_far[v]["cost"] <= best_cost:
          (best_node, best_cost ) = (v, cost_so_far[v]["cost"] )
          if cost_so_far[v]["cost"] == best_cost:
            if cost_so_far[v]["cost"] < cost_so_far[best_node]["cost"]:
              best_node = v

    return best_node


def dijkstra(flight_graph, v, flight_info):
    start_time = flight_info[v]["departure_time"]
    
    cost_so_far = {}
    cost_so_far[v] = {"cost":0, "time":0}

    final_cost = {}

    path_dict = {v:"start"}

    # while len(final_cost) < len(open_cities):
    while cost_so_far:

      # get current min node
      w = min_node(cost_so_far)
      
      # found min value, add to final
      final_cost[w] = cost_so_far[w]
      del cost_so_far[w]

      if w in flight_graph:
        for next_flight in flight_graph[w].keys():

            if next_flight not in final_cost:
                 
               # check if this node needs to be added to the cost so far
                if next_flight not in cost_so_far: 
                    # make dicitonary for new flight
                    cost_so_far[next_flight] = {}

                    # for finding the cost of the flight
                    cost_so_far[next_flight]["cost"] = final_cost[w]["cost"] + flight_graph[w][next_flight]['cost']

                    # for finding the time of the flight. 
                    cost_so_far[next_flight]["time"] = final_cost[w]["time"] + flight_graph[w][next_flight]["time"]
                    
                    # to keep track of the shortest paths
                    path_dict[next_flight] = w

                # check to see if the new path is better
                elif final_cost[w]["cost"] + flight_graph[w][next_flight]['cost'] <= cost_so_far[next_flight]["cost"]:
                      
                    # for finding the cost of the flight (added whether the time is better or not)
                    cost_so_far[next_flight]["cost"] = final_cost[w]["cost"] + flight_graph[w][next_flight]['cost']
                      
                    # for finding the time of the flight. 
                    cost_so_far[next_flight]["time"] = final_cost[w]["time"] + cost_so_far[next_flight]["time"]
                    
                    # to keep track of the shortest paths
                    path_dict[next_flight] = w

                    # check to see if new path is cheaper and faster
                    if final_cost[w]["cost"] + flight_graph[w][next_flight]['cost'] == cost_so_far[next_flight]["cost"]:

                        if final_cost[w]["time"] + flight_graph[w][next_flight]["time"] < cost_so_far[next_flight]["time"]:

                             # for finding the cost of the flight (added whether the time is better or not)
                            cost_so_far[next_flight]["cost"] = final_cost[w]["cost"] + flight_graph[w][next_flight]['cost']
                              
                            # for finding the time of the flight. 
                            cost_so_far[next_flight]["time"] = final_cost[w]["time"] + cost_so_far[next_flight]["time"]
                            
                            # to keep track of the shortest paths
                            path_dict[next_flight] = w
                   
    return final_cost, path_dict


# ================================================================================================================================================
# ================================================================================================================================================
# ================================================================================================================================================


def make_graph(all_flights):
    G = {}
    flight_info = {}
    city_to_flights = {"outbound":{}, "inbound":{}}
    # flight_info['start'] = {"arrival_time": 0}
    for flight in all_flights:
        make_directed_link(G, city_to_flights, flight_info ,flight)
    return G, flight_info, city_to_flights

def make_directed_link(G, city_to_flights, flight_info ,flight):
    number = flight[0]
    origin = flight[1]
    destination = flight[2]
    [arrival_time,departure_time] = get_time(flight)
    cost = flight[-1]

    if origin not in G:
        G[origin] = {}
        city_to_flights[origin] = set()
    
    if destination not in G[origin]:
        G[origin][destination] = {}
    
    (G[origin])[destination][number] = {'cost':cost, 'arrival_time':arrival_time,'departure_time':departure_time }
    flight_info[number] = {'cost':cost, 'arrival_time':arrival_time,'departure_time':departure_time,"origin":origin,"destination":destination }
    
    city_to_flights[origin].add(number)

    return G, flight_info, city_to_flights

def make_flight_connection(flight_graph, flight_info, checked, source_flight, dest_flight):
    if source_flight not in flight_graph:
      flight_graph[source_flight] = {}

    if flight_info[source_flight]["arrival_time"] < flight_info[dest_flight]["departure_time"]:
        checked.add(source_flight)
        # make_flight_connection(flight_graph, flight_info, source_flight, dest_flight)
        flight_graph[source_flight][dest_flight] = {"cost":flight_info[source_flight]["cost"], "time":flight_info[dest_flight]["arrival_time"] - flight_info[source_flight]["departure_time"]}

    flight_graph[source_flight][flight_info[source_flight]['destination']] = {"cost":flight_info[source_flight]["cost"], "time":flight_info[source_flight]["arrival_time"] - flight_info[source_flight]["departure_time"]}

def build_flight_graph(G, flight_info):
    flight_graph = {}
    checked = set()
    for source_flight in flight_info:
      destination_city = flight_info[source_flight]["destination"]
      for city in G[destination_city].keys():
        for dest_flight in G[destination_city][city].keys():
          make_flight_connection(flight_graph, flight_info, checked, source_flight, dest_flight)
    return flight_graph


def get_time(flight):
    departure = time.strptime(flight[3],'%H:%M')
    arrival = time.strptime(flight[4],'%H:%M')
    arrival_time = arrival.tm_hour*60 + arrival.tm_min 
    departure_time =  departure.tm_hour*60 + departure.tm_min
    return arrival_time,departure_time



def dfs(graph, start, visited_cities=None, visited_flights=None, arrival=0):
    if visited_cities is None:
        visited_cities = set()
        visited_flights = set()
    else:
      visited_cities.add(start)
    for destination in set(graph[start].keys()):
        for flight in graph[start][destination].keys():
          if flight not in visited_flights:
            if graph[start][destination][flight]["departure_time"] > arrival: 
              dfs(graph, destination, visited_cities,visited_flights, graph[start][destination][flight]["arrival_time"])
              visited_flights.add(flight)


    return visited_cities, visited_flights


def get_path(path_dict, i, j):
    path = [j]
    current = j
    while  current != i:
        current = path_dict[current]
        path.append(current)
    path.reverse()
    return path
