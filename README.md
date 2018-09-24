# Harry_Potter_sorting_hat
A program that sorts students into Hogwarts houses using logistic regression and machine learning in ~10 variables. Along with a sequence of simple data visualization.

This is a first project I did in python and I took the oppotunity to explore various tools and packages in the field.

## Task 1: Build a describe function
![alt text](https://github.com/conanwu777/Harry_Potter_sorting_hat/blob/master/describe.png)

## Task 2: Find subjects with homogenuous distribution across the 4 houses through histogram
![alt text](https://github.com/conanwu777/Harry_Potter_sorting_hat/blob/master/histogram.png)

## Task 3: Pairplot to filter the subjects to use for logistic regression
(I removed the two homogenuous subjects and one of the linearly related ones, used remaining 10 dimensions for the regression)
![alt text](https://github.com/conanwu777/Harry_Potter_sorting_hat/blob/master/pairplot.png)

## Task 4: Implement logistic regression to find separating hyperplans in 10-dimensional space
two-dimensional conceptual demo:
![alt text](https://github.com/conanwu777/Harry_Potter_sorting_hat/blob/master/Figure_1.png)

## Task 5: Training the model
- Training data size 1600
- Autocompleted missing fields with house average
- Implemented Schocastic regression
![alt text](https://github.com/conanwu777/Harry_Potter_sorting_hat/blob/master/train.jpg)

## Task 6: Prediction
- Testing data size 400
- Correct rate 99%
Graph of resulted prediction in pairplot (with missing field filled in with average over all students)
![alt text](https://github.com/conanwu777/Harry_Potter_sorting_hat/blob/master/check.png)
