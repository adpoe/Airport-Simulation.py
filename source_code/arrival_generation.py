import variate_generators as vg


"""
These are passenger arrival generation mechanisms for an airport simulation that can be initiated in 'main.py'.
This class will generate 6 hours worth of passenger arrivals, and store the data in two arrays:
- One for commuters passengers
- One for international passengers

For each passenger, also need to generate their wait times for each queue. Or is that done when a passenger queues up?

"""

###########################
### ARRIVAL GENERATION ####
###########################
# Generate next 6 hours of arrivals for:
# 1. International Flights
# 2. Commuter flights

def generate_six_hours_of_commuter_arrivals():
    """
    Generate six hours of commuter arrivals by pulling numbers from the commuter arrival variate generator
    UNTIL the total time for arrivals is >= 6 hours.

    We're getting time from this distro in minutes, so we can just keep a running total.

    Each individual arrival time should be stored in an array. These times are each relative to the LAST time generated.

    NOTE:   >>> If we generate an arrival that comes after the 6 hour period, it will be discarded, never read <<<
    :return: An array of commuter arrival times.
    """
    # variables we need
    commuter_arrival_times = []
    six_hours_of_arrivals = 360.0 # = 6 hours * 60 minutes, so this is time in minutes
    total_arrival_time_in_this_6_hour_segment = 0.0

    # main loop to generate arrivals
    while total_arrival_time_in_this_6_hour_segment <= six_hours_of_arrivals:
        # generate next arrival
        next_arrival = vg.gen_commuter_arrivals_at_airport()
        # update the total arrival time
        total_arrival_time_in_this_6_hour_segment += next_arrival
        # add that arrival to our array of commuter arrivals
        commuter_arrival_times.append(total_arrival_time_in_this_6_hour_segment)

        # If we get an arrival that is over 6 hours, that's okay. It will be discarded.

    return commuter_arrival_times




def generate_six_hours_first_class_intl_arrivals():
    """
    Generate six hours of international arrivals by pulling numbers from the international arrival variate generator.
    To do this, we first use the BINOMIAL to determine how many first class tickets were sold.
    THEN --> Generate that many numbers. Where each distributed number is the amount of time BEFORE the flight that
    this passenger arrived.

    Also, do we need to transform these into numbers RELATIVE to the departure time?
    How long into the simulation they entered?

    Later, we'll need to know how far ahead these passengers arrived, so probably useful to keep this number somewhere.
    Generally, need a flag next to each passenger before they are put in Queue, telling us what they're on. Hard
    part is that commuter coach and international coach passengers mix in the coach queue....
    Maybe, take that into account here... or later. not sure yet.
    :return: array of international first class arrival times.
    """
    # variables we need
    international_first_class_arrival_times = []
    number_of_first_class_tickets_sold = vg.gen_number_of_intl_first_class_seats_sold()

    # generate as many arrivals as we have tickets sold
    counter = 0
    while counter < number_of_first_class_tickets_sold:
        # generate nth arrival
        arrival_time = vg.gen_international_arrivals_via_polar_coords()
        # Transform the time to be relative to the next departure
        departure_time = 360.0
        arrival_time_BEFORE_departure = departure_time - arrival_time
        # add that arrival to our array of commuter arrivals
        international_first_class_arrival_times.append(arrival_time_BEFORE_departure)
        # update the counter
        counter += 1

    # Need to sort the arrivals when we're done
    international_first_class_arrival_times.sort()
    # Should be ascending order. Print this out to confirm it.

    return  international_first_class_arrival_times



def generate_six_hours_coach_intl_arrivals():
    """
    Generate six hours of international arrivals by pulling numbers from the international arrival variate generator.
    To do this, we first use the BINOMIAL to determine how many first class tickets were sold.
    THEN --> Generate that many numbers. Where each distributed number is the amount of time BEFORE the flight that
    this passenger arrived.

    Also, do we need to transform these into numbers RELATIVE to the departure time?
    How long into the simulation they entered?

    Later, we'll need to know how far ahead these passengers arrived, so probably useful to keep this number somewhere.
    Generally, need a flag next to each passenger before they are put in Queue, telling us what they're on. Hard
    part is that commuter coach and international coach passengers mix in the coach queue....
    Maybe, take that into account here... or later. not sure yet.
    :return: array of international first class arrival times.
    """
    # variables we need
    international_coach_arrival_times = []
    number_of_coach_tickets_sold = vg.gen_number_of_intl_coach_seats_sold()

    # generate as many arrivals as we have tickets sold
    counter = 0
    while counter < number_of_coach_tickets_sold:
        # generate nth arrival
        arrival_time = vg.gen_international_arrivals_via_polar_coords()
        # Transform the time to be relative to the next departure
        departure_time = 360.0
        arrival_time_BEFORE_departure = departure_time - arrival_time
        # add that arrival to our array of commuter arrivals
        international_coach_arrival_times.append(arrival_time_BEFORE_departure)
        # update the counter
        counter += 1

    # Need to sort the arrivals when we're done
    international_coach_arrival_times.sort()
    # Should be ascending order. Print this out to confirm it.

    return  international_coach_arrival_times



##########################################
###### GENERATORS FOR SERVICE TIME #######
##########################################

def gen_check_in_service_time_per_passenger( passenger_type ):
    """
    Generate total service time per check in, per passenger
    :param passenger_type: "commuter", or "international"
    :return: total service time, per passenger
    """
    total_service_time = 0.0
    number_of_bags = 0

    # Generate correct number of bags, determined by passenger type
    if passenger_type == "commuter":
        number_of_bags = vg.gen_number_of_carry_on_items__for_COMMUTER_passenger()
    else:
        number_of_bags = vg.gen_number_of_carry_on_items__for_INTL_passenger()

    # 1.  Get service time to print boarding pass
    total_service_time += vg.gen_print_boarding_pass_time()

    # 2.  Get service time to check all bags
    counter = 0
    while counter < number_of_bags:
        total_service_time += vg.gen_time_to_check_bag()
        counter += 1

    # 3.  Get service time for other delays
    total_service_time += vg.gen_time_for_other_problems_and_delays()

    return total_service_time


def gen_security_screening_time():
    """
    Generates service time for a security screening
    :return: the service time for an individual passenger
    """
    return vg.gen_avg_service_time_for_security_screening_machine()

