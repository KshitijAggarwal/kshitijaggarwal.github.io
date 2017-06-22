---
layout: post
title: Deep Reinforcement Learning to play Flappy Bird using A3C algorithm
---

# Overview
This project uses Asynchronous advantage actor-critic algorithm (A3C) to play Flappy Bird using Keras. The details of this algorithm are mentioned in this paper by Deep Mind. The code for this project can be found in [this](https://github.com/shalabhsingh/A3C_Keras_FlappyBird) github repository.

# Installation Dependencies
* Python 3.5
* Keras 2.0
* pygame 
* scikit-image

# How to Run?
Clone the repository or download it. To test the pretrained model, run the "test.py" file. To retrain the model from scratch, run the "train_network.py" script. 

The trained models at different stages will be saved in "saved_models" folder.

# What is Deep Reinforcement Learning?
Deep Reinforcement learning is a technique that uses Deep Neural Networks to solve Reinforcement learning problems. Reinforcement learning is a machine learning method that lies somewhere in between supervised and unsupervised learning. Whereas in supervised learning one has a target label for each training example and in unsupervised learning one has no labels at all, in reinforcement learning one has sparse and time-delayed labels – the rewards. Based only on those rewards the agent (bird) has to learn to behave in the environment (flappy bird game).

The following post is a must read for good introduction to Deep Reinforcement Learning - [Demystifying Deep Reinforcement Learning](https://www.nervanasys.com/demystifying-deep-reinforcement-learning/)

# What is A3C ?
Till 2016, Deep Q-learning was the got to method to solve reinforcement learning problems. In february 2016, A3C refers to Asynchronous advantage actor-critic algorithm for deep reinforcement learning. It was proposed over the famous DQN network for playing atari games, first made by DeepMind back in 2013. DQN was the first RL algorithm which was able to play games successfully because of which Google bought DeepMind itself. However it had some drawbacks which have been solved by A3C-

* DQN had a very large training time (~1 week on a GPU) whereas basic A3C takes 1 day to train on a CPU. (infact training time for Flappy Bird game in this project was just 6 hours !!)
* DQN used experience replay for getting good convergence which requires a lot of memory. A3C use multiple threads for this purpose which eliminates huge memory requirement.
* The major objective of DQN is to estimate Q-value for all actions in different environment states possible. As a result in early stages of learning, it mostly tries to learn Q-value for states which won't even be a part of optimal strategy. On the other hand, A3C learns the best policy to take at good states at the current point of time because of which it is faster to train.

However because of better exploration by DQN, it generally settles at global minima whereas A3C might settle at a local minima leading to sub-optimal results.

**Learning Resources-**

1. For theoretical and implementation details of how a DQN works, see this blog page- https://yanpanlau.github.io/2016/07/10/FlappyBird-Keras.html
2. For theoretical and implementation details of how an A3C works, see this blog page- https://jaromiru.com/2017/03/26/lets-make-an-a3c-implementation/

# Model Desciption
The input to the neural network is a stack of 4, 84x84 grayscale game frames. The network used a convolutional layer with 16 filters of size 8x8 with stride 4, followed by a convolutional layer with with 32 filters of size 4x4 with stride 2, followed by a fully connected layer with 256 hidden units. All three hidden layers were followed by a rectifier nonlinearity. There are two set of outputs – a softmax output with one output representing the probability of flapping, and a single linear output representing the value function.

The hyperparameters used are-
* Learning rate = 7e-4 which is decreased by 3.2e-8 (can be tuned better) every update.
* No. of threads = 16
* Frames/thread used for each update = 5
* Reward discount (gamma) = 0.99
* RMSProp cache decay rate = 0.99
* Entropy regularization, as suggested by the paper has not been used. However I believe that using it, could lead to better performance of the model.

The best model I have got is still not very good but is able to cross 5 pipes on average (i.e. it has developed a good understanding of when to flap and when not to). To train better models, tinkering with above hyperparameters can be beneficial.


# From Blog

This is a summary of what I learned in the Deep Reinforcement Learning project to create an agent which learned to play Flappy Bird game.

What is Q value?

Q-value is the expected discounted reward value that is obtained in a particular state s, after carrying out the greedy action a, i.e. it is a function of s and a - Q(s,a).

Where does Deep Neural Nets come into Picture?

In any particular environment, you may be able to obtain Q-Value for all the possible (state, action) pair and whenever you reach a state, choose the action with highest Q value and hurray, your job is done. However in a game, where each state is a grayscale 84*84*3 image, the number of possible states is enormously high. Hence we can't list down all the states and perform actions on them to find the best one. We need to approximate the best action based on experience, so as to learn how to play. And that's where deep neural nets come to our rescue.

Why Deep-RL is awesome?

Deep-RL is awesome because they eventually learn how to master any game by just seeing the game frame images, giving a feel of a unsupervised general purpose learner.

Different algos for the Deep Rl

1. 1 step Q learning - This is an off policy learning algorithm as the updates it makes are independent of the actions taken, as the we assume that maximum Q value action will be taken in the next frame.

The algorithm performs actions based on epsilon greedy policy (a random action with a probability epsilon and action predicted by the neural net with probability 1-epsilon). the rewards obtained in that frame are measured and error is taken as

E[r + gamma* max_a ( Q(s',a') ) - Q(s, a) ]. A large chunk of such frames and actions are stored in an experience replay store, from where a random mini-batch of experiences are sampled each time after some time to update weights. However over here asynchronous methods instead of experience replay have been used. The epsilon value keeps decreasing gradually.

2.  SARSA algorithm - It is same as 1 step Q learning except the fact that it uses an on policy approach to perform updates, (updates are dependent on action taken. i.e. error is E[r + gamma* Q(s',a') - Q(s, a) ] where a' is the action i.e. actually chosen according to policy and it may/may not be the action with highest Q value. In general Q value leads to better performance that Q learning but it may well depend on case to case.

3. n-Step Q learning - It is same as 1 step Q learning except the fact that it uses n steps in future to calculate the error because of which updates are transferred back to earlier states quickly.

4. A3C - Asynchronous advantage actor-critic is the fastest algorithm to train, among all. It has 2 versions, a FF one and a LSTM one. This uses a policy based approach along with a critic which promotes or criticises any action taken, depending upon how much the actual reward is in comparison to the average reward it expected out of that state.

The update is grad( sum(Advantage * log p(a|theta)) ) + beta * sum(entropy) where advantage is actual reward - expected reward. the secnd term is the regularization term which prevents premature convergence. The policy and critic, both use the same network with 2 different outputs and respective losses. Optimizer used in all cases is RMSprop with initial learning rate of 7e-4 which is annealed to 0 gradually.



Summary

This project was mainly focused on tuning the hyperparameters of the neural net as it is pretty difficult to converge as a3c searches for local optimum rather than global optimum. Another focus was to learn about the state of the art algorithms that are changing the deep learning scenarios, by producing universal AIs.

