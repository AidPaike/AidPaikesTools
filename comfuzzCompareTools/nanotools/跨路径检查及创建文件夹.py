import os
save_path = r"C:\Users\AidPaike\Projects\pythonProject\AidPaikeProject\comfuzzCompareTools\nanotools\a\b"

if not os.path.exists(save_path):
    os.makedirs(save_path)
else:
    print(os.path.exists(save_path))