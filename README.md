# myBotFinal
 
 Credit
  * This project is for cs 396 artificial life in Northwestern University.
  * The project uses the structure from Ludobots.
  * The project uses the pakage of pyrosim.
 
 Objective
  * Generate robots with randomization.
  * Artificially select among robots, so it learned to move in xy-plane.

 Robot Design
  - Task
    * Build a limb like robot with random length of random sized rectangles.
    * The limb can potentially fill up the 3d space.
    * Whether one rectangle has a sensor or not is randomly decided.
    * If the rectangle has the sensor, it is colored green. Otherwise, it is colored blue.
    
  - Morphology
 ![b480d47df2d9cc7b0e09b923e2014dc](https://user-images.githubusercontent.com/88709397/222052582-df66f0e4-f4b8-437c-8725-8262b651d742.jpg)

    * I used numpy to randomly choose the length range from 2 to 11.
    * Then I use numpy to randomly decided if each rectangle has a sensor with a probability of 0.5.
    * Then the size of each rectangle is decided by three random numbers ranging from 0.1 to 1.1.  
    * For the body plan, I used a tree structure. I added each cube to an available tree node. Each tree node has strictlly no more than 5 children. When the number of children reaches 5, that tree node is no longer considered as available.
    * I assigned the connection direction to each cube and its children. Following the rule that, no two children share the same direction and no child grows below the xy plane.
    * The position of joint and rectangle is placed based on its size and a randomly decided direction.
    * Consider a cube i and its child j. The joint is placed at size[j] * (dir[i] + dir[j]) / 2. Cube j is placed at dir[j] * size[j] / 2. The calculation is using relative position. 
 
   - Brain
   ![c8034c3e1475e85e5a27b3a044494b3](https://user-images.githubusercontent.com/88709397/222052635-e040325e-d7cf-4b26-b9d2-1df43dfd18ab.jpg)

     * All sensor nerons send information to all motor neurons.
     * The weight is random decided, ranging from (-1, 1).
     
 Evolution Plan
  ![IMG_0666](https://user-images.githubusercontent.com/88709397/222330450-2f67e2d1-313a-4087-bb55-98ad5bcccd96.jpg)

   - Mutation
     ![3394c737a60a2f015f5dfebcfbabe0d](https://user-images.githubusercontent.com/88709397/222052701-a674ba4a-2315-4e40-945b-504a57bf1d73.jpg)
     * Each time I update some number of parameters. The number is based on learning rate.
     * For each generation, I either update the body, or I update the brain, or I swap the sensors.
     
   - Selection
     * My objective is to train a robot with the maximum xy-plane movement. Thus, I set the fitness score to be the maximum among the absolute values of the x, y coordinates at the end of each simulation. During the selection process, I always choose the ones with a higher fitness score.
   - Fitness Curve

![Fitscore](https://user-images.githubusercontent.com/88709397/222328421-6799b6fe-fe2a-4e52-a203-8d6267c1c968.png)


 Future Work
    * I am thinking of using more complicated evolution plan such as for each generation we choose the best 50 % and duplicate them. Moreover, ideas such as cross-over can be simulated.
    * Different joints can be used.
