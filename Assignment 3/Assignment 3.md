# <center>Web Application Assignment 3</center>

<center>Ruiyu Zhang || rz213 2019.02.16</center>



## Project README

This project is based on Python3, please make sure that proper csv data kept in "./data/" and that Numpy is available for your Python version. Then run "bayesian_curve_fitting.py" in terminal at Project directory.

```bash
$ cd Project
$ python bayesian_curve_fitting.py
```



## Data and Tests

In this assignment, a total of 10 real stocks datasets covering several tech giants have been chosen for test. The output result of the program is copied below for convenience.

```pseudocode
-----FB-hist-2016-2017 Summary----------
Predicted Val   : 120.2975
Actual Val      : 120.9000
Range Predction : [119.3870, 121.2079]
Absolute Error  : 0.6025
Relative Error  : 0.4984%
----------------------------------------


-----MSFT-03-02-2017 Summary------------
Predicted Val   : 64.4717
Actual Val      : 64.4700
Range Predction : [63.5551, 65.3884]
Absolute Error  : 0.0017
Relative Error  : 0.0027%
----------------------------------------


-----CCF-hist-2016-2017 Summary---------
Predicted Val   : 87.3372
Actual Val      : 89.2500
Range Predction : [86.4268, 88.2476]
Absolute Error  : 1.9128
Relative Error  : 2.1432%
----------------------------------------


-----YHOO-03-02-2017 Summary------------
Predicted Val   : 46.3315
Actual Val      : 46.2700
Range Predction : [45.4148, 47.2482]
Absolute Error  : 0.0615
Relative Error  : 0.1328%
----------------------------------------


-----CCF-03-02-2017 Summary-------------
Predicted Val   : 93.9848
Actual Val      : 93.9500
Range Predction : [93.0670, 94.9027]
Absolute Error  : 0.0348
Relative Error  : 0.0371%
----------------------------------------


-----FB-03-02-2017 Summary--------------
Predicted Val   : 136.7452
Actual Val      : 136.8776
Range Predction : [135.8274, 137.6631]
Absolute Error  : 0.1324
Relative Error  : 0.0967%
----------------------------------------


-----MSFT-hist-2016-2017 Summary--------
Predicted Val   : 63.1379
Actual Val      : 62.9500
Range Predction : [62.2274, 64.0483]
Absolute Error  : 0.1879
Relative Error  : 0.2985%
----------------------------------------


-----GOOG-03-02-2017 Summary------------
Predicted Val   : 832.8301
Actual Val      : 832.1900
Range Predction : [831.9134, 833.7468]
Absolute Error  : 0.6401
Relative Error  : 0.0769%
----------------------------------------


-----YHOO-hist-2016-2017 Summary--------
Predicted Val   : 36.7166
Actual Val      : 36.6100
Range Predction : [35.8062, 37.6271]
Absolute Error  : 0.1066
Relative Error  : 0.2912%
----------------------------------------


-----GOOG-hist-2016-2017 Summary--------
Predicted Val   : 795.0877
Actual Val      : 800.4000
Range Predction : [794.1772, 795.9981]
Absolute Error  : 5.3123
Relative Error  : 0.6637%
----------------------------------------
```



## Summary

In 90% cases, the relative error is less than 7‰, Bayesian Curve Fitting based prediction seems to work well for stock prices.