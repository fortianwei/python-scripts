#!/usr/bin/env python

__AUTHER__ = 'tianwei'
__DATE__ = '2014-11-07'

import os
import os.path
import paramiko
import zipfile


_SERVER_ADDRESS = "172.16.73.103"
_USER_NAME = "tianwei"
_PASSWORD = "tianweitianwei;"

_DOPPIO_ROOT_PATH = "/home/tianwei/study/doppio"
_DOPPIO_ROOT_PATH_ON_SERVER = "/usr/local/webserver/nodejs/doppio/build"
_DOPPIO_ROOT_PATH_ON_SERVER_WITHOUT_BUILD = "/usr/local/webserver/nodejs/doppio"
_SERVER_HOME_PATH = "/home/tianwei"
_RELEASE_PATH = _DOPPIO_ROOT_PATH + "/build/release/"
#j2me classes
_VENDOR_MICROEDITION_PATH = _DOPPIO_ROOT_PATH + "/vendor/classes/javax/microedition/"
#sgt login js/css/jpg...
_SGT_LOGIN_PATH = _DOPPIO_ROOT_PATH + "/vendor/sgt-login/"
_DIST_PATH = _DOPPIO_ROOT_PATH + "/dist/"

_EXCLUDE_DIRS_BASE = (".git", ".svn", ".idea")
_EXCLUDE_DIRS = _EXCLUDE_DIRS_BASE + ("games", "upload", "temp", "classes", "vendor")
_EXCLUDE_FILES = ("games.json", "listings.json")


paramiko.util.log_to_file('/tmp/publish_doppio.log')

