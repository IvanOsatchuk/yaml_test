import yaml

vars = yaml.full_load(open("vars.yaml"))

print(vars.get('valor1'))

print(vars.get('valor2'))

print(vars.get('valor3'))

print("hello Python")
