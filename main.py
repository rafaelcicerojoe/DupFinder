from duplicate_finder import DuplicateFinder


def main():
    dup_finder = DuplicateFinder('/home/fernando/duplicator/')
    dup_finder.find_duplicate_by_size()
    dup_finder.find_duplicate_by_full_hash()
    dup_finder.send_duplicate_to_trash()
    dup_finder.remove_empty_folder()
    dup_finder.export_log()


if __name__ == '__main__':
    main()
