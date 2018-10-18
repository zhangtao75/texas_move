
"""
Analyse PioSOLVER Results

Author:
Tao Zhang (zhangtao75@gmail.com)

Function:
Analyse PioSOLVER Results to generate possible options for each player when the 
user is BTN,SB,BB,UTG,UTG+1,UTG+2,HJ,CO in different straddle limits.

The analysis - possible_actions should be like the following:
{
    straddle_limit_1:
        {
            user_position_1 : {'BTN':('check', 'call', 'nstrd', ...), 
                               'SB' :('check', 'call', 'fold', ...),
                              }, ...
            user_position_n : {'BTN':(...), ...}
        }, ...
    straddle_limit_2: {...},
    ...
    straddle_limit_n: {...}
}

Different data persistence program can store the above result in the 
pickle/csv/ini/json formats.

Known Issues:

Python version:
Python 3.6
"""

import configparser
import os
import re
import glob
import json

class Pio_Res_Analyser:
    """ The Pio_Res_Analyser will read all file names within recursively
    """
    def __init__(self, conf_file_name='analysePioRes.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(conf_file_name)
        self.pio_result_path = self.config['GENERAL']['Pio_Res_Path']
        self.possible_action_path = self.config['GENERAL']['Possible_Action_Path']
        self.strategy_files = {}
        self.res_possible_actions = {}
        self.res_max_round = 0
        self.res_max_round_file = ""

    def read_pio_result_files(self):
        """ read all file names of PioSOLVER's result files in self.strategy_files
            the output should be {strd_limit: {user_position: [file_names]}.
            if there are any duplicated files, raise an exception.
        """
        p_strd_pattern = re.compile('\w*straddles')
        
        # straddle level
        for path_strd in os.listdir(self.pio_result_path):
            full_path_strd = os.path.join(self.pio_result_path,path_strd)
            # bypass invalid straddle path
            if not(os.path.isdir(full_path_strd) & 
                bool(re.match(p_strd_pattern, path_strd))):
                continue
            # strategy_files {strd1:{}, strd2:{}, ...}
            self.strategy_files[path_strd] =  {} 
            
            # position level
            position_dict = {}
            for path_position in os.listdir(full_path_strd):
                full_path_position = os.path.join(full_path_strd, 
                    path_position)
                # bypass invalid position path
                if not(os.path.isdir(full_path_position)):
                    continue
                
                # file level
                file_iterator = glob.iglob(full_path_position+'/**/*.txt', 
                    recursive=True)     # iterator to get all files
                file_list = []
                for file in file_iterator:
                    (path_name, short_file_name) = os.path.split(file)
                    # file_list = [{f1}, {f2}, ...]
                    file_list.append(short_file_name)
                
                # position_dict {'BB': [f1, f2], 'CO': [f1, f2], ...}
                position_dict[path_position] = file_list
                    
            # strategy_files {strd1:{{'BB': [f1, f2], 'CO': [f1, f2], ...}}, ...}
            self.strategy_files[path_strd] = position_dict
        #print(len(self.strategy_files['100straddles']['BB'])) #debug = 521
        #print(len(self.strategy_files['200straddles']['CO'])) #debug = 552

    def print_raw_data(self, strd, position, num):
        print(strd + ' - ' + position)
        for i in range(num):
            print(self.strategy_files[strd][position][i])

    def get_strategy_files(self):
        return self.strategy_files

    def get_strddle_list(self):
        strddle_list = []
        for strd in self.strategy_files:
            strddle_list.append(strd)
        return(strddle_list)

    def analyse_possible_actions(self):
        """ analyse all file names of PioSOLVER's result files, generate 
            possible_actions (refer to the file comment)
        """
        self.res_possible_actions = {}
        for strd in self.strategy_files.keys():
            #print("in " + strd) #debug
            self.res_possible_actions[strd] = {}
            for user_position in self.strategy_files[strd].keys():
                #print("in " + user_position) #debug
                self.res_possible_actions[strd][user_position] = {}
                
                suffix = user_position + '_strategy.txt'
                suffix_len = len(suffix)
                #print("suffix : " + suffix) #debug

                player_actions = {}
                for short_file_name in self.strategy_files[strd][user_position]:
                    # try to get other player's possible action, which is like
                    # {'BB' :('check', 'call', 'nstrd', ...), 
                    #  'SB' :('check', 'call', 'fold', ...), ... }
                    
                    # remove the "BB_strategy.txt" part to get scenario
                    # by pass - files without invalid suffix
                    if short_file_name[-suffix_len:] != suffix:
                        #print(short_file_name + " bypassed - wrong name") #debug
                        continue
                    # by pass - no actions of other players
                    if len(short_file_name) == suffix_len:
                        # print(short_file_name + " bypassed - no other actions") #debug
                        continue
                    # remove the "BB_strategy.txt" part to get scenario
                    scenario = short_file_name[:-suffix_len-1]
                    #print(scenario) #debug
                    
                    # get player-action pairs
                    scenario_pieces = scenario.split(sep='_')
                    pieces_num = len(scenario_pieces)
                    # by pass - invalid player-action pairs
                    if pieces_num % 2 == 1:
                        print(short_file_name + " bypassed - invalid pairs") #debug
                        continue
                    for idx in range(0, pieces_num, 2):
                        player = scenario_pieces[idx]
                        action = scenario_pieces[idx+1]
                        #print(player + " - " + action) #debug
                        # new other player
                        if player not in player_actions:
                            player_actions[player] = set(['Fold'])
                        # existent other player, add action to the action set
                        player_actions[player].add(action)

                for player in player_actions:
                    player_action_list = list(player_actions[player])
                    # sort
                    strd_list = []
                    other_list = []
                    for action in player_action_list:
                        if action[-4:] == 'strd':
                            strd_list.append(action)
                        else:
                            other_list.append(action)
                    other_list.sort(reverse=True)
                    strd_list.sort(key=lambda x:float(x[:-4]))
                    player_actions[player] = other_list + strd_list
                        
                self.res_possible_actions[strd][user_position] = player_actions
        #print(self.res_possible_actions) debug

    def get_possible_actions(self):
        return self.res_possible_actions

    def save_possible_actions(self, fmt='json'):
        if fmt == 'json':
            # clear the output path
            if os.path.exists(self.possible_action_path):
                file_iterator = glob.iglob(self.possible_action_path+'*', 
                    recursive=True)     # iterator to get all files
                for file in file_iterator:
                    os.remove(file)
            else:
                os.makedirs(self.possible_action_path)
            # save json file
            for strd in self.res_possible_actions:
                for player in self.res_possible_actions[strd]:
                    file_name = self.possible_action_path+'possible_actions_'+strd+'_'+player+'.json'
                    try:
                        with open(file_name, 'w') as fp:
                            json.dump(self.res_possible_actions[strd][player],fp)
                    except IOError:
                        print('cannot create file: possible_actions_'+strd+'_'+player+'.json')
        else:
            print('This format has not been supported.\nPlease use the json format.')

    def analyse_max_round(self):
        # this analysis depends on the self.strategy_files 
        # i.e. run the read_pio_result_files first() before this method
        self.res_max_round = 0  # reset the res_max_round
        for strd in self.strategy_files.keys():
            for position in self.strategy_files[strd]:
                for file in self.strategy_files[strd][position]:
                    # update UTG+1 to UT1, UTG+2 to UT2 to avoid confusing UTG 
                    #   with UTG+1 or UTG+2
                    file_upd = file.replace('UTG+1', 'UT1')
                    file_upd = file_upd.replace('UTG+2', 'UT2')
                    position_upd = position.replace('UTG+1', 'UT1')
                    position_upd = position_upd.replace('UTG+2', 'UT2')
                    # count around
                    round = file_upd.count(position_upd)
                    if round > self.res_max_round:
                        self.res_max_round = round
                        self.res_max_round_file = file

    def get_max_round_and_file(self):
        return(self.res_max_round, self.res_max_round_file)

class Sequence_Persister:
    """ 
    """
    def __init__(self, file_type="csv"):
        self.file_type = file_type
        
    def set_input_data(self, input_data):
        self.output_data = input_data

    def set_file_type(self, file_type):
        self.file_type = file_type

    def get_output_data(self):
        return(self.output_data)

    def dictlist_to_list(self, input_dict):
        output_list = []
        for key in input_dict.keys():
            for value in input_dict[key]:
                if isinstance(value, list):
                    output_list.append([key] + value)
                else:
                    output_list.append([key,value])
        return(output_list)

    def dictdictlist_to_list(self):
        for key in self.output_data.keys():
            self.output_data[key] = self.dictlist_to_list(self.output_data[key])
        self.output_data = self.dictlist_to_list(self.output_data)

    def save_to_file(self, file_name):
        pass

    def save_to_csv(self):
        pass

    def save_to_pickle(self):
        import pickle
        sfile=u'E:/texas/tmp_pickle.pkl'
        pfile = open(sfile, 'wb')
        pickle.dump(a, pfile)
        pfile.close()
        pass
        sfile=u'E:/texas/tmp_pickle.pkl'
        pfile = open(sfile, 'rb')
        d = pickle.load(pfile)

    def list_dict(dic):
        for k in dic:
            if type(dic[k]) == dict:
                l = list_dict(dic[k])

# main program
if __name__ == '__main__':
    
    print('in main')
    analyser = Pio_Res_Analyser('analysePioRes.ini')
    sp = Sequence_Persister()

    analyser.read_pio_result_files()

    print("\n===== strategy_files =====")
    #print(analyser.get_strategy_files())
    #analyser.print_raw_data('100straddles','BB',10)
    #analyser.print_raw_data('200straddles','CO',10)
    print("===== strategy_files =====")

    print("\n===== straddle list =====")
    print(analyser.get_strddle_list())
    
    print("\n===== possible_actions =====")
    analyser.analyse_possible_actions()
    analyser.save_possible_actions()
    #print(analyser.get_possible_actions())
    print("===== possible_actions =====")

    print("\n===== max round & max file =====")
    analyser.analyse_max_round()
    print(analyser.get_max_round_and_file())
    print("===== max round & max file =====")
    
    

    print('out main')
  