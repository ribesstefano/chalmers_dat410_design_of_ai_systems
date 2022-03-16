from data_cleaner import load_dataset

import os
import tensorflow as tf
import numpy as np

def load_model(model_filename):
    return tf.keras.models.load_model(model_filename)

def train_model(dataset_filename, model_filename=None, epochs=10):
    input_transposed = True
    x_train, y_train, x_test, y_test = load_dataset(dataset_filename)
    # Add one dimension in last position
    x_train = x_train[..., np.newaxis]
    y_train = y_train[..., np.newaxis]
    x_test = x_test[..., np.newaxis]
    y_test = y_test[..., np.newaxis]

    model = load_model(model_filename)
    history = None

    # inp = tf.keras.layers.Input(shape=x_train.shape[1:])
    # c1 = tf.keras.layers.Conv1D(2 * 2, 5, 2, 'same', activation='relu')(inp)
    # c2 = tf.keras.layers.Conv1D(2 * 4, 5, 2, 'same', activation='relu')(c1)
    # c3 = tf.keras.layers.Conv1D(2 * 8, 5, 2, 'same', activation='relu')(c2)
    # c4 = tf.keras.layers.Conv1D(2 * 16, 5, 2, 'same', activation='relu')(c3)
    # c5 = tf.keras.layers.Conv1D(2 * 32, 5, 2, 'same', activation='relu')(c4)

    # dc1 = tf.keras.layers.Conv1DTranspose(2 * 32, 32, 1, padding='same')(c5)
    # conc = tf.keras.layers.Concatenate()([c5, dc1])
    # dc2 = tf.keras.layers.Conv1DTranspose(2 * 16, 32, 2, padding='same')(conc)
    # conc = tf.keras.layers.Concatenate()([c4, dc2])
    # dc3 = tf.keras.layers.Conv1DTranspose(2 * 8, 32, 2, padding='same')(conc)
    # conc = tf.keras.layers.Concatenate()([c3, dc3])
    # dc4 = tf.keras.layers.Conv1DTranspose(2 * 4, 32, 2, padding='same')(conc)
    # conc = tf.keras.layers.Concatenate()([c2, dc4])
    # dc5 = tf.keras.layers.Conv1DTranspose(2 * 2, 32, 2, padding='same')(conc)
    # conc = tf.keras.layers.Concatenate()([c1, dc5])
    # dc6 = tf.keras.layers.Conv1DTranspose(2 * 1, 32, 2, padding='same')(conc)
    # conc = tf.keras.layers.Concatenate()([inp, dc6])
    # dc7 = tf.keras.layers.Conv1DTranspose(1 * 1, 32, 1, padding='same', activation='linear')(conc)

    # model = tf.keras.models.Model(inp, dc7)
    # model.compile(optimizer='adam', loss='mse', metrics=['mse'])
    # history = model.fit(x=x_train, y=y_train,
    #                     batch_size=128,
    #                     epochs=epochs,
    #                     validation_data=(x_test, y_test), verbose=1)

    # if model_filename is not None:
    #     model.save(model_filename)
    return model, x_test, y_test, input_transposed, history

def main():
    frame_rate = '8k'

    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
    dataset_filename = os.path.join(data_dir, f'{frame_rate}.npy')
    model_filename = os.path.join(data_dir, f'conv1d_{frame_rate}.h5')
    train_model(dataset_filename, model_filename, epochs=1)


if __name__ == '__main__':
    main()