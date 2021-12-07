import yaml
import sys
import subprocess
import argparse

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


parser = config_parse()
args = parser.parse_args()
print("Started args: ", args)

env = args.env
sensitive_path = args.sensitive_path
non_sensitive_path = args.non_sensitive_path
path_project = ''

file = yaml.full_load(open('vars.yaml'))

if file['IsSensitive'] == True:
    path_project = sensitive_path
else:
    path_project = non_sensitive_path
    

for func in file['Functions']:
    subprocess.call(f"echo gcloud functions deploy $func --region=us-central1 --project={path_project} --source=./cloudfunction/{func} --trigger-http --entry-point=main --runtime=python39 --memory=2048MB --timeout=540 --set-env-vars=ENVIRONMENT=${env}", shell=True)


#print(" ".join(file['Functions']))

#subprocess.call('echo ' + str(file['IsSensitive']).lower() + '> /workspace/validate_sensitive.txt', shell=True)

#subprocess.call('echo ' + "".join(file['Functions']) + '> /workspace/functions_name.txt', shell=True)
    
    
if 'IsSensitive' not in file:
    raise Exception("[ERROR] IsSensitive fields not found")
if 'Functions' not in file:
    raise Exception("[ERROR] Functions fields not found")
if file['IsSensitive'] not in [True, False]:
    raise Exception("[ERROR] IsSensitive invalid value")
