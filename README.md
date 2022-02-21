# streamlit-dbt-metrics-explorer

This repo contains the code for the X-treme MetriX X-plorer, a very simple Streamlit
app that parses a dbt project's graph for metrics nodes, queries a database according
to the provided metric / dimensions, and plots the results using matplotlib.

To access the project online, go to [Streamlit Share](https://share.streamlit.io/stkbailey/streamlit-dbt-metrics-explorer/main/app.py).

## Running locally

To run the project locally, you will need to build the dbt `example_dbt_project` against a Postgres database. Example code is below:

First, set Postgres database environment variables.

```
export POSTGRES_SERVER="my_server.com"
export POSTGRES_USER="my_user"
export POSTGRES_PASSWORD="my_pasword"
export POSTGRES_DATABASE="my_database"
```

Then, install the project requirements, which includes `dbt-postgres` using [Poetry](https://python-poetry.org/docs/), a package manager for Python.

```
poetry install
```

Then, build the dbt project against your database. The included profile is set to run against an `analytics` database,
but you can override this using the `POSTGRES_DATABASE` environment variable as shown above.

```
cd example_dbt_project
poetry run dbt build --profiles-dir .
```

If successful, you will now have the seed data and models available in your database.
To add new metrics, seeds, etc., you can now simply add them to this dbt project.

Now, you're ready to run the Streamlit app! Return to the root directory and run the Streamlit app.

```
cd ..       # should be in the root of the project
poetry run streamlit run app.py
```

Now go do some extreme metrixing!

## Terraform

If you want to stand up a Postgres database in AWS, you can use the Terraform provided to do so quickly and from the command line.
It will stand up a new VPC, some subnets, a security group, and a micro-sized RDS Postgresql database.
It should be publicly accessible to all IPs. You can modify the security group settings to lock this down if desired.
