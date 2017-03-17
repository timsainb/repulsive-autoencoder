import argparse
import exp
from model_gaussian import get_latent_dim

parser = argparse.ArgumentParser()

parser.add_argument('ini_file', nargs='*', help="Ini file to use for configuration")

parser.add_argument('--prefix', dest="prefix", default="dcgan/trash", help="File prefix for the output visualizations and models.")
parser.add_argument('--lr', dest="lr", default="0.00005", type=float, help="Learning rate for RMS prop.")
parser.add_argument('--wd', dest="wd", type=float, default=0.0, help="Weight decay param")
parser.add_argument('--latent_dim', dest="latent_dim", type=int, default=100, help="Latent dimension")
parser.add_argument('--batch_size', dest="batch_size", default=100, type=int, help="Batch size.")
parser.add_argument('--nb_iter', dest="nb_iter", type=int, default=1300, help="Number of iterations")
parser.add_argument('--dataset', dest="dataset", default="mnist", help="Dataset to use: mnist/celeba")
parser.add_argument('--trainSize', dest="trainSize", type=int, default=0, help="Train set size (0 means default size)")
parser.add_argument('--testSize', dest="testSize", type=int, default=0, help="Test set size (0 means default size)")
parser.add_argument('--color', dest="color", default=1, type=int, help="color(0/1)")
parser.add_argument('--shape', dest="shape", default="64,64", help="image shape, currently only 64,64 supported")
parser.add_argument('--frequency', dest="frequency", type=int, default=20, help="image saving frequency")
parser.add_argument('--memory_share', dest="memory_share", type=float, default=0.45, help="fraction of memory that can be allocated to this process")
parser.add_argument('--verbose', dest="verbose", type=int, default=0, help="Logging verbosity: 0-silent, 1-verbose, 2-perEpoch")
parser.add_argument('--optimizer', dest="optimizer", type=str, default="adam", help="Optimizer, adam, rmsprop, sgd.")
parser.add_argument('--clipValue', dest="clipValue", type=float, default=0.01, help="Critic clipping range is (-clipValue, clipValue)")
parser.add_argument('--use_bn_gen', dest="use_bn_gen", type=int, default=0, help="Use batch normalization in generator 0/1")
parser.add_argument('--use_bn_disc', dest="use_bn_disc", type=int, default=0, help="Use batch normalization in discriminator 0/1")
parser.add_argument('--gen_size', dest="gen_size", default="small", help="small/large")
parser.add_argument('--disc_size', dest="disc_size", default="large", help="small/large")

args_param = parser.parse_args()
args = exp.mergeParamsWithInis(args_param)
ini_file = args.prefix + ".ini"
exp.dumpParams(args, ini_file)

def getArgs():
    if args.color == 1:
        args.color = True
    else:
        args.color = False

    args.use_bn_gen = (args.use_bn_gen == 1)
    args.use_bn_disc = (args.use_bn_disc == 1)

    args.shape = tuple(map(int, str(args.shape).split(",")))
    return args