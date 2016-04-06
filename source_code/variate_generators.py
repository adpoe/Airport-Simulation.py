import math
import random
import numpy as np

#########################################
#####  RANDOM_VARIATE_GENERATORS   ######
#########################################

#                         #
# Arrivals at the Airport #
#                         #

def gen_commuter_arrivals_at_airport():
    """
    Arrivals of commuters follows a POISSON PROCESS
    Arrival Rate = 40 people/hour
                 = 40/60 (minutes)
                 = 2/3
    Implemantation from:  http://preshing.com/20111007/how-to-generate-random-timings-for-a-poisson-process/
    :return:  Return value is time until NEXT ARRIVAL, in minutes.
    """
    arrival_rate = 2.0/3.0
    return -math.log(1.0 - random.random()) / arrival_rate


def gen_international_arrivals_at_airport():
    """
    Arrivals of international passengers follows a NORMAL DISTRIBUTION
    Mean = 75 minutes
    Variance = (50 minutes)^2
    Note:  If SAME arrival time is generated twice, must be differentiated even by split seconds.
           No duplicates are allowed.

    Implementation found at:
    http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.random.normal.html
    :return: Time that passenger has arrived BEFORE his next flight, in minutes.

    Note this gives a normal distribution value which is sometimes BELOW zero.... AND passes variance test.
    Maybe, just say that, if below zero --> zero arrivals.
    also doesn't appear to be time until next arrival. Normal distro around 75, with variance 50^2
    """
    mu = 75.0        # mean
    sigma = 50.0     # standard deviation
    s = np.random.normal(mu, sigma)

    return s


def gen_international_arrivals_via_polar_coords( ):
    """
    Arrivals of international passengers follows a NORMAL DISTRIBUTION
    Mean = 75 minutes
    Variance = (50 minutes)^2
    Note:  If SAME arrival time is generated twice, must be differentiated even by split seconds.
           No duplicates are allowed.
    :return: Time that passenger has arrived BEFORE his next flight, in minutes.

    # Note this gives a normal distribution value which is always ABOVE zero, BUT variance doesn't seem right.
    # also doesn't appear to be time until next arrival. Normal distro around 75, with variance 50^2
    """
    mu = 75.0              # mean
    sigma_value = 50.0     # standard deviation
    num_iterations = 1
    reject = False
    rejections = 0
    writeValue1 = ""
    writeValue2 = ""
    X = 0.0
    Y = 0.0

    # counter for how many iterations we've run
    counter = 0

    # Open a file for output
    # outFile = open("polar_coords.txt", "wb")

    #Perfom number of iterations requested by user
    while counter < num_iterations:
        # Process from Sheldon Ross' Simulations 5th edition, page 83
        # Step 1:  Generate random numbers U1 and U2
        U1 = random.random()
        U2 = random.random()
        # Step 2:  Set V1 = 2U1 - 1, V2 = 2U2 - 1, S = V1^2 + V2^2
        V1 = 2.0*U1 - 1.0
        V2 = 2.0*U2 - 1.0
        S = (V1 ** 2) + (V2 ** 2)

        if S > 1.0:
            reject = True
            rejections += 1
        if reject == False:
            X = math.sqrt( (-2.0 * math.log(S))/S )*V1
            Y = math.sqrt( (-2.0 * math.log(S))/S )*V2
            Z = X * math.sqrt(sigma_value) + mu
            writeValue1 = str(Z)
        # write to output file
        # outFile.write(writeValue1 + "\n")
            # print "num: " + " " + str(counter) +":: " + writeValue1
            # Only increment counter if we get a valid output
            counter = counter+1

        # Reset the rejection criteria the data
        reject = False

    # outFile.close()

    # print "Found this many rejections: " + str(rejections)
    # print "Successfully stored " + str(num_iterations) + " random numbers in file named: 'polar_coords.txt'."

    return Z


def gen_number_of_intl_coach_seats_sold():
    """
    Generates number of passengers who will fly coach on our next international flight.
    :return: number of coach passengers
    """
    return np.random.binomial(150, 0.85)

def gen_number_of_intl_first_class_seats_sold():
    """
    Generates number of passengers who will fly first class on our next international flight.
    :return: number of first class passengers
    """
    return np.random.binomial(50, 0.80)


#                                  #
# Carry-on Distribution Generation #
#                                  #
def bernoulli_trial_intl():
    """
    A BERNOULLI TRIAL with success probability: Percent chance
    :param percent_chance: 0.6 for INTL, 0.8 COMMUTER
    :return:
    """
    return np.random.binomial(1, 0.6)

def bernoulli_trial_commuter():
    """
    A BERNOULLI TRIAL with success probability: Percent chance
    :param percent_chance: 0.6 for INTL, 0.8 COMMUTER
    :return:
    """
    return np.random.binomial(1, 0.8)


def gen_number_of_carry_on_items__for_INTL_passenger():
    """
    Number of bags a passenger carries is determined using a GEOMETRIC DISTIBUTION
    BERNOULLI TRIAL with success bias %p = chance of passenger bringing bags
    Bernoulli with 60% chance
    P = 0.60 for international
    :return: Number of bags an international passenger has carried on
    """
    # Count number o iterations until a success
    counter = 0
    successful_trial = 0
    while successful_trial == 0:
        successful_trial = bernoulli_trial_intl()
        counter += 1

    return counter


def gen_number_of_carry_on_items__for_COMMUTER_passenger():
    """
    Number of bags a passenger carries is determined using a GEOMETRIC DISTIBUTION
    BERNOULLI TRIAL with success bias %p = chance of passenger bringing bags
    Bernoulli with 80% chance
    P = 0.80 for international
    :return: Number of bags a commuter passenger has carried on
    """

    # Count number of iterations until a success
    counter = 0
    successful_trial = 0
    while successful_trial == 0:
        successful_trial = bernoulli_trial_commuter()
        counter += 1

    return counter


#                            #
# Check-in Queuing Processes #
#                            #
def gen_print_boarding_pass_time():
    """
    EXPONENTIAL distribution
    Average service time = 1 event every 2 minutes --> 1/2
    :return: Time to print boarding pass
    """
    service_time = 1.0/2.0
    return -math.log(1.0 - random.random()) / service_time

def gen_time_to_check_bag():
    """
    The checking of each bag follows an EXPONENTIAL distribution with
    Average Service time = 1 min
    If passenger has NO bags, service time = 0
    :return:
    """
    return -math.log(1.0 - random.random())


def gen_time_for_other_problems_and_delays():
    """
    EXPONENTIAL distribution with
    Average service time = 3 mins
    :return:
    """
    service_time = 1.0/3.0
    return -math.log(1.0 - random.random()) / service_time


#                                      #
# Security Screening Queuing Processes #
#                                      #
def gen_avg_service_time_for_security_screening_machine():
    """
    EXPONENTIAL distribution with
    Average Service time = 3 mins
    :return:
    """
    service_time = 1.0/3.0
    return -math.log(1.0 - random.random()) / service_time




