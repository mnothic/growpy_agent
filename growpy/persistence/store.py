__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

from growpy.persistence.orm import *
from growpy.core.config import config


class Store():

    def __init__(self):
        """
        strConnect = 'sqlite:///growpy.db'
        """
        if config['database']['provider'] == 'sqlite':
            str_connect = config['database']['provider']
            str_connect += ':///'
            str_connect += config['database']['dbstring']
        else:
            str_connect = config['database']['provider']
            str_connect += ':///'
            str_connect += config['database']['dbstring']

        ng = create_engine(str_connect, echo=config['core']['debug'])
        session_factory = sessionmaker(bind=ng)
        self.session = session_factory()
        Base.metadata.create_all(ng, checkfirst=True)
        self.session.commit()

    def save_node(self, node):
        if node is not None:
            self.session.add(node)
            self.session.commit()

    def save_fs(self, node, fs):
        if node is not None and fs is not None:
            try:
                f = self.session.query(Filesystem).filter(Filesystem.fs_name == fs.name,
                                                          Filesystem.node_id == node.node_id).first()
                if f is None:
                    f = Filesystem(node.node_id, fs.name, fs.mount_on)
                    self.session.add(f)
                    self.session.commit()
                    self.session.refresh(f)
                    fs.id = f.fs_id
                else:
                    fs.id = f.fs_id
            except:
                f = Filesystem(node.node_id, fs.name, fs.mount_on)
                self.session.add(f)
                self.session.commit()
                self.session.refresh(f)
                fs.id = f.fs_id
                raise
            self.save_status(fs.id, fs.size, fs.used)

    def save_status(self, fs_id, size, used):
        status = Status(fs_id, size, used)
        self.session.add(status)
        self.session.commit()

    def get_node_list(self):
        return self.session.query(Node).all()

    def get_fs_list(self, node):
        return self.session.query(Filesystem).filter(Filesystem.node_id == node.node_id).all()
