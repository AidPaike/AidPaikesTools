import torch
import os
import random
import math
import logging
import json

from conf import hparams
from typing import *


device = torch.device(f"cuda:{hparams.gpu}" if torch.cuda.is_available() else "cpu")


def logger_config(
        prefix: str = 'NULL',
        file_level: str = 'INFO',
        console_level: str = 'INFO',
        log_file: str = 'test.log'):
    logger = logging.getLogger()
    logger.setLevel('NOTSET')

    if prefix == 'NULL':
        BASIC_FORMAT = f'%(asctime)s - %(levelname)s: %(message)s'
    else:
        BASIC_FORMAT = f'[{prefix}]%(asctime)s - %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

    chlr = logging.StreamHandler()
    chlr.setFormatter(formatter)
    chlr.setLevel(console_level)

    fhlr = logging.FileHandler(log_file, encoding='utf-8')
    fhlr.setFormatter(formatter)
    fhlr.setLevel(file_level)

    logger.addHandler(chlr)
    logger.addHandler(fhlr)


def load_json(json_path, transfer=False):
    with open(json_path, 'r', encoding='utf-8') as f:
        _dict = json.load(f)

    if transfer:
        _dict = {int(key): value for key, value in _dict.items()}
    return _dict


def save_json(_dict, json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(_dict))


def get_batch_iter(preprocess, batch_size):
    train_data = preprocess.train_data
    token_to_idx = preprocess.token_to_idx
    unk_idx = preprocess.token_to_idx.get('<unk>')
    eos_idx = preprocess.token_to_idx.get('<eos>')
    pad_idx = preprocess.token_to_idx.get('<pad>')

    random.shuffle(train_data)

    batch_num = math.ceil(len(train_data) / batch_size)

    for i in range(batch_num):
        if i != batch_num - 1:
            batch_data = train_data[i * batch_size: (i+1) * batch_size]
        else:
            batch_data = train_data[i * batch_size:]

        curr_batch_size = len(batch_data)
        max_length = 0
        for line in batch_data:
            max_length = max(max_length, len(line))

        batch_data_tensor = torch.zeros(curr_batch_size, max_length + 1, device=device)
        target_data_tensor = torch.zeros(curr_batch_size, max_length + 1, dtype=torch.int64, device=device)

        for j, line in enumerate(batch_data):
            k = 0
            for k, token in enumerate(line):
                batch_data_tensor[j][k] = token_to_idx.get(token, unk_idx)
                if k >= 1:
                    target_data_tensor[j][k - 1] = token_to_idx.get(token, unk_idx)

            k += 1
            batch_data_tensor[j][k] = eos_idx
            target_data_tensor[j][k - 1] = eos_idx

            for n in range(k + 1, max_length + 1):
                batch_data_tensor[j][n] = pad_idx
            for n in range(k, max_length + 1):
                target_data_tensor[j][n] = pad_idx

        yield batch_data_tensor, target_data_tensor


def segmentation(prefix, segment_length):
    batch_num = math.ceil(len(prefix) / segment_length)

    for i in range(batch_num):
        if i != batch_num - 1:
            yield prefix[i * segment_length: (i+1) * segment_length]
        else:
            yield prefix[i * segment_length:]


def text2token(text: str, token_to_idx: dict, batch_size: int, embedding_level):

    token_tensor = torch.zeros(batch_size, len(text), device=device)
    for idx, char in enumerate(text):
        token_tensor = token_tensor.index_fill(dim=1,
                                               index=torch.tensor([idx], device=device),
                                               value=token_to_idx.get(char, token_to_idx.get('<unk>')))

    return token_tensor
