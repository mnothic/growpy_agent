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

    @classmethod
    def main(self):
        store = Store()
        for n in store.get_node_list():
            fsc = FSCollector()
            if fsc.ssh_connect(n) is not None:
                fsc.collecting_node_info(n)


class FSCollector(object):
    _ssh = None
    _os_name = None

    def __init__(self):
        self._ssh = SSHClient()

    def ssh_connect(self, Node=None):
        """

        :param Node:
        :return:
        """
        try:
            self._ssh.set_missing_host_key_policy(AutoAddPolicy())
            self._ssh.connect(Node.node_name, username=Node.node_login, password=Node.node_password)
        except BadHostKeyException as ssh_error:
            print("SSH INFO: {} {}".format(Node.node_name, ssh_error))
            return None
        except AuthenticationException as ssh_error:
            print("SSH INFO: {} {}".format(Node.node_name, ssh_error))
            return None
        except SSHException as ssh_error:
            print("SSH INFO: {} {}".format(Node.node_name, ssh_error))
            return None
        except OSError as socketError:
            print("SSH INFO: {} {}".format(Node.node_name, socketError))
            return None
        return self

    def set_os_name(self):
        """
        parse OS name as http://en.wikipedia.org/wiki/Uname

        """
        os_list = []
        os_list.append('AIX')
        cmd = 'uname -s'
        try:
            stdout = self._ssh.exec_command(cmd, 16, 10, False)
            self._os_name = stdout.read()
            stdout.close()
        except SSHException as sshErr:
            print("ssh connection error {}".format(sshErr))

    def collecting_node_info(self, node):

        if node.node_os_name == 'HP-UX':
            self.set_fs_list(node, self.parse_hpux_stdout())
        else:
            self.set_fs_list(node, self.parse_stdout())

    def parse_stdout(self):
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
        fs_list = []
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
                if not self._fs_exist(fs_list, fs):
                    fs_list.append(fs)
            i += 1
        return fs_list

    def parse_hpux_stdout(self):
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
        fs_list = []
        i = 0
        for rs in df.split('\n'):
            row = rs.split()
            if i > 0 and len(row) > 0:
                fs = FS(row[0], row[5], row[1], row[2])
                if not self._fs_exist(fs_list, fs):
                    fs_list.append(fs)
            i += 1
        return fs_list

    def _fs_exist(self, fs_list, fs):
        """
        Check for a existent fs
        """
        if len(fs_list) == 0:
            return False

        for fs_instance in fs_list:
            if fs_instance.get_name() == fs.get_name():
                return True

        return False

    def set_fs_list(self, node, fs_list):
        for fs in fs_list:
            store = Store()
            store.save_fs(node, fs)

    def __del__(self):
        self._ssh.close()
