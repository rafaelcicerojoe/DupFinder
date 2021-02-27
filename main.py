import json
from controls.duplicate_finder import DuplicateFinder


def main():

    with open('configs/configs.json') as i:
        _config = json.load(i)

    dup_finder = DuplicateFinder(_config['directory'], _config['log_directory'], _config['hash_algorithm'], _config['to_trash'], _config['deletion_mode'])
    dup_finder.find_duplicate_by_size()
    dup_finder.find_duplicate_by_full_hash()
    dup_finder.send_duplicate_to_trash()
    dup_finder.remove_empty_folder()
    dup_finder.export_log()


if __name__ == '__main__':
    main()
