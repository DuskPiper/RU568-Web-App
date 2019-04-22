'''
@author: Ruiyu Zhang
@create: 2019.04.22
@intro.: Predicts stocks price with 3 techniques (Bayes, SVR, DNN)
'''
from os import cpu_count
import numpy as np
from sklearn.linear_model import BayesianRidge
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR

class Predictor:

    @staticmethod
    def bayes(train_x: np.ndarray, train_y: np.ndarray, pred_x: np.ndarray):
        '''predicts with Bayesian Regression.'''

        def calculate_score(feature_deg, train_x, train_y):
            '''constructs pipeline under Bayesian model and evaluates score.'''
            pipe = make_pipeline(
                StandardScaler(), 
                PolynomialFeatures(feature_deg), # featire_deg: 多项式的度
                BayesianRidge(normalize=False)
                )
            pipe.fit(train_x, train_y)
            return pipe.score(train_x, train_y)

        record = -1 # best score
        best_deg = -1 # degree to gain best score
        deg_range = 50 # degree range for testing

        '''find the best degree for PolynomialFeatures'''
        for deg in range(1, deg_range):
            score = calculate_score(deg, train_x, train_y)
            if score > record:
                record = score
                best_deg = deg

        '''build model, train with best deg, and predict'''
        pipe = make_pipeline(
            StandardScaler(),
            PolynomialFeatures(best_deg),
            BayesianRidge(normalize=False)
        )
        pipe.fit(train_x, train_y)
        return pipe.predict(pred_x)

    @staticmethod
    def SVR(train_x: np.ndarray, train_y: np.ndarray, pred_x: np.ndarray):
        '''predicts with SVM based Regression'''

        '''build model'''
        pipe = make_pipeline(
            StandardScaler(),
            SVR()
        )

        '''train with auto-var grad search'''
        model = GridSearchCV(
            pipe,
            param_grid={
                'svr__gamma': np.logspace(-2, 2, 5),
                'svr__C': [1e0, 1e1, 1e2, 1e3]
            },
            n_jobs=cpu_count(),
            cv=(train_x.shape[0] // 10),
            verbose=0
        )

        '''predict'''
        model.fit(train_x, train_y)
        return model.predict(pred_x)

    @staticmethod
    def dnn(train_x: np.ndarray, train_y: np.ndarray, pred_x: np.ndarray):
        '''predicts with TensorFlow based Neural Network'''
        return None
