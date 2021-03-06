
import sys
import pickle

import cloud
cloud.setkey(7513, api_secretkey='ca43a3535fa17e28b687f0f1691c67db261392ae')
cloud_environment = 'Julia'

"""
number_of_clusters = int(sys.argv[1])
if_zero_shortlearning = sys.argv[2] # Should be "yes" or "no"
experiment_name = sys.argv[3]"""

# Usage: python picloud_runner.py 200 10 20


TRIALS = int(sys.argv[1])
NUM_PARTICLES = int(sys.argv[2])
REPETITIONS = int(sys.argv[3])
DATASET = int(sys.argv[4])


def run_on_instance(trial_id):
  global number_of_clusters
  global if_zero_shortlearning
  global experiment_name
  import subprocess
  import os
  os.environ['DISPLAY'] = ":1"
  print "Starting"
  ls_output = subprocess.Popen(["/home/picloud/julia/julia", "putative_runner.jl", str(NUM_PARTICLES), str(trial_id), str(REPETITIONS), str(DATASET)], \
                               cwd = "/home/picloud/DPMixtureModel/DPMM_MaxFilter/",  \
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  out, err = ls_output.communicate()
  return out
 
#result = run_on_instance([1])  

jids = cloud.map(run_on_instance, range(TRIALS), _env=cloud_environment, _type='c2', _cores=1)
print jids
result = cloud.result(jids)
pickle.dump(result, open("DATASET="+str(DATASET)+"_putative_result_"+str(NUM_PARTICLES)+"particles_"+str(REPETITIONS)+"path.pkl","wb"))
print "RESULT:", result
