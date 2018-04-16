# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 22:44:00 2016

@author: o-4
"""

from __future__ import print_function
import dbasehandler as dbh
import mysql.connector
import metaCollector as mc
import os
import fparser as fp
import re
import time
import subprocess
from mysql.connector import errorcode
import repo
import pdb

def dbInit():
    repo.craftSystem()
    session = repo.get_session()
    print("Performing data init")
    dbh.data_init(session)
    print("Performing Alg Class Init")
    dbh.alg_class_init(session)
    print("Perfomring Algorithms init")
    dbh.algorithms_init(session)
    print("Performing Runs init")
    dbh.run_init(session)

def data_init(session):
    for dirpath,dirname,filelist in os.walk('./data/init'):
        for filename in filelist:
            if(re.search(r".*[.]data",filename)):
                print ("dirpath: {}, dirname: {}, filename: {}"
                       .format(dirpath,dirname,filename))
                dpath = '{}/{}'.format(dirpath,filename)
                data = fp.parser(fp.LC_SINGLE,dpath,False,0)
                full_set = data.convert_file()
                repo.add_dset(filename, dpath, full_set, len(full_set[0]),session)

def alg_class_init(session):
    class_A = repo.alg_class(class_name='supervised')
    session.add(class_A)
    session.commit()

def algorithms_init(session):
    algTypes= {
              'svm':('sk.svm','supervised'),
              'clustering':('sk.clustering','supervised'),
              'neural_network':('sk.neural_network','supervised'),
              'bayes':('sk.bayes','supervised'),
              'regression':('sk.regression','supervised')
              }
    for key in algTypes:
        class_id = session.query(repo.alg_class).\
            filter_by(class_name=algTypes[key][1]).first()
        class_id = class_id.class_id
        repo.add_alg(key,algTypes[key][0],class_id,session)

def run_init(session):
    import sk_handler as skh
    d_sets = session.query(repo.data_set).all()
    algs = session.query(repo.algorithm).all()
    for d_set in d_sets:
        data_id = d_set.data_id
        data = fp.parser(fp.COMMA_DL,d_set.data_path,
                         fp.TP_TRUE,per=.25)
        target_input = data.convert_file()
        train_data,test_data = data.write_csv(target_input)
        X_train,y_train = data.split_last_column(train_data)
        X_test,y_test = data.split_last_column(test_data)
        sk = skh.sk_handler(X_train,y_train,X_test,y_test)
        for alg  in algs:
            alg_id = alg.alg_id
            evstring = '{}()'.format(alg.alg_path)
            durr,acc = eval(evstring)
            repo.add_run(data_id,alg_id,durr,acc,session)

def print_databases():
    cnx = mysql.connector.connect(user='root', password='Welcome07', host='127.0.0.1')
    cursor = cnx.cursor()
    cursor.execute('show databases')
    for i in cursor:
        print (i)
    cnx.close()
