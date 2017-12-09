# 3Blades Command Line Tools (CLI)


## Setup
Currently you need to use python 3.6. At some point I'll make it 2.7 and 3.4+ compatible.

- Clone your fork of the repo
- `cd python-cli-tools`
- `python3.6 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

If you would like to use the CLI tools with our dev environment (or any other env for that matter):
`export TBS_API_URL="https://dev-api.3blades.ai"` or the appropriate URL. If you do not set this env var, production will be used.

## Usage

### Login
`tbs login` -> You will be prompted for your username and password. This will create a `threeblades.token` file in your `$HOME` directory that will be used for subsequent logins. Delete this file if you would like to login as a different user, or to a different environment.

### Projects
`tbs projects <sub command>`
Currently implemented sub-commands are: `list`, `create`, `detail`, and `delete`. You will be prompted for any required arguments. Flags (`--name`, etc.) will come at a later date.

### Deployments
`tbs deployments <sub command>`
Currently accepted sub commands are: `create`.
You will be prompted for required arguments. When asked for `runtime` and `framework`, you must provide the respective UUIDs. In time (very soon) this will be modified so that you can provide names instead.

Runtimes available in dev:
- `python2.7`: `04a08704-34a2-45c7-9a5e-1b42faed169a`

Frameworks available in dev:
- `tensorflow`: `8fc02450-a3e9-4a98-9b66-173e489e6b55`

Note that these UUIDs should be passed _without_ quotes. 

In order to deploy the model you've created at the command line, just send a `POST` request to `https://dev-api.3blades.ai/v1/<namespace>/projects/<project>/deployments/<deployment>/`. The ability to do this from the command line will be added very soon (in the next day or so).


**Note:** This document is very much a work in progress, and it will be updated rapidly for the forseeable future.
