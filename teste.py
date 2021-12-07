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
    
parser = config_parse()
args = parser.parse_args()
print("Started args: ", args)

file = yaml.full_load(open('vars.yaml'))


#with open('./workspace/validate_sensitive.txt','w') as f:
#    f.write(str(file['IsSensitive']).lower())

#with open('./workspace/functions_name.txt','w') as f:
#    f.write(' '.join(file['Functions']))

print(" ".join(file['Functions']))

subprocess.call('echo ' + str(file['IsSensitive']).lower() + '> /workspace/validate_sensitive.txt', shell=True)

subprocess.call('echo ' + "".join(file['Functions']) + '> /workspace/functions_name.txt', shell=True)
    
    
if 'IsSensitive' not in file:
    raise Exception("[ERROR] IsSensitive fields not found")
if 'Functions' not in file:
    raise Exception("[ERROR] Functions fields not found")
if file['IsSensitive'] not in [True, False]:
    raise Exception("[ERROR] IsSensitive invalid value")
