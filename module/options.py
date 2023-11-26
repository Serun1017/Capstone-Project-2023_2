import argparse

class Option:
    def __init__(self):
        parser = argparse.ArgumentParser(description="args for model")

        # model
        parser.add_argument("--cls_number", type=int, default=100)
        parser.add_argument("--d_model", type=int, default=768)
        parser.add_argument("--d_ff", type=int, default=1024)
        parser.add_argument("--head", type=int, default=8)
        parser.add_argument("--number", type=int, default=1)
        parser.add_argument("--pretrained", default=True, action="store_false")
        parser.add_argument("--anchor_number", "-a", type=int, default=49)

        # test
        parser.add_argument("--load", "-l", type=str, default="./module/checkpoints/sketchy_ext/best_checkpoint.pth")
        parser.add_argument("--retrieval", "-r", type=str, default="rn", choices=["rn", "sa"])
        parser.add_argument("--testall", default=False, action="store_true", help="train/test scale")
        parser.add_argument("--test_sk", type=int, default=20)
        parser.add_argument("--test_im", type=int, default=20)
        parser.add_argument("--num_workers", type=int, default=4)
        parser.add_argument("--batch", type=int, default=20)

        # other
        parser.add_argument("--choose_cuda", "-c", type=str, default="0")
        parser.add_argument("--seed", type=int, default=2021, help="random seed.")

        self.parser = parser

    def parse(self):
        return self.parser.parse_args()
