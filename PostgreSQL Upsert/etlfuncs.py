import pandas as pd
import numpy as np
import os
import pyodbc
import csv
import gzip
from cryptography.fernet import Fernet
import hdfs
from crdntls import hdfs_info
import boto3
from crdntls import s3_info
from crdntls import bi_email_server
from datetime import datetime
import smtplib
import pysftp
import paramiko
from email.message import EmailMessage
from ftplib import FTP
import json
import sys
import time

key = os.getenv("PYKEY1")

def log_screen(txt):
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S") + ' ' + txt)

def log_db(job_id, job_name, run_id, event_type, error_msg, job_metadata):
    local_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insertquery = '''
    insert into bi20.jobs_log values ('{}','{}','{}','{}','{}','{}','{}')
    '''.format(job_id, local_ts, job_name, run_id, event_type, error_msg, job_metadata)
    run_sql('citus', insertquery)

#key = Fernet.generate_key()
#with open("key.key", "wb") as key_file:
#   key_file.write(key)

def encrypt_pwd(pwd, key):
    cipher_eng = Fernet(key)
    enc_pwd = cipher_eng.encrypt(bytes(pwd, 'utf-8')) 
    print(enc_pwd.decode('utf-8'))

def decrypt_pwd(pwd, key):
    cipher_eng = Fernet(key)
    dec_pwd = cipher_eng.decrypt(bytes(pwd, 'utf-8')) 
    return dec_pwd.decode("utf-8")

def run_sql(dsn, query):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.close()

def run_sql_hive(dsn, query, partitions):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    cursor = conn.cursor()
    cursor.execute(f'SET spark.sql.shuffle.partitions={partitions}')
    cursor.execute(query)
    cursor.close()
    conn.close()
 
def get_sql_data(dsn, query):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    return pd.read_sql(query, conn)
    conn.close()

def load_to_hdfs(upload_dir, local_fname):
    HDFS_URL = hdfs_info["URL"]
    HDFS_BASE_PATH = hdfs_info["BASE_PATH"]
    HDFS_USER = hdfs_info["USER"]
    hdfs_upload_dir = HDFS_BASE_PATH + upload_dir
    hdfs_client = hdfs.InsecureClient(HDFS_URL, user=HDFS_USER)
    hdfs_client.makedirs(hdfs_upload_dir, permission=777)
    hdfs_client.upload(hdfs_upload_dir, local_fname,overwrite=True)

def delete_from_hdfs(file_or_dir):
    HDFS_URL = hdfs_info["URL"]
    HDFS_BASE_PATH = hdfs_info["BASE_PATH"]
    HDFS_USER = hdfs_info["USER"]
    delete_dir = HDFS_BASE_PATH + file_or_dir
    hdfs_client = hdfs.InsecureClient(HDFS_URL, user=HDFS_USER)
    hdfs_client.delete(delete_dir, recursive=True)

def download_from_hdfs(remote_dir, local_dir):
    HDFS_URL = hdfs_info["URL"]
    HDFS_BASE_PATH = hdfs_info["BASE_PATH"]
    HDFS_USER = hdfs_info["USER"]
    download_dir = HDFS_BASE_PATH + remote_dir
    hdfs_client = hdfs.InsecureClient(HDFS_URL, user=HDFS_USER)
    hdfs_client.download(download_dir, local_dir)

def load_to_s3(local_fname, remote_dir, remote_fname):
    s3_client = boto3.client('s3', aws_access_key_id=s3_info['ACCESS_KEY'],
                   aws_secret_access_key=decrypt_pwd(s3_info['SECRET_KEY'], key))
    s3_client.upload_file(local_fname, s3_info['BUCKET'],
                          remote_dir + '/' + remote_fname)

def load_from_s3_to_red(remote_dir, remote_fname, table_name, delimiter,
                        ignoreheader):
    bucket = s3_info['BUCKET']
    aws_access_key_id = s3_info['ACCESS_KEY']
    aws_secret_access_key = decrypt_pwd(s3_info['SECRET_KEY'], key)
    sqlquery = f'''
        copy {table_name}
        from 's3://{bucket}/{remote_dir}/{remote_fname}'
        credentials 'aws_access_key_id={aws_access_key_id};aws_secret_access_key={aws_secret_access_key}'
        delimiter as ',' ignoreheader {ignoreheader}
        gzip;'''
    run_sql('redshiftsys', sqlquery)

def delete_from_s3(remote_dir, remote_fname):
    s3_client = boto3.client('s3', aws_access_key_id=s3_info['ACCESS_KEY'],
                   aws_secret_access_key=decrypt_pwd(s3_info['SECRET_KEY'], key))
    s3_client.delete_object(Bucket=s3_info['BUCKET'],
                            Key=remote_dir + '/' + remote_fname)

