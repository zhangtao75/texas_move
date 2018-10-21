import tkinter as tk
from tkinter import messagebox
import configparser

class GUI_PLAYER:
    def __init__(self, ini_parser, frm_father, player_position, 
        gui_row, gui_column,            # the player's position in the GUI
        var_user_pos, int_user_pos,     # the control var of user position & 
                                        # the value for this player
        var_current_pos, int_current_pos,   # the control var of current player &
                                            # the value for this player
        set_current_event_process_pg):  # the event: click the current radio btn

        self.set_current_event_process_pg = set_current_event_process_pg
        
        # GUI part
        # the main frame
        frm_player = tk.Frame(frm_father, bd=2, relief=tk.GROOVE)
        frm_player.grid(row=gui_row, column=gui_column, padx=5, pady=5)
        # the user position
        self.rdb_user_pos = tk.Radiobutton(frm_player, 
            variable=var_user_pos, value=int_user_pos)
        self.rdb_user_pos.grid(row=0, column=0, padx=5)
        # the user name label
        lbl_player = tk.Label(frm_player, text=player_position)
        lbl_player.grid(row=0, column=1, padx=5)
        # the current player 
        self.rdb_current_pos = tk.Radiobutton(frm_player, 
            variable=var_current_pos, value=int_current_pos)
        self.rdb_current_pos.grid(row=0, column=2, padx=5)
        self.rdb_current_pos.config(command=self.current_pos_click)

        # action list
        # import constants definition
        self.action_list_length = int(ini_parser['GUI_PLAYER']['Action_List_Len'])
        action_label_width = 10
        action_label_bd = 2
        action_label_style = tk.GROOVE
        action_label_columnspan = 3
        action_label_padx = 5
        
        self.action_list = []       # display control variable list
        action_label_list = []      # label widget list 

        for action_idx in range(self.action_list_length):
            self.action_list.append(tk.StringVar())
            self.action_list[action_idx].set('')
            self.action_list[action_idx].set(str(action_idx))   #debug
            action_label_list.append(
                tk.Label(frm_player, textvariable=self.action_list[action_idx], 
                    width=action_label_width, bd=action_label_bd, 
                    relief=action_label_style))
            action_label_list[action_idx].grid(row=action_idx+1, column=0, 
                columnspan=action_label_columnspan, padx=action_label_padx)

    def current_pos_click(self):
        if self.action_list[0].get() == '':
            messagebox.showinfo("Warning", "This user hasn't acted yet")
            self.set_current_event_process_pg(process_flag=False)
            return
        self.set_current_event_process_pg(process_flag=True)

    def clear_actions(self):
        for action_idx in range(self.action_list_length):
            self.action_list[action_idx].set('')

    def enable_user_pos(self):
        self.rdb_user_pos.config(state=tk.NORMAL)

    def disable_user_pos(self):
        self.rdb_user_pos.config(state=tk.DISABLED)

    def enable_current_pos(self):
        self.rdb_current_pos.config(state=tk.NORMAL)

    def disable_current_pos(self):
        self.rdb_current_pos.config(state=tk.DISABLED)

    def set_action(self, action, is_new):
        if is_new:
            for action_idx in range(self.action_list_length):
                if self.action_list[action_idx].get() == '':
                    self.action_list[action_idx].set(action)
                    break
        else:
            for action_idx in range(self.action_list_length):
                if self.action_list[self.action_list_length - 1 - action_idx].get() != '':
                    self.action_list[self.action_list_length - 1 - action_idx].set(action)
                    break

    def get_action(self):
        actions = []
        for action_idx in range(self.action_list_length):
            if self.action_list[action_idx].get() == '':
                return actions
            actions.append(self.action_list[action_idx].get())

    def get_previous_action(self):
        previous_action = self.action_list[0].get()
        for action_idx in range(1,self.action_list_length):
            if self.action_list[action_idx].get() != '':
                previous_action = self.action_list[action_idx].get()
            else:
                return previous_action
        return previous_action


