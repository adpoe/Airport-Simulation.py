import time_advance_mechanisms as tam

"""
@Author: Tony Poerio
@email:  adp59@pitt.edu
University of Pittsburgh
Spring 2016
CS1538 - Simulation
Assignment #4 - Airport Simluation

Generates an airport simulation.

#Objectives:
    1.  Determine an allocation policy for the number of agents to help 1st class vs. coach passengers
          ::  Want to ensure that 1st class passengers don't wait in the line for long
          ::  But still keep the wait time for coach passengers reasonable
          ::  Minimize agents' idle time
"""

####################
### CONTROL FLOW ###
####################
def main():
    print "UNIVERISTY OF PITTSBURGH - SPRING 2016:: CS1538, Assignment #4"
    print "--------------------------------------------------------------"
    print ""
    print "This program simulates the check-in process at a small local airport. "
    print "Throughout the process, data is collected. At the end of the simulation, the relevant"
    print "data points are output here, at the console."
    print "If you simulate more than about 7 days, please allow a few minutes of runtime, depending"
    print "on how powerful your computer is. "
    print "------------------------------------"
    print "How may days would you like to simulate?"
    simulation_time = raw_input("> ")
    simulation_time = int(simulation_time)
    mySim = tam.Simulation()
    mySim.run_simulation(simulation_time)
    mySim.print_simulation_results()


    return


###################
### ENTRY POINT ###
###################

if __name__ == "__main__":
    main()

