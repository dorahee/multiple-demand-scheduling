:: argv 1 - no. of houses
:: argv 2 - no. of iterations
:: argv 3 - randomization or not
:: argv 4 - no. of scheduling periods in a day
:: argv 5 - create new test data or read existing data
:: argv 6 - penalty scale factor
:: argv 7 - look up scale parameter
:: Experiment 1 - test the number of iterations required to converge when the number of houses increases
::              test the impacts of unhappiness on peak and cost reduction
::              test the impacts of pricing table on peak and cost reduction
:: set houses = 200, 400, 600, 800, 1000
:: table 1: set unhappiness = 10, 30, 60, 90
:: table 2: set lookup = 1, 1.04, 1.08, 1.12
:: table 3: set periods = 48, 96, 144
:: Experiment 2 - test randomization (maybe not needed for this paper)
::              test the relation between radomization and the number of time slots, unhappiness and pricing table
:: set rand = 0, 1
:: table 1: set unhappiness = 10, 30, 60, 90
:: table 2: set lookup = 1, 1.04, 1.08, 1.12
:: table 3: set periods = 48, 96, 144
:: Experiment - test the randomization on peak reduction and cost redudction
:: set rand = 0, 1
set no_houses=500
for /l %%x in (1, 1, 20) do python run.py %no_houses%
:: set no_houses=1000
:: for /l %%x in (1, 1, 5) do python run.py %no_houses%
:: set no_houses=1500
:: for /l %%x in (1, 1, 20) do python run.py %no_houses%
set no_houses=2000
for /l %%x in (1, 1, 10) do python run.py %no_houses%
:: set no_houses=2500
:: for /l %%x in (1, 1, 20) do python run.py %no_houses%
:: set no_houses=3000
:: for /l %%x in (1, 1, 20) do python run.py %no_houses%
set no_houses=5000
for /l %%x in (1, 1, 5) do python run.py %no_houses%
:: set no_houses=7000
:: for /l %%x in (1, 1, 20) do python run.py %no_houses%
:: set no_houses=9000
:: for /l %%x in (1, 1, 20) do python run.py %no_houses%
set no_houses=10000
for /l %%x in (1, 1, 5) do python run.py %no_houses%
:: set no_houses=13000
:: for /l %%x in (1, 1, 20) do python run.py %no_houses%
set no_houses=15000
for /l %%x in (1, 1, 20) do python run.py %no_houses%
:: set no_houses=17000
:: for /l %%x in (1, 1, 20) do python run.py %no_houses%
:: set no_houses=19000
:: for /l %%x in (1, 1, 5) do python run.py %no_houses%
set no_houses=21000
for /l %%x in (1, 1, 20) do python run.py %no_houses%





