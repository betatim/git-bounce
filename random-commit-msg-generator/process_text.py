
def read_process_text(filename):
    raw_text = open(filename).readlines()
    raw_text = ''.join(raw_text).lower()
    raw_text = raw_text.replace('\n', 'X')
    return raw_text


def get_training_data(raw_text, n_chars, seq_length, char_to_int):
    dataX = []
    dataY = []
    for i in range(0, n_chars - seq_length, 1):
        seq_in = raw_text[i:i + seq_length]
        seq_out = raw_text[i + seq_length]
        dataX.append([char_to_int[char] for char in seq_in])
        dataY.append(char_to_int[seq_out])
    return dataX, dataY
