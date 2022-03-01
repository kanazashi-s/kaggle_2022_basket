import os
import numpy as np
import matplotlib.pyplot as plt


def main():
    in_out_dict = {
        'data/raw/train/good': 'data/processed/train/good',
        'data/raw/test/good': 'data/processed/test/good',
        'data/raw/test/crack': 'data/processed/test/crack',
    }

    for input_path, output_path in in_out_dict.items():
        imgs, _ = load_images_labels(input_path)
        imgs = preprocess_img(imgs)
        np.save(output_path, imgs)


def load_images_labels(img_dir: str):
    img_names = os.listdir(img_dir)

    # 指定されたディレクトリ直下の画像をすべて読み込み、リスト imgs に格納する
    imgs = []
    for img_name in img_names:
        img_path = f'{img_dir}/{img_name}'
        imgs.append(plt.imread(img_path))

    # NumPy 配列に変換
    imgs_array = np.array(imgs)

    # 画像の枚数と同じ要素数のラベルの配列 labels_array を作成する
    labels_array = np.empty((len(img_names)))
    # ディレクトリ名 img_dir の末尾が good であれば 0 、それ以外であれば 1 で埋める
    is_good = 0 if img_dir[-4:] == 'good' else 1
    labels_array.fill(is_good)

    return imgs_array, labels_array


def preprocess_img(imgs: np.array):
    imgs = imgs.reshape(imgs.shape[0], 256, 256, 3).astype('float32')
    imgs = (imgs - 127.5) / 127.5  # Normalize the images to [-1, 1]

    return imgs


if __name__ == '__main__':
    main()
