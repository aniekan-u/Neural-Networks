import numpy as np


class Neural_Network(object):
    def __init__(self, input_, hidden_, output_, numHiddenLayer_, numExamples_):
        # Define Hyperparameters
        self.inputLayerSize = input_
        self.outputLayerSize = output_
        self.hiddenLayerSize = hidden_
        self.numHiddenLayer = numHiddenLayer_
        self.numExamples = numExamples_
        self.scalar = 0.0000000001 # LEARNING RATE: Why does ReLU produce such large dJdW values?
        # in -> out
        self.weights = [] # stores matrices of each layer of weights
        self.z = [] # stores matrices of each layer of weighted sums
        self.a = [] # stores matrices of each layer of activity 
        self.biases = [] # stores all biases

        # Biases are matrices that are added to activity matrix
        # Dimensions -> numExamples_*hiddenLayerSize or numExamples_*outputLayerSize
        for i in range(self.numHiddenLayer):
            # Biases for hidden layer
            b = [np.random.random() for x in range(self.hiddenLayerSize)];
            B = [b for x in range(self.numExamples)];
            self.biases.append(np.mat(B))
        # Biases for output layer
        b = [np.random.random() for x in range(self.outputLayerSize)]
        B = [b for x in range(self.numExamples)];
        self.biases.append(np.mat(B))


        # Weights (Parameters)
        # Weight matrix between input and first layer
        W = np.random.rand(self.inputLayerSize, self.hiddenLayerSize)
        self.weights.append(W)

        for i in range(self.numHiddenLayer-1):
            # Weight matrices between hidden layers
            W = np.random.rand(self.hiddenLayerSize, self.hiddenLayerSize)
            self.weights.append(W)
        # Weight matric between hiddenlayer and outputlayer
        self.weights.append(np.random.rand(self.hiddenLayerSize, self.outputLayerSize))

    def setBatchSize(self, numExamples):
        # Changes the number of rows (examples) for biases
        if (self.numExamples > numExamples):
            self.biases = [b[:numExamples] for b in self.biases]

    def sigmoid(self, z):
        # Apply sigmoid activation function
        return 1/(1+np.exp(-z))

    def sigmoidPrime(self, z):
        # Derivative of sigmoid function
        return 1-self.sigmoid(z)

    def ReLU(self, z):
        # Apply activation function
        for (i, j), item in np.ndenumerate(z):
            if (item < 0):
                item *= 0.01
            else:
                item = item
        return z        


    def ReLUPrime(self, z):
        # Derivative of ReLU activation function
        for (i, j), item in np.ndenumerate(z):
            if (item < 0):
                item = 0.01
            else:
                item = 1

        return z

    def forward(self, X):
        # Propagate outputs through network

        self.z.append(np.dot(X, self.weights[0]) + self.biases[0])
        self.a.append(self.ReLU(self.z[0]))

        for i in range(1, self.numHiddenLayer):
            self.z.append(np.dot(self.a[-1], self.weights[i]) + self.biases[i])
            self.a.append(self.ReLU(self.z[-1]))

        self.z.append(np.dot(self.z[-1], self.weights[-1]) + self.biases[-1])
        self.a.append(self.ReLU(self.z[-1]))
        yHat = self.ReLU(self.z[-1])
        return yHat

    def backProp(self, X, y):
        # Compute derivative wrt W
        # out -> in
        dJdW = [] # stores matrices of each dJdW (equal in size to self.weights[])
        delta = [] # stores matrices of each backpropagating error

        self.yHat = self.forward(X)
        delta.insert(0,np.multiply(-(y-self.yHat), self.ReLUPrime(self.z[-1]))) # delta = (y-yHat)(sigmoidPrime(final layer unactivated))
        dJdW.insert(0, np.dot(self.a[-2].T, delta[0])) # dJdW
        for i in range(len(self.weights)-1, 1, -1):
            # Iterate from self.weights[-1] -> self.weights[1]
            delta.insert(0, np.multiply(np.dot(delta[0], self.weights[i].T), self.ReLUPrime(self.z[i-1])))
            dJdW.insert(0, np.dot(self.a[i-2].T, delta[0]))

        delta.insert(0, np.multiply(np.dot(delta[0], self.weights[1].T), self.ReLUPrime(self.z[0])))
        dJdW.insert(0, np.dot(X.T, delta[0]))


        return dJdW

    def train(self, X, y):
        for t in range(60000):
            dJdW = self.backProp(X, y)
            for i in range(len(dJdW)):
                self.weights[i] -= self.scalar*dJdW[i]

# Instantiating Neural Network
inputs = [int(np.random.randint(0,100)) for x in range(100)]
x = np.mat([x for x in inputs]).reshape(100,1)
y = np.mat([x+1 for x in inputs]).reshape(100,1)
NN = Neural_Network(1,3,1,1,100)


# Training
print("INPUT: ", end = '\n')
print(x, end = '\n\n')

print("BEFORE TRAINING", NN.forward(x), sep = '\n', end = '\n\n')
NN.train(x,y)
print("AFTER TRAINING", NN.forward(x), sep = '\n', end = '\n\n')

# Testing
test = np.mat([int(np.random.randint(0,100)) for x in range(100)]).reshape(100,1)
print("TEST INPUT:", test, sep = '\n', end = '\n\n')
print(NN.forward(test), end = '\n\n')


NN.setBatchSize(1) # changing settings to receive one input at a time

while True:
    # Give numbers between 0-100 (I need to fix overfitting) and it will get next value
    inputs = input()
    x = np.mat([int(i) for i in inputs.split(" ")])
    print(NN.forward(x))