import sys
import math
import time
import random

class Planet:
    def __init__(self, id, my_units, my_tolerance, other_units, other_tolerance, can_assign):
        self.id = id
        self.my_units = my_units
        self.my_tolerance = my_tolerance
        self.other_units = other_units
        self.other_tolerance = other_tolerance
        self.can_assign = can_assign
        self.priority = 0
        
    def enemy_dist(self):
        l = []
        q = []
        l.append(0)
        q.append(self.id)
        i = 0
        start = 0
        
        while all_planet[q[start]].own() >= 0:
            for x in planet_neig[q[start]]:
                if x not in q: 
                    q.append(x)
                    l.append(l[start]+1)
            if start < planet_count - 1: 
                #print(start,planet_count,file=sys.stderr)
                start += 1
            else: return l[start]    
            #print(start,file=sys.stderr)
        return l[start]
        
    
    def enemy_count(self):
        count = 0
        for x in planet_neig[self.id]:
            f = all_planet[x]
            if f.own() == -1:
                count += 1
        return count
    
    def cost(self):
        return self.other_units - self.my_units - (self.my_count() - self.enemy_count())*2
    
    def my_count(self):
        count = 0
        for x in planet_neig[self.id]:
            f = all_planet[x]
            if f.own() == 1:
                count += 1
        return count
    
    def own(self, ad = 0):
        if self.my_units + ad > self.other_units: return 1
        if self.my_units + ad < self.other_units: return -1
        if self.my_units + ad == self.other_units: return 0
    
    def set_priority():
        pass
    
def to_id(m):
    a = []
    for x in m:
        a.append(x.id)
    return a    
    
        
my_planets = 0    
edges = []
planet_count, edge_count = [int(i) for i in input().split()]
for i in range(edge_count):
    edges.append(list(map(int, input().split())))

#Dict of planets: list of neighbors
planet_neig = dict()
for i in edges:
    if planet_neig.get(i[0]):
        planet_neig[i[0]] = planet_neig.get(i[0]) + [i[1]]
    else: 
        planet_neig[i[0]] = [] + [i[1]]
    if planet_neig.get(i[1]):
        planet_neig[i[1]] = planet_neig.get(i[1]) + [i[0]]   
    else: planet_neig[i[1]] = [] + [i[0]] 
    
#3print(planet_neig,file = sys.stderr)    
all_planet = []
valid_planet = []
# game loop
while True:
    loop_start = time.perf_counter()
    valid_planet = []
    all_planet = dict()
    default_planet = False
    en_valid_planet = []
    for i in range(planet_count):
        my_units, my_tolerance, other_units, other_tolerance, can_assign = [int(j) for j in input().split()]
        temp = Planet(i, my_units, my_tolerance, other_units, other_tolerance, can_assign)
        all_planet[i] = temp
        if temp.can_assign: #and temp.own() < 1
            valid_planet.append(temp)
    a=valid_planet[0].enemy_count()    
    for i in valid_planet:
        if i.enemy_dist() == 1 and i.other_tolerance > 0: en_valid_planet.append(i)
        if i.own() < 1: default_planet = i
    en_valid_planet.sort(key=lambda x: (x.my_count()))    
    
    #valid_planet.sort(key=lambda x: (x.enemy_dist(),x.enemy_count(),x.cost()))
    
    #valid_planet.sort(key=lambda x: ((x.my_count()+x.enemy_count()),x.cost(),x.enemy_dist()))
    
    valid_planet.sort(key=lambda x: (x.enemy_count(),x.cost(),x.enemy_dist()))
    
    if default_planet == False: 
        default_planet = all_planet[0]
    v_id = []
    score_planets = []
    for i in valid_planet: 
        if i.own() < 1:
            score_planets.append(i)
            v_id.append(i)
    #print (*v_id, '!',len(valid_planet),file = sys.stderr)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    spread = 'NONE'
    move=[]
    now = time.perf_counter()
    cnt = len(score_planets)
    for x in score_planets:
        dop = x.enemy_count() - x.my_count() if (x.enemy_count() - x.my_count()) > 0 else 1
        r = x.other_units - x.my_units + dop +1
        #print('r', r, file=sys.stderr)
        if r < 1 and len(move) < 5: 
            move.append(x.id)
        else:
            for i in range(r):
                if len(move) < 5: 
                    move.append(x.id)
        if x.my_units - x.other_units > 5 and x.enemy_dist() > 1: 
            spread = x.id
    while len(move) < 5:
        move.append(default_planet.id)
          
    print(*move, sep="\n")   
    print(spread)
