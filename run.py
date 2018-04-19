from scripts import jobsGenerator as J, batteriesGenerator as B, pricing as PR, \
    aggregateDemands as AD, frankWolfe4 as FW2, \
    writeResults as WR, inputs as P, computeCosts2 as CC, \
    readFiles as RF, scheduleBattery2 as SB, computeLookup as CLU, sampleSchedules as SS
from scripts.inputs import lookup_param, i_bill, i_penalty, interval, \
    no_intervals_day, no_pricing_periods, no_jobs_min, no_jobs_max, penalty_coefficient, randomization, use_solver
from time import time
from sys import argv

if use_solver:
    from scripts import scheduleJobCP as SJ
else:
    from scripts import scheduleJob4 as SJ

if len(argv) > 1:
    P.no_houses = int(argv[1])

if len(argv) > 2:
    P.no_itrs = int(argv[2])

# Generate data
community = J.main(P.load_data)
no_houses = len(community)
demands_itr = []
demands_short, demands_households = AD.main(community)
demands_itr.append(demands_households)
lookup_coeff = max(demands_short) * lookup_param
penalties_itr = []
total_penalty = 0
penalties_itr.append([0 for _ in range(no_houses)])

batteries = B.main(P.battery_data)
no_batteries = len(batteries)
if P.use_battery == 0:
    no_batteries = "No"

# lookup_file = ""
lookup_file = 'files/lookup-0.csv'
# lookup_file = 'files/lookup-0-renew.csv'
# lookup_file = 'files/lookup-100-zero-threshold9-flu.csv'
P.lookup_base = RF.main(lookup_file)
# region = "sa"
# lookup_file= region
# P.lookup_base = CLU.main(region, P.no_pricing_periods)
prices = PR.main(demands_short, lookup_coeff)

# -------------------- Meta data of this experiment --------------------
print str(no_houses) + " houses, " + str(no_jobs_min) + " ~ " + str(no_jobs_max) + " jobs per house, " \
      + str(no_batteries) + " batteries."
print str(no_intervals_day) + " scheduling periods, " + str(no_pricing_periods) + " pricing periods, "
# print str(P.no_itrs) + " iterations"
# print "---------------"

if not lookup_file == "":
    lookup_file = lookup_file
    notes = lookup_file
    # notes = lookup_file[lookup_file.index("lookup") + len("lookup") + 1: lookup_file.index("-zero")] + "% renewable."
else:
    lookup_file = ""
    notes = ""

s_loads_houses, s_overview, s_costs, s_lookup, s_demands, s_prices, s_fw, sub_dir \
    = WR.prepare(no_houses, no_batteries, no_jobs_max, no_jobs_min,
                 P.max_battery_capacity, P.max_battery_charge, P.max_battery_discharge,
                 lookup_coeff, lookup_file, notes, penalty_coefficient, no_intervals_day,
                 no_pricing_periods, demands_short, prices, P.lookup_base)

# -------------------- Meta data of this experiment --------------------

