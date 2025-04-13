---
title: ML Basics
date: 2024-07-21
publish: true
website_path: machine-learning/concepts
layout: note
---

#concept  #basics #ml-basics 

### Linear Regression:

Assumptions:
1. Linearity: The relationship between X and Y is linear.
2. Independence: Observations are independent of each other.
3. Homoscedasticity: Constant variance of residuals.
4. Normality: Residuals are normally distributed.
5. No multicollinearity: Independent variables are not highly correlated.

### Logistic Regression: 

- Odds: The ratio of the probability of success to the probability of failure.
- Log-odds (logit): The logarithm of the odds.

Assumptions:
1. Binary outcome: The dependent variable is binary.
2. Independence: Observations are independent of each other.
3. No multicollinearity: Independent variables are not highly correlated.
4. Linearity: The log-odds of the outcome are linearly related to the predictors.
5. Large sample size: Generally, a minimum of 10 events per predictor variable.

Coefficients in logistic regression represent the change in log odds for a one-unit increase in the corresponding independent variable.


#### K-means Clustering:
How it works:
- Choose K (number of clusters)
- Randomly initialize K centroids
- Assign each data point to the nearest centroid
- Recalculate centroids based on assigned points
- Repeat steps 3-4 until convergence

#### DBSCAN (Density-Based Spatial Clustering of Applications with Noise):
How it works:
- Choose epsilon (ε) and minimum points (minPts)
- For each point, find all points within ε distance
- If a point has at least minPts points within ε, it's a core point
- Connect core points that are within ε of each other
- Points that are within ε of a core point but have fewer than minPts neighbors are border points
- Points that are not core or border points are considered noise

### Bagging and Boosting 

### Bagging: 
Definition: A method that creates multiple subsets of the original dataset, trains a model on each subset, and then aggregates the predictions.

How it works:
1. Create multiple subsets of the original dataset using bootstrap sampling (sampling with replacement)
2. Train a separate model on each subset
3. Aggregate predictions (usually by voting for classification or averaging for regression)

Key characteristics:
- Reduces variance (overfitting) without increasing bias
- Models are trained independently and can be trained in parallel
- Works well with high-variance, low-bias algorithms (e.g., decision trees)

Example algorithm: Random Forest

### Boosting:
Definition: A method that trains models sequentially, with each new model focusing on the errors of the previous ones.

How it works:
1. Train a base model on the original dataset
2. Identify misclassified instances and increase their weights
3. Train a new model on the weighted dataset
4. Repeat steps 2-3 for a specified number of iterations
5. Combine predictions from all models (weighted voting or averaging)

Key characteristics:
- Reduces bias (underfitting) and variance
- Models are trained sequentially
- Works well with high-bias, low-variance algorithms (e.g., shallow decision trees)
Example algorithms: AdaBoost, Gradient Boosting, XGBoost

When to use:
- Bagging: When you have high-variance models and want to reduce overfitting
- Boosting: When you have high-bias models and want to increase predictive power

### Bias Variance

Very sensitive to training data and perform poorly on new data: low bias, high variance
underfitting (not performing on training or new data): high bias, low variance

- A very shallow tree (e.g., only one split) would have high bias and low variance.
- A very deep tree (fitting perfectly to the training data) would have low bias but high variance.

### SVM

SVC: 
![Screenshot 2024-07-21 at 8.42.49 PM.png](/images/89272fc8.png)

SVM:
Start with data in low dim
move the data to higher dim 
find the SVC that divides the data into 2 groups

polynomial kernels can be used to get high dim relationship between two points, instead of actually transforming the data. 

radial kernel (RBF): https://www.youtube.com/watch?v=Qc5IyLW_hns

### Gradient Descent 

Derivative of the error/loss -> take steps in the direction opposite to the slope to reduce the error -> multiply learning rate to control size of step -> keep doing that when the step size gets too small 

### SGD with momentum:

$V_t = \beta V_{t-1} + (1-\beta) S_t$   
$S_t$ is the noisy data
$V_t$ is approx averaging over $1/(1-\beta)$ datapoints

Compute exponentialy weighted average of gradients and use that for weight update

#### RMSProp

$S_{dw} = \beta S + (1-\beta) dW^2$
$W = W - \alpha dW/\sqrt S_{dw}$

### Adam

Exponentially Weighted Averages: is used in sequential noisy data to reduce the noise and smoothen the data. To denoise the data, we can use the following equation to generate a new sequence of data with less noise.

has both: SGD with momentum + RMSProp

