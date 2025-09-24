## About
This git repository is the simulator and calibrator used for case study 1 of doi:10.1145/3731599.3767698 and is capable of reproducing the experiments done in that case study.

It is broken into 2 parts, the simulator its self, and the calibration scripts used to calibrate.  There is a separate README file the calibration directory.

The install.sh script will build and install SimGrid, Wrench, and the simulator, and install Simcal.  
It requires sudo, CMake, make, GCC, git, and Python 3.12 (and corresponding pip)

To reproduce the experiments, you will need the ground-truth data available at https://github.com/wrench-project/pmbs2025_calibration_casestudy1_reproducibility


## Workflow execution simulator used for simulation calibration experiments

Code tested with:
 - SimGrid 4.0: `https://github.com/simgrid/simgrid/releases/download/v4.0/simgrid-4.0.tar.gz`
 - WRENCH 2.6: `https://github.com/wrench-project/wrench/archive/refs/tags/v2.6.tar.gz`
 - Wfcommons master commit ID: `29c69989fe5701bc07eb66c0077531f60e8a4414`
 - Boost: `1.81.0`
 - Python: `3.12.3`
 - simcal master commit ID: `86445d59177922fa3711473bbf4e5e207005fcc2` 
---


## How to invoke the simulator stand-alone

The simulator takes as input a single JSON file. An example input file
is in `simulator/data/sample_input.json`. An invocation of the simulator could be:
```bash
./workflow-simulator-for-calibration data/sample_input.json
```
which will print three numbers of standard output formatted as `A:B:C`,
where `A` is the simulated makespan computed by the simulator (in seconds),
`B` is the actual makespan of the workflow, observed on a real platform
(see `data/sample_workflow.json`), and `C` is the relative error between
`A` and `B` computed as $C=\frac{\left| A - B \right|}{B}$.

The simulator can also take the json directly from the terminal by replacing the file path with a valid json object like
```bash
./workflow-simulator-for-calibration `cat data/sample_input.json`
```