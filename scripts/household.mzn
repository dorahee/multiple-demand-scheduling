include "globals.mzn";

% parameters
int: no_intervals;
set of int: INTERVALS = 1 .. no_intervals; 

int:no_devices;
set of int: DEVICES = 1..no_devices;
array[DEVICES] of int: durations;
array[DEVICES] of int: demands;

array [DEVICES, INTERVALS] of float: run_costs;

int: num_precedences;
set of int: PREC = 1..num_precedences;
array[PREC] of DEVICES: predecessors;
array[PREC] of DEVICES: successors;
array[PREC] of int: prec_delays;
int: max_demand;

% variables
array[DEVICES] of var INTERVALS: actual_starts;

% constraint forall (d in DEVICES) (earliest_starts[d] <= actual_starts[d] /\ actual_starts[d] + durations[d] - 1 <= latest_ends[d]);

% predecessor constraint
constraint forall (p in PREC) (
    let { DEVICES: pre = predecessors[p] ;
           DEVICES: succ = successors[p] ;
           int: d = prec_delays[p]; } in
     actual_starts[pre] + durations[pre] <= actual_starts[succ] /\ actual_starts[succ] <= actual_starts[pre] + durations[pre] + d
   ); 

% resource capacity constraint   
constraint cumulative(actual_starts, durations, demands, max_demand);

solve minimize sum (d in DEVICES) (run_costs[d, actual_starts[d]]);

% output ["{AastartsA:["] ++ [if d < no_devices then show(actual_starts[d] - 1) ++ ","  else show(actual_starts[d] - 1) endif | d in DEVICES] ++ ["]"] ++ [",AobjA: " ++ show(sum (d in DEVICES) (run_costs[d, actual_starts[d]])) ++ "}"];

% output [show(actual_starts)];