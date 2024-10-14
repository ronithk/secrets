import subprocess
import json
import sys
import uuid
import os
import argparse

def get_repo_details():
    try:
        json_output = subprocess.check_output(
            ['gh', 'repo', 'view', '--json', 'name,owner'],
            stderr=subprocess.PIPE,
            universal_newlines=True
        ).strip()

        repo_details = json.loads(json_output)
        return repo_details
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error: failed to get git repo details.")

def get_secrets(repo_details, profile=""):
    try:
        json_output = subprocess.check_output(
            ['op', 'item', 'get', repo_details["name"], '--vault', repo_details["owner"]["login"], '--fields', 'type=concealed', '--format', 'json'],
            stderr=subprocess.PIPE,
            universal_newlines=True
        ).strip()

        json_data = json.loads(json_output)
        secrets_array = [json_data] if isinstance(json_data, dict) else json_data

        secrets = {}
        for item in secrets_array:
            item_contains_secret = "label" in item and "value" in item
            item_section = item.get("section", {}).get("id", "")
            if item_contains_secret and item_section.lower() == profile.lower():
                secrets[item['label']] = item['value']

        return secrets
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error: couldn't find secrets for {repo_details}.")

def shell(secrets):
    print("Spawing subshell with the following environment variables exported:")
    for key in secrets.keys():
        print(f'• {key}')

    new_env = os.environ.copy()
    new_env.update(secrets)

    current_shell = os.environ.get('SHELL', '/bin/bash')

    subprocess.run(current_shell, env=new_env)

def run(secrets, args):
    new_env = os.environ.copy()
    new_env.update(secrets)

    current_shell = os.environ.get('SHELL', '/bin/bash')

    subprocess.run(" ".join(args), shell=True, executable=current_shell, env=new_env)

def main():
    parser = argparse.ArgumentParser(description="Secret manager for 1Password.")
    parser.add_argument('command', choices=["run", "shell"] , help="Execute command in subshell.")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Additional arguments for the command.")
    args = parser.parse_args()

    try:
        repo_details = get_repo_details()
        secrets = get_secrets(repo_details)

        if args.command == "run":
            run(secrets, args.args)
        elif args.command == "shell":
            shell(secrets)
    except Exception as e:
        print(f"\033[91m{e}\033[0m", file=sys.stderr)

if __name__ == "__main__":
    main()
