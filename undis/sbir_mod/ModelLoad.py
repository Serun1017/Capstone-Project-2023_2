import torch

from .model.model import Model

from .utils.util import load_checkpoint


def load_model(args):
    model = Model(args)
    model = model.half()

    if args.load is not None:
        checkpoint = load_checkpoint(args.load)

    cur = model.state_dict()
    new = {k: v for k, v in checkpoint["model"].items() if k in cur.keys()}  # type:ignore
    cur.update(new)
    model.load_state_dict(cur)

    if len(args.choose_cuda) > 1:
        model = torch.nn.parallel.DataParallel(model.to("cuda"))
    model = model.cuda()

    model.eval()
    torch.set_grad_enabled(False)
    return model
