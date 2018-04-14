Version15 is an updated version of Version14.
This improved performance dramatically by
1. replacing deepcopy with shallow copy
2. fixing a mistake in job scheduling
3. not using an array to store alphas of all periods
4. moving all the output string preparation to writeResults.prepare function
5. moving the first pricing function just under the while loop (it is duplicated. )

30s can be reduced for optimizing 5000H + 5000B

