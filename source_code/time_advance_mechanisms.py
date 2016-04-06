import math
import random
import time
import arrival_generation as ag
import Queue as q
import constants_and_params as params

"""
Discrete time advance mechanisms for airport simulation project.
This class will generate 6 hours worth of passenger arrivals, and store the data in two arrays:
- One for commuters passengers
- One for international passengers

For each passenger, also need to generate their wait times for each queue. Or is that done when a passenger queues up?

"""

###########################
### ARRIVAL GENERATION ####
###########################
class Arrivals:
    """ Class used to generate six hours of arrivals at a time
    """
    def __init__(self):
        self.commuter_coach_arrivals = []
        self.intl_coach_arrivals = []
        self.intl_first_class_arrivals = []

    def get_arrivals(self):
        """ Get all the arrivals to the system in the next six hours. Store the values in instance vars.
        """
        self.commuter_coach_arrivals = ag.generate_six_hours_of_commuter_arrivals()
        self.intl_coach_arrivals = ag.generate_six_hours_coach_intl_arrivals()
        self.intl_first_class_arrivals = ag.generate_six_hours_first_class_intl_arrivals()



##########################
#### CHECK-IN QUEUES #####
##########################
class CheckInQueue:
    """ Class used to model a check-in line Queue
    """
    def __init__(self):
        self.queue = q.Queue()
        self.customers_added = 0

    def add_passenger(self, new_passenger):
        self.queue.put_nowait(new_passenger)
        self.customers_added += 1

    def get_next_passenger_in_line(self):
        if not self.queue.empty():
            next_customer = self.queue.get_nowait()
            self.queue.task_done()
        else:
            next_customer = None
        return next_customer

##########################
#### SECURITY QUEUES #####
##########################

""" Again, may need to add a GET method here, as well
"""
class SecurityQueue:
    """ Class used to model a security line Queue
    """
    def __init__(self):
        self.queue = q.Queue()
        self.customers_added = 0

    def add_passenger(self, new_passenger):
        self.queue.put(new_passenger)
        self.customers_added += 1

    def get_next_passenger_in_line(self):
        if not self.queue.empty():
            next_customer = self.queue.get_nowait()
            self.queue.task_done()
        else:
            next_customer = None
        return next_customer

###########################
##### AIRPORT SERVERS #####
###########################
class CheckInServer:
    """ Class used to model a server at the Check-in terminal
    """
    def __init__(self):
        """ Initialize the class variables
        """
        #----COMMENTED OUT ARE FOR PREVIOUS VERSION-----
        self.service_time = 0.0
        self.busy = False
        # self.customer = None
        self.customer_being_served = q.Queue()
        self.is_first_class = False
        self.customers_added = 0
        self.customers_served = 0
        # self.last_customer_served = q.Queue()
        self.idle_time = 0.00

    def set_service_time(self, passenger_type):
        """ Sets the service time for a new passenger
        :param passenger_type:  either "commuter" or "international"
        """
        self.service_time = ag.gen_check_in_service_time_per_passenger( passenger_type )
        self.busy = True

    def update_service_time(self):
        """ Updates the service time and tells us if the server is busy or not
        """
        self.service_time -= 0.01

        if self.service_time <= 0:
            self.service_time = 0
            self.busy = False
            # ------COMMENTED OUT FOR PREVIOUS VERSION-----
            # self.last_customer_served.put(self.customer)

        if not self.is_busy():
            self.idle_time += 0.01

    def is_busy(self):
        """ Call this after updating the service time at each change in system time (delta). Tells us if server is busy.
        :return: True if server is busy. False if server is NOT busy.
        """
        return self.busy

    def add_customer(self, new_passenger):
        """ Adds a customer to the sever and sets his service time
        :param new_passenger: the passenger we are adding
        """
        #-----PREVIOUS VERSION---
        # self.customer = new_passenger
        # self.set_service_time(new_passenger.type_of_flight)
        # self.customers_added += 1

        # NEW VERSION
        # get the type of flight his passenger is on
        type_of_flight = new_passenger.type_of_flight
        # add the passenger to our service queue
        self.customer_being_served.put_nowait(new_passenger)
        # set the service time, depending on what type of flight the customer is on
        self.set_service_time(type_of_flight)
        # update the count of customers added
        self.customers_added += 1


    def complete_service(self):
        """ Models completion of our service
        :return: the customer who has just finished at this station
        """
        #------PREVIOUS VERSION------
        # completed_customer = None
        # if not self.last_customer_served.empty():
        #     completed_customer = self.last_customer_served.get_nowait()
        #     self.last_customer_served.task_done()
        # if not completed_customer == None:
        #     self.customers_served += 1
        # return completed_customer
        next_customer = None
        # only try to pull a customer from the queue if we are NOT busy
        # AND the queue isn't empty
        # else we just return a None
        if not self.is_busy() and not self.customer_being_served.empty():
            next_customer = self.customer_being_served.get_nowait()
            self.customer_being_served.task_done()
            self.customers_served += 1
        else:
            next_customer = None
        return next_customer


