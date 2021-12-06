import executor

def func_labs_migration_pipeline(env):
  
  executor.call_term('gcloud projects describe rapid-strength-333817')
  
  
  print(env)
