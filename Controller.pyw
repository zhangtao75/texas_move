from GUI import GUI
from TexasStrategy import TexasStrategy

class Controller():
    """docstring for controller"""
    def __init__(self, module):
        self.possible_action_list = []
        self.module = module

    def open_event_process(self, view):
        view.strd.set_open_state()
        view.player_group.set_open_state()
        view.hole_cards.set_open_state()
        view.actions.set_open_state()
        view.start.set_open_state()
        view.advice.set_advice(["", "", "", ""])

    def run_event_process(self, view):
        hole_card1, hole_card2 = view.hole_cards.get_hole_cards()
        # check
        if view.strd.get_strd_limit() == 0:
            view.dialog_warn('Please set the straddle limitation')
            return
        if view.player_group.get_user_pos() == 0:
            view.dialog_warn("Please set the user's position")
            return
        if (hole_card1[0] == '空' or 
            hole_card1[1] == '空' or 
            hole_card2[0] == '空' or 
            hole_card2[1] == '空'):
            view.dialog_warn("Please set the user's hole cards")
            return
        if hole_card1 == hole_card2:
            view.dialog_warn("Please set the user's hole cards correctly")
            return
        
        # set
        view.strd.set_running_state()
        view.player_group.set_running_state()
        view.hole_cards.set_running_state()
        view.start.set_running_state()
        self.set_act(view)
        self.set_advice(view)
        
    def act_event_process(self, view, act_num):
        action = self.possible_action_list[act_num]
        view.player_group.process_player_action(action)
        self.set_act(view)
        self.set_advice(view)
        # if (auto_process == False) and \
        #     (view.player_group.get_current_player_previous_action() == 'Fold'):
        if view.player_group.get_current_player_previous_action() == 'Fold':
            self.act_event_process(view, 0)
        
    def set_current_event_process(self, view):
        self.set_act(view)
        self.set_advice(view)
        
    def set_act(self, view):
        self.possible_action_list = self.module.get_possible_actions(
            view.strd.get_strd_limit(),
            view.player_group.get_user_name(),
            view.player_group.get_current_player_name())
        view.actions.set_possible_actions(self.possible_action_list)

    def set_advice(self, view):
        if view.player_group.get_user_pos() == view.player_group.get_current_pos():
            current_advice_list = self.module.get_advice(
                view.strd.get_strd_limit(),
                view.player_group.get_user_name(),
                view.player_group.get_players_valid_actions(),
                view.hole_cards.get_hole_cards())
        else:
            current_advice_list = ["", "", "", ""]
        view.advice.set_advice(current_advice_list)

if __name__ == '__main__':
    texasStrategy = TexasStrategy()
    controller = Controller(texasStrategy)
    mainProgram = GUI(controller)
    mainProgram.mainloop()