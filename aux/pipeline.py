import executor

def func_labs_migration_pipeline(env):
  
  instance_output = subprocess.run(
        shlex.split("gcloud projects describe rapid-strength-333817"),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
  
  print(instance_output)
  
  print(env)
