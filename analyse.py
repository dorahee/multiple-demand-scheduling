from scripts import analysis_task as AJ
from scripts import analysis_results as AR
from sys import argv

# -------- parameters--------
date = "20-09-16"
# assumptions: all results have 144 scheduling periods, otherwise this program doesn't work

if "-d" in argv:
    date = argv[argv.index("-d") + 1]

columns = [{'key': 'dur',         'value': [1 * 6, 6 * 6, 12 * 6, 24 * 6]},  # in hours
           {'key': 'consumption', 'value': [0.01, 0.05, 0.1, 0.5, 1, 2, 3, 999999]},
           {'key': 'caf',         'value': [0.1, 0.3, 0.6, 0.9, 1]},
           {'key': 'pstart',      'value': [8 * 6 - 1, 16 * 6 - 1, 24 * 6 -1]}]
# -------- END: parameters --------

# AJ.main(date)
AR.main(date)

print(str(date) + '. All done!')
