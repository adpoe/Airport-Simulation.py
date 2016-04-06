import variate_generators as vg
import numpy as np
import matplotlib.pyplot as plt
import arrival_generation as ag
import time_advance_mechanisms as tam



########################################
#### TESTS FOR VARIATE GENERATION ######
########################################

def confirm_commuter_arrivals_avg_40_per_hour():
    count = 0
    total_arrival_time = 0.0
    # Run 10,000 hours worth of data simulations
    while count < (10000 * 60):
        time_until_next_arrival = vg.gen_commuter_arrivals_at_airport()
        total_arrival_time += time_until_next_arrival
        count += 1

    average_arrivals_per_hour = total_arrival_time / (10000 * 60)
    print "-----Testing Commuter Arrival Distribution-----"
    print "COMMUTER ARRIVALS: Average inter-arrival time over a data set for 10,000 hours is: "+ str(average_arrivals_per_hour)

    # Expected value is 60/40 = 1.5 mins between arrivals
    testResult = False

    if (1.5 - average_arrivals_per_hour < 0.01):
        testResult = True

    return testResult


def confirm_international_arrivals_follow_normal_distro():
    mu = 75.0        # mean
    sigma = 50.0     # standard deviation

    # USE THIS VERSION IF USING PYTHON'S RANDOM #
    # s = np.random.normal(mu, sigma, 10000)
    #                                           #

    # USE THIS VERSION IF DOING BOX-MULLER #
    s = []
    counter = 0
    while counter < 10000:
        s.append(vg.gen_international_arrivals_via_polar_coords())
        counter += 1
                                          #

    diff_btwn_expected_and_actual_mean = abs(mu - np.mean(s))
    diff_btwn_expected_and_actual_sigma = abs(sigma - np.std(s, ddof=1))
    print "-----Testing International Arrival Distribution-----"
    print "CONFIRM:  mean is close to what we specified: " + str(abs(mu - np.mean(s)) < 1.0)
    print "CONFIRM:  variance is close to what we specified: " + str(abs(sigma - np.std(s, ddof=1)) < 1.0)

    # UNCOMMENT THE BELOW TO SEE A HISTOGRAM
    count, bins, ignored = plt.hist(s, 30,normed=False)
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *  np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='r')
    plt.show()

def confirm_intl_coach_passengers_follows_binomial():
    count = 0
    sum = 0
    while count < 10000:
        sum += vg.gen_number_of_intl_coach_seats_sold()
        count += 1

    long_run_avg = sum/10000
    expected_value = 0.85 * 150

    return (abs(expected_value - long_run_avg) < 1.0)

def confirm_intl_first_class_passengers_follows_binomial():
    count = 0
    sum = 0
    while count < 10000:
        sum += vg.gen_number_of_intl_first_class_seats_sold()
        count += 1

    long_run_avg = sum/10000.0
    expected_value = 0.80 * 50

    return (abs(expected_value - long_run_avg) < 1.0)

def confirm_geometric_distro_for_baggage_works():
    test_passed = True
    counter = 0
    total_international_bags = 0
    total_commuter_bags = 0
    while counter < 10000:
        total_international_bags += vg.gen_number_of_carry_on_items__for_INTL_passenger()
        total_commuter_bags += vg.gen_number_of_carry_on_items__for_COMMUTER_passenger()
        counter += 1

    expected_value_international_bags = 1.0 / 0.60
    expected_value_of_commuter_bags = 1.0 / 0.80

    long_run_avg_intl_bags_generated = total_international_bags / 10000.0
    long_run_avg_commuter_bags_generated = total_commuter_bags / 10000.0

    print "Long run average for international carry on bags per passenger = " + str(long_run_avg_intl_bags_generated)
    print "Correct is 1.666"
    if ( abs(long_run_avg_intl_bags_generated - expected_value_international_bags) > 1.0 ):
        test_passed = False
    print "Long run average for international carry on bags per passenger = " + str(long_run_avg_commuter_bags_generated)
    print "Correct is 1.25"
    if ( abs(long_run_avg_commuter_bags_generated - expected_value_of_commuter_bags) > 1.0 ):
        test_passed = False

    return test_passed

