from copy import deepcopy


def main(battery, sorted_periods, loads, prices):
    # print "loads          = " + str(loads)
    # print "battery        = " + str(battery)
    # print "sorted periods = " + str(sorted_periods)

    sorted_periods0 = deepcopy(sorted_periods)

    # stage one battery scheduling

    while len(sorted_periods) > 1:

        p_cheap = sorted_periods[0]
        p_expensive = sorted_periods[-1]

        e_remaining_discharge_end = battery['discharge'] + battery['activities'][p_expensive]
        while (loads[p_expensive] == 0 or e_remaining_discharge_end == 0 or prices[p_expensive] <= prices[p_cheap]) and len(sorted_periods) > 1:
            del sorted_periods[-1]
            p_expensive = sorted_periods[-1]
            e_remaining_discharge_end = battery['discharge'] + battery['activities'][p_expensive]

        e_remaining_charge_start = battery['charge'] - battery['activities'][p_cheap]
        e_remaining = battery['capacity'] - battery['energy'][p_cheap]
        while (e_remaining_charge_start == 0 or e_remaining == 0) and len(sorted_periods) > 1:
            del sorted_periods[0]
            p_cheap = sorted_periods[0]
            e_remaining_charge_start = battery['charge'] - battery['activities'][p_cheap]
            e_remaining = battery['capacity'] - battery['energy'][p_cheap]

        if len(sorted_periods) >= 2:
            if p_cheap < p_expensive:
                e_cap = battery['energy'][p_cheap + 1:p_expensive]
                # else:
                #     periods_ranges = range(p_cheap, no_periods_day) + range(p_expensive)
                #     e_cap = battery['energy'][p_cheap: no_periods_day] + battery['energy'][:p_expensive]
                e_remaining_cap_max = battery['capacity'] - max(e_cap)

                if not e_remaining_cap_max == 0:
                    e_charge = min(loads[p_expensive], e_remaining_discharge_end,  e_remaining_charge_start, e_remaining_cap_max)
                    loads[p_cheap] += e_charge
                    loads[p_expensive] -= e_charge
                    battery['activities'][p_cheap] += e_charge
                    battery['activities'][p_expensive] -= e_charge
                    for i in xrange(p_cheap, p_expensive):
                        battery['energy'][i] += e_charge
                else:
                    periods_full = [t for t in sorted_periods if battery['energy'][t] == battery['capacity']]
                    del sorted_periods[0]
                    for p in periods_full:
                        try:
                            sorted_periods.remove(p)
                        except ValueError:
                                pass
            else:
                del sorted_periods[-1]

    # stage two battery scheduling
    sorted_periods = deepcopy(sorted_periods0)

    while len(sorted_periods) > 1:
        p_cheap = sorted_periods[0]
        p_expensive = sorted_periods[-1]

        e_remaining_discharge_start = battery['discharge'] + battery['activities'][p_expensive]
        e_remaining = battery['energy'][p_expensive]
        while (loads[p_expensive] == 0 or e_remaining_discharge_start == 0 or e_remaining == 0 or prices[p_expensive] <= prices[p_cheap]) \
                and len(sorted_periods) > 1:
            del sorted_periods[-1]
            p_expensive = sorted_periods[-1]
            e_remaining_discharge_start = battery['discharge'] + battery['activities'][p_expensive]
            e_remaining = battery['energy'][p_expensive]

        e_remaining_charge_end = battery['charge'] - battery['activities'][p_cheap]
        while e_remaining_charge_end == 0 and len(sorted_periods) > 1:
            del sorted_periods[0]
            p_cheap = sorted_periods[0]
            e_remaining_charge_end = battery['charge'] - battery['activities'][p_cheap]

        if len(sorted_periods) >= 2:
            if p_expensive < p_cheap:
                e_remaining = battery['energy'][p_expensive + 1:p_cheap]
                e_remaining_min = min(e_remaining)

                if not e_remaining_min == 0:
                    e_discharge = min(loads[p_expensive], e_remaining_discharge_start, e_remaining_charge_end, e_remaining_min)
                    loads[p_expensive] -= e_discharge
                    loads[p_cheap] += e_discharge
                    battery['activities'][p_expensive] -= e_discharge
                    battery['activities'][p_cheap] += e_discharge
                    for i in xrange(p_expensive, p_cheap):
                        battery['energy'][i] -= e_discharge
                else:
                    periods_empty = [t for t in sorted_periods if battery['energy'][t] == 0]
                    del sorted_periods[-1]
                    for p in periods_empty:
                        try:
                            sorted_periods.remove(p)
                        except ValueError:
                            pass
            else:
                del sorted_periods[0]

    # print "loads          = " + str([round(x, 2) for x in loads])
    # print "battery        = " + str(battery['energy'])
    # print "****"

    # stage 2 charging and discharging

    return battery, loads


