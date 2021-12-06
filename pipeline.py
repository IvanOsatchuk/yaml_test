
import executor
import subprocess
import shlex

def func_labs_migration_pipeline(env):
    print('ENTROU')
    output = subprocess.run(shlex.split("gcloud projects describe rapid-strength-333817"), capture_output=True)
    res = output.stdout.decode("utf-8")
    err = output.stderr.decode("utf-8")

    result = {"res": res, "err": err}
    print('RESULTADO')
    print(result)
    #return result
