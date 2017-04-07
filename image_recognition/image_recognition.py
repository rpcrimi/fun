import numpy as np
from sklearn.datasets import fetch_mldata
from sklearn.metrics import confusion_matrix
from sklearn import linear_model
from sknn.mlp import Classifier, Layer
mnist = fetch_mldata("MNIST original", data_home="./")

logreg = linear_model.LogisticRegression()

logreg.fit(mnist.data[:60000], mnist.target[:60000])

predicted = logreg.predict(mnist.data[-10000:])

print confusion_matrix(mnist.target[-10000:], predicted)