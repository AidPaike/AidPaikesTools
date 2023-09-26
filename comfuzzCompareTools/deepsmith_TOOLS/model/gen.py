import os
import torch
from tqdm import trange
import subprocess
from conf import hparams
from model import LSTM
from utils import load_json
from sample import sample_multi
import sys

device = torch.device(f"cuda:{hparams.gpu}" if torch.cuda.is_available() else "cpu")

def howmanytestall(path):
    cmd = f"ls -lh {path}|wc -l"
    if sys.platform.startswith('win'):  # 假如是windows
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    else:  # 假如是linux
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return int(stdout.decode('ascii'))

if __name__ == '__main__':
    path = "/root/software/fuzzers/DeepSmithNISL/deepsmith_testcase/"
    flag = howmanytestall(path)
    print("Loading model...")
    workspace_path = os.path.dirname(hparams.gen_model)
    token_to_idx = load_json(os.path.join(workspace_path, 'token_to_idx.json'))
    idx_to_token = load_json(os.path.join(workspace_path, 'idx_to_token.json'), transfer=True)

    if not os.path.exists(hparams.gen_model):
        raise FileNotFoundError('Model not found, please try again.')

    model = torch.load(hparams.gen_model).to(device)
    model.device = device

    import time

    start_time = time.time()
    print("Generating...")
    with open(hparams.gen_file, 'a+', encoding='utf-8') as f:

        n_batches = int(hparams.gen_number / hparams.gen_batch_size)

        for _ in trange(n_batches):
            gen_code_list = sample_multi(model,
                                         prefix=hparams.gen_prefix,
                                         batch_size=hparams.gen_batch_size,
                                         max_gen_length=hparams.max_gen_length,
                                         token_to_idx=token_to_idx,
                                         idx_to_token=idx_to_token,
                                         segment_length=hparams.segment_length,
                                         temperature=hparams.temperature)
            gen_code_list = [i.split('<eos>')[0] for i in gen_code_list]
            for testcase_content in gen_code_list:
                testcase_path = path + str(flag) + ".js"

                try:
                    # 此处手动转换为bytes类型再存储是为了防止代码中有乱码而无法存储的情况
                    with open(testcase_path, 'w', encoding='utf-8') as f:
                        f.write(testcase_content)
                except Exception as e:
                    print(e)
                # print(testcase_content)
                flag += 1
            # f.write('\n'.join(gen_code_list) + '\n')

    print(f'Generated {hparams.gen_number} cases and spent {int(time.time() - start_time)} seconds.')
    print(f'Generated test cases are saved in: {os.path.join(os.getcwd(), hparams.gen_file)}')
