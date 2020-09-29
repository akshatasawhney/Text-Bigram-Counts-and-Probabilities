# Text Bigram Counts and Probabilities
 Python program to calculate bigram counts and probabilities using different smoothing techniques.

# To run the program - 
1. Make sure python3.x is installed

2. Library required - ujson

3. The training corpus is included in the folder.

4. To train the model, run train.py.

5. To test the model on own input, run test.py in the following manner - 
  
  python test.py <"input text"> <"Type of Smoothing">

  Type of smoothing can be - 
  i) "NS" for No Smoothing
  ii) "AO" for Add One Smoothing
  iii) "GT" for Good Turing Smoothing
