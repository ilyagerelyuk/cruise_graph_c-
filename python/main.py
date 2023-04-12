import curses
import sys
from time import time_ns
from resource import getrusage, RUSAGE_SELF

from algos import *
from classes import *

def get_rss():
    return getrusage(RUSAGE_SELF).ru_maxrss

logname = "pylog.txt"
log = open(logname, "w")
print("start prog max rss =",get_rss(),"KB", file=log)
input_filename = sys.argv[1]

city2ind={}
ind2city={}
countid1=0

tr2ind={}
ind2tr={}
countid2=0

graph={}

with open(input_filename) as input_file:
    deli = "\""
    for line in input_file:
        line=line.rstrip()
        if len(line)==0 or line[0]=="#": continue
        n1=0
        n2=line.find(deli)
        n1=n2+1
        n2=line.find(deli,n1)
        from_city=line[n1:n2]
        n1=n2+1
        n2=line.find(deli,n1)
        n1=n2+1
        n2=line.find(deli,n1)
        to_city=line[n1:n2]
        n1=n2+1
        n2=line.find(deli,n1)
        n1=n2+1
        n2=line.find(deli,n1)
        transport_type=line[n1:n2]
        n1=n2+2
        numline=line[n1:].split()
        cruise_time=int(numline[0])
        cruise_fare=int(numline[1])
        id_from=0
        id_to=0
        id_tr=0
        if (from_city in city2ind): id_from=city2ind[from_city]
        else:
            id_from=countid1
            city2ind[from_city]=countid1
            ind2city[countid1]=from_city
            countid1+=1
        if (to_city in city2ind): id_to=city2ind[to_city]
        else:
            id_to=countid1
            city2ind[to_city]=countid1
            ind2city[countid1]=to_city
            countid1+=1
        if (transport_type in tr2ind): id_tr=tr2ind[transport_type]
        else:
            id_tr=countid2
            tr2ind[transport_type]=countid2
            ind2tr[countid2]=transport_type
            countid2+=1
        ed = edge(id_from, id_to, id_tr, cruise_time, cruise_fare)
        if id_from in graph:
            if id_to in graph[id_from]:
                graph[id_from][id_to].append(ed)
            else:
                graph[id_from][id_to]=[ed]
        else:
            graph[id_from]={}
            graph[id_from][id_to]=[ed]
print("after graph uploading max rss =" ,get_rss(),"KB", file=log)
print("================", file=log)
log.close()

