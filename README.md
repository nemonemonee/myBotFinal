# myBotFinal
 
 Credit
  * This project is for cs 396 artificial life in Northwestern University.
  * The project uses the structure from Ludobots.
  * The project uses the pakage of pyrosim.
 
 Task
  * Build a snake like robot with random length of random sized rectangles.
  * Whether one rectangle has a sensor or not is randomly decided.
  * If the rectangle has the sensor, it is colored green. Otherwise, it is colored blue.
  
 My solution
  * I used numpy to randomly choose the length range from 2 to 11.
  * Then I use numpy to randomly decided if each rectangle has a sensor with a probability of 0.5.
  * Then the size for each rectangle is three random number range from 0.5 to 2.5.
  * The position of joint and rectangle is replaced based on the size of each.
  
