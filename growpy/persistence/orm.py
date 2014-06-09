__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

from sqlalchemy import Column, ForeignKey, DateTime, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()


class Node(Base):
    __tablename__ = 'node'
    node_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    node_name = Column(String, unique=True, nullable=False)
    node_os_name = Column(String, unique=False, nullable=False)
    node_login = Column(String, unique=False, nullable=False)
    node_password = Column(String, unique=False, nullable=False)

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
    fs_name = Column(String, nullable=False)
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

    def __init__(self, fs_id, size, used, day=date.today()):
        self.fs_id = fs_id
        self.status_size = size
        self.status_used = used
        self.status_date = day
