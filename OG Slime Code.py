import random
import math
import matplotlib.pyplot as plt
import numpy as np

#general variables
totaltime = 10
timestep = 1
init_rad = 2
length = 50
centre = (length // 2, length // 2)
num_agents = 100
num_cities = 4
inter_rad = 5

#agent and city important variables
city_dict = {}
city_list = []
positions = []
velocities = []

#random city pop and location allocation, where no positions should be inside the initialisation radius
#for i in range(0, num_cities):
   #city_dict[i] = [random.randint(1, 1000), random.choice([random.randint(0, centre[1] - init_rad), random.randint(centre[1] + init_rad, length)]), random.choice([random.randint(0, centre[1] - init_rad), random.randint(centre[1] + init_rad, length)])]
city_dict[0] = [random.randint(1, 1000), 3, 3]
city_dict[1] = [random.randint(1, 1000), 3, 47]
city_dict[2] = [random.randint(1, 1000), 47, 3]
city_dict[3] = [random.randint(1, 1000), 47, 47]
city_list.append(0)
city_list.append(1)
city_list.append(2)
city_list.append(3)
    
#making distance and attraction functions to keep the class a bit tidier
def attraction_velocity(position, attraction, cities):
    x = cities[attraction][1] - position[0]
    y = cities[attraction][2] - position[1]
    x = x / abs(x)
    y = y / abs(y)
    return [x, y]
    
def find_distance(positions1, positions2):
    distance = math.sqrt((positions1[0] - positions2[0])**2 + (positions1[1] - positions2[1])**2)
    return distance
    
#class for the slime agents
class Slime:
    
    def assign_position(self):
        self.position = (round(random.uniform(centre[1] - init_rad, centre[1] + init_rad), 2), round(random.uniform(centre[1] - init_rad, centre[1] + init_rad), 2))
        positions.append(self.position)
        return self.position
    
    #determines the city attraction for a given agent (constant)
    def find_attraction(self):
        difference = []
        for i in city_dict:
            cost = 50 * (math.sqrt((abs(self.position[0] - city_dict[i][1])**2) + (abs(self.position[1] - city_dict[i][2])**2)))
            gain = city_dict[i][0] * 2500
            difference.append(gain / cost)
        total = sum(difference)
    
        count = 0
        for i in range(0, len(difference)):
            difference[i] = difference[count] / total
            count += 1
        self.attraction = np.random.choice(city_list, p = difference)
        return self.attraction
        
    #randomly assigns a float value of velocity (x, y) between -1 and 1, as I don't want particles moving more than this per timestep
    def assign_velocity(self):
        self.velocity = (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        return self.velocity

def find_neighbourhood_velocity(agent, agents):
    for agent in agents:
        avg_velocity = [0, 0]
        count = 0
        if find_distance(agents[agents.index(agent)][0], agent[0]) <= inter_rad:
            count += 1
            avg_velocity[0] += agent[1][0]
            avg_velocity[1] += agent[1][1]
            
        if count > 0:
            avg_velocity[0] += avg_velocity[0] / count
            avg_velocity[1] += avg_velocity[1] / count
        else:
            avg_velocity[0] = 0
            avg_velocity[1] = 0
        return avg_velocity        

def update_position(position, velocity, attraction, avg_velocity, cities):
    movement = [0, 0]
    velo_temp = [velocity[0], velocity[1]]
    movement[0] = float(position[0]) + float(velocity[0])
    movement[1] = float(position[1]) + float(velocity[1])
    position = movement
    
    denom0 = velo_temp[0] + attraction_velocity(position, attraction, cities)[0] + avg_velocity[0]
    denom1 = velo_temp[1] + attraction_velocity(position, attraction, cities)[1] + avg_velocity[1]
    velo_temp[0] = (velo_temp[0] + random.uniform(0.5, 1) * attraction_velocity(position, attraction, cities)[0] + random.uniform(0, 0.5) * avg_velocity[0]) / denom0
    velo_temp[1] = (velo_temp[1] + random.uniform(0.5, 1) * attraction_velocity(position, attraction, cities)[1] + random.uniform(0, 0.5) * avg_velocity[1]) / denom1
    velocity = (velo_temp[0], velo_temp[1])
    return [position, velocity]
    
#Creating all the agents and storing them into a list
agents = []
for agent in range(num_agents):
    agent = Slime()
    agents.append([agent.assign_position(), agent.assign_velocity(), agent.find_attraction(), 0])

def update_other(agents):
    for agent in agents:
        agent[3] = find_neighbourhood_velocity(agent, agents)

update_other(agents)
        
plt.xlim(0, 50)
plt.ylim(0, 50)
plt.title("Initialisation of Slime")
plt.xlabel("x axis")
plt.ylabel("y axis")
for city in city_dict:
    x = city_dict[city][1]
    y = city_dict[city][2]
    plt.plot(x, y, marker = 'o', markersize = 10, markerfacecolor = 'green')
for agent in agents:
    x = agent[0][0]
    y = agent[0][1]
    plt.plot(x, y, marker = 'o', markersize = 2, markerfacecolor = 'red')
plt.grid()
plt.show()    

for time in range(0, totaltime):
    for agent in agents:
        plt.xlim(0, 50)
        plt.ylim(0, 50)
        plt.title("Timestep {} of slime".format(time))
        plt.xlabel("x axis")
        plt.ylabel("y axis")
        agents[agents.index(agent)][0] = update_position(agent[0], agent[1], agent[2], agent[3], city_dict)[0]
        agents[agents.index(agent)][1] = update_position(agent[0], agent[1], agent[2], agent[3], city_dict)[1]
       # update_other(agents)
        x = agent[0][0]
        y = agent[0][1]
        plt.plot(x, y, marker = 'o', markersize = 2, markerfacecolor = 'red')
        
    for city in city_dict:
        x = city_dict[city][1]
        y = city_dict[city][2]
        plt.plot(x, y, marker = 'o', markersize = 10, markerfacecolor = 'green')
        
    plt.grid()
    plt.show()
    time += timestep
    
