from scripts import analyseJobs as AJ
from scripts import analyseResults as AR

# -------- parameters--------
date = "18-04-19"
# assumptions: all results have 144 scheduling periods, otherwise this program doesn't work
columns = [{'key': 'dur',         'value': [1 * 6, 6 * 6, 12 * 6, 24 * 6]},  # in hours
           {'key': 'consumption', 'value': [0.01, 0.05, 0.1, 0.5, 1, 2, 3, 999999]},
           {'key': 'caf',         'value': [0.1, 0.3, 0.6, 0.9, 1]},
           {'key': 'pstart',      'value': [8 * 6 - 1, 16 * 6 - 1, 24 * 6 -1]}]
# -------- END: parameters --------

# AJ.main(date)
AR.main(date)

print str(date) + '. All done!'
