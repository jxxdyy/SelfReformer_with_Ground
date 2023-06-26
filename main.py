import json
import importlib
import torch
from option import get_option
from solver import Solver
from tester import Tester
from utils import LogWritter
import glob
from tqdm import tqdm
import time


def main():
    opt = get_option()
    torch.manual_seed(opt.seed)

    module = importlib.import_module("model.{}".format(opt.model.lower()))
    logger = LogWritter(opt)

    if not opt.test_only:
        msg = json.dumps(vars(opt), indent=4)
        print(msg)
        logger.update_txt(msg + '\n', mode='w')


    # start_time = time.time_ns()
    
    if opt.test_only:
        
        tester = Tester(module, opt)
        ckpt = glob.glob('{}/{}'.format(opt.ckpt_root, opt.pretrain))

        assert len(ckpt)!=0, "cannot find checkpoint {} in {}".format(opt.pretrain, opt.ckpt_root)
        print("Evaluate {} (loaded from {}) on {} dataset".format(opt.model,
                                                                  ckpt[0],
                                                                  opt.test_dataset.split('_')[1]))

        tester.evaluate(path=ckpt[0])
        msg = "ckpt:{}\n".format(ckpt[0])
        print(msg)
        print('done testing')
    else:
        solver = Solver(module, opt)
        solver.fit()


    # end_time = time.time_ns()
    # print('전체 코드 실행 시간(나노초 ns) : <<%10d>>' % (end_time - start_time)) 


if __name__ == "__main__":
    main()
