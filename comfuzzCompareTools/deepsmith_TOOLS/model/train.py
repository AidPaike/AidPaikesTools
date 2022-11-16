import os
import torch
import torch.nn as nn


from model import LSTM
from tqdm import tqdm


from preprocess import preprocessor
from conf import hparams
from utils import *


device = torch.device(f"cuda:{hparams.gpu}" if torch.cuda.is_available() else "cpu")


if __name__ == '__main__':
    workspace_path = os.path.join('workspace', hparams.workspace)
    save_json(hparams.__dict__, os.path.join(workspace_path, 'hparams.json'))
    save_json(preprocessor.token_to_idx, os.path.join(workspace_path, 'token_to_idx.json'))
    save_json(preprocessor.idx_to_token, os.path.join(workspace_path, 'idx_to_token.json'))

    token_to_idx = preprocessor.token_to_idx
    vocab_size = len(token_to_idx)
    assert vocab_size == preprocessor.token_number

    model = LSTM(vocab_size,
                 vocab_size,
                 hparams.embedding_size,
                 hparams.hidden_size,
                 hparams.n_layers,
                 device,
                 hparams.dropout)

    model = model.to(device)

    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=hparams.lr)

    print()
    print("Model training, please wait...")
    print("Note: Please do not terminate early, it is saved only when the model has been trained.")
    all_losses = []
    for e in tqdm(range(1, hparams.epoch + 1)):

        data_iter = get_batch_iter(preprocessor, hparams.batch_size)
        total_loss = 0
        n_batches = 0

        for idx, (input_batch, target_batch) in enumerate(data_iter):
            curr_batch_size = input_batch.size(0)

            hidden = model.init_hidden(curr_batch_size)
            model.zero_grad()

            logit, _ = model(input_batch, hidden)
            logit = logit / hparams.temperature
            logit_2d = logit.contiguous().view(-1, logit.size(2))
            target_batch = target_batch.contiguous().view(-1)

            loss = loss_function(logit_2d, target_batch)
            total_loss += loss
            loss.backward()

            nn.utils.clip_grad_norm_(model.parameters(), hparams.grad_clip)

            optimizer.step()
            n_batches += 1

        all_losses.append(total_loss/n_batches)

        print(f"Epoch: {e}, Loss: {total_loss/n_batches}")

        if e % hparams.save_every_epoch == 0:
            torch.save(model, os.path.join(workspace_path, f'model_{e}.ckpt'))

