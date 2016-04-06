###############################
### TIME ADVANCE MECHANISMS ###
###############################
# Maybe do next-event time advance? --> generate for 6hours at time... up until an international flight..
# then.... advance to next event each time, add to queue, until we're at flight.... then redo.....


# Fixed-increment time advance will work.... and probably easier  <<<<<
# This way, just check if the next value in either array.... hm undecided.
# 1. Simulation clock initialized to zero
# advance by 1/100th of a minute.  Easier.
simulation_time = 0.00
# 2. Increment clock by a fixed amount (delta T)  -- 1 second?
deltaTime = 0.01

# 3. Check to see if one or more events should have occurred during the previous interval of length delta T
# For commuter flights, I get time until next arrival, but how often to check that?
# 4. If so, consider them to occur at the end of the interval, update system state state variables

# Time Constants, all in MINUTES
# --- Calling a month 30 days, even though this varies.
# A day is 60 mins * 24 hours
day = 60.0 * 24.0  # = 1440 mins
month = day * 30   # = 43200 mins
year = month * 12  # = 51840 mins

##################
### CONSTANTS ####
##################

# Flight departure constants, in minutes
COMMUTER_FLIGHT_DEPARTURE_INTERVAL = 60.0
INTL_FLIGHT_DEPARTURE_INTERVAL = 500.0

# Capacity for our flights
COMMUTER_FLIGHT_CAPACITY = 50.0
INTL_FLIGHT_CAPACITY_COACH = 150.0
INTL_FLIGHT_CAPACITY_FIRST = 50.0
INTL_FLIGHT_CAPACITY_TOTAL = INTL_FLIGHT_CAPACITY_COACH + INTL_FLIGHT_CAPACITY_FIRST

# Probabilities of filling Int'l flight seats
CHANCE_OF_FILLING_FIRSTCLASS_SEAT = 0.80
CHANCE_OF_FILLING_COACH_SEAT = 0.85

# Demand
# Assumed:  Identical for all flights, all times of day

# Ticket Costs for our Flights
INTL_FIRST_CLASS_TICKET_COST = 1000.0
INTL_COACH_TICKET_COST = 500.0
COMMUTER_COACH_TICKET_COST = 200.0

# Operating Costs
OPERATING_COST_FOR_INTL_FLIGHT = 10000.0      # $10k
OPERATING_COST_FOR_DOMESTIC_FLIGHT = 1000.0   # $1k
HOURLY_WAGE_OF_CHECKIN_AGENT = 25.0           # $25/hour
MAX_ACCEPTABLE_COST_OF_LABOR = 0.05           # 5% of total revenue

# Check in counters
MAX_CHECK_IN_COUNTERS = 6.0


###################
### PARAMETERS ####
###################

# Check in counters
FIRST_CLASS_CHECK_IN_COUNTERS = 1.0
COMMUTER_CHECK_IN_COUNTERS = 3.0
# When counters are all full --> passengers wait in lines
# Two separate lines, one or each class of passengers.
CUSTOMERS_IN_FIRST_CLASS_CHECK_IN_QUEUE = 0.0
CUSTOMERS_IN_COMMUTER_CHECK_IN_QUEUE = 0.0

# Security screening
# Again, two separate waiting lines here. One for 1st class, and one for coach.
NUM_SECURITY_SCREENING_MACHINES_FOR_FIRST_CLASS = 1.0
NUM_SECURITY_SCREENING_MACHINES_FOR_COACH = 2.0
CUSTOMERS_IN_FIRST_CLASS_SCREENING_QUEUE = 0.0
CUSTOMERS_IN_COMMUTER_SCREENING_QUEUE = 0.0

# Gate area
NUM_COMMUTER_PASSENGERS_IN_QUEUE_AT_GATE = 0.0