def confirm_boarding_pass_generation_works():
    avg_time_to_print_boarding_pass = sum([vg.gen_print_boarding_pass_time() for i in xrange(1000000)]) / 1000000.0
    print "Average time to print boarding pass="+str(avg_time_to_print_boarding_pass)
    return ( abs(2.0 - avg_time_to_print_boarding_pass) < 0.01)

def confirm_service_time_for_bag_check_generation_works():
    avg_time_to_check_bag = sum([vg.gen_time_to_check_bag() for i in xrange(1000000)]) / 1000000.0
    print "Average time to check bag="+str(avg_time_to_check_bag)
    return ( abs(1.0 - avg_time_to_check_bag) < 0.01)

def confirm_service_time_for_other_problems_and_delays_works():
    avg_time_for_delays = sum([vg.gen_time_for_other_problems_and_delays() for i in xrange(1000000)]) / 1000000.0
    print "Average time for delays and problems="+str(avg_time_for_delays)
    return ( abs(3.0 - avg_time_for_delays) < 0.01)

def confirm_service_time_for_other_sercurity_screening_works():
    avg_time_for_delays = sum([vg.gen_time_for_other_problems_and_delays() for i in xrange(1000000)]) / 1000000.0
    print "Average time to pass security screening="+str(avg_time_for_delays)
    return ( abs(3.0 - avg_time_for_delays) < 0.01)

#############################
###### DATA GENERATION ######
#############################
def generate_commuter_arrival_data_set():
    count = 0
    while count < 1000:
        commuter_arrivals_per_hour = vg.gen_commuter_arrivals_at_airport()
        print "Generated this variate for commuter arrivals " + str(commuter_arrivals_per_hour)
        count += 1
    # Write to a file if needed

def generate_data_set( function ):
    count = 0
    while count < 1000:
        rand_variate = function()
        print "Generated this variate for function passed: " + str(rand_variate)
        count += 1
    # Write to a file if needed


#######################################
#### TESTS FOR ARRIVAL GENERATION #####
#######################################
def confirm_that_6hours_of_commuter_arrival_generation_works():
    commuter_arrivals = ag.generate_six_hours_of_commuter_arrivals()
    #--- Uncomment to see all the arrivals ---
    for next_arrival in commuter_arrivals:
        print "Next arrival is this many minutes from now: " + str(next_arrival)
    # return abs(360.0 - sum(commuter_arrivals)) < 5.00

def confirm_that_6hours_of_first_class_intl_arrivals_works():
    first_class_intl_arrivals = ag.generate_six_hours_first_class_intl_arrivals()
    #--- Uncomment to see all the arrivals ---
    for next_arrival in first_class_intl_arrivals:
        print "Next arrival is this many minutes from now: " + str(next_arrival)

def confirm_that_6hours_of_coach_intl_arrivals_works():
    coach_intl_arrivals = ag.generate_six_hours_coach_intl_arrivals()
    #--- Uncomment to see all the arrivals ---
    for next_arrival in coach_intl_arrivals:
        print "Next arrival is this many minutes from now: " + str(next_arrival)

###################################################
##### TESTS FOR TOTAL SERVICE TIME GENERATION #####
###################################################
def confirm_that_checkin_service_time_works_for_commuters():
    count = 0
    sum = 0

    while count < 100:
        total_service_time = ag.gen_check_in_service_time_per_passenger( "commuter" )
        sum += total_service_time
        # ---Uncomment below to view output---
        # print "Commuter service time is: " + str(total_service_time)
        count += 1

    return sum



def confirm_that_checkin_service_time_works_for_international():
    count = 0
    sum = 0

    while count < 100:
        total_service_time = ag.gen_check_in_service_time_per_passenger( "international" )
        sum += total_service_time
        # --Uncomment Below to view output---
        # print "International service time is: " + str(total_service_time)
        count += 1

    return sum



def confirm_confirm_check_service_times_correct():
    total_time_for_100_intl_passengers = confirm_that_checkin_service_time_works_for_international()
    total_time_for_100_commuter_passengers = confirm_that_checkin_service_time_works_for_commuters()

    return total_time_for_100_commuter_passengers < total_time_for_100_intl_passengers

