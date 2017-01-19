import numpy
import sys
from process_text import read_process_text
from keras.models import model_from_json
from process_text import get_training_data

seq_length = 7

raw_text = read_process_text('commit-messages.txt')
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
n_chars = len(raw_text)
n_vocab = len(chars)
dataX, dataY = get_training_data(raw_text, n_chars, seq_length, char_to_int)
# load json and create model
json_file = open('model_l%i.json' % (seq_length), 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model_l%i.h5" % (seq_length))
print("Loaded model from disk")


def write_commit(model):
    counter = 0
    done = False
    start = numpy.random.randint(0, len(dataX) - 1)
    pattern = dataX[start]
    pattern[len(pattern) - 1] = char_to_int['X']
    while not done and counter < 1000:
        counter += 1
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        prediction = prediction / numpy.sum(prediction)
        index = numpy.random.choice(numpy.arange(
            0, len(prediction[0])), p=prediction[0], size=1)[0]
        result = int_to_char[index]
        if result == 'X':
            done = True
        else:
            sys.stdout.write(result)
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
    sys.stdout.write('\n')


for i in range(0, 20):
    write_commit(model)

print("\nDone.")
