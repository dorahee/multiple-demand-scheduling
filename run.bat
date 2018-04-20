
@echo off

for /l %%i in (1,1,4) do start cmd /k "for /l %%h in (2000,2000,10000) do (python run.py %%h False create && python run.py %%h True read)"