def download_from_s3(remote_dir, remote_fname, local_fname):
    s3_client = boto3.client('s3', aws_access_key_id=s3_info['ACCESS_KEY'],
                   aws_secret_access_key=decrypt_pwd(s3_info['SECRET_KEY'], key))
    s3_client.download_file(s3_info['BUCKET'], remote_dir + '/' + remote_fname,
                            local_fname)

def sql_to_csv(dsn, query, fname, chunksize, separator, compress, header):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    cursor = conn.cursor()
    cursor.execute(query)
    col_names = tuple([column[0] for column in cursor.description])
    i = 0
    recs = 0
    try:
        os.remove(fname)
    except OSError:
        pass    
    while True:
            i += 1
            chunk_tuples = cursor.fetchmany(chunksize)
            if not chunk_tuples:
                break
            if compress:
                with gzip.open(fname, 'at', newline='') as f:
                  file_writer = csv.writer(f, delimiter = separator)
                  if header and i == 1:
                      file_writer.writerow(col_names)
                  file_writer.writerows(chunk_tuples)
            else:
                with open(fname, 'at', newline='') as f:
                  file_writer = csv.writer(f, delimiter = separator)
                  if header and i == 1:
                      file_writer.writerow(col_names)
                  file_writer.writerows(chunk_tuples)
            recs += len(chunk_tuples)   
    cursor.close()
    conn.close()
    return recs



def sql_to_csv_encoding(dsn, query, fname, chunksize, separator, compress, header, encodingselected):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    cursor = conn.cursor()
    cursor.execute(query)
    col_names = tuple([column[0] for column in cursor.description])
    i = 0
    recs = 0
    try:
        os.remove(fname)
    except OSError:
        pass    
    while True:
            i += 1
            chunk_tuples = cursor.fetchmany(chunksize)
            if not chunk_tuples:
                break
            if compress:
                with gzip.open(fname, 'at', newline='', encoding = encodingselected) as f:
                  file_writer = csv.writer(f, delimiter = separator)
                  if header and i == 1:
                      file_writer.writerow(col_names)
                  file_writer.writerows(chunk_tuples)
            else:
                with open(fname, 'at', newline='', encoding= encodingselected) as f:
                  file_writer = csv.writer(f, delimiter = separator)
                  if header and i == 1:
                      file_writer.writerow(col_names)
                  file_writer.writerows(chunk_tuples)
            recs += len(chunk_tuples)   
    cursor.close()
    conn.close()
    return recs


def index_marks(nrows, chunk_size):
    return range(1 * chunk_size, (nrows // chunk_size + 1) * chunk_size, chunk_size)
def split(dfm, chunk_size):
    indices = index_marks(dfm.shape[0], chunk_size)
    return np.split(dfm, indices)

def df_to_db_slow(dsn, df, table, chunksize, fast_execute_many=False):
    if dsn == 'impalasys':
        conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    else:
        conn = pyodbc.connect(f'DSN={dsn}', autocommit=False)
    cols = df.columns.to_list()
    qmarks = ('?,' * len(cols)).rstrip(',')
    insert_stmt = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({qmarks})"
    chunks = split(df, chunksize)
    i=0
    for df_chunk in chunks:
        i+=1
        cursor = conn.cursor()
        cursor.fast_executemany = fast_execute_many
        cursor.executemany(insert_stmt, df_chunk.values.tolist())
        cursor.commit()
        cursor.close()
    conn.close()

def sftp_listdir(credentials_dict, folder):
    host = credentials_dict["HOST"]
    user = credentials_dict["USER"]
    port = credentials_dict["PORT"]
    pwd = decrypt_pwd(credentials_dict["PWD"], key)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host, username=user, password=pwd, cnopts=cnopts, port=port) as sftp:
        return sftp.listdir(folder)

def sftp_upload(credentials_dict, fname_local, fname_remote):
    host = credentials_dict["HOST"]
    user = credentials_dict["USER"]
    port = credentials_dict["PORT"]
    pwd = decrypt_pwd(credentials_dict["PWD"], key)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host, username=user, password=pwd, cnopts=cnopts, port=port) as sftp:
        return sftp.put(fname_local, fname_remote)

def sftp_download(credentials_dict, fname_remote, fname_local):
    host = credentials_dict["HOST"]
    user = credentials_dict["USER"]
    port = credentials_dict["PORT"]
    pwd = decrypt_pwd(credentials_dict["PWD"], key)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host, username=user, password=pwd, cnopts=cnopts, port=port) as sftp:
        return sftp.get(fname_remote, fname_local)

def sftp_delete(credentials_dict, fname_remote):
    host = credentials_dict["HOST"]
    user = credentials_dict["USER"]
    port = credentials_dict["PORT"]
    pwd = decrypt_pwd(credentials_dict["PWD"], key)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host, username=user, password=pwd, cnopts=cnopts, port=port) as sftp:
        return sftp.remove(fname_remote)

