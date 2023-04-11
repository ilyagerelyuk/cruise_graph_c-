import queue
import heapq
from classes import edge

def algo1(graph, n_cities, transport, start):
    d = [[15000000, 15000000] for j in range(n_cities)] #d=[{время, стоимость}] Лучшие* в этот город
    p={} #p[куда]=ребро - Запоминание путей
    d[start][0]=0 #Время
    d[start][1]=0 #Стоимость
    q = [] #Куча {время, стоимость, номер вершины}
    heapq.heappush(q, [0,0,start])
    while q:
        elem = heapq.heappop(q)
        cur_time = elem[0]
        cur_cost = elem[1]
        cur_num = elem[2]
        if (cur_time > d[cur_num][0]): continue
        if ((cur_time == d[cur_num][0]) and (cur_cost > d[cur_num][1])): continue
        ways = graph[cur_num] #map[key, list]
        for citynum, it in ways.items():
            for it2 in it:
                if (it2.transport_type not in transport): continue
                if (d[citynum][0] > d[cur_num][0] + it2.cruise_time):
                    d[citynum][0] = d[cur_num][0]+(it2.cruise_time)
                    d[citynum][1] = d[cur_num][1]+(it2.cruise_fare)
                    p[citynum] = edge(cur_num, citynum, it2.transport_type, it2.cruise_time, it2.cruise_fare)
                    heapq.heappush(q, [d[citynum][0], d[citynum][1], citynum])
                elif ((d[citynum][0] == d[cur_num][0]+(it2.cruise_time)) and 
                (d[citynum][1] > d[cur_num][1] +(it2.cruise_fare))):
                    d[citynum][0] = d[cur_num][0]+(it2.cruise_time)
                    d[citynum][1] = d[cur_num][1]+(it2.cruise_fare)
                    p[citynum] = edge(cur_num, citynum, it2.transport_type, it2.cruise_time, it2.cruise_fare)
                    heapq.heappush(q, [d[citynum][0], d[citynum][1], citynum])
    return p

def algo2(graph, n_cities, transport, start):
     d = [[15000000, 15000000] for j in range(n_cities)] #d=[{стоимость, время}] Лучшие* в этот город
     p={} #p[куда]=ребро - Запоминание путей
     d[start][0]=0 #Стоимость
     d[start][1]=0 #Время
     q = [] #Куча {стоимость, время, номер вершины}
     heapq.heappush(q, [0,0,start])
     while q:
         elem = heapq.heappop(q)
         cur_time = elem[1]
         cur_cost = elem[0]
         cur_num = elem[2]
         if (cur_cost > d[cur_num][0]): continue
         if ((cur_cost == d[cur_num][0]) and (cur_time > d[cur_num][1])): continue
         ways = graph[cur_num]
         for citynum, it in ways.items():
             for it2 in it:
                 if (it2.transport_type not in transport): continue
                 if (d[citynum][0] > d[cur_num][0]+(it2.cruise_fare)):
                     d[citynum][0] = d[cur_num][0]+(it2.cruise_fare)
                     d[citynum][1] = d[cur_num][1]+(it2.cruise_time)
                     p[citynum] = edge(cur_num, citynum, it2.transport_type, it2.cruise_time, it2.cruise_fare)
                     heapq.heappush(q, [d[citynum][0], d[citynum][1], citynum])
                 elif ((d[citynum][0] == d[cur_num][0]+(it2.cruise_fare)) and
                       (d[citynum][1] > d[cur_num][1] +(it2.cruise_time))):
                     d[citynum][0] = d[cur_num][0]+(it2.cruise_fare)
                     d[citynum][1] = d[cur_num][1]+(it2.cruise_time)
                     p[citynum] = edge(cur_num, citynum, it2.transport_type, it2.cruise_time, it2.cruise_fare)
                     heapq.heappush(q, [d[citynum][0], d[citynum][1], citynum])
     return p

def algo3(graph, n_cities, transport, start):
    MAX=15000000
    q=queue.Queue()
    q.put(start)
    d = [15000000 for j in range(n_cities)]
    p={}
    d[start]=0
    while not q.empty():
        v = q.get()
        ways = graph[v]
        for numcity, it in ways.items():
            if (d[numcity]==MAX):
                for it2 in it:
                    if (it2.transport_type not in transport): continue
                    d[numcity] = d[v]+1
                    p[numcity] = edge(v, numcity, it2.transport_type, it2.cruise_time, it2.cruise_fare)
                    q.put(numcity)
                    break
    return p

def algo4(graph, n_cities, transport, start, maxcost):
     d = [15000000 for j in range(n_cities)] #d=[{мин стоимость до города}]
     p={} #p[куда]=ребро - Запоминание путей
     d[start]=0
     q = [] #Куча {стоимость, номер вершины}
     heapq.heappush(q, [0,start])
     while q:
         elem = heapq.heappop(q)
         cur_cost = elem[0]
         cur_num = elem[1]
         if (cur_cost > d[cur_num]): continue
         if (cur_cost > maxcost): break
         ways = graph[cur_num]
         for numcity, it in ways.items():
             for it2 in it:
                 if (it2.transport_type not in transport): continue
                 if ((d[numcity] > d[cur_num]+it2.cruise_fare) and (d[cur_num]+it2.cruise_fare <= maxcost)):
                     d[numcity] = d[cur_num]+it2.cruise_fare
                     p[numcity] = edge(cur_num, numcity, it2.transport_type, it2.cruise_time, it2.cruise_fare)
                     heapq.heappush(q,[d[numcity], numcity])
     return p

def algo5(graph, n_cities, transport, start, maxtime):
     d = [15000000 for j in range(n_cities)] #d=[{время до города}]
     p={} #p[куда]=ребро - Запоминание путей
     d[start]=0
     q = [] #Куча {время, номер вершины}
     heapq.heappush(q, [0,start])
     while q:
         elem = heapq.heappop(q)
         cur_time = elem[0]
         cur_num = elem[1]
         if (cur_time > d[cur_num]): continue
         if (cur_time > maxtime): break
         ways = graph[cur_num]
         for numcity, it in ways.items():
             for it2 in it:
                 if (it2.transport_type not in transport): continue
                 if ((d[numcity] > d[cur_num]+it2.cruise_time) and (d[cur_num]+it2.cruise_time <= maxtime)):
                     d[numcity] = d[cur_num]+it2.cruise_time
                     p[numcity] = edge(cur_num, numcity, it2.transport_type, it2.cruise_time, it2.cruise_fare)
                     heapq.heappush(q,[d[numcity], numcity])
     return p

def print_track(screen, tr, ind2tr, ind2city):
    if not tr.way:
        screen.addstr("Такого пути не существует\n")
        screen.addstr("=================================================\n")
        screen.addstr("\n")
        return
    for it in tr.way:
        screen.addstr(ind2tr[it.transport_type])
        screen.addstr(" из ")
        screen.addstr(ind2city[it.fr])
        screen.addstr(" в ")
        screen.addstr(ind2city[it.to])
        screen.addstr("\nВремя ")
        screen.addstr(str(it.cruise_time))
        screen.addstr(" мин; Стоимость ")
        screen.addstr(str(it.cruise_fare))
        screen.addstr(" руб\n\n")
    screen.addstr("Общее время в пути ")
    screen.addstr(str(tr.time))
    screen.addstr(" мин\n")
    screen.addstr("Общая стоимость поездки ")
    screen.addstr(str(tr.cost))
    screen.addstr(" руб\n")
    return
