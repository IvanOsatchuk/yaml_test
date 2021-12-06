import executor

def func_labs_migration_pipeline(env):
  
  test = executor.call_term("gcloud projects describe rapid-strength-333817", return_first_line=True)
  
  
  print(env)
