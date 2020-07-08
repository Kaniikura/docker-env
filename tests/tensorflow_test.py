from src.tensorflow_mnist import main as mnist_example
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


if __name__ == '__main__':
    assert len(tf.config.list_physical_devices('GPU')
               ) > 0, "CUDA is not available from tensorflow"
    print('------ GPU is now available, starting with the MNIST example. -----')
    mnist_example()
