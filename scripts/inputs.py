__author__ = 'dora'

# ------ BEGIN: CUSTOMISABLE DATA ------
load_data = "read"
# load_data = "create"

use_solver = False
# use_solver = True

use_globals = True

show_astart = False
# show_astart = True

# battery_data = "read"
# battery_data = "create"
battery_data = "null"

# use_battery = 1
use_battery = 0

lookup_base = ""

# 1. Parameters for running the program
no_itrs = 100
no_intervals_day = 144
no_pricing_periods = 48
interval = no_intervals_day / no_pricing_periods

# 2. Parameters for generating data
no_houses = 1000
no_jobs_min = 5
no_jobs_max = 5
i_demand = "demand"
i_name = "name"
i_estart = "estart"
i_pstart = "pstart"
i_lfinish = "lfinish"
i_dur = "dur"
i_caf = "caf"
i_astart = "astart"
i_bill = "bill"
i_penalty = "penalty"
i_predecessor = "predecessor"
i_succeeding_delay = "max-succeeding-delay"

# 3. Parameters for scheduling jobs
penalty_coefficient = 10
randomization = 0
minizinc_model = "household.mzn"
minizinc_data = "household.dzn"

# 4. Parameters for computing prices
lookup_param = 1.0
next_level_difference = 0.001

# 5. Parameters for scheduling batteries
min_battery_capacity = 12
max_battery_capacity = 12
min_battery_charge = 4
max_battery_charge = 4
min_battery_discharge = 5
max_battery_discharge = 5
min_battery_remain = 0
max_battery_remain = min_battery_remain

# 6. default result folders and files
jobs_file = "jobs.csv"
batteries_file = "batteries.csv"

# ------ END: CUSTOMISABLE DATA ------

# ------ BEGIN: DO NOT CHANGE THE FOLLOWING DATA ------
devices = [1.5, 2.3, 3.5, 6, 0.008, 1.1, 2.4, 0.6, 0.5, 0.004, 0.002, 4, 0.6, 0.1, 0.015, 2.4, 0.05, 0.12, 1.2, 2.2,
           0.7, 1.7, 2.1, 0.0015, 0.09, 0.05, 0.01, 0.056, 0.072, 0.65, 2, 1.5, 0.1, 2.4, 1.2, 2.4, 1.2, 1, 0.3, 2.4,
           1.2, 0.075, 0.052, 0.015, 0.045, 0.011, 0.0625, 0.15, 1, 0.005, 1.1, 5, 0.55, 0.1, 0.14, 0.038, 0.035,
           0.068, 0.072, 0.093, 0.148, 0.7, 0.3, 1, 0.08, 0.12, 0.015, 6, 0.02, 0.075, 0.055, 0.03, 0.13, 0.05, 0.21,
           0.1, 0.005, 1, 3.6, 1.2, 0.9, 1.2, 1.2, 0.05, 0.06, 0.9, 0.4, 2.4, 0.35, 2]

# Option 1 - typical Victoria summer demand profile at 2026, medium scenario, 50 probability
# prob = [
#     [2011, 1827, 2110, 1949, 1718, 1546, 1445, 1403, 1463, 1590,
#      1887, 2196, 2326, 2559, 2570, 2650, 2755, 2797, 2834, 2864,
#      2889, 2914, 2922, 2926, 2935, 2937, 2946, 2936, 2914, 2905,
#      2917, 2922, 2897, 2860, 2748, 2649, 2556, 2545, 2546, 2543,
#      2487, 2456, 2404, 2227, 2084, 1999, 2310, 2246],
#     [2011, 3838, 5948, 7897, 9615, 11161, 12606, 14009, 15472, 17062,
#      18949, 21145, 23471, 26030, 28600, 31250, 34005, 36802, 39636, 42500,
#      45389, 48303, 51225, 54151, 57086, 60023, 62969, 65905, 68819, 71724,
#      74641, 77563, 80460, 83320, 86068, 88717, 91273, 93818, 96364, 98907,
#      101394, 103850, 106254, 108481, 110565, 112564, 114874, 117120]
# ]

