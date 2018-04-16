from sqlalchemy import Column, String, Integer, Float, MetaData, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import repo
import time
import re
import metaCollector as mc
import os
import subprocess
import fparser as fp

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class data_set(Base):
    __tablename__ = 'dataset'

    data_name = Column(String)
    data_path = Column(String)
    data_id = Column(Integer, primary_key = True)
    weighted_mean = Column(Float)
    standard_deviation = Column(Float)
    fpskew = Column(Float)
    kurtosis = Column(Float)
    information = Column(Float)

    def __repr__(self):
        return '<data_set(name= {}, path= {}, weighted_mean= {}, standard_deviation= {}, fpskew= {}, kurtosis= {}, .\
                information= {})>'.format(self.data_name,self.data_path,
                                          self.weighted_mean,self.standard_deviation,
                                          self.fpskew,self.kurtosis,self.information)

class alg_class(Base):
    __tablename__= 'alg_class'

    class_name = Column(String)
    class_id = Column(Integer, primary_key = True)

    def __repr__(self):
        return '<alg_class(id={}, name={})>'.format(self.class_id,self.class_name)

class algorithm(Base):
    __tablename__= 'algorithm'

    alg_name = Column(String)
    alg_path = Column(String)
    alg_id = Column(Integer, primary_key = True)
    class_id = Column(Integer, ForeignKey('alg_class.class_id'))

    def __repr__(self):
        return '<algorithm(alg_id={}, name={}, path={}, class_id={})>'.format(self.alg_id,self.alg_name,self.alg_path,self.class_id)

class run(Base):
    __tablename__= 'run'

    data_id = Column(Integer, ForeignKey('dataset.data_id'))
    alg_id = Column(Integer, ForeignKey('algorithm.alg_id'))
    run_id = Column(Integer, primary_key = True)
    train_time = Column(Float)
    accuracy = Column(Float)
    alg = relationship("algorithm",backref="run")
    data = relationship("data_set",backref="run")

    def __repr__(self):
        return '<run(run_id={},alg_name={},data_name={},train_time={},accuracy={})>'.format(self.run_id,self.alg.alg_name,self.data.data_name,self.train_time,self.accuracy)

def get_session():
    #Retrieve session object
    engine=create_engine('sqlite:///metabase.db')
    Session=sessionmaker(bind=engine)
    session=Session()
    return session

def craftSystem():
    import create_db as cdb
    cdb.create_tables(metadata)

def add_dset(dname,dpath, dset, nc, session):
    dwmean,ds_dev,dpskew,dkurt = mc.extractFeatures(dset,nc)
    minfo = 0
    dw,ds,dp,dk = dwmean[0], ds_dev[0], dpskew[0],dkurt[0]
    d_set = data_set(data_name=dname,
                     data_path=dpath,
                     weighted_mean=dw,
                     standard_deviation=ds,
                     fpskew=dp,
                     kurtosis=dk,
                     information=minfo)
    session.add(d_set)
    session.commit()

def add_run(data_id,alg_id,train_time,accuracy,session):
     n_run = run(data_id=data_id,
                 alg_id=alg_id,
                 train_time=train_time,
                 accuracy=accuracy)
     session.add(n_run)
     session.commit()

# Populates the algorithms table
def add_alg(alg_name,alg_path,class_id,session):
    n_algorithm = algorithm(alg_name=alg_name,
                            alg_path=alg_path,
                            class_id=class_id)
    session.add(n_algorithm)
    session.commit()


def add_algClass(class_name,session):
    n_class = alg_class(class_name=class_name)
    session.add(n_class)
    session.commit()
