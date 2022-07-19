import sys
import os
from CarryCARI_prj.settings import BASE_DIR

# sys.path.append('ml/encoder4editing')
# sys.path.append('ml/StyleCLIP')
# sys.path.append('ml/encoder4editing/utils')
# sys.path.append('ml')
# print(sys.path)

import torch
import clip

import torchvision.transforms as transforms
import torch
from argparse import Namespace
# from ml.encoder4editing.models.psp import pSp
from ml.StyleCLIP.global_directions.manipulate import Manipulator
import numpy as np

from PIL import Image
from ml.encoder4editing.utils.common import tensor2im
from ml.StyleCLIP.global_directions.MapTS import GetFs, GetBoundary, GetDt
import matplotlib.pyplot as plt

import dlib
from ml.encoder4editing.utils.alignment import align_face
import numpy as np
from PIL import Image


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

pwd = os.path.dirname(os.path.realpath(__file__))

os.chdir(os.path.join(BASE_DIR, 'ml/StyleCLIP/global_directions'))

os.system('python GetCode.py --dataset_name "ffhq" --code_type "w" ')
os.system('python GetCode.py --dataset_name "ffhq" --code_type "s" ')
os.system('python GetCode.py --dataset_name "ffhq" --code_type "s_mean_std" ')

os.chdir(pwd)

resize_dims = (256, 256)


def run_alignment(image_path):
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    aligned_image = align_face(filepath=image_path, predictor=predictor)
    print("Aligned image has shape: {}".format(aligned_image.size))
    return aligned_image


def display_alongside_source_image(result_image, source_image):
    res = np.concatenate([np.array(source_image.resize(resize_dims)),
                          np.array(result_image.resize(resize_dims))], axis=1)
    return Image.fromarray(res)


def run_on_batch(inputs, net):
    images, latents = net(inputs.to("cuda").float(), randomize_noise=False, return_latents=True)
    return images, latents


# main
def generate_imageclip(user_id, image_path, emotion):

    EXPERIMENT_ARGS = {
        "model_path": "ml/encoder4editing/e4e_ffhq_encode.pt"
    }
    EXPERIMENT_ARGS['transform'] = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])

    model_path = EXPERIMENT_ARGS['model_path']
    ckpt = torch.load(model_path, map_location='cpu')
    opts = ckpt['opts']

    # opts['checkpoint_path'] = model_path
    # opts = Namespace(**opts)
    # net = pSp(opts)
    # net.eval()
    # net.cuda()
    # print('Model successfully loaded!')
    #
    # fs3 = np.load('./npy/ffhq/fs3.npy')
    # M = Manipulator(dataset_name='ffhq')
    # np.set_printoptions(suppress=True)
