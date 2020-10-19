# Version 2 combines scheduling and aggregating loads together
# Version 3 uses a for loop to find the cheapest time slot, instead of using the list comprehension

from scripts.input_parameters import no_intervals_day, penalty_coefficient, \
    i_pstart, i_astart, i_estart, i_dur, i_lfinish, i_caf, i_demand, i_bill, i_penalty, \
    i_predecessor, i_succeeding_delay, i_name, minizinc_model, show_astart
from time import time
# from gurobipy import *
from minizinc import Instance, Model, Solver


def main(household, prices_long, total_penalty):

    costs_matrix = []
    job_durations = []
    job_demands = []
    num_precedences = 0
    predecessors = []
    successors = []
    prec_delays = []
    percent = 1

    for job in household:
        job_durations.append(job[i_dur])
        job_demands.append(int(job[i_demand] * 1000))

        if i_predecessor in job.keys():
            num_precedences += 1
            predecessors.append(job[i_predecessor] + 1)
            successors.append(int(job[i_name]) + 1)
            prec_delays.append(job[i_succeeding_delay])

    dur_max = max(job_durations)
    for job in household:
        job, costs_job = evaluate_job(job, prices_long, dur_max)
        costs_matrix.append(costs_job)

    # minizinc
    t_schedule = time()
    job_astarts = solve_minizinc(costs_matrix, job_demands, job_durations, num_precedences, predecessors,
    successors, prec_delays, percent)
    print(time() - t_schedule)

    # gurobi
    # job_astarts = solve_gurobi(costs_matrix, job_demands, job_durations, num_precedences, predecessors, successors,
    # prec_delays, percent)

    demands_household = [0] * no_intervals_day
    for i, astart in enumerate(job_astarts):
        job = household[i]
        job[i_astart] = astart % no_intervals_day
        job[i_penalty] = abs(astart - job[i_pstart]) * job[i_caf] * penalty_coefficient
        total_penalty += job[i_penalty]

        # update the household demand
        for i in range(job[i_dur]):
            demands_household[(job[i_astart] + i) % no_intervals_day] += job[i_demand]

    return total_penalty, demands_household


def evaluate_job(job, price_long, dur_max):

    # t_begin = time()
    load_per_scheduling_period = job[i_demand] / (no_intervals_day / 24.0)
    e_s = job[i_estart]
    p_s = job[i_pstart]
    dur = job[i_dur]
    l_f = job[i_lfinish]
    caf = job[i_caf]

    big_num = 999 * max(price_long)
    p_s_cp = p_s + dur_max - 1
    price_irrelevant_day = [big_num for _ in range(dur_max - 1)]

    # if e_s and l_f are NOT in the same day
    if 0 <= e_s <= p_s and p_s + dur - 1 <= l_f <= no_intervals_day - 1:
        price_today = [p if e_s <= i <= l_f else big_num for i, p in enumerate(price_long)]
        price_long_cp = price_irrelevant_day + price_today + price_irrelevant_day
    else:
        price_previous_day = [price_long[i % no_intervals_day] if i >= e_s else big_num for i in range(-dur_max + 1, 0)]
        price_next_day = [price_long[i] if i + no_intervals_day <= l_f else big_num
                          for i in range(no_intervals_day, no_intervals_day + dur_max - 1)]

        # if e_s is in the previous day and l_f is in today
        if e_s < 0:
            price_today = [p if i <= l_f else big_num for i, p in enumerate(price_long)]
            price_long_cp = price_previous_day + price_today + price_irrelevant_day

        # if l_f is in the next day and e_f is in today
        elif l_f > no_intervals_day - 1:
            price_today = [p if i >= e_s else big_num for i, p in enumerate(price_long)]
            price_long_cp = price_irrelevant_day + price_today + price_next_day

        # if e_s is in the previous day and l_f is in the next day
        else:
            price_long_cp = price_previous_day + price_long + price_next_day

    INTERVALS = range(len(price_long_cp))
    bills = [sum(price_long_cp[i: i + dur]) * load_per_scheduling_period for i in INTERVALS]
    penalties = [abs(p_s_cp - i) * caf * penalty_coefficient for i in INTERVALS]
    costs_job = [x + y for x, y in zip(bills, penalties)]
    # costs_matrix.append(costs_job)

    return job, costs_job


