from inputs import i_astart, i_dur, i_demand, no_intervals_day, interval


def main(community):
    demands = [0] * no_intervals_day
    demands_households = []
    for household in community:
        demands_per_household = [0] * no_intervals_day
        for job in household:
            # load_per_scheduling_period = job[i_demand] / (no_intervals_day / 24.0)
            start = job[i_astart]
            for i in range(job[i_dur]):
                if start + i > no_intervals_day - 1:
                    demands[start + i - no_intervals_day] += job[i_demand]
                    demands_per_household[start + i - no_intervals_day] += job[i_demand]
                else:
                    demands[start + i] += job[i_demand]
                    demands_per_household[start + i] += job[i_demand]

        # demands_per_household = [max([demands_per_household[i + j] for j in xrange(interval)]) for i in
        #                    xrange(0, no_intervals_day, interval)]
        demands_households.append(demands_per_household)

    # convert load per scheduling period into load per pricing period
    # print [i + j for i in xrange(no_per.iods_day) if i % interval == 0 for j in xrange(interval)]
    demands = [max([demands[i + j] for j in xrange(interval)]) for i in xrange(0, no_intervals_day, interval)]

    return demands, demands_households
