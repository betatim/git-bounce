# Code coming from
# http://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/

# Load Larger LSTM network and generate text
import sys
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
# load ascii text and covert to lowercase
from process_text import read_process_text
from process_text import get_training_data

seq_length = 4
n_epoch = 3

filename = sys.argv[1]

raw_text = read_process_text(filename)
## raw_text = raw_text[0:200]

# create mapping of unique chars to integers, and a reverse mapping
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)
# prepare the dataset of input to output pairs encoded as integers


dataX, dataY = get_training_data(raw_text, n_chars, seq_length, char_to_int)
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(
    X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
# load the network weights
# filename = "weights-improvement-47-1.2219-bigger.hdf5"
# model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')


model.fit(X, y, nb_epoch=n_epoch, batch_size=64)
# pick a random seed
start = numpy.random.randint(0, len(dataX) - 1)
pattern = dataX[start]
print("Seed:")
print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
# generate characters
for i in range(1000):
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    index = numpy.random.choice(numpy.arange(
        0, len(prediction[0])), p=prediction[0], size=1)[0]
    result = int_to_char[index]
    seq_in = [int_to_char[value] for value in pattern]
    sys.stdout.write(result)
    pattern.append(index)
    pattern = pattern[1:len(pattern)]
print("\nDone.")


# serialize model to JSON
model_json = model.to_json()
with open("model_l%i.json" % (seq_length), "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model_l%i.h5" % (seq_length))
print("Saved model to disk")
