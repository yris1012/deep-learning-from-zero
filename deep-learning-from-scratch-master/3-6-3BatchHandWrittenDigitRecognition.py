# 3-6-1HandWrittenDigitRecognition.pyのミニバッチ学習編

# MNISTを用いた手書き数字認識
# 学習済みのパラメータを用いてニューラルネットワークの推論処理だけを実装
# なお、この推論処理を「ニューラルネットワークの順方向伝播(forward propagation)とも言う

import sys, os
sys.path.append(os.pardir) # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from dataset.mnist import load_mnist
import pickle

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

(x_train, t_train), (x_test, t_test) = \
  load_mnist(flatten=True, normalize=False)
# load_mnistのとる引数について(3種類ある)
# flatten=Trueで入力画像(1 x 28 x 28)を一次元配列(要素:784個)にする
# normilize=Trueで入力画像を0.0~1.0の値に正規化する(今回はしない)
# one_hot_label=Trueで正解となるラベルが1,それ以外が0の配列。Falseのときは7, 2といった正解のラベルがそのまま格納される

# それぞれのデータの形状を出力
print(x_train.shape) # (60000, 784)
print(t_train.shape) # (60000, ) 訓練画像が60000枚
print(x_test.shape) # (10000, 784)
print(t_test.shape) # (10000, ) テスト画像が10000枚

# 以下より、推論処理を行うニューラルネットワークを実装
# 入力層を784個、出力層を10個のニューロンで構成
# 隠れ層は2つ、隠れ層1は50個、隠れ層2は100個のニューロンを持つ

# モデルの定義
def get_data():
  (x_train, t_train), (x_test, t_test) = \
    load_mnist(normalize=True, flatten=True, one_hot_label=False)
    # normalize=True により、画像の各ピクセルの値を255で除算しデータの値が0.0~1.0に収まるように変換される
    # このようにデータをある決まった範囲に変換する処理を「正規化」という
  return x_test, t_test

def init_network(): # 学習済みの重みパラメータを読み込む
  with open("/Users/yuri/sophia/deep-learning-from-zero/deep-learning-from-scratch-master/ch03/sample_weight.pkl", 'rb') as f:
    network = pickle.load(f)
  return network

def predict(network, x):
  W1, W2, W3 = network['W1'], network['W2'], network['W3']
  b1, b2, b3 = network['b1'], network['b2'], network['b3']

  a1 = np.dot(x, W1) + b1
  z1 = sigmoid(a1)
  a2 = np.dot(z1, W2) + b2
  z2 = sigmoid(a2)
  a3 = np.dot(z2, W3) + b3
  y = sigmoid(a3)
  return y


# 認識精度(どれだけ正しく分類できるか)を評価
x, t = get_data()
network = init_network()

batch_size = 100 # バッチの数
accuracy_cnt = 0
for i in range(0 ,len(x), batch_size):
  x_batch = x[i:i+batch_size] # 先頭から100枚(batch_size)ずつ取り出す
  y_batch = predict(network, x_batch)
  p = np.argmax(y_batch, axis=1)
  # axis=1により100x10の配列の1次元めの要素ごとに(1次元めを軸として)、最大値にindexを見つけることを指定(最初の次元は0次元)
  accuracy_cnt += np.sum(p == t[i:i+batch_size])

print( "Accuracy:" + str(float(accuracy_cnt) / len(x)) )
# Accuracy:0.9352
