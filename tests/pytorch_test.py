import torch
from src.pytorch_mnist import main as mnist_example

if __name__ == '__main__':
    assert torch.cuda.is_available(), "CUDA is not available from pytorch"
    print('------ GPU is now available, starting with the MNIST example. -----')
    mnist_example()
