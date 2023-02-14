import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
class SOLUTION:
    def __init__(self, id):
        self.myID = id
        self.length = 2 + numpy.random.randint(10)
        print(self.length)
        self.sensorOrNot = numpy.random.rand(self.length) < 0.5
        self.numSensorNeurons = numpy.sum(self.sensorOrNot)
        self.numMotorNeurons = self.length
        self.weights = numpy.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
        
        
    def Evaluate(self):
        self.Start_Simulation()
        self.Wait_For_Simulation_To_End()
    
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py "+directOrGUI+" "+str(self.myID))#+" &")
        
    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        f = open(fitnessFileName, "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm "+fitnessFileName)
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-5,-5,0.5] , size=[1,1,1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        size_0 = 0.5 + 2 * numpy.random.rand(3)
        cn, cs = [], []
        for i in range(self.length):
            if self.sensorOrNot[i]:
                cn.append("Green")
                cs.append('    <color rgba="0 1.0 0 1.0"/>')
            else :
                cn.append("Blue")
                cs.append('    <color rgba="0 0 1.0 1.0"/>')
        pyrosim.Send_Cube(name="0", pos=[0,0,0.5], size=size_0, colorName = cn[0], colorString = cs[0])
        offset = size_0[1] / 2
        pyrosim.Send_Joint(name = "0_1", parent= "0", child = "1", type = "revolute", position = [0,offset,0.5], jointAxis = "1 1 1")
        size_1 = 0.5 + 2 * numpy.random.rand(3)
        offset = size_1[1] / 2
        pyrosim.Send_Cube(name="1", pos=[0,offset,0] , size=size_1, colorName = cn[1], colorString = cs[1])
        
        for i in range(2, self.length):
            size_i = 0.5 + 2 * numpy.random.rand(3)
            pyrosim.Send_Joint(name = str(i-1)+"_"+str(i) , parent= str(i-1) , child = str(i) , type = "revolute", position = [0,offset*2,0], jointAxis = "1 1 1")
            offset = size_i[1] / 2
            pyrosim.Send_Cube(name=str(i), pos=[0,offset,0] , size=size_i, colorName = cn[i], colorString = cs[i])
            
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        j = 0
        for i in range(self.length):
            if (self.sensorOrNot[i]):
                pyrosim.Send_Sensor_Neuron(name = j, linkName = str(i))
                j += 1
        for i in range(1, self.length):
            pyrosim.Send_Motor_Neuron(name = j, jointName = str(i-1)+"_"+str(i))
            j += 1
        for i in range(self.numSensorNeurons):
            for j in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = i, targetNeuronName = j + self.numSensorNeurons, weight = self.weights[i][j])
        pyrosim.End()
        
    def Mutate(self):
        randomRow = random.randint(0, self.numSensorNeurons - 1)
        randomColumn = random.randint(0, self.numMotorNeurons - 1)
        self.weights[randomRow,randomColumn] = numpy.random.rand() * 2 - 1
        
    def Set_ID(self, id):
        self.myID = id
