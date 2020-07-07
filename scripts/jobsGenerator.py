import bisect
import random as r
from numpy import sqrt, pi, random
import scripts.inputs as P
from csv import reader


def main(option):
    if option == "read":
        return read()
        # visualise(community)
    else:
        return create()


def convert(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def read():
    with open(P.jobs_file, mode='r') as file:
        csv_reader = reader(file)
        headers = [h.strip(" \'") for h in csv_reader.next()]
        del headers[0]

        community = []
        household = []
        for row in csv_reader:
            if int(row[1]) == 0 and int(row[0]) > 0:
                community.append(household)
                household = []
            del row[0]
            job = {h: convert(i) for h, i in zip(headers[:len(row)], row)}
            household.append(job)
        community.append(household)

    # community = community_json
    print ("Job data is read from {}.".format(P.jobs_file))

    return community


def create():
    p_d = P.prob
    p_d_short = p_d[1]
    l_demands = P.devices

    p_d_long = []
    for i in list(range(len(p_d_short) - 1)):
        for j in list(range(P.interval)):
            p_d_long.append(p_d_short[i] + (p_d_short[i + 1] - p_d_short[i]) / P.interval * j)

    # i should be 46 at this time
    i = len(p_d_short) - 2  # make sure i is 46
    for j in range(P.interval):
        p_d_long.append(p_d_short[i + 1] + (p_d_short[i + 1] - p_d_short[i]) / P.interval * j)

    p_d_min = p_d_long[0] - p_d_long[0] / 3
    p_d_max = p_d_long[P.no_intervals_day - 1]

    # I meant mean value is 40 minutes
    mean_value = 40.0 / (24.0 * 60.0 / P.no_intervals_day)
    mode_value = sqrt(2 / pi) * mean_value

    community = []
    attributes = ["noh", "name", "demand", "estart", "pstart", "lfinish", "dur", "caf", "astart",
                  "predecessor", "max-succeeding-delay"]
    s_community = str(attributes)[1:-1].replace("'", "").replace(" ", "") + "\r\n"
    for counter_h in range(P.no_houses):
        # household instance
        # household = H.Household()
        # household.name = "household" + str(counter_h)
        no_jobs = r.randint(P.no_jobs_min, P.no_jobs_max)
        # household.no_jobs = no_jobs + 1
        household = []
        s_household = ""
        for counter_j in range(no_jobs):
            job = dict()

            # job name
            name = str(counter_j)

            # job consumption per hour
            demand = r.choice(l_demands)

            # job duration
            seed = r.uniform(p_d_min, p_d_max)
            middle_point = bisect.bisect(p_d_long, seed)

            duration = int(random.rayleigh(mode_value, 1)[0])
            while duration == 0:
                duration = int(random.rayleigh(mode_value, 1)[0])

            # job preferred start time
            p_start = (middle_point - int(duration / 2)) % P.no_intervals_day
            # if p_start < 0:
            #     p_start += P.no_intervals_day - 1

            # job earliest starting time
            e_start = r.choice([i for i in range(-duration + 1, p_start + 1)])
            e_start = 0

            # job latest finish time
            l_finish = r.choice([i for i in range(p_start - duration + 1, P.no_intervals_day - 1 + duration)])
            l_finish = P.no_intervals_day - 1
            # l_finish = p_start - 2

            # job care factor
            care_f = round(r.random(), 1)
            if care_f == 0:
                care_f = 0.01
            # care_f = 0

            # job instance
            job['name'] = name
            job['demand'] = demand
            job['estart'] = e_start
            job['pstart'] = p_start
            job['lfinish'] = l_finish
            job['dur'] = duration
            job['caf'] = care_f
            job['astart'] = p_start

            s_household += str(counter_h) + "," + name + "," + str(demand) + "," + str(e_start) + "," \
                         + str(p_start) + "," + str(l_finish) + "," + str(duration) + "," + str(care_f) + "," \
                           + str(p_start)

            if r.choice([True, False]) and counter_j > 0:
                id_predecessor_set = [i for i in range(counter_j)]
                id_predecessor = r.choice(id_predecessor_set)
                job['predecessor'] = id_predecessor
                s_household += "," + str(id_predecessor)

                delay = 0 if household[id_predecessor]['dur'] + job['dur'] >= P.no_intervals_day \
                    else r.randint(0, P.no_intervals_day - household[id_predecessor]['dur'] - job['dur'] - 1)
                # delay = 144
                job['max-succeeding-delay'] = delay
                s_household += "," + str(delay)

                # while household[id_predecessor]['pstart'] - job['pstart']:
                #     id_predecessor_set.remove(id_predecessor)
                #     if len(id_predecessor_set) > 0:
                #         id_predecessor = r.choice(id_predecessor_set)
                #     else:
                #         break
                #
                # if len(id_predecessor_set) > 0:
                #     job['predecessor'] = id_predecessor
                #     delay = 0 if household[id_predecessor]['dur'] + job['dur'] >= P.no_intervals_day \
                #         else r.randint(0, P.no_intervals_day - household[id_predecessor]['dur'] - job['dur'] - 1)
                #     job['max-succeeding-delay'] = delay
                #     s_household += "," + str(id_predecessor) + "," + str(delay)

            # print (job)

            # job added to the household
            household.append(job)
            s_household += "\r\n"
        # household added to the community
        community.append(household)
        s_community += s_household
        # community.aggregated_loads = [x + y for x, y in zip(community.aggregated_loads, household.aggregated_loads)]

    with open(P.jobs_file, 'w') as output_file:
        output_file.write(s_community)
    print("Job data is generated and saved to {}.".format(P.jobs_file))

    return community

# create()