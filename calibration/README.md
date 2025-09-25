# Calibration Scripts

## Overview

This directory includes the implementation of the simulator calibrator:

+ `Simulator.py` : A class that knows how to run the simulator
+ `Util.py` : Various utilities and abstractions (such as different loss function definitions, `Experiment` and `ExperimentSet` to define batches of experiments, `WorkflowSetSpec` for describing specific subsets of the ground-truth data)
+ `WorkflowSimulatorCalibrator.py` : The code of the simulator calibrator itself, which defines . 

This directory also includes scripts needed to run the calibration experiments for Case Study #1 in the paper:

+ `calibration_from_pickle.py` : A command-line utility that takes an output pickle created by one of the calibration scripts and extracts the calibration as a json file
+ `generate_synthetic_data.py` : A command-line utility to generate the synthetic data file from the ground-truth data file and a best-guess calibration
+ `Loss.py` : The Loss function definitions
+ `pickle_format.txt` : A description of the structure of an output pickle
+ `pickle_to_json.py` : A command-line utility that takes an output pickle created by one of the calibration scripts and converts it to a json object for easier exploration.  
+ `run_single_calibration.py` : A command-line utility to calibrate the simulator using a single set of experiments.  Generates an output pickle file of the experiments and calibration.
+ `run_single_evaluation.py` :  A command-line utility that takes an output pickle and evaluates it on a new set of ground-truth data
+ `run_single_parameter_evaluation.py` : A command-line utility that takes a calibration as a json string and evaluates it on a set of ground-truth data
+ `run_single_workflow_experiments.py` : A command-line utility that runs multiple calibration on different experiment sets

In all that follows, each script is detailed.



## `calibration_from_pickle.py` 
A command-line utility that takes an output pickle created by one of the calibration scripts and extracts the calibration as a json file.

```bash
./calibration_from_pickle.py [-H] <pickle_file> [path_to_json] 
```
	
  - `pickle_file` is the path to the output pickle file to extract calibration from 
  - `path_to_json` is the path to save the resulting json object to.  If empty (default), the json object is instead output on std_out
  - `-H` converts all numeric types in the calibration to human readable number with suffix (e.g. 10000000000Bps to 10GBps)

## `generate_synthetic_data.py`

A command-line utility to generate the synthetic data file from the ground-truth data file and a best-guess calibration 

```bash
./generate_synthetic_data.py 
	-a <best_guess_parameters> 
	-o <output_path> 
	-cs <compute_service_scheme> 
	-ss <storage_service_scheme> 
	-ns <network_topology_scheme>		
```
	
  - `best_guess_parameters` The parameters you wish to generate synthetic data for as well as other control paramters for the simulator.
  - `output_path` The file path to save the synthetic data file to
  - `storage_service_scheme` The storage service arg to pass to the simulator from the options `[submit_only|submit_and_compute_hosts]`. The best guess parameters must contain the correct args for the scheme
  - `compute_service_scheme` The compute service arg to pass to the simulator from the options `[all_bare_metal|htcondor_bare_metal]`.  The best guess parameters must contain the correct args for the scheme
  - `network_topology_scheme` The network topology arg to pass to the simulator from the options `[one_link|one_and_then_many_links|many_links]`.  The best guess parameters must contain the correct args for the scheme
	
	### Command to Generate Synthetic Data used in the Case Study: 