class SecurityServer:
    """ Class used to model a server at the Security terminal
    """
    def __init__(self):
        """ Initialize the class variables
        """
        #-----PREVIOUS VERSION------
        #self.service_time = 0.0
        #self.busy = None
        #self.customer = None
        #self.is_first_class = False
        #self.customers_added = 0
        #self.customers_served = 0
        # vvv This can be a list, and we can stop the BS
        #self.last_customer_served = q.Queue()
        #self.last_customer_returned = None
        #self.redundant = None

        self.service_time = 0.0
        self.busy = None
        # self.customer = None
        self.customer_being_served = q.Queue()
        self.is_first_class = False
        self.customers_added = 0
        self.customers_served = 0
        self.idle_time = 0.0

    def set_service_time(self):
        """ Sets the service time for a new passenger
        :param passenger_type:  either "commuter" or "international"
        """
        self.service_time = ag.gen_security_screening_time()
        self.busy = True

    def update_service_time(self):
        """ Updates the service time and tells us if the server is busy or not
        """
        self.service_time -= 0.01

        if self.service_time <= 0:
            self.service_time = 0
            self.busy = False
        #------PREVIOUS VERSION------
        #    self.last_customer_served.put(self.customer)

        if not self.is_busy():
            self.idle_time += 0.01

    def is_busy(self):
        """ Call this after updating the service time at each change in system time (delta). Tells us if server is busy.
        :return: True if server is busy. False if server is NOT busy.
        """
        return self.busy

    def add_customer(self, new_passenger):
        """ Adds a customer to the sever and sets his service time
        :param new_passenger: the passenger we are adding
        """
        #-----PREVIOUS VERSION-----
        #self.customer = new_passenger
        #self.set_service_time()
        #self.customers_added += 1
        # NEW VERSION
        # add the passenger to our service queue
        self.customer_being_served.put_nowait(new_passenger)
        # set the service time, depending on what type of flight the customer is on
        self.set_service_time()
        # update the count of customers added
        self.customers_added += 1

    def complete_service(self):
        """ Models completion of our service
        :return: the customer who has just finished at this station
        """
        # comment this stuff out and try again....
        # do the tests... make sure they pass...
        # then do passenger class tests....
        # then start on the individual tests for the Simulation Class
        # Run simulation first once though, to see what all breaks...

        #-------PREVIOUS VERSION
        #matches_redundant = False
        # redundant = previous completed customer
        #self.redundant = self.last_customer_returned
        # then try to get a new one
        #completed_customer = None
        #if not self.last_customer_served.empty():
        #    completed_customer = self.last_customer_served.get_nowait()
        #    self.last_customer_served.task_done()
        #    if not self.redundant is None and not completed_customer is None:
        #        matches_redundant = str(completed_customer.system_time_entered) == str(self.redundant.system_time_entered)
        #if not completed_customer is None and not matches_redundant:
        #    self.customers_served += 1
        #if matches_redundant:
        #    return None
        #self.last_customer_returned = completed_customer
        #return completed_customer
        next_customer = None
        # only try to pull a customer from the queue if we are NOT busy
        # AND the queue isn't empty
        # else we just return a None
        if not self.is_busy() and not self.customer_being_served.empty():
            next_customer = self.customer_being_served.get_nowait()
            self.customer_being_served.task_done()
            self.customers_served += 1
        else:
            next_customer = None
        return next_customer



##############################
##### AIRPORT PASSENGERS #####
##############################
class Passenger:
    """ Class used to model a passenger in our simluation
    """
    def __init__(self, system_time, flight_type, ticket_class, system_iteration, relative_time):
        self.system_time_entered = system_time
        self.type_of_flight = flight_type
        self.flight_class = ticket_class
        self.gets_refund = False
        self.international_flight_number = system_iteration
        self.relative_time = relative_time
        #--------DEBUGGING-------
        #if flight_type == "international" and system_time > 1490:
        #    print "here"
        #
        #confirm_system_time = (system_time / system_iteration)
        #confirm_relative_time = str(relative_time)
        #relative_system_time = system_time / (system_iteration * 360.0)
        #if not str(math.floor((system_time / system_iteration))) == str(math.floor(relative_time)):
        #    print "something's off."
        #------------------------
        # International passengers who arrived more than 90 mins before their flight get a refund if they miss
        if flight_type == "international" and (360.0 - relative_time ) > 90.0:
            self.gets_refund = True

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))

##########################
#### SIMULATION CLASS ####
##########################