class GUI_PLAYER_GROUP:
    def __init__(self, ini_parser, frm_father, set_current_event_process_gui):
        self.var_user_pos = tk.IntVar()
        self.var_current_pos = tk.IntVar()
        self.latest_next_pos = 0
        self.set_current_event_process_gui = set_current_event_process_gui

        # player_idx: 0:SB, 1:BB, 2:STR, 3:UTG, 4:UTG+1, 5:HJ, 6:CO, 7:BTN
        # var_idx = player_idx + 1 
        self.player_group = []
        self.player_name = ini_parser['GENERAL']['Players'].split(',')
        # player_position - each player uses its index to find its position
        player_position =  ini_parser['GUI_PLAYER_GROUP']['Player_Position'].split(';')
        for player_idx in range(8):
            self.player_group.append(GUI_PLAYER(ini_parser, frm_father, 
                self.player_name[player_idx], 
                gui_row=int(player_position[player_idx].split(',')[0]), 
                gui_column=int(player_position[player_idx].split(',')[1]), 
                var_user_pos=self.var_user_pos, int_user_pos=player_idx+1,
                var_current_pos=self.var_current_pos, int_current_pos=player_idx+1, 
                set_current_event_process_pg=self.set_current_event_process_pg))

    def set_current_event_process_pg(self, process_flag=True):
        if process_flag == False:
            self.var_current_pos.set(self.latest_next_pos)
            return
        self.set_current_event_process_gui()

    def get_user_pos(self):
        return self.var_user_pos.get()

    def get_user_name(self):
        return self.player_name[self.var_user_pos.get()-1]

    def get_current_pos(self):
        return self.var_current_pos.get()

    def get_current_player_name(self):
        return self.player_name[self.var_current_pos.get() - 1]

    def get_latest_next_pos(self):
        return self.latest_next_pos

    def next_latest_next_pos(self):
        self.latest_next_pos = self.latest_next_pos % 8 + 1

    def next_current_pos(self):
        self.var_current_pos.set(self.var_current_pos.get() % 8 + 1)

    def get_current_player_previous_action(self):
        return self.player_group[self.var_current_pos.get()-1].get_previous_action()
        
    def set_open_state(self):
        for player in self.player_group:
            player.clear_actions()
            player.enable_user_pos()
            player.disable_current_pos()
        self.var_user_pos.set(0)
        self.var_current_pos.set(0)
        self.latest_next_pos = -1

    def set_running_state(self):
        self.player_group[0].set_action('SB', True)
        self.player_group[1].set_action('BB', True)
        self.player_group[2].set_action('2BB', True)
        self.var_current_pos.set(4)     # STR
        self.latest_next_pos = 4        # STR
        for player in self.player_group:
            player.disable_user_pos()
            player.enable_current_pos()

    def process_player_action(self, action):
        current_pos = self.var_current_pos.get()
        if current_pos == self.latest_next_pos:
            self.player_group[current_pos-1].set_action(action, True)
            self.next_current_pos()
            self.next_latest_next_pos()
        else:
            self.player_group[current_pos-1].set_action(action, False)
            self.next_current_pos()

    def get_players_all_actions(self):
        # players_action_list: 
        # [{'SB':['call', 'fold']}, {'BB':['call', '3 strd']}]
        players_action_list = []
        for player_idx, player in enumerate(self.player_group):
            player_action_dict = {}
            player_action_dict[self.player_name[player_idx]] = player.get_action()
            players_action_list.append(player_action_dict)
        return players_action_list

    def get_players_valid_actions(self):
        # players_action_list: 
        # [{'SB':['call', 'fold']}, {'BB':['call', '3 strd']}]
        prior_current_player_idx = (self.var_current_pos.get() + 6) % 8 # idx_in_list = var - 1
        players_action_list = []
        valid_action_num = len(self.player_group[prior_current_player_idx].get_action())
        for player_idx, player in enumerate(self.player_group):
            player_action_dict = {}
            player_action = player.get_action()
            if player_idx <= prior_current_player_idx:
                player_action = player_action[:valid_action_num]
            elif player_idx > prior_current_player_idx:
                player_action = player_action[:valid_action_num-1]
            player_action_dict[self.player_name[player_idx]] = player_action
            players_action_list.append(player_action_dict)
        return players_action_list


