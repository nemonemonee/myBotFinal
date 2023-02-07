import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
class SOLUTION:
    def __init__(self, id):
        self.myID = id
        self.weights = numpy.random.rand(c.numSensorNeurons,c.numMotorNeurons) * 2 - 1
        
        
    def Evaluate(self):
        self.Start_Simulation()
        self.Wait_For_Simulation_To_End()
    
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py "+directOrGUI+" "+str(self.myID)+" &")
        
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
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5] , size=[1,3,1])
        
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [-0.5,1,1.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0,-0.25] , size=[0.2,0.2,0.5])
        
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.5,1,1.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,0,-0.25] , size=[0.2,0.2,0.5])
        
        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5,-1,1.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[0,0,-0.25] , size=[0.2,0.2,0.5])
        
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5,-1,1.5], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0,0,-0.25] , size=[0.2,0.2,0.5])
        
        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0,0,-0.25], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        
        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0,0,-0.25], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        
        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [0,0,-0.25], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [0,0,-0.25], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "RightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "RightLeg_RightLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "BackLeg_BackLowerLeg")
        
        for i in range(c.numSensorNeurons):
            for j in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = i, targetNeuronName = j + c.numSensorNeurons, weight = self.weights[i][j])
        pyrosim.End()
        
    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow,randomColumn] = numpy.random.rand() * 2 - 1
        
    def Set_ID(self, id):
        self.myID = id
