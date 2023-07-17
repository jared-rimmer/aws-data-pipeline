## Requirements

- Docker
- Python3.8+

### Setting Up The Python Environment

1. Ensure you are in the root of this repository
2. Create the virtual environment by typing `python3 -m venv ./env` in your terminal
3. Activate the virtual environment by typing `source env/bin/activate` in your terminal
4. Install the project dependencies by typing `pip install -r requirements.txt` in your terminal

### Setting Up Python Path

If you are using VS Code:

1. Create a directory in the root of the folder called .vscode `mkdir .vscode`
2. Within that directory create a file called `settings.json`
3. In this file copy the following:

```json
{
    "terminal.integrated.env.osx": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
}
```

If you are not on a Mac you will have to replace the terminal to the one that matches your development machine.

If you aren't using VS code you can type the following into your terminal

```bash
export PYTHONPATH=${PYTHONPATH}:./src
```

**Please note**: 

- If using the VS code method you might have to reload your terminal / VS code in order for these updated settings to persist.

- If using the export method this variable will only persist for the duration of your terminal. If you close your terminal this will have to be re-run in order to set the environment variable again.

### Bring Up The Docker Containers

1. Ensure that you are in the root of this repository
2. Ensure that Docker is running on your machine.
3. Bring up the Docker containers by typing `docker-compose up -d` in your terminal.

## Running The Tests

The test suite has been set up to run using Tox for Python versions:

- 3.8
- 3.9
- 3.10
- 3.11

If you have all of these versions installed on your machine you can go ahead and type the following in your terminal:

```bash
tox -e py38,py39,py310,py311
```

However, if you do not have all versions of Python installed on your machine then you can just remove the ones that you don't have.

For example just Python 3.8:

```bash
tox -e py38
```

Just Python 3.10 and 3.11

```bash
tox -e py310,py311
```

### Bring Down The Docker Containers

1. Ensure that you are in the root of this repository
2. Bring down the Docker containers by typing `docker-compose down` in your terminal.
