from scripts.input_parameters import no_houses, no_pricing_periods, no_intervals_day, interval
from numpy.random import choice
from scripts import pricing_prices as PR


def schedule(prob_dist, demands_itr, penalties_itr, lookup_coeff, sub_dir):

    no_totalSamples = 10
    sampled_outcomes = ""
    for _ in range(no_totalSamples):
        total_itrs = len(demands_itr)
        no_houses = len(demands_itr[0])
        selction_households = choice(total_itrs, no_houses, p=prob_dist)
        # print(selction_households)
        # print (prob_dist)

        actual_penalties = [penalties_itr[selction_households[h]][h] for h in range(no_houses)]
        # print(actual_costs)
        actual_demands = [demands_itr[selction_households[h]][h] for h in range(no_houses)]

        actual_total_penalty = sum(actual_penalties)
        actual_total_demands = [sum([actual_demands[h][t] for h in range(no_houses)]) for t in range(no_intervals_day)]
        actual_total_demands_short = [sum([actual_total_demands[i + j] for j in range(interval)]) / interval
                                    for i in range(0, no_intervals_day, interval)]
        prices_short = PR.main(actual_total_demands_short, lookup_coeff)
        actual_total_cost = sum([p * d * 0.5 for p, d in zip(prices_short, actual_total_demands_short)])
        actual_max_demand = max(actual_total_demands_short)

        # print("actual max demand", actual_max_demand)
        # print("actual total demands", actual_total_demands_short)
        # print("actual total costs", actual_total_cost)
        # print("actual total penalty", actual_total_penalty)
        # print("Done sampling. ")
        # print("\n")

        sampled_outcomes += ",".join(map(str, actual_total_demands_short)) + "\n"

        # join(map(str, my_lst))

    with open(sub_dir + "sampled_schedules.csv", 'w') as output_file:
        output_file.write(sampled_outcomes)

    print(str(no_totalSamples) + " schedules sampled. \n")

    return actual_total_demands_short, prices_short, actual_total_cost
