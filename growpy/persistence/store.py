__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

from growpy.core.base import Singleton
from growpy.persistence.orm import *


class Store(Singleton):

    session = None

    def __init__(self):
        """
        strConnect = 'sqlite:///delta.db'

        """

        from growpy.main import BASE_DIRS, CFG
        if CFG.get('database', 'provider') == 'sqlite':
            strConnect = CFG.get('database', 'provider')
            strConnect += '://' + BASE_DIRS['db'] + '/'
            strConnect += CFG.get('database', 'dbstring')
        else:
            strConnect = CFG.get('database', 'provider')
            strConnect += '://'
            strConnect += CFG.get('database', 'dbstring')

        engine = create_engine(strConnect, echo=True)
        SessionFactory = sessionmaker(bind=engine)
        self.session = SessionFactory()
        Base.metadata.create_all(engine, checkfirst=True)
        self.session.commit()

    def save_node(self, Node):
        if Node is not None:
            self.session.add(Node)
            self.session.commit()

    def save_fs(self, node, fs):
        if node is not None and fs is not None:
            try:
                f = self.session.query(Filesystem).filter(Filesystem.fs_name == fs.get_name(),
                                                          Filesystem.node_id == node.node_id).first()
                if f is None:
                    f = Filesystem(node.node_id, fs.get_name(), fs.get_mount_on())
                    self.session.add(f)
                    self.session.commit()
                    self.session.refresh(f)
                    fs.set_id(f.fs_id)
                else:
                    fs.set_id(f.fs_id)
            except:
                f = Filesystem(node.node_id, fs.get_name(), fs.get_mount_on())
                self.session.add(f)
                self.session.commit()
                self.session.refresh(f)
                fs.set_id(f.fs_id)
                raise
            self.save_status(fs.get_id(), fs.get_size(), fs.get_used())

    def save_status(self, fs_id, size, used):
        status = Status(fs_id, size, used)
        self.session.add(status)
        self.session.commit()

    def get_node_list(self):
        return self.session.query(Node).all()


if __name__ == '__main__':
    store = Store()
