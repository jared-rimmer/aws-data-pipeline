## Background

This project was inspired by:

- [An article](https://www.startdataengineering.com/post/setting-up-e2e-tests/) on end-to-end data testing on the Start Data Engineering blog
- The [Robust ETL Design and Implementation for Amazon Redshift](https://redshiftresearchproject.org/white_papers/downloads/robust_etl_design_and_implementation_for_amazon_redshift.html) Whitepaper

The project uses the ETL implementation detailed in the Whitepaper, which uses versioned files that are compared against the data warehouse in order to run updates and deletes to ensure the data warehouse is always up-to-date with these latest file versions.

The structure of the project is built using the [Start Data Engineering git repository](https://github.com/josephmachado/e2e_datapipeline_test) that accompanies the end-to-end data testing blog post. I have kept the bits that I liked and changed bits out to use tools and packages that I  I thought were a better fit such as Tox and pg8000 for the Python Postgres client.

### What I learnt:

- [Moto](https://github.com/getmoto/moto) for mocking out AWS services
- [pg8000](https://github.com/tlocke/pg8000) is a good alternative to [psycopg2](https://github.com/psycopg/psycopg2) when using it in AWS Lambda functions
- AWS Lambdas need the Python [dependencies to be included in the ZIP file](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies) that gets deployed.
- Lots more about [Tox](https://tox.wiki/en/latest/user_guide.html) and how to configure it
- More about patching in tests in order to ensure specific behaviour is being tested. 
- How set-up and tear-down methods are done differently in Pytest vs Unittest
- Setting up Docker networking correctly for Moto Server so the Lambda function is executed in a standalone Docker container.

## Data Pipeline Structure

1. Files loaded to SFTP server
2. Check for files on SFTP server that have been updated after the last pipeline run
3. Load the files from step 2 to an Amazon S3 bucket for raw data
4. Retrieve the latest version of all files in the Amazon S3 raw data bucket and load them to a Amazon S3 bucket for staging data
5. Delete all files in the Amazon S3 staging bucket except for the latest files that have been loaded
6. Check the Postgres data warehouse for rows with a source_data column equal to file names in the Amazon S3 staging bucket that are not in the Postgres data warehouse. Load these into the Postgres data warehouse.
7. Check the Postgres data warehouse for rows with a source_data column equal to file names that are no longer in the Amazon S3 staging bucket and remove them from Postgres


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
