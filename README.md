<h1 align="center">
    <strong>data load tool (dlt) — hashing and droping pii data</strong>
</h1>
<p align="center">

This example shows how to use dlthub to process Personally Identifiable Information coming from a postgres database. dlt is library ([not a platform](https://dlthub.com/product/#a-library-not-a-platform)) to quickly moc and run a meaningul pipeline dumping data to somewhere. It has a nice philosophy and what's inside the lib just works efficiently.

## dlt official repo
The official repo of dlt is https://github.com/dlt-hub/dlt. The site with documentation and GPT support is https://dlthub.com

## Prepare your venv
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt #pip freezed
```

## dlt init

This repo already contains all the necessary files to use dlt to extract data from postgres. You could use the command below if you want to compare or generate the sources from scratch.

<em>The code inside [/src](./src/) was created with this command.</em>

```bash
# dlt init <source> <destiny>
dlt init sql_database filesystem
```

- List of dlt "verified sources": https://dlthub.com/docs/dlt-ecosystem/verified-sources/
- List of destinations: https://dlthub.com/docs/dlt-ecosystem/destinations/

Don't fool yourself, you may not found your prefereble source but is easy to create your own. Seriosly.

## Start a local Postgres instance
Run a postgres instance through docker.

```bash
docker run --name postgres-dlt -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

<em>Take a look at [src/data_generator.sql](/src/data_generator.sql). The file helps you create a table with random data to run the example.</em>

## Run the example

Call [sql_database_pipeline.py](sql_database_pipeline.py) to run a pipe that reads data from the postgres instance and load to a local folder as jsonl format. The script will also output the data to your terminal. Note how the email column will be hashed.



```bash
python sql_database_pipeline.py
```

```bash
{'id': 1, 'first_name': 'name1', 'email': '0a85ae3e47a0a3c91bfd7af40b507cce15d796dbc3729fdfb5cb80fdb9b52d93', 'address': 'stree1', 'updated_at': datetime.datetime(2023, 9, 13, 16, 45, 5, 53497)}
{'id': 2, 'first_name': 'name2', 'email': '7e715e3b6cf5fa3de641e5bdb1e7a05771a3ed7e693f268397c0be96fcb71eef', 'address': 'stree2', 'updated_at': datetime.datetime(2023, 9, 13, 16, 45, 5, 53497)}
{'id': 3, 'first_name': 'name3', 'email': '674e862f1a9d4a5f93022dd3d4de1c846f67f7140191c5e69730fe5eb9fd5b0c', 'address': 'stree3', 'updated_at': datetime.datetime(2023, 9, 13, 16, 45, 5, 53497)}
{'id': 4, 'first_name': 'name4', 'email': 'e10c0f386a086706ca4e8353ab2f8d615bab385ce1950b2ada202c7f1d02f1bf', 'address': 'stree4', 'updated_at': datetime.datetime(2023, 9, 13, 16, 45, 5, 53497)}
```

The file contains two functions to hash or drop any column. We just need to add_map to the table being extracted.

```python
def hash_column(col):
    def hash(doc):
        salt = "WI@N57%zZrmk#88c"
        salted_string = doc["email"] + salt
        sh = hashlib.sha256()
        sh.update(salted_string.encode())
        hashed_string = sh.digest().hex()
        doc[col] = hashed_string
        doc[f"new_{col}_hashed"] = hashed_string
        return doc

    return hash

def drop_column(col):
    def drop(doc):
        doc.pop(col, None)
        return doc

    return drop
```

```python
source_1.sensible_table.add_map(hash_column("email"))
# source_1.sensible_table.add_map(drop_column("email"))
```


<em>In this example, dlt will create a local folder called destiny_pii_data to save the extracted data. But it also can [load data directly to s3.](https://dlthub.com/docs/dlt-ecosystem/destinations/filesystem)</em>
