import configparser
import glob
import json

class TexasStrategy():
    """docstring for TexasStrategy"""
    def __init__(self):
        self.debug_strd_num = 2 # debug
        
        config = configparser.ConfigParser()
        config.read('analysePioRes.ini')
        self.strategy_files_root = config['GENERAL']['Pio_Res_Path']
        self.possible_action_path = config['GENERAL']['Possible_Action_Path']
        self.action_list_length = 4 # same setting as GUI
        self.current_strd = 0
        self.current_user_name = ''
        self.possible_actions = {}

        # create pairs
        cards = []
        for value in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
            for suit in [chr(9824), chr(9829), chr(9830), chr(9827)]:
                cards.append([suit, value])
        self.pairs = []
        for card1 in cards[1:]:
            for card2 in cards[:cards.index(card1)]:
                self.pairs.append([card1, card2])
        #debug
        # fn = 'C:\\WorkSpace\\texas_holdem\\pairs'
        # fp = open(fn, 'w')
        # fp.write(str(self.pairs))
        # fp.close()
        
    def get_possible_actions(self, strd_limit, user_name, player_name):
        # new straddle-user pair, open the json file
        if (self.current_strd != strd_limit) or \
            (self.current_user_name != user_name):
            file_name = self.possible_action_path + 'possible_actions_' + \
                str(strd_limit) + 'straddles_' + user_name + '.json'
            try:
                with open(file_name, 'r') as fp:
                    self.possible_actions = json.load(fp)
            except IOError:
                print('cannot create file: possible_actions_'+strd+'_'+player+'.json')
        # get possible actions self.possible_actions
        return self.possible_actions[player_name]
        
    def get_advice_file_name(self, user_name, action_list):
        hidden_action_list = ['SB', 'BB', '2BB', 'Fold']
        file_name = ''
        for action_turn in range(self.action_list_length):
            for player_with_action in action_list:
                for player_name in player_with_action:
                    if len(player_with_action[player_name]) > action_turn:
                        if player_with_action[player_name][action_turn] not in hidden_action_list:
                            file_name += player_name + '_' + player_with_action[player_name][action_turn] + '_'
        file_name += user_name + '_strategy.txt'
        return file_name

    def read_strategy_file(self, absolute_file_name, hole_cards):
        # read strategy file
        strategy_file = open(absolute_file_name, 'r')
        strategy_lines = strategy_file.readlines()
        strategy_file.close()
        # the order of hole cards may not consist with the pairs
        # print(hole_cards) # debug
        if hole_cards in self.pairs:
            strategy_idx = self.pairs.index(hole_cards)
        else:
            strategy_idx = self.pairs.index(hole_cards[::-1])
        # get advice from strategy lines
        advice = []
        for strategy_line_no in range(3, len(strategy_lines), 2):
            strategy_raw_line = strategy_lines[strategy_line_no]
            strategy_item = strategy_raw_line.split()
            advice.append(strategy_item[1] + ':' + strategy_item[strategy_idx+2])
        return advice

    def get_advice(self, straddle, user_name, action_list, hole_cards):
        file_name = self.get_advice_file_name(user_name, action_list)
        wildcard_file_name = self.strategy_files_root + \
            str(straddle) + 'straddles\\' + \
            user_name + '\\**\\' + \
            file_name
        file_list = glob.glob(wildcard_file_name, recursive=True)
        if len(file_list) == 0:
            return ['No strategy', 'found']
        elif len(file_list) > 1:
            return ['Multiple', 'strategies', 'found']
        else:
            return self.read_strategy_file(file_list[0], hole_cards)
        