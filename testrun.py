# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 06:08:09 2016

@author: o-4
"""
import pdb
import fparser as fp
import re
import subprocess
import os
import time
import sk_handler as skh
#import dbasehandler


def parsetest(parseOption):
    """
    ParseOptions:
    -------------
    COMMA_DL=0;
    SPACE_DL=1;
    LC_SINGLE=1
    LC_SEPERATE=2
    LC_SVM_A=3
    LC_SVM_B=4
    LC_SVM_C = 5
    """
    dname = '{}/data/init/adult/adultsmall.data'.format(os.getcwd())
    data = fp.parser(parseOption, dname, True, .25)
    target_input = data.convert_file()
    train_data,test_data = data.write_csv(target_input)
    X_train,y_train = data.split_last_column(train_data)
    X_test,y_test = data.split_last_column(test_data)
    sk = skh.sk_handler(X_train,y_train,X_test,y_test)
    duration, acc = sk.svm()
    dur2, acc2 = sk.clustering()
    pdb.set_trace()

def testSubProcc():
   pwd = os.getcwd()
   os.chdir('/home/o-4/Downloads/meta/pml/seq/libsvm-3.22/models')
   #Training time of the initial classisfication
   trainer = '/home/o-4/Downloads/meta/pml/seq/libsvm-3.22/svm-train'
   parsefile = '/home/o-4/Downloads/meta/pml/data/init/adult/adultsmall.data'
   comp = re.compile(r"""
                (.*)   #full directory path containing file
                ([/])  #slash at the end
                (\w*)  #filename
                ([.])  #trailing dot
                (\w*)  #file type
                """,re.VERBOSE)
   filename = filter(None,comp.split(parsefile))[2]
   trainfile ='/home/o-4/Downloads/meta/pml/data/init/adult/adultsmall.data.svmb.train'
   modelname = filename + ".model"
   modelfile = "/home/o-4/Downloads/meta/pml/seq/libsvm-3.22/models/adultsmall.model"
   dsetA = fp.parse_file(fp.LC_SVM_B,parsefile, fp.TP_TRUE, .25, fp.COMMA_DL)
   t0 = time.clock()
   subprocess.call(trainer + " " + trainfile + " " + modelname, shell=True)
   ptime = time.clock()-t0
   predictor = "/home/o-4/Downloads/meta/pml/seq/libsvm-3.22/svm-predict"
   testfile = "/home/o-4/Downloads/meta/pml/data/init/adult/adultsmall.data.svmb.test"
   outputname = filename + ".output"
   outputfile = "/home/o-4/Downloads/meta/pml/seq/libsvm-3.22/models/adultsmall.output"
   results=subprocess.check_output("{0} {1} {2} {3}".format(predictor, testfile, modelfile, outputfile), shell=True)
   pattern=r"(.*[aA]ccuracy\s*=\s*)(\d*[.]\d*)"
   x=filter(None,re.split(pattern,results))
   os.chdir(pwd)
