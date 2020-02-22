#!/usr/bin/env python3
import os
import tarfile
import silence_tensorflow
import numpy as np
import tensorflow as tf
from PIL import Image
from six.moves import urllib


# avoid removing by the import rearrangement
if silence_tensorflow:
    pass

def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--path',
                        dest='path',
                        required=True,
                        help='An absolute path to a folder with stored screenshots from cameras.')
    options = parser.parse_args()

    return options


options = get_arguments()

MODEL_NAME = 'xception_coco_voctrainaug'

_DOWNLOAD_URL_PREFIX = 'http://download.tensorflow.org/models/'
_MODEL_URLS = {
    'mobilenetv2_coco_voctrainaug':
        'deeplabv3_mnv2_pascal_train_aug_2018_01_29.tar.gz',
    'mobilenetv2_coco_voctrainval':
        'deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz',
    'xception_coco_voctrainaug':
        'deeplabv3_pascal_train_aug_2018_01_04.tar.gz',
    'xception_coco_voctrainval':
        'deeplabv3_pascal_trainval_2018_01_04.tar.gz',
}
_TARBALL_NAME = 'deeplab_model.tar.gz'
SAMPLE_IMAGE = 'image1'
_SAMPLE_URL = ('https://github.com/tensorflow/models/blob/master/research/'
               'deeplab/g3doc/img/%s.jpg?raw=true')
LABEL_NAMES = np.asarray([
    'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
    'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
    'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
])
SAMPLE_IMAGE = 'image1'  # @param ['image1', 'image2', 'image3']
IMAGE_URL = ''  # @param {type:"string"}


# https://colab.research.google.com/github/tensorflow/models/blob/master/research/deeplab/deeplab_demo.ipynb#scrollTo
# =vN0kU6NJ1Ye5
class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()
        model_dir = './models/'  # tempfile.mkdtemp()
        tf.gfile.MakeDirs(model_dir)
        tarball_path = os.path.join(model_dir, MODEL_NAME + _TARBALL_NAME)
        if not os.path.exists(tarball_path):
            print('Downloading the training model, this might take a while')
            urllib.request.urlretrieve(_DOWNLOAD_URL_PREFIX + _MODEL_URLS[MODEL_NAME],
                                       tarball_path)
            print('Downloading has been completed')

        print('Starting the training model')

        graph_def = None
        # Extract frozen graph from tar archive.
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise Exception('Cannot find inference graph in the tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)
        print('The training model has been initialized')

    def run(self, image):
        """Runs inference on a single image.

        Args:
          image: A PIL.Image object, raw input image.

        Returns:
          resized_image: RGB image resized from original input image.
          seg_map: Segmentation map of `resized_image`.
        """
        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
                    self.OUTPUT_TENSOR_NAME,
                    feed_dict={
                        self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]
                    })
        seg_map = batch_seg_map[0]
        return resized_image, seg_map

    def get_labels_from_image_file(self, image_path):
        """Inferences DeepLab model and return a set of labels."""
        try:
            original_im = Image.open(image_path)
        except IOError:
            raise Exception('Cannot open image, please check the file: ' + image_path)
        resized_im, seg_map = self.run(original_im)
        unique_labels = np.unique(seg_map)
        labels = set()
        for label in LABEL_NAMES[unique_labels]:
            labels.add(label)
        return labels


def get_all_images_from_path(path):
    screenshots = []
    for file in os.listdir(path):
        if 'jpg' in file:
            screenshots.append(f"{path}{file}")

    screenshots = screenshots.copy()
    screenshots.sort()
    return screenshots


def main():
    options = get_arguments()
    model = DeepLabModel()

    screenshots = get_all_images_from_path(options.path)

    for screenshot_path in screenshots:
        print(f'Processing [{screenshot_path}]', end='', flush=True)
        labels = model.get_labels_from_image_file(image_path=screenshot_path)
        if labels:
            print(f" - [{'; '.join(labels)}]")


if __name__ == '__main__':
    main()
