#Calibration

##Overview

The calibration scripts include all the scripts need to run the calibration experiments found in the paper.

+ `calibration_from_pickle.py` : A command line utility function that takes an output pickle created by one of the calibration scripts and extracts the calibration as a json file
+ `generate_synthetic_data.py` : A command line utility to generate the synthetic data set from the ground-truth data and a best-guess calibration
+ `gradient_descent_hyperparameters.py` : A command line utility to explore various epsilon and delta parameters for gradient descent
+ `Loss.py` : The Loss function definitions
+ `pickle_format.txt` : A description of the structure of an output pickle
+ `pickle_to_json.py` : A command line utility function that takes an output pickle created by one of the calibration scripts and converts it to a json object for easier exploration.  This json can be used as an argument to the simulator directly
+ `run_single_calibration.py` : A command line utility to calibrate the simulator using a single set of experiments.  Generates an output pickle file of the experiments and calibration.
+ `run_single_evaluation.py` :  A command line utility that takes an output pickle and evaluates it on a new set of ground-truth data
+ `run_single_parameter_evaluation.py` : A command line utility that takes a calibration as a json string and evaluates it on a set of ground-truth data
+ `run_single_workflow_experiments.py` : A command line utility that runs multiple calibration on different experiment sets
+ `Simulator.py` : The code to run the simulator in any configuration
+ `Util.py` : various utilities, as well as Experiment and ExperimentSet for batches of Experiments and WorkflowSetSpec for managing ground-truth data subsets
+ `WorkflowSimulatorCalibrator.py` : The code to handle arguments to make various calibration configurations
