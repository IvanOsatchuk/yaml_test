# ===========================================================================================
# Objeto........: tb_eud_score_cad_clearsale
# Data Criacao..: 28/09/2021
# Projeto.......: Migração dados de Anti Fraude Clearsale
# Descricao.....: ETL - de: SFTP Clearsale | para: BQ
# Departamento..: Arquitetura e Engenharia de Dados
# Autor.........: Eric Carlos
# Email.........: t_leega.eric.carlos@grupoboticario.com.br
# ===========================================================================================
from datetime import datetime
import paramiko
import os
import io
import json
import pytz
import pandas as pd
from api_loader import ApiLoader

job_name = "ingestao_raw-tb_eud_score_cad_clearsale"
environment = os.environ.get("ENVIRONMENT")
timezone = pytz.timezone('America/Sao_Paulo')
init_time = datetime.now(tz=timezone)

with open(f"config-{environment}.json") as f:
  config = json.load(f)
  
secret = ApiLoader.load_secret(config["secret_project_id"], config["secret_id"])
config = {**config, **secret}

tablename = "{}.{}.{}".format(config['project_id'],config['raw_dataset'],config['raw_table'])
log_tablename = "{}.{}".format(config['raw_dataset'], config['raw_table'])

sftp_path = 'Eudora_CadastroRepresentante'

def load_sftp_file(filepath, hostname, username, password, port):
  ssh = paramiko.SSHClient()
  ssh.load_system_host_keys()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(hostname=hostname, username=username, password=password, port=port)
  sftp = ssh.open_sftp()
  buffer = sftp.open(filepath)
  buffer.prefetch()
  file = buffer.read()
  return file

def load_df(file):
  df = pd.read_csv(io.BytesIO(file), encoding='latin-1', sep=";")
  df['dt_atz_log'] = datetime.now(tz=timezone).strftime("%Y-%m-%d %H:%M:%S")
  df.columns = ApiLoader.table_schema(tablename)
  df[["data_crearsale", "datafinalizacao"]] = df[["data_crearsale", "datafinalizacao"]].astype('datetime64[s]')
  df = df.fillna(value='').astype(str)
  df['datafinalizacao'] = df['datafinalizacao'].astype('datetime64[s]')
  return df

# Entry point
def main(request):
  print(f"[INFO] Executando arquivo: {config['filepath']!r}")
  success = True
  df = pd.DataFrame()

  try:
    
    # Load file, create df
    file = load_sftp_file(config['filepath'], config['hostname'], config['username'], config['password'], config['port'])
    df = load_df(file)

    # Insert data into bigquery temp table
    ApiLoader.save_bq(df, tablename + '_tmp',True)
  
    # Query delta values
    sql = f"""SELECT tmp.*
            FROM {tablename + "_tmp"  } tmp
            LEFT JOIN {tablename} main
              ON tmp.datafinalizacao = main.datafinalizacao
              AND tmp.pedido = main.pedido
            WHERE main.pedido is null"""
    df_delta = ApiLoader.load_sql(sql, as_df=True)

    # Insert data to bigquery
    if len(df_delta) > 0:
      ApiLoader.save_bq(df_delta, tablename)
    
  except Exception as e:
    print(f"[ERROR] The following error ocurred: {e}")
    success = False
    
  total_lines = len(df_delta)
  end_time = datetime.now().astimezone(timezone)
  ApiLoader.save_log(config['log_tablename'], log_tablename, success, job_name, init_time, end_time, total_lines)

  status = "Completed" if success else "Failure"
  return f"Job {status}. Inserted a total of {total_lines} rows."  