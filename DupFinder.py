import time
import json
from controls.smwinservice import SMWinservice
from controls.duplicate_finder import DuplicateFinder


class DupFinder(SMWinservice):
    _svc_name_ = "DupFinder"
    _svc_display_name_ = "Dup Finder"
    _svc_description_ = "O serviço DupFinder realiza o escaneamento de diretórios e subdiretórios em busca de " \
                        "arquivos duplicados por tamanho e hash, assim como pastas vazias afim de realizar a exclusão" \
                        " segura. "

    def __init__(self, args):
        super().__init__(args)
        self.is_running = False

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def main(self):
        with open('C:\\GitHub\\DupFinder\\configs\\configs.json') as i:
            _config = json.load(i)

        dup_finder = DuplicateFinder(_config['directory'], _config['log_directory'], _config['hash_algorithm'],
                                     _config['to_trash'], _config['deletion_mode'])

        while self.is_running:
            dict_by_size = dup_finder.find_duplicate_by_size()
            dict_by_hash = dup_finder.find_duplicate_by_full_hash(dict_by_size)
            dup_finder.send_duplicate_to_trash(dict_by_hash)
            dup_finder.remove_empty_folder(_config['directory'])
            dup_finder.export_log()
            time.sleep(30)


if __name__ == '__main__':
    DupFinder.parse_command_line()
