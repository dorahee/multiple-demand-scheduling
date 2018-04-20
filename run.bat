
@echo off

for /L %%i in (2000,2000,10000) do (
    for /L %%x in (1,1,5) do (
        echo %%i %%x
        python run.py %%i True Create
        python run.py %%i False Read    
    )
)






