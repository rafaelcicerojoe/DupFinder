import json
from controls.duplicate_finder import DuplicateFinder


def prog():
    with open('C:/Users/rafae/Desktop/RmSvc_SO/conf/cfg.json') as i:
        _conf = json.load(i)

    see_duplicata = DuplicateFinder(_conf['directory'], _conf['log_directory'], _conf['hash_algorithm'],
                                 _conf['to_trash'], _conf['deletion_mode'])

    do_per_size = see_duplicata.find_duplicate_by_size()
    do_per_hash = see_duplicata.find_duplicate_by_full_hash(do_per_size)
    see_duplicata.send_duplicate_to_trash(do_per_hash)
    see_duplicata.remove_empty_folder(_conf['directory'])
    see_duplicata.export_log()