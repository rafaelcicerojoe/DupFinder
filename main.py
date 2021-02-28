import json
from controls.duplicate_finder import DuplicateFinder


def main():
    with open('configs/configs.json') as i:
        _config = json.load(i)

    dup_finder = DuplicateFinder(_config['directory'], _config['log_directory'], _config['hash_algorithm'],
                                 _config['to_trash'], _config['deletion_mode'])

    dict_by_size = dup_finder.find_duplicate_by_size()
    dict_by_hash = dup_finder.find_duplicate_by_full_hash(dict_by_size)
    dup_finder.send_duplicate_to_trash(dict_by_hash)
    dup_finder.remove_empty_folder(_config['directory'])
    dup_finder.export_log()


if __name__ == '__main__':
    main()
