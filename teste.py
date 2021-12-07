import yaml
import sys

print(sys.argv)

file = yaml.full_load(open('vars.yaml'))


with open('./workspace/validate_sensitive.txt','w') as f:
    f.write(str(file['IsSensitive']).lower())

with open('./workspace/functions_name.txt','w') as f:
    f.write(' '.join(file['Functions']))


if 'IsSensitive' not in file:
    raise Exception("[ERROR] IsSensitive fields not found")
if 'Functions' not in file:
    raise Exception("[ERROR] Functions fields not found")
if file['IsSensitive'] not in [True, False]:
    raise Exception("[ERROR] IsSensitive invalid value")
