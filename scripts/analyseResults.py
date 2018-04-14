from os import path, walk, makedirs
from csv import reader


def main(data_folder):
    # output files locations
    in_directory = "results/" + data_folder + "/"
    # in_directory_sub = next(walk(in_directory))[1]
    out_directory = "analysis/results/"
    out_file = out_directory + data_folder + ".csv"

    headers = ["instance", "houses", "batteries", "itrs", "runtime", "fw_time", "pricing_time", "scheduling_time"]
    headers += ["peak_reduction", "peak_begin", "peak_end", "par_reduction", "par_begin", "par_end"]
    headers += ["bill_reduction", "bill_begin", "bill_end", "penalty_end"]
    s_out = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\r\n"

    for sub_dir in next(walk(in_directory))[1]:
        this_dir = in_directory + sub_dir
        files = next(walk(this_dir))[2]

        no_houses = 0
        no_batteries = 0
        no_itrs = 0
        total_time = 0
        fw_time = 0
        pricing_time = 0
        scheduling_time = 0
        peak_reduction = 0
        peak_begin = 0
        peak_end = 0
        par_reduction = 0
        par_begin = 0
        par_end = 0
        bill_reduction = 0
        bill_begin = 0
        bill_end = 0

        for file in files:

            if "cost" in file or "fw" in file or "load" in file or "price" in file or 'overview' in file:
                with open(this_dir + "/" + file, mode='r') as csv_file:
                    csv_reader = reader(csv_file)
                    headers = [h.strip(" \'") for h in csv_reader.next()]

                    rows = list(csv_reader)
                    no_rows = len(rows)
                    no_itrs = int(rows[no_rows - 1][0]) + 1

                    if "cost" in file:
                        bill_begin = float(rows[0][2])
                        bill_end = float(rows[no_rows - 1][2])
                        penalty_end = float(rows[no_rows - 1][3])
                        cost_begin = float(bill_begin)
                        cost_end = float(bill_end + penalty_end)

                        bill_reduction = round((bill_begin - bill_end)/bill_begin, 4) * 100
                        cost_reduction = round((cost_begin - cost_end)/cost_begin, 4) * 100

                    elif "fw" in file:
                        pass

                    elif "load" in file:
                        loads_begin = [float(x) for x in rows[0][2:]]
                        loads_end = [float(x) for x in rows[no_rows - 1][2:]]
                        no_periods = len(loads_begin)
                        peak_begin = max(loads_begin)
                        aver_begin = sum(loads_begin) / no_periods
                        peak_end = max(loads_end)
                        aver_end = sum(loads_end) / no_periods
                        par_begin = peak_begin / aver_begin
                        par_end = peak_end / aver_end

                        peak_reduction = round((peak_begin - peak_end) / peak_begin, 4) * 100
                        par_reduction = round((par_begin - par_end) / par_begin, 4) * 100

                    elif "price" in file:
                        prices_begin = [float(x) for x in rows[0][2:]]
                        prices_end = [float(x) for x in rows[no_rows - 1][2:]]
                        no_periods = len(prices_begin)
                        aver_begin = sum(prices_begin) / no_periods
                        aver_end = sum(prices_end) / no_periods

                        aver_reduction = round((aver_begin - aver_end) / aver_begin, 4) * 100

                    elif "overview" in file:
                        no_houses = rows[0][0]
                        no_batteries = rows[0][1]
                        total_time = rows[0][9]
                        fw_time = rows[0][10]
                        pricing_time = rows[0][11]
                        scheduling_time = rows[0][12]

        s_out += sub_dir + "," + str(no_houses) + "," + str(no_batteries) + "," + str(no_itrs) + ","
        s_out += str(total_time) + "," + str(fw_time) + "," + str(pricing_time) + "," + str(scheduling_time) + ","
        s_out += str(peak_reduction) + "," + str(peak_begin) + "," + str(peak_end) + ","
        s_out += str(par_reduction) + "," + str(par_begin) + "," + str(par_end) + ","
        s_out += str(bill_reduction) + "," + str(bill_begin) + "," + str(bill_end) + "," + str(penalty_end) + "\r\n"

    print "Analysing results is done."

    if not path.exists(out_directory):
        makedirs(out_directory)

    with open(out_file, 'wb') as output_file:
            output_file.write(s_out)



