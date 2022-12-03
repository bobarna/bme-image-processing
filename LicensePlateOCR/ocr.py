import sys
import os
import cv2
import pdb
import json
import math
import pickle
import logging
import warnings
from tqdm import *
import numpy as np
import torch
from torch import nn
from torch.utils.data.sampler import SubsetRandomSampler
import torchvision
from torch.utils.data import random_split
from argparse import ArgumentParser

from src.options.opts import base_opts
from src.criterions.ctc import CustomCTCLoss
from src.utils.utils import *
from src.models.crnn import CRNN
from src.data.synth_dataset import SynthDataset, SynthCollator
from src.data.alphabets import *

warnings.filterwarnings("ignore")
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
torch.manual_seed(0)
np.random.seed(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

use_cuda = False


def detect_characters(args):
    """
    Performs character recognition
    Returns the predicted text entries
    """

    loader = torch.utils.data.DataLoader(args.data,
                                         batch_size=args.batch_size,
                                         collate_fn=args.collate_fn)
    model = args.model
    model.eval()
    converter = OCRLabelConverter(args.alphabet)
    labels, predictions = [], []
    for iteration, batch in enumerate(tqdm(loader)):
        input_ = batch['img'].to(device)
        logits = model(input_).transpose(1, 0)
        logits = torch.nn.functional.log_softmax(logits, 2)
        logits = logits.contiguous().cpu()
        T, B, H = logits.size()
        pred_sizes = torch.LongTensor([T for i in range(B)])
        probs, pos = logits.max(2)
        pos = pos.transpose(1, 0).contiguous().view(-1)
        sim_preds = converter.decode(pos.data, pred_sizes.data, raw=False)
        predictions.extend(sim_preds)
    return predictions


def main(**kwargs):
    parser = ArgumentParser()
    base_opts(parser)
    args = parser.parse_args()
    args.data = SynthDataset(args)
    args.collate_fn = SynthCollator()
    args.alphabet = full_alphabet
    args.nClasses = len(args.alphabet)

    model = CRNN(args)
    if (use_cuda):
        model = model.cuda()

    resume_file = os.path.join(args.save_dir, args.name, 'best.ckpt')
    if os.path.isfile(resume_file):
        print('Loading OCR model %s' % resume_file)
        checkpoint = torch.load(resume_file)
        model.load_state_dict(checkpoint['state_dict'])
        args.model = model
        print('Extracting text')
        predictions = detect_characters(args)
        print('Prediction count ', len(predictions))
        print(predictions)
    else:
        print("=> no checkpoint found for OCR at '{}'".format(resume_file))
        print('Exiting')


if __name__ == '__main__':
    main()
