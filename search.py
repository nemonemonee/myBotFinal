import os
#from parallelHillClimber import PARALLEL_HILL_CLIMBER
from solution import SOLUTION

os.system("rm brain*.nndf")
os.system("rm fitness*.nndf")
for i in range(10):
    s = SOLUTION(0)
    s.Start_Simulation("GUI")
#phc = PARALLEL_HILL_CLIMBER()
#phc.Evolve()
#phc.Show_Best()
