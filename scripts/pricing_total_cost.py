from scripts.input_parameters import no_pricing_periods
import scripts.input_parameters as P


def main(prices, loads, coefficient):

    lookup_base = P.lookup_base

    no_periods = len(loads)
    no_levels = len(lookup_base)

    total_cost = 0

    for p in range(no_periods):

        cost_period = 0

        if lookup_base[0][0] == prices[p]:
            cost_period += prices[p] * loads[p]

        else:
            cost_period += lookup_base[0][0] * lookup_base[0][p + 1] * coefficient

            for i in xrange(1, no_levels):
                if lookup_base[i][0] < prices[p]:
                    cost_period += lookup_base[i][0] * (lookup_base[i][p + 1] - lookup_base[i - 1][p + 1]) * coefficient
                elif lookup_base[i][0] == prices[p]:
                    cost_period += lookup_base[i][0] * (loads[p] - lookup_base[i - 1][p + 1] * coefficient)
                    break

        total_cost += cost_period

    return total_cost
