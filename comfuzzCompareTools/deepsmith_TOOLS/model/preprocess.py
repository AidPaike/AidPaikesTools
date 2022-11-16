import os
import logging
import math

from tqdm import tqdm
from collections import Counter

from conf import hparams
from utils import logger_config

# create workspace
if not os.path.exists('workspace'):
    os.mkdir('workspace')
workspace_path = os.path.join('workspace', hparams.workspace)
if not os.path.exists(workspace_path):
    os.mkdir(workspace_path)
else:
    raise FileExistsError("Specified workspace already exists. Please reenter it.")

log_file = os.path.join(workspace_path, 'log.txt')
logger_config(prefix='train', log_file=log_file)
logging.info(f"This workspace is: {workspace_path}")


class Preprocessor:
    def __init__(self, hparams):
        self.hparams = hparams
        self.data_path = hparams.data_path
        self.max_length = hparams.max_length
        self.split_length = hparams.split_length
        self.embedding_level = hparams.embedding_level

        train_data = self.read_data(self.data_path, hparams.data_prefix)
        self.init_data_number = len(train_data)
        train_data = self.preprocess(train_data)
        self.train_data = train_data

        self.token_to_idx, self.idx_to_token, self.token_number = self.statistic(train_data, hparams.vocab_size)

    @staticmethod
    def read_data(data_path, prefix):
        with open(data_path, 'r', encoding='utf-8') as f:
            content = f.read()

        functions = content.split(prefix)[1:]
        functions = [i.strip() for i in functions]

        return functions

    def preprocess(self, train_data):
        train_data = self.limit_max_length(train_data, self.max_length)
        train_data = self.data_split(train_data, self.split_length)
        train_data = self.tokenize(train_data, self.embedding_level)

        return train_data

    @staticmethod
    def limit_max_length(train_data, max_length):
        if max_length == -1:
            return train_data
        return [i for i in tqdm(train_data) if len(i) <= max_length - 1]  # -1 for <eos>

    @staticmethod
    def data_split(train_data, split_length):
        if split_length == -1:
            return train_data

        def split(text, length):
            if len(text) <= length:
                return [text]

            count = math.ceil(len(text) / length)
            split_data = []
            for i in range(count):
                if i != count - 1:
                    split_data.append(text[i * length: (i + 1) * length])
                else:
                    split_data.append(text[i * length:])
            return split_data

        logging.info('Spliting...')
        split_data = []
        for line in tqdm(train_data):
            split_data += split(line, split_length)
        return split_data

    @staticmethod
    def tokenize(train_data, embedding_level):
        logging.info(f'Tokenize...')

        def char_tokenize(code):
            return list(code)

        tokenized_data = []
        if embedding_level == 'char':
            for line in tqdm(train_data):
                tokenized_data.append(char_tokenize(line))

        else:
            raise ValueError('Embedding_level error, only accept "char"!')

        return tokenized_data

    def statistic(self, train_data, vocab_size):
        token_to_idx = {}
        max_length_actual = 0

        # add <eos> & <pad> & <sos> & <unk>
        token_to_idx['<eos>'] = len(token_to_idx)
        token_to_idx['<pad>'] = len(token_to_idx)
        token_to_idx['<sos>'] = len(token_to_idx)
        token_to_idx['<unk>'] = len(token_to_idx)

        counter = Counter()
        for tokenized_line in train_data:
            counter.update(tokenized_line)
            max_length_actual = max(max_length_actual, len(tokenized_line))

        if vocab_size == -1:
            most_common_token = counter.most_common(len(counter))
        else:
            most_common_token = counter.most_common(vocab_size - 4)
        for idx, item in enumerate(most_common_token, start=len(token_to_idx)):
            token_to_idx[item[0]] = idx

        idx_to_token = {v: k for k, v in token_to_idx.items()}

        logging.info(f"Statistic info:")
        logging.info(f"Trainging data file: {self.data_path}")
        logging.info(f"Trainging data number: {len(train_data)}")
        logging.info(f"Vocab size: {len(token_to_idx)}")

        return token_to_idx, idx_to_token, len(token_to_idx)


logging.info("Preprocessing...")
preprocessor = Preprocessor(hparams)
