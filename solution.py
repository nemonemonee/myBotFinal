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
        if directOrGUI=="GUI":
            os.system("python3 simulate.py "+directOrGUI+" "+str(self.myID))
        else:
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
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        self.InitializeRandomVariables()
        
        self.BuildBodyPlan()
        self.ArrangementPlan()
        
        self.curr_pos = numpy.array([0.,0.,self.size[0,2]*.5+.1])
        pyrosim.Send_Cube(name="0", pos=self.curr_pos, size=self.size[0], colorName=self.GetColor(0)[0], colorString=self.GetColor(0)[1])
        
        
#        allDir = {0:(1,0,0), 1:(0,1,0), 2:(0,0,1),
#                  3:(0,0,-1), 4:(0,-1,0), 5:(-1,0,0)}
        allDir = {0:numpy.array([1,0,0]), 1:numpy.array([0,1,0]), 2:numpy.array([0,0,1]),
                  3:numpy.array([0,0,-1]), 4:numpy.array([0,-1,0]), 5:numpy.array([-1,0,0])}
       # center2pivot = allDir[growDir[0]]
        
#        center2pivot = numpy.random.randint(-1,2,3)
       # self.curr_pos += (self.size[0] + self.size[1]) * 0.5 * center2pivot

        for j in self.bodyPlan[0]:
            center2pivot = allDir[self.growDir[j]]
            pyrosim.Send_Joint(name="0_"+str(j), parent="0", child=str(j), type="revolute", position=self.curr_pos+self.size[0]*0.5*center2pivot, jointAxis = "1 1 1")
            pyrosim.Send_Cube(name=str(j), pos=self.size[j]*0.5*center2pivot, size=self.size[j], colorName=self.GetColor(j)[0], colorString=self.GetColor(j)[1])
        
        
        for i in range(1, len(self.bodyPlan)):
            pivot2center = allDir[self.growDir[i]]
            for j in self.bodyPlan[i]:
                center2pivot = allDir[self.growDir[j]]
                pivot2pivot = (center2pivot + pivot2center) * 0.5
                pyrosim.Send_Joint(name=str(i)+"_"+str(j), parent=str(i), child=str(j), type="revolute", position=self.size[i]*pivot2pivot, jointAxis="1 1 1")
                pyrosim.Send_Cube(name=str(j), pos=self.size[j]*0.5*center2pivot, size=self.size[j], colorName=self.GetColor(j)[0], colorString=self.GetColor(j)[1])
    
        
        pyrosim.End()
#        print("body finished")
#        self.BottomDetection(1, center2pivot)
#        pyrosim.Send_Joint(name="0_1", parent="0", child="1", type="revolute", position=self.curr_pos-self.size[1]*0.5*center2pivot, jointAxis = "1 1 1")
#        pyrosim.Send_Cube(name="1", pos=self.size[1]*0.5*center2pivot, size=self.size[1], colorName=self.GetColor(1)[0], colorString=self.GetColor(1)[1])
#        pivot2center = center2pivot
#        for i in range(2, self.length):
#            center2pivot = self.Grow(pivot2center)
#            self.curr_pos += (self.size[i-1] + self.size[i]) * 0.5 * center2pivot
#            self.BottomDetection(i, center2pivot)
#            pivot2pivot = (center2pivot + pivot2center) * 0.5
#            pyrosim.Send_Joint(name=str(i-1)+"_"+str(i), parent=str(i-1) , child=str(i), type="revolute", position=self.size[i-1]*pivot2pivot, jointAxis="1 1 1")
#            pyrosim.Send_Cube(name=str(i), pos=self.size[i]*0.5*center2pivot, size=self.size[i], colorName=self.GetColor(i)[0], colorString=self.GetColor(i)[1])
#            pivot2center = center2pivot
        

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        k = 0
        for i in range(self.length):
            if (self.sensorOrNot[i]):
                pyrosim.Send_Sensor_Neuron(name = k, linkName = str(i))
                k += 1
        for i in range(self.length):
            for j in self.bodyPlan[i]:
                pyrosim.Send_Motor_Neuron(name = k, jointName = str(i)+"_"+str(j))
                k += 1
        for i in range(self.numSensorNeurons):
            for j in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = i, targetNeuronName = j + self.numSensorNeurons, weight = self.weights[i][j])
        pyrosim.End()
        #print("brain finished")
    
        
    # Initialize the random variables for the robots including
    #  - the length of the limb
    #  - whether each cube has a sensor
    #  - the size of each cube
    # Then it will calculate the the number of sensors and motors, and intialize a
    #  weight matrix based on those numbers.
    def InitializeRandomVariables(self):
        self.length = 2 + numpy.random.randint(10)
        self.sensorOrNot = numpy.random.rand(self.length) < 0.5
        if numpy.sum(self.sensorOrNot) == 0: self.sensorOrNot[0] = True
        self.size = .1 + numpy.random.rand(self.length, 3)
        self.numSensorNeurons = numpy.sum(self.sensorOrNot)
        self.numMotorNeurons = self.length
        self.weights = numpy.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1
    
    def BuildBodyPlan(self):
        self.bodyPlan = {0:[1], 1:[]}
        potentialParent = [0, 1]
        for i in range(2, self.length):
          pre_i = numpy.random.choice(potentialParent)
          self.bodyPlan[pre_i].append(i)
          if len(self.bodyPlan[pre_i]) >= 4: potentialParent.remove(pre_i)
          potentialParent.append(i)
          self.bodyPlan[i] = []
    
    def ArrangementPlan(self):
        self.growDir = {}
        remainDir = {_:list(range(6)) for _ in range(self.length)}
        remainDir[0].remove(3)
        for i in range(len(self.bodyPlan)):
           for j in self.bodyPlan[i]:
             d = numpy.random.choice(remainDir[i])
             remainDir[i].remove(d)
             remainDir[j].remove(5-d)
             self.growDir[j] = d
    
    
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
    
    def MutateBrain(self, lr):
        n_i = int(max(1, numpy.floor(self.numSensorNeurons * lr)))
        n_j = int(max(1, numpy.floor(self.numMotorNeurons * 0.25)))
        i_s = numpy.random.choice(list(range(self.numSensorNeurons)), n_i)
        j_s = numpy.random.choice(list(range(self.numMotorNeurons)), n_j)
        #randomRow = random.randint(0, self.numSensorNeurons - 1)
        #randomColumn = random.randint(0, self.numMotorNeurons - 1)
        randWeight = numpy.random.rand(n_i, n_j) * 2 - 1
        for i, p in enumerate(i_s):
            for j, q in enumerate(j_s):
                self.weights[p, q] = randWeight[i,j]
                
    def MutateBody(self, lr):
        n = int(max(1,numpy.floor(self.length * lr)))
        idxs = numpy.random.choice(list(range(self.length)), n)
        randSize =  .1 + numpy.random.rand(n, 3)
        self.size[idxs] = randSize
        self.Create_Body()
        
        
    def Set_ID(self, id):
        self.myID = id
        
    def save(self):
        fn = "save" + str(self.myID) + ".nndf"
        with open(fn, 'wb') as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)