class GUI_STRD:
    def __init__(self, ini_parser, frm_father, gui_row, gui_column):
        # create the form
        frm_strd = tk.Frame(frm_father)
        frm_strd.grid(row=gui_row, column=gui_column, padx=5, pady=5)
        # create radiobox buttons
        self.var_strd_limit = tk.IntVar()
        self.strd_disp_list = []
        self.strd_type_num = int(ini_parser['GUI_STRD']['Strd_Type_Num'])
        for strd_idx in range(self.strd_type_num):
            self.strd_disp_list.append(
                tk.Radiobutton(frm_strd, 
                    text=ini_parser['GUI_STRD']['Strd_limit_'+str(strd_idx)]+' strd', 
                    variable=self.var_strd_limit, 
                    value=int(ini_parser['GUI_STRD']['Strd_limit_'+str(strd_idx)])))
            self.strd_disp_list[strd_idx].grid(row=strd_idx, column=0, padx=5)
        # default straddle value
        # why self: default value may be used in other methods
        self.default_strd_limit = 50
        self.var_strd_limit.set(self.default_strd_limit)
        # set to the open_state
        self.set_open_state()

    def set_open_state(self):
        #self.var_strd_limit.set(self.default_strd_limit)
        for strd_idx in range(self.strd_type_num):
            self.strd_disp_list[strd_idx].config(state=tk.NORMAL)

    def get_strd_limit(self):
        return self.var_strd_limit.get()

    def set_running_state(self):
        for strd_idx in range(self.strd_type_num):
            self.strd_disp_list[strd_idx].config(state=tk.DISABLED)


class GUI_HOLE_CARDS:
    def __init__(self, ini_parser, frm_father, gui_row, gui_column):
        # constants for hole cards
        self.hole_card_num = int(ini_parser['GUI_HOLE_CARDS']['Hole_Card_Num'])
        self.hole_card_disp_width = 10
        # the suit order below is 黑, 红, 片, 梅
        self.card_suit_list = ini_parser['GUI_HOLE_CARDS']['Suit_List'].split(',')
        self.card_suit_red_list = ini_parser['GUI_HOLE_CARDS']['Suit_Red_List'].split(',')
        self.card_rank_list = ini_parser['GUI_HOLE_CARDS']['Rank_List'].split(',')
        # icon for the selection dialog
        self.icon = ini_parser['GUI_HOLE_CARDS']['Icon']
        # number of selected hole cards
        self.selected_hole_card_num = 0
        # this list contains hole cards
        self.hole_card_list = []
        # this list contains label widgets
        self.hole_card_disp_list = []
        
        # create the form
        frm_hole_card = tk.Frame(frm_father)
        frm_hole_card.grid(row=gui_row, column=gui_column, padx=5, pady=5)
        # create labels to display hole cards
        for hc_idx in range(self.hole_card_num):
            self.hole_card_list.append(tk.StringVar())
            self.hole_card_list[hc_idx].set('')
            self.hole_card_list[hc_idx].set(str(hc_idx+1))   #debug
            self.hole_card_disp_list.append(
                tk.Label(frm_hole_card, textvariable=self.hole_card_list[hc_idx], 
                    width=self.hole_card_disp_width))
            self.hole_card_disp_list[hc_idx].grid(row=hc_idx, column=0, pady=2)
        # button
        self.btn_hc = tk.Button(frm_hole_card, text='set', width=9)
        self.btn_hc.grid(row=2, column=0, padx=5, pady=5)
        self.btn_hc.bind('<Button-1>', self.select_hole_cards)
        # set to the open_state
        self.set_open_state()
        
    def select_hole_cards(self, event):
        # create hole cards dialog 
        self.hc_dialog = tk.Toplevel()
        self.hc_dialog.title("Hole cards")
        self.hc_dialog.iconbitmap(self.icon)
        self.hc_dialog.geometry("450x130+%d+%d" % (event.x_root, event.y_root))
        # reset 
        self.clear_hole_cards()
        # create cards
        self.hc_var_list = []
        self.hc_button_list = []  # button widget list (maybe convert this list to a _local one)
        hc_idx = 0
        for suit_idx, suit in enumerate(self.card_suit_list):
            for rank_idx, rank in enumerate(self.card_rank_list):
                self.hc_var_list.append(tk.StringVar())
                self.hc_var_list[hc_idx].set(suit+rank)
                self.hc_button_list.append(
                    tk.Button(self.hc_dialog,
                        text=self.hc_var_list[hc_idx].get(), width=3))
                def hole_card_button_click(hc_button_clicked=hc_idx):
                    self.hole_card_select_event_process(hc_button_clicked)
                self.hc_button_list[hc_idx].config(command=hole_card_button_click)
                if suit in self.card_suit_red_list:
                    self.hc_button_list[hc_idx].config(fg='red')
                self.hc_button_list[hc_idx].grid(row=suit_idx, column=rank_idx,
                    padx=2, pady=2)
                hc_idx += 1
        
    def clear_hole_cards(self):
        self.selected_hole_card_num = 0
        for hc_idx in range(self.hole_card_num):
            self.hole_card_list[hc_idx].set('')

    def hole_card_select_event_process(self, hc_button_clicked):
        self.hole_card_list[self.selected_hole_card_num].set(
            self.hc_var_list[hc_button_clicked].get())
        if self.hc_var_list[hc_button_clicked].get()[0] in self.card_suit_red_list:
            self.hole_card_disp_list[self.selected_hole_card_num].config(fg='red')
        else:
            self.hole_card_disp_list[self.selected_hole_card_num].config(fg='black')
        # 
        self.selected_hole_card_num += 1
        if self.selected_hole_card_num == 1:
            self.hc_button_list[hc_button_clicked].config(state=tk.DISABLED)
        else:
            self.hc_dialog.destroy()

    def set_open_state(self):
        self.clear_hole_cards()
        self.btn_hc.config(state=tk.NORMAL)

    def set_running_state(self):
        self.btn_hc.config(state=tk.DISABLED)

    def hc_string_to_list(self, hc_string):
        return [hc_string[0], hc_string[1]]

    def get_hole_cards(self):
        if self.selected_hole_card_num == 2:
            return [self.hc_string_to_list(self.hole_card_list[0].get()), \
                self.hc_string_to_list(self.hole_card_list[1].get())]
        else:
            return [['空','空'], ['空','空']]


