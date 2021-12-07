import yaml
import sys
import subprocess
from subprocess import Popen, PIPE
import argparse

def validate(file):
    if 'IsSensitive' not in file:
        raise Exception("[ERROR] IsSensitive fields not found")
    if 'Functions' not in file:
        raise Exception("[ERROR] Functions fields not found")
    if file['IsSensitive'] not in [True, False]:
        raise Exception("[ERROR] IsSensitive invalid value")
        
def call_gcloud(func, path_project, env, log_on_cbuild=True, return_first_line=True):
    #p = subprocess.call(f"""
    #          gcloud functions deploy {func} --region=us-central1 --project={path_project} --source=./cloudfunction/{func} --trigger-http --entry-point=main --runtime=python39 --memory=2048MB --timeout=540 --set-env-vars=ENVIRONMENT={env}
    #          """, shell=True)
    p = Popen(f"""
              gcloud functions deploy {func} --region=us-central1 --project={path_project} --source=./cloudfunction/{func} --trigger-http --entry-point=main --runtime=python39 --memory=2048MB --timeout=540 --set-env-vars=ENVIRONMENT={env}
              """, shell=True)
    subprocess.call("""echo teste""", shell=True)
    print(p)

def config_parse():
    print("Start Data Fusion CICD")
    parser = argparse.ArgumentParser(description="ENV vars")

    parser.add_argument(
        "--ENV",
        type=str,
        dest="env" 
    )
    parser.add_argument(
        "--SENSITIVEPATH",
        type=str,
        dest="sensitive_path" 
    )
    parser.add_argument(
        "--NONSENSITIVEPATH",
        type=str,
        dest="non_sensitive_path" 
    )
    return parser

if __name__ == "__main__":
    
    file = yaml.full_load(open('vars.yaml'))
    
    validate(file)

    parser = config_parse()
    args = parser.parse_args()
    print("Started args: ", args)

    env = args.env
    sensitive_path = args.sensitive_path
    non_sensitive_path = args.non_sensitive_path
    path_project = ''

    if file['IsSensitive'] == True:
        path_project = sensitive_path
    else:
        path_project = non_sensitive_path
    
    
    
    
        

    for func in file['Functions']:
        print(f"teste {func}")
        
        cmd = f"""gcloud functions deploy {func} --region=us-central1 --project={path_project} --source=./cloudfunction/{func} --trigger-http --entry-point=main --runtime=python39 --memory=2048MB --timeout=540 --set-env-vars=ENVIRONMENT={env}"""
        
        subprocess.call(f"""echo  {cmd}  > /workspace/run.sh""", shell=True)
        #subprocess.call(f"""gcloud functions deploy {func} --region=us-central1 --project={path_project} --source=./cloudfunction/{func} --trigger-http --entry-point=main --runtime=python39 --memory=2048MB --timeout=540 --set-env-vars=ENVIRONMENT={env}""", shell=True)
    subprocess.call("""cat  /workspace/run.sh""", shell=True)
        
        
        #subprocess.call('echo "teste"')
        #subprocess.call(f"gcloud functions deploy {func} --region=us-central1 --project={path_project} --source=./cloudfunction/{func} --trigger-http --entry-point=main --runtime=python39 --memory=2048MB --timeout=540 --set-env-vars=ENVIRONMENT={env}", shell=True)


   

    
