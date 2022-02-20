#%%
import streamlit
import dbt
import json
import pathlib
import subprocess
import pandas
import snowflake.connector
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization



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
        subprocess.run(["dbt", "compile"], cwd=self.dbt_dir.as_posix())

    def get_db_connection(self):
        account = os.environ["SNOWFLAKE_ACCOUNT"]
        user = os.environ["SNOWFLAKE_USER"]
        key_path = os.environ["SNOWFLAKE_KEY_PATH"]

        # Read Private ssh key from .p8 file
        with open(key_path, "rb") as key:
            p_key= serialization.load_pem_private_key(
                key.read(),
                password=None,
                backend=default_backend()
            )

        pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())

        # Connect to snowflake using the Provaiet key created above
        conn = snowflake.connector.connect(
            account=account,
            user=user,
            private_key=pkb,
            database='scratch',
            schema='dbt',
            warehouse='dbt',
        )
        return conn

    def _get_compiled_query(self, raw_query):
        name = "dynamic_query.sql"
        output_model_path = self.dbt_dir / "models" / name
        compiled_query_path = self.dbt_dir / "target" / "compiled" / "example_dbt_project" / "models" / name
        output_model_path.write_text(raw_query)
        self._compile_project()
        query = compiled_query_path.read_text()
        output_model_path.unlink()
        return query

    def get_query_results(self, raw_query):
        compiled = self._get_compiled_query(raw_query)
        return pandas.read_sql_query(compiled, self.conn)


    def populate_template_query(self, metric_name, time_grain, dimensions_list=[], secondary_calcs_list=[]):
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
        """.format(metric_name=metric_name, time_grain=time_grain, dimensions_list=dimensions_list, secondary_calcs_list=secondary_calcs_list)
        return query


    def get_metric_names(self):
        return {v["name"]: k for k, v in self.manifest["metrics"].items()}

