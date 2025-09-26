---
## Workflow Execution Simulator


The simulator takes as input a single JSON file. An example input file
is in `simulator/data/sample_input.json`. An invocation of the simulator, once installed, using that input
file would be as:
```bash
workflow-simulator-for-calibration simulator/data/sample_input.json
```
which will print three numbers of standard output formatted as `A:B:C`,
where `A` is the simulated makespan computed by the simulator (in seconds),
`B` is the actual makespan of the workflow, observed on a real platform
(based on the [WfCommons](https://wfcommons.org/) workflow file `data/sample_workflow.json`), and `C` is the relative error between
`A` and `B` computed as $C=\frac{\left| A - B \right|}{B}$.

The simulator can also take the json directly from the command line by replacing the file path with a valid json object:
```bash
workflow-simulator-for-calibration `cat simulator/data/sample_input.json`
``` 


