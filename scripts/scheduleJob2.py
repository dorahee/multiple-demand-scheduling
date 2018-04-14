# This version combines scheduling and aggregating loads together

from random import choice
from inputs import no_intervals_day, no_pricing_periods, interval, randomization, penalty_coefficient, \
    i_pstart, i_astart, i_estart, i_dur, i_lfinish, i_caf, i_demand, i_bill, i_penalty
from time import time


def main(job, price_long, loads):
    # t_begin = time()
    load_per_scheduling_period = job[i_demand] / (no_intervals_day / 24.0)
    e_s = job[i_estart]
    p_s = job[i_pstart]
    l_f = job[i_lfinish]
    dur = job[i_dur]
    caf = job[i_caf]

    # if e_s and l_f are in the same day
    if 0 <= e_s <= p_s and p_s + dur - 1 <= l_f <= no_intervals_day - 1:
        price_modified = price_long[e_s:l_f + 1]
        p_s2 = p_s
    else:
        # if e_s is in the previous day and l_f is in the next day
        if e_s > p_s and p_s + dur - 1 > l_f:
            price_modified = price_long[e_s: no_intervals_day] + price_long + price_long[:l_f + 1]
        # if e_s is in the previous day or l_f is in the next day
        else:
            price_modified = price_long[e_s: no_intervals_day] + price_long[:l_f + 1]

        if e_s > p_s:
            p_s2 = p_s + no_intervals_day - e_s
        else:
            p_s2 = p_s - e_s

    bills = [sum(price_modified[i: i + dur]) * load_per_scheduling_period for i in xrange(len(price_modified) - dur + 1)]
    penalties = [abs(p_s2 - i) * caf * penalty_coefficient for i in xrange(len(price_modified) - dur + 1)]
    costs = [x + y for x, y in zip(bills, penalties)]
    min_cost = min(costs)

    min_cost_indices = [i for i, x in enumerate(costs) if x == min_cost]
    chosen_index = min_cost_indices[0]
    if randomization == 1:
        chosen_index = choice(min_cost_indices)
    actual_start = chosen_index + e_s
    if e_s + chosen_index >= no_intervals_day:
        actual_start -= no_intervals_day

    job[i_astart] = actual_start
    job[i_bill] = bills[chosen_index]
    job[i_penalty] = penalties[chosen_index]

    # print str(time() - t_begin) + "s"

    # add this load to the aggregate loads
    for i in range(job[i_dur]):
        if actual_start + i > no_intervals_day - 1:
            loads[actual_start + i - no_intervals_day] += load_per_scheduling_period
        else:
            loads[actual_start + i] += load_per_scheduling_period

    return job, loads


