import configparser
import os
import glob

class preProcessPioRes:
    def __init__(self, conf_file_name='analysePioRes.ini'):
        config = configparser.ConfigParser()
        config.read(conf_file_name)
        self.pio_result_path = config['GENERAL']['Pio_Res_Path']

    def process_change_player_name_dir(self, subdir, src, dst):
        if subdir[-1] not in ['/', '\\']:
            subdir += '/'
        path_iterator = glob.iglob(self.pio_result_path+subdir+'**/'+src, 
            recursive=True)     # iterator to get all STR dirs
        process_count = 0
        for path in path_iterator:
            if os.path.isdir(path):
                new_path_name = path[:-len(src)]+dst
                os.rename(path, new_path_name)
                process_count += 1
        print('Directories ' + src + ' have been changed to ' + dst + ' : ' + str(process_count))

    def process_change_player_name_file(self, subdir, src, dst):
        if subdir[-1] not in ['/', '\\']:
            subdir += '/'
        file_iterator = glob.iglob(self.pio_result_path+subdir+'**/*_strategy.txt', 
            recursive=True)     # iterator to get all files
        process_count = 0
        for file in file_iterator:
            (path_name, short_file_name) = os.path.split(file)
            if src in short_file_name:
                new_file_name = os.path.join(path_name,
                    short_file_name.replace(src+'_', dst+'_'))
                os.rename(file, new_file_name)
                process_count += 1
        print('Files with ' + src + ' have been changed to ' + dst + ' : ' + str(process_count))
        
    def process_remove_fold_pair(self):
        file_iterator = glob.iglob(self.pio_result_path+'**/*_strategy.txt', 
            recursive=True)     # iterator to get all files
        process_count = 0
        for file in file_iterator:
            (path_name, short_file_name) = os.path.split(file)
            if 'Fold' in short_file_name:   
                file_name_pieces = short_file_name.split('_')
                # loop to remove multiple Folds
                while 'Fold' in file_name_pieces:
                    fold_pos = file_name_pieces.index('Fold')
                    if fold_pos % 2 == 1:   # Fold in the action position
                        file_name_pieces.pop(fold_pos-1)    # remove the Fold player
                        file_name_pieces.pop(fold_pos-1)    # remove Fold
                # rename the file
                short_file_name = '_'.join(file_name_pieces)
                new_file_name = os.path.join(path_name,short_file_name)
                os.rename(file, new_file_name)
                process_count += 1
        print('Files with Fold have been processed : ' + str(process_count))

# main program
if __name__ == '__main__':
    preprocess = preProcessPioRes()
    
    preprocess.process_remove_fold_pair()
    
    preprocess.process_change_player_name_dir('50straddles', 'UTG+1', 'UTG+2')
    preprocess.process_change_player_name_dir('50straddles', 'UTG', 'UTG+1')
    preprocess.process_change_player_name_dir('50straddles', 'STR', 'UTG')
    preprocess.process_change_player_name_file('50straddles', 'UTG+1', 'UT2')
    preprocess.process_change_player_name_file('50straddles', 'UTG', 'UTG+1')
    preprocess.process_change_player_name_file('50straddles', 'STR', 'UTG')
    preprocess.process_change_player_name_file('50straddles', 'UT2', 'UTG+2')

    preprocess.process_change_player_name_dir('200straddles', 'UTG+1', 'UTG+2')
    preprocess.process_change_player_name_dir('200straddles', 'UTG', 'UTG+1')
    preprocess.process_change_player_name_dir('200straddles', 'STR', 'UTG')
    preprocess.process_change_player_name_file('200straddles', 'UTG+1', 'UT2')
    preprocess.process_change_player_name_file('200straddles', 'UTG', 'UTG+1')
    preprocess.process_change_player_name_file('200straddles', 'STR', 'UTG')
    preprocess.process_change_player_name_file('200straddles', 'UT2', 'UTG+2')
    