######################################
##### TESTS FOR SIMULATION CLASS #####
######################################
def confirm_arrival_generation_is_correct():
    # iterate through each array and print the values
    mySimulation = tam.Simulation()
    mySimulation.generate_SIX_HOURS_of_arrivals()

    # Print international first class arrivals
    count_first_class_intl_arrivals = 0
    print "----International First Class Arrivals----"
    for p in mySimulation.international_first_class_ARRIVALS:
        print "International FIRST class arrival: " + str(p)
        count_first_class_intl_arrivals += 1
    print "TOTAL INTERNATIONAL FIRST CLASS ARRIVALS="+str(count_first_class_intl_arrivals)

    # Print international coach class arrivals
    count_coach_class_intl_arrivals = 0
    print "----International Coach Class Arrivals----"
    for p in mySimulation.international_coach_class_ARRIVALS:
        print "International COACH class arrival: " + str(p)
        count_coach_class_intl_arrivals += 1
    print "TOTAL INTERNATIONAL FIRST CLASS ARRIVALS="+str(count_coach_class_intl_arrivals)

    # Print commuter coach class arrivals
    count_coach_class_commuter_arrivals = 0
    print "----International Coach Class Arrivals----"
    for p in mySimulation.commuter_coach_class_ARRIVALS:
        print "International COACH class arrival: " + str(p)
        count_coach_class_commuter_arrivals += 1
    print "TOTAL COACH CLASS COMMUTER ARRIVALS="+str(count_coach_class_commuter_arrivals)



def confirm_revenue_collection_is_correct():
    # test the revenue collection
    mySimulation = tam.Simulation()
    mySimulation.generate_SIX_HOURS_of_arrivals()

    # get number of arrivals for each item
    num_commuter_arrivals = len(mySimulation.commuter_coach_class_ARRIVALS)
    num_first_class_intl_arrivals = len(mySimulation.international_first_class_ARRIVALS)
    num_coach_intl_arrivals = len(mySimulation.international_coach_class_ARRIVALS)

    # collect revenue!
    mySimulation.collect_revenue()

    # how much revenue should there be?
    print "-----Confirming revenue collection works-----"
    commuter_revenue = num_commuter_arrivals * mySimulation.commuter_ticket_price
    print "Commuter revenue="+str(commuter_revenue)
    intl_first_class_revenue = num_first_class_intl_arrivals * mySimulation.intl_first_class_ticket_price
    print "First Class Intl revenue="+str(intl_first_class_revenue)
    intl_coach_revenue = num_coach_intl_arrivals * mySimulation.intl_coach_ticket_price
    print "Coach Class Intl revenue="+str(intl_coach_revenue)
    total_revenue_expected = commuter_revenue + intl_first_class_revenue + intl_coach_revenue
    print "TOTAL REVENUE SHOULD BE="+str(total_revenue_expected)
    print "REVENUE COLLECTED BY SIMULATION="+str(mySimulation.revenue_total)

    return total_revenue_expected == mySimulation.revenue_total

def confirm_update_service_time_works():
    mySimulation = tam.Simulation()
    mySimulation.update_servers()

    # Check that udpate service time has decremented the servers' service time, which starts at 0.0, by -0.01
    for server in mySimulation.servers:
        if server.service_time == -0.01:
            return False

    # if we get this far
    return True

############################
##### TEST QUEUE CLASS #####
############################
# Test each operation with simplistic data, make sure they all work.
def confirm_add_passenger_to_checkin_queue_works():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1, 10.00)
    my_checkin_queue = tam.CheckInQueue()
    my_checkin_queue.add_passenger(new_passenger)

    confirm_add_works = True

    if not my_checkin_queue.customers_added == 1:
        confirm_add_works = False
    return confirm_add_works

def confirm_get_passenger_form_checkin_queue_works():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_checkin_queue = tam.CheckInQueue()
    my_checkin_queue.add_passenger(new_passenger)
    # confirm we get the right passenger
    confirm_remove_works = True
    next_passenger_in_line = my_checkin_queue.get_next_passenger_in_line()
    if not next_passenger_in_line.__eq__(new_passenger):
        confirm_remove_works = False
    # confirm we DON'T get duplicates of a passenger
    should_be_NONE = my_checkin_queue.get_next_passenger_in_line()
    if not should_be_NONE is None:
        confirm_remove_works = False
    return confirm_remove_works
