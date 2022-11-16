import argparse


class Hparams:
    parser = argparse.ArgumentParser()

    parser.add_argument('--workspace', default='default', type=str)

    # Model
    parser.add_argument('--batch_size', default=32, type=int)
    parser.add_argument('--embedding_size', default=32, type=int)
    parser.add_argument('--n_layers', default=2, type=int)
    parser.add_argument('--hidden_size', default=512, type=int)
    parser.add_argument('--dropout', default=0.2, type=float)
    parser.add_argument('--lr', default=0.001, type=float)
    parser.add_argument('--grad_clip', default=0.1, type=float)
    parser.add_argument('--temperature', default=1.0, type=float)

    # Training
    parser.add_argument('--data_path', default='/root/data/top10000.txt', type=str)
    parser.add_argument('--data_prefix', default='//JavascriptTop2000Functions\n', type=str)
    parser.add_argument('--max_length', default=1000, type=int)
    parser.add_argument('--split_length', default=-1, type=int)
    parser.add_argument('--embedding_level', default='char', type=str)
    parser.add_argument('--vocab_size', default=-1, type=int)
    parser.add_argument('--epoch', default=10, type=int)
    parser.add_argument('--gpu', default=0, type=int)
    parser.add_argument('--save_every_epoch', default=1, type=int)

    # generating
    parser.add_argument('--gen_model', default='workspace/default/model_10.ckpt', type=str)
    parser.add_argument('--gen_prefix', default='function(', type=str)
    parser.add_argument('--gen_file', default='gen.txt', type=str)
    parser.add_argument('--gen_number', default=10000, type=int)
    parser.add_argument('--gen_batch_size', default=64, type=int)
    parser.add_argument('--max_gen_length', default=1000, type=int)
    parser.add_argument('--segment_length', default=1000, type=int)
    parser.add_argument('--sample', default=False, type=bool)


hparams = Hparams().parser.parse_args()
