from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.nndf")
        self.nextAvailableID = 0
        self.parents = dict()
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        
    
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Select()
    
    def Spawn(self):
        self.children = dict()
        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[0])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

        
    
    def Mutate(self):
        for i in self.children:
            self.children[i].Mutate()
        
    def Select(self):
        for i in self.parents:
            print(self.parents[i].fitness, self.children[i].fitness)
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]
            print()
       
    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")
            
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()
        
        
        
    def Show_Best(self):
        t = 0
        for i in self.parents:
            if self.parents[i].fitness < self.parents[t].fitness:
                t = i
        self.parents[t].Start_Simulation("GUI")

