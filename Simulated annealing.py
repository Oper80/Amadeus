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

def to_id(m):
    a = []
    for x in m:
        a.append(x.id)
    return a    

def planet_own(p, ad = 0):
    if p.my_units + ad > p.other_units: return 1
    if p.my_units + ad < p.other_units: return -1
    if p.my_units + ad == p.other_units: return 0
    
def neig_count(p):
    count = 0
    for x in planet_neig[p.id]:
        f = all_planet[x]
        if planet_own(f) >= 0:
            count += 1
        
    return count
    
def move_eff(m):
    planets = 0
    my_edge = 0
    s = set(m)
    for i in s:
        if planet_own(i) < 1 and planet_own(i, m.count(i)) > 0:
            planets += 1
    return planets + my_edge    

def mut(m):
    r = random.randint(0,4)
    m[r] = random.choice(valid_planet)
    return m
        
my_planets = 0    
edges = []
planet_count, edge_count = [int(i) for i in input().split()]
for i in range(edge_count):
    edges.append(list(map(int, input().split())))
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
    
    for i in range(planet_count):
        my_units, my_tolerance, other_units, other_tolerance, can_assign = [int(j) for j in input().split()]
        temp = Planet(i, my_units, my_tolerance, other_units, other_tolerance, can_assign)
        all_planet[i] = temp
        print(temp.id,planet_own(temp),file=sys.stderr)
        if temp.can_assign and planet_own(temp) < 1:
            valid_planet.append(temp)
            print(len(valid_planet),file=sys.stderr)
    
    default_planet = all_planet[0]        
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    i = 5
    now = time.perf_counter()
    best_score = 0
    best_move = []
    l = len(valid_planet)
    move = []
    for i in range(5):
        try:
            move.append(random.choice(valid_planet))
            best_move.append(random.choice(valid_planet))
            print(1,file=sys.stderr)
        except (IndexError):
            move.append(default_planet)
            best_move.append(default_planet)
            print(2,file=sys.stderr)
    print(3,file=sys.stderr)
    
    while now - loop_start < 0.0004:
        #print("1",file=sys.stderr)
        move_score = move_eff(move)
        if move_score > best_score:
            best_score = move_score
            best_move = move[:]
            move = mut(move)
            now = time.perf_counter()
           
    print(*to_id(best_move), sep="\n")    
    print("NONE")
