import executor
import subprocess
import shlex

def func_labs_migration_pipeline(env):
  
  output = subprocess.run(shlex.split(command), capture_output=True)
  
  print(output)
  
  print(env)