$V_t = \beta_1 V_{t-1} + (1-\beta_1)dW$ 
$S_{dw} = \beta_2 S + (1-\beta_2) dW^2$

$V_{dw} = V_{dw}/(1-\beta_1)$
$S_{dw} = S_{dw}/(1-\beta_2)$

$W = W - \frac{\alpha V_{dw}}{\sqrt S_{dw} + \epsilon}$

$\beta_1 = 0.9, \beta_2 = 0.999$


### L1 Regularization 

- **Penalty Term**: L1 regularization adds the sum of the absolute values of the weights (coefficients) to the loss function. The modified loss function for a linear regression model can be expressed as:	
    
- **Effect on Weights**: The L1 regularization term encourages the optimization process to drive some of the weights to exactly zero. This happens because minimizing the absolute value of the weights can result in solutions where the optimal weight for certain features is zero, especially if those features have less predictive power.
    
- **Optimization Process**: During the optimization process, the gradient descent (or another optimization algorithm) updates the weights to minimize the loss function. The presence of the absolute value in the penalty term makes the optimization path different from L2 regularization (Ridge regression), which uses the squared values of the weights. In L1 regularization, the gradient is constant (either +λ or -λ) when the weight is not zero, causing weights to be reduced more aggressively. When the weights are small, they can be driven to zero, effectively removing the corresponding feature from the model.

### Decision Trees
Quantify impurity of the tree: gini impurity 

##### Classification 

For binary: 
Calculate Gini Impurity of individual leaves = 1 - (prob of yes)^2  - (1-prob of no)^2
Total Gini Impurity: Weighted average of gini impurities of the leaves

For continuous values: 
1. Sort the values 
2. Average values between each successive example 
3. Calculate Gini impurity for each such average
	1. Same as above now. <threshold, > threshold. Calculate gini for each case as above. Weighted average. 
4. Take the one with min impurity 

The feature with min Gini Impurity is chosen as the node. 


#### Regression 

Similar as above. Just use the sum of squared error as the measure of impurity. 

Steps: 
1. Find the best threshold for each feature. 
	1. Try all thresholds. See what gives min sum of squared error. 
2. The feature with min error is the root. 
3. Divide into two. 
	1. Repeat 1 and 2 on left and right leaf. 

Prediction is the average value from the relevant leaf node. 


### Covariance vs Correlation

Covariance and correlation are both statistical measures that describe the relationship between two variables, but they have some key differences:

1. Scale:
	- Covariance is not standardized and can take any value from negative infinity to positive infinity.
	- Correlation is standardized and always falls between -1 and 1.

1. Interpretation:
	- Covariance only indicates the direction of the linear relationship between variables (positive or negative).
	- Correlation indicates both the direction and strength of the linear relationship.

2. Units:
	- Covariance is expressed in units that are the product of the units of the two variables.
	- Correlation is unitless, making it easier to compare relationships between different pairs of variables.

3. Formula:
	- Covariance: cov(X,Y) = E[(X - μX)(Y - μY)]
	- Correlation: ρ(X,Y) = cov(X,Y) / (σX * σY), where σ is the standard deviation

4. Sensitivity to scale:
	- Covariance is sensitive to changes in scale of the variables.
	- Correlation is not affected by changes in scale or units of measurement.

In summary, correlation can be thought of as a standardized version of covariance, making it easier to interpret and compare across different datasets.

#### ReLU, vanishing gradient problem, and tanh: 
ReLU and vanishing gradient: 
- ReLU (Rectified Linear Unit) actually helps mitigate the vanishing gradient problem, not suffer from it.
- For positive inputs, ReLU has a constant gradient of 1, which helps prevent vanishing gradients.
- However, ReLU can suffer from the "dying ReLU" problem, where neurons can get stuck in a state where they always output 0.

Tanh and vanishing gradient:
- Tanh does suffer from the vanishing gradient problem.
- Reason: The derivative of tanh approaches zero for very large or very small inputs.
- This can slow down learning in the earlier layers of deep networks.

In summary, ReLU helps with the vanishing gradient problem but can face the dying ReLU issue, while tanh does suffer from vanishing gradients due to its bounded nature and derivative characteristics.



```python

THERE is a difference between torch.Tensor and torch.tensor!!!! 

```

`torch.tensor` infers the `dtype` automatically, while `torch.Tensor` returns a `torch.FloatTensor`.  I would recommend to stick to `torch.tensor`, which also has arguments like `dtype`, if you would like to change the type. - ptrblck