def solve_minizinc(costs_matrix, job_demands, job_durations, num_precedences, predecessors, successors, prec_delays, percent):

    dur_max = max(job_durations)
    no_intervals = no_intervals_day + (dur_max - 1) * 2

    multipleDSP = Model("scripts/{}".format(minizinc_model))
    gecode = Solver.lookup("gecode")
    ins = Instance(gecode, multipleDSP)

    max_demand = int(sum(job_demands) * percent)
    ins["no_intervals"] = no_intervals
    ins["no_devices"] = len(costs_matrix)
    ins["durations"] = job_durations
    ins["demands"] = job_demands
    ins["num_precedences"] = num_precedences
    ins["predecessors"] = predecessors
    ins["successors"] = successors
    ins["prec_delays"] = prec_delays
    ins["max_demand"] = max_demand
    ins["run_costs"] = costs_matrix

    result = ins.solve()

    cp_astarts_temp = result["actual_starts"]

    cp_astarts = [(astart - dur_max + 1) % no_intervals_day for astart in cp_astarts_temp]
    #
    # actual_start = (chosen_index - dur + 1) % no_intervals_day

    return cp_astarts

    # costs_matrix_str = str(costs_matrix).replace("], [", "|").replace("[[", "[|").replace("]]", "|]")
    # dzn_file_str = "no_intervals={0};\n" \
    #                "no_devices={1};\n" \
    #                "durations={2};\n" \
    #                "demands={3};\n" \
    #                "num_precedences={4};\n" \
    #                "predecessors={5};\n" \
    #                "successors={6};\n" \
    #                "prec_delays={7};\n" \
    #                "max_demand={8};\n" \
    #                "run_costs={9};" \
    #     .format(no_intervals_day * 2,
    #             len(costs_matrix),
    #             str(job_durations),
    #             str(job_demands),
    #             num_precedences,
    #             predecessors,
    #             successors,
    #             prec_delays,
    #             max_demand,
    #             costs_matrix_str)
    #
    # path_data = "scripts/{}".format(minizinc_data)
    # f = open(path_data, "w")
    # f.write(dzn_file_str)
    # f.close()

    # path_model = "scripts/{}".format(minizinc_model)
    # out = Popen(["minizinc", "-G", "linear", "-f", "mzn-cbc", path_model, path_data], stdout=PIPE, stderr=PIPE)
    # out = Popen(["minizinc", "-G", "linear", "-f", "mzn-gurobi", path_model, path_data], stdout=PIPE, stderr=PIPE)
    # out_str = ",".join(out.stdout.readlines()[:1]).replace("A", '"')
    # print(out_str)

    # out_json = loads(str(out_str))
    # cp_astarts = out_json["astarts"]
    # print("m solution", cp_astarts, out_json["obj"])


# def solve_gurobi(costs_matrix, job_demands, job_durations, num_precedences, predecessors, successors,
# prec_delays, percent):
#
#     m = Model("household_load_scheduling")
#
#     devices = []
#     DEVICES = range(len(costs_matrix))
#     PREC = range(num_precedences)
#     max_demand = int(sum(job_demands) * percent) + 999999
#
#     for i in DEVICES:
#         d_times = []
#         for _ in range(len(costs_matrix[i])):
#             d_t = m.addVar(vtype=GRB.BINARY)
#             d_times.append(d_t)
#         devices.append(d_times)
#         m.addConstr(sum(d_times) == 1)
#
#     # for _ in DEVICES:
#     #     d_t = m.addVar(INTERVALS, vtype=GRB.INTEGER)
#
#     for t in range(no_intervals_day):
#         m.addConstr(sum([devices[i][t] * job_demands[i] for i in DEVICES]) <= max_demand)
#     #
#     for p in PREC:
#         pre = predecessors[p] - 1
#         succ = successors[p] - 1
#         d = prec_delays[p]
#
#         m.addConstr(sum([devices[pre][t] * t for t in range(len(costs_matrix[pre]))]) + job_durations[pre]
#                     <= sum([devices[succ][t] * t for t in range(len(costs_matrix[succ]))])
#                     <= sum([devices[pre][t] * t for t in range(len(costs_matrix[pre]))]) + job_durations[pre] + d)
#
#     m.setObjective(sum([sum([devices[i][t] * costs_matrix[i][t] for t in range(len(costs_matrix[i]))])
#                         for i in DEVICES]), GRB.MINIMIZE)
#
#     m.setParam('OutputFlag', False)
#     m.optimize()
#
#     astarts = [(sum([int(i * t.x) for i, t in enumerate(d)]) - job_durations[j] + 1) % no_intervals_day
#                for j, d in enumerate(devices)]
#
#     if show_astart:
#         print("g solution", astarts, m.objVal)
#
#     return astarts
