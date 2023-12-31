import importlib
from termios import N_MOUSE
import numpy as np
import skimage.io as io
import skimage.color as color
import torch
from augments import Augment
from tqdm import tqdm
import os


def generate_loader(phase, opt):
    cname = opt.dataset.replace("_", "")
    if phase == "test":
        mname = importlib.import_module("data.benchmark")
        cname = "Benchmark" # Benchmark class
    else:
        if "DUTSTR" == opt.dataset:
            mname = importlib.import_module("data.dutstr")
        
        elif "SERM" in opt.dataset:
            mname = importlib.import_module("data.dutstr_serm")
            
        elif "benchmark" in opt.dataset:
            mname = importlib.import_module("data.benchmark")
            cname = "Benchmark"
        else:
            raise ValueError("Unsupported dataset: {}".format(opt.dataset))

    kwargs = {
        "batch_size": opt.batch_size if phase == "train" else 1,
        "num_workers": opt.num_workers if phase == "train" else 1,
        "shuffle": phase == "train",
        "drop_last": phase == "train",
    }

    print("module_name :", mname)
    print("class_name :", cname)
    dataset = getattr(mname, cname)(phase, opt)
    num_samples = len(dataset)
    print("num_samples :", num_samples)

    if not num_samples > 0:
        raise ValueError("The dataset should have at least one sample.")
    
    return torch.utils.data.DataLoader(dataset, **kwargs)


class BaseDataset(torch.utils.data.Dataset):
    def __init__(self, phase, opt):
        print("Load dataset... (phase: {}, len: {})".format(phase, len(self.MASK_paths)))
        self.MASK, self.IMG = list(), list()

        for MASK_path, IMG_path in tqdm(zip(self.MASK_paths, self.IMG_paths), total=len(self.MASK_paths)):
            self.MASK += [io.imread(MASK_path)]
            self.IMG += [io.imread(IMG_path)]

        self.phase = phase
        self.opt = opt
        self.aug = Augment(self.opt)

    def __getitem__(self, index):
        if self.phase == "train":
            index = index % len(self.MASK)

        MASK, IMG = self.MASK[index], self.IMG[index]

        if len(MASK.shape) > 2:
            MASK = color.rgb2gray(MASK)  # shape of [h, w]
            
        NAME = (os.path.split(self.MASK_paths[index])[1]).split('.')[0]

        if len(IMG.shape) < 3:
            IMG = color.gray2rgb(IMG)

        if self.phase == "train":
            MASK, IMG = self.aug.crop(MASK, IMG)  # mask value [0, 1] because of resize
            MASK, IMG = self.aug.flip_and_rotate(MASK, IMG)

            IMG = np.ascontiguousarray(IMG.transpose((2, 0, 1)))
            IMG = self.aug.norm(self.aug.to_tensor(IMG) / 255.)
            MASK = self.aug.to_tensor(MASK).unsqueeze(0)

            return MASK, IMG  # , CTR
        else:
            IMG = self.aug.resize(IMG)
            IMG = np.ascontiguousarray(IMG.transpose((2, 0, 1)))
            IMG = self.aug.norm(self.aug.to_tensor(IMG) / 255.)
            MASK = self.aug.to_tensor(MASK).unsqueeze(0) / 255.  # [0,1]

            return MASK, IMG, NAME
        
        # IMG = self.aug.resize(IMG)
        # IMG = np.ascontiguousarray(IMG.transpose((2, 0, 1)))
        # IMG = self.aug.norm(self.aug.to_tensor(IMG) / 255.)
        
        # return IMG, NAME

    def __len__(self):
        return len(self.MASK)
    