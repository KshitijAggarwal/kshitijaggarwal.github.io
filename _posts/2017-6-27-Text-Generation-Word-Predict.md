---
layout: post
title: Text Generation & Word Prediction using RNN
-disqus: true
---

There are a lot of beautiful things about neural networks and one of them is Recurrent Neural Networks (RNN). RNNs have been used in a variety of fields lately and have given very good results.

## What is RNN?
RNN stands for Recurrent neural networks. Recurrent is used to refer to repeating things. And hence an RNN is a neural network which repeats itself. In an RNN, the value of hidden layer neurons is dependent on the present input as well as the input given to hidden layer neuron values in the past. As past hidden layer neuron values are obtained from previous inputs, we can say that an RNN takes into consideration all the previous inputs given to the network in the past to calculate the output. You can visualize an RNN as follows-


![](/images/RNN-unrolled.png)
{:refdef: style="text-align: center;"}
_Image taken from [Colah's blog](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)_
{: refdef}

There is a loop in the hidden layers because the hidden layer values are also calculated from previous hidden layer values. If we unroll an RNN as shown in the right part of the image above, this dependency becomes clearer.

For a better understanding, we need to dig a little into mathematics of how this works. In vanilla RNN, the hidden layer value of a neuron is calculated by adding the value obtained by multiply the input of the previous layer and the weight matrix and then adding to it the previous value of that neuron. This is generally followed by a ```tanh``` or ```ReLU``` activation function. For a first hidden layer of a network, this can be written as-

{:refdef: style="text-align: center;"}
![equation](http://latex.codecogs.com/gif.latex?h_t%20%3D%20tanh%28W_%7Bhh%7Dh_%7Bt-1%7D%20&plus;%20W_%7Bxh%7Dx_t%29)
{: refdef}

where ![](http://latex.codecogs.com/gif.latex?h_t) and ![](http://latex.codecogs.com/gif.latex?h_%7Bt-1%7D) are hidden neuron's value at time ![](http://latex.codecogs.com/gif.latex?t) and ![](http://latex.codecogs.com/gif.latex?t-1) respectively, ![](http://latex.codecogs.com/gif.latex?W_%7Bhh%7D) and ![](http://latex.codecogs.com/gif.latex?W_%7Bxh%7D) are weight matrices from hidden to hidden and input to hidden layers respectively. 

However traditional RNN networks are not very good at remembering things because of sigmoid/tanh activation function which is not very good at transferring weight updates during backpropagation. Another reason for this is relatively simple formulation of recurrent nature of the network. The recurrent function might require something more powerful to remember previous inputs, than a simple adding mechanism followed by an activation function as showed in the equation above.

This problem is solved by using Long Short Term Memory neurons (LSTM). LSTMs are more powerful in transferring relevant previous input information in the network by using a more complicated function to calculate new hidden layer neuron values. They key to their good performance is the use of cell states and different gates. Gates are a way to optionally let information through. The different gates used are as follows-

1. **Forget gate :** This gate taken as input the hidden layer neuron values for previous input and the most recent input given to the model. This gate uses a sigmoid function which outputs how much of the previous information has to be propagated further. A value of 0 indicates the network to forget all previous information and a value of 1 means that all the previous information should be retained.

2. **Update gate :** In this gate, the previous cell state is updated and new insights are obtained from current inputs. The new information is then added to the output of forget gate to calculate the new cell state, which will used when the next input is provided.

3. **Output Gate :** An output gate is used if the neural network outputs any information, for the current input. A sigmoid gate is used to decide which part of information, we are going to output.

I know that it isn't easy to digest what we have just read, until we see some mathematical expressions which explain this stuff. However I won't discuss it here because it is a bit complicated and not for everybody. I will suggest interested readers to have a look at these posts for a more mathematical approach to RNN and LSTM (specially the second one). The first link is also a good read as it shows how RNNs and LSTMs are used to solve a variety of problems today-

* [The Unreasonable Effectiveness of Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
* [Understanding LSTM Networks - colah's blog](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)

To illustrate the power of RNNs and LSTMs, we will train a neural network model that learns to understand English language. Later it is used for 2 applications-

1. To generate text given an intial piece of text as input.
2. To suggest next word while we are writing a sentence.

**The code for the project below can be found on [this](https://github.com/shalabhsingh/Text_generation_prediction_RNN) GitHub repository I have created.** Although the results are not outstanding, but they are sufficient to illustrate the concept we are dealing with over here. We will begin going through the code now so that we can understand what's going on. The neural model is created in python using Keras library in Jupyter notebook.

**The codes and applications of RNN developed in this blog post are highly based on this [blog post](http://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/) on machinelearningmastery.com**

## Model development and training

First of all, we import the numpy and keras modules, important for storing data and defining the model respectively.


```python
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.optimizers import RMSprop, Adam
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
```

    Using TensorFlow backend.
    


```python
SEQ_LENGTH = 100
```

We define the model now. The model is given an input of 100 character sequences and it outputs the respective probabilities with which a character can succeed the input sequence. The model consists of 3 hidden layers. The first two hidden layers consist of 256 LSTM cells, and the second layer is fully connected to the third layer. The number of neurons in the third layer is same as the number of unique characters in the training set (the vocabulary of the training set). The neurons in the third layer, use softmax activation so as to convert their outputs into respective probabilities. The loss used is Categorical cross entropy and the optimizer used is Adam.


```python
def buildmodel(VOCABULARY):
    model = Sequential()
    model.add(LSTM(256, input_shape = (SEQ_LENGTH, 1), return_sequences = True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(VOCABULARY, activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam')
    return model
```

Next, we download the training data. The popular book "Alice's Adventures in Wonderland" written by Lewis Caroll has been used as training dataset for this project. The e-book can be downloaded from [here](http://www.gutenberg.org/ebooks/11?msg=welcome_stranger) in Plain Text UTF-8 format. The downloaded book has been stored in the root directory with the name 'wonderland.txt'. We open this book using the open command and convert all characters into lowercase (so as to reduce the number of characters in the vocabulary, making it easier to learn for the model.)


```python
file = open('wonderland.txt', encoding = 'utf8')
raw_text = file.read()    #you need to read further characters as well
raw_text = raw_text.lower()
```

Next, we store all the distinct characters occurring in the book in the ```chars``` variable. We also remove some of the rare characters (stored in bad-chars) from the book. The final vocabulary of the book is printed at the end of code segment.


```python
chars = sorted(list(set(raw_text)))
print(chars)

bad_chars = ['#', '*', '@', '_', '\ufeff']
for i in range(len(bad_chars)):
    raw_text = raw_text.replace(bad_chars[i],"")

chars = sorted(list(set(raw_text)))
print(chars)
```

    ['\n', ' ', '!', '#', '$', '%', '(', ')', '*', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', '@', '[', ']', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '‘', '’', '“', '”', '\ufeff']
    ['\n', ' ', '!', '$', '%', '(', ')', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', '[', ']', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '‘', '’', '“', '”']
    

Now, we summarize the entire book to find that the book consists of a total of 163,721 characters (which is relatively small to train a RNN model) and the final number of characters in the vocabulary is 56.


```python
text_length = len(raw_text)
char_length = len(chars)
VOCABULARY = char_length
print("Text length = " + str(text_length))
print("No. of characters = " + str(char_length))
```

    Text length = 163721
    No. of characters = 56
    

Now, we need to modify the dataset representation to bring it in the form the model will need. So, we create an input window of 100 characters (SEQ_LENGTH = 100) and shift the window one character at a time until we reach the end of the book. An encoding is used, so as to map each of the characters into it's corresponding location in the vocabulary. Each time the input window contains a new sequence, it is converted into integers, using this encoding and appended to the input list of the dataset, ```input_strings```. For all such input windows, the character just following the sequence is appended to the output list ```output_strings```.


```python
char_to_int = dict((c, i) for i, c in enumerate(chars))
input_strings = []
output_strings = []

for i in range(len(raw_text) - SEQ_LENGTH):
    X_text = raw_text[i: i + SEQ_LENGTH]
    X = [char_to_int[char] for char in X_text]
    input_strings.append(X)    
    Y = raw_text[i + SEQ_LENGTH]
    output_strings.append(char_to_int[Y])
```

Now, the ```input_strings``` and ```output_strings``` lists are converted into a numpy array of required dimensions, so that they can be fed to the model for the training.


```python
length = len(input_strings)
input_strings = np.array(input_strings)
input_strings = np.reshape(input_strings, (input_strings.shape[0], input_strings.shape[1], 1))
input_strings = input_strings/float(VOCABULARY)

output_strings = np.array(output_strings)
output_strings = np_utils.to_categorical(output_strings)
print(input_strings.shape)
print(output_strings.shape)
```

    (163621, 100, 1)
    (163621, 56)
    

Finally the model is built and then fitted for training. The model is trained for 50 epochs and a batch size of 128 sequences has been used. After every epoch, the current model state is saved if the model has the least loss encountered till that time. The training loss decreases in almost every epoch till 50 epochs are finished which suggests that there is further scope to decrease the loss by training for more epochs.

The total training time is ~90 hours on a CPU and ~12 hours (expected) if performed on a GPU. Because I trained on a CPU the time taken was very large and I didn't train for more epochs. Every 10th epoch is shown below to have an idea of how the training loss decreased.


```python
model = buildmodel(VOCABULARY)
filepath="saved_models/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

history = model.fit(input_strings, output_strings, epochs = 50, batch_size = 128, callbacks = callbacks_list)
```

    Epoch 1/50
    163584/163621 [============================>.] - ETA: 1s - loss: 2.9082Epoch 00000: loss improved from inf to 2.90829, saving model to saved_models/weights-improvement-00-2.9083.hdf5
    163621/163621 [==============================] - 6029s - loss: 2.9083    
    Epoch 10/50
    163584/163621 [============================>.] - ETA: 1s - loss: 1.8646Epoch 00009: loss improved from 1.90604 to 1.86468, saving model to saved_models/weights-improvement-09-1.8647.hdf5
    163621/163621 [==============================] - 5928s - loss: 1.8647 
    Epoch 20/50
    163584/163621 [============================>.] - ETA: 1s - loss: 1.5952Epoch 00019: loss improved from 1.61431 to 1.59517, saving model to saved_models/weights-improvement-19-1.5952.hdf5
    163621/163621 [==============================] - 5860s - loss: 1.5952   
    Epoch 30/50
    163584/163621 [============================>.] - ETA: 1s - loss: 1.4652Epoch 00029: loss improved from 1.47327 to 1.46526, saving model to saved_models/weights-improvement-29-1.4653.hdf5
    163621/163621 [==============================] - 5951s - loss: 1.4653  
    Epoch 40/50
    163584/163621 [============================>.] - ETA: 1s - loss: 1.3892Epoch 00039: loss improved from 1.39005 to 1.38922, saving model to saved_models/weights-improvement-39-1.3892.hdf5
    163621/163621 [==============================] - 5916s - loss: 1.3892    
    Epoch 50/50
    163584/163621 [============================>.] - ETA: 1s - loss: 1.3420Epoch 00049: loss improved from 1.34926 to 1.34199, saving model to saved_models/weights-improvement-49-1.3420.hdf5
    163621/163621 [==============================] - 5937s - loss: 1.3420  
    

Now that our model has been trained, we can use it for generating texts as well as predicting next word, which is what we will do now.

## Text Generation

Now, we are going to generate 1000 character texts, given an initial seed of characters. This will help us evaluate that how much the model has understood about word formation, English grammar and context of the given initial seed.

The best model with least loss as we obtained in the last epoch of training is loaded and the model is build and recompiled.

```python
filename = 'saved_models/weights-improvement-49-1.3420.hdf5'
model = buildmodel(VOCABULARY)
model.load_weights(filename)
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam')
```

The initial 100 character seed used for generating text are the first few characters of the famous children book 'The Cat in the Hat' by Dr. Seuss available [here](http://www.stylist.co.uk/books/100-best-opening-lines-from-childrens-books#gallery-1). 


```python
initial_text = ' the sun did not shine, it was too wet to play, so we sat in the house all that cold, cold wet day. '# we sat here we two and we said how we wish we had something to do.'
initial_text = [char_to_int[c] for c in initial_text]
```

Starting with the initial seed, next 1000 characters are generated by shifting the 100 character input window for generating the next character as shown below-


```python
GENERATED_LENGTH = 1000
test_text = initial_text
generated_text = []

for i in range(1000):
    X = np.reshape(test_text, (1, SEQ_LENGTH, 1))
    next_character = model.predict(X/float(VOCABULARY))
    index = np.argmax(next_character)
    generated_text.append(int_to_char[index])
    test_text.append(index)
    test_text = test_text[1:]
```


```python
print(''.join(generated_text))
```

    and the white rabbit was a little botk of the sable of the garden, the mock turtle said nothing on the soog, and she shought thene was not a moment to be no mistle thing, and she was soomding of the soecs of the gad she was soo mloe ald spok as the mock turtle with a siate oige back on the shate.
    
    ‘well, it doesn’t kike the bar,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said the king. 
    ‘i dan’t remember it,’ said 
    

### Conclusion

We can see the 1000 characters as generated by the model and there are a lot of insights to conclude about the model-

* Most of the words generated by the model are proper English words, although there are exceptions at many places. This shows that the model has a good understanding of how letters are combined to form different words. Even though it is very obvious to do for a human, but for a computer model to give a reasonable performance at word formation is itself a huge feat.
* There are a few drawbacks as well. One of them is that the model often suggests ```and```, both after a comma and a full stop which may be correct in case 1, but is always wrong for case 2. Also some incorrected words are generated as well.
* The model has understood the use of inverted quotes and apostrophes quite nicely. All the inverted commas are closed appropriately and succeeded by proper endings, such as 'said the king.'.
* The model has understood the use of spaces and indentations quite well. After each of the 'said the king' lines, succeeding text always begins in the new line, giving the generated text, a clean look.
* The model has almost no understanding of the context of the initial seed. The initial text consists of a cold wet day and how playing is difficult on such a day, but generated text talks about rabbits and turtles (which still seems reasonable), but then  starts a conversation of king, later in the generated sequence which is quite absurd. However results on this are expected to improve once the model is trained on a variety of texts rather than just a single book.


## Word Prediction

Now we are going to touch another interesting application. We are going to predict the next word that someone is going to write, similar to the ones used by mobile phone keyboards. This will help us evaluate that how much the neural network has understood about dependencies between different letters that combine to form a word. We can also get an idea of how much the model has understood about the order of different types of word in a sentence. The gif below shows how the model predicting the next word, in this project.

![](/images/type1.gif)

The original model has been defined in a manner to take in 100 character inputs. So when the user initially starts typing the words, the total length of input string will be less than 100 characters. To solve this issue, the input has been padded with series of spaces in the beginning in order to make the total length of 100 characters. As the total length exceeds 100 characters, only last 100 characters are taken into consideration as the LSTM nodes take care of remembering the context of the document from before.

Succeeding characters are predicted by the model until a space or full stop is encountered. The predicted characters are joined to form the next word, predicted by the model.


```python
original_text = []
predicted_text = []

text = widgets.Text()
display(text)

def handle_submit(sender):
    global predicted_text
    global original_text
    
    inp = list(text.value)
    
    last_word = inp[len(original_text):]
    inp = inp[:len(original_text)]    
    original_text = text.value    
    last_word.append(' ')
    
    inp_text = [char_to_int[c] for c in inp]
    last_word = [char_to_int[c] for c in last_word]
    
    if len(inp_text) > 100:
        inp_text = inp_text[len(inp_text)-100: ]
    if len(inp_text) < 100:
        pad = []
        space = char_to_int[' ']
        pad = [space for i in range(100-len(inp_text))]
        inp_text = pad + inp_text
    
    while len(last_word)>0:
        X = np.reshape(inp_text, (1, SEQ_LENGTH, 1))
        next_char = model.predict(X/float(VOCABULARY))
        inp_text.append(last_word[0])
        inp_text = inp_text[1:]
        last_word.pop(0)
    
    next_word = []
    next_char = ':'
    while next_char != ' ':
        X = np.reshape(inp_text, (1, SEQ_LENGTH, 1))
        next_char = model.predict(X/float(VOCABULARY))
        index = np.argmax(next_char)        
        next_word.append(int_to_char[index])
        inp_text.append(index)
        inp_text = inp_text[1:]
        next_char = int_to_char[index]
    
    predicted_text = predicted_text + [''.join(next_word)]
    print(" " + ''.join(next_word), end='|')
    
text.on_submit(handle_submit)
```



     ’ | of | y | a | the | dia | out | see | it | see | and | she | kean | the | a | wind, | of | the | would | and | it |  | and | shink | an | was | i | and | dou’e | the | at | hear | of | the | hear | thing | to | heard | the | hev | at | must | do | you |

Running this code segment generates a text box in which enter the input, as shown in the gif. The text box (not visible in the output) above shows the text as written by the user. The text used over here is same as in the previous application. As the text is typed over, pressing enter just after the character ends (before the space), gives us the next word suggestion as can be seen above, followed by a vertical bar to separate the words.

Next we summarize the predictions made by the model, in a nice tabular form listing the actual word typed by the user and the word suggested by the model before typing it, side by side as shown after the code segment below.


```python
from tabulate import tabulate

original_text = original_text.split()
predicted_text.insert(0,"")
predicted_text.pop()

table = []
for i in range(len(original_text)):
    table.append([original_text[i], predicted_text[i]])
print(tabulate(table, headers = ['Actual Word', 'Predicted Word']))
```

    Actual Word    Predicted Word
    -------------  ----------------
    the
    sun            ’
    did            of
    not            y
    shine,         a
    it             the
    was            dia
    too            out
    wet            see
    to             it
    play,          see
    so             and
    we             she
    sat            kean
    in             the
    the            a
    house          wind,
    all            of
    that           the
    cold,          would
    cold           and
    wet            it
    day.
    i              and
    sat            shink
    there          an
    with           was
    sally.         i
    we             and
    sat            dou’e
    here           the
    we             at
    two            hear
    and            of
    we             the
    said           hear
    how            thing
    we             to
    wish           heard
    we             the
    had            hev
    something      at
    to             must
    do.            do
    

### Conclusion
A lot of observations can be made from the table above-
* Just like in the last application, most of the words generated by the model are proper English words, which shows that the model has developed understanding about word formation.
* The model has also understood to some extent about grammar of English language. In the above case, we can see that it often suggests verb at place of a verb like 'wet to see' in place of 'wet to play'. Also many a times, words of other part of speech are suggested but they fit well, for example, 'we sat in the wind' is suggested in place of 'we sat in the house'. Relationships like this show great hope, although the model has to further learn a lot in this area.
* There are a few drawbacks as well. One of them is that the model often suggests 'and', both after a comma and a full stop which may be correct in case 1, but is always wrong for case 2 just like in the previous application

Overall, this makes up a nice demonstration for word prediction using RNNs with LSTM nodes. Seeing the performance of these models show that how advanced models phone keyboard suggestions use, which are very accurate. Further improvements in this model can be made by further training, tuning the hyperparameters, using a deeper network etc.

I hope that a lot was learnt while going through this blog post. If you have any comments/suggestions or any doubt, please write it in the comments below.

Happy learning.


