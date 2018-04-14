from scripts import jobsGenerator as J, batteriesGenerator as B, pricing as PR, \
    scheduleJob3 as SJ, aggregateLoads as AL, frankWolfe4 as FW2, \
    writeResults as WR, inputs as P, computeCosts2 as CC, \
    readFiles as RF, scheduleBattery2 as SB
from scripts.inputs import lookup_param, i_bill, i_penalty, interval, \
    no_intervals_day, no_pricing_periods, no_jobs_min, no_jobs_max, penalty_coefficient, randomization
from time import time
from sys import argv

if len(argv) > 1:
    P.no_houses = int(argv[1])

if len(argv) > 2:
    P.no_itrs = int(argv[2])

# lookup_file = ""
lookup_file = 'files/lookup-0.csv'
# lookup_file = 'files/lookup-100-zero-threshold9-flu.csv'
P.lookup_base = RF.main(lookup_file)

# Generate data
community = J.main(P.load_data)
no_houses = len(community)

batteries = B.main(P.battery_data)
no_batteries = len(batteries)

if P.use_battery == 0:
    no_batteries = "No"

headers = ["house"] + [i + 1 for i in range(no_pricing_periods)]
s_loads_houses = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\n"

loads = AL.main(community)
lookup_coeff = max(loads) * lookup_param
total_penalty = 0

# -------------------- Meta data of this experiment --------------------
print str(no_houses) + " houses, " + str(no_jobs_min) + " ~ " + str(no_jobs_max) + " jobs per house, " + str(no_batteries) + " batteries."
print str(no_intervals_day) + " scheduling periods, " + str(no_pricing_periods) + " pricing periods, "
print str(P.no_itrs) + " iterations"
print "---------------"

headers = ["households", "batteries", "maxJobs", "minJobs", "lookupf", "lookupfile", "notes", "unhappinessf", "schedulingp", "time",
           "fw_time", "pricing_time", "scheduling_time"]
s_overview = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\n"
if not lookup_file == "":
    lookup_file = lookup_file
    notes = lookup_file
    # notes = lookup_file[lookup_file.index("lookup") + len("lookup") + 1: lookup_file.index("-zero")] + "% renewable."
else:
    lookup_file = ""
    notes = ""
s_overview += str(no_houses) + "," + str(no_batteries) + "," + str(no_jobs_max) + "," + str(no_jobs_min) + "," \
              + str(lookup_coeff) + "," + str(lookup_file) + "," + str(notes) + "," + str(penalty_coefficient) + "," \
              + str(no_intervals_day) + ","

headers = ["itr", "type", "tbill", "tpenalty"]
s_costs = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\n"

headers = ["prices"] + [i + 1 for i in range(no_pricing_periods)]
s_lookup = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\n"
for row in P.lookup_base:
    rows = ""
    for index, item in enumerate(row):
        if index == 0:
            rows += str(item)
        else:
            rows += "," + str(item * lookup_coeff)
    s_lookup += rows + "\n"

headers = ["itr", "type"] + [i + 1 for i in range(no_pricing_periods)]
s_loads = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\n"
s_loads += "0," + "o," + str(loads)[1:-1].replace(" ", "") + "\n"
s_loads += "0," + "f," + str(loads)[1:-1].replace(" ", "") + "\n"
s_prices = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\n"

headers = ["itr", "alpha", "fw_itrs_t", "fw_itrs"]
s_fw = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\n"

# -------------------- Meta data of this experiment --------------------

t_begin = t_end = time()
t_fw_total = 0
t_pricing_total = 0
t_scheduling_total = 0
counter_fw = -1

for itr in range(P.no_itrs + 1):
    # print "========"
    # print "Iteration " + str(itr)

    # pricing
    t_pricing = time()
    prices = PR.main(loads, lookup_coeff)
    t_pricing_total += time() - t_pricing
    s_prices += str(itr) + "," + "o," + str(prices)[1:-1].replace(" ", "") + "\n"

    prices_long = [p for p in prices for i in xrange(interval)]
    sorted_periods = sorted(range(len(prices_long)), key=lambda x: prices_long[x])
    flag_schedule_battery = 1
    if prices_long[sorted_periods[0]] == prices_long[sorted_periods[-1]] or P.use_battery == 0:
        flag_schedule_battery = 0

    # total cost
    total_cost = CC.main(prices=prices, loads=loads, coefficient=lookup_coeff)
    # print "obj = " + str(total_cost + total_penalty)
    s_costs += str(itr) + "," + "f," + str(total_cost) + "," + str(total_penalty) + "\n"

    if itr == P.no_itrs or counter_fw == 0:
        t_end = time()
        s_overview += str(t_end - t_begin) + "," + str(t_fw_total) + "," + str(t_pricing_total) + "," \
                      + str(t_scheduling_total) + "\n"
        break

    # start new iteration
    s_itr = itr + 1
    loads_pre = loads[:]
    total_penalty_pre = total_penalty
    loads = [0] * no_intervals_day
    total_penalty = 0

    # scheduling and aggregating demand
    t_scheduling_begin = time()
    # id_h = -1
    for household, battery in zip(community, batteries):
        # id_h += 1
        # print "house " + str(id_h)

        # scheduling jobs
        loads_household = [0] * no_intervals_day
        for job in household:
            job, loads_household = SJ.main(job, prices_long, loads_household)
            total_penalty += job[i_penalty]

        # scheduling the battery
        p
        if flag_schedule_battery == 1:
            if itr == 0:
                battery['energy'] = [battery['min']] * P.no_intervals_day
                battery['activities'] = [0] * P.no_intervals_day
            battery, loads_household = SB.main(battery, sorted_periods[:], loads_household, prices_long)

        # aggregating loads
        loads = [x + y for x, y in zip(loads, loads_household)]
        p
    t_scheduling_total += time() - t_scheduling_begin
    s_loads += str(s_itr) + "," + "o," + str(loads)[1:-1].replace(" ", "") + "\n"
    # print "scheduling: " + str(time() - t_scheduling_begin) + "s"

    # total demand per pricing period
    loads = [sum([loads[i + j] for j in xrange(interval)]) for i in xrange(no_intervals_day) if i % interval == 0]

    # frank-Wolfe
    t_fw_begin = time()
    loads, prices_fw, total_penalty, alpha, counter_fw = \
        FW2.main(loads, loads_pre, prices, total_penalty, total_penalty_pre, lookup_coeff)
    t_fw_itr = time() - t_fw_begin
    t_fw_total += t_fw_itr

    s_loads += str(s_itr) + "," + "f," + str(loads)[1:-1].replace(" ", "") + "\n"
    s_prices += str(s_itr) + "," + "f," + str(prices_fw)[1:-1].replace(" ", "") + "\n"
    s_fw += str(s_itr) + "," + str(alpha) + ", " + str(t_fw_itr) + "," + str(counter_fw) + "\n"

    # print alpha
    # print counter_fw

# Time the entire experiment including recording data
print ""
print str(t_end - t_begin) + "s"
# print str(time() - t_begin) + "s"

# Write results to a json file
WR.main(s_overview, s_loads, s_costs, s_prices, s_fw, s_lookup, s_loads_houses, no_houses,
        P.no_itrs, randomization, no_intervals_day, P.load_data, penalty_coefficient, lookup_param)
