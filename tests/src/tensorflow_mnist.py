# referenced "https://www.tensorflow.org/tutorials/quickstart/beginner"
import tensorflow as tf
import os
dataset_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'data', 'mnist.npz')


def main():
    # prepare the MNIST dataset
    mnist = tf.keras.datasets.mnist

    if not os.path.exists(os.path.dirname(dataset_path)):
        os.makedirs(os.path.dirname(dataset_path))
    (x_train, y_train), (x_test, y_test) = mnist.load_data(dataset_path)
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # build the model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
    ])

    # loss function
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    # compile
    model.compile(optimizer='adam',
                  loss=loss_fn,
                  metrics=['accuracy'])

    # train
    model.fit(x_train, y_train, epochs=5)

    # eval
    model.evaluate(x_test,  y_test, verbose=2)
