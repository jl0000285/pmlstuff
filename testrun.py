# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 06:08:09 2016

@author: o-4
"""

import fparser as fp
import re
import subprocess
import os
import time
#import dbasehandler 


def parsetest(): 
    dname = '/home/o-4/Downloads/meta/pml/data/init/adult/adultsmall.test'   
    dsetA = fp.parse_file(fp.LC_SVM_B,dname, fp.TP_TRUE, .25, fp.COMMA_DL)
    #dbasehandler.add_data(dname,dset,len(dset[0]))
    
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