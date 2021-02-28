import json
import hashlib
from os import walk, stat, remove, rmdir, listdir
from os.path import join, getsize, isdir
from send2trash import send2trash
from datetime import datetime
from controls.file import File


class DuplicateFinder:
    errors = []
    log = {'duplicates_by_size': {"Qtd": 0, 'Files': []},
           'duplicates_by_hash': {"Qtd": 0, 'Files': []},
           'deleted_files': {"Qtd": 0, 'Files': []},
           'deleted_empty_folders': {"Qtd": 0, 'Files': []},
           'errors': {"Qtd": 0, 'Files': []}
           }

    def __init__(self, directory, log_directory, hash_algorithm, to_trash, deletion_mode):
        self._directory = directory
        self._log_directory = log_directory
        self._hash_algorithm = hash_algorithm
        self._to_trash = to_trash
        self._deletion_mode = deletion_mode

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        self._directory = value

    @property
    def log_directory(self):
        return self._log_directory

    @log_directory.setter
    def log_directory(self, value):
        self._log_directory = value

    @property
    def hash_algorithm(self):
        return self._hash_algorithm

    @hash_algorithm.setter
    def hash_algorithm(self, value):
        self._hash_algorithm = value

    @property
    def to_trash(self):
        return self._to_trash

    @to_trash.setter
    def to_trash(self, value):
        self._to_trash = value

    @property
    def deletion_mode(self):
        return self._deletion_mode

    @deletion_mode.setter
    def deletion_mode(self, value):
        self._deletion_mode = value

    def get_hash(self, file_path):
        hash_algorithm = hashlib.new(self._hash_algorithm)
        with open(file_path, "rb") as f:
            file = f.read()
            hash_algorithm.update(file)
        return hash_algorithm.hexdigest()

    def find_duplicate_by_size(self):
        try:
            total = []
            dict_by_size = {}
            for path, dirs, files in walk(self._directory):
                for file in files:
                    try:
                        file_name = file
                        file_path = path
                        file_full_path = join(path, file)
                        file_size = getsize(file_full_path)
                        file_time = datetime.fromtimestamp(stat(file_full_path).st_mtime)
                        file_obj = File(file_name, file_path, file_full_path, file_size, file_time)
                        total.append(file_obj)
                        if file_size not in dict_by_size:
                            dict_by_size[file_size] = [file_obj]
                        else:
                            dict_by_size[file_size].append(file_obj)
                    except Exception as e:
                        self.log['errors']['Files'].append(str(e))
                        continue

            unique_file_per_size = []
            for i in dict_by_size:
                if len(dict_by_size[i]) < 2:
                    unique_file_per_size.append(i)
            for i in unique_file_per_size:
                del (dict_by_size[i])

            for key, obj_list in dict_by_size.items():
                for obj in obj_list:
                    self.log['duplicates_by_size']['Files'].append(str(obj))

            self.log['duplicates_by_size']['Qtd'] = len(self.log['duplicates_by_size']['Files'])
            return dict_by_size
        except Exception as e:
            self.log['errors']['Files'].append(str(e))
            print(e)

    def find_duplicate_by_full_hash(self, dict_by_size):
        try:
            dict_by_hash = {}
            for key, obj_list in dict_by_size.items():
                for obj in obj_list:
                    hash_id = self.get_hash(obj.full_path)
                    obj.hash_id = hash_id
                    if hash_id not in dict_by_hash:
                        dict_by_hash[hash_id] = [obj]
                    else:
                        dict_by_hash[hash_id].append(obj)

            unique_file_per_hash = []
            for i in dict_by_hash:
                if len(dict_by_hash[i]) < 2:
                    unique_file_per_hash.append(i)
            for i in unique_file_per_hash:
                del (dict_by_hash[i])

            for key, obj_list in dict_by_hash.items():
                for obj in obj_list:
                    self.log['duplicates_by_hash']['Files'].append(str(obj))

            self.log['duplicates_by_hash']['Qtd'] = len(self.log['duplicates_by_hash']['Files'])
            return dict_by_hash
        except Exception as e:
            self.log['errors']['Files'].append(str(e))
            print(e)

    def send_duplicate_to_trash(self, dict_by_hash):
        try:
            duplicates = []
            for key, obj_list in dict_by_hash.items():
                if self._deletion_mode == 1:
                    original = obj_list[0]
                    for obj in obj_list:
                        if len(obj.name) < len(original.name):
                            original = obj
                    obj_list.remove(original)
                    for obj in obj_list:
                        duplicates.append(obj.full_path)
                        self.log['deleted_files']['Files'].append(str(obj))
                elif self._deletion_mode == 2:
                    original = obj_list[0]
                    for obj in obj_list:
                        if obj.time > original.time:
                            original = obj
                    obj_list.remove(original)
                    for obj in obj_list:
                        duplicates.append(obj.full_path)
                        self.log['deleted_files']['Files'].append(str(obj))
                elif self._deletion_mode == 3:
                    longest_path_list = []
                    longest_path = obj_list[0].path
                    for obj in obj_list:
                        if len(obj.path) > len(longest_path):
                            longest_path = obj.path
                    for obj in obj_list:
                        if obj.path == longest_path:
                            longest_path_list.append(obj)
                    if len(longest_path_list) > 1:
                        original = longest_path_list[0]
                        for obj in longest_path_list:
                            if len(obj.name) < len(original.name):
                                original = obj
                        obj_list.remove(original)
                    else:
                        original = longest_path_list[0]
                        obj_list.remove(original)
                    for obj in obj_list:
                        duplicates.append(obj.full_path)
                        self.log['deleted_files']['Files'].append(str(obj))

            self.log['deleted_files']['Qtd'] = len(duplicates)

            for i in duplicates:
                try:
                    if self._to_trash == 0:
                        remove(i)
                    else:
                        send2trash(i)

                except Exception as e:
                    self.log['errors']['Files'].append(str(e))
                    continue
        except Exception as e:
            self.log['errors']['Files'].append(str(e))
            print(e)

    def remove_empty_folder(self, path):
        try:
            if not isdir(path):
                return

            files = listdir(path)
            if len(files):
                for f in files:
                    full_path = join(path, f)
                    if isdir(full_path):
                        self.remove_empty_folder(full_path)

            files = listdir(path)
            if len(files) == 0:
                try:
                    if self._to_trash == 0:
                        rmdir(path)
                    else:
                        send2trash(path)
                    self.log['deleted_empty_folders']['Files'].append(path)
                except Exception as e:
                    self.log['deleted_empty_folders']['Files'].remove(path)
                    self.log['errors']['Files'].append(str(e))

            self.log['deleted_empty_folders']['Qtd'] = len(self.log['deleted_empty_folders']['Files'])
        except Exception as e:
            self.log['errors']['Files'].append(str(e))
            print(e)

    def export_log(self):
        import datetime
        ts = str(datetime.datetime.now())
        ts = ts.replace(":", "-")
        ts = ts.replace(" ", "_")
        ts = ts.replace(".", "_")

        try:
            self.log['errors']['Qtd'] = len(self.log['errors']['Files'])
            out_file = open(self._log_directory + ts + ".json", "w")
            json.dump(self.log, out_file, indent=6)
            out_file.close()

            print("\n{}".format(self._log_directory + ts + ".json"))
            for i in self.log:
                print("{}: {}".format(i, self.log[i]['Qtd']))

            self.log = {'duplicates_by_size': {"Qtd": 0, 'Files': []},
                        'duplicates_by_hash': {"Qtd": 0, 'Files': []},
                        'deleted_files': {"Qtd": 0, 'Files': []},
                        'deleted_empty_folders': {"Qtd": 0, 'Files': []},
                        'errors': {"Qtd": 0, 'Files': []}
                        }

        except Exception as e:
            self.log['errors']['Files'].append(str(e))
            print(e)
