from os import path, walk, makedirs
from csv import reader

i_consumption = "consumption"
i_name = "name"
i_estart = "estart"
i_pstart = "pstart"
i_lfinish = "lfinish"
i_dur = "dur"
i_caf = "caf"
i_astart = "astart"
i_bill = "bill"
i_penalty = "penalty"
i_key = 'key'
i_value = 'value'


def main(data_folder):
    in_directory = "results/" + data_folder + "/"
    # in_files = next(walk(in_directory))
    out_directory = "analysis/jobs/"
    out_file = out_directory + data_folder + ".csv"

    headers = ["instance", "total_houses", "total_jobs"]
    s_out = str(headers)[1:-1].replace("'", "").replace(" ", "") + "\n"

    for sub_dir in next(walk(in_directory))[1]:
        this_dir = in_directory + sub_dir
        files = next(walk(this_dir))[2]

        no_jobs = 0
        no_houses = 0

        for file in files:
            if "job" in file or "batter" in file:
                with open(this_dir + "/" + file, mode='r') as csv_file:
                    csv_reader = reader(csv_file)
                    headers = [h.strip(" \'") for h in csv_reader.next()]

                    rows = list(csv_reader)
                    no_jobs = len(rows)
                    no_houses = int(rows[no_jobs - 1][0]) + 1

                    for row in rows:
                        # print row
                        j_consum = row[2]
                        j_estart = row[3]
                        j_pstart = row[4]
                        j_lfinis = row[5]
                        j_durati = row[6]
                        j_carefa = row[7]
                        j_astart = row[8]

        s_out += sub_dir + "," + str(no_houses) + "," + str(no_jobs) + "\n"



    #
    #
    # header1 = [" ", "", ""]
    # header2 = ["instance", "total houses", "total jobs"]
    # blank_counters_instance = {}
    # for c in columns:
    #     blank_counters_instance[c[i_key]] = [0] * len(c['value'])
    #     for i in c['value']:
    #         header1.append(c['key'])
    #         header2.append(i)
    # output_entire = str(header1)[1:-1] + "\n" + str(header2)[1:-1] + "\n"
    # # print output_entire
    #
    # # in_files[0] is the directory path,
    # # in_files[1] is an empty list,
    # # in_files[2] are the file names in in_files[0]
    # for f in in_files[2]:
    #     if f.endswith("-J.py"):
    #         # Prepare counters
    #         new_counters_instances = deepcopy(blank_counters_instance)
    #         # Begin counting
    #         count_total_jobs = 0
    #         count_total_houses = 0
    #         for house in read(in_directory + f):
    #             count_total_houses += 1
    #             for job in house:
    #                 count_total_jobs += 1
    #                 for c in columns:
    #                     l = len(c[i_value])
    #                     indexes = [i for i in xrange(l) if c[i_value][i] >= job[c[i_key]]]
    #                     new_counters_instances[c[i_key]][indexes[0]] += 1
    #
    #         # Write output
    #         output_instance = f  + ", " + str(count_total_houses) + ", " + str(count_total_jobs) + ", "
    #         for c in columns:
    #             output_instance += str(new_counters_instances[c[i_key]])[1:-1] + ", "
    #         output_instance += "\n"
    #         output_entire += output_instance

    print ("Analysing jobs is done.")

    if not path.exists(out_directory):
        makedirs(out_directory)

    with open(out_file, 'wb') as output_file:
            output_file.write(s_out)