# Concurrency Simulator
This project simulates an OS-style concurrent task scheduler that assigns tasks to worker threads that simulate CPU cores. The *simple-pilot* branch holds my first iteration of a scheduler, trial and erroring a simple concept to help me develop a foundation to build a more sophisticated model. The main branch holds my most recent additions and iterations of this concurrency model.

## Main concurrency simulator (current as of December 14 2025)
Added a priority policy to the simulation. Add the string *"priority"* to the policy input in main to use priority policy, otherwise the model defaults to round robin. Currently, every other function is identical to the pilot.

## Pilot concurrency simulator
This project simulates a minimal round-robin scheduler. The central scheduler iteratively assigns tasks that have remaining work to worker threads with fixed-size time slices. These worker threads independently execute the assigned work, mark it as done and report back to the scheduler. This simulates a concurrent scheduling loop with low complexity, and demonstrates task selection, time slicing, execution and state updates.
