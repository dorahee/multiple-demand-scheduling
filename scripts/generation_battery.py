import random as r
import scripts.input_parameters as P
from csv import reader


def main(option):
    if option == "read":
        return read()
    else:
        return create()


def convert(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def read():
    with open("batteries.csv", mode='r') as file:
        csv_reader = reader(file)
        headers = [h.strip(" \'") for h in csv_reader.next()]
        del headers[0]

        community_batteries = []
        for row in csv_reader:
            del row[0]
            battery = {h: convert(i) for h, i in zip(headers, row)}
            community_batteries.append(battery)
    print("Batteries data is read.")

    return community_batteries


def create():
    attributes = ["noh", "capacity", "charge", "discharge", "min"]
    s_batteries = str(attributes)[1:-1].replace("'", "").replace(" ", "") + "\r\n"
    community_batteries = []
    for counter_h in range(P.no_houses):
        battery = dict()

        capacity = r.randint(P.min_battery_capacity, P.max_battery_capacity)
        if P.min_battery_charge < 1:
            charge = round(r.uniform(P.min_battery_charge, P.max_battery_charge), 1)
        else:
            charge = r.randint(P.min_battery_charge, P.max_battery_charge)
        if P.min_battery_discharge < 1:
            discharge = round(r.uniform(P.min_battery_discharge, P.max_battery_discharge), 1)
        else:
            discharge = r.randint(P.min_battery_discharge, P.max_battery_discharge)
        min = r.randint(P.min_battery_remain, P.max_battery_remain)

        battery['name'] = "b" + str(counter_h)
        battery['capacity'] = capacity
        battery['charge'] = charge
        battery['discharge'] = discharge
        battery['min'] = min

        s_batteries += str(counter_h) + "," + str(capacity) + "," + str(charge) + "," + str(discharge) + "," \
                        + str(min) + "\r\n"

        community_batteries.append(battery)

    with open('batteries.csv', 'w') as output_file:
            output_file.write(s_batteries)
    print("Batteries data is generated.")

    return community_batteries


# Version history:
# 0.1 - initial script
# 0.2 - fixed the periods error (changed p.no_periods to p.no_pricing_periods)
# 0.3 - fixed indentation from 'with open' to 'return'
# 0.5 - added an ID for each battery
