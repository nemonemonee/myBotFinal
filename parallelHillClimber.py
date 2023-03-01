from solution import SOLUTION
import constants as c
import copy
import os
import numpy

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.nndf")
        self.nextAvailableID = 0
        self.parents = dict()
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.fitnessRecords = numpy.zeros((c.populationSize, c.numberOfGenerations))
        self.lr = 0.5
        

    def Evolve(self):
        #print("start evolve")
        self.Evaluate(self.parents)
        #self.fitnessRecords = {_:[self.parents[_].fitness] for _ in range(c.populationSize)}
        for self.currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            self.lr -= 0.004
        
    
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
            if self.currentGeneration % 2 == 1:
                self.children[i].MutateBody(self.lr)
            else:
                self.children[i].MutateBrain(self.lr)
        
    def Select(self):
        for i in self.parents:
            print(self.parents[i].fitness, self.children[i].fitness)
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]
            self.fitnessRecords[i, self.currentGeneration] = self.parents[i].fitness
        print("Generation#{}".format(self.currentGeneration))
       
    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")
            
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()
        
        
        
    def Show_Best(self):
        t = 0
        print(self.fitnessRecords)
        numpy.save("fitData.npy", self.fitnessRecords)
        for i in self.parents:
            self.parents[i].Start_Simulation("GUI")

