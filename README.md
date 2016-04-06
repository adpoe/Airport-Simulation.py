# Airport Simulation 
This is folder contains the written analysis, data collection and source code
for a discrete-event simulation undertaken to determine the best way to staff
an airport. The initial assignment prompt, as an HTML page is also included.

## How to run the simulation
In order to run the simulation, please navigate to the source code folder via
the command line and execute the following command:  "python main.py".

Running this command will initiate a prompt, asking you how many days you would
like to run the simulation. Anything over about 7 days may take a minute or two,
depending on your processing power, so please give it time. Please be aware that
this simulation generates arrivals for the system every six hours of simulation time,
and when arrivals are generated, I'm printing a confirmation message to the screen.
I kept this because I like to know that the simulation is still working when I run long
simulation (say a full year).

At the end of the simulation, the results for all key data points will be printed to the
console, so you can see how everything did.

I ran a number of simulations with different parameters over the course of this project,
and this source code represents the final state--this is these are the parameters
I am recommending the airport to use. So my design decisions are reflected when
you run the simulation, and my data analysis can be seen in the accompanying documents.


## How to run my unit tests
In order to run the unit tests created for this simulation, you can run the command
"python run_tests.py".

Please note that the unit tests do include a MatPlotLib graph, so a popup will
will appear with the graph that the unit tests generate.

One test is expected to fail:  That is the confirmation test for variance in
the International Passenger Arrival method. I chose to use the Box-Muller (Polar Coordinates)
method to generate these random variates, and this test does NOT produce any negative values.
The variance for this generation method is very high, and the NumPy built-in generation 
method produced some negative values, but I chose to use a generation method without this
feature, because it didn't make sense for my simulation. Everything else should pass.

## Dependencies
NumPy
MatPlotLib
Python ibraries:  Random, Math, Queue

## Additional Notes
The initial version of the experiment for this project is still intact, and I've included here.
The file which contains this version is named: "initial_experiment.py". This experiment can still
be run, if you'd like to see how the system looked when I first ran it. In order to do this,
take the following steps:
    1.  Backup the file named "time_advancement_mechanisms.py"
    2.  Rename "initial_experiment.py" to "time_advancement_mechanisms.py"
Run the project as usual:  "python main.py"

Voila--you're running the initial experiment. But be forewarned: The results will. be. ugly.

Beyond that--enjoy.

t

