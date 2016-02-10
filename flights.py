
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
#
# In many path-finding applications, a natural scoring function is
# "lexicographic ordering".  That is, there is one attribute of the
# path (say cost) that is the most important thing to minimize.
# However, all things being equal, if you have two paths with the same
# cost, you might prefer one with a shorter total flight time.
#

# We want you to take the list of flights, given below, and create a
# graph.  Then, write a modified Dijkstra's algorithm to find the best
# combination of flights to get between two cities, where flights `x`
# is better than flights `y` if `x` has lower cost *or* if they are
# tied in cost, `x` has shorter total flight time.
#
# Concretely, to get from Broome to Fitroy Crossing,
# flights [530, 112] are better than flights [526, 622]
# because, since they both cost 110, the first flights are
# shorter - 5 hours and 52 minutes compared to 
# 6 hours and 23 minutes. There maybe be even better flights, but
# you'll have to search the graph to find them.
#

def find_best_flights(flights, origin, destination):
    
    (G , flight_info, city_to_flights) = make_graph(flights)
    [open_cities, open_flights] = dfs(G, origin)
    best_flights = []
    min_cost = 10000000
    min_time = 24*60
    if destination not in open_cities:
      return None

    startpoints = city_to_flights[origin]
    possible_paths = {}

    for flight in startpoints:
      if flight in flight_graph:
        (final_cost, path_dict) = dijkstra(flight_graph, flight, flight_info)
        # for last_flight in endpoints:
        if destination in final_cost:
          if final_cost[destination]['cost'] <= min_cost:
              min_cost = final_cost[destination]['cost']
              best_flights = get_path(path_dict, flight, destination)
              if final_cost[destination]['cost'] == min_cost:
                if final_cost[destination]['time'] < min_time:
                    min_time = final_cost[destination]['time']
                    best_flights = get_path(path_dict, flight, destination)
    
    return best_flights[:-1]
    # return best_flights