def send_email(email_subject, sent_from, send_to, cc, bcc, content_plain,
               content_html, attach_dir, attach_files):
    msg = EmailMessage()
    msg['Subject'] = email_subject
    msg['From'] = sent_from
    msg['To'] = send_to
    msg['Cc'] = cc
    msg['Bcc'] = bcc
    #msg.add_header('reply-to', 'reporting@upstreamsystems.com')
    msg.set_content(content_plain)
    msg.add_alternative(content_html, subtype='html')
    
    if attach_dir is not None:
        for fname in attach_files:
            with open(attach_dir + '/' + fname, 'rb') as fp:
                msg.add_attachment(fp.read(),
                                    maintype='application',
                                    subtype='octet-stream',
                                    filename=fname)

    s = smtplib.SMTP('lhvmsrv107.lh.upstreamsystems.com')
    s.send_message(msg)
    s.quit()

def send_email_ext(email_subject, sent_from, send_to, cc, bcc, content_plain,
               content_html, attach_dir, attach_files):
    msg = EmailMessage()
    msg['Subject'] = email_subject
    msg['From'] = sent_from
    msg['To'] = send_to
    msg['Cc'] = cc
    msg['Bcc'] = bcc
    #msg.add_header('reply-to', 'reporting@upstreamsystems.com')
    msg.set_content(content_plain)
    msg.add_alternative(content_html, subtype='html')
    
    if attach_dir is not None:
        for fname in attach_files:
            with open(attach_dir + '/' + fname, 'rb') as fp:
                msg.add_attachment(fp.read(),
                                    maintype='application',
                                    subtype='octet-stream',
                                    filename=fname)
    user = bi_email_server["USER"]
    pwd = decrypt_pwd(bi_email_server["PWD"], key)
    s = smtplib.SMTP_SSL(bi_email_server["URL"])
    s.login(user, pwd)
    s.send_message(msg)
    s.quit()

def ftp_listdir(credentials_dict, folder):
    host = credentials_dict["HOST"]
    user = credentials_dict["USER"]
    pwd = decrypt_pwd(credentials_dict["PWD"], key)
   
    with FTP(host) as ftp:
        ftp.login(user=user, passwd=pwd)
        ftp.cwd(folder)
        return ftp.nlst()

# remote path should be like this /new_daily_report/2022-02-21-CRMnew.csv.gz
# local_path should be like this data/2022-02-21-CRMnew.csv.gz
def ftp_download(credentials_dict, remote_path, local_path):
    host = credentials_dict["HOST"]
    user = credentials_dict["USER"]
    pwd = decrypt_pwd(credentials_dict["PWD"], key)
   
    with FTP(host) as ftp, open(local_path, 'wb') as f:
        ftp.login(user=user, passwd=pwd)
        ftp.retrbinary(f'RETR {remote_path}', f.write)

def ftp_upload(credentials_dict, remote_path, local_path):
    host = credentials_dict["HOST"]
    user = credentials_dict["USER"]
    pwd = decrypt_pwd(credentials_dict["PWD"], key)
   
    with FTP(host) as ftp, open(local_path, 'rb') as f:
        ftp.login(user=user, passwd=pwd)
        ftp.storbinary(f'STOR {remote_path}', f)


# function to execute main() and send email upon failure
def exec_main(main, job_id, job_name, run_id, job_metadata,
              db_logging=True, send_to='reporting@upstreamsystems.com', send_cc=''):
    email_subject = 'Failed job - ' + job_id + ' / ' + job_name + ' / ' + run_id
    sent_from = 'BI @ Upstream <reporting@upstreamsystems.com>'
    send_bcc = ''

    try:
        log_screen('STARTED')
        if db_logging:
            log_db(job_id, job_name, run_id, 'STARTED', '', json.dumps(job_metadata))
        main()
        time.sleep(2)
        log_screen('FINISHED')
        if db_logging:
            log_db(job_id, job_name, run_id, 'FINISHED', '', json.dumps(job_metadata))
    except Exception as e:
        time.sleep(2)
        log_screen('FAILED')
        log_screen(str(e).replace("'",""))
        send_email(email_subject, sent_from, send_to, send_cc, send_bcc, str(e).replace("'",""),
                       str(e).replace("'",""),'','')
        if db_logging:
            log_db(job_id, job_name, run_id, 'FAILED', str(e).replace("'",""), json.dumps(job_metadata))

# gcloud functions for quick execution
def gc_listdir(gc_client, bucket, folder):
    file_list = []
    for blob in gc_client.list_blobs(bucket, prefix=folder):
      file_list.append(blob.name)
    return file_list

def gc_upload(gc_client, bucket, fname_remote, fname_local):
    blob = bucket.blob(fname_remote)
    blob.upload_from_filename(fname_local)

def gc_download(gc_client, bucket, fname_remote, fname_local):
    blob = bucket.blob(fname_remote)
    blob.download_to_filename(fname_local)

def gc_delete(gc_client, bucket, fname_remote):
    blob = bucket.blob(fname_remote)
    blob.delete()
