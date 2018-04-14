# Version 2 combines scheduling and aggregating loads together
# Version 3 uses a for loop to find the cheapest time slot, instead of using the list comprehension

from inputs import no_intervals_day, penalty_coefficient, \
    i_pstart, i_astart, i_estart, i_dur, i_lfinish, i_caf, i_demand, i_bill, i_penalty, \
    i_predecessor, i_succeeding_delay, i_name, minizinc_model, minizinc_data
from subprocess import PIPE, Popen
from json import loads
from time import time
from gurobipy import *


def main(household, prices_long, total_penalty):

    begin = time()

    loads_household = [0] * no_intervals_day
    costs_matrix = []
    job_durations = []
    job_demands = []
    num_precedences = 0
    predecessors = []
    successors = []
    prec_delays = []
    percent = 0.7

    for job in household:
        job_durations.append(job[i_dur])
        job_demands.append(int(job[i_demand] * 1000))
        job, costs_matrix = evaluate_job(job, prices_long, costs_matrix)

        if i_predecessor in job.keys():
            num_precedences += 1
            predecessors.append(job[i_predecessor] + 1)
            successors.append(int(job[i_name]) + 1)
            prec_delays.append(job[i_succeeding_delay])

    # minizinc
    # job_astarts = solve_minizinc(costs_matrix, job_demands, job_durations, num_precedences, predecessors, successors, prec_delays, percent)

    # gurobi
    job_astarts = solve_gurobi(costs_matrix, job_demands, job_durations, num_precedences, predecessors, successors, prec_delays, percent)

    # start = time()
    for i, astart in enumerate(job_astarts):
        job = household[i]
        job[i_astart] = astart % no_intervals_day
        job[i_penalty] = abs(astart - job[i_pstart]) * job[i_caf] * penalty_coefficient
        total_penalty += job[i_penalty]

        load_per_scheduling_period = job[i_demand] / (no_intervals_day / 24.0)

        for i in xrange(job[i_dur]):
            if astart + i > no_intervals_day - 1:
                loads_household[astart + i - no_intervals_day] += load_per_scheduling_period
            else:
                loads_household[astart + i] += load_per_scheduling_period
    # print("update jobs time", time()-start)

    # print("total scheudling time", time() - begin)

    return total_penalty, loads_household


def solve_gurobi(costs_matrix, job_demands, job_durations, num_precedences, predecessors, successors, prec_delays, percent):

    start = time()
    m = Model("household_load_scheduling")

    devices = []
    DEVICES = range(len(costs_matrix))
    INTERVALS = range(no_intervals_day)
    PREC = range(num_precedences)
    max_demand = int(sum(job_demands) * percent)

    # for _ in DEVICES:
    #     d_times = []
    #     for _ in INTERVALS:
    #         d_t = m.addVar(vtype=GRB.BINARY)
    #         d_times.append(d_t)
    #     devices.append(d_times)
    #     m.addConstr(sum(d_times) == 1)

    for _ in DEVICES:
        d_t = m.addVar(vtype=GRB.INTEGER)
        devices.append(d_times)

    # for t in INTERVALS:
    #     m.addConstr(sum([devices[i][t] * job_demands[i] for i in DEVICES]) <= max_demand)
    #
    # for p in PREC:
    #     pre = predecessors[p] - 1
    #     succ = successors[p] - 1
    #     d = prec_delays[p]
    #     m.addConstr(sum([devices[pre][t] * t for t in INTERVALS]) + job_durations[pre]
    #                 <= sum([devices[succ][t] * t for t in INTERVALS])
    #                 <= sum([devices[pre][t] * t for t in INTERVALS]) + job_durations[pre] + d)

    m.setObjective(sum([sum([devices[i][t] * costs_matrix[i][t] for t in INTERVALS]) for i in DEVICES]), GRB.MINIMIZE)

    m.setParam('OutputFlag', False)
    m.optimize()

    # print("g solve time", time() - start)
    #
    # print('\nTOTAL COSTS: %g' % m.objVal)
    # print('SOLUTION:')
    astarts = [sum([int(i * t.x) for i, t in enumerate(d)]) for d in devices]
    # print("g solution", astarts, m.objVal)

    return astarts


