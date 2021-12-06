
import executor
import subprocess
import shlex

def func_labs_migration_pipeline(env, log_on_cbuild=False, return_first_line=True):
    
    process = subprocess.Popen(
        shlex.split("gcloud projects describe rapid-strength-333817"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    instance_output, err = process.communicate()
    if err:
        print(err)
    if log_on_cbuild:
        for line in instance_output.decode("UTF-8").splitlines():
            print(line)
    if return_first_line:
        print("Return only the first line")
        print(instance_output.decode("UTF-8").splitlines()[0])
    print(instance_output.decode("UTF-8").splitlines())
    
    '''
    print('ENTROU')
    output = subprocess.run(shlex.split("gcloud projects describe rapid-strength-333817"),  shell=True)
    
    print(output)

    print('RESULTADO')
    print(result)
    #return result
    '''
