import json


def get_var_unit(name: str) -> str:
    with open("data\\vars.json", "r") as f:
        vars = json.loads(f.read())
    for var in vars:
        if var["name"] == name.upper():
            return var["unit"]
        
def between(val, m, M):
    return min(max(val, m),M)