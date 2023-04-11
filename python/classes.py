class edge:
    def __init__(self, a=0,b=0,c=0,d=0,e=0):
        self.fr = a
        self.to = b
        self.transport_type = c
        self.cruise_time = d
        self.cruise_fare = e

class track:
    way = []
    time = 0
    cost = 0
    def __init__(self, a, b=0, c=0): #Конструктор пути из вектора ребер
        self.way=a
        if (b==0 and c==0):
            for e in a:
                b+=e.cruise_time
                c+=e.cruise_fare
        self.time=b
        self.cost=c
    def __add__(self, other): #сложение путей
        if type(other)==list:
            newway=self.way+other.way
            return track(newway, self.time+other.time, self.cost+other.cost)
        else:
            newway=[other]+self.way
            return track(newway, self.time+other.cruise_time, self.cost+other.cruise_fare)

    def __getitem__(self, i): #Доступ к ребру в пути
        return self.way[i]