```bash
for file in $(ls ../../GROUND_TRUTH/*) ; do 
	file=$(basename $file) ; echo $file; ./generate_synthetic_data.py \
	-a '{"workflow":{"file":"'../../GROUND_TRUTH/$file'","reference_flops":"100Mf"},"error_computation_scheme":"makespan","error_computation_scheme_parameters":{"makespan":{}},"scheduling_overhead":"10ms","compute_service_scheme":"htcondor_bare_metal","compute_service_scheme_parameters":{"all_bare_metal":{"submit_host":{"num_cores":"16","speed":"12345Gf"},"compute_hosts":{"num_cores":"16","speed":"1f"},"properties":{"BareMetalComputeServiceProperty::THREAD_STARTUP_OVERHEAD":"42s"},"payloads":{}},"htcondor_bare_metal":{"submit_host":{"num_cores":"1231","speed":"123Gf"},"compute_hosts":{"num_cores":"16","speed":"982452266.749154f"},"bare_metal_properties":{"BareMetalComputeServiceProperty::THREAD_STARTUP_OVERHEAD":"3.045662s"},"bare_metal_payloads":{},"htcondor_properties":{"HTCondorComputeServiceProperty::NEGOTIATOR_OVERHEAD":"12.338810s","HTCondorComputeServiceProperty::GRID_PRE_EXECUTION_DELAY":"14.790155s","HTCondorComputeServiceProperty::GRID_POST_EXECUTION_DELAY":"14.079311s"},"htcondor_payloads":{}}},"storage_service_scheme":"submit_and_compute_hosts","storage_service_scheme_parameters":{"submit_only":{"bandwidth_submit_disk_read":"10000MBps","bandwidth_submit_disk_write":"10000MBps","submit_properties":{"StorageServiceProperty::BUFFER_SIZE":"42MB","SimpleStorageServiceProperty::MAX_NUM_CONCURRENT_DATA_CONNECTIONS":"8"},"submit_payloads":{}},"submit_and_compute_hosts":{"bandwidth_submit_disk_read":"428823427550.539185bps","bandwidth_submit_disk_write":"4398215356.339356bps","submit_properties":{"StorageServiceProperty::BUFFER_SIZE":"42000000","SimpleStorageServiceProperty::MAX_NUM_CONCURRENT_DATA_CONNECTIONS":"59"},"submit_payloads":{},"bandwidth_compute_host_disk_read":"28687530839.627506bps","bandwidth_compute_host_write":"24561408103.754391bps","compute_host_properties":{"StorageServiceProperty::BUFFER_SIZE":"1048576B","SimpleStorageServiceProperty::MAX_NUM_CONCURRENT_DATA_CONNECTIONS":"28"},"compute_host_payloads":{}}},"network_topology_scheme":"one_and_then_many_links","network_topology_scheme_parameters":{"one_link":{"bandwidth":"4MBps","latency":"10us"},"many_links":{"bandwidth_submit_to_compute_host":"4000MBps","latency_submit_to_compute_host":"10us"},"one_and_then_many_links":{"bandwidth_out_of_submit":"16226331284.128448bps","latency_out_of_submit":"0.009044s","bandwidth_to_compute_hosts":"11195981534.552021bps","latency_to_compute_hosts":"10us","latency_submit_to_compute_host":"0.008494s"}}}' \
	-o ../../SYNTHETIC_DATA/$file \
	-cs htcondor_bare_metal \
	-ss submit_and_compute_hosts \
	-ns one_and_then_many_links ; 
	echo done $file ;
done
```

## `pickle_to_json.py` 

A command-line utility that takes an output pickle created by one of the calibration scripts and converts it to a json object for easier exploration.  

```bash
./pickle_to_json.py <pickle_file> [path_to_json] 
```
	
  - `pickle_file` The path to convert to json
  - `path_to_json` The path to save the resulting json object to.  If empty (default), the json object is instead output on std_out
	
## `run_single_calibration.py`

A command-line utility to calibrate the simulator using a single set of experiments.  Generates an output pickle file of the experiments and calibration.
```bash 
./run_single_calibration.py 
	-wd <workflow_dir> 
	-cn <computer_name> 
	-al <algorithm>
	-tl <time_limit>
	-th <num_threads>
	-lf <loss_function>
	-la <loss_aggregator>
	-cs <compute_service_scheme> 
	-ss <storage_service_scheme> 
	-ns <network_topology_scheme>	
	-ts <training_set>
	[-es] <evaluation_set>
```
This script will create an output file named`pickled-one_calibration-{hash(training_set,8 bytes)}-{hash(training_set,8 bytes)}-[compute_service_scheme]-[storage_service_scheme]-[network_topology_scheme]-[algorithm]-[loss_function]-[loss_aggregator]-[time_limit]-[num_threads]-[computer_name].pickled`
	
