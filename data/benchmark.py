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
            self.MASK_paths = sorted(glob.glob(os.path.join(root, dir_MASK, "*.png")))
            self.IMG_paths = sorted(glob.glob(os.path.join(root, dir_IMG, "*.jpg")))
        
        
        #self.IMG_paths = sorted(glob.glob(os.path.join(root, "dataset_root/dataset/STheReO_Dataset/kaist_afternoon/image/case2/HE/*.png")))
        #self.IMG_paths = sorted(glob.glob(os.path.join(root, "dataset_root/dataset/STheReO_Dataset/valley_morning/image/HE2/*.png")))
        #self.IMG_paths = sorted(glob.glob(os.path.join(root, "dataset_root/dataset/Private_Dataset/neubie24/campus/230516/campus_seq2/HE/*.png")))

        super().__init__(phase, opt)

    def get_subdir(self):
        # dir_MASK = "benchmark/{}/Masks".format(self.name)
        # dir_IMG = "benchmark/{}/Images".format(self.name)
        dir_MASK = "benchmark/{}/DUTS-TE-Mask".format(self.name)
        dir_IMG = "benchmark/{}/DUTS-TE-Image".format(self.name)

        
        return dir_MASK, dir_IMG