import executor
import subprocess
import shlex

def func_labs_migration_pipeline(env):
  
  instance_output = subprocess.run(
        "gcloud projects describe rapid-strength-333817",
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        shell=True,
    )
  
  print(instance_output)
  
  print(env)