# Option 2
# prob = [
#     [2222,2022,1794,1586,1431,1323,1268,1254,1305,1431,
#      1729,2094,2750,3199,3646,3642,3329,2952,2590,2291,
#      2048,1892,1764,1768,1743,1814,1889,2025,2142,2357,
#      2627,3051,3548,3946,4449,4860,4896,4864,4758,4738,
#      4706,4475,4174,3876,3536,3200,2966,2689],
#     [2222,4244,6038,7624,9055,10378,11646,12900,14205,15636,
#      17365,19459,22209,25408,29054,32696,36025,38977,41567,43858,
#      45906,47798,49562,51330,53073,54887,56776,58801,60943,63300,
#      65927,68978,72526,76472,80921,85781,90677,95541,100299,105037,
#      109743,114218,118392,122268,125804,129004,131970,134659]
# ]

# Option 3 - Peaky Queensland winter demand profile at 2026, high scenario, 50 probability
prob = [
    [2722, 2522, 2294, 2086, 1931, 1823, 1768, 1754, 1805, 1931,
     2229, 2594, 3250, 3699, 4146, 4142, 3829, 3452, 3090, 2791,
     2548, 2392, 2264, 2268, 2243, 2314, 2389, 2525, 2642, 2857,
     3127, 3551, 4048, 4446, 4949, 5360, 5396, 5364, 5258, 5238,
     5206, 4975, 4674, 4376, 4036, 3700, 3466, 3189],
    [2722, 5244, 7538, 9624, 11555, 13378, 15146, 16900, 18705, 20636,
     22865, 25459, 28709, 32408, 36554, 40696, 44525, 47977, 51067, 53858,
     56406, 58798, 61062, 63330, 65573, 67887, 70276, 72801, 75443, 78300,
     81427, 84978, 89026, 93472, 98421, 103781, 109177, 114541, 119799, 125037,
     130243, 135218, 139892, 144268, 148304, 152004, 155470, 158659]
]

# Option 4 - Flat
# prob = [[0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333,
#          0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333,
#          0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333,
#          0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333,
#          0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333,
#          0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333, 0.020833333],
#         [0.020833333, 0.041666667, 0.0625, 0.083333333, 0.104166667, 0.125, 0.145833333, 0.166666667,
#          0.1875, 0.208333333, 0.229166667, 0.25, 0.270833333, 0.291666667, 0.3125, 0.333333333,
#          0.354166667, 0.375, 0.395833333, 0.416666667, 0.4375, 0.458333333, 0.479166667, 0.5,
#          0.520833333, 0.541666667, 0.5625, 0.583333333, 0.604166667, 0.625, 0.645833333, 0.666666667,
#          0.6875, 0.708333333, 0.729166667, 0.75, 0.770833333, 0.791666667, 0.8125, 0.833333333,
#          0.854166667, 0.875, 0.895833333, 0.916666667, 0.9375, 0.958333333, 0.979166667, 1]
#         ]

# Option 5 - Triangle
# prob = [[0.001666667, 0.003333333, 0.005, 0.006666667, 0.008333333, 0.01, 0.011666667, 0.013333333, 0.015, 0.01666667,
#          0.018333333, 0.02, 0.021666667, 0.023333333, 0.025, 0.026666667, 0.028333333, 0.03, 0.031666667, 0.033333333,
#          0.035, 0.036666667, 0.038333333, 0.04, 0.04, 0.038333333, 0.036666667, 0.035, 0.033333333, 0.031666667, 0.03,
#          0.028333333, 0.026666667, 0.025, 0.023333333, 0.021666667, 0.02, 0.018333333, 0.016666667, 0.015, 0.01333333,
#          0.011666667, 0.01, 0.008333333, 0.006666667, 0.005, 0.003333333, 0.001666667],
#         [0.001666667, 0.005, 0.01, 0.016666667, 0.025, 0.035, 0.046666667, 0.06, 0.075, 0.091666667, 0.11, 0.13,
#          0.151666667, 0.175, 0.2, 0.226666667, 0.255, 0.285, 0.316666667, 0.35, 0.385, 0.421666667, 0.46, 0.5, 0.54,
#          0.578333333, 0.615, 0.65, 0.683333333, 0.715, 0.745, 0.773333333, 0.8, 0.825, 0.848333333, 0.87, 0.89,
#          0.908333333, 0.925, 0.94, 0.953333333, 0.965, 0.975, 0.983333333, 0.99, 0.995, 0.998333333, 1]]

