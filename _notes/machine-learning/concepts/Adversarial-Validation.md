---
title: Adversarial Validation
date: 2024-04-06
publish: true
category: tech
tags:
- machine-learning
website_path: machine-learning/concepts
layout: note
---

[tweet](https://twitter.com/svpino/status/1775154270708396215?utm_source=ainews&utm_medium=email&utm_campaign=ainews-realm-reference-resolution-as-language) 

1. Put your train and test set together. 
2. Get rid of the target column. 
3. Create a new binary feature, and set every sample from your train set to 0 and every sample from the test set to 1. This feature will be the new target. 
4. Now, train a simple binary classification model on this new dataset. The goal of this model is to predict whether a sample comes from the train or the test split.

After you build a model, you can use the ROC-AUC to evaluate it. If the AUC is close to 0.5, your model can't separate the samples. This means your training and test data come from the same distribution. If the AUC is closer to 1.0, your model learned to differentiate the samples. Your training and test data come from different distributions.

![Pasted image 20240406085055.png](/images/c3f3d6b2.png)