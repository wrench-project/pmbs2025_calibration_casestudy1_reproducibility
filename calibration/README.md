# Calibration

## Overview

The calibration scripts include all the scripts need to run the calibration experiments found in the paper.

+ `calibration_from_pickle.py` : A command line utility function that takes an output pickle created by one of the calibration scripts and extracts the calibration as a json file
+ `generate_synthetic_data.py` : A command line utility to generate the synthetic data file from the ground-truth data file and a best-guess calibration
+ `Loss.py` : The Loss function definitions
+ `pickle_format.txt` : A description of the structure of an output pickle
+ `pickle_to_json.py` : A command line utility function that takes an output pickle created by one of the calibration scripts and converts it to a json object for easier exploration.  
+ `run_single_calibration.py` : A command line utility to calibrate the simulator using a single set of experiments.  Generates an output pickle file of the experiments and calibration.
+ `run_single_evaluation.py` :  A command line utility that takes an output pickle and evaluates it on a new set of ground-truth data
+ `run_single_parameter_evaluation.py` : A command line utility that takes a calibration as a json string and evaluates it on a set of ground-truth data
+ `run_single_workflow_experiments.py` : A command line utility that runs multiple calibration on different experiment sets
+ `Simulator.py` : The code to run the simulator in any configuration
+ `Util.py` : various utilities, as well as Experiment and ExperimentSet for batches of Experiments and WorkflowSetSpec for managing ground-truth data subsets
+ `WorkflowSimulatorCalibrator.py` : The code to handle arguments to make various calibration configurations


# `calibration_from_pickle.py` 
A command line utility function that takes an output pickle created by one of the calibration scripts and extracts the calibration as a json file.
```bash
./calibration_from_pickle.py [-H] <pickle_file> [path_to_json] 
```
	
	`pickle_file` is the path to the output pickle file to extract calibration from 
	
	`path_to_json` is the path to save the resulting json object to.  If empty (default), the json object is instead output on std_out
	
	`-H` converts all numeric types in the calibration to human readable number with suffix (e.g. 10000000000Bps to 10GBps)
# `generate_synthetic_data.py`
A command line utility to generate the synthetic data file from the ground-truth data file and a best-guess calibration 

```bash
./generate_synthetic_data.py 
	-a <best_guess_parameters> 
	-o <output_path> 
	-cs <compute_service_scheme> 
	-ss <storage_service_scheme> 
	-ns <network_topology_scheme>		
```
	
	`best_guess_parameters` The parameters you wish to generate synthetic data for as well as other control paramters for the simulator.
	
	`output_path` The file path to save the synthetic data file to
	
	`storage_service_scheme` The storage service arg to pass to the simulator from the options `[submit_only|submit_and_compute_hosts]`. The best guess parameters must contain the correct args for the scheme
	
	`compute_service_scheme` The compute service arg to pass to the simulator from the options `[all_bare_metal|htcondor_bare_metal]`.  The best guess parameters must contain the correct args for the scheme
	
	`network_topology_scheme` The network topology arg to pass to the simulator from the options `[one_link|one_and_then_many_links|many_links]`.  The best guess parameters must contain the correct args for the scheme
	
	## Command to Generate Synthetic Data Used: 
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
# `pickle_to_json.py` 
A command line utility function that takes an output pickle created by one of the calibration scripts and converts it to a json object for easier exploration.  
```bash
./pickle_to_json.py <pickle_file> [path_to_json] 
```
	
	`pickle_file` is the path to convert to json
	
	`path_to_json` is the path to save the resulting json object to.  If empty (default), the json object is instead output on std_out
# `run_single_calibration.py` 

# `run_single_evaluation.py` 

# `run_single_parameter_evaluation.py` 

# `run_single_workflow_experiments.py` 
