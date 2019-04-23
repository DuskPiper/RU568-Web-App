'''
@author: Ruiyu Zhang
@create: 2019.04.22
@intro.: Predicts stocks price with 3 techniques (Bayes, SVR, DNN)
'''
from os import cpu_count
from random import sample
import numpy as np
import tensorflow as tf
from sklearn.linear_model import BayesianRidge
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR

class Predictor:
    '''
    collection of predictors
    all predictor input x&y shape: (-1, 1), dtype = float
    '''

    @staticmethod
    def bayes(train_x: np.ndarray, train_y: np.ndarray, pred_x: np.ndarray):
        '''predicts with Bayesian Regression (sklearn.linear_model.BayesianRidge()'''

        train_y = np.ravel(train_y, order='C')

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

        # find the best degree for PolynomialFeatures
        for deg in range(1, deg_range):
            score = calculate_score(deg, train_x, train_y)
            if score > record:
                record = score
                best_deg = deg

        # build model, train with best deg, and predict
        pipe = make_pipeline(
            StandardScaler(),
            PolynomialFeatures(best_deg),
            BayesianRidge(normalize=False)
        )
        pipe.fit(train_x, train_y)
        return pipe.predict(pred_x)

    @staticmethod
    def SVR(train_x: np.ndarray, train_y: np.ndarray, pred_x: np.ndarray):
        '''predicts with SVM based Regression (sklearn.svm.SVR())'''

        train_y = np.ravel(train_y, order='C')

        # build model
        pipe = make_pipeline(
            StandardScaler(),
            SVR()
        )

        # train with auto-var grad search
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

        # predict
        model.fit(train_x, train_y)
        return model.predict(pred_x)

    @staticmethod
    def DNN(train_x: np.ndarray, train_y: np.ndarray, pred_x: np.ndarray):
        '''predicts with TensorFlow based Neural Network (DNNRegressor.Estimator())'''

        train_y = np.ravel(train_y, order='C')

        STEPS = 1000
        PRICE_NORM_FACTOR = 10
        SECONDS_OF_ONE_DAY = 86400
        SHUFFLE_TIMES = 1000 # shuffle multiple times (likely > dataset size) to ensure enough mixture
        DEBUG = True
        
        # preprocess
        pred_x = train_x[0] - pred_x
        train_x = train_x[0] - train_x
        pred_x /= SECONDS_OF_ONE_DAY
        train_x /= SECONDS_OF_ONE_DAY

        rate = 1 # typically 0.7
        l1 = sample(list(range(train_x.shape[0])), int(len(train_x) * rate))
        x_trainset = train_x[l1]
        y_trainset = train_y[l1]
        l2 = list(set(list(range(train_x.shape[0]))) - set(l1))
        x_testset = train_x[l2]
        y_testset = train_y[l2]

        x_train_dist = {"time": x_trainset}
        x_test_dist = {"time": x_testset}
        x_dist = {"time": pred_x}

        train = tf.data.Dataset.from_tensor_slices((dict(x_train_dist), y_trainset))
        test = tf.data.Dataset.from_tensor_slices((dict(x_test_dist), y_testset))
        to_predict_x = tf.data.Dataset.from_tensor_slices(dict(x_dist))

        def normalize_price(features, labels):
            return features, labels / PRICE_NORM_FACTOR
        train = train.map(normalize_price)
        test = test.map(normalize_price)

        # build training and evaluation input_functions
        def input_train():
            return (train.shuffle(SHUFFLE_TIMES).batch(128) # shuffle
                    .repeat().make_one_shot_iterator().get_next()) # Repeat forever

        def input_test():
            return (test.shuffle(SHUFFLE_TIMES).batch(128)
                    .make_one_shot_iterator().get_next())

        # build Neural Network model
        model = tf.estimator.DNNRegressor(
            hidden_units=[20, 20],
            feature_columns=tf.feature_column.numeric_column(key="time"),
            optimizer=tf.train.ProximalAdagradOptimizer(
                learning_rate=0.3,
                l1_regularization_strength=0.001
            )
        )

        # train
        model.train(input_fn=input_train(), steps=STEPS)
        prediction = model.predict(input_fn=to_predict_x.make_one_shot_iterator().get_next())
        pred_list = list(prediction)

        # evaluate
        eval_res = model.evaluate(input_fn=input_test())
        ave_loss = eval_res["average_loss"]

        # debug
        if DEBUG:
            print(pred_list[0]['predictions'][0] * PRICE_NORM_FACTOR)
            print("\n" + 80 * "*")
            print("\nRMS err on testset: ${:.0f}".format(PRICE_NORM_FACTOR * average_loss ** 0.5),
                  end="\n")

        return pred_list[0]['predictions'][0] * PRICE_NORM_FACTOR

    @staticmethod
    def _calculateEMA(val: np.ndarray) -> np.float_:
        '''calculates Exponential Moving Average, DOES NOT PREDICT'''

        if val.size < 10: return np.float_(-1)
        ret = sum(val[:10]) / 10
        multiplier = 2 / (10 + 1)
        for v in val[10:]:
            ret = (v - ret) * multiplier + ret
        return ret


if __name__ == "__main__":
    '''driver codes as sample & debugger'''
    # preparation
    tf.logging.set_verbosity(tf.logging.INFO) # setup tf logs

    # generate test data
    import random
    train_x = np.array([float(i) for i in range(30)]).reshape(-1, 1)
    train_y = np.array([float(i) * 10 + random.randint(1, 9) for i in range(30)]).reshape(-1, 1)
    pred_x = np.array([float(i) for i in range(30, 34)]).reshape(-1, 1)

    # test
    print(train_x.reshape(1, -1))
    print(train_y.reshape(1, -1))
    print(pred_x.reshape(1, -1))

    print("BAYES:")
    print(Predictor.bayes(train_x, train_y, pred_x))

    print("SVR:")
    print(Predictor.SVR(train_x, train_y, pred_x))

    print("DNN:")
    print(Predictor.DNN(train_x, train_y, pred_x))

