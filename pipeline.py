
import executor
import subprocess
import shlex
import os

def func_labs_migration_pipeline(env):
    
    process = subprocess.run(
        shlex.split("""gcloud projects describe rapid-strength-333817"""), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
   
    print(process)
    
    '''
    print('ENTROU')
    output = subprocess.run(shlex.split("gcloud projects describe rapid-strength-333817"),  shell=True)
    
    print(output)

    print('RESULTADO')
    print(result)
    #return result
    '''
