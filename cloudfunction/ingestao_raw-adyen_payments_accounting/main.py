# ===========================================================================================
# Objeto........: adyen_payment_accouting
# Data Criacao..: 29/10/2021
# Projeto.......: Migração dados de pagamento Adyen
# Descricao.....: ETL - de: API Adyen | para: BQ
# Departamento..: Arquitetura e Engenharia de Dados
# Autor.........: Eric Carlos
# Email.........: t_leega.eric.carlos@grupoboticario.com.br
# ===========================================================================================
import pandas as pd
from datetime import datetime, date, timedelta
import os
import io
import json
import pytz
from api_loader import ApiLoader


# Enviroment Variables
DAYS_WINDOW = 4
environment = os.environ.get("ENVIRONMENT", "dev")
timezone = pytz.timezone('America/Sao_Paulo')

# Deduplication fields
dedup_fields = ["merchant_reference","booking_date"]

init_time = datetime.now().astimezone(timezone) 
job_name = "ingestao_raw-adyen_payment_accounting"
merchant_account = "Boticario-US"

# Read Config file
with open(f"config-{environment}.json") as f:
  config = json.load(f)

# Read Google Cloud Secret
secret = ApiLoader.load_secret(config["secret_project_id"], config["secret_id"])
config = {**config, **secret}

# Create tables name
tablename = config['project_id'] + '.' + config['raw_dataset'] + '.' + config['raw_table']
log_tablename = config['raw_dataset'] + '.' + config['raw_table']

def load_df(responses):
  df = pd.concat([pd.read_csv(io.StringIO(r[1])) for r in responses])
  df = df.fillna("").astype(str)
  df.columns = ApiLoader.rename_columns(df.columns.tolist(), mode="space")
  df['nr_safra'] = df.booking_date.str.replace('-', '').str[:8] 
  df['dt_atz_log'] = datetime.now().astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")
  return df

# Entry point
def main(request):
  print(f"[INFO] Running environment: {environment}")  
  success = True

  # Generating date array
  min_date = ApiLoader.max_table_value(tablename=tablename, column="booking_date")
  min_date = min_date.date()
  min_date -= timedelta(days=DAYS_WINDOW)
  max_date = (datetime.now().astimezone(timezone) - timedelta(days=1)).date()
  date_range = ApiLoader.create_date_range(min_date, max_date)
  print(f"[INFO] Running dates: {date_range}")

  # Getting history data to compare
  sql = f""" 
    SELECT {','.join(dedup_fields)}
    FROM {tablename}
    WHERE date(booking_date) >= '{min_date}' """
  df_hist = ApiLoader.load_sql(sql,as_df=True)
  df_hist['booking_date'] = df_hist['booking_date'].astype('datetime64[ns]')
  print(f"[INFO] Extracting history data")
  
  
  # Making request to adyen site
  urls = [config['url'].format(merchant_account, str(dt).replace("-", "_")) for dt in date_range]
  responses = ApiLoader.load_auth_urls(urls, config['username'], config['password'])
  
  # Getting request response
  empty_responses = list(filter(lambda r: not r[1], responses))
  df = pd.DataFrame()
    
  # Verify if reponse is null
  if empty_responses:
    empty_responses = '\n'.join([r[0] for r in empty_responses])
    print(f"[WARNING] The following URL's were not loaded:\n{empty_responses}")
    success = False
  
  # Getting input data request
  if success:
    df = load_df(responses)
    df['booking_date'] = df['booking_date'].astype('datetime64[ns]')

    # Deduplicating data 
    df_merged = df.merge(df_hist, how='left',indicator=True)
    df_delta = df_merged[df_merged._merge == 'left_only'].drop('_merge', axis=1)

    # Changing data type fit in bigquery 
    df_delta = df_delta.astype('str')

    # Load data into bigquery
    ApiLoader.save_bq(df_delta, tablename)
  
  if success:
    total_lines = len(df_delta)
  else:
    total_lines = 0
  
  end_time = datetime.now().astimezone(timezone)
  ApiLoader.save_log(config['log_tablename'], log_tablename, success, job_name, init_time, end_time, total_lines)

  status = "Completed" if success else "Failure"
  return f"Job {status}. Inserted a total of {total_lines} rows."