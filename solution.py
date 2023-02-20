import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
class SOLUTION:
    def __init__(self, id):
        self.myID = id
        
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
        self.InitializeRandomVariables()
        self.curr_pos = numpy.array([0.,0.,self.size[0,2]*.5+.1])
        pyrosim.Send_Cube(name="0", pos=self.curr_pos, size=self.size[0], colorName=self.GetColor(0)[0], colorString=self.GetColor(0)[1])
        center2pivot = numpy.random.randint(-1,2,3)
        self.curr_pos += (self.size[0] + self.size[1]) * 0.5 * center2pivot
        self.BottomDetection(1, center2pivot)
        pyrosim.Send_Joint(name="0_1", parent="0", child="1", type="revolute", position=self.curr_pos-self.size[1]*0.5*center2pivot, jointAxis = "1 1 1")
        pyrosim.Send_Cube(name="1", pos=self.size[1]*0.5*center2pivot, size=self.size[1], colorName=self.GetColor(1)[0], colorString=self.GetColor(1)[1])
        pivot2center = center2pivot
        for i in range(2, self.length):
            center2pivot = self.Grow(pivot2center)
            self.curr_pos += (self.size[i-1] + self.size[i]) * 0.5 * center2pivot
            self.BottomDetection(i, center2pivot)
            pivot2pivot = (center2pivot + pivot2center) * 0.5
            pyrosim.Send_Joint(name=str(i-1)+"_"+str(i), parent=str(i-1) , child=str(i), type="revolute", position=self.size[i-1]*pivot2pivot, jointAxis="1 1 1")
            pyrosim.Send_Cube(name=str(i), pos=self.size[i]*0.5*center2pivot, size=self.size[i], colorName=self.GetColor(i)[0], colorString=self.GetColor(i)[1])
            pivot2center = center2pivot
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
    
    
    # It takes in the previous growing direction and decides the next one
    def Grow(self, prev_dir):
        dir = prev_dir.copy()
        for i, j in enumerate(dir):
            dir[i] = self.GrowAxis(j)
        if numpy.sum(numpy.abs(dir)) == 0:
            dir = prev_dir.copy()
        return dir
    
    # It decides the growing direction in one axis
    def GrowAxis(self, v):
        if v == 0:
            v = numpy.random.choice([-1,0,1], 1)
        elif v == 1:
            v = numpy.random.choice([0,1], 1)
        else:
            v = numpy.random.choice([-1,0], 1)
        return v
        
    # Initialize the random variables for the robots including
    #  - the length of the limb
    #  - whether each cube has a sensor
    #  - the size of each cube
    # Then it will calculate the the number of sensors and motors, and intialize a
    #  weight matrix based on those numbers.
    def InitializeRandomVariables(self):
        self.length = 2 + numpy.random.randint(10)
        self.sensorOrNot = numpy.random.rand(self.length) < 0.5
        self.size = .1 + numpy.random.rand(self.length, 3)
        self.numSensorNeurons = numpy.sum(self.sensorOrNot)
        self.numMotorNeurons = self.length
        self.weights = numpy.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
    
    
    # It takes in the index of the cube
    # It decides the color based on if the cube has a sensor or not
    # It returns the color string and color name of the given cube
    def GetColor(self, idx):
        if self.sensorOrNot[idx]:
            return "Green", '    <color rgba="0 1.0 0 1.0"/>'
        else :
            return "Blue", '    <color rgba="0 0 1.0 1.0"/>'
    
    # check if the cube is itersecting with the ground if so lift the cube up
    def BottomDetection(self, idx, dir):
        bottom = (self.curr_pos - 0.5 * self.size[idx])[2]
        self.curr_pos -= self.size[idx] * 0.5 * dir
        while bottom < 0:
            dir[2] += 1
            bottom += 0.5 * self.size[idx,2]
        self.ZeroDrtection(dir)
        self.curr_pos += self.size[idx] * 0.5 * dir
        
    def ZeroDrtection(self, dir):
        if numpy.sum(numpy.abs(dir)) == 0:
            dir[2] = 1
    
    def Mutate(self):
        randomRow = random.randint(0, self.numSensorNeurons - 1)
        randomColumn = random.randint(0, self.numMotorNeurons - 1)
        self.weights[randomRow,randomColumn] = numpy.random.rand() * 2 - 1
        
    def Set_ID(self, id):
        self.myID = id

