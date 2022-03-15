from data_cleaner import load_dataset

import os
from tensorflow.keras.experimental import LinearModel

def load_model(model_filename):
    return tf.keras.models.load_model(model_filename)

def train_model(dataset_filename, model_filename=None, epochs=10):
    x_train, y_train, x_test, y_test = load_dataset(dataset_filename)
    model = LinearModel(units=y_test.shape[-1])
    model.compile(optimizer='adam', loss='mse')
    model.fit(x_train, y_train, epochs=epochs)
    if model_filename is not None:
        model.save(model_filename)
    return model

def main():
    frame_rate = '8k'

    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
    dataset_filename = os.path.join(data_dir, f'{frame_rate}.npy')
    model_filename = os.path.join(data_dir, f'linear_model_{frame_rate}.h5')
    train_model(dataset_filename, model_filename, epochs=1)


if __name__ == '__main__':
    main()