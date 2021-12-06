
import executor
import subprocess
import shlex
import os

def func_labs_migration_pipeline(env):
    
    subprocess.run(["gcloud", "projects", "describe", "rapid-strength-333817"], shell=True)
    
    
    process = subprocess.run(
        shlex.split("""gcloud auth print-access-token"""), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
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
