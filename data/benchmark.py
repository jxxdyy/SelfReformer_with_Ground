import os
import glob
import data


# for vairous benchmark datasets
class Benchmark(data.BaseDataset):
    def __init__(self, phase, opt):
        print("phase :", phase)
        root = opt.dataset_root
        if phase == "test" and opt.test_dataset != "":
            self.name = opt.test_dataset.split('_')[1]
        else:
            self.name = opt.dataset.split('_')[1]

        dir_MASK, dir_IMG = self.get_subdir()
        
        if self.name == 'HKUIS':
            self.MASK_paths = sorted(glob.glob(os.path.join(root, dir_MASK, "*.png")))
            self.IMG_paths = sorted(glob.glob(os.path.join(root, dir_IMG, "*.png")))
        else:
            self.MASK_paths = sorted(glob.glob(os.path.join(root, dir_MASK, "*")))
            self.IMG_paths = sorted(glob.glob(os.path.join(root, dir_IMG, "*")))
        

        super().__init__(phase, opt)

    def get_subdir(self):
        dir_MASK = "benchmark/{}/{}-Mask".format(self.name, self.name)
        dir_IMG = "benchmark/{}/{}-Image".format(self.name, self.name)

        
        return dir_MASK, dir_IMG