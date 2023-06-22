import os
import glob
import data


# dataset for DUTS-TR + SeRM
class DUTSTRSERM(data.BaseDataset):
    def __init__(self, phase, opt):
        root = opt.dataset_root

        dir_MASK, dir_IMG = self.get_subdir()
        self.MASK_paths = sorted(glob.glob(os.path.join(root, dir_MASK, "*.png")))
        self.IMG_paths = sorted(glob.glob(os.path.join(root, dir_IMG, "*")))

        super().__init__(phase, opt)

    def get_subdir(self):
        dir_MASK = "DUTS_SeRM-TR/DUTS_SeRM-TR-Mask"
        dir_IMG = "DUTS_SeRM-TR/DUTS_SeRM-TR-Image"
        
        return dir_MASK, dir_IMG