import os
import tempfile
import argparse
import json


def save_storage(storage_path, storage):
    with open(storage_path, 'w') as f:
        json.dump(storage, f)


def load_storage(storage_path):
    if not os.path.exists(storage_path):
        return dict()

    with open(storage_path, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    parser = argparse.ArgumentParser()
    parser.add_argument('--key')
    parser.add_argument('--val')
    args = parser.parse_args()

    storage = load_storage(storage_path)

    # --key --val
    if args.val:
        if args.key not in storage:
            storage[args.key] = list()
        storage[args.key].append(args.val)

        save_storage(storage_path, storage)
    # --key
    else:
        if args.key not in storage:
            print('')
        else:
            print(', '.join(storage[args.key]))
