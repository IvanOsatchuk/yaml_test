
import executor
import subprocess
import shlex

def func_labs_migration_pipeline(env):
    print('ENTROU')
    output = subprocess.run(shlex.split("gcloud projects describe rapid-strength-333817"),  shell=True)
    
    print(output)

    print('RESULTADO')
    print(result)
    #return result
