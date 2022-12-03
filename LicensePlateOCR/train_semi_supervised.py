import os
import pdb
import pickle
import logging
import shutil

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from argparse import ArgumentParser
import itertools 
from torch.utils.data import random_split

from src.modules.trainer import OCRTrainer
from src.utils.utils import EarlyStopping, gmkdir
from src.models.crnn import CRNN
from src.options.ss_opts import base_opts
from src.data.synth_dataset import  SynthCollator
from src.criterions.ctc import CustomCTCLoss 
from src.utils.top_sampler import SamplingTop
from train import Learner
from src.data.alphabets import *
from src.data.synth_dataset import *

class LearnerSemi(Learner):
    def __init__(self, model, optimizer, savepath=None, resume=False):
        self.model = model
        self.optimizer = optimizer
        self.savepath = os.path.join(savepath, 'finetuned.ckpt')
        self.cuda = torch.cuda.is_available() 
        self.cuda_count = torch.cuda.device_count()
        if self.cuda:
            self.model = self.model.cuda()
        self.epoch = 0
        if self.cuda_count > 1:
            print("Let's use", torch.cuda.device_count(), "GPUs!")
            self.model = nn.DataParallel(self.model)
        self.best_score = None

    def freeze(self, index, boolean=False):
        layer = self.get_layer_groups()[index]
        for params in layer.parameters():
            params.requires_grad = boolean

    def freeze_all_but(self, index):
        n_layers = len(self.get_layer_groups())
        for i in range(n_layers):
            self.freeze(i)
        self.freeze(index, boolean=True)

    def unfreeze(self, index):
        self.freeze(index, boolean=True)

    def unfreeze_all(self):
        n_layers = len(self.get_layer_groups())
        for i in range(n_layers):
            self.unfreeze(i)

    def child(self, x):
        return list(x.children())
    
    def recursive_(self, child):
        if hasattr(child, 'children'):
            if len(self.child(child)) != 0:
                child = self.child(child)
                return self.recursive_(child)
        return child

    def get_layer_groups(self):
        children = []
        for child in self.child(self.model):
            children.extend(self.recursive_(child))
        children = [child for child in children if list(child.parameters())]
        return children
        

is_cuda_enabled = False

if __name__ == '__main__':
    parser = ArgumentParser()
    base_opts(parser)
    args = parser.parse_args()
    # Loading souce data
    args.imgdir = 'data/cutouts'
    args.source_data = SynthDataset(args)
    args.collate_fn = SynthCollator()

    args.alphabet = reduced_alphabet
    args.nClasses = len(args.alphabet)
    model = CRNN(args)
    if (is_cuda_enabled):
        model = model.cuda()

    args.criterion = CustomCTCLoss()
    save_path = os.path.join(args.save_dir, args.name)
    gmkdir(save_path)
    gmkdir(args.log_dir)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    # Loading specific model to get top samples
    load_prev_model = False
    if (load_prev_model):
        resume_file = save_path + '\\' + 'finetuned_ocr_nn.ckpt'
        print('Loading model %s'%resume_file)
        checkpoint = torch.load(resume_file)
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['opt_state_dict'])
    
    # Generating top samples
    args.model = model
    args.imgdir = 'target_top'
    finetunepath = args.path + '\\' + args.imgdir
    gmkdir(finetunepath)
    # Joining source and top samples
    args.top_samples = SynthDataset(args)
    args.data_train = torch.utils.data.ConcatDataset([args.source_data, args.top_samples])
    sampler = SamplingTop(args)
    sampler.get_samples(train_on_pred=args.train_on_pred, 
        combine_scoring=args.combine_scoring)
    print('Traininig Data Size:{}\nVal Data Size:{}'.format(
        len(args.data_train), len(args.data_val)))
    learner = LearnerSemi(args.model, optimizer, savepath=save_path, resume=args.resume)
    learner.fit(args)
    shutil.rmtree(finetunepath)