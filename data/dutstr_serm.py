import os
import glob
import data


# dataset for DUTS-TR + SeRM
class DUTSTRSERM(data.BaseDataset):
    def __init__(self, phase, opt):
        root = opt.dataset_root
        self.name = "DUTS-TR_SeRM5_neg"
        
        dir_MASK, dir_IMG = self.get_subdir()
        self.MASK_paths = sorted(glob.glob(os.path.join(root, dir_MASK, "*.png")))
        self.IMG_paths = sorted(glob.glob(os.path.join(root, dir_IMG, "*")))

        super().__init__(phase, opt)

    def get_subdir(self):
        dir_MASK = "{}/{}-Mask".format(self.name, self.name)
        dir_IMG = "{}/{}-Image".format(self.name, self.name)
        
        return dir_MASK, dir_IMG