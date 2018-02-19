import time
import random
from sklearn.metrics import accuracy_score
import pdb

class sk_handler():
    """Class to help handle sk-learn methods
    SVM, Clusterer, Regression, Neural Networks, Bayesian
    """
    def __init__(self,X_train,y_train,X_test,y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def svm(self):
        """
        X = Data
        y = Labels
        per = percentage of data to withhold for testing (remainder will be used to train)
        """
        from sklearn.svm import SVC
        clf = SVC()
        #TODO: Explore possibility of using timeit as stopwatch
        t0 = time.time()
        clf.fit(self.X_train, self.y_train)
        t1 = time.time()
        duration = t1-t0
        result = list(clf.predict(self.X_test))
        acc = accuracy_score(result,self.y_test)
        #TODO: measure the accuracy of trained clf with test data here
        return duration, acc

    def clustering(self):
        from sklearn.cluster import KMeans
        import numpy as np
        X = np.array(self.X_train)
        num_clust = len(np.unique(self.y_train))
        Kmeans = KMeans(n_clusters=num_clust, random_state=0).fit(X)
        labs = list(Kmeans.labels_)
        duration = 0
        acc = 0
        nums = dict()
        for i in range(len(np.unique(self.y_train))):
            nums[i]=dict()
        for key in nums:
            for i in range(len(np.unique(self.y_train))):
                nums[key][i] = 0
        pdb.set_trace()
        for inx, item in enumerate(self.y_train):
            lab = labs[inx]
            nums[item][lab] += 1

        pdb.set_trace()
        return duration, acc

    def neural_network(self):
        from sklearn.neural_network import MLPClassifier
        X = np.arry(self.X_train)
        y = np.array(self.y_train)
        clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                       hidden_layer_sizes=(5, 2), random_state=1)
        t0 = time.time()
        clf.fit(X_train, y_train)
        t1 = time.time()
        result = list(clf.predict(self.X_test))
        duration = t1-t0
        acc = accuracy_score(result,self.y_test)
        return duration, acc

    def bayes(self):
        from sklearn.naive_bayes import GaussianNB
        X = np.array(self.X_train)
        y = np.array(self.y_train)
        gnb = GaussianNB()
        t0 = time.time()
        gnb.fit(X,y)
        t1 = time.time()
        result = list(gnb.predict(self.X_test))
        acc = accuracy_score(result,self.y_test)
        duration = t1-t0
        return duration, acc

    def regression():
        from sklearn import linear_model
        regr = linear_model.LinearRegression()
        t0 = time.time()
        regr.fit(self.X_train,slef.y_train)
        t1 = time.time()
        duration = t1-t0
        result = list(regr.predict(self.X_test))
        acc = accuracy_score(result,self.y_test)
        return duration, acc
