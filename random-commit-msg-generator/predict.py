import numpy
import sys
from process_text import read_process_text
from keras.models import model_from_json
from process_text import get_training_data

seq_length = 4

raw_text = read_process_text('commit-messages.txt')
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
n_chars = len(raw_text)
n_vocab = len(chars)
dataX, dataY = get_training_data(raw_text, n_chars, seq_length, char_to_int)
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

start = numpy.random.randint(0, len(dataX) - 1)
pattern = dataX[start]
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