If the file already exists, the calibration is skipped
	
  - `workflow_dir` The directory the ground-truth is in. Unused, but left for consistency with other scripts.
  - `computer_name` A data versioning parameter: as compute systems run at different speeds, they can produce different calibrations by running for different times.  This parameter should be set to a unique name for each system running calibrations to prevent confusing the results.  Exclusively used in output file naming
  - `algorithm` The algorithm to use for calibration.  Must be in the list `[grid|random|gradient|skopt.gp|skopt.gbrt|skopt.rf|skopt.et]`
  - `time_limit` how long to run the calibration process for
  - `num_threads` how many threads to use for calibration
  - `loss_function` which loss function to use. Must be in the list `[makespan|average_runtimes|max_runtimes]`
  - `loss_aggregator` which loss aggregator to use. Must be in the list `[average_error|max_error]`
  - `storage_service_scheme` The storage service arg to pass to the simulator from the options `[submit_only|submit_and_compute_hosts]`.
  - `compute_service_scheme` The compute service arg to pass to the simulator from the options `[all_bare_metal|htcondor_bare_metal]`.  
  - `network_topology_scheme` The network topology arg to pass to the simulator from the options `[one_link|one_and_then_many_links|many_links]`. 	
  - `training_set` The list of json files to use for training
  - `evaluation_set` The list of json files to use for evaluation.  If excluded, the training set is used for evaluation as well.

	Example:
```bash
./run_single_calibration.py \
	-wd ../../GROUND_TRUTH/ \
	-cn KOA \
	-al skopt.gbrt \
	-la average_error \
	-lf max_runtimes \
	-tl 86400 \
	-th 48 \ 
	-cs htcondor_bare_metal \
	-ss submit_and_compute_hosts \
	-ns one_and_then_many_links \
	-ts ../GROUND_TRUTH/*.json
```
Output file name: `pickled-one_calibration-gV3DnU0I-gV3DnU0I-htcondor_bare_metal-submit_and_compute_hosts-one_and_then_many_links-skopt.gbrt-max_runtimes-average_error-86400-48-KOA.pickled`

# `run_single_evaluation.py`

A command-line utility that takes a set of simulation parameters and evaluates it on a set of ground-truth data

```bash 
./run_single_parameter_evaluation.py 
	-p <input_pickle> 
	-th <num_threads>
	-lf <loss_function>
	-la <loss_aggregator>
	-es <evaluation_set>
```
The script will create an output file named`[input_pickle]-Reevaluation-{hash(training_set,8 bytes)}-{hash(sim_args,8 bytes)}-[loss_function]-[loss_aggregator].pickled`
	
If the file already exists, the reevaluation is skipped
	
  - `simulation_parameters` A JSON string representing the calibrated simulation parameters.  The output of pickle_to_json.py can be used for this.
  - `num_threads` how many threads to use for evaluation
  - `loss_function` which loss function to use. Must be in the list `[makespan|average_runtimes|max_runtimes]`
  - `loss_aggregator` which loss aggregator to use. Must be in the list `[average_error|max_error]`
  - `evaluation_set` The list of json files to use for evaluation. 


# `run_single_parameter_evaluation.py`

A command-line utility that takes a set of simulation parameters and evaluates it on a set of ground-truth data

```bash 
./run_single_parameter_evaluation.py 
	-a <simulation_parameters> 
	-th <num_threads>
	-lf <loss_function>
	-la <loss_aggregator>
	-cs <compute_service_scheme> 
	-ss <storage_service_scheme> 
	-ns <network_topology_scheme>	
	-es <evaluation_set>
```
The script will create an output file named`Evaluation-{hash(training_set,8 bytes)}-{hash(sim_args,8 bytes)}-[loss_function]-[loss_aggregator].pickled`
	
