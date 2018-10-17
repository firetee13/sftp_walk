import paramiko
import os
paramiko.util.log_to_file('/tmp/sftp_data_transfer.log')
from stat import S_ISDIR

host = "sftp.example.com"
port = 22
username = "sftp_walk"
pkey = paramiko.RSAKey.from_private_key(open("./id_rsa")) #your private ssh key
remote_path = '/' #remote path to copy
local_path = os.getcwd()+"/data" # local path to copy to


def connect_to_sftp():
    #initiate the connection
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, pkey=pkey)
    sftp = paramiko.SFTPClient.from_transport(transport)




def get_sftp_data():
    # walk through the folder structure and create the generators

    def sftp_walk(remotepath):
        path = remotepath
        files = []
        folders = []
        for f in sftp.listdir_attr(remotepath):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        if files:
            yield path, files
        for folder in folders:
            new_path = os.path.join(remotepath, folder)
            for x in sftp_walk(new_path):
                yield x

    for path, files in sftp_walk(remote_path):
        # create the folder sturcture localy
        try:
            print "creating "+local_path+path
            os.makedirs(local_path+path)
        except:
            pass

    # copy the files from the sftp to the local folders
        for file in files:
            print "copying "+file
            sftp.get(path+"/"+file, local_path+path+"/"+file)

def main():
    connect_to_sftp()
    get_sftp_data()

if __name__=="__main__":
    main()