# Option 1 = all periods same pricing table
lookup_base = [
    # originally 14.1
    [14.0, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031,
     0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031,
     0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031,
     0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031, 0.5031],
    # originally 14.2
    [14.1, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215,
     0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215,
     0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215,
     0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215, 0.5215],
    [14.2, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337,
     0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337,
     0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337,
     0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337, 0.5337],
    [14.3, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521,
     0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521,
     0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521,
     0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521, 0.5521],
    [14.4, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706,
     0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706,
     0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706,
     0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706, 0.5706],
    [14.5, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589,
     0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589,
     0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589, 0.589,
     0.589],
    [14.6, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074,
     0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074,
     0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074,
     0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074, 0.6074],
    [14.8, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196,
     0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196,
     0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196,
     0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196, 0.6196],
    [15.1, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638,
     0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638,
     0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638, 0.638,
     0.638],
    [15.4, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564,
     0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564,
     0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564,
     0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564, 0.6564],
    [15.8, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748,
     0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748,
     0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748,
     0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748, 0.6748],
    [16.3, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933,
     0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933,
     0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933,
     0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933, 0.6933],
    [17, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055,
     0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055,
     0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055,
     0.7055, 0.7055, 0.7055, 0.7055, 0.7055, 0.7055],
    [17.8, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239,
     0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239,
     0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239,
     0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239, 0.7239],
    [18.9, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423,
     0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423,
     0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423,
     0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423, 0.7423],
    [20.3, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607,
     0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607,
     0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607,
     0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607, 0.7607],
    [22.1, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791,
     0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791,
     0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791,
     0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791, 0.7791],
    [24.5, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914,
     0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914,
     0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914,
     0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914, 0.7914],
    [27.5, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098,
     0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098,
     0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098,
     0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098, 0.8098],
    [31.3, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282,
     0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282,
     0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282,
     0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282, 0.8282],
    [36.3, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466,
     0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466,
     0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466,
     0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466, 0.8466],
    [42.7, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865,
     0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865,
     0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865, 0.865,
     0.865],
    [50.9, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834,
     0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834,
     0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834,
     0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834, 0.8834],
    [61.6, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957,
     0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957,
     0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957,
     0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957, 0.8957],
    [75.2, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141,
     0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141,
     0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141,
     0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141, 0.9141],
    [92.8, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325,
     0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325,
     0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325,
     0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325, 0.9325],
    [115.5, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509,
     0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509,
     0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509,
     0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509, 0.9509],
    [144.6, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693,
     0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693,
     0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693,
     0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693, 0.9693],
    [182.1, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816,
     0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816,
     0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816,
     0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816, 0.9816],
    [230.4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Option 2 = periods have different pricing table
# lookup_base = [
#     [14.14, 0.2497, 0.2482, 0.2452, 0.2436, 0.2461, 0.2593, 0.5742, 0.261, 0.562, 0.261, 0.2589, 0.2575, 0.2558, 0.2556,
#      0.2572, 0.26, 0.6067, 0.642, 0.7132, 0.7464, 0.7641, 0.7559, 0.7469, 0.672, 0.701, 0.7034, 0.6809, 0.6658, 0.7149,
#      0.7598, 0.7524, 0.7651, 0.7496, 0.7371, 0.7455, 0.7602, 0.7352, 0.616, 0.6036, 0.2593, 0.2514, 0.2484, 0.247,
#      0.2463, 0.2438, 0.2426, 0.2424, 0.2423],
#     [14.18, 0.2578, 0.2563, 0.2533, 0.2517, 0.2542, 0.2674, 0.5823, 0.2691, 0.5701, 0.2691, 0.267, 0.2656, 0.2639,
#      0.2637, 0.2653, 0.2681, 0.6148, 0.6501, 0.7213, 0.7545, 0.7722, 0.764, 0.755, 0.6801, 0.7091, 0.7115, 0.689,
#      0.6739, 0.723, 0.7679, 0.7605, 0.7732, 0.7577, 0.7452, 0.7536, 0.7683, 0.7433, 0.6241, 0.6117, 0.2674, 0.2595,
#      0.2565, 0.2551, 0.2544, 0.2519, 0.2507, 0.2505, 0.2504],
#     [14.23, 0.2659, 0.2644, 0.2614, 0.2598, 0.2623, 0.2755, 0.5904, 0.2772, 0.5782, 0.2772, 0.2751, 0.2737, 0.272,
#      0.2718, 0.2734, 0.2762, 0.6229, 0.6582, 0.7294, 0.7626, 0.7803, 0.7721, 0.7631, 0.6882, 0.7172, 0.7196, 0.6971,
#      0.682, 0.7311, 0.776, 0.7686, 0.7813, 0.7658, 0.7533, 0.7617, 0.7764, 0.7514, 0.6322, 0.6198, 0.2755, 0.2676,
#      0.2646, 0.2632, 0.2625, 0.26, 0.2588, 0.2586, 0.2585],
#     [14.3, 0.274, 0.2725, 0.2695, 0.2679, 0.2704, 0.2836, 0.5985, 0.2853, 0.5863, 0.2853, 0.2832, 0.2818, 0.2801,
#      0.2799, 0.2815, 0.2843, 0.631, 0.6663, 0.7375, 0.7707, 0.7884, 0.7802, 0.7712, 0.6963, 0.7253, 0.7277, 0.7052,
#      0.6901, 0.7392, 0.7841, 0.7767, 0.7894, 0.7739, 0.7614, 0.7698, 0.7845, 0.7595, 0.6403, 0.6279, 0.2836, 0.2757,
#      0.2727, 0.2713, 0.2706, 0.2681, 0.2669, 0.2667, 0.2666],
#     [14.39, 0.2821, 0.2806, 0.2776, 0.276, 0.2785, 0.2917, 0.6066, 0.2933, 0.5944, 0.2934, 0.2913, 0.2899, 0.2882,
#      0.288, 0.2896, 0.2924, 0.6391, 0.6744, 0.7456, 0.7788, 0.7965, 0.7883, 0.7793, 0.7044, 0.7334, 0.7358, 0.7133,
#      0.6982, 0.7473, 0.7922, 0.7848, 0.7975, 0.782, 0.7695, 0.7779, 0.7926, 0.7676, 0.6484, 0.636, 0.2917, 0.2838,
#      0.2808, 0.2794, 0.2787, 0.2762, 0.275, 0.2748, 0.2747],
#     [14.5, 0.2902, 0.2887, 0.2857, 0.2841, 0.2866, 0.2998, 0.6147, 0.3014, 0.6025, 0.3015, 0.2994, 0.298, 0.2963,
#      0.2961, 0.2977, 0.3005, 0.6472, 0.6825, 0.7537, 0.7869, 0.8046, 0.7964, 0.7874, 0.7125, 0.7415, 0.7439, 0.7213,
#      0.7063, 0.7554, 0.8003, 0.7929, 0.8056, 0.7901, 0.7776, 0.786, 0.8007, 0.7757, 0.6565, 0.6441, 0.2998, 0.2919,
#      0.2889, 0.2875, 0.2868, 0.2843, 0.2831, 0.2829, 0.2828],
#     [14.65, 0.2983, 0.2968, 0.2938, 0.2922, 0.2947, 0.3079, 0.6228, 0.3095, 0.6106, 0.3096, 0.3075, 0.3061, 0.3044,
#      0.3042, 0.3058, 0.3086, 0.6553, 0.6906, 0.7618, 0.795, 0.8127, 0.8045, 0.7955, 0.7206, 0.7496, 0.752, 0.7294,
#      0.7144, 0.7635, 0.8084, 0.801, 0.8137, 0.7982, 0.7857, 0.7941, 0.8088, 0.7838, 0.6646, 0.6522, 0.3079, 0.3, 0.297,
#      0.2956, 0.2949, 0.2924, 0.2912, 0.291, 0.2909],
#     [14.83, 0.3064, 0.3049, 0.3019, 0.3003, 0.3028, 0.316, 0.6309, 0.3176, 0.6187, 0.3177, 0.3156, 0.3142, 0.3125,
#      0.3123, 0.3139, 0.3167, 0.6634, 0.6987, 0.7699, 0.8031, 0.8208, 0.8126, 0.8036, 0.7287, 0.7577, 0.7601, 0.7375,
#      0.7225, 0.7716, 0.8165, 0.8091, 0.8218, 0.8063, 0.7938, 0.8022, 0.8169, 0.7919, 0.6727, 0.6603, 0.316, 0.3081,
#      0.3051, 0.3037, 0.303, 0.3005, 0.2993, 0.2991, 0.299],
#     [15.07, 0.3145, 0.313, 0.31, 0.3084, 0.3109, 0.3241, 0.639, 0.3257, 0.6268, 0.3258, 0.3237, 0.3223, 0.3206, 0.3204,
#      0.322, 0.3248, 0.6715, 0.7068, 0.778, 0.8111, 0.8289, 0.8207, 0.8117, 0.7368, 0.7658, 0.7682, 0.7456, 0.7306,
#      0.7797, 0.8246, 0.8172, 0.8299, 0.8143, 0.8019, 0.8103, 0.825, 0.8, 0.6808, 0.6684, 0.3241, 0.3162, 0.3132, 0.3118,
#      0.3111, 0.3086, 0.3074, 0.3071, 0.3071],
#     [15.38, 0.3226, 0.3211, 0.3181, 0.3165, 0.319, 0.3322, 0.6471, 0.3338, 0.6349, 0.3339, 0.3318, 0.3304, 0.3287,
#      0.3285, 0.3301, 0.3329, 0.6796, 0.7149, 0.7861, 0.8192, 0.837, 0.8288, 0.8198, 0.7449, 0.7739, 0.7763, 0.7537,
#      0.7387, 0.7878, 0.8327, 0.8253, 0.838, 0.8224, 0.81, 0.8184, 0.8331, 0.8081, 0.6889, 0.6765, 0.3322, 0.3243,
#      0.3213, 0.3199, 0.3192, 0.3167, 0.3155, 0.3152, 0.3152],
#     [15.78, 0.3307, 0.3292, 0.3262, 0.3246, 0.3271, 0.3403, 0.6552, 0.3419, 0.643, 0.342, 0.3399, 0.3385, 0.3368,
#      0.3366, 0.3382, 0.341, 0.6877, 0.723, 0.7942, 0.8273, 0.8451, 0.8368, 0.8279, 0.753, 0.782, 0.7844, 0.7618, 0.7468,
#      0.7959, 0.8408, 0.8334, 0.8461, 0.8305, 0.8181, 0.8265, 0.8412, 0.8162, 0.697, 0.6846, 0.3403, 0.3324, 0.3294,
#      0.328, 0.3273, 0.3248, 0.3236, 0.3233, 0.3233],
#     [16.29, 0.3388, 0.3373, 0.3343, 0.3327, 0.3352, 0.3484, 0.6633, 0.35, 0.6511, 0.3501, 0.348, 0.3466, 0.3449, 0.3447,
#      0.3463, 0.3491, 0.6958, 0.7311, 0.8023, 0.8354, 0.8532, 0.8449, 0.836, 0.7611, 0.7901, 0.7925, 0.7699, 0.7549,
#      0.804, 0.8489, 0.8415, 0.8542, 0.8386, 0.8262, 0.8346, 0.8493, 0.8243, 0.7051, 0.6927, 0.3484, 0.3405, 0.3375,
#      0.3361, 0.3354, 0.3329, 0.3317, 0.3314, 0.3314],
#     [16.95, 0.3469, 0.3454, 0.3424, 0.3407, 0.3433, 0.3565, 0.6714, 0.3581, 0.6592, 0.3582, 0.3561, 0.3547, 0.353,
#      0.3528, 0.3544, 0.3572, 0.7039, 0.7392, 0.8104, 0.8435, 0.8613, 0.853, 0.8441, 0.7692, 0.7982, 0.8006, 0.778,
#      0.763, 0.8121, 0.857, 0.8496, 0.8623, 0.8467, 0.8343, 0.8427, 0.8574, 0.8324, 0.7132, 0.7008, 0.3565, 0.3486,
#      0.3456, 0.3442, 0.3435, 0.341, 0.3398, 0.3395, 0.3395],
#     [17.8, 0.355, 0.3535, 0.3505, 0.3488, 0.3514, 0.3646, 0.6795, 0.3662, 0.6673, 0.3663, 0.3642, 0.3628, 0.3611,
#      0.3609, 0.3625, 0.3653, 0.712, 0.7473, 0.8185, 0.8516, 0.8694, 0.8611, 0.8522, 0.7773, 0.8063, 0.8087, 0.7861,
#      0.7711, 0.8202, 0.8651, 0.8577, 0.8704, 0.8548, 0.8424, 0.8508, 0.8655, 0.8405, 0.7213, 0.7089, 0.3646, 0.3567,
#      0.3537, 0.3523, 0.3516, 0.3491, 0.3479, 0.3476, 0.3476],
#     [18.9, 0.3631, 0.3616, 0.3586, 0.3569, 0.3595, 0.3727, 0.6876, 0.3743, 0.6754, 0.3744, 0.3723, 0.3709, 0.3692,
#      0.369, 0.3706, 0.3734, 0.7201, 0.7554, 0.8266, 0.8597, 0.8775, 0.8692, 0.8603, 0.7854, 0.8144, 0.8168, 0.7942,
#      0.7792, 0.8283, 0.8731, 0.8658, 0.8785, 0.8629, 0.8505, 0.8589, 0.8736, 0.8486, 0.7294, 0.717, 0.3727, 0.3648,
#      0.3618, 0.3604, 0.3597, 0.3572, 0.356, 0.3557, 0.3557],
#     [20.31, 0.3712, 0.3697, 0.3667, 0.365, 0.3676, 0.3808, 0.6957, 0.3824, 0.6835, 0.3825, 0.3804, 0.379, 0.3773,
#      0.3771, 0.3787, 0.3815, 0.7282, 0.7635, 0.8347, 0.8678, 0.8856, 0.8773, 0.8684, 0.7935, 0.8225, 0.8249, 0.8023,
#      0.7873, 0.8364, 0.8812, 0.8739, 0.8866, 0.871, 0.8586, 0.867, 0.8817, 0.8567, 0.7375, 0.7251, 0.3808, 0.3729,
#      0.3699, 0.3685, 0.3678, 0.3653, 0.3641, 0.3638, 0.3638],
#     [22.12, 0.3793, 0.3778, 0.3748, 0.3731, 0.3757, 0.3889, 0.7038, 0.3905, 0.6916, 0.3906, 0.3885, 0.3871, 0.3854,
#      0.3852, 0.3867, 0.3896, 0.7363, 0.7716, 0.8428, 0.8759, 0.8937, 0.8854, 0.8765, 0.8016, 0.8306, 0.833, 0.8104,
#      0.7954, 0.8445, 0.8893, 0.882, 0.8947, 0.8791, 0.8667, 0.8751, 0.8898, 0.8648, 0.7456, 0.7332, 0.3889, 0.381,
#      0.378, 0.3766, 0.3758, 0.3734, 0.3722, 0.3719, 0.3719],
#     [24.45, 0.3874, 0.3859, 0.3829, 0.3812, 0.3838, 0.397, 0.7119, 0.3986, 0.6997, 0.3987, 0.3966, 0.3952, 0.3935,
#      0.3933, 0.3948, 0.3977, 0.7444, 0.7797, 0.8509, 0.884, 0.9018, 0.8935, 0.8846, 0.8097, 0.8387, 0.8411, 0.8185,
#      0.8035, 0.8526, 0.8974, 0.8901, 0.9028, 0.8872, 0.8748, 0.8832, 0.8979, 0.8729, 0.7537, 0.7413, 0.397, 0.3891,
#      0.3861, 0.3847, 0.3839, 0.3815, 0.3803, 0.38, 0.38],
#     [27.45, 0.3955, 0.394, 0.391, 0.3893, 0.3919, 0.4051, 0.72, 0.4067, 0.7078, 0.4068, 0.4047, 0.4033, 0.4016, 0.4014,
#      0.4029, 0.4058, 0.7525, 0.7878, 0.8589, 0.8921, 0.9099, 0.9016, 0.8927, 0.8178, 0.8468, 0.8492, 0.8266, 0.8116,
#      0.8607, 0.9055, 0.8982, 0.9109, 0.8953, 0.8829, 0.8913, 0.906, 0.881, 0.7618, 0.7494, 0.4051, 0.3972, 0.3942,
#      0.3928, 0.392, 0.3896, 0.3884, 0.3881, 0.3881],
#     [31.32, 0.4036, 0.4021, 0.3991, 0.3974, 0.4, 0.4132, 0.7281, 0.4148, 0.7159, 0.4149, 0.4128, 0.4114, 0.4097, 0.4095,
#      0.411, 0.4139, 0.7606, 0.7959, 0.867, 0.9002, 0.918, 0.9097, 0.9008, 0.8259, 0.8549, 0.8572, 0.8347, 0.8197,
#      0.8688, 0.9136, 0.9063, 0.919, 0.9034, 0.891, 0.8994, 0.9141, 0.8891, 0.7699, 0.7575, 0.4132, 0.4053, 0.4023,
#      0.4009, 0.4001, 0.3977, 0.3965, 0.3962, 0.3962],
#     [36.29, 0.4117, 0.4102, 0.4072, 0.4055, 0.4081, 0.4213, 0.7362, 0.4229, 0.724, 0.423, 0.4209, 0.4195, 0.4178,
#      0.4176, 0.4191, 0.422, 0.7687, 0.804, 0.8751, 0.9083, 0.9261, 0.9178, 0.9089, 0.834, 0.863, 0.8653, 0.8428, 0.8278,
#      0.8769, 0.9217, 0.9144, 0.9271, 0.9115, 0.8991, 0.9074, 0.9222, 0.8972, 0.778, 0.7656, 0.4213, 0.4134, 0.4104,
#      0.409, 0.4082, 0.4058, 0.4046, 0.4043, 0.4043],
#     [42.7, 0.4198, 0.4183, 0.4153, 0.4136, 0.4162, 0.4294, 0.7443, 0.431, 0.7321, 0.4311, 0.429, 0.4276, 0.4259, 0.4257,
#      0.4272, 0.4301, 0.7768, 0.8121, 0.8832, 0.9164, 0.9342, 0.9259, 0.917, 0.8421, 0.8711, 0.8734, 0.8509, 0.8359,
#      0.885, 0.9298, 0.9224, 0.9352, 0.9196, 0.9072, 0.9155, 0.9303, 0.9053, 0.7861, 0.7737, 0.4294, 0.4215, 0.4185,
#      0.4171, 0.4163, 0.4139, 0.4127, 0.4124, 0.4124],
#     [50.95, 0.4279, 0.4264, 0.4234, 0.4217, 0.4243, 0.4374, 0.7524, 0.4391, 0.7402, 0.4392, 0.4371, 0.4357, 0.434,
#      0.4338, 0.4353, 0.4382, 0.7849, 0.8202, 0.8913, 0.9245, 0.9423, 0.934, 0.9251, 0.8502, 0.8792, 0.8815, 0.859,
#      0.844, 0.8931, 0.9379, 0.9305, 0.9433, 0.9277, 0.9153, 0.9236, 0.9384, 0.9134, 0.7942, 0.7818, 0.4375, 0.4296,
#      0.4266, 0.4252, 0.4244, 0.422, 0.4208, 0.4205, 0.4205],
#     [61.56, 0.436, 0.4345, 0.4315, 0.4298, 0.4324, 0.4455, 0.7605, 0.4472, 0.7483, 0.4472, 0.4452, 0.4438, 0.4421,
#      0.4419, 0.4434, 0.4463, 0.793, 0.8283, 0.8994, 0.9326, 0.9504, 0.9421, 0.9332, 0.8583, 0.8873, 0.8896, 0.8671,
#      0.8521, 0.9012, 0.946, 0.9386, 0.9514, 0.9358, 0.9234, 0.9317, 0.9465, 0.9215, 0.8023, 0.7899, 0.4456, 0.4377,
#      0.4347, 0.4333, 0.4325, 0.4301, 0.4289, 0.4286, 0.4286],
#     [75.22, 0.4441, 0.4426, 0.4396, 0.4379, 0.4405, 0.4536, 0.7686, 0.4553, 0.7564, 0.4553, 0.4533, 0.4519, 0.4502,
#      0.45, 0.4515, 0.4544, 0.8011, 0.8364, 0.9075, 0.9407, 0.9585, 0.9502, 0.9413, 0.8664, 0.8954, 0.8977, 0.8752,
#      0.8602, 0.9093, 0.9541, 0.9467, 0.9595, 0.9439, 0.9315, 0.9398, 0.9546, 0.9296, 0.8104, 0.798, 0.4537, 0.4458,
#      0.4428, 0.4414, 0.4406, 0.4382, 0.437, 0.4367, 0.4367],
#     [92.81, 0.4522, 0.4507, 0.4477, 0.446, 0.4486, 0.4617, 0.7767, 0.4634, 0.7645, 0.4634, 0.4614, 0.46, 0.4583, 0.4581,
#      0.4596, 0.4625, 0.8092, 0.8445, 0.9156, 0.9488, 0.9666, 0.9583, 0.9494, 0.8745, 0.9035, 0.9058, 0.8833, 0.8683,
#      0.9174, 0.9622, 0.9548, 0.9676, 0.952, 0.9396, 0.9479, 0.9627, 0.9377, 0.8185, 0.8061, 0.4618, 0.4539, 0.4509,
#      0.4495, 0.4487, 0.4463, 0.4451, 0.4448, 0.4448],
#     [115.46, 0.4602, 0.4588, 0.4558, 0.4541, 0.4567, 0.4698, 0.7848, 0.4715, 0.7726, 0.4715, 0.4695, 0.4681, 0.4664,
#      0.4662, 0.4677, 0.4706, 0.8173, 0.8526, 0.9237, 0.9569, 0.9747, 0.9664, 0.9574, 0.8826, 0.9116, 0.9139, 0.8914,
#      0.8764, 0.9255, 0.9703, 0.9629, 0.9757, 0.9601, 0.9477, 0.956, 0.9708, 0.9458, 0.8266, 0.8142, 0.4699, 0.462,
#      0.459, 0.4576, 0.4568, 0.4544, 0.4532, 0.4529, 0.4529],
#     [144.6, 0.4683, 0.4669, 0.4639, 0.4622, 0.4648, 0.4779, 0.7929, 0.4796, 0.7807, 0.4796, 0.4776, 0.4762, 0.4745,
#      0.4743, 0.4758, 0.4787, 0.8254, 0.8607, 0.9318, 0.965, 0.9828, 0.9745, 0.9655, 0.8907, 0.9197, 0.922, 0.8995,
#      0.8845, 0.9336, 0.9784, 0.971, 0.9838, 0.9682, 0.9558, 0.9641, 0.9789, 0.9539, 0.8347, 0.8223, 0.478, 0.4701,
#      0.4671, 0.4657, 0.4649, 0.4625, 0.4613, 0.461, 0.461],
#     [182.12, 0.4764, 0.475, 0.472, 0.4703, 0.4729, 0.486, 0.801, 0.4877, 0.7888, 0.4877, 0.4857, 0.4843, 0.4826, 0.4823,
#      0.4839, 0.4868, 0.8335, 0.8688, 0.9399, 0.9731, 0.9909, 0.9826, 0.9736, 0.8988, 0.9278, 0.9301, 0.9076, 0.8926,
#      0.9417, 0.9865, 0.9791, 0.9919, 0.9763, 0.9639, 0.9722, 0.987, 0.962, 0.8428, 0.8304, 0.4861, 0.4782, 0.4752,
#      0.4738, 0.473, 0.4706, 0.4694, 0.4691, 0.4691],
#     [230.42, 0.4845, 0.4831, 0.4801, 0.4784, 0.481, 0.4941, 0.8091, 0.4958, 0.7969, 0.4958, 0.4938, 0.4924, 0.4907,
#      0.4904, 0.492, 0.4949, 0.8416, 0.8769, 0.948, 0.9812, 0.999, 0.9907, 0.9817, 0.9069, 0.9359, 0.9382, 0.9157,
#      0.9007, 0.9498, 0.9946, 0.9872, 1, 0.9844, 0.972, 0.9803, 0.9951, 0.9701, 0.8509, 0.8385, 0.4942, 0.4863, 0.4833,
#      0.4819, 0.4811, 0.4787, 0.4775, 0.4772, 0.4772]]

len_lookup = len(lookup_base)
i_price = 0
# ------ END: DO NOT CHANGE THE ABOVE DATA ------
