from ftplib import FTP
import os
from dotenv import load_dotenv

# Env vars
load_dotenv()

def download_folder(ftp:FTP, remote_path, local_path):
  try:
    filenames = []
    ftp.cwd(remote_path)
    ftp.dir(filenames.append)

    for filename in filenames:
      fileType = filename.split()[0][0]
      fileName = ' '.join(filename.split()[8:])
      remote_file = remote_path + '/' + fileName
      local_file = local_path + '/' + fileName

      if fileType == 'd':  # Es una carpeta
        if not os.path.exists(local_file):
          os.makedirs(local_file)
        download_folder(ftp, remote_file, local_file)
      else:  # Es un archivo
        with open(local_file, 'wb') as local_fp:
          ftp.retrbinary('RETR ' + remote_file, local_fp.write)
    print(f'Carpeta descargada: {remote_path}')
  except Exception as e:
    print(f'Error al descargar carpeta {remote_path}: {e}')
    print(f'Type: {filename.split()}')


# Folder remote and local
remote_directory = os.getenv('FTP_DIR')
local_directory = './config'

# Login
with FTP(os.getenv('FTP_HOST')) as ftp:
  ftp.login(user = os.getenv('FTP_USER'), passwd = os.getenv('FTP_PASS'))
  download_folder(ftp, remote_directory, local_directory)