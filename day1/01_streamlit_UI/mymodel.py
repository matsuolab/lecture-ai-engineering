import torch
from torch import nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms

class Cifar10Model(nn.Module):
    def __init__(self, activation = "ReLU", negative_slope=0.01):
        # negative_slope : when activation is LeakyReLU, user select this paramater. 
        super().__init__()
        self.conv1 = nn.Conv2d(3, 4, kernel_size=5)
        self.conv2 = nn.Conv2d(4, 8, kernel_size=5)

        self.pool = nn.MaxPool2d(kernel_size=2)

        self.conv3 = nn.Conv2d(8, 16, kernel_size=5)
        self.conv4 = nn.Conv2d(16, 32, kernel_size=5)

        self.fc1 = nn.Linear(32*4*4, 128)
        self.fc2 = nn.Linear(128, 32)
        self.fc3 = nn.Linear(32, 10)

        self.activation = nn.ReLU()
        if activation == "ReLU":
            self.activation = nn.ReLU()
        elif activation == "LeakyReLU":
            self.activation = nn.LeakyReLU(negative_slope=negative_slope)
        elif activation == "Sigmoid":
            self.activation = nn.Sigmoid()
        elif activation == "GLU":
            self.activation = nn.GLU()

    def forward(self, x):
        batch_size = x.shape[0]
        x = self.activation(self.conv1(x))
        x = self.activation(self.conv2(x))
        
        x = self.pool(x)

        x = self.activation(self.conv3(x))
        x = self.activation(self.conv4(x))

        x = x.reshape(batch_size, -1)

        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc3(x))

        return x
    
class trainer:
    def __init__(self, activation="ReLU", negative_slope = 0.01, optimizer = "Adam", lr = 0.001):
        self.model = Cifar10Model(activation=activation, negative_slope=negative_slope)
        # デバイス設定（GPUが使える場合はGPUを使う）
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # データ変換：Tensor化と標準化
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        print("init")

        # CIFAR-10 データセット読み込み
        train_dataset = torchvision.datasets.CIFAR10(
            root='./data', train=True, download=True, transform=transform)
        test_dataset = torchvision.datasets.CIFAR10(
            root='./data', train=False, download=True, transform=transform)

        self.train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
        self.test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
        # 損失関数と最適化手法の設定
        self.criterion = nn.CrossEntropyLoss()

        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        if optimizer == "Adam":
            self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        elif optimizer == "AdamW":
            self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        elif optimizer == "Adadelta":
            self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        elif optimizer == "RMSprop":
            self.optimizer = optim.RMSprop(self.model.parameters(), lr=lr)
        elif optimizer == "Adagrad":
            self.optimizer = optim.Adagrad(self.model.parameters(), lr=lr)
        elif optimizer == "SGD":
            self.optimizer = optim.SGD(self.model.parameters(), lr=lr)
    # 学習ループ
    def train_model(self, num_epochs=10):
        accuracy = []
        loss_array = []

        accuracy_valid = []
        for epoch in range(num_epochs):
            print(num_epochs)
            self.model.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for images, labels in self.train_loader:
                images, labels = images.to(self.device), labels.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                running_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

            accuracy.append(100 * correct / total)
            loss_array.append(running_loss / len(self.train_loader))

            # accuracy_valid.append(self.evaluate_model())
            print(self.evaluate_model())
            # print(f"Epoch [{epoch+1}/{num_epochs}], "
            #     f"Loss: {running_loss/len(train_loader):.4f}, "
            #     f"Accuracy: {100*correct/total:.2f}%")
        # return accuracy, loss_array, accuracy_valid
        return accuracy, loss_array, self.evaluate_model()
    # 評価関数
    def evaluate_model(self):
        self.model.eval()
        correct = 0
        total = 0

        accuracy = 0

        with torch.no_grad():
            for images, labels in self.test_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
        
        accuracy = 100 * correct / total
        # print(f'Test Accuracy: {100 * correct / total:.2f}%')
        return accuracy 
        # 実行
        # train_model(num_epochs=10)
        # evaluate_model()
        
if __name__ == "__main__":
    model = Cifar10Model()

    # デバイス設定（GPUが使える場合はGPUを使う）
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # データ変換：Tensor化と標準化
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # CIFAR-10 データセット読み込み
    train_dataset = torchvision.datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform)
    test_dataset = torchvision.datasets.CIFAR10(
        root='./data', train=False, download=True, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

    # 損失関数と最適化手法の設定
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 学習ループ
    def train_model(num_epochs=10):
        for epoch in range(num_epochs):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for images, labels in train_loader:
                images, labels = images.to(device), labels.to(device)

                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

            print(f"Epoch [{epoch+1}/{num_epochs}], "
                f"Loss: {running_loss/len(train_loader):.4f}, "
                f"Accuracy: {100*correct/total:.2f}%")

    # 評価関数
    def evaluate_model():
        model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

        print(f'Test Accuracy: {100 * correct / total:.2f}%')

    # 実行
    train_model(num_epochs=10)
    evaluate_model()