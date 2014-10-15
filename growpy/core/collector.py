__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"
from threading import Thread
from paramiko import SSHClient, AutoAddPolicy
from paramiko import SSHException, BadHostKeyException, AuthenticationException
from growpy.persistence.store import Store
from growpy.core.base import FS, AESCipher
from growpy.core.config import config


class Collector():

    @classmethod
    def main(cls):
        store = Store(dburl=config['database']['dburl'])
        for n in store.get_node_list():
            fsc = FSCollector(n, AESCipher(config['core']['aes_key']))
            fsc.start()


class FSCollector(Thread):

    def __init__(self, node, cypher):
        self.cypher = cypher
        self.node = node
        self.node.node_password = self.cypher.decrypt(self.node.node_password)
        self._ssh = SSHClient()
        Thread.__init__(self, name=node.node_name)

    def run(self):
        if self.ssh_connect() is not None:
            self.collecting_node_info()

    def ssh_connect(self):
        """ This wrap the ssh connection process and handle the errors
        return self to chain syntax.
        :param: None
        :return: self
        """
        try:
            self._ssh.set_missing_host_key_policy(AutoAddPolicy())
            self._ssh.connect(self.node.node_name, username=self.node.node_login, password=self.node.node_password)
        except BadHostKeyException as ssh_error:
            print("SSH INFO: {} {}".format(self.node.node_name, ssh_error))
            return None
        except AuthenticationException as ssh_error:
            print("SSH INFO: {} {}".format(self.node.node_name, ssh_error))
            return None
        except SSHException as ssh_error:
            print("SSH INFO: {} {}".format(self.node.node_name, ssh_error))
            return None
        except OSError as ssh_error:
            print("SSH INFO: {} {}".format(self.node.node_name, ssh_error))
            return None
        return self

    def collecting_node_info(self):
        """ take parsed node information stat and set into persistence broker
        """
        self.set_fs_list(self.parse_stdout())

    def parse_stdout(self):
        """ this function parse all standard df output and return the a tokenized list
        :param: None
        :return: list
        """
        if self.node.node_os_name == 'HP-UX':
            cmd = 'bdf'
        else:
            cmd = 'df'
        df = None
        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)
            df = stdout.read().decode('utf-8')
            self._ssh.close()
        except SSHException:
            print('ssh error')
        fs_list = []
        i = 0
        for rs in df.split('\n'):
            row = rs.split()
            try:
                if 'Filesystem' in row[0][0:11]:
                    continue
            except IndexError:
                pass
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

    @staticmethod
    def _fs_exist(fs_list, fs):
        """
        Check for a existent fs
        """
        if len(fs_list) == 0:
            return False
        for fs_instance in fs_list:
            if fs_instance.name == fs.name:
                return True
        return False

    def set_fs_list(self, fs_list):
        if config['core']['debug']:
            print("INFO: Saving FS stats on ", self.node.node_name)
        for fs in fs_list:
            store = Store()
            store.save_fs(self.node, fs)
