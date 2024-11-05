import paramiko
from etlfuncs import decrypt_pwd, key, log_screen
import time
import stat
import datetime

class SFTPConnection:
    """
    Auto-closeable wrapper for paramiko's SFTP client, meant to be used in `with` clauses.

    The returned object on `__enter__` is Paramiko's SFTP client. This class just makes sure that
    the connection is closed when exiting the with clause.
    """

    def __init__(self, credentials_dict):
        """
        Initialize an SSH connection with given host and credentials, then generate an SFTP client
        from paramiko library.

        Supports both password or private-public key authentication. If `PKEY` is given in the credentials dictionary,
        then the latter will be used, and any `PWD` attribute given will be considered to be the password needed
        by the privary key file.

        :param credentials_dict: credentials dictionary, expecting keys HOST, PORT, USER, and either PWD or PKEY
        :type credentials_dict: dict
        """
        self.host = credentials_dict["HOST"]
        self.user = credentials_dict["USER"]
        self.port = credentials_dict["PORT"]
        self.pwd = None
        self.pkey = None
        self.transport = None
        self.sftp = None        
        if "PWD" in credentials_dict:
            self.pwd = decrypt_pwd(credentials_dict["PWD"], key)

        if "PKEY" in credentials_dict:
            self.pkey = paramiko.rsakey.RSAKey.from_private_key_file(credentials_dict["PKEY"], password=self.pwd)

    def connect(self):
        """
        Establishes the SFTP connection.
        """
        self.transport = paramiko.Transport((self.host, int(self.port)))
        self.transport.set_keepalive(10)

        if self.pkey:
            self.transport.connect(hostkey=None, username=self.user, pkey=self.pkey)
        else:
            self.transport.connect(hostkey=None, username=self.user, password=self.pwd)

        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.sftp.sock.settimeout(900)

    def disconnect(self):
        """
        Closes the SFTP connection.
        """
        if self.sftp:
            self.sftp.close()
            self.sftp = None
        if self.transport:
            self.transport.close()
            self.transport = None
            
    def list_directories(self, path="."):
        """
        List all directories in the given path.
        """
        directories = []
        for item in self.sftp.listdir_attr(path):
            if stat.S_ISDIR(item.st_mode):
                directories.append(item.filename)
        return directories            
    
    def delete_old_files(self, path, days):
        """
        Recursively delete files older than the given number of days in the specified directory.
        """
        now = datetime.datetime.now()
        cutoff = now - datetime.timedelta(days=days)
    
        print(f"Current time: {now}")
        print(f"Cutoff time: {cutoff}")
    
        for item in self.sftp.listdir_attr(path):
            item_path = f"{path}/{item.filename}"
            file_mtime = datetime.datetime.fromtimestamp(item.st_mtime)
            print(f"Checking file: {item.filename}, Last modified: {file_mtime}")
            
            if stat.S_ISDIR(item.st_mode):
                # Recursively traverse directories
                self.delete_old_files(item_path, days)
            else:
                # Check the modification time of the file
                if file_mtime < cutoff:
                    print(f"Deleting file: {item_path}")
                    self.sftp.remove(item_path)
                else:
                    print(f"Skipping file: {item_path} (not old enough)")

def sftp_listdir(sftp_connection, folder):
    """
    List directory contents using an existing SFTP connection.
    """
    return sftp_connection.sftp.listdir(folder)

def sftp_upload(sftp_connection, fname_local, fname_remote):
    """
    Upload a file using an existing SFTP connection.
    """
    try:
        sftp_connection.sftp.put(fname_local, fname_remote)
    except (paramiko.SSHException, OSError) as e:
        log_screen(f"Error during SFTP upload: {e}")
        # Attempt to reconnect and retry the upload
        try:
            sftp_connection.disconnect()
            time.sleep(10)
            sftp_connection.connect()
            sftp_connection.sftp.put(fname_local, fname_remote)
        except Exception as e:
            log_screen("Failed to re-upload the file: " + str(e))
            raise

def sftp_download(sftp_connection, fname_remote, fname_local):
    """
    Download a file using an existing SFTP connection.
    """
    sftp_connection.sftp.get(fname_remote, fname_local)

def sftp_delete(sftp_connection, fname_remote):
    """
    Delete a file using an existing SFTP connection.
    """
    sftp_connection.sftp.remove(fname_remote)