class Simulation:
    """ Class used to house our whole simulation
    """
    def __init__(self):
        """ Sets up all the variables we need for the simulation
        """
        #----TIME----
        # Time variables
        self.system_time = 0.00
        self.delta = 0.01
        self.international_flight_number = 0   # = number of system iterations
        self.system_iteration = 0
        self.relative_global_time = 0.00

        #---MONEY---
        # Money variables
        # Revenue
        self.revenue_total = 0.0
        self.commuter_revenue = 0.0
        self.first_class_intl_revenue = 0.0
        self.coach_class_intl_revenue = 0.0
        # Losses
        self.refunds_issued = 0
        self.money_lost_to_refunds = 0.0
        self.wages_paid = 0.0
        self.cost_per_server = params.HOURLY_WAGE_OF_CHECKIN_AGENT
        self.cost_of_international_flight = params.OPERATING_COST_FOR_INTL_FLIGHT
        self.cost_of_commuter_flight = params.OPERATING_COST_FOR_DOMESTIC_FLIGHT
        # Constants
        self.commuter_ticket_price = params.COMMUTER_COACH_TICKET_COST
        self.intl_coach_ticket_price = params.INTL_COACH_TICKET_COST
        self.intl_first_class_ticket_price = params.INTL_FIRST_CLASS_TICKET_COST
        self.number_of_passengers_who_would_get_refund = 0
        self.refund_confirmation_number = 0


        #-----ARRIVALS-----
        # Arrival list
        self.international_first_class_ARRIVALS = []
        self.international_coach_class_ARRIVALS = []
        self.commuter_coach_class_ARRIVALS = []
        # All arrivals
        self.arrivals = [self.international_first_class_ARRIVALS,
                         self.international_coach_class_ARRIVALS,
                         self.commuter_coach_class_ARRIVALS]

        #----QUEUES-----
        # Check-in Queues - separate for first and coach
        self.first_class_check_in_QUEUE = CheckInQueue()
        self.coach_class_check_in_QUEUE = CheckInQueue()
        # Security Queues - also separate for first and coach
        self.first_class_security_QUEUE = SecurityQueue()
        self.coach_class_security_QUEUE = SecurityQueue()
        # All Queues
        self.queues = [self.first_class_check_in_QUEUE,
                       self.coach_class_check_in_QUEUE,
                       self.first_class_security_QUEUE,
                       self.coach_class_security_QUEUE]

        #------SERVERS-------
        # Check-in Servers
        self.first_class_CHECK_IN_server01 = CheckInServer()
        self.first_class_CHECK_IN_server01.is_first_class = True
        self.coach_class_CHECK_IN_server01 = CheckInServer()
        self.coach_class_CHECK_IN_server02 = CheckInServer()
        self.coach_class_CHECK_IN_server03 = CheckInServer()
        self.coach_class_CHECK_IN_server04 = CheckInServer()
        self.coach_class_CHECK_IN_server05 = CheckInServer()
        self.coach_class_CHECK_IN_server06 = CheckInServer()
        self.coach_class_CHECK_IN_server07 = CheckInServer()
        self.coach_class_CHECK_IN_server08 = CheckInServer()
        self.check_in_servers = [self.first_class_CHECK_IN_server01,
                                 self.coach_class_CHECK_IN_server01,
                                 self.coach_class_CHECK_IN_server02,
                                 self.coach_class_CHECK_IN_server03,
                                 self.coach_class_CHECK_IN_server04,
                                 self.coach_class_CHECK_IN_server05,
                                 self.coach_class_CHECK_IN_server06,
                                 self.coach_class_CHECK_IN_server07,
                                 self.coach_class_CHECK_IN_server08]
        # Security Servers
        self.first_class_SECURITY_server01 = SecurityServer()
        self.first_class_SECURITY_server01.is_first_class = True
        self.coach_class_SECURITY_server01 = SecurityServer()
        self.coach_class_SECURITY_server02 = SecurityServer()
        self.coach_class_SECURITY_server03 = SecurityServer()
        self.coach_class_SECURITY_server04 = SecurityServer()
        self.coach_class_SECURITY_server05 = SecurityServer()
        self.coach_class_SECURITY_server06 = SecurityServer()
        self.coach_class_SECURITY_server07 = SecurityServer()
        self.coach_class_SECURITY_server08 = SecurityServer()
        self.security_servers = [self.first_class_SECURITY_server01,
                                 self.coach_class_SECURITY_server01,
                                 self.coach_class_SECURITY_server02,
                                 self.coach_class_SECURITY_server03,
                                 self.coach_class_SECURITY_server04,
                                 self.coach_class_SECURITY_server05,
                                 self.coach_class_SECURITY_server06,
                                 self.coach_class_SECURITY_server07,
                                 self.coach_class_SECURITY_server08]
        # All servers
        self.servers = [self.first_class_CHECK_IN_server01,
                        self.coach_class_CHECK_IN_server01,
                        self.coach_class_CHECK_IN_server02,
                        self.coach_class_CHECK_IN_server03,
                        self.coach_class_CHECK_IN_server04,
                        self.coach_class_CHECK_IN_server05,
                        self.coach_class_CHECK_IN_server06,
                        self.coach_class_CHECK_IN_server07,
                        self.coach_class_CHECK_IN_server08,
                        self.first_class_SECURITY_server01,
                        self.coach_class_SECURITY_server01,
                        self.coach_class_SECURITY_server02,
                        self.coach_class_SECURITY_server03,
                        self.coach_class_SECURITY_server04,
                        self.coach_class_SECURITY_server05,
                        self.coach_class_SECURITY_server06,
                        self.coach_class_SECURITY_server07,
                        self.coach_class_SECURITY_server08]

        #-----GATE-----
        self.commuter_passengers_at_gate = 0
        self.international_passengers_at_gate = 0
        self.commuter_passengers_at_gate_list = []


        #-----FLIGHTS-----
        # HOW TO DEAL WITH INTERNATIONAL PASSENGERS WHO MISS THEIR FLIGHT?
        # Relative time vs. system time....
        self.time_until_commuter_flight = 30.00      # at start of simulation we are 30 mins until a commmuter flight
        self.time_until_international_flight = 0.00  # at start of simulation we have just had an int'l flight
        self.international_flight_departures = 0
        self.commuter_flight_departures = 0


        #----INTERNAL_DATA COLLECTION-----
        self.total_commuter_passengers_arrived = 0
        self.total_commuter_passengers_departed = 0
        self.total_intl_coach_passengers_arrived = 0
        self.total_intl_coach_passengers_departed = 0
        self.total_intl_first_class_passengers_arrived = 0
        self.total_intl_first_class_passengers_departed = 0
        self.intl_passengers_departed_combined = 0
        self.data_num_international_that_passengers_missed_flight = 0
        # Then counters to see how far people are making it in the system....
        # Averaged data
        self.time_in_system = []
        self.time_in_system_first_class = []
        self.avg_time_in_system = 0 # Later, should be sum(self.time_until_international_flight)
        self.avg_time_in_system_first_class = []
        self.time_in_system_coach = []
        self.time_in_system_commuter = []
        self.likelihood_intl_passenger_catches_plane = 0
        self.avg_wait_time_at_commuter_gate = 0
        self.INTL_passengers_who_missed_flight_and_not_refunded_time_arrived_before = []


        #-----INTERNAL MECHANISMS------
        self.data_users_added_to_COACH_CHECKIN_QUEUE = 0
        self.data_users_added_to_FIRSTCLASS_CHECKIN_QUEUE = 0
        self.data_users_added_to_COACH_SECURITY_QUEUE = 0
        self.data_users_added_to_FIRSTCLASS_SECURITY_QUEUE = 0
        self.data_users_moved_to_COMMUTER_GATE = 0
        self.data_users_moved_to_INTL_GATE = 0
        self.data_users_currently_in_system = 0
        self.total_server_idle_time = 0.0



    def generate_SIX_HOURS_of_arrivals(self):
        """ Generates six hours of arrivals and stores in our ARRIVAL LIST instance variables.
        """
        # Create instance of arrival class
        new_arrivals = Arrivals()
        # Generate new arrivals
        new_arrivals.get_arrivals()
        # Add one to the system iteration (denoted by international flight number)
        self.international_flight_number += 1

        # Transfer those values into our simulation, as arrivals for next six hours
        self.international_first_class_ARRIVALS = new_arrivals.intl_first_class_arrivals
        self.international_coach_class_ARRIVALS = new_arrivals.intl_coach_arrivals
        self.commuter_coach_class_ARRIVALS = new_arrivals.commuter_coach_arrivals

        # Count our arrivals for data collection
        self.total_commuter_passengers_arrived += len(new_arrivals.commuter_coach_arrivals)
        self.total_intl_coach_passengers_arrived += len(new_arrivals.intl_coach_arrivals)
        self.total_intl_first_class_passengers_arrived += len(new_arrivals.intl_first_class_arrivals)
        # can count how many arrivals SHOULD get refunds here, and then compare to how many actually ARE getting tagged
        coach_refunds = sum(i < 270 for i in self.international_coach_class_ARRIVALS)
        first_class_refunds = sum(i < 270 for i in self.international_first_class_ARRIVALS)
        self.refund_confirmation_number += coach_refunds
        self.refund_confirmation_number += first_class_refunds
        print "arrivals generated"

    def collect_revenue(self):
        """ Collects revenue from last set of arrivals
        """
        # Collect revenue for all international first class tickets
        for p in self.international_first_class_ARRIVALS:
            self.first_class_intl_revenue += self.intl_first_class_ticket_price
        # Add first class international ticket revenue to total
        self.revenue_total += self.first_class_intl_revenue

        # Collect revenue for all international coach class tickets
        for p in self.international_coach_class_ARRIVALS:
            self.coach_class_intl_revenue += self.intl_coach_ticket_price
        # Add coach class international ticket revenue to total
        self.revenue_total += self.coach_class_intl_revenue

        # Collect revenue for all commuter coach class tickets
        for p in self.commuter_coach_class_ARRIVALS:
            self.commuter_revenue += self.commuter_ticket_price
        # Add commuter revenue tot total
        self.revenue_total += self.commuter_revenue

    def update_servers(self):
        """ Updates servers after a change of DELTA in system time
        """
        for server in self.servers:
            server.update_service_time()

    def collect_and_create_passengers_from_arrivals(self):
        """ Looks at all arrival lists, and if there is new arrival at the current system time,
            creates a passenger object for use in the system, and places it in the check-in queue
        """
        current_time = self.system_time
        current_flight = self.international_flight_number
        relative_time = self.relative_global_time


        # make sure we're not checking an array that's empty
        if not len(self.international_first_class_ARRIVALS) == 0:
            # Then get next available item from INTL FIRST CLASS ARRIVALS
            if self.international_first_class_ARRIVALS[0] <= relative_time:
                # create passenger, put it in first class check in queue
                new_passenger = Passenger(self.system_time, "international", "first_class", self.international_flight_number,
                                          self.international_first_class_ARRIVALS[0])
                self.first_class_check_in_QUEUE.add_passenger(new_passenger)
                # pop from the list
                self.international_first_class_ARRIVALS.pop(0)
                # collect refund data
                if new_passenger.gets_refund:
                    self.number_of_passengers_who_would_get_refund += 1

        # make sure we're not checking an array that's empty
        if not len(self.international_coach_class_ARRIVALS) == 0:
            # Then get next available item from INTL COACH CLASS ARRIVALS
            if self.international_coach_class_ARRIVALS[0] <= relative_time:
                # create passenger, put it it in coach class check in queue
                new_passenger = Passenger(self.system_time, "international", "coach", self.international_flight_number,
                                          self.international_coach_class_ARRIVALS[0])
                self.coach_class_check_in_QUEUE.add_passenger(new_passenger)
                # pop from the list
                self.international_coach_class_ARRIVALS.pop(0)
                # collect refund data
                if new_passenger.gets_refund:
                    self.number_of_passengers_who_would_get_refund += 1

        # make sure we're not checking an array that's empty
        if not len(self.commuter_coach_class_ARRIVALS) == 0:
            # Then get next available item from COMMUTER COACH CLASS ARRIVALS
            if self.commuter_coach_class_ARRIVALS[0] <= relative_time:
                # create passenger, put it in coach class check in queue
                new_passenger = Passenger(self.system_time, "commuter", "coach", self.international_flight_number,
                                          self.commuter_coach_class_ARRIVALS[0])
                self.coach_class_check_in_QUEUE.add_passenger(new_passenger)
                # pop from the list
                self.commuter_coach_class_ARRIVALS.pop(0)

    def move_to_CHECK_IN_server(self):
        """ Look at check in servers, and if they are not busy, advance the first item in the correct queue
            to the correct (and open) check in server
        """
        #>>>>>> Later, change this go through all checkin servers in a loop and do same action.
        #       This code can be very much condensed

        # If first class check-in server is NOT busy
        if not self.first_class_CHECK_IN_server01.is_busy():
            # de-queue from the FIRST class check-in queue
            if not self.first_class_check_in_QUEUE.queue.empty():
                next_passenger = self.first_class_check_in_QUEUE.queue.get()
                self.first_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.first_class_CHECK_IN_server01.add_customer(next_passenger)

        # If coach check in server 01 is NOT busy
        if not self.coach_class_CHECK_IN_server01.is_busy():
            # de-queue from the COACH class check-in queue
            if not self.coach_class_check_in_QUEUE.queue.empty():
                next_passenger = self.coach_class_check_in_QUEUE.queue.get()
                self.coach_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.coach_class_CHECK_IN_server01.add_customer(next_passenger)

        # If coach check in server 02 is NOT busy
        if not self.coach_class_CHECK_IN_server02.is_busy():
            # de-queue from the COACH class check-in queue
            if not self.coach_class_check_in_QUEUE.queue.empty():
                next_passenger = self.coach_class_check_in_QUEUE.queue.get()
                self.coach_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.coach_class_CHECK_IN_server02.add_customer(next_passenger)

        # If coach check in server 03 is NOT busy
        if not self.coach_class_CHECK_IN_server03.is_busy():
            # de-queue from the COACH class check-in queue
            if not self.coach_class_check_in_QUEUE.queue.empty():
                next_passenger = self.coach_class_check_in_QUEUE.queue.get()
                self.coach_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.coach_class_CHECK_IN_server03.add_customer(next_passenger)

        # If coach check in server 04 is NOT busy
        if not self.coach_class_CHECK_IN_server04.is_busy():
            # de-queue from the COACH class check-in queue
            if not self.coach_class_check_in_QUEUE.queue.empty():
                next_passenger = self.coach_class_check_in_QUEUE.queue.get()
                self.coach_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.coach_class_CHECK_IN_server04.add_customer(next_passenger)

        # If coach check in server 05 is NOT busy
        if not self.coach_class_CHECK_IN_server05.is_busy():
            # de-queue from the COACH class check-in queue
            if not self.coach_class_check_in_QUEUE.queue.empty():
                next_passenger = self.coach_class_check_in_QUEUE.queue.get()
                self.coach_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.coach_class_CHECK_IN_server05.add_customer(next_passenger)

        # If coach check in server 06 is NOT busy
        if not self.coach_class_CHECK_IN_server06.is_busy():
            # de-queue from the COACH class check-in queue
            if not self.coach_class_check_in_QUEUE.queue.empty():
                next_passenger = self.coach_class_check_in_QUEUE.queue.get()
                self.coach_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.coach_class_CHECK_IN_server06.add_customer(next_passenger)

        # If coach check in server 07 is NOT busy
        if not self.coach_class_CHECK_IN_server07.is_busy():
            # de-queue from the COACH class check-in queue
            if not self.coach_class_check_in_QUEUE.queue.empty():
                next_passenger = self.coach_class_check_in_QUEUE.queue.get()
                self.coach_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.coach_class_CHECK_IN_server07.add_customer(next_passenger)

        # If coach check in server 08 is NOT busy
        if not self.coach_class_CHECK_IN_server08.is_busy():
            # de-queue from the COACH class check-in queue
            if not self.coach_class_check_in_QUEUE.queue.empty():
                next_passenger = self.coach_class_check_in_QUEUE.queue.get()
                self.coach_class_check_in_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.coach_class_CHECK_IN_server08.add_customer(next_passenger)



    def update_check_in_queues(self):
        """ Updates queues after a change of DELTA in system time
        """
        # then check the servers, and if they're free move from queue to server
        self.move_to_CHECK_IN_server()
        # Check all arrivals and if the arrival time matches system time...
        # Create a passenger and ADD the correct queue
        self.collect_and_create_passengers_from_arrivals()


    def update_security_queues(self):
        """ Updates queues after a change of DELTA in system time
        """
        # Check all check-in servers...  and if they are NOT busy, take their passenger...
        # Take the passenger, add the correct security queue

        # First, look at all servers
        for server in self.check_in_servers:
            # and if the server is NOT busy
            # if not server.is_busy():
            #if not server.last_customer_served.empty():
                # Take the passenger, who must have just finished being served
                my_passenger = server.complete_service()
                # and move them to the correct security queue
                if not my_passenger == None:
                    # but first make sure that the passenger does not == None
                    if my_passenger.flight_class == "coach":
                        # add to coach security queue
                        self.coach_class_security_QUEUE.add_passenger(my_passenger)
                        # else, add to first class security queue
                    else:
                        # because if they are NOT coach, they must be first class
                        self.first_class_security_QUEUE.add_passenger(my_passenger)


    def move_to_SECURITY_server(self):
        """ If servers are not busy, advance next passenger in the security queue to to security server
        """
        # step through all the security servers and check if they are busy
        for server in self.security_servers:
            # if the server isn't busy, we can take the next passenger from security queue
            # and put him in the server
            if not server.is_busy():
            #if not server.last_customer_served.empty():
                # if server is first class, take a passenger from the first class security queue
                if server.is_first_class == True:
                    # first make sure it's not empty
                    if not self.first_class_security_QUEUE.queue.empty():
                        # and if it's not, grab the next passenger out of it
                        next_passenger = self.first_class_security_QUEUE.queue.get()
                        self.first_class_security_QUEUE.queue.task_done()
                        # And move that passenger into the available security server
                        server.add_customer(next_passenger)
                # else, take the passenger from the commuter class security queue
                else:
                    # first make sure it's not empty
                    if not self.coach_class_security_QUEUE.queue.empty():
                        # and if it's not, grab the next passenger out of it
                        next_passenger = self.coach_class_security_QUEUE.queue.get()
                        self.coach_class_security_QUEUE.queue.task_done()
                        # And move that passenger into the available security server
                        server.add_customer(next_passenger)

    def move_to_GATE(self):
        """ Look at Security servers, and if they are NOT busy, someone just finished security screening.
            This means they've completed the queuing process.
            ---
            Once through queuing, go to GATE.
            Commuters --> Go straight to gate waiting area
            International --> First check if they missed their flight.
                - If yes:  They leave
                - If no:   They go to international gate
        """
        # step through all the security servers
        for server in self.security_servers:
            # if the server is NOT busy
            #if not server.is_busy():
            #if not server.last_customer_served.empty():
                # passenger has completed queuing phase, and can move to gate.
                # but first, we need to check if they are commuters or international flyers
                # and in each case, need to handle that accordingly
                next_passenger = server.complete_service()
                # first make sure that the passenger isn't a NONE
                if not next_passenger == None:
                    # if the passenger is a commuter, they just go to gate
                    if next_passenger.type_of_flight == "commuter":
                        self.commuter_passengers_at_gate += 1
                        self.data_users_moved_to_COMMUTER_GATE += 1
                        self.commuter_passengers_at_gate_list.append(self.system_time)
                        # data collection for coach
                        time_in_system = self.system_time - next_passenger.system_time_entered
                        self.time_in_system.append(time_in_system)
                        self.time_in_system_coach.append(time_in_system)
                        # data collection for commuters
                        self.time_in_system_commuter.append(time_in_system)
                        self.time_in_system_coach.append(time_in_system)
                    # else, they are international travelers, and we need to check if they missed their flight
                    else:
                        self.check_if_international_passenger_missed_flight(next_passenger)

    def check_if_international_passenger_missed_flight(self, passenger_to_check):
        """ Checks if an international passenger that has completed this gauntlet is on time!
        """
        # first, check if they made their flight --> is TRUE if the system iteration equals current flight number
        if passenger_to_check.international_flight_number == self.international_flight_number:
            self.international_passengers_at_gate += 1
            self.data_users_moved_to_INTL_GATE += 1
        # ----BELOW HERE, MISSED FLIGHT-------
        # Else, check if they arrived more than 90 minutes BEFORE their flight
        elif passenger_to_check.gets_refund == True:
            # handle refund issue
            self.data_num_international_that_passengers_missed_flight += 1
            self.issue_refund(passenger_to_check)
        # ELSE:  if they DON'T get a refund, and they missed their flight... they just leave.
        #        by not moving them to the international passenger gate, they are effectively exiting the system.
        #        That is, they are no longer accounted for at all.
        else:
            self.data_num_international_that_passengers_missed_flight += 1
            time_arrived_BEFORE_flight = passenger_to_check.system_time_entered/passenger_to_check.international_flight_number
            self.INTL_passengers_who_missed_flight_and_not_refunded_time_arrived_before.append(time_arrived_BEFORE_flight)

        # for everyone --> collect data, so we can compare
        if passenger_to_check.flight_class == "coach":
            self.total_intl_coach_passengers_departed += 1
            # data collection
            time_in_system = self.system_time - passenger_to_check.system_time_entered
            self.time_in_system.append(time_in_system)
            self.time_in_system_coach.append(time_in_system)
        else:
            self.total_intl_first_class_passengers_departed += 1
            # data collection
            time_in_system = self.system_time - passenger_to_check.system_time_entered
            self.time_in_system.append(time_in_system)
            self.time_in_system_first_class.append(time_in_system)

    def issue_refund(self, passenger):
        """ Issue a refund to international passengers who missed flight,
            but arrived more than 90 minutes early
        """
        self.refunds_issued += 1
        if passenger.flight_class == "coach":
            self.revenue_total -= self.intl_coach_ticket_price
            self.coach_class_intl_revenue -= self.intl_coach_ticket_price
            self.money_lost_to_refunds += self.intl_coach_ticket_price
        else:
            self.revenue_total -= self.intl_first_class_ticket_price
            self.first_class_intl_revenue -= self.intl_first_class_ticket_price
            self.money_lost_to_refunds += self.intl_first_class_ticket_price

    def check_if_commuter_plane_departs(self):
        """ Models departure of a commuter plane. Occurs every 30 mins. takes 50 people from the GATE for commuters.
        """
        # If system_time/30.0 is an integer --> commuter plane is departing
        if self.time_until_commuter_flight <= 0.0:
            # and we take 50 passengers at the commuter gate
            self.commuter_passengers_at_gate -= 50
            # if we take too many passengers putting the gate count into negatives,
            # set the number at gate back to zero
            if self.commuter_passengers_at_gate < 0:
                self.commuter_passengers_at_gate = 0

            # reset counter
            self.time_until_commuter_flight = 60.0
            self.commuter_flight_departures += 1

            # find out how long each passenger we take has been waiting
            current_system_time = self.system_time
            passenger_wait_time_for_group = 0
            line_length = len(self.commuter_passengers_at_gate_list)
            counter = 0
            for passenger in range(0,50):
                if passenger < line_length:
                    counter += 1
                    time_arrived_at_gate = self.commuter_passengers_at_gate_list[0]
                    passenger_wait_time_for_group += current_system_time - time_arrived_at_gate
                    self.commuter_passengers_at_gate_list.pop(0)
            if counter > 0:
                group_average = passenger_wait_time_for_group/counter
                self.total_commuter_passengers_departed += counter
                self.avg_wait_time_at_commuter_gate += group_average


    def check_if_international_plane_departs(self):
        """ Models departure of an international plane. Occurs every 6 hours. Takes EVERYONE at gate.
        """
        # If system_time/360.0 is an integer --> then an international plane is departing
        if self.time_until_international_flight <= 0.0:
            # update our data set, to be sure all is working
            self.intl_passengers_departed_combined += self.international_passengers_at_gate

            # and we take everyone at the international gate
            self.international_passengers_at_gate = 0

            # reset counter
            self.time_until_international_flight = 360.0
            self.international_flight_departures += 1


    def every_six_hours_deduct_operating_costs(self):
        """ Deducts operating costs of flights and servers for past 6 hours.
        """
        num_servers = 0
        for server in self.check_in_servers:
          num_servers += 1

        total_hours_worked = num_servers * 6
        total_operating_costs = total_hours_worked * self.cost_per_server

        self.wages_paid += total_operating_costs

    def at_end_of_simulation_deduct_flight_costs(self):
        cost_of_domestic_flights = params.OPERATING_COST_FOR_DOMESTIC_FLIGHT * self.commuter_flight_departures
        cost_of_intl_flights = params.OPERATING_COST_FOR_INTL_FLIGHT * self.international_flight_departures
        print "Cost of domestic flights="+str(cost_of_domestic_flights)
        print "Cost of international flights="+str(cost_of_intl_flights)
        self.revenue_total -= cost_of_domestic_flights
        self.revenue_total -= cost_of_intl_flights

    def advance_system_time(self):
        """ Advances the system time by delta --> .01 of a minute
            - Looks for arrivals at current time
            - If an arrival is valid, create a passenger object and place it in the proper Queue
            - Needs to update EVERY QUEUE and SERVER, advance wherever needed
        """
        # every six hours, generate new arrivals,
        # and perform accounting procedures on ticket
        # for those arrivals
        #if self.time_until_international_flight <= 0.0:
        #    self.generate_SIX_HOURS_of_arrivals()
        #    self.collect_revenue()
        #    self.every_six_hours_deduct_operating_costs()


        # increment the system time by delta
        self.system_time += self.delta
        self.time_until_commuter_flight -= self.delta
        self.time_until_international_flight -= self.delta

        # keep track of relative global time
        self.relative_global_time += self.delta
        if self.relative_global_time >= 360.0:
            self.relative_global_time = 0.0

        #print "gets system time update"
        """ Old version, just shifting order to see if we can fix why no one
            can move past the CHECK IN SERVERS. Think the updates aren't timed correctly.


        # skip these on the first iteration because we don't have data yet
        if not self.international_flight_number == 0:
            # update all the servers
            self.update_servers()
            #print "gets past update server"

            # check arrivals, and if someone should enter the system, put them in the correct check-in queue
            # And, if we can move someone to any of the check in servers, do it
            self.update_check_in_queues()
            #print "updates check in queues"

            # and if we can, move passengers to the security server
            self.move_to_SECURITY_server()
            #print "moves to security server"

            # update then the security queues
            self.update_security_queues()
            #print "updates security queues"

            # if we can move everyone to gate, do it
            self.move_to_GATE()
            #print "moves to gate"

        """
        # skip these on the first iteration because we don't have data yet
        if not self.international_flight_number == 0:

            #DO IT IN REVERSE ORDER
            # start by updating the servers
            self.update_servers()
            # then, if we can pull someone FROM a sever, while not busy, do it
            self.move_to_GATE()
            self.update_security_queues()
            # then get passengers from arrivals, and fill the queues
            self.collect_and_create_passengers_from_arrivals()
            # then move people into any empty spots in the servers
            self.move_to_SECURITY_server()
            self.move_to_CHECK_IN_server()

        # every six hours, generate new arrivals,
        # and perform accounting procedures on ticket
        # for those arrivals
        if self.time_until_international_flight <= 0:
            self.generate_SIX_HOURS_of_arrivals()
            self.collect_revenue()
            self.every_six_hours_deduct_operating_costs()

        # check if planes should be departing
        self.check_if_commuter_plane_departs()
        self.check_if_international_plane_departs()
        #print "checks if planes depart"

        # print self.system_time

    def run_simulation(self, simulation_time_in_days):
        """ Use this to run simulation for as long as user has specified, in days
            While the counter < # of days, keep generating the arrivals every 6 hours
            and stepping through the simulation
        """
        simulation_time_in_minutes = simulation_time_in_days * 24 * 60
        # = days * 24 hours in a day * 60 minutes in an hour
        while self.system_time < simulation_time_in_minutes:
            # then, advance system time by delta:  0.01
            self.advance_system_time()
        self.at_end_of_simulation_deduct_flight_costs()
        print "SIMULATION COMPLETE:"
        print "Total revenue collected="+str(self.revenue_total)

    #############################################
    ####### DATA REPORTING AND ANALYSIS #########
    #############################################

    def print_simulation_results(self):
        """ prints the results of our simulation to the command line/console
        """
        print "###################################"
        print "####### SIMULATION RESULTS ########"
        print "###################################"
        print "#--------Money---------"
        print "TOTAL PROFIT MADE="+str(self.revenue_total-self.money_lost_to_refunds-self.wages_paid)
        #print "Revenue from COMMUTER flights="+str(self.commuter_revenue)
        #print "Revenue from FIRST class INTERNATIONAL flights="+str(self.first_class_intl_revenue)
        #print "Revenue from COACH class INTERNATIONAL flights="+str(self.coach_class_intl_revenue )
        print "Refunds issued="+str(self.refunds_issued)
        print "Money lost to refunds="+str(self.money_lost_to_refunds)
        print "Wages paid, total="+str(self.wages_paid)
        print "Number of passengers who would get a refund if they don't make it on time="+str(self.number_of_passengers_who_would_get_refund)
        print "Confirmation number of passengers who get refund="+str(self.refund_confirmation_number)
        print "#-----System Info-----"
        print "Note: --> 'ARRIVED' means 'entered system' ;;; 'DEPARTED' means 'left system', whether a flight was made OR missed."
        print "Total COMMUTER passengers ARRIVED="+str(self.total_commuter_passengers_arrived)
        print "Total COMMUTER passengers DEPARTED="+str(self.total_commuter_passengers_departed)
        print "Total INTERNATIONAL first class passengers ARRIVED="+str(self.total_intl_first_class_passengers_arrived)
        print "Total INTERNATIONAL first class passengers DEPARTED="+str(self.total_intl_first_class_passengers_departed)
        print "Total INTERNATIONAL coach class passengers ARRIVED="+str(self.total_intl_coach_passengers_arrived)
        print "Total INTERNATIONAL coach class passengers DEPARTED="+str(self.total_intl_coach_passengers_departed)
        total_intl_departs = self.total_intl_first_class_passengers_departed + self.total_intl_coach_passengers_departed
        print "Total INTERNATIONAL passengers (all types) DEPARTED="+str(total_intl_departs)
        print "-------Averages-------"
        sum_time_in_system = sum(self.time_in_system)
        length_of_time_in_system_list = len(self.time_in_system)
        length_of_time_in_system_list = float(length_of_time_in_system_list)
        #print "SUM OF TIME IN SYSTEM: "+str(sum_time_in_system)
        #print "LENGTH OF TIME IN SYSTEM: "+str(length_of_time_in_system_list)
        self.avg_time_in_system = sum(self.time_in_system)/len(self.time_in_system)
        print "AVG Time In System for users who make it to a gate="+str(self.avg_time_in_system)
        self.time_in_system.sort(reverse=True)
        longest_time_in_system = self.time_in_system.pop(0)
        print "Longest time in system="+str(longest_time_in_system)
        average_time_in_system_first_class = sum(self.time_in_system_first_class)/len(self.time_in_system_first_class)
        print "AVG Time in system FIRST CLASS="+str(average_time_in_system_first_class)
        average_time_in_system_coach = sum(self.time_in_system_coach)/len(self.time_in_system_coach)
        print "AVG Time in system all COACH="+str(average_time_in_system_coach)
        average_time_in_system_commuters = sum(self.time_in_system_commuter)/len(self.time_in_system_commuter)
        print "AVG Time in system COMMUTERS="+str(average_time_in_system_commuters)
        print "------Internal Mechanisms-------"
        print ".......Stage 1......"
        print "Users added to COACH CheckInQueues="+str(self.coach_class_check_in_QUEUE.customers_added)
        print "Users added to FIRSTCLASS CheckInQueue="+str(self.first_class_check_in_QUEUE.customers_added)
        print "......Stage 2......."
        print "Users added to COACH SecurityQueue="+str(self.coach_class_security_QUEUE.customers_added)
        print "Users added to FIRSTCLASS SecurityQueue="+str(self.first_class_security_QUEUE.customers_added)
        print "......Stage 3......."
        print "Users moved to INTL_GATE="+str(self.data_users_moved_to_INTL_GATE)
        print "Users moved to COMMUTER GATE="+str(self.data_users_moved_to_COMMUTER_GATE)
        print ". . . . didn't make it . . . . ."
        still_in_system = 0
        for queue in self.queues:
            still_in_system += queue.queue.qsize()
        waiting_at_gate = self.commuter_passengers_at_gate
        waiting_at_gate += self.international_passengers_at_gate
        print "Users waiting at a GATE="+str(waiting_at_gate)
        print "Users STILL in SYSTEM="+str(still_in_system)
        print "NUMBER OF International passengers that missed their flight="+str(self.data_num_international_that_passengers_missed_flight)
                # print shorted time in the list.... of missed int'l flights
        # make this reverse=true to check it
        self.INTL_passengers_who_missed_flight_and_not_refunded_time_arrived_before.sort()
        print ". . . confirm system works . . ."
        print "Of INTERNATIONAL passengers who missed flights and NOT refunded, \nearliest arrival was this long before " \
              "the flight was scheduled to depart: "+str(360 - self.INTL_passengers_who_missed_flight_and_not_refunded_time_arrived_before.pop(0))

        print "======= GOALS ========"
        self.likelihood_intl_passenger_catches_plane = self.data_users_moved_to_INTL_GATE / float(self.data_users_moved_to_INTL_GATE + self.data_num_international_that_passengers_missed_flight)
        print "Likelihood that INTERNATIONAL Passenger catches plane="+str(self.likelihood_intl_passenger_catches_plane)
        self.avg_wait_time_at_commuter_gate = self.avg_wait_time_at_commuter_gate/self.commuter_flight_departures
        print "Post-Security Wait Time for COMMUTER Passengers, AVG="+str(self.avg_wait_time_at_commuter_gate)
        self.total_server_idle_time = 0.0
        for server in self.check_in_servers:
            if not server.is_first_class:
                self.total_server_idle_time += server.idle_time
        print "AGENTS' Total Idle Time="+str(self.total_server_idle_time)
        server_count = len(self.servers)
        print "AGENTS AVG IDLE TIME="+str(self.total_server_idle_time/server_count)

    def goal_reporting(self):
        # maximize profit
        # minimize check-in wait time (esp for first class)
        #   --> need to start collecting check-in wait times
        # Maximize likelihood that international passengers catches plane
        #   --> already have this
        # Minimize post-security screening wait time for commuter passengers
        #   --> need to start storing the passengers, or at least their times in a list
        #       then removing top 50 items from that list, and when we do it, iterate through
        #       the list and calculate (entered_time - current_system_time)
        #       then take the average and print it
        # Minimize agents' idle time
        #   --> need to put a counter for idle time in at each server, if incremented and
        #       their queue is empty... or just False... not busy, then increment idle time
        return

    def actions(self):
        # reallocate check-in agents
        # increase number of check-in agents (can be up to 6)
        # change number of commuter flights per day
        return
