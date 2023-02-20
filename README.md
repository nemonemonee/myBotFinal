# myBotFinal
 
 Credit
  * This project is for cs 396 artificial life in Northwestern University.
  * The project uses the structure from Ludobots.
  * The project uses the pakage of pyrosim.
 
 Task
  * Build a limb like robot with random length of random sized rectangles.
  * The limb can potentially fill up the 3d space.
  * Whether one rectangle has a sensor or not is randomly decided.
  * If the rectangle has the sensor, it is colored green. Otherwise, it is colored blue.
  
 My solution
  - Morphology
    * I used numpy to randomly choose the length range from 2 to 11.
    * Then I use numpy to randomly decided if each rectangle has a sensor with a probability of 0.5.
    * Then the size for each rectangle is three random number range from 0.1 to 1.1.
    * The position of joint and rectangle is placed based on the size of each and a randomly decided direction to grow, the calculation is shown in the graph below:
  ![_cgi-bin_mmwebwx-bin_webwxgetmsgimg__ MsgID=3253886853985681229 skey=@crypt_c8ba3495_b732f8902ab86ac0ca66d79992c92ed7 mmweb_appid=wx_webfilehelper](https://user-images.githubusercontent.com/88709397/220211758-caac9447-3132-414c-a182-856cbb1da80a.jpg)

    * Bottom Detection
      * I keep track of the current absolute position of the center of the cube.
      * If the bottom is below xy plane (z < 0), I will update the growth direction of the cube so that it grows up.
   
    * Overlap Detection
      * The program makes sure if the limb grew into one direction on the previous time step, it would not grow into the opposite direction in the current time step.
      * If the growth direction returns (0,0,0), the program will just replace it with the previous growth direction. It prevents the overlapping and also encourges the tendency to keep growing in the same direction.
   
   
   - Brain
    * All sensor nerons send information to all motor neurons.
    * The weight is random decided, ranging from (-1, 1).
    * The brain is not trained in this assignment.
  
