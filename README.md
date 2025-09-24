## About

This repository contains the software used for Case Study #1 in [https://doi.org/10.1145/3731599.3767698](https://doi.org/10.1145/3731599.3767698), with the objective of making the experiments and results in that case study reproducible.

The software is comprised of two parts:

  - 1. The simulator in the `simulator/` directory; and
  - 2. The simulator calibration scripts in the `calibration/` directory.

The `install.sh` script in the root directory will build and install all needed software, including:
[SimGrid 4.0](https://framagit.org/simgrid/simgrid/),
[WRENCH 2.6](https://github.com/wrench-project/wrench), the simulator in `simulator/`, and
the simulation calibration framework
[Simcal](https://github.com/wrench-project/simcal) (commit tag `86445d59177922fa3711473bbf4e5e207005fcc2`).  It is assumed that
`sudo`, `cmake`, `make`, `gcc`, `git`, Boost 1.81 or above, and Python 3.12 (and corresponding
pip) are already installed.

The experiments in the case study are conducted with the ground-truth data available [there](https://doi.org/10.6084/m9.figshare.30132955).

---

## Workflow execution simulator

The simulator is invoked by the calibration scripts in (see the `README` file in the `calibration/` directory). But
the simulator can also be invoked stand-alone. 
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

---

## Simulator calibration scripts

All scripts are in the `calibration/` directory. See the `README` file therein.

---