#
# Here is a fictious flight schedule that is roughly based on routes
# flown by Skipper, a regional airline in Australia
# (http://www.skippers.com.au/).
#
# Each tuple contains six items: 
#   Flight Number, Origin, Destination, Departure Time, Arrival Time, Cost
# (Don't worry about any time zone issues; assume everything happens
# in the same time zone)
# Also note that overnight layovers are not allowed.
# 
all_flights = [(523, 'Broome', 'Derby', '07:17', '08:57', 60),
               (526, 'Broome', 'Derby', '08:41', '10:30', 50),
               (527, 'Broome', 'Derby', '11:46', '13:24', 200),
               (530, 'Broome', 'Derby', '14:23', '15:59', 50),
               (540, 'Broome', 'Derby', '17:49', '19:40', 50),
               (546, 'Broome', 'Derby', '20:34', '22:09', 20),
               (547, 'Broome', 'Perth', '06:41', '08:44', 30),
               (549, 'Broome', 'Perth', '17:16', '19:18', 100),
               (559, 'Carnarvon', 'Geraldton', '09:05', '10:57', 50),
               (561, 'Carnarvon', 'Geraldton', '11:14', '13:03', 30),
               (578, 'Carnarvon', 'Geraldton', '14:56', '16:48', 150),
               (582, 'Carnarvon', 'Geraldton', '17:05', '18:46', 50),
               (598, 'Carnarvon', 'Geraldton', '22:08', '23:49', 20),
               (599, 'Carnarvon', 'Perth', '07:04', '09:46', 200),
               (100, 'Carnarvon', 'Perth', '10:53', '13:38', 60),
               (604, 'Carnarvon', 'Perth', '14:50', '17:16', 200),
               (612, 'Carnarvon', 'Perth', '19:54', '22:38', 50),
               (107, 'Derby', 'Broome', '08:44', '10:36', 160),
               (108, 'Derby', 'Broome', '21:18', '23:04', 30),
               (622, 'Derby', 'Fitzroy Crossing', '13:59', '15:04', 60),
               (112, 'Derby', 'Fitzroy Crossing', '19:24', '20:15', 60),
               (113, 'Derby', 'Geraldton', '07:00', '08:10', 20),
               (115, 'Derby', 'Geraldton', '10:00', '11:07', 200),
               (118, 'Derby', 'Geraldton', '13:24', '14:31', 50),
               (121, 'Derby', 'Geraldton', '14:41', '15:52', 50),
               (122, 'Derby', 'Geraldton', '17:05', '18:09', 60),
               (635, 'Derby', 'Geraldton', '18:59', '20:18', 60),
               (638, 'Fitzroy Crossing', 'Derby', '09:18', '10:08', 50),
               (131, 'Fitzroy Crossing', 'Derby', '13:59', '14:51', 160),
               (226, 'Fitzroy Crossing', 'Derby', '14:34', '15:34', 110),
               (139, 'Fitzroy Crossing', 'Derby', '18:43', '19:36', 50),
               (654, 'Fitzroy Crossing', 'Halls Creek', '07:55', '09:48', 180),
               (143, 'Fitzroy Crossing', 'Halls Creek', '09:45', '11:39', 20),
               (280, 'Fitzroy Crossing', 'Halls Creek', '15:10', '17:07', 110),
               (660, 'Fitzroy Crossing', 'Halls Creek', '18:41', '20:24', 30),
               (661, 'Fitzroy Crossing', 'Halls Creek', '20:35', '22:19', 200),
               (663, 'Geraldton', 'Carnarvon', '08:30', '10:24', 30),
               (152, 'Geraldton', 'Carnarvon', '12:52', '14:42', 50),
               (153, 'Geraldton', 'Carnarvon', '15:24', '17:15', 30),
               (154, 'Geraldton', 'Carnarvon', '18:07', '19:53', 180),
               (671, 'Geraldton', 'Derby', '06:01', '07:10', 120),
               (676, 'Geraldton', 'Derby', '10:46', '12:09', 20),
               (165, 'Geraldton', 'Derby', '11:29', '12:45', 30),
               (683, 'Geraldton', 'Derby', '14:17', '15:23', 50),
               (174, 'Geraldton', 'Derby', '16:45', '17:58', 180),
               (175, 'Geraldton', 'Derby', '18:31', '19:47', 20),
               (179, 'Halls Creek', 'Fitzroy Crossing', '06:32', '08:22', 200),
               (187, 'Halls Creek', 'Fitzroy Crossing', '13:19', '15:03', 200),
               (702, 'Halls Creek', 'Fitzroy Crossing', '14:04', '15:45', 20),
               (192, 'Halls Creek', 'Fitzroy Crossing', '20:08', '21:59', 160),
               (195, 'Halls Creek', 'Kalbarri', '06:43', '09:01', 110),
               (709, 'Halls Creek', 'Kalbarri', '08:45', '11:04', 200),
               (199, 'Halls Creek', 'Kalbarri', '13:21', '15:39', 20),
               (209, 'Halls Creek', 'Kalbarri', '15:45', '18:01', 100),
               (723, 'Halls Creek', 'Kalbarri', '16:04', '18:10', 50),
               (724, 'Halls Creek', 'Kalbarri', '19:52', '22:07', 160),
               (216, 'Kalbarri', 'Halls Creek', '06:15', '08:34', 100),
               (217, 'Kalbarri', 'Halls Creek', '14:57', '17:14', 200),
               (730, 'Kalbarri', 'Halls Creek', '21:05', '23:24', 20),
               (731, 'Kalbarri', 'Perth', '06:18', '08:50', 50),
               (734, 'Kalbarri', 'Perth', '12:23', '14:59', 120),
               (735, 'Kalbarri', 'Perth', '12:59', '15:19', 30),
               (738, 'Kalbarri', 'Perth', '18:41', '21:10', 60),
               (739, 'Kalbarri', 'Perth', '19:42', '22:18', 60),
               (740, 'Laverton', 'Leonora', '07:39', '08:53', 180),
               (745, 'Laverton', 'Leonora', '12:20', '13:32', 20),
               (748, 'Laverton', 'Leonora', '13:44', '15:08', 30),
               (751, 'Laverton', 'Leonora', '18:00', '19:11', 200),
               (240, 'Laverton', 'Leonora', '20:34', '21:40', 110),
               (754, 'Laverton', 'Perth', '07:21', '08:21', 180),
               (247, 'Laverton', 'Perth', '20:11', '21:22', 160),
               (248, 'Leinster', 'Perth', '08:37', '11:16', 180),
               (249, 'Leinster', 'Perth', '13:44', '16:12', 110),
               (763, 'Leinster', 'Perth', '16:29', '19:06', 160),
               (765, 'Leinster', 'Perth', '19:17', '21:47', 20),
               (981, 'Leinster', 'Wiluna', '10:51', '13:03', 200),
               (770, 'Leinster', 'Wiluna', '16:02', '18:17', 50),
               (259, 'Leinster', 'Wiluna', '19:44', '22:09', 60),
               (772, 'Leonora', 'Laverton', '10:39', '11:59', 110),
               (987, 'Leonora', 'Laverton', '15:56', '17:13', 110),
               (264, 'Leonora', 'Laverton', '21:39', '22:48', 200),
               (779, 'Leonora', 'Perth', '10:29', '11:59', 50),
               (780, 'Leonora', 'Perth', '11:26', '12:58', 50),
               (783, 'Leonora', 'Perth', '19:48', '21:25', 30),
               (278, 'Meekatharra', 'Mt Magnet', '07:40', '08:42', 60),
               (792, 'Meekatharra', 'Mt Magnet', '08:35', '09:35', 60),
               (793, 'Meekatharra', 'Mt Magnet', '11:50', '12:44', 110),
               (796, 'Meekatharra', 'Mt Magnet', '14:32', '15:26', 30),
               (798, 'Meekatharra', 'Mt Magnet', '16:56', '17:52', 160),
               (288, 'Meekatharra', 'Mt Magnet', '19:38', '20:27', 60),
               (289, 'Meekatharra', 'Perth', '08:12', '09:28', 50),
               (803, 'Meekatharra', 'Perth', '09:12', '10:25', 30),
               (805, 'Meekatharra', 'Perth', '12:10', '13:16', 50),
               (298, 'Meekatharra', 'Perth', '13:33', '14:40', 50),
               (391, 'Meekatharra', 'Perth', '16:45', '17:50', 30),
               (815, 'Meekatharra', 'Perth', '20:17', '21:29', 110),
               (817, 'Monkey Mia', 'Perth', '08:26', '10:51', 20),
               (393, 'Monkey Mia', 'Perth', '13:12', '15:51', 30),
               (825, 'Monkey Mia', 'Perth', '21:01', '23:37', 180),
               (314, 'Mt Magnet', 'Meekatharra', '06:29', '07:30', 30),
               (827, 'Mt Magnet', 'Meekatharra', '08:56', '10:00', 50),
               (829, 'Mt Magnet', 'Meekatharra', '13:09', '14:14', 30),
               (832, 'Mt Magnet', 'Meekatharra', '14:10', '15:09', 30),
               (833, 'Mt Magnet', 'Meekatharra', '17:39', '18:41', 180),
               (322, 'Mt Magnet', 'Meekatharra', '19:51', '20:55', 160),
               (333, 'Mt Magnet', 'Perth', '07:53', '08:38', 120),
               (846, 'Mt Magnet', 'Perth', '15:45', '16:29', 20),
               (967, 'Mt Magnet', 'Perth', '18:04', '18:49', 20),
               (336, 'Mt Magnet', 'Wiluna', '07:34', '09:08', 200),
               (338, 'Mt Magnet', 'Wiluna', '13:35', '15:17', 30),
               (856, 'Mt Magnet', 'Wiluna', '14:54', '16:27', 50),
               (345, 'Mt Magnet', 'Wiluna', '18:03', '19:35', 50),
               (859, 'Perth', 'Broome', '07:21', '09:14', 50),
               (348, 'Perth', 'Broome', '10:37', '12:46', 60),
               (349, 'Perth', 'Broome', '12:56', '14:57', 20),
               (350, 'Perth', 'Broome', '15:01', '17:11', 110),
               (356, 'Perth', 'Broome', '18:03', '20:03', 60),
               (364, 'Perth', 'Broome', '18:45', '20:54', 150),
               (880, 'Perth', 'Carnarvon', '07:39', '10:09', 50),
               (884, 'Perth', 'Carnarvon', '10:33', '13:11', 30),
               (374, 'Perth', 'Carnarvon', '12:04', '14:31', 50),
               (375, 'Perth', 'Carnarvon', '13:59', '16:32', 30),
               (378, 'Perth', 'Carnarvon', '17:04', '19:38', 50),
               (299, 'Perth', 'Carnarvon', '19:27', '22:09', 50),
               (383, 'Perth', 'Kalbarri', '06:41', '09:12', 120),
               (384, 'Perth', 'Kalbarri', '12:42', '15:03', 20),
               (898, 'Perth', 'Kalbarri', '19:13', '21:38', 30),
               (390, 'Perth', 'Laverton', '10:20', '11:23', 60),
               (321, 'Perth', 'Laverton', '14:08', '15:03', 60),
               (905, 'Perth', 'Laverton', '19:58', '20:53', 100),
               (395, 'Perth', 'Leinster', '06:59', '09:28', 200),
               (396, 'Perth', 'Leinster', '10:17', '12:48', 100),
               (401, 'Perth', 'Leinster', '14:24', '16:50', 50),
               (914, 'Perth', 'Leinster', '18:54', '21:34', 160),
               (404, 'Perth', 'Leonora', '11:03', '12:40', 30),
               (918, 'Perth', 'Leonora', '12:37', '14:17', 150),
               (408, 'Perth', 'Leonora', '20:42', '22:10', 100),
               (923, 'Perth', 'Meekatharra', '06:21', '07:35', 110),
               (927, 'Perth', 'Meekatharra', '10:25', '11:26', 20),
               (933, 'Perth', 'Meekatharra', '14:27', '15:24', 50),
               (934, 'Perth', 'Meekatharra', '17:49', '18:50', 200),
               (941, 'Perth', 'Meekatharra', '21:56', '23:08', 30),
               (430, 'Perth', 'Monkey Mia', '06:18', '08:48', 30),
               (943, 'Perth', 'Monkey Mia', '12:11', '14:48', 180),
               (432, 'Perth', 'Monkey Mia', '17:32', '20:13', 50),
               (433, 'Perth', 'Monkey Mia', '19:48', '22:23', 100),
               (947, 'Perth', 'Mt Magnet', '06:43', '07:23', 100),
               (948, 'Perth', 'Mt Magnet', '13:59', '14:54', 20),
               (954, 'Perth', 'Mt Magnet', '15:44', '16:26', 120),
               (955, 'Perth', 'Mt Magnet', '19:34', '20:26', 200),
               (475, 'Perth', 'Wiluna', '07:34', '09:57', 60),
               (959, 'Perth', 'Wiluna', '09:44', '12:22', 50),
               (455, 'Perth', 'Wiluna', '12:22', '14:45', 60),
               (969, 'Perth', 'Wiluna', '14:26', '16:59', 50),
               (458, 'Perth', 'Wiluna', '17:19', '19:38', 60),
               (459, 'Perth', 'Wiluna', '19:09', '21:35', 30),
               (461, 'Wiluna', 'Leinster', '07:54', '10:16', 20),
               (462, 'Wiluna', 'Leinster', '08:35', '10:50', 200),
               (463, 'Wiluna', 'Leinster', '11:50', '14:01', 200),
               (976, 'Wiluna', 'Leinster', '13:54', '16:15', 50),
               (469, 'Wiluna', 'Leinster', '17:24', '19:43', 30),
               (984, 'Wiluna', 'Leinster', '19:58', '22:13', 200),
               (847, 'Wiluna', 'Mt Magnet', '07:13', '08:42', 30),
               (478, 'Wiluna', 'Mt Magnet', '11:48', '13:14', 50),
               (993, 'Wiluna', 'Mt Magnet', '13:00', '14:27', 20),
               (483, 'Wiluna', 'Mt Magnet', '17:20', '18:57', 60),
               (422, 'Wiluna', 'Mt Magnet', '21:40', '23:21', 60),
               (494, 'Wiluna', 'Perth', '08:28', '11:07', 160),
               (253, 'Wiluna', 'Perth', '11:17', '13:41', 150),
               (498, 'Wiluna', 'Perth', '13:53', '16:13', 60),
               (501, 'Wiluna', 'Perth', '17:59', '20:27', 20),
               (505, 'Wiluna', 'Perth', '20:21', '22:41', 180)]



# ===========================================================================================================================
# ===========================================================================================================================
# ===========================================================================================================================

def test():
    flights = find_best_flights(all_flights, 'Mt Magnet', 'Fitzroy Crossing')
    print flights
    assert flights == [314, 803, 348, 530, 112]

    flights = find_best_flights(all_flights, 'Leonora', 'Fitzroy Crossing')
    print flights
    assert flights == None

    flights = find_best_flights(all_flights, 'Meekatharra', 'Wiluna')
    print flights
    assert flights == [391, 459]


(G, flight_info, city_to_flights) =  make_graph(all_flights)

flight_graph = build_flight_graph(G, flight_info)


origin = 'Mt Magnet'
destination = "Fitzroy Crossing"
# print city_to_flights["outbound"][origin]
# print city_to_flights["inbound"][destination]
[open_cities, open_flights] = dfs(G, origin )

v = 391
(dist_dict,path_dict) = dijkstra(flight_graph, v, flight_info)


print get_path(path_dict,391,'Wiluna')



test()


