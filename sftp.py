import paramiko
from helper import log

class SFTPServerClient:

    def __init__(self, hostname, port, username, password):
        self.__hostName = hostname
        self.__port = port
        self.__userName = username
        self.__password = password
        self.__SSH_Client = paramiko.SSHClient()

    def connect(self):
        try:
            self.__SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__SSH_Client.connect(
                hostname=self.__hostName,
                port=self.__port,
                username=self.__userName,
                password=self.__password,
                look_for_keys=False
            )
        except Exception as excp:
            log(excp)
            raise Exception(excp)
        else:
            log(f"Connected to server {self.__hostName}:{self.__port} as {self.__userName}.")
            print(f"Connected to server {self.__hostName}:{self.__port} as {self.__userName}.")

    def disconnect(self):
        self.__SSH_Client.close()
        log(f"{self.__userName} is disconnected to server {self.__hostName}: {self.__port}")
        print(f"{self.__userName} is disconnected to server {self.__hostName}: {self.__port}")

    def getListofFiles(self, remoteFilePath):
        files_list = []
        sftp_client = self.__SSH_Client.open_sftp()
        try:
            files_list = sftp_client.listdir(remoteFilePath)
            log(f"lists of files {files_list}")
            print(f"lists of files {files_list}")
        except:
            log(f"Error while getting the list of files")
            print(f"Error while getting the list of files")
        return files_list

    def downloadFiles(self, remoteFilePath, localFilePath):
        print(f"downloading file {remoteFilePath} to remote {localFilePath}")

        sftp_client = self.__SSH_Client.open_sftp()
        try:
            sftp_client.get(remoteFilePath, localFilePath)
        except FileNotFoundError as err:
            print(f"File: {remoteFilePath} was not found on the server")
        sftp_client.close()

    def uploadFiles(self, remoteFilePath, localFilePath):
        print(f"uploading file {localFilePath} to remote {remoteFilePath}")
        log(f"uploading file {localFilePath} to remote {remoteFilePath}")
        sftp_client = self.__SSH_Client.open_sftp()
        try:
            sftp_client.put(localFilePath, remoteFilePath)
        except FileNotFoundError as err:
            log(f"File {localFilePath} was not found on the local system")
            print(f"File {localFilePath} was not found on the local system")
        sftp_client.close()

    # def executeCommand(self, command):
    #     stdin, stdout, stderr = self.__SSH_Client.exec_command(command)
    #     print(stdout.readlines())
    #     print(stderr.readlines())


