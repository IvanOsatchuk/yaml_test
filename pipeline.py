import executor
import subprocess
import shlex

def func_labs_migration_pipeline(env):
  
  output = subprocess.run("gcloud projects describe rapid-strength-333817", capture_output=True)
  
  print(output)
  
  print(env)