class GUI_START:
    def __init__(self, frm_father, gui_row, gui_column, 
        open_event_process, run_event_process):
        # create the form
        frm_start = tk.Frame(frm_father)
        frm_start.grid(row=gui_row, column=gui_column, padx=5, pady=5)
        # create buttons
        self.btn_start = tk.Button(frm_start, text='New Game', width=9)
        self.btn_start.grid(row=0, column=0, padx=5, pady=5)
        self.btn_start.config(command=open_event_process)

        self.btn_confirm = tk.Button(frm_start, text='Confirm', width=9)
        self.btn_confirm.grid(row=1, column=0, padx=5, pady=5)
        self.btn_confirm.config(command=run_event_process)
        self.btn_confirm.config(state=tk.DISABLED)

    def set_open_state(self):
        self.btn_confirm.config(state=tk.NORMAL)

    def set_running_state(self):
        self.btn_confirm.config(state=tk.DISABLED)


class GUI_ACTIONS:
    def __init__(self, frm_father, gui_row, gui_column, act_event_process):
        # the actions form
        frm_actions = tk.Frame(frm_father)
        frm_actions.grid(row=gui_row, column=gui_column, columnspan=3,
            padx=5, pady=5)

        # constants of actions
        self.action_button_rows = 5
        self.action_button_columns = 6
        action_button_width = 9
        action_button_padx = 4
        action_button_pady = 2

        self.action_list = []       # display control variable list
        self.action_button_list = []  # button widget list (maybe convert this list to a _local one)

        # action buttons
        for row in range(self.action_button_rows):
            for column in range(self.action_button_columns):
                action_idx = row * self.action_button_columns + column
                self.action_list.append(tk.StringVar())
                self.action_list[action_idx].set('')
                self.action_list[action_idx].set(str(action_idx))   #debug
                self.action_button_list.append(
                    tk.Button(frm_actions, 
                        textvariable=self.action_list[action_idx], 
                        width=action_button_width))
                self.action_button_list[action_idx].grid(row=row, column=column, 
                    padx=action_button_padx, pady=action_button_pady)
                def action_buttion_click(act_num = action_idx):
                    act_event_process(act_num)
                self.action_button_list[action_idx].config(command=action_buttion_click)

    def set_open_state(self):
        for action_idx in range(self.action_button_rows * self.action_button_columns):
            self.action_list[action_idx].set('')
            self.action_button_list[action_idx].config(state=tk.DISABLED)

    def set_possible_actions(self, possible_action_list):
        self.set_open_state()
        for action_idx, action in enumerate(possible_action_list):
            self.action_list[action_idx].set(action)
            self.action_button_list[action_idx].config(state=tk.NORMAL)