If the file already exists, the evaluation is skipped
	
  - `simulation_parameters` A JSON string representing the calibrated simulation parameters.  The output of pickle_to_json.py can be used for this.
  - `num_threads` how many threads to use for evaluation
  - `loss_function` the loss function to use. Must be in the list `[makespan|average_runtimes|max_runtimes]`
  - `loss_aggregator` the loss aggregator to use. Must be in the list `[average_error|max_error]`
  - `storage_service_scheme` The storage service arg to pass to the simulator from the options `[submit_only|submit_and_compute_hosts]`. 
  - `compute_service_scheme` The compute service arg to pass to the simulator from the options `[all_bare_metal|htcondor_bare_metal]`. 
  - `network_topology_scheme` The network topology arg to pass to the simulator from the options `[one_link|one_and_then_many_links|many_links]`.  
  - `evaluation_set` The list of json files to use for evaluation. 

# `run_single_workflow_experiments.py`

A command-line utility that runs multiple calibration on different experiment sets

```bash 
./run_single_calibration.py 
	-wd <workflow_dir> 
	-cn <computer_name>  	
	-wn <workflow_name>
	-ar <architecture>
	-al <algorithm>
	-tl <time_limit>
	-th <num_threads>
	-lf <loss_function>
	-la <loss_aggregator>
	-cs <compute_service_scheme> 
	-ss <storage_service_scheme> 
	-ns <network_topology_scheme>	
```
The script will create an output file named`pickled-one_workflow_experiments-workflow_name-architecture-[compute_service_scheme]-[storage_service_scheme]-[network_topology_scheme]-[algorithm]-[loss_function]-[loss_aggregator]-[time_limit]-[num_threads]-[computer_name].pickled`
	
If the file already exists, the calibration is skipped
	
  - `workflow_dir` The directory the ground-truth is in
  - `computer_name` A data versioning parameter: as compute systems run at different speeds, they can produce different calibrations by running for different times.  This parameter should be set to a unique name for each system running calibrations to prevent confusing the results.  Exclusively used in output file naming
  - `workflow_name` A ground-truth data filtering parameter:  Filters files in `workflow_dir` based on `workflow_name`
  - `architecture` A ground-truth data filtering parameter:  Filters files in `workflow_dir` based on `architecture`
  - `algorithm` The algorithm to use for calibration.  Must be in the list `[grid|random|gradient|skopt.gp|skopt.gbrt|skopt.rf|skopt.et]`
  - `time_limit` how long to run the calibration process for
  - `num_threads` how many threads to use for calibration
  - `loss_function` which loss function to use. Must be in the list `[makespan|average_runtimes|max_runtimes]`
  - `loss_aggregator` which loss aggregator to use. Must be in the list `[average_error|max_error]`
  - `storage_service_scheme` The storage service arg to pass to the simulator from the options `[submit_only|submit_and_compute_hosts]`. 
  - `compute_service_scheme` The compute service arg to pass to the simulator from the options `[all_bare_metal|htcondor_bare_metal]`.  
  - `network_topology_scheme` The network topology arg to pass to the simulator from the options `[one_link|one_and_then_many_links|many_links]`. 
	
## Ground-Truth Naming Scheme

The script expects a flattened directory with each file named in this format: ` [workflow_name]-[#tasks]-[CPU_work]-[legacy_placeholder]-[amount_of_data]-[architecture]-[#nodes]-[trial_incrimenter]-[timestamp].json`
Example: `epigenomics-129-1000-1.0-1500000000-icelake-2-4-1726336286.json`

  - `workflow_name` the name of the workflow 
  - `#tasks` the number of tasks in the workflow
  - `CPU_work` the amount of CPU work done by each task
  - `legacy_placeholder` a legacy placeholder value.  generally set to `1.0` .
  - `amount_of_data` the amount of data created by each task
  - `architecture` the chameleon cloud CPU architecture of the nodes this ground-truth data was collected on
  - `#nodes` the number of nodes used to run the workflow
  - `trial_incrimenter` to control for random elements in the real world platform, each trial was ran 10 times, each time incrementing this field.
  - `timestamp` the UNIX timestamp of when the file was created, ensures unique file names.

These values are exclusively used by the scripts for filtering.  The simulator does not care about the file name.