# Test each operation with simplistic data, make sure they all work.

def confirm_add_passenger_to_security_queue_works():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_checkin_queue = tam.SecurityQueue()
    my_checkin_queue.add_passenger(new_passenger)

    confirm_add_works = True

    if not my_checkin_queue.customers_added == 1:
        confirm_add_works = False
    return confirm_add_works

def confirm_get_passenger_from_security_queue_works():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_checkin_queue = tam.SecurityQueue()
    my_checkin_queue.add_passenger(new_passenger)
    # confirm we get the right passenger
    confirm_remove_works = True
    next_passenger_in_line = my_checkin_queue.get_next_passenger_in_line()
    if not next_passenger_in_line.__eq__(new_passenger):
        confirm_remove_works = False
    # confirm we DON'T get duplicates of a passenger
    should_be_NONE = my_checkin_queue.get_next_passenger_in_line()
    if not should_be_NONE is None:
        confirm_remove_works = False
    return confirm_remove_works

###################################
##### TEST CheckInServer CASS #####
###################################

# --> Just use a list for this, security server first, to avoid issues.
#     Check if not not, remove from front of list, etc. It'll make life easier
def confirm_add_customer_to_SECURITY_server_works():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_SECURITY_server = tam.SecurityServer()
    my_SECURITY_server.add_customer(new_passenger)
    # confirm it works
    test_works = True
    if not my_SECURITY_server.customers_added == 1:
        test_works = False
    return test_works

def confirm_remove_customer_from_SECURITY_server_works():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_SECURITY_SERVER = tam.SecurityServer()
    my_SECURITY_SERVER.add_customer(new_passenger)
    # confirm we get the right passenger on removal
    confirm_remove_works = True

    # first we confirm that you CAN'T remove someone from the queue if they are still being served
    next_passenger_in_line = my_SECURITY_SERVER.complete_service()
    if not next_passenger_in_line is None:
        return False

    # then we confirm that you CAN remove someone from the queue if they are DONE being served
    my_SECURITY_SERVER.service_time = 0.01
    my_SECURITY_SERVER.update_service_time()
    next_passenger_in_line = my_SECURITY_SERVER.complete_service()
    # first make sure we didn't get a done
    if next_passenger_in_line is None:
        return False
    # then make sure we have the right passenger
    if not next_passenger_in_line.__eq__(new_passenger):
        confirm_remove_works = False

    # Finally, confirm we DON'T get duplicates of a passenger
    should_be_NONE = my_SECURITY_SERVER.complete_service()
    # try and pull an invalid user 20 times. approximate what may happen in the system
    for i in range(0,10):
        if not should_be_NONE is None:
            confirm_remove_works = False

    # and return the final results of our test
    return confirm_remove_works

def confirm_update_system_time_works_for_SecurityServer():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_SECURITY_server= tam.SecurityServer()
    my_SECURITY_server.add_customer(new_passenger)
    # artificially set the service time to 0.01 to make testing easier
    my_SECURITY_server.service_time = 0.01
    # now update the service time --> and we should be NOT busy, with service time = 0.0
    for i in range(1,50):
        my_SECURITY_server.update_service_time()

    # start out true, and if any test fails... we know this doesn't work
    update_service_time_works = True

    # check that the boolean flag gets set properly
    if my_SECURITY_server.is_busy():
        is_busy = my_SECURITY_server.is_busy()
        update_service_time_works = False
    if not str(my_SECURITY_server.service_time) == str(0):
        service_time_after_50_ticks = my_SECURITY_server.service_time
        service_time_after_50_ticks_as_string = str(service_time_after_50_ticks)
        update_service_time_works = False

    return update_service_time_works

########################################
###### TEST SecurityServer CLASS #######
########################################
# --> Just use a list for this, security server first, to avoid issues.
#     Check if not not, remove from front of list, etc. It'll make life easier
def confirm_add_customer_to_checkin_server_works():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_checkin_server = tam.CheckInServer()
    my_checkin_server.add_customer(new_passenger)
    # confirm it works
    test_works = True
    if not my_checkin_server.customers_added == 1:
        test_works = False
    return test_works