class PublishDoppio:
    """
    publish doppio to server.
    step 1: zip the files
    step 2: transfer files(via scp)
    step 3: login server & unzip files & restart node.js server(need sudo)
    """

    def __init__(self):
        self.timestamp = self.getTimestamp()
        if not os.path.isdir(_DIST_PATH):
            os.mkdir(_DIST_PATH)
        self.releaseFileName = "release-"+self.timestamp+".zip"
        self.vendorFileName = "vendor-"+self.timestamp+".zip"

    def start(self):
        self.compressFiles()
        self.doSCP()
        self.manipulateServer()

    def compressFiles(self):
        print "compress files..."
        self.compressReleaseFile()
        self.compressVendorFile()

    def compressReleaseFile(self):
        """
        compress doppio release directory,need to exclude some files/directories
        :return: None
        """
        destFilePath = os.path.join(_DIST_PATH, self.releaseFileName)

        self.makeZipFile(_RELEASE_PATH,
                         destFilePath, _EXCLUDE_DIRS, _EXCLUDE_FILES)

    def compressVendorFile(self):
        destFilePath = os.path.join(_DIST_PATH, self.vendorFileName)
        self.makeZipFile((_VENDOR_MICROEDITION_PATH, _SGT_LOGIN_PATH),
                         destFilePath, _EXCLUDE_DIRS_BASE, ())

    def doSCP(self):
        print "copy zip files to server..."
        scp = paramiko.Transport((_SERVER_ADDRESS, 22))
        scp.connect(username=_USER_NAME,password=_PASSWORD)

        def asCallback(fileName):
            def wrapper(func):
                print "copy file ", fileName, "start..."

                def _wrapper(current, total):
                    print fileName, ":(total=", total, ") (current=", current, ")"
                return _wrapper
            return wrapper

        @asCallback(self.releaseFileName)
        def releaseFileCallback():
            pass

        @asCallback(self.vendorFileName)
        def vendorFileCallback():
            pass

        with paramiko.SFTPClient.from_transport(scp) as sftp:
            sftp.put(os.path.join(_DIST_PATH, self.releaseFileName),
                     _SERVER_HOME_PATH+os.sep+self.releaseFileName, callback =releaseFileCallback)
            sftp.put(os.path.join(_DIST_PATH, self.vendorFileName),
                     _SERVER_HOME_PATH+os.sep+self.vendorFileName, callback=vendorFileCallback)

        print "Copy files complete."

    def manipulateServer(self):

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(_SERVER_ADDRESS, port=22, username=_USER_NAME, password=_PASSWORD, compress=True)

        sshShell = ssh.invoke_shell()
        import time
        time.sleep(0.1)
        self.loginWithSudo(sshShell)

        #step1: backup old release directory
        #step2: unzip files
        #step3: generate lisints.json
        #step4: kill old nodejs service process
        #step5: start nodejs service

        cmds = []

        #step1: eg. tar zcf /usr/local/webserver/nodejs/doppio/build/release-bak-20141107
        # /usr/local/webserver/nodejs/doppio/build/release
        cmdBackup = "tar zcf "+_DOPPIO_ROOT_PATH_ON_SERVER+os.sep+"release-bak-"+self.timestamp+".tar"+\
                    " "+_DOPPIO_ROOT_PATH_ON_SERVER+os.sep+"release"
        cmds.append(cmdBackup)

        #step2: eg. unzip -o /home/tianwei/release-20141107.zip -d /usr/local/webserver/nodejs/doppio/build/
        cmdUnzip = 'unzip -o '+_SERVER_HOME_PATH+os.sep+self.releaseFileName+' -d '+ _DOPPIO_ROOT_PATH_ON_SERVER+os.sep
        cmds.append(cmdUnzip)

        #step3: eg. cd /usr/local/webserver/nodejs/doppio/build/release &
        # coffee ../../tools/gen_dir_listings.coffee >./browser/listings.json
        cmdGenerateListingsJson = 'cd '+_DOPPIO_ROOT_PATH_ON_SERVER+'/release && ' \
                                  'coffee ../../tools/gen_dir_listings.coffee >./browser/listings.json'
        cmds.append(cmdGenerateListingsJson)

        #step4: eg. ps ax |grep tools/server.coffee | awk '{print $1}' |xargs kill -9
        cmdKillDoppioServiceProcess = "ps ax |grep tools/server.coffee | awk '{print $1}' |xargs kill -9"
        cmds.append(cmdKillDoppioServiceProcess)

        #step5: eg. nohup /usr/local/webserver/nodejs/doppio/tools/server.coffee --release &
        cmdStartDoppioService = 'nohup '+_DOPPIO_ROOT_PATH_ON_SERVER_WITHOUT_BUILD+'/tools/server.coffee --release &'
        cmds.append(cmdStartDoppioService)

        for cmd in cmds:
            self.runCommandOnServer(sshShell,cmd)


        ssh.close()

    def loginWithSudo(self,sshShell):
        sshShell.send("sudo -i \n")
        buff = ''
        while not buff.endswith('password for '+_USER_NAME+': '):
            resp = sshShell.recv(9999)
            buff += resp
        sshShell.send(_PASSWORD)
        sshShell.send("\n")

        while not buff.endswith('# '):
            resp = sshShell.recv(9999)
            buff += resp

    def runCommandOnServer(self,sshShell,command):
        """
        Be sure the ssh is ok first!

        :param sshShell: ssh shell
        :param command: command to be executed
        :return: output buff of this command bing executed on server
        """
        print "run command :",command
        sshShell.send(command)
        sshShell.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = sshShell.recv(9999)
            buff += resp
        print buff
        print "run command :", command, ",complete."

    def makeZipFile(self,dirPaths, fileName, excludeDirs=(), excludeFiles=()):
        """
        :param dirPaths: src directories , maybe more than one
        :param fileName: destination zip file name
        :param excludeDirs: exclude directory names
        :param excludeFiles: exclude files name
        :return: None

        eg.
        makeZipFile("/home/tianwei/study/doppio/browser",
        "/home/tianwei/somefile.zip",(".svn",".idea"),("123.html"))

        """

        if not ((type(dirPaths) is tuple) or (type(dirPaths) is list) or (type(dirPaths) is set)):
            """
            if dirPaths is not tuple/list/set,the for loop will split /home/tianwei/xxx to
            directories '/'  'h'  'o'   'm'   'e'  '/'  't' and so on
            """
            dirPaths = [dirPaths]

        fileList = []
        for dirPath in dirPaths:
            if os.path.isfile(dirPath):
                fileList.append(dirPath)
            else:
                #need to exclude some directories/files,DO NOT use os.walk/os.path.walk
                def filterWalk(filePath):
                    # print "filePath:", filePath
                    if os.path.isfile(filePath):
                        fileList.append(filePath)
                    else:
                        for f in [x for x in os.listdir(filePath) if not
                        ((os.path.isdir(os.path.join(filePath, x)) and (x in excludeDirs)) or
                             (os.path.isfile(os.path.join(filePath, x)) and (x in excludeFiles)))]:

                            filterWalk(os.path.join(filePath, f))

                filterWalk(dirPath)
                # print "fileList:",fileList

        with zipfile.ZipFile(fileName, "w", zipfile.zlib.DEFLATED) as zf:
            for f in fileList:
                orcname = f[len(_DOPPIO_ROOT_PATH):]
                if str(orcname).startswith("/vendor"):
                    orcname = "/release" + orcname
                else:
                    orcname = orcname[len("/build"):]

                zf.write(f, orcname)
                # print "name:",orcname

    def getTimestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d")



if __name__ == '__main__':
    publishDoppio = PublishDoppio()
    publishDoppio.start()