stdscr = curses.initscr()
stdscr.scrollok(True)
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
while(1): #Основной цикл программы
    curses.noecho()
    curses.curs_set(0)
    mode=0
    chosen=False
    choices = ["Найти кратчайший по времени путь (и самый дешевый из них)",
        "Найти путь минимальной стоимости (и самый быстрый из них)",
        "Найти путь с наименьшим числом пересадок",
        "Найти города, достижимые за заданное количество денег",
        "Найти города, достижимые за заданное время",
        "EXIT"]
    
    while not chosen:
        stdscr.clear()
        stdscr.keypad(True)
        stdscr.addstr("Выберите режим работы\n\n")
        stdscr.refresh()
        for i in range(6):
            if (i==5) and (i!=mode):
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(choices[i]+'\n')
                stdscr.attroff(curses.color_pair(2))
            elif (i==5) and (i==mode):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(choices[i]+'\n')
                stdscr.attroff(curses.color_pair(1))
            elif (i==mode):
                stdscr.attron(curses.A_STANDOUT)
                stdscr.addstr(choices[i]+'\n')
                stdscr.attroff(curses.A_STANDOUT)
            else:
                stdscr.addstr(choices[i]+'\n')
            stdscr.refresh()
        ch=stdscr.getch()
        if ch==curses.KEY_UP:
            if mode>0: mode-=1
        elif ch==curses.KEY_DOWN:
            if mode<5: mode+=1
        elif ch in [curses.KEY_ENTER, 10, 13]:
            chosen=True
    if mode==5: break
    en_transp=set()
    tp=0
    chosen=False
    choices_tr = ["Ввести виды транспорта, на которых разрешено ехать",
        "Ввести виды транспорта на которых запрещено ехать",
        "Нет ограничений на виды транспорта",
        "Назад в меню"]
    while not chosen:
        stdscr.clear()
        stdscr.keypad(True)
        curses.curs_set(0)
        stdscr.addstr("Выберите режим фильтрации транспорта\n\n")
        stdscr.refresh()
        for i in range(4):
            if (i==tp):
                stdscr.attron(curses.A_STANDOUT)
                stdscr.addstr(choices_tr[i]+'\n')
                stdscr.attroff(curses.A_STANDOUT)
            else:
                stdscr.addstr(choices_tr[i]+'\n')
            stdscr.refresh()
        ch=stdscr.getch()
        if ch==curses.KEY_UP:
            if tp>0: tp-=1
        elif ch==curses.KEY_DOWN:
            if tp<3: tp+=1
        elif ch in [curses.KEY_ENTER, 10, 13]:
            chosen=True
    stdscr.clear()
    if (tp==3): continue
    if (tp==0):
        curses.curs_set(1)
        stdscr.addstr("Введите названия разрешенных видов транспорта со строчной буквы через Enter\n")
        stdscr.addstr("По окончании нажмите дважды Enter\n")
        curses.echo()
        trtype = str(stdscr.getstr(), 'utf-8', errors='ignore')
        while(1):
            if (trtype==""): break
            if (trtype in tr2ind):
                en_transp.add(tr2ind[trtype])
            else:
                stdscr.addstr("Не найден данный вид транспорта. Продолжайте ввод\n")
            trtype = str(stdscr.getstr(), 'utf-8', errors='ignore')
    elif (tp==1):
        curses.curs_set(1)
        stdscr.keypad(True)
        zapr=set()
        stdscr.addstr("Введите названия запрещенных видов транспорта со строчной буквы через Enter\n")
        stdscr.addstr("По окончании нажмите дважды Enter\n")
        curses.echo()
        trtype = str(stdscr.getstr(), 'utf-8', errors='ignore')
        while(1):
            if (trtype==""): break
            if (trtype in tr2ind):
                zapr.add(tr2ind[trtype])
            else:
                stdscr.addstr("Не найден данный вид транспорта. Продолжайте ввод\n")
            trtype = str(stdscr.getstr(), 'utf-8', errors='ignore')
        for key, value in ind2tr.items():
            if key not in zapr: en_transp.add(key)
        del zapr
    else:
        for key,value in ind2tr.items():
            en_transp.add(key)
    stdscr.keypad(False)
    stdscr.clear()
    stdscr.addstr("Введите город отправления\n")
    curses.curs_set(1)
    curses.echo()
    stdscr.keypad(True)
    while(1):
        fr = str(stdscr.getstr(), 'utf-8', errors='ignore')
        flag=False
        from_id=0
        if (fr in city2ind):
            from_id=city2ind[fr]
            flag=True
        if flag: break
        stdscr.addstr("Такого города не найдено в базе данных. ")
        stdscr.addstr("Введите другой город\n")
    if mode==0: # 1 РЕЖИМ
        stdscr.addstr("Введите город прибытия\n")
        while(1):
            to = str(stdscr.getstr(), 'utf-8', errors='ignore')
            flag=False
            to_id=0
            if (to in city2ind):
                to_id = city2ind[to]
                flag = True
            if ((to_id == from_id) and (flag==True)):
                stdscr.addstr("Город прибытия совпадает с городом отправления. ")
                stdscr.addstr("Введите другой город\n")
                continue
            if (flag==True): break
            stdscr.addstr("Такого города не найдено в базе данных. ")
            stdscr.addstr("Введите другой город\n")
        begin_time = time_ns()
        res = algo1(graph, countid1, en_transp, from_id)
        cruise = track([])
        curver = to_id
        while (curver!=from_id):
            if (curver not in res): break
            cruise=cruise+res[curver]
            curver=res[curver].fr
        end_time = time_ns()
        elapsed = end_time - begin_time
        stdscr.addstr("\n")
        print_track(stdscr, cruise, ind2tr, ind2city)
        log = open(logname, 'a')
        print("calling algorithm 1", file=log, end=" ")
        print("algo time elapsed",elapsed/1000,"mcs", file=log, end=" | ")
        print("max rss =",get_rss(),"KB", file=log)
        log.close()
    elif mode==1: # 2 РЕЖИМ
        stdscr.addstr("Введите город прибытия\n")
        while(1):
            to = str(stdscr.getstr(), 'utf-8', errors='ignore')
            flag=False
            if (to in city2ind):
                to_id = city2ind[to]
                flag = True
            if ((to_id == from_id) and (flag==True)):
                stdscr.addstr("Город прибытия совпадает с городом отправления. ")
                stdscr.addstr("Введите другой город\n")
                continue
            if (flag==True): break
            stdscr.addstr("Такого города не найдено в базе данных. ")
            stdscr.addstr("Введите другой город\n")
        begin_time = time_ns()
        res = algo2(graph, countid1, en_transp, from_id)
        cruise = track([])
        curver = to_id
        while (curver!=from_id):
            if (curver not in res): break
            cruise=cruise+res[curver]
            curver=res[curver].fr
        end_time = time_ns()
        elapsed = end_time - begin_time
        stdscr.addstr("\n")
        print_track(stdscr, cruise, ind2tr, ind2city)
        log = open(logname, 'a')
        print("calling algorithm 2", file=log, end=" ")
        print("algo time elapsed",elapsed/1000,"mcs", file=log, end=" | ")
        print("max rss =",get_rss(),"KB", file=log)
        log.close()
    elif mode==2: # 3 РЕЖИМ
        stdscr.addstr("Введите город прибытия\n")
        while(1):
            to = str(stdscr.getstr(), 'utf-8', errors='ignore')
            flag=False
            if (to in city2ind):
                to_id = city2ind[to]
                flag = True
            if ((to_id == from_id) and (flag==True)):
                stdscr.addstr("Город прибытия совпадает с городом отправления. ")
                stdscr.addstr("Введите другой город\n")
                continue
            if (flag==True): break
            stdscr.addstr("Такого города не найдено в базе данных. ")
            stdscr.addstr("Введите другой город\n")
        begin_time = time_ns()
        res = algo3(graph, countid1, en_transp, from_id)
        cruise = track([])
        curver = to_id
        while (curver!=from_id):
            if (curver not in res): break
            cruise=cruise+res[curver]
            curver=res[curver].fr
        end_time = time_ns()
        elapsed = end_time - begin_time
        stdscr.addstr("\n")
        print_track(stdscr, cruise, ind2tr, ind2city)
        log = open(logname, 'a')
        print("calling algorithm 3", file=log, end=" ")
        print("algo time elapsed",elapsed/1000,"mcs", file=log, end=" | ")
        print("max rss =",get_rss(),"KB", file=log)
        log.close()
    elif mode==3: # 4 РЕЖИМ
        ifcity=False
        stdscr.addstr("Введите максимальную стоимость поездки руб ")
        maxcost = int(str(stdscr.getstr(), 'utf-8', errors='ignore'))
        stdscr.addstr("\n")
        begin_time=time_ns()
        end_time=time_ns()
        elapsed=end_time-begin_time
        begin_time=time_ns()
        res = algo4(graph, countid1, en_transp, from_id, maxcost)
        i=0
        while (i<countid1):
            if i not in res:
                i+=1
                continue
            ifcity=True
            cruise=track([])
            curver=i
            while curver!=from_id:
                if curver not in res: break
                cruise=cruise+res[curver]
                curver=res[curver].fr
            end_time=time_ns()
            elapsed+=end_time-begin_time
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(ind2city[i])
            stdscr.attroff(curses.color_pair(3))
            stdscr.addstr('\n')
            print_track(stdscr, cruise, ind2tr, ind2city)
            stdscr.addstr("\n\n")
            begin_time = time_ns()
            i+=1
        end_time = time_ns()
        elapsed+=end_time-begin_time
        if not ifcity: stdscr.addstr("Таких городов нет\n\n")
        else: stdscr.addstr("===============Конец==============\n\n")
        log = open(logname, 'a')
        print("calling algorithm 4", file=log, end=" ")
        print("algo time elapsed",elapsed/1000,"mcs", file=log, end=" | ")
        print("max rss =",get_rss(),"KB", file=log)
        log.close
    else: # 5 РЕЖИМ
        ifcity=False
        stdscr.addstr("Введите максимальное время поездки, мин ")
        maxtime = int(str(stdscr.getstr(), 'utf-8', errors='ignore'))
        stdscr.addstr("\n")
        begin_time=time_ns()
        end_time=time_ns()
        elapsed=end_time-begin_time
        begin_time=time_ns()
        res = algo5(graph, countid1, en_transp, from_id, maxtime)
        i=0
        while (i<countid1):
            if i not in res:
                i+=1
                continue
            ifcity=True
            cruise=track([])
            curver=i
            while curver!=from_id:
                if curver not in res: break
                cruise=cruise+res[curver]
                curver=res[curver].fr
            end_time=time_ns()
            elapsed+=end_time-begin_time
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(ind2city[i])
            stdscr.attroff(curses.color_pair(3))
            stdscr.addstr('\n')
            print_track(stdscr, cruise, ind2tr, ind2city)
            stdscr.addstr("\n\n")
            begin_time = time_ns()
            i+=1
        end_time = time_ns()
        elapsed+=end_time-begin_time
        if not ifcity: stdscr.addstr("Таких городов нет\n\n")
        else: stdscr.addstr("===============Конец==============\n\n")
        log = open(logname, 'a')
        print("calling algorithm 5", file=log, end=" ")
        print("algo time elapsed",elapsed/1000,"mcs", file=log, end=" | ")
        print("max rss =",get_rss(),"KB", file=log)
        log.close()
    stdscr.addstr("\n")
    stdscr.addstr("Для продолжения нажмите любую клавишу\n")
    stdscr.getch()
curses.endwin()
log.close()
