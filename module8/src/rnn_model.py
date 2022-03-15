import tensorflow as tf
from tensorflow.keras.layers import LSTM, Input, Dropout, BatchNormalization, Reshape  # ,CuDNNLSTM, CuDNNGRU
from tensorflow.keras.models import Model

from data_cleaner import load_dataset


def load_model(model_filename):
    return tf.keras.models.load_model(model_filename)


def train_model(dataset_filename, model_filename=None, epochs=10):
    x_train, y_train, x_test, y_test = load_dataset(dataset_filename)
    # model = LinearModel(units=y_test.shape[-1])
    # model.compile(optimizer='adam', loss='mse')
    # model.fit(x_train, y_train, epochs=epochs)
    out_shape = y_train.shape[1] * y_train.shape[2]
    n_units = 500
    input = Input(shape=x_train.shape[1:])
    hid1 = LSTM(n_units, return_sequences=True, activation='relu')(input)
    dp1 = Dropout(0.2)(hid1)
    hid2 = LSTM(n_units, return_sequences=True, activation='relu')(dp1)
    dp2 = Dropout(0.2)(hid2)
    hid3 = LSTM(n_units, return_sequences=True, activation='relu')(dp2)
    bn = BatchNormalization(momentum=0.0)(hid3)
    hid4 = LSTM(n_units, return_sequences=True, activation='relu')(bn)
    dp3 = Dropout(0.2)(hid4)

    output = Reshape((y_train.shape[1], y_train.shape[2]))(bn)
    model = Model(input, dp3)
    model.compile(optimizer='adam', loss='mse', metrics=['mse'])
    model.summary()
    if model_filename is not None:
        model.save(model_filename)
    return model
