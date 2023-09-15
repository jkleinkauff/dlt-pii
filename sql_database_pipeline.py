from typing import List

import dlt
from dlt.sources.credentials import ConnectionStringCredentials
import hashlib
from dlt.common import pendulum

from src.sql_database import sql_database, sql_table


def hash_column(col):
    def hash(doc):
        salt = "WI@N57%zZrmk#88c"
        salted_string = doc["email"] + salt
        sh = hashlib.sha256()
        sh.update(salted_string.encode())
        hashed_string = sh.digest().hex()
        doc[col] = hashed_string
        # doc[f"new_{col}_hashed"] = hashed_string
        return doc

    return hash


def drop_column(col):
    def drop(doc):
        doc.pop(col, None)
        return doc

    return drop


def load_select_tables_from_database() -> None:
    """Use the sql_database source to reflect an entire database schema and load select tables from it.

    This example sources data from the public Rfam MySQL database.
    """
    pipeline = dlt.pipeline(
        pipeline_name="pii_pipeline",
        destination="filesystem",
        dataset_name="pii_dataset",
        progress="log",
    )

    # Configure the source to load a few select tables incrementally
    # Use source = sql_database() to load all tables
    source_1 = sql_database().with_resources("sensible_table")

    # Use when doing incremental
    # source_1.sensible_table.apply_hints(incremental=dlt.sources.incremental("updated_at"))
    # dlt could automatically identify the primary key, tho
    # source_1.sensible_table.apply_hints(primary_key="id")

    # handle pii data or any sensible info - before load
    source_1.sensible_table.add_map(hash_column("email"))
    # source_1.sensible_table.add_map(drop_column("email"))
    for row in source_1.sensible_table:
        print(row)

    info = pipeline.run([source_1], write_disposition="replace")
    print(info)


if __name__ == "__main__":
    load_select_tables_from_database()
