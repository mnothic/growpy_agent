__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko import SSHException
from paramiko import BadHostKeyException
from paramiko import AuthenticationException
from growpy.persistence.store import Store
from growpy.core.base import FS


class Collector():

    def main(self):
        store = Store()
        for n in store.get_node_list():
            fsc = FSCollector()
            if fsc.sshConnect(n) is not None:
                fsc.collectingNodeInfo(n)


class FSCollector(object):
    _ssh = None
    _OSName = None

    def __init__(self):
        self._ssh = SSHClient()

    def sshConnect(self, Node=None):
        """

        :param Node:
        :return:
        """
        try:
            self._ssh.set_missing_host_key_policy(AutoAddPolicy())
            self._ssh.connect(Node.node_name, username=Node.node_login, password=Node.node_password)
        except BadHostKeyException as sshErr:
            print("SSH INFO: {} {}".format(Node.node_name, sshErr))
            return None
        except AuthenticationException as sshErr:
            print("SSH INFO: {} {}".format(Node.node_name, sshErr))
            return None
        except SSHException as sshErr:
            print("SSH INFO: {} {}".format(Node.node_name, sshErr))
            return None
        except OSError as socketError:
            print("SSH INFO: {} {}".format(Node.node_name, socketError))
            return None
        return self

    def setOSName(self):
        """
        parse OS name as http://en.wikipedia.org/wiki/Uname

        """
        OSList = []
        OSList.append('AIX')
        cmd = 'uname -s'
        try:
            stdout = self._ssh.exec_command(cmd, 16, 10, False)
            self._OSName = stdout.read()
            stdout.close()
        except SSHException as sshErr:
            print("ssh connection error {}".format(sshErr))

    def collectingNodeInfo(self, node):

        if node.node_os_name == 'HP-UX':
            self.setFSList(node, self.parseHPUXOut())
        else:
            self.setFSList(node, self.parseStdOut())

    def parseStdOut(self):
        """
        parse all standard df output
        :param: output
        :return: list
        """
        df = None
        cmd = 'df'
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            df = stdout.read().decode('utf-8')
        except SSHException:
            print('ssh error')
        fsList = []
        i = 0
        for rs in df.split('\n'):
            row = rs.split()
            if 'Filesystem' in row[0][0:11]:
                continue
            if len(row) > 0:
                if len(row) == 1:
                    aux = row[0]
                elif len(row) == 5:
                    fs = FS(aux, row[4], row[0], row[1])
                else:
                    fs = FS(row[0], row[5], row[1], row[2])
                if not self._existFS(fsList, fs):
                    fsList.append(fs)
            i += 1
        return fsList

    def parseHPUXOut(self):
        """
        TODO: implement method by OS output hpux has different output.
        parse double lines with large paths
        """
        df = None
        cmd = 'bdf'
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            df = stdout.read().decode('utf-8')
        except SSHException:
            print('ssh error')
        fsList = []
        i = 0
        for rs in df.split('\n'):
            row = rs.split()
            if i > 0 and len(row) > 0:
                fs = FS(row[0], row[5], row[1], row[2])
                if not self._existFS(fsList, fs):
                    fsList.append(fs)
            i += 1
        return fsList

    def _existFS(self, fsList, fs):
        """
        Check for a existent fs
        """
        if len(fsList) == 0:
            return False

        for fsInst in fsList:
            if fsInst.get_name() == fs.get_name():
                return True

        return False

    def setFSList(self, node, FSList):
        for fs in FSList:
            store = Store()
            store.save_fs(node, fs)

    def __del__(self):
        self._ssh.close()
