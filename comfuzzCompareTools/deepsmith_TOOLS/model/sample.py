import torch
from utils import text2token, segmentation


def sample_multi(model, prefix, batch_size, max_gen_length, token_to_idx, idx_to_token, segment_length, temperature=1.0):

    with torch.no_grad():
        gen_code_list = [prefix] * batch_size

        hidden = model.init_hidden(batch_size)

        prefix_iter = segmentation(prefix, segment_length)
        for prefix in prefix_iter:
            input_batch = text2token(prefix, token_to_idx, batch_size, embedding_level='char')
            logit, hidden = model(input_batch, hidden)

        logit = logit / temperature
        logit_2d = logit[:, -1, :]
        prob = logit_2d.softmax(dim=1)

        _, topi = prob.topk(1)

        for idx in range(topi.size(0)):
            gen_code_list[idx] = gen_code_list[idx] + idx_to_token.get(int(topi[idx].data))

        for _ in range(max_gen_length):
            logit, hidden = model(topi, hidden)

            logit_2d = logit[:, -1, :]
            prob = logit_2d.softmax(dim=1)
            _, topi = prob.topk(1)

            for idx in range(topi.size(0)):
                gen_code_list[idx] = gen_code_list[idx] + idx_to_token.get(int(topi[idx].data))

        return gen_code_list
