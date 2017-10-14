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
    data_id = Column(Integer, primary_key = True)
    weighted_mean = Column(Float)
    standard_deviation = Column(Float)
    fpskew = Column(Float)
    kurtosis = Column(Float)
    information = Column(Float)
    
    def __repr__(self): 
        return '<data_set(name= {}, weighted_mean= {}, standard_deviation= {}, fpskew= {}, kurtosis= {}, .\
                information= {})>'.format(self.name,self.weighted_mean,self.standard_deviation,self.fpskew,self.kurtosis,self.information)
                
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
    data = relationship("data",backref="run")
    
    def __repr__(self):
        return '<run(run_id={},alg_name={},data_name={},train_time={},accuracy={})>'.format(self.run_id,self.alg.alg_name,self.data.data_name,self.train_time,self.accuracy)

def get_session():
    #Retrieve session object
    engine=create_engine('sqlite:///metabase.db')
    Session=sessionmaker(bind=engine)
    session=Session()
    return session
        

def dbInit(passw='Welcome07'):
    #Populate database with initial information 
    pass
                    
def data_init(session):
    for dirpath,dirname,filelist in os.walk('./data/init'):
        for filename in filelist:
            if(re.search(r".*[.]data",filename)):
                print "dirpath: {}, dirname: {}, filename: {}".format(dirpath,dirname,filename)
                dpath = '{}/{}'.format(dirpath,filename)
                dsetA, dsetB = fp.parse_file(fp.LC_SVM_B,dpath, fp.TP_TRUE, .25, fp.COMMA_DL)
                repo.add_dset(filename, dsetA, len(dsetA[0]),session)

def alg_class_init(session):
    class_A = alg_class(class_name='supervised')
    session.add(class_A)
    session.commit()    

def algorithms_init(session):
    algTypes= {
              'svm':'classifier'
              }
    for dirpath,dirname,filelist in os.walk('./seq'):
        for filename in filelist:
            if(re.search(r".*[-]train",filename)):   
                algname=filter(None,re.split(r"(.*)([-]train)",filename))[0]
                algpath='{}/{}'.format(dirpath,filename)
                session.add(algorithm(alg_name=algname,alg_path=algpath))           
    session.commit()        
    
def run_init(session):
    pass

def craftSystem():
    import create_db as cdb    
    cdb.create_tables(metadata)
    
def add_dset(dname, dset, nc, session):
    dwmean,ds_dev,dpskew,dkurt = mc.extractFeatures(dset,nc)
    minfo = 0
    dw,ds,dp,dk = dwmean[0], ds_dev[0], dpskew[0],dkurt[0]
    d_set = data_set(data_name=dname,
                     weighted_mean=dw,
                     standard_deviation=ds,
                     fpskew=dp,
                     kurtosis=dk,
                     information=minfo)
    session.add(d_set)
    session.commit()

def add_run():
     '''
     pwd = os.getcwd()
     os.chdir(dirpath2+'/models')
     #Training time of the initial classisfication 
     t0 = time.clock()
     subprocess.call(["./" + filename2 + " " + dpath ])
     ptime = time.clock()-t0
     predictor = "../{0}-predict".format(clfnames[0])
     testfile = dirpath + dnames[0] + ".test"
     modelfile = filename + ".model"
     outputfile = filename + ".output"
     results=subprocess.check_call("{0} {1} {2} {3}".format(predictor, testfile, modelfile, outputfile), shell=True)
     pattern=r"(.*[aA]ccuracy\s*=\s*)(\d*[.]\d*)"
     x=re.split(pattern,results)
     os.chdir(pwd)
     '''
     pass    