class GUI_ADVICE:
    def __init__(self, ini_parser, frm_father, gui_row, gui_column):
        # the advice form
        frm_advice = tk.Frame(frm_father)
        frm_advice.grid(row=gui_row, column=gui_column, pady=5)

        # constants of advice
        advice_disp_width = 15
        self.advice_list_length = int(ini_parser['GUI_ADVICE']['Adice_List_Len'])
        self.advice_list = []       # display control variable list
        self.advice_disp_list = []  # label widget list (maybe convert this list to a _local one)

        # advice label (4 lines)
        for advice_idx in range(self.advice_list_length):
            self.advice_list.append(tk.StringVar())
            self.advice_list[advice_idx].set('')
            self.advice_list[advice_idx].set(str(advice_idx+1))   #debug
            self.advice_disp_list.append(
                tk.Label(frm_advice, textvariable=self.advice_list[advice_idx], 
                    width=advice_disp_width))
            self.advice_disp_list[advice_idx].grid(row=advice_idx, column=0, 
                pady=2)

    def set_advice(self, advices):
        for advice_idx, advice in enumerate(advices):
            if advice_idx >= self.advice_list_length:
                messagebox.showinfo("advice error", "more advices than expectation")
                return
            self.advice_list[advice_idx].set(advice)


class GUI:
    def __init__(self, main_controller):
        # register the controller
        if main_controller is None:
            exit(-1)
        self.controller = main_controller
        
        # create the ini parser
        config = configparser.ConfigParser()
        config.read('texas_move.ini', encoding='utf-8')

        # main window
        win_root = tk.Tk()
        win_root.title("Texas Hold'em")
        win_root.iconbitmap('texas.ico')
        self.frm_root = tk.Frame(win_root, width=800+15*2, height=450+100)
        self.frm_root.grid_propagate(0)
        self.frm_root.grid(padx=15, pady=15)

        # components (keep self. to make test easy)
        self.strd = GUI_STRD(config, self.frm_root, 0, 0)
        self.player_group = GUI_PLAYER_GROUP(config, self.frm_root, 
            self.set_current_event_process_gui)
        self.hole_cards = GUI_HOLE_CARDS(config, self.frm_root, 0, 4)
        self.actions = GUI_ACTIONS(self.frm_root, 1, 1, self.act_event_process)
        self.start = GUI_START(self.frm_root, 2, 0, 
            self.open_event_process, self.run_event_process)
        self.advice = GUI_ADVICE(config, self.frm_root, 2, 4)

        # test buttons
        # _frm_test = tk.Frame(self.frm_root)
        # _frm_test.grid(row=3, column=0, columnspan=5, padx=5, pady=5)

        # _btn_01 = tk.Button(_frm_test, text='S-OPEN', width=9)
        # _btn_01.grid(row=0, column=0, padx=5, pady=2)
        # _btn_01.config(command=self.strd.set_open_state)

        # _btn_02 = tk.Button(_frm_test, text='S-GET', width=9)
        # _btn_02.grid(row=0, column=1, padx=5, pady=2)
        # _btn_02.config(command=self.strd_running)

        # _btn_03 = tk.Button(_frm_test, text='S-RUNNING', width=9)
        # _btn_03.grid(row=0, column=2, padx=5, pady=2)
        # _btn_03.config(command=self.strd.set_running_state)

        # _btn_04 = tk.Button(_frm_test, text='c-open', width=9)
        # _btn_04.grid(row=0, column=3, padx=5, pady=2)
        # _btn_04.config(command=self.hole_cards.set_open_state)

        # _btn_05 = tk.Button(_frm_test, text='c-running', width=9)
        # _btn_05.grid(row=0, column=4, padx=5, pady=2)
        # _btn_05.config(command=self.hole_cards.set_running_state)

        # _btn_06 = tk.Button(_frm_test, text='c-get', width=9)
        # _btn_06.grid(row=0, column=5, padx=5, pady=2)
        # _btn_06.config(command=self.get_hc)

        # _btn_07 = tk.Button(_frm_test, text='g-clear', width=9)
        # _btn_07.grid(row=0, column=6, padx=5, pady=2)
        # _btn_07.config(command=self.player_group.set_open_state)

        # _btn_08 = tk.Button(_frm_test, text='g-running', width=9)
        # _btn_08.grid(row=0, column=7, padx=5, pady=2)
        # _btn_08.config(command=self.player_group.set_running_state)

        # _btn_09 = tk.Button(_frm_test, text='g-call', width=9)
        # _btn_09.grid(row=1, column=0, padx=5, pady=2)
        # _btn_09.config(command=self.pg_call)

        # _btn_10 = tk.Button(_frm_test, text='g-fold', width=9)
        # _btn_10.grid(row=1, column=1, padx=5, pady=2)
        # _btn_10.config(command=self.pg_fold)

        # _btn_11 = tk.Button(_frm_test, text='g-acts', width=9)
        # _btn_11.grid(row=1, column=2, padx=5, pady=2)
        # _btn_11.config(command=self.pg_acts)

        # _btn_12 = tk.Button(_frm_test, text='st-open', width=9)
        # _btn_12.grid(row=1, column=3, padx=5, pady=2)
        # _btn_12.config(command=self.start.set_open_state)

        # _btn_13 = tk.Button(_frm_test, text='st-run', width=9)
        # _btn_13.grid(row=1, column=4, padx=5, pady=2)
        # _btn_13.config(command=self.start.set_running_state)

        # _btn_14 = tk.Button(_frm_test, text='ad-set', width=9)
        # _btn_14.grid(row=1, column=5, padx=5, pady=2)
        # _btn_14.config(command=self.ad_set)

        # _btn_15 = tk.Button(_frm_test, text='act-open', width=9)
        # _btn_15.grid(row=1, column=6, padx=5, pady=2)
        # _btn_15.config(command=self.actions.set_open_state)

        # _btn_16 = tk.Button(_frm_test, text='act-set1', width=9)
        # _btn_16.grid(row=1, column=7, padx=5, pady=2)
        # _btn_16.config(command=self.act_set1)

        # _btn_17 = tk.Button(_frm_test, text='act-set2', width=9)
        # _btn_17.grid(row=2, column=0, padx=5, pady=2)
        # _btn_17.config(command=self.act_set2)

        # _btn_18 = tk.Button(_frm_test, text='g-user', width=9)
        # _btn_18.grid(row=2, column=1, padx=5, pady=2)
        # _btn_18.config(command=self.pg_user)

        # _btn_19 = tk.Button(_frm_test, text='v_acts', width=9)
        # _btn_19.grid(row=2, column=2, padx=5, pady=2)
        # _btn_19.config(command=self.pg_valid_acts)

    def dialog_warn(self, msg):
        messagebox.showinfo("Warning", msg)

    def open_event_process(self):
        self.controller.open_event_process(self)

    def run_event_process(self):
        self.controller.run_event_process(self)

    def act_event_process(self, act_num):
        self.controller.act_event_process(self, act_num)

    def set_current_event_process_gui(self):
        self.controller.set_current_event_process(self)

    def mainloop(self):
        """start the GUI"""
        self.frm_root.mainloop()
        
    # test methods
    # def strd_running(self):     # gui test
    #     messagebox.showinfo("straddle limitation", self.strd.get_strd_limit())

    # def pg_call(self):
    #     self.player_group.process_player_action("CALL")

    # def pg_fold(self):
    #     self.player_group.process_player_action("FOLD")

    # def pg_acts(self):
    #     messagebox.showinfo("player's actions", self.player_group.get_players_all_actions())

    # def pg_valid_acts(self):
    #     messagebox.showinfo("player's actions", self.player_group.get_players_valid_actions())

    # def get_hc(self):
    #     messagebox.showinfo("hole card", self.hole_cards.get_hole_cards())

    # def act_set1(self):
    #     self.actions.set_possible_actions(['call', 'fold', '3 strd'])

    # def act_set2(self):
    #     self.actions.set_possible_actions(['fold', '6 strd', '9 strd', 'all in'])

    # def ad_set(self):
    #     self.advice.set_advice('["fold: 12%", "call: 12%", "23.3 strd: 30%", "pass: 4%"]')

    # def pg_user(self):
    #     messagebox.showinfo("player's actions", self.player_group.get_user_pos())


if __name__ == '__main__':
    # create the GUI and, tell the GUI which controller to use
    mainProgram = GUI()
    # start the GUI, waiting user events
    mainProgram.mainloop()