def confirm_remove_customer_from_checkin_server_works():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_checkin_SERVER = tam.CheckInServer()
    my_checkin_SERVER.add_customer(new_passenger)
    # confirm we get the right passenger on removal
    confirm_remove_works = True

    # first we confirm that you CAN'T remove someone from the queue if they are still being served
    next_passenger_in_line = my_checkin_SERVER.complete_service()
    if not next_passenger_in_line is None:
        return False

    # then we confirm that you CAN remove someone from the queue if they are DONE being served
    my_checkin_SERVER.service_time = 0.01
    my_checkin_SERVER.update_service_time()
    next_passenger_in_line = my_checkin_SERVER.complete_service()
    # first make sure we didn't get a done
    if next_passenger_in_line is None:
        return False
    # then make sure we have the right passenger
    if not next_passenger_in_line.__eq__(new_passenger):
        confirm_remove_works = False

    # Finally, confirm we DON'T get duplicates of a passenger
    should_be_NONE = my_checkin_SERVER.complete_service()
    # try and pull an invalid user 20 times. approximate what may happen in the system
    for i in range(0,10):
        if not should_be_NONE is None:
            confirm_remove_works = False

    # and return the final results of our test
    return confirm_remove_works

def confirm_update_system_time_works_for_CheckInServer():
    # initialize the system with system_time=10.00
    mySim = tam.Simulation
    mySim.system_time = 10.00
    # create a new passenger, and add him to the queue. make sure this works.
    new_passenger = tam.Passenger(10.00, "commuter","coach",1,10.00)
    my_checkin_server = tam.CheckInServer()
    my_checkin_server.add_customer(new_passenger)
    # artificially set the service time to 0.01 to make testing easier
    my_checkin_server.service_time = 0.01
    # now update the service time --> and we should be NOT busy, with service time = 0.0
    for i in range(1,50):
        my_checkin_server.update_service_time()

    # start out true, and if any test fails... we know this doesn't work
    update_service_time_works = True

    # check that the boolean flag gets set properly
    if my_checkin_server.is_busy():
        is_busy = my_checkin_server.is_busy()
        update_service_time_works = False
    if not str(my_checkin_server.service_time) == str(0):
        service_time_after_50_ticks = my_checkin_server.service_time
        service_time_after_50_ticks_as_string = str(service_time_after_50_ticks)
        update_service_time_works = False

    return update_service_time_works



##################################
##### TEST PASSENGER CLASS #######
##################################


#################################################
#### TEST EACH FUNCTION IN SIMULATION CLASS #####
#################################################

# --> Write mocks (fake data) that's easy to test, and add it to class directly.
#     spawn a new class object for each test method to ensure encapsulation is okay
#     As needed, add updates so we can get data on who is in system and where, at what time.
#     Need to also think of planes as SERVERS with service time=time_between_departures
#     Need to make sure we store everyone who leaves the system in a diff list, depending on how they left
#        Also need system times for this, to verify what's going on
#     >> Put on headphones sit down, maybe at home, and do it. chug.


