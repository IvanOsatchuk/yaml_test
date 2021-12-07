# ===========================================================================================
# Data Criacao..: 28/09/2021
# Projeto.......: Api Loader
# Descricao.....: Classe genérica p consulta de apis com paralelismo e inserção no BQ
# Departamento..: Arquitetura e Engenharia de Dados
# Autor.........: Eric Carlos
# Email.........: t_leega.eric.carlos@grupoboticario.com.br
# ===========================================================================================
import json
import re
import requests
import concurrent.futures as futures
from google.cloud import bigquery
from google.cloud import secretmanager
from datetime import datetime
import pytz
import pandas as pd


class ApiLoader():

  client = bigquery.Client()
  timezone = pytz.timezone('America/Sao_Paulo')
  rename_modes = ["camel", "space"]

  # Loads credentials from Secret Manager
  @staticmethod
  def load_secret(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return json.loads(payload)    

  # Loads from BQ max value from a specific column
  @staticmethod
  def max_table_value(tablename, column, dtype="STRING"):
    sql = f"SELECT MAX(CAST({column} AS {dtype})) AS max_value FROM {tablename}"
    query_job = ApiLoader.client.query(sql)
    result = query_job.result()  # Waits for job to complete.
    max_value = next(result).max_value
    return max_value

  # Creates a data range from min and max date. Expects both in %Y-%m-%d format
  @staticmethod
  def create_date_range(min_date, max_date):
    min_date, max_date = str(min_date), str(max_date)
    date_range = pd.date_range(min_date, max_date).astype(str).tolist()
    return date_range
  
  # Retrieves column names from specified table
  @staticmethod
  def table_schema(tablename, with_types=False):
    schema = ApiLoader.client.get_table(tablename).schema
    
    columns = []
    
    for col in schema:
      columns.append((col.name, col.field_type) if with_types else col.name)

    return columns

  # Truncates table
  @staticmethod
  def truncate_table(tablename):
    print(f"[INFO] Truncanting table {tablename!r}")
    sql = f"TRUNCATE TABLE {tablename}"
    ApiLoader.load_sql(sql)

  # Deduplicate table based on fields
  @staticmethod
  def deduplicate_table(df, tablename, dedup_field):
    print(f"[INFO] Deduplicating table {tablename!r} by field {dedup_field!r}")
    values_to_delete = str(df[dedup_field].unique().tolist())[1:-1]
    dedup_filter = f"{dedup_field} IN ({values_to_delete})"
    sql = f"DELETE FROM {tablename} WHERE {dedup_filter}"
    ApiLoader.load_sql(sql)

  # Loads Dataframe via SQL string
  @staticmethod
  def load_sql(sql, as_df=False):    
    result = ApiLoader.client.query(sql).result()  

    if not as_df:
      return result

    df = result.to_dataframe()
    return df

  # Convert column names from specific appraoches
  @staticmethod
  def rename_columns(columns, mode="camel"):
    
    if mode not in ApiLoader.rename_modes:
        raise Exception(f"Mode must be one of {ApiLoader.rename_modes}.")
        
    function = getattr(ApiLoader, f"_{mode}_to_snake")
    columns = [function(ApiLoader, c) for c in columns] 
    # prefix with underline columns with name forbidden by BQ(e.g. starts with numbers, special chars, etc)
    columns = [f"_{c}" if re.match("[^a-z_].+", c) else c for c in columns] 
    return columns

  # Load urls by username and password with paralellism
  @staticmethod
  def load_auth_urls(urls, username, password, encoding="utf-8", timeout=5):

    def load_url(url, timeout):
      res = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))
      return url, res.content.decode(encoding)

    urls = [urls] if type(urls) is str else urls
    with futures.ThreadPoolExecutor(max_workers=max(1, len(urls) // 2)) as executor:
      future_urls = (executor.submit(load_url, url, timeout) for url in urls)
      items = [future.result() for future in futures.as_completed(future_urls)]
    
    return items

  # Load urls by header paramswith paralellism
  @staticmethod
  def load_param_urls(urls, params, encoding="utf-8", timeout=5):

    def load_url(url, timeout):
      res = requests.get(url, params=params)
      return url, res.content.decode(encoding)

    urls = [urls] if type(urls) is str else urls
    with futures.ThreadPoolExecutor(max_workers=max(1, len(urls) // 2)) as executor:
      future_urls = (executor.submit(load_url, url, timeout) for url in urls)
      items = [future.result() for future in futures.as_completed(future_urls)]
    
    return items

  # Saves data to BigQuery
  @staticmethod
  def save_bq(df, tablename, is_temp_table=False , chunksize=300000):
    print(f"[INFO] Saving {tablename} to BQ...")

    # if temp table then truncate before insert
    if is_temp_table:
      sql = f"TRUNCATE TABLE {tablename}"
      ApiLoader.load_sql(sql)
      print(f"[INFO] Truncating temp table {tablename}")

    if not df.empty:
        df.to_gbq(tablename, if_exists='append', chunksize=chunksize)
    print(f"[INFO] Inserted {len(df)} rows in table {tablename!r}.")

  # Saves log from execution
  @staticmethod
  def save_log(log_tablename, tablename, success, job_name, init_time, end_time, total_lines=0):
    print("[INFO] Saving logs ...")

    log = {
      'TABELA': [tablename],
      'DATA_INICIO': [init_time],
      'DATA_FIM': [end_time],
      'LINHAS_CARREGADAS': [total_lines],
      'STS_CARGA': ["SUCESSO" if success else "ERRO"],
      'HOST': ["GCFUNCTION"],
      'NOME_JOB': [job_name]
    }
    
    df = pd.DataFrame(log)
    df.to_gbq(log_tablename, if_exists="append")
    
  # Convert column names from scace/underline to snakecase
  def _space_to_snake(self, string):
    groups = re.findall("(\w+)", string)
    return '_'.join(groups).lower()

  # Convert column names from camelcase to snakecase
  def _camel_to_snake(self, string):
    string = string[0].upper() + string[1:]
    groups = re.findall("([A-z\d][a-z\d]+)", string)
    return '_'.join(groups).lower()
