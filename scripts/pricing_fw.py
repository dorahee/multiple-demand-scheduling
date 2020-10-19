# This version finds the next energy level for every period in every iteration
# This version improved 2 by not using an array to store alphas of all periods
# This version improved 3 by reducing the loops in eval_incr

from scripts.input_parameters import no_pricing_periods, next_level_difference
import scripts.input_parameters as P
import scripts.pricing_prices as PR


def main(loads_tent, loads_old, prices, penalty, penalty_pre, coe):
    # compute the initial slope
    lookup_base = P.lookup_base
    loads_incr = [lt - lo for lt, lo in zip(loads_tent, loads_old)]
    delta_cost_init = sum([p * d for p, d in zip(prices, loads_incr)])
    delta_penalty_init = penalty - penalty_pre
    slope = delta_cost_init + delta_penalty_init
    slope_fw = slope
    # print slope

    loads_fw = loads_old[:]
    prices_fw = prices[:]
    prices_fw_pre = prices[:]

    def eval_incr(p):
        loads_move1 = loads_tent[p] - loads_fw[p]

        # add_on = next_level_difference + 0.001
        add_on = next_level_difference + 1
        if loads_incr[p] > 0:
            for i, r in enumerate(lookup_base[:-1]):
                if int(r[p + 1] * coe - loads_fw[p]) >= next_level_difference and lookup_base[i + 1][0] > prices_fw[p]:
                    next_energy = r[p + 1] * coe
                    loads_move1 = next_energy + add_on - loads_fw[p]
                    break
        else:
            for i, r in enumerate(lookup_base):
                if int(loads_fw[p] - r[p + 1] * coe) >= next_level_difference and lookup_base[i][0] < prices_fw[p]:
                    next_energy = r[p + 1] * coe
                    loads_move1 = next_energy - add_on - loads_fw[p]
                else:
                    break

        return loads_move1

    changed_cost = 0.02
    alpha_current = 0
    alpha_final = 0
    counter_loop = 0

    while slope < 0 and not changed_cost == 0 and alpha_current < 1:
    # while slope < 0 and alpha_current <= 1:
        alpha_incr_min = 1
        for p in range(no_pricing_periods):
            if abs(loads_incr[p]) > 0:
                e_incr = eval_incr(p)
                alpha_incr = float(e_incr) / float(loads_incr[p])
            else:
                alpha_incr = 1
            if alpha_incr < alpha_incr_min:
                alpha_incr_min = alpha_incr

        alpha_current += alpha_incr_min
        if alpha_current <= 1:
            loads_fw = [l_old + alpha_current * l_incr for l_old, l_incr in zip(loads_old, loads_incr)]
            prices_fw = PR.main(loads_fw, coe)

            # changed_cost = sum(
            #     [(p_fw - p_fw_pre) * l_incr for p_fw, p_fw_pre, l_incr in zip(prices_fw, prices_fw_pre, loads_incr)])
            # if not changed_cost == 0:
            #     slope += changed_cost
            #     if slope < 0:
            #         prices_fw_pre = prices_fw[:]
            #         alpha_final = alpha_current
            #         counter_loop += 1

            delta_cost_current = sum([p * d for p, d in zip(prices_fw, loads_incr)])
            slope = delta_cost_current + delta_penalty_init

            if slope < 0:
                prices_fw_pre = prices_fw[:]
                alpha_final = alpha_current
                counter_loop += 1
                slope_fw = slope


    loads_fw = [l_old + alpha_final * l_incr for l_old, l_incr in zip(loads_old, loads_incr)]
    penalty_fw = penalty_pre + alpha_final * delta_penalty_init

    obj_fw = sum([p * d for p, d in zip(prices_fw, loads_fw)]) + penalty_fw

    # print str(sum(loads_fw))
    # print str(sum(loads_old))

    # Loads_fw is the solution that after the slope turns positive
    # I am not sure if I should the keep the solution before or after the slope turns positive
    # Mark has confirmed that it should be before.
    return loads_fw, prices_fw_pre, penalty_fw, alpha_final, counter_loop, obj_fw, slope_fw

    # changed_cost = sum(
    #     [(p_fw - p_fw_pre) * l_incr for p_fw, p_fw_pre, l_incr in zip(prices_fw, prices_fw_pre, loads_incr)])
    # if not changed_cost == 0:
    #     slope += changed_cost
    #     if slope < 0:
    #         prices_fw_pre = prices_fw[:]
    #         alpha_final = alpha_current
    #         counter_loop += 1

    # previous version of eval_incr(p)

    # def eval_incr(p):

    # if loads_incr[p] > 0:
    #     next_energy_levels = [row[p + 1] * coefficient for row in lookup_base if
    #                           (row[p + 1] * coefficient - loads_fw[p]) >= next_level_difference]
    #     if not next_energy_levels or len(next_energy_levels) == 1:
    #         energy_next = loads_tent[p]
    #     else:
    #         energy_next = next_energy_levels[0] + 0.000001
    # else:
    #     next_energy_levels = [row[p + 1] * coefficient for row in lookup_base if
    #                           (loads_fw[p] - row[p + 1] * coefficient) >= next_level_difference]
    #     if not next_energy_levels:
    #         energy_next = loads_tent[p]
    #     else:
    #         energy_next = next_energy_levels[0]
    # return energy_next - loads_fw[p]

# if loads_incr[p] > 0:
#     # try:
#         next_energy = [r[p + 1] * coe for i, r in enumerate(lookup_base[:-1])
#                        if((r[p + 1] * coe - loads_fw[p]) > next_level_difference
#                        and lookup_base[i + 1][0] > prices_fw[p])]
#     # except IndexError:
#     #     next_energy = []
# else:  # lif loads_incr[p] < 0:
#     next_energy = [r[p + 1] * coe for i, r in enumerate(lookup_base)
#                    if (loads_fw[p] - r[p + 1] * coe) > next_level_difference
#                    and lookup_base[i][0] < prices_fw[p]]
#     next_energy.reverse()
#
# if not next_energy:
#     loads_move1 = loads_tent[p] - loads_fw[p]
# else:
#     add_on = next_level_difference + 0.000001
#     # loads_move1 = next_energy[0] + add_on - loads_fw[p] if loads_incr[p] > 0 \
#     #     else next_energy[0] - add_on - loads_fw[p]
#     loads_move1 = next_energy[0] - loads_fw[p] if loads_incr[p] > 0 else next_energy[0] - add_on - loads_fw[p]
#
# if loads_incr[p] > 0:
#     try:
#         next_energy = [r[p + 1] * coe for i, r in enumerate(lookup_base)
#                        if((r[p + 1] * coe - loads_fw[p]) > next_level_difference
#                        and lookup_base[i + 1][0] > prices_fw[p])]
#     except IndexError:
#         next_energy = []
# else:  # lif loads_incr[p] < 0:
#     next_energy = [r[p + 1] * coe for i, r in enumerate(lookup_base)
#                    if (loads_fw[p] - r[p + 1] * coe) > next_level_difference
#                    and lookup_base[i][0] < prices_fw[p]]
#     next_energy.reverse()
#
# if not next_energy:
#     loads_move1 = loads_tent[p] - loads_fw[p]
# else:
#     add_on = next_level_difference + 0.000001
#     # loads_move1 = next_energy[0] + add_on - loads_fw[p] if loads_incr[p] > 0 \
#     #     else next_energy[0] - add_on - loads_fw[p]
#     loads_move1 = next_energy[0] - loads_fw[p] if loads_incr[p] > 0 else next_energy[0] - add_on - loads_fw[p]
