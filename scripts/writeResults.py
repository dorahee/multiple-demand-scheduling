from datetime import datetime
from os import path, makedirs
from shutil import copy, copytree


def prepare(no_houses, no_batteries, no_jobs_max, no_jobs_min,
            battery_cap, battery_charge, battery_discharge,
            lookup_coeff, lookup_file, notes, penalty_coefficient, no_intervals_day,
            no_pricing_periods, demands, prices, lookup_base):
    headers_periods = [str(i + 1) for i in range(no_pricing_periods)]

    headers = ["house"] + headers_periods
    s_loads_houses = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\r\n"

    headers = ["households", "batteries", "maxJobs", "minJobs",
               "battery_cap", "battery_charge", "battery_discharge",
               "lookupf", "lookupfile", "notes", "unhappinessf", "schedulingp",
               "time", "fw_time", "pricing_time", "scheduling_time", "convergence", "use_globals"]
    s_overview = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\r\n"

    # if not lookup_file == "":
    #     lookup_file = lookup_file
    #     notes = lookup_file[
    #             lookup_file.index("lookup") + len("lookup") + 1: lookup_file.index("-zero")] + "% renewable."
    # else:
    #     lookup_file = ""
    #     notes = ""

    s_overview += str(no_houses) + "," + str(no_batteries) + "," + str(no_jobs_max) + "," + str(
        no_jobs_min) + "," + str(battery_cap) + "," + str(battery_charge) + "," + str(battery_discharge) + "," + str(lookup_coeff) + "," \
                  + str(lookup_file) + "," + str(notes) + "," + str(penalty_coefficient) + "," + str(no_intervals_day) + ","

    headers = ["itr", "type", "tbill", "tpenalty", "obj"]
    s_costs = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\r\n"

    headers = ["prices"] + headers_periods
    s_lookup = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\r\n"
    for row in lookup_base:
        rows = ""
        for index, item in enumerate(row):
            if index == 0:
                rows += str(item)
            else:
                rows += "," + str(item * lookup_coeff)
        s_lookup += rows + "\r\n"

    headers = ["itr", "type"] + headers_periods
    s_demands = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\r\n"
    s_demands += "0," + "o," + str(demands)[1:-1].replace(" ", "") + "\r\n"
    s_demands += "0," + "f," + str(demands)[1:-1].replace(" ", "") + "\r\n"

    s_prices = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\r\n"
    s_prices += "0," + "o," + str(prices)[1:-1].replace(" ", "") + "\r\n"
    s_prices += "0," + "f," + str(prices)[1:-1].replace(" ", "") + "\r\n"

    headers = ["itr", "alpha", "fw_itrs_t", "fw_itrs", "fw_obj", "fw_slope"]
    s_fw = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\r\n"

    nowtime = datetime.now()
    # now = nowtime.strftime("%y-%m-%d_%H.%M.%S") + "." + str(nowtime.microsecond)
    now = nowtime.strftime("%H.%M.%S") + "." + str(nowtime.microsecond)
    date_name = datetime.now().strftime("%y-%m-%d")
    directory = "results/" + date_name + "/"
    sub_dir = directory + now + "-" + str(no_houses) + "h" + "/"

    if not path.exists(sub_dir):
        makedirs(sub_dir)

    return s_loads_houses, s_overview, s_costs, s_lookup, s_demands, s_prices, s_fw, sub_dir


def append(sub_dir, s_demands, s_costs, s_prices, s_fw):

    file_name = "costs.csv"
    with open(sub_dir + file_name, 'a') as output_file:
        output_file.write(s_costs)

    file_name = "loads.csv"
    with open(sub_dir + file_name, 'a') as output_file:
        output_file.write(s_demands)

    file_name = "prices.csv"
    with open(sub_dir + file_name, 'a') as output_file:
        output_file.write(s_prices)

    file_name = "fw.csv"
    with open(sub_dir + file_name, 'a') as output_file:
        output_file.write(s_fw)


def final(sub_dir, s_overview, s_loads, s_costs, s_prices, s_fw, s_lookup,
          s_loads_houses, h, i, r, t, data, incon, lookup, notes, jobs_file):

    file_name = "overview.csv"
    with open(sub_dir + file_name, 'w') as output_file:
        output_file.write(s_overview)

    # file_name = "costs.csv"
    # with open(sub_dir + file_name, 'wb') as output_file:
    #     output_file.write(s_costs)
    #
    # file_name = "loads.csv"
    # with open(sub_dir + file_name, 'wb') as output_file:
    #     output_file.write(s_loads)
    #
    # file_name = "prices.csv"
    # with open(sub_dir + file_name, 'wb') as output_file:
    #     output_file.write(s_prices)
    #
    # file_name = "fw.csv"
    # with open(sub_dir + file_name, 'wb') as output_file:
    #     output_file.write(s_fw)

    file_name = "lookup.csv"
    with open(sub_dir + file_name, 'w') as output_file:
        output_file.write(s_lookup)

    file_name = "notes.txt"
    with open(sub_dir + file_name, 'w') as output_file:
        output_file.write(notes)

    copy(jobs_file, sub_dir)
    copy("batteries.csv", sub_dir)
    copy("scripts/inputs.py", sub_dir)

    print("Results data is written.")
