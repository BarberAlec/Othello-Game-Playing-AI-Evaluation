import torch
from torch.nn import Linear, ReLU, CrossEntropyLoss, Sequential, Conv2d, MaxPool2d, MaxUnpool2d, Module, Softmax, BatchNorm2d, Dropout


class OthelloCNN(Module):
    def __init__(self):
        super(OthelloCNN, self).__init__()

        self.conv1 = Sequential(
            Conv2d(3, 64, kernel_size=3, padding=1, stride=1),
            BatchNorm2d(64),
            ReLU() )

        self.conv2 = Sequential(
            Conv2d(64, 64, kernel_size=3, padding=1, stride=1),
            BatchNorm2d(64),
            ReLU())

        self.conv3 = Sequential(
            Conv2d(64, 128, kernel_size=3, padding=1, stride=1),
            BatchNorm2d(128),
            ReLU())

        self.conv4 = Sequential(
            Conv2d(128, 128, kernel_size=3, padding=1, stride=1),
            BatchNorm2d(128),
            ReLU())

        self.conv5 = Sequential(
            Conv2d(128, 256, kernel_size=3, padding=1, stride=1),
            BatchNorm2d(256),
            ReLU())

        self.conv6 = Sequential(
            Conv2d(256, 256, kernel_size=3, padding=1, stride=1),
            BatchNorm2d(256),
            ReLU())

        self.conv7 = Sequential(
            Conv2d(256, 256, kernel_size=3, padding=1, stride=1),
            BatchNorm2d(256),
            ReLU())
        
        self.conv8 = Sequential(
            Conv2d(256, 256, kernel_size=3, padding=1, stride=1),
            BatchNorm2d(256),
            ReLU())

        self.fc1 = Linear( 256 * 8 * 8, 128 )

        self.fc2 = Linear( 128, 60 )

    def forward(self, x):
        
        x = self.conv1(x)
#         print(x.size())
        x = self.conv2(x)
#         print(x.size())
        x = self.conv3(x)
#         print(x.size())
        x = self.conv4(x)
#         print(x.size())
        x = self.conv5(x)
#         print(x.size())
        x = self.conv6(x)
#         print(x.size())
        x = self.conv7(x)
#         print(x.size())
        x = self.conv8(x)
#         print(x.size())
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
#         print(x.size())
        x = self.fc2(x)
#         print(x.size())

        return x
