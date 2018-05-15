# ROS package ros_stdr_ga
A simple framework to evolve the neural controller of a robot with ROS and the STDR robotic simulator.

## Dependencies 
* Python inspyred

## Instructions to install ros_stdr_ga
First of all, you will need to install, test and understand the *ros_stdr_ga* package. To install it, follow the next steps:

1. Install dependencies. This package depends on *rospy*, *stdmsgs*, *geometrymsgs* and *messagegeneration*; double check that you have all of them properly installated in your system.
2. Download ros_stdr_ga. The easy method (although less nerdy) is to download it from https://github.com/dfbarrero/ros_stdr_ga with a browser. The nerdy way is using Git to clone the repository executing the command *git clone https//github.com/dfbarrero/ros_stdr_ga*
3. (Optional) Delete the .git folder in the repository. This removes any Git metadata.
4. Move the package to your ROS workspace, in the sources space (folder src).
5. Compile the projects with *catkin_make*. This generates all the wrappers around the service that provides the fitness evaluation.
6. Update the environment variables with *source devel/setup.bash* in all the tabs you are using. Not following this step is a major cause of trouble.
7. Move the working folder to the *ros_stdr_ga* package root and test the installation running the simulation with *roslaunch launch/road.launch*

If everything is correct, there should be a STDR simulator window with a robot with the scenario shown in the figure.

![Map](resources/road.png)

In case there were any problem, check out whether the environment variables in each tab were updated with *source devel/setup.bash* and uninstalled ROS packages.

## Package contents

The package provides almost a full implementation of the neuroevolutive controller with the exception of the critical parts that define the ANN topology and its training. The package *ros_stdr_ga* provides some extra utility features along with the main one to ease the ANN development and training. It is important to understand what features the package provides, how it is implemented and that is needed to develop the neurocontroller.

The package provides some launch files:

* **road.launch**: Simulation with a simple layout and a custom robot on it. This simulation must be running when tranining the robot.
* **simple.launch**: Simulation with several obstacles and a custom robot. This simulation must be running when tranining the robot.
* **teleop.launch**: Executes a teleoperation node. Useful for testing.

The folder *scripts* contains the following interesting files:

* **neurocontroller.py**: Node that partially implements the service providing the fitness computation. The service, *computeFitness()*, takes an array of floats with the ANN weights, builds the ANN, feeds it with the sensors measures and controls the motion with its output. It runs the simulation for 3 seconds and returns the fitness value.

* **testFitness.py**: It computes the fitness of an ANN given by argument. This is quite usefull to observe the behaviour of an evolved ANN. Take into account that since *neurocontroller.py* is given without ANN implementation, a call to *testFitness.py* will fail until that code is written. The simulation must be running along with *neurocontroller.py* in order to properly execute this script. Give the ANN weights as an argument, for instance: *./testFitness.py "[0.2, 2.3, 1.1, -3.6, 3.2]"* for a network with five weights.

A potential source of problems is that computeFitness() must receive a vector with the same number of weights than the ANN, otherwise there will be unexpected consequences.

## Fitness assessment

The fitness is computed as the sum of the distance between the initial point and the final point, as measured by its odometry, and the distance traveled by the robot. Take into account that odometry contains noise, and therefore the fitness computation is noisy, which has a big impact in the evolution. The control loop iterates  times, which is enough to measure the robot behaviour while does not takes too much time to run. You can run this node and test *computeFitness()* with the command rosservice.

A tricky issue is how to map the array of weights given to *computeFitness()* to the actual weights in the ANN. Fortunately, that is almost irrelevant because the the ANN will eventually learn where each input and output neuron is connected. However, it is critical to keep consistency between the genotype encoding and the order in which the weights are sent to *computeFitness()*, i.e., use always the same mapping.

## Evolving the neurocontroller

In order to develop a neurocontroller, there are basically two different tasks:

1. Implement the ANN. This is done by editing the file *neurocontroller.py*. Just check out the two "TODO" comments in that file. 
2. Implement the EA. Do this in an external file. Call the ROS service "/computeFitness" to get the fitness value. You can implement the EA as you prefere (albeit we recommend using the [Inspyred](https://pythonhosted.org/inspyred/) Python Evolutionary Computation framework).

We describe those tasks in more detail.

There are three issues to implement the ANN:

1. Initialize the ANN. Fill the function *initANN()* in *neurocontroller.py*. The part of the script you must customized is marked with ``TODO''. Take into account that the ANN must have N_SONAR (which actually values 4) and two outputs.
2. Set the ANN weights.
3. Feed the network with the sonar measures (stored in the global variable ranges), propagate the input and store its output in the out global variable (remember, just two values, linear and angular velocities).

In this stage, you should be able to use testFitness.py to test the previous steps with random (or zero) weights. Do not expect a good robot behaviour at this point, just random motion, if any. Take into account that you must send the same number of weights that the ANN expects.

Now implement the evolutionary algorithm in *evolution.py*. This is just a regular Python script (i.e., no ROS involved here) using the EA of your choice. Use the following Python code to get the fitness function:

```Python
from subprocess import call

try:
	output = check_output(["rosservice", "call", "/computeFitness", string]) 
	fitness = float(output.split(" ")[1])
except Exception as e:
	print(__file__)
	print(e)
	return(0)

```

Where string is a string cointaing a vector of weights with Python syntax, for instance *[0.2, 2.3, 1.1, -3.6, 3.2]*.

Once all the previous tasks are completed, you should be able to perform the robot trainning with the following steps:

1. Run the simulation (*roslaunch launch/road.launch*).
2. Run the robot controller (*neurocontroller.py*).
3. Run the script that implements the evolutionary trainning (*evolution.py*). You should be able to view in real-time the behaviour of the robot in the STDR window.


