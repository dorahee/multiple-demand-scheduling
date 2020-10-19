@echo off
SET COPYCMD=/Y
::FOR /R "rerun" %%G in (*.*) do (
::if %%~nG==jobs (xcopy "%%G" "."
::echo 'copied')
::)
FOR /d %%G in (rerun\*.*) do (
xcopy ".\%%G\jobs.csv" "."
xcopy ".\%%G\batteries.csv" "."
python run.py
)

::echo %%~nG
::IF fname=="prices" echo yeah
::xcopy "%%G" "community.json"
::python run.py




