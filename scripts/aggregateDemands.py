from scripts.inputs import i_astart, i_dur, i_demand, no_intervals_day, interval


def main(community, batteries):
    demands = [0] * no_intervals_day
    demands_households = []

    for household in community:
        demands_per_household = aggregate_household(household)
        demands = [x + y for x, y in zip(demands, demands_per_household)]
        demands_households.append(demands_per_household)


    if not batteries is None:
        demands_updated = [0] * no_intervals_day
        demands_households_updated = []
        for demands_h, b in zip(demands_households, batteries):
            demands_per_household_updated = [x + y for x, y in zip(demands_h, b['activities'])]
            demands_updated = [x + y for x, y in zip(demands_updated, demands_per_household_updated)]
            demands_households_updated.append(demands_per_household_updated)

        demands = demands_updated
        demands_households = demands_households_updated

    # convert from long to short demand profile
    demands = [sum([demands[i + j] for j in range(interval)]) / interval for i in
                   range(0, no_intervals_day, interval)]


    return demands, demands_households


def aggregate_household (household):
    demands_per_household = [0] * no_intervals_day
    for job in household:
        start = job[i_astart]
        for i in range(job[i_dur]):
            demands_per_household[(start + i) % no_intervals_day] += job[i_demand]
            # if start + i > no_intervals_day - 1:
            #     demands_per_household[start + i - no_intervals_day] += job[i_demand]
            # else:
            #     demands_per_household[start + i] += job[i_demand]

    return demands_per_household
