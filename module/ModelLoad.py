import torch

from .model.model import Model

from .utils.util import load_checkpoint

class ModelLoader :
    def __init__(self, args) :
        # prepare model
        self.model = Model(args)
        self.model = self.model.half()

        if args.load is not None:
            checkpoint = load_checkpoint(args.load)
        
        cur = self.model.state_dict()
        new = {k: v for k, v in checkpoint['model'].items() if k in cur.keys()} # type:ignore
        cur.update(new)
        self.model.load_state_dict(cur)

        if len(args.choose_cuda) > 1:
            self.model = torch.nn.parallel.DataParallel(self.model.to('cuda'))
        self.model = self.model.cuda()

        self.model.eval()
        torch.set_grad_enabled(False)

    def __getitem__(self) :
        return self.model

    def __call__(self, sk, im, stage='train', only_sa=False) :
        return self.model(sk, im, stage, only_sa)