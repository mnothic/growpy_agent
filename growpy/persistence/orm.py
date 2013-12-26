__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

from sqlalchemy import Column, ForeignKey, DateTime, Integer, String
from sqlalchemy import create_engine, exc, exists
from sqlalchemy.orm import sessionmaker, synonym, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()


class Node(Base):
    __tablename__ = 'node'
    node_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    node_name = Column(String, unique=True, nullable=False)
    node_os_name = Column(String, unique=True, nullable=False)
    node_login = Column(String, unique=True, nullable=False)
    node_password = Column(String, unique=True, nullable=False)

    def __init__(self, name, os, login, passwd):
        self.node_name = name
        self.node_os_name = os
        self.node_login = login
        self.node_password = passwd

    filesystem = relationship("Filesystem",
                              order_by="Filesystem.fs_id",
                              back_populates="node")


class Filesystem(Base):
    __tablename__ = 'filesystem'
    fs_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    node_id = Column(Integer, ForeignKey('node.node_id'))
    fs_name = Column(String, unique=True, nullable=False)
    fs_pmount = Column(String, nullable=False)
    
    node = relationship('Node')

    def __init__(self, node_id, name, pmount):
        self.node_id = node_id
        self.fs_name = name
        self.fs_pmount = pmount

    status = relationship('Status',
                          back_populates='filesystem')

    
class Status(Base):
    __tablename__ = 'status'
    status_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    fs_id = Column(Integer, ForeignKey('filesystem.fs_id'))
    status_size = Column(Integer, nullable=False)
    status_used = Column(Integer, nullable=False)
    status_date = Column(DateTime, nullable=False)

    filesystem = relationship('Filesystem')

    def __init__(self, fs_id, size, used):
        self.fs_id = fs_id
        self.status_size = size
        self.status_used = used
        self.status_date = date.today()



if __name__ == '__main__':
    strConnect = 'sqlite:///delta.db'
    engine = create_engine(strConnect, echo=True)
    Session = sessionmaker(bind=engine)
    connection = Session()
    Base.metadata.create_all(engine)
    n = connection.query(Node).filter(Node.node_name=='localhost').one()
    if not n:
        n = Node('localhost', 'Linux', 'root', 'sinclave')
        connection.add(n)
        connection.commit()
        connection.refresh(n)
    try:
        fs = connection.query(Filesystem).filter(Filesystem.node_id==n.node_id,
                                                 Filesystem.fs_name=='/dev/mapper/vg_sys-lv_demo').all()
        fs = fs[0]
    except IndexError as e:
        print("{}".format(str(e)))
        fs = None

    if fs is None:
        fs = Filesystem(n.node_id, '/dev/mapper/vg_sys-lv_demo', '/demo')
        connection.add(fs)
        connection.commit()
        connection.refresh(fs)
    s = Status(fs_id=fs.fs_id, size=100, used=30)
    connection.add(s)
    connection.commit()
    for n in connection.query(Node).all():
        print(n.node_name)
