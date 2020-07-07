from scripts.inputs import no_pricing_periods, next_level_difference
import scripts.inputs as P


def main(demands, coefficient):

    lookup_base = P.lookup_base
    prices = []

    for p in range(no_pricing_periods):

        # version 2 - compute the prices only - the price of the smallest higher consumption level
        next_prices = lookup_base[-1][0]
        d = demands[p]
        for row in lookup_base:
            if int(row[p + 1] * coefficient - d) >= next_level_difference:
                next_prices = row[0]
                break

        prices.append(next_prices)

    return prices

# def main(loads, coefficient):
    # lookup_base = P.lookup_base
    # prices = [0] * no_pricing_periods
    # for p in range(no_pricing_periods):
        # version 1 - compute the prices and loads
        # next_prices_loads = [(row[0], row[p + 1] * coefficient) for row in lookup_base if
        #                      (float(row[p + 1] * coefficient) - float(loads[p])) > 0.00000001]
        # if not next_prices_loads:
        #     prices[p] = lookup_base[-1][0]
        # else:
        # prices[p] = next_prices_loads[0][0]

        # version 2 - compute the prices only
        # next_prices = [row[0] for row in lookup_base if
        #                int(row[p + 1] * coefficient - loads[p]) > next_level_difference]
        # if not next_prices:
        #     prices[p] = lookup_base[-1][0]
        # else:
        #     prices[p] = next_prices[0]

        # version 3 - compute the prices and their indexes
        # next_prices = [[lookup_base[i][0], i] for i in xrange(len_lookup) if
        #                (lookup_base[i][p + 1] * coefficient - loads[p]) >= 0.5]
        # next_prices = [[lookup_base[i][0], i] for i in xrange(len_lookup) if
        #                (round(lookup_base[i][p + 1] * coefficient, 1) - round(loads[p], 1)) > 0]
        # if not next_prices:
        #     prices[p] = lookup_base[-1][0]
        #     indexes[p] = len_lookup - 1
        # else:
        #     prices[p] = next_prices[0][0]
        #     indexes[p] = next_prices[0][1]

            # if loads[p] > lookup_base[len_lookup - 1][p] * coefficient:
            #     prices[p] = lookup_base[len_lookup - 1][0]
            # else:
            #     prices[p] = min([row[0] for row in lookup_base if loads[p] <= row[p + 1] * coefficient])

    # print prices
    return prices
    # return prices, indexes
