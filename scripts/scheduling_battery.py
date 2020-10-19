
def main(battery, sorted_periods, loads, prices):

    max_capacity = battery['capacity']
    max_charge_rate = battery['charge']
    max_discharge_rate = battery['discharge']

    def charge_then_discharge(p_cheap, p_expensive):
        # e_cap = battery['energy'][p_cheap: p_expensive]
        e_remaining_cap_max = max_capacity - max(battery['energy'][p_cheap: p_expensive])

        if not e_remaining_cap_max == 0:
            e_charge = min(loads[p_expensive], e_remaining_discharge, e_remaining_charge, e_remaining_cap_max)
            loads[p_cheap] += e_charge
            loads[p_expensive] -= e_charge
            battery['activities'][p_cheap] += e_charge
            battery['activities'][p_expensive] -= e_charge
            for i in range(p_cheap, p_expensive):
                battery['energy'][i] += e_charge
        else:
            del sorted_periods[0]
            p_cheap = sorted_periods[0]
            # periods_full = [t for t in sorted_periods if battery['energy'][t] == battery['capacity']]
            # for p in periods_full:
            #     try:
            #         sorted_periods.remove(p)
            #     except ValueError:
            #         pass
        return p_cheap

    def discharge_then_charge(p_cheap, p_expensive):
        # e_remaining = battery['energy'][p_expensive + 1:p_cheap]
        e_remaining_min = min(battery['energy'][p_expensive: p_cheap])

        if not e_remaining_min == 0:
            e_discharge = min(loads[p_expensive], e_remaining_discharge, e_remaining_charge, e_remaining_min)
            loads[p_expensive] -= e_discharge
            loads[p_cheap] += e_discharge
            battery['activities'][p_expensive] -= e_discharge
            battery['activities'][p_cheap] += e_discharge
            for i in range(p_expensive, p_cheap):
                battery['energy'][i] -= e_discharge
        else:
            # del sorted_periods[-1]
            # p_expensive = sorted_periods[-1]
            del sorted_periods[-1]
            p_expensive = sorted_periods[-1]
            # periods_empty = [t for t in sorted_periods if battery['energy'][t] == 0]
            # for p in periods_empty:
            #     try:
            #         sorted_periods.remove(p)
            #     except ValueError:
            #         pass
        return p_expensive

    # stage one battery scheduling
    sorted_periods0 = sorted_periods[:]
    p_cheap = sorted_periods[0]
    p_expensive = sorted_periods[-1]
    while len(sorted_periods) > 1:

        e_remaining_discharge = max_discharge_rate + battery['activities'][p_expensive]
        while (loads[p_expensive] == 0 or e_remaining_discharge == 0 or prices[p_expensive] <= prices[p_cheap]) and len(sorted_periods) > 1:
            del sorted_periods[-1]
            p_expensive = sorted_periods[-1]
            e_remaining_discharge = max_discharge_rate + battery['activities'][p_expensive]

        e_remaining_charge = max_charge_rate - battery['activities'][p_cheap]
        # e_remaining = battery['energy'][p_cheap]
        # while (e_remaining_charge_start == 0 or e_remaining == max_capacity) and len(sorted_periods) > 1:
        while e_remaining_charge == 0 and len(sorted_periods) > 1:
            del sorted_periods[0]
            p_cheap = sorted_periods[0]
            e_remaining_charge = max_charge_rate - battery['activities'][p_cheap]
            # e_remaining = battery['energy'][p_cheap]

        if len(sorted_periods) >= 2:
            if p_cheap < p_expensive:
                p_cheap = charge_then_discharge(p_cheap, p_expensive)
            # elif p_expensive < p_cheap:
            #     p_expensive = discharge_then_charge(p_cheap, p_expensive)
            else:
                del sorted_periods[-1]
                p_expensive = sorted_periods[-1]
                # del sorted_periods[0]
                # p_cheap = sorted_periods[0]

    # # stage two battery scheduling
    sorted_periods = sorted_periods0
    p_cheap = sorted_periods[0]
    p_expensive = sorted_periods[-1]
    while len(sorted_periods) > 1:

        e_remaining_discharge = max_discharge_rate + battery['activities'][p_expensive]
        e_remaining = battery['energy'][p_expensive]
        while (loads[p_expensive] == 0 or e_remaining_discharge == 0 or e_remaining == 0 or prices[p_expensive] <= prices[p_cheap]) \
                and len(sorted_periods) > 1:
            del sorted_periods[-1]
            p_expensive = sorted_periods[-1]
            e_remaining_discharge = max_discharge_rate + battery['activities'][p_expensive]
            e_remaining = battery['energy'][p_expensive]

        e_remaining_charge = max_charge_rate - battery['activities'][p_cheap]
        while e_remaining_charge == 0 and len(sorted_periods) > 1:
            del sorted_periods[0]
            p_cheap = sorted_periods[0]
            e_remaining_charge = max_charge_rate - battery['activities'][p_cheap]

        if len(sorted_periods) >= 2:
            if p_expensive < p_cheap:
                p_expensive = discharge_then_charge(p_cheap, p_expensive)
            else:
                # del sorted_periods[-1]
                # p_expensive = sorted_periods[-1]
                del sorted_periods[0]
                p_cheap = sorted_periods[0]

    return battery