def evaluate_job(job, price_long, costs_matrix):

    # t_begin = time()
    load_per_scheduling_period = job[i_demand] / (no_intervals_day / 24.0)
    e_s = job[i_estart]
    p_s = job[i_pstart]
    dur = job[i_dur]
    l_f = job[i_lfinish]
    caf = job[i_caf]

    big_num = 999 * max(price_long)
    # price_irrelevant_day = [big_num for _ in range(no_intervals_day)

    p_s_cp = p_s

    # start and finish on the same day
    if 0 <= e_s <= p_s and p_s + dur - 1 <= l_f <= no_intervals_day - 1:
        price_today = [p if e_s <= i <= l_f else big_num for i, p in enumerate(price_long)]
        price_prev = [big_num for _ in range(dur - 1)]
        price_next = [big_num for _ in range(dur - 1)]

    # if e_s and l_f are NOT in the same day
    if 0 <= e_s <= p_s and p_s + dur - 1 <= l_f <= no_intervals_day - 1:
        price_today = [p if e_s <= i <= l_f else big_num for i, p in enumerate(price_long)]
        price_irrelevant_day = [big_num for _ in range(dur - 1)]
        price_long_cp = price_today + price_irrelevant_day
    else:
        price_previous_day = [p if i >= e_s else big_num for i, p in enumerate(price_long)]
        price_next_day = [p for p in price_long[:dur - 1]]

        # if e_s is in the previous day and l_f is in the next day
        if p_s < e_s and p_s + dur - 1 > l_f:
            price_long_cp = price_previous_day + price_long

        # if e_s is in the previous day or l_f is in the next day
        else:
            price_long_cp = price_previous_day + price_next_day

    # bills = [sum(price_long_cp[i: i + dur]) * load_per_scheduling_period for i in xrange(len(price_long_cp))]
    bills = [sum(price_long_cp[i: i + dur]) * load_per_scheduling_period for i in xrange(no_intervals_day)]
    # penalties = [abs(p_s_cp - i) * caf * penalty_coefficient for i in xrange(len(price_long_cp))]
    penalties = [abs(p_s_cp - i) * caf * penalty_coefficient for i in xrange(no_intervals_day)]
    costs_job = [x + y for x, y in zip(bills, penalties)]
    costs_matrix.append(costs_job)

    return job, costs_matrix


def solve_minizinc(costs_matrix, job_demands, job_durations, num_precedences, predecessors, successors, prec_delays, percent):

    # begin_model = time()
    costs_matrix_str = str(costs_matrix).replace("], [", "|").replace("[[", "[|").replace("]]", "|]")
    max_demand = int(sum(job_demands) * percent)
    dzn_file_str = "no_intervals={0};\n" \
                   "no_devices={1};\n" \
                   "durations={2};\n" \
                   "demands={3};\n" \
                   "num_precedences={4};\n" \
                   "predecessors={5};\n" \
                   "successors={6};\n" \
                   "prec_delays={7};\n" \
                   "max_demand={8};\n" \
                   "run_costs={9};" \
        .format(no_intervals_day * 2,
                len(costs_matrix),
                str(job_durations),
                str(job_demands),
                num_precedences,
                predecessors,
                successors,
                prec_delays,
                max_demand,
                costs_matrix_str)

    path_data = "scripts/{}".format(minizinc_data)
    f = open(path_data, "w")
    f.write(dzn_file_str)
    f.close()

    path_model = "scripts/{}".format(minizinc_model)
    # out = Popen(["minizinc", "-G", "linear", "-f", "mzn-cbc", path_model, path_data], stdout=PIPE, stderr=PIPE)
    out = Popen(["minizinc", "-G", "linear", "-f", "mzn-gurobi", path_model, path_data], stdout=PIPE, stderr=PIPE)
    out_str = ",".join(out.stdout.readlines()[:1]).replace("A", '"')
    # print("m solve time", time() - begin_model)

    out_json = loads(str(out_str))
    cp_astarts = out_json["astarts"]
    # print("m solution", cp_astarts, out_json["obj"])

    return cp_astarts