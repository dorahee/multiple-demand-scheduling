
@echo off

for /l %%i in (1,1,4) do start cmd /k "for /l %%h in (2000,2000,10000) do (python run.py -no_houses %%h -use_solver False -c -jobs_file jobs%%i.csv && python run.py -no_houses %%h -use_solver True -r -jobs_file jobs%%i.csv)"


