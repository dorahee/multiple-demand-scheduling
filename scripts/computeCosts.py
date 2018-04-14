from inputs import no_pricing_periods
import inputs as P


def main(prices, loads, coefficient):
    total_cost = 0
    lookup_base = P.lookup_base
    for p in range(no_pricing_periods):
        prices_load = [(row[0], row[p + 1] * coefficient) for row in lookup_base if row[0] < prices[p]]
        if not prices_load:
            cost_period = prices[p] * loads[p]
        else:
            # todo: something wrong
            cost_period = prices_load[0][0] * prices_load[0][1] + prices[p] * (loads[p] - prices_load[-1][1])
            indexes = range(len(prices_load))[1:]
            cost_level = [prices_load[i][0] * (prices_load[i][1] - prices_load[i - 1][1]) for i in indexes]
            cost_period += sum(cost_level)

            # cost_period += sum([i[0] * i[1] for i in prices_load])

        total_cost += cost_period

    return total_cost