##############################
#### RUN WHOLE TEST SUITE ####
##############################
# Biggest question:   Generate international arrival using python's built in? Or use polar coords method?
#                     Decided on polar coords for now....Because too many people would come AFTER their flight takes off
#                     And doesn't make sense for them ENTER QUEUE for no reason at all.
def run_variate_generator_tests():

    print "Commuter inter-arrival rate is about 1 customer every 1.5mins (40/hr): " + str(confirm_commuter_arrivals_avg_40_per_hour())
    confirm_international_arrivals_follow_normal_distro()
    print "Number of international passengers in coach follows binomial="+str(confirm_intl_coach_passengers_follows_binomial())
    print "Number of international passengers in first class follows binomial="+str(confirm_intl_first_class_passengers_follows_binomial())
    print "-------Testing Check-in Process Distributions------"
    print "CONFIRM:  Geometric distribution for baggage works=" + str( confirm_geometric_distro_for_baggage_works() )
    print "CONFIRM:  Boarding pass service time generation works="+str(confirm_boarding_pass_generation_works())
    print "CONFIRM:  Bag check service time generation works="+str(confirm_service_time_for_bag_check_generation_works())
    print "CONFIRM:  Delays and problems service time generation works="+str(confirm_service_time_for_other_problems_and_delays_works())
    print "-------Testing Security Screening Distributions----"
    print "CONFIRM:  Security screening service time generation works="+str(confirm_service_time_for_other_sercurity_screening_works())
    # generate_data_set(vg.gen_international_arrivals_at_airport)
    # vg.gen_international_arrivals_via_polar_coords()
    print "-------Testing Generation for 6 hours of arrival times------"
    print "CONFIRM:  Six hours of COMMUTER ARRIVALS works=(uncomment line below to view output)"
    confirm_that_6hours_of_commuter_arrival_generation_works()
    print "CONFIRM:  Six hours of FIRST CLASS INT'L ARRIVALS works=(uncomment line below to view output)"
    confirm_that_6hours_of_first_class_intl_arrivals_works()
    print "CONFIRM:  Six hours of COMMUTER CLASS INT'L ARRIVALS works=(uncomment line below to view output)"
    # confirm_that_6hours_of_coach_intl_arrivals_works()
    print "-----Testing Variate Generation Time Check in Queue-----"
    print "CONFIRM:  Total service time at CHECK IN for COMMUTERS works=(uncomment line below to view output)"
    # confirm_that_checkin_service_time_works_for_commuters()
    print "CONFIRM:  Service times for int'l and commuter passengers at CHECK-IN make sense="+str(confirm_confirm_check_service_times_correct())
    print "-----Testing Variate Generation Time for Security Queue-----"
    print "CONFIRM:  Security screening time generation works="+str(confirm_service_time_for_other_sercurity_screening_works())
    print "-----Testing that Time Advance Mechanisms Work------"
    print "CONFIRM: Generation of arrivals is correct=(uncomment line below to view output)"
            # TEST ARRIVALS IN TIME ADVANCE....
    #confirm_arrival_generation_is_correct()
    print "CONFIRM: Revenue collection is correct="+str(confirm_revenue_collection_is_correct())
            # TEST THAT REVENUES COLLLECTED CORRECTLY
    print "CONFIRM: Update Service Time works="+str(confirm_update_service_time_works())
    """
        WRITE MORE TESTS --> need ot make sure queues work, passengers modeled correctly, etc.
    """
    print "-----Testing CheckIn Queue Class Works------"
    print "CONFIRM:  Adding to CheckinQueue works="+str(confirm_add_passenger_to_checkin_queue_works())
    print "CONFIRM:  Removing from CheckinQueue works="+str(confirm_get_passenger_form_checkin_queue_works())
    print "-----Testing Security Queue Works------"
    print "CONFIRM:  Adding to SecurityQueue works="+str(confirm_add_passenger_to_security_queue_works())
    print "CONFIRM:  Removing from SecurityQueue works="+str(confirm_get_passenger_from_security_queue_works())
    "CAN SPAWN A NEW CHECKINQUE Later to hold passenger at gate"
    print "-----Testing that CheckInServer Class Works-----"
    print "CONFIRM:  Adding to CheckInServer works="+str(confirm_add_customer_to_checkin_server_works())
    print "CONFIRM:  Remove customer from CheckInServer works="+str(confirm_remove_customer_from_checkin_server_works())
    print "CONFIRM:  Update service time for CheckInServer works="+str(confirm_update_system_time_works_for_CheckInServer())
    print "-----Testing that SecurityServer Class Works-----"
    print "CONFIRM:  Adding to CheckInServer works="+str(confirm_add_customer_to_SECURITY_server_works())
    print "CONFIRM:  Remove customer from CheckInServer works="+str(confirm_remove_customer_from_SECURITY_server_works())
    print "CONFIRM:  Update service time for CheckInServer works="+str(confirm_update_system_time_works_for_SecurityServer())
    print "-----Testing that CommuterPlaneServer Class Works-----"
    print "-----Testing that InternationalPlaneServer Class Works----"
    print "-----TEST WHOLE SIMULATION----"
    #mySimulation = tam.Simulation()
    #mySimulation.run_simulation(1)

