# Version 2 combines scheduling and aggregating loads together
# Version 3 uses a for loop to find the cheapest time slot, instead of using the list comprehension

from inputs import no_intervals_day, penalty_coefficient, i_name, \
    i_pstart, i_astart, i_estart, i_dur, i_lfinish, i_caf, i_demand, i_bill, i_penalty, show_astart, i_predecessor, i_succeeding_delay
from time import time
from aggregateDemands import aggregate_household


def main(household, prices_long, total_penalty):

    begin = time()

    job_durations = []
    job_demands = []
    num_precedences = 0
    predecessors = []
    successors = []
    prec_delays = []
    percent = 1

    max_demand = int(sum([j[i_demand] for j in household]) * percent) + 1

    for job in household:
        job_durations.append(job[i_dur])
        job_demands.append(int(job[i_demand] * 1000))
        job = evaluate_job(job, prices_long, household[:], max_demand)
        total_penalty += job[i_penalty]
        # print(job[i_penalty])

    if show_astart:
        print("astarts", [j[i_astart] for j in household], "obj", sum([j[i_penalty] + j[i_bill] for j in household]))

    return total_penalty


def evaluate_job(job, price_long, household, max_demand):

    e_s = job[i_estart]
    p_s = job[i_pstart]
    dur = job[i_dur]
    l_f = job[i_lfinish]
    caf = job[i_caf]
    demand = job[i_demand]
    id = int(job[i_name])

    if i_predecessor in job.keys():
        prec = job[i_predecessor]
        prec_astart = household[prec][i_astart]
        prec_dur = household[prec][i_dur]
        delay = job[i_succeeding_delay]
        e_s = max(e_s, prec_astart + prec_dur)
        l_f = min(l_f, prec_astart + prec_dur - 1 + delay + dur)

    big_num = 999 * max(price_long)
    p_s_cp = p_s + dur - 1
    price_irrelevant_day = [big_num for _ in range(dur - 1)]

    # if e_s and l_f are NOT in the same day
    if 0 <= e_s <= p_s and p_s + dur - 1 <= l_f <= no_intervals_day - 1:
        price_today = [p if e_s <= i <= l_f else big_num for i, p in enumerate(price_long)]
        price_long_cp = price_irrelevant_day + price_today + price_irrelevant_day
    else:
        price_previous_day = [price_long[i % no_intervals_day] if i >= e_s else big_num for i in range(-dur + 1, 0)]
        price_next_day = [price_long[i] if i + no_intervals_day <= l_f else big_num
                          for i in range(no_intervals_day, no_intervals_day + dur - 1)]

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

    INTERVALS = xrange(len(price_long_cp))
    load_per_scheduling_period = demand / (no_intervals_day / 24.0)
    bills = [sum(price_long_cp[i: i + dur]) * load_per_scheduling_period for i in INTERVALS]
    penalties = [abs(p_s_cp - i) * caf * penalty_coefficient for i in INTERVALS]
    costs_job = [x + y for x, y in zip(bills, penalties)]

    if id > 0:
        current_demands_household = aggregate_household(household[:id])
    else:
        current_demands_household = [0] * no_intervals_day
    DONE = False
    while DONE is False:
        min_cost = min(costs_job)
        min_cost_indices = [i for i, x in enumerate(costs_job) if x == min_cost]
        # print(min_cost_indices)

        chosen_index = min_cost_indices[0]
        actual_start = (chosen_index - dur + 1) % no_intervals_day

        current_demands_household2 = current_demands_household[:]
        for d in range(dur):
            current_demands_household2[(actual_start + d) % no_intervals_day] += demand
        if max(current_demands_household2) <= max_demand or len(min_cost_indices) == 1:
            DONE = True
            break
        else:
            costs_job[actual_start] += 99999


    # for i in xrange(len(price_long) - dur + 1):
    #     bill = sum(price_long[i: i + dur]) * load_per_scheduling_period
    #     penalty = abs(i - p_s) * caf * penalty_coefficient
    #     cost = bill + penalty
    #     if cost < cost_min:
    #     # if cost < cost_min or (cost == cost_min and penalty < penalty_min):
    #         cost_min = cost
    #         actual_start = i
    #         bill_min = bill
    #         penalty_min = penalty

    job[i_bill] = sum(price_long_cp[chosen_index: chosen_index + dur]) * load_per_scheduling_period
    job[i_penalty] = penalties[chosen_index]
    
    job[i_astart] = actual_start

    # print str(time() - t_begin) + "s"

    # add this load to the aggregate loads
    # for i in xrange(dur):
    #     if actual_start + i > no_intervals_day - 1:
    #         demands_household[actual_start + i - no_intervals_day] += demand
    #     else:
    #         demands_household[actual_start + i] += demand

    return job


