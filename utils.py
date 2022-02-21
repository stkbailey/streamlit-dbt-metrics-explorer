#%%
import streamlit
import dbt
import json
import pathlib
import subprocess
import pandas
import os
import psycopg2


class MetricsUtil:
    def __init__(self):
        self.dbt_dir = pathlib.Path().cwd() / "example_dbt_project"
        self.conn = self.get_db_connection()
        self.manifest = self._read_manifest_file()
        self.metrics_list = self.get_metric_names()

    def _read_manifest_file(self):
        manifest_path = self.dbt_dir / "target" / "manifest.json"
        if not manifest_path.exists():
            self._compile_project()
        text = manifest_path.read_text()
        return json.loads(text)

    def _compile_project(self):
        cmd = ["dbt", "compile", "--profiles-dir", "."]
        subprocess.run(cmd, cwd=self.dbt_dir.as_posix())

    def _build_project(self):
        cmd = ["dbt", "build", "--profiles-dir", "."]
        subprocess.run(cmd, cwd=self.dbt_dir.as_posix())

    def _run_project(self):
        cmd = ["dbt", "run", "--profiles-dir", "."]
        subprocess.run(cmd, cwd=self.dbt_dir.as_posix())

    def get_db_connection(self):
        # Connect to snowflake using the Provaiet key created above
        conn = psycopg2.connect(
            host=os.environ["POSTGRES_SERVER"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            dbname="analytics",
        )
        return conn

    def _get_compiled_query(self, raw_query):
        name = "dynamic_query.sql"
        output_model_path = self.dbt_dir / "models" / name
        compiled_query_path = (
            self.dbt_dir
            / "target"
            / "compiled"
            / "example_dbt_project"
            / "models"
            / name
        )
        output_model_path.write_text(raw_query)
        self._compile_project()
        query = compiled_query_path.read_text()
        output_model_path.unlink()
        return query

    def get_query_results(self, raw_query):
        compiled = self._get_compiled_query(raw_query)
        return pandas.read_sql_query(compiled, self.conn)

    def populate_template_query(
        self, metric_name, time_grain, dimensions_list=[], secondary_calcs_list=[]
    ):
        query = """
        select * from
        {{{{ 
            metrics.metric(
                metric_name='{metric_name}',
                grain='{time_grain}',
                dimensions={dimensions_list},
                secondary_calculations={secondary_calcs_list}
            )
        }}}}
        where period between '2016-01-01':: date and '2021-10-01':: date
        order by period
        """.format(
            metric_name=metric_name,
            time_grain=time_grain,
            dimensions_list=dimensions_list,
            secondary_calcs_list=secondary_calcs_list,
        )
        return query

    def get_metric_names(self):
        return {v["name"]: k for k, v in self.manifest["metrics"].items()}
