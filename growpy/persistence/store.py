__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

from growpy.persistence.model import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class Store():
    """
    This class contain the logic to persist the information
    Collected by collector and implement save and get methods
    """
    def __init__(self, db_url='sqlite:///growpy.db', debug=False):
        """
        Initialization of session factory
        """
        ng = create_engine(db_url, echo=debug)
        session_factory = sessionmaker(bind=ng)
        self.session = session_factory()
        """
        Created the Scheme if not exist, in the future move
        to exec into the Exception.
        """
        Base.metadata.create_all(ng, checkfirst=True)
        self.session.commit()

    def save_node(self, node):
        """
        Persist the node
        @param node:
        @return: None
        """
        if node is not None:
            self.session.add(node)
            self.session.commit()

    def save_fs(self, node, fs):
        """
        persist the fs by parent node
        @param node: Node instance
        @param fs: fs of node instance
        @return: None
        """
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
        """
        persiste the variable stats of fs by parent fs
        @param fs_id: fs id
        @param size: fs size
        @param used: fs utilization size
        @return: None
        """
        status = Status(fs_id, size, used)
        self.session.add(status)
        self.session.commit()

    def get_node_list(self):
        """
        This method return all instances of Node in a list of object
        Described by Model.Node
        @return: list of Node
        """
        return self.session.query(Node).all()

    def get_fs_list(self, node):
        """
        This method return all instances of the fs in the parent node
        @param node: parent node
        @return: list of Model.FS
        """
        return self.session.query(Filesystem).filter(Filesystem.node_id == node.node_id).all()
