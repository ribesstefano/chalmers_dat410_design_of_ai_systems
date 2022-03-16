from data_cleaner import load_dataset

import os
from tensorflow.keras.experimental import LinearModel
import tensorflow as tf

def load_model(model_filename):
    return tf.keras.models.load_model(model_filename)

def train_model(dataset_filename, model_filename=None, epochs=10):
    input_transposed = False
    x_train, y_train, x_test, y_test = load_dataset(dataset_filename, reshape=True)

    model = load_model(model_filename)
    history = None

    # model = tf.keras.models.Sequential([
    #     tf.keras.layers.Dense(y_train.shape[-1], input_shape=x_train.shape[1:]),
    # ])
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
    model_filename = os.path.join(data_dir, f'linear_model_{frame_rate}.h5')
    train_model(dataset_filename, model_filename, epochs=1)


if __name__ == '__main__':
    main()