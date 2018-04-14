# Version 2 compute the loads for each household

from inputs import i_astart, i_dur, i_consumption, no_intervals_day, interval, no_pricing_periods


def main(community):
    loads = [0] * no_pricing_periods
    for household in community:
        loads_household = [0] * no_intervals_day
        for job in household:
            load_per_scheduling_period = job[i_consumption] / (no_intervals_day / 24.0)
            start = job[i_astart]
            for i in range(job[i_dur]):
                if start + i > no_intervals_day - 1:
                    loads_household[start + i - no_intervals_day] += load_per_scheduling_period
                else:
                    loads_household[start + i] += load_per_scheduling_period

        loads_household = [sum([loads_household[i + j] for j in xrange(interval)]) for i in xrange(no_intervals_day) if i % interval == 0]
        loads = [x + y for x, y in zip(loads, loads_household)]
    # convert load per scheduling period into load per pricing period
    # print [i + j for i in xrange(no_periods_day) if i % interval == 0 for j in xrange(interval)]
    # loads = [sum([loads[i + j] for j in xrange(interval)]) for i in xrange(no_periods_day) if i % interval == 0]

    return loads