t_begin = t_end = time()
t_fw_total = 0
t_pricing_total = 0
t_scheduling_total = 0
counter_fw = -1
prob_dist = []
s_itr = 0
itr = 0
for itr in range(P.no_itrs + 1):
    print "========"
    print "Iteration " + str(itr)

    # computing the total electricity cost
    # total_cost = CC.main(prices=prices, loads=demands, coefficient=lookup_coeff)
    total_cost = sum([p * d * 0.5 for p, d in zip(prices, demands_short)])
    s_costs += str(itr) + "," + "f," + str(total_cost) + "," + str(total_penalty) + "\r\n"

    WR.append(sub_dir, s_demands, s_costs, s_prices, s_fw)
    s_costs = ""

    if itr == P.no_itrs or counter_fw == 0:
        t_end = time()
        s_overview += str(t_end - t_begin) + "," + str(t_fw_total) + "," + str(t_pricing_total) + "," \
                      + str(t_scheduling_total) + "\r\n"
        break

    # pricing
    prices_long = [p for p in prices for i in xrange(interval)]
    sorted_periods = sorted(range(len(prices_long)), key=lambda x: prices_long[x])
    flag_schedule_battery = 1
    if prices_long[sorted_periods[0]] == prices_long[sorted_periods[-1]] or P.use_battery == 0:
        flag_schedule_battery = 0

    # start new iteration
    s_itr = itr + 1
    demands_short_pre = demands_short[:]
    total_penalty_pre = total_penalty
    demands_long = [0] * no_intervals_day
    total_penalty = 0

    # scheduling and aggregating demand
    t_scheduling_begin = time()
    counter = 0
    penalties_households = []
    for household, battery in zip(community, batteries):
        counter += 1
        # print("house id", counter)
        # scheduling jobs
        # loads_household = [0] * no_intervals_day
        # for job in household:
        #     job, loads_household = SJ.main(job, prices_long, loads_household)
        #     total_penalty += job[i_penalty]
        total_penalty_pre = total_penalty
        total_penalty = SJ.main(household, prices_long, total_penalty)
        penalty_per_household = total_penalty - total_penalty_pre
        penalties_households.append(penalty_per_household)

        # scheduling the battery
        # if flag_schedule_battery == 1:
        #     if itr == 0:
        #         battery['energy'] = [battery['min']] * P.no_intervals_day
        #         battery['activities'] = [0] * P.no_intervals_day
        #     battery, demands_household = SB.main(battery, sorted_periods[:], demands_household, prices_long)

    t_scheduling_total += time() - t_scheduling_begin
    penalties_itr.append(penalties_households)

    # total demand per pricing period
    demands_short, demands_households = AD.main(community)
    demands_itr.append(demands_households)
    prices_actual_short = PR.main(demands_short, lookup_coeff)

    s_demands = str(s_itr) + "," + "o," + str(demands_short)[1:-1].replace(" ", "") + "\r\n"
    s_prices = str(s_itr) + "," + "o," + str(prices_actual_short)[1:-1].replace(" ", "") + "\r\n"

    # frank-Wolfe
    t_fw_begin = time()
    demands_short, prices, total_penalty, alpha, counter_fw = \
        FW2.main(demands_short, demands_short_pre, prices, total_penalty, total_penalty_pre, lookup_coeff)
    t_fw_itr = time() - t_fw_begin
    t_fw_total += t_fw_itr

    if prob_dist == []:
        prob_dist.append(1 - alpha)
        prob_dist.append(alpha)
    else:
        prob_dist = [p_d * (1-alpha) for p_d in prob_dist]
        prob_dist.append(alpha)
    # print(prob_dist)
    # print(len(prob_dist))
    # print(len(demands_itr))

    s_demands += str(s_itr) + "," + "f," + str(demands_short)[1:-1].replace(" ", "") + "\r\n"
    s_prices += str(s_itr) + "," + "f," + str(prices)[1:-1].replace(" ", "") + "\r\n"
    # s_prices += str(s_itr) + "," + "o," + str(prices)[1:-1].replace(" ", "") + "\n"
    s_fw = str(s_itr) + "," + str(alpha) + ", " + str(t_fw_itr) + "," + str(counter_fw) + "\r\n"

    # print alpha
    # print counter_fw

# Time the entire experiment including recording data
print ""
print str(t_end - t_begin) + "s"

# Write results to a json file
WR.final(sub_dir, s_overview, s_demands, s_costs, s_prices, s_fw, s_lookup, s_loads_houses, no_houses,
        P.no_itrs, randomization, no_intervals_day, P.load_data, penalty_coefficient, lookup_param, notes)


actual_total_demands_short, prices_short, actual_total_cost = SS.schedule(prob_dist, demands_itr, penalties_itr, lookup_coeff)
s_fw = ""
s_demands = str(s_itr + 1) + "," + "o," + str(actual_total_demands_short)[1:-1].replace(" ", "") + "\r\n"
s_demands += str(s_itr + 1) + "," + "f," + str(actual_total_demands_short)[1:-1].replace(" ", "") + "\r\n"
s_prices = str(s_itr + 1) + "," + "o," + str(prices_short)[1:-1].replace(" ", "") + "\r\n"
s_prices += str(s_itr + 1) + "," + "f," + str(prices_short)[1:-1].replace(" ", "") + "\r\n"
s_costs = str(itr + 1) + "," + "f," + str(actual_total_cost) + "," + str(total_penalty) + "\r\n"
WR.append(sub_dir, s_demands, s_costs, s_prices, s_fw)
