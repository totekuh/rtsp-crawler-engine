#!/usr/bin/env python3
import json
import os
import tarfile

import numpy as np
import requests
import silence_tensorflow
import tensorflow as tf
from PIL import Image
from six.moves import urllib

# avoid removing by the import rearrangement
if silence_tensorflow:
    pass

DEFAULT_MODEL_PATH = './models/'


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--path',
                        dest='path',
                        required=True,
                        help='A path to a folder with stored screenshots from cameras.')
    parser.add_argument('--model-path',
                        dest='model_path',
                        default=DEFAULT_MODEL_PATH,
                        required=False,
                        help='A path to the folder with stored neural-network models. '
                        f'Default is {DEFAULT_MODEL_PATH}')
    parser.add_argument('--import-endpoint',
                        dest='import_endpoint',
                        required=False,
                        help='The endpoint of the backend API import service. '
                             'If this argument is given, the scripts sends discovered labels '
                             'to the backend API immediately')
    options = parser.parse_args()

    return options


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


# https://colab.research.google.com/github/tensorflow/models/blob/master/research/deeplab/deeplab_demo.ipynb#scrollTo
# =vN0kU6NJ1Ye5
class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self, model_dir):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()
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
            raise Exception(f'Cannot open image, please check the file: {image_path}')
        resized_im, seg_map = self.run(original_im)
        unique_labels = np.unique(seg_map)
        labels = []
        for label in LABEL_NAMES[unique_labels]:
            labels.append(label)
        return labels


def get_all_images_from_path(path):
    if not path.endswith('/'):
        path = f"{path}/"

    screenshots = []
    files = [file for file in os.listdir(path) if 'jpg' in file]
    for i, file in enumerate(files):
        print(f'Reading [{file}][{i}/{len(files)}]\r', end='', flush=True)
        screenshots.append(f"{path}{file}")

    screenshots = screenshots.copy()
    screenshots.sort()
    return screenshots


def main():
    options = get_arguments()

    model = DeepLabModel(options.model_path)

    screenshots = get_all_images_from_path(options.path)

    for i, screenshot_path in enumerate(screenshots):
        labels = model.get_labels_from_image_file(image_path=screenshot_path)
        print(f'Processing [{screenshot_path}][{i + 1}/{len(screenshots)}]', end='', flush=True)
        if labels:
            print(f" - [{'; '.join(labels)}]")

            # update the metadata file to include discovered labels
            json_file_name = screenshot_path.replace('.jpg', '.json')
            if os.path.exists(json_file_name):
                with open(json_file_name, 'r', encoding='utf-8') as f:
                    stored_camera_data = json.load(f)
                stored_camera_data['labels'] = [{
                    'name': label
                } for label in labels]
                with open(json_file_name, 'w', encoding='utf-8') as f:
                    json.dump(stored_camera_data, f)

                if options.import_endpoint:
                    print('Sending the labels to the backend API ', end='', flush=True)
                    try:
                        camera_update_params = {
                            'url': stored_camera_data['rtspUrl'],
                            'labels': [{
                                'name': label
                            } for label in labels]
                        }
                        resp = requests.put(options.import_endpoint, json=camera_update_params)
                        if resp.ok:
                            print(f' - HTTP/1.1 {resp.status_code}')
                        else:
                            print(f' - HTTP/1.1 {resp.status_code} {resp.json()}')
                    except Exception as e:
                        print(f' - {e}')


if __name__ == '__main__':
    main()
