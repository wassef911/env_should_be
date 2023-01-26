import os

def load_env_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    with open(file_path, 'r') as file:
        env_vars = {}
        for line in file:
            key, value = line.strip().split('=')
            env_vars[key] = value
    return env_vars

