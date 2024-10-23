Secrets makes it easy to export secrets as environment variables. It (currently) wraps the 1Password CLI tool and uses 1Password as a source of truth for your environment variables.

# Installation
Before you can use Secrets, you need to:
* [Set up 1Password and its CLI tool](https://1password.com/downloads/command-line).
* [Set up the gh CLI tool](https://cli.github.com/).

Make sure you're signed into both of them! In the future, Secrets will be updated to remove `gh` as a dependency, and it will allow other sources for your secrets besides 1Password.

---

The easiest way to install Secrets itself is with pip:
```bash
pip install git+https://github.com/ronithk/secrets.git
```

However, you can also just add the secrets.py script to your PATH. Right now there are no external dependencies (although, this might change in the future).

Note that you do need to have at least `Python 3.11` installed.

# Setup
Let's setup the secrets for your projects inside 1Password. `secrets` resolves which secrets it should apply using the GitHub repo of the folder you're in. For example, if you're running Secrets in a folder linked to `interface-club/hello-world`, it will:
1. Sign in to your last used 1Password account
2. Look for a 1Password vault named `Secrets`.
3. Look for a 1Password item in that vault that matches `hello-world`.
4. Look for all the "password" fields in that item and export them as environment variables.

If you are using multiple 1Password accounts, or multiple orgs: you can specify a specific 1Password account and vault to use for a specific organization in `~/.config/secrets.toml`.
```toml
[github.interface-club]
op_account="{OP_ACCOUNT_USER_ID}"
op_vault="repo-secrets"
```

Now if we use `secrets` in the same `interface-club/hello-world` folder as before, it will:
1. Sign in to the 1Password account with the user ID specified in `~/.config/secrets.toml`.
2. Look for a 1Password vault named `repo-secrets`.
3. Look for a 1Password item in that vault that matches `hello-world`.
4. Look for all the "password" fields in that item and export them as environment variables.

In the future, you will be able to make separate "sections" within an item and switch between them using a `--profile` flag. This is useful, for example, if you need different environment variables for dev, staging, production, etc.

We will also add support for other sources of secrets besides 1Password, such as a private git repository.

# Usage
To inject secrets into your environment at runtime, wrap your command with `secrets run`. For example, lets say you have a python project that you're running with `poetry run python main.py`. To inject your secrets:
```bash
secrets run poetry run python main.py
```

You can also start an interactive subshell with your secrets:
```bash
secrets shell
```
