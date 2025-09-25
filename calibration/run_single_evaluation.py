#!/usr/bin/env python3
import argparse
import time
from glob import glob
from datetime import timedelta
from Util import *
from itertools import groupby
def group(flat):
	# Use a regular expression to split the string before the last part (repeat number)
	def split_key(s):
		return '-'.join(s.split('-')[0:7])

	# Sort the strings based on the non-repeat part
	sorted_strings = sorted(flat, key=split_key)
	
	# Group by the non-repeat part
	grouped_strings = [list(group) for _, group in groupby(sorted_strings, key=split_key)]
	
	return grouped_strings
def parse_command_line_arguments(program_name: str):
	epilog_string = ""

	parser = argparse.ArgumentParser(
		prog=program_name,
		description='Workflow simulator calibrator',
		epilog=epilog_string)

	try:

		parser.add_argument('-p', '--pickle', type=str, metavar="<pickle>", required=True,
							help='Pickled calibration to use')
		
		parser.add_argument('-th', '--num_threads', type=int, metavar="<number of threads (default=1)>", nargs='?',
							default=1, help='A number of threads to use for training')
		parser.add_argument('-lf', '--loss_function', type=str,
							metavar="makespan, average_runtimes, max_runtimes",
							choices=['makespan', 'average_runtimes','max_runtimes'], nargs='?',
							default="makespan",
							help='The loss function to evaluate a calibration')
		parser.add_argument('-la', '--loss_aggregator', type=str,
							metavar="average_error, max_error",
							choices=['average_error', 'max_error'], nargs='?',
							default="average_error",
							help='The loss aggregator to evaluate a calibration')					
		parser.add_argument('-es', '--evaluation_set', type=str, nargs="*",default=None, 
							help='The list of json files to use for evaluation')
		return vars(parser.parse_args()), parser, None

	except argparse.ArgumentError as error:
		return None, parser, error



def main(args):
	
	evaluation=group(args['evaluation_set'])
	pickle_file_name = f"{args['pickle']}-Reevaluation-" \
					   f"{orderinvarient_hash(evaluation,8)}-" \
					   f"{args['loss_function']}-" \
					   f"{args['loss_aggregator']}.pickled"

	# If the pickled file already exists, then print a warning and move on
	if os.path.isfile(pickle_file_name):
		sys.stderr.write(f"There is already a pickled file '{pickle_file_name}'... Not doing anything!\n")
		sys.exit(1)

	sys.stderr.write(f"repacking expiriments for {pickle_file_name}\n")

	with open(args['pickle'], 'rb') as f:
		experiment_set = pickle.load(f)
	#experiment_set.algorithm = args["algorithm"]
	experiment_set.loss_function = args["loss_function"]
	experiment_set.loss_aggregator = args["loss_aggregator"]
	experiment_set.num_threads = args["num_threads"]
	#experiment_set.experiments = []
	if(len(experiment_set.experiments)!=1):
		sys.stderr.write("Currently only supports pickles with exactly 1 expiriemnt]n");
	experiment_set.experiments[0].evaluation_set_specs=[WorkflowSetSpec().set_workflows(evaluation)	]
		
	sys.stderr.write(f"\nCreated {len(experiment_set)} experiments...\n")
	start = time.perf_counter()
	pickle_path=sys.argv[1]
	experiment_set.compute_all_evaluations()
	elapsed = int(time.perf_counter() - start)
	sys.stderr.write(f"Actually ran in {timedelta(seconds=elapsed)}\n")
	
	# Pickle it
	with open(pickle_file_name, 'wb') as f:
		pickle.dump(experiment_set, f)
	#sys.stderr.write(f"Pickled to ./{pickle_file_name}\n")
	print(pickle_file_name)
	return pickle_file_name
if __name__ == "__main__":
	args, parser, error = parse_command_line_arguments(sys.argv[0])
	# Parse command-line arguments
	if not args:
		sys.stderr.write(f"Error: {error}\n")
		parser.print_usage()
		sys.exit(1)
	main(args)
