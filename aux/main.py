import yaml

vars = yaml.full_load(open("vars.yaml"))

print(vars.get('sensitive'))

print(vars.get('functions'))

print("hello Python")
