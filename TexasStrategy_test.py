import unittest
import TexasStrategy

class TexasStrategyTest(unittest.TestCase):
    def setUp(self):
        print("Creating test objects ...")
        self.ts = TexasStrategy.TexasStrategy()
        
    def test_get_advice_file_name_01(self):
        print('\ntest_get_advice_file_name_01 :')
        print(r"test case: 50straddles\CO\CO_strategy.txt")
        user_name = 'CO'
        action_list = [{'SB':['SB']}, {'BB':['BB']}, {'UTG':['2BB']}, {'UTG+1':['Fold']}, {'UTG+2':['Fold']}, {'HJ':['Fold']}, {'CO':[]}, {'BTN':[]}]
        test_file_name = self.ts.get_advice_file_name(user_name, action_list)
        expected_file_name = 'CO_strategy.txt'
        self.assertEqual(expected_file_name, test_file_name)

    def test_get_advice_file_name_02(self):
        print('\ntest_get_advice_file_name_02 :')
        print(r"test case: 50straddles\BTN\vs_4bet\BTN_3.5strd_BB_Call_UTG_15.7strd_BTN_Call_BB_AllIn_UTG_Fold_BTN_strategy")
        user_name = 'BTN'
        action_list = [{'SB':['SB', 'Fold', 'Fold']}, \
            {'BB':['BB', 'Call', 'AllIn']}, \
            {'UTG':['2BB', '15.7strd', 'Fold']}, \
            {'UTG+1':['Fold', 'Fold', 'Fold']}, \
            {'UTG+2':['Fold', 'Fold', 'Fold']}, \
            {'HJ':['Fold', 'Fold', 'Fold']}, \
            {'CO':['Fold', 'Fold', 'Fold']}, \
            {'BTN':['3.5strd', 'Call']}]
        test_file_name = self.ts.get_advice_file_name(user_name, action_list)
        expected_file_name = 'BTN_3.5strd_BB_Call_UTG_15.7strd_BTN_Call_BB_AllIn_UTG_Fold_BTN_strategy.txt'
        self.assertEqual(expected_file_name, test_file_name)

    def test_get_advice_file_name_03(self):
        print('\ntest_get_advice_file_name_03 :')
        print(r"test case: 100straddles\UTG+2\vs_5bet\UTG+1_3.5strd_UTG+2_10.6strd_CO_24.0strd_BTN_AllIn_BB_Call_UTG_Call_UTG+1_Call_UTG+2_strategy")
        user_name = 'UTG+2'
        action_list = [{'SB':['SB', 'Fold']}, \
            {'BB':['BB', 'Call']}, \
            {'UTG':['2BB', 'Call']}, \
            {'UTG+1':['3.5strd', 'Call']}, \
            {'UTG+2':['10.6strd']}, \
            {'HJ':['Fold']}, \
            {'CO':['24.0strd']}, \
            {'BTN':['AllIn']}]
        test_file_name = self.ts.get_advice_file_name(user_name, action_list)
        expected_file_name = 'UTG+1_3.5strd_UTG+2_10.6strd_CO_24.0strd_BTN_AllIn_BB_Call_UTG_Call_UTG+1_Call_UTG+2_strategy.txt'
        self.assertEqual(expected_file_name, test_file_name)

    def test_read_strategy_file_01(self):
        absolute_file_name = r'C:\WorkSpace\texas_holdem\PrecalRes\100straddles\UTG\SB_Call_BB_6.0strd_UTG_strategy.txt'
        hole_cards = [['黑','T'],['红','T']]
        print('\ntest_read_strategy_file_01:')
        print(r'100straddles\UTG\SB_Call_BB_6.0strd_UTG_strategy.txt' + ' - ' + "['黑','T'],['红','T']")
        test_advice = self.ts.read_strategy_file(absolute_file_name, hole_cards)
        expected_advice = ['Fold:0.0','18.0strd:0.062','Call:0.938']
        self.assertEqual(expected_advice, test_advice)

    def test_read_strategy_file_02(self):
        absolute_file_name = r'C:\WorkSpace\texas_holdem\PrecalRes\100straddles\UTG\SB_Call_BB_6.0strd_UTG_strategy.txt'
        hole_cards = [['黑','T'],['黑','6']]
        print('\ntest_read_strategy_file_02:')
        print(r'100straddles\UTG\SB_Call_BB_6.0strd_UTG_strategy.txt' + ' - ' + "['黑','T'],['黑','6']")
        test_advice = self.ts.read_strategy_file(absolute_file_name, hole_cards)
        expected_advice = ['Fold:0.002','18.0strd:0.218','Call:0.782']
        self.assertEqual(expected_advice, test_advice)   

    def test_read_strategy_file_03(self):
        absolute_file_name = r'C:\WorkSpace\texas_holdem\PrecalRes\100straddles\UTG\SB_Call_BB_6.0strd_UTG_strategy.txt'
        hole_cards = [['黑','6'],['黑','T']]
        print('\ntest_read_strategy_file_03:')
        print(r'100straddles\UTG\SB_Call_BB_6.0strd_UTG_strategy.txt' + ' - ' + "['黑','6'],['黑','T']")
        test_advice = self.ts.read_strategy_file(absolute_file_name, hole_cards)
        expected_advice = ['Fold:0.002','18.0strd:0.218','Call:0.782']
        self.assertEqual(expected_advice, test_advice)  

    def test_read_strategy_file_04(self):
        absolute_file_name = r'C:\WorkSpace\texas_holdem\PrecalRes\100straddles\BTN\UTG+1_3.5strd_UTG+2_Call_BTN_strategy.txt'
        hole_cards = [['片','K'],['梅','Q']]
        print('\ntest_read_strategy_file_04:')
        print(r'100straddles\BTN\UTG+1_3.5strd_UTG+2_Call_BTN_strategy' + ' - ' + "['片','K'],['梅','Q']")
        test_advice = self.ts.read_strategy_file(absolute_file_name, hole_cards)
        expected_advice = ['Fold:0.716','14.1strd:0.284']
        self.assertEqual(expected_advice, test_advice) 

    def test_read_strategy_file_05(self):
        absolute_file_name = r'C:\WorkSpace\texas_holdem\PrecalRes\100straddles\BTN\UTG+1_3.5strd_UTG+2_Call_BTN_strategy.txt'
        hole_cards = [['片','2'],['梅','2']]
        print('\ntest_read_strategy_file_05:')
        print(r'100straddles\BTN\UTG+1_3.5strd_UTG+2_Call_BTN_strategy' + ' - ' + "['片','2'],['梅','2']")
        test_advice = self.ts.read_strategy_file(absolute_file_name, hole_cards)
        expected_advice = ['Fold:1.0','14.1strd:0.0']
        self.assertEqual(expected_advice, test_advice) 

    def test_read_strategy_file_06(self):
        absolute_file_name = r'C:\WorkSpace\texas_holdem\PrecalRes\100straddles\BTN\vs_3bet\HJ_3.5strd_BTN_Call_SB_17.6strd_HJ_Fold_BTN_strategy.txt'
        hole_cards = [['片','J'],['梅','J']]
        print('\ntest_read_strategy_file_06:')
        print(r'100straddles\BTN\vs_3bet\HJ_3.5strd_BTN_Call_SB_17.6strd_HJ_Fold_BTN_strategy' + ' - ' + "['片','J'],['梅','J']")
        test_advice = self.ts.read_strategy_file(absolute_file_name, hole_cards)
        expected_advice = ['Call:0.242','40.8strd:0.0', 'Fold:0.0', 'AllIn:0.758']
        self.assertEqual(expected_advice, test_advice) 

    def test_read_strategy_file_07(self):
        absolute_file_name = r'C:\WorkSpace\texas_holdem\PrecalRes\100straddles\BTN\vs_3bet\HJ_3.5strd_BTN_Call_SB_17.6strd_HJ_Fold_BTN_strategy.txt'
        hole_cards = [['片','4'],['片','A']]
        print('\ntest_read_strategy_file_07:')
        print(r'100straddles\BTN\vs_3bet\HJ_3.5strd_BTN_Call_SB_17.6strd_HJ_Fold_BTN_strategy' + ' - ' + "['片','4'],['片','A']")
        test_advice = self.ts.read_strategy_file(absolute_file_name, hole_cards)
        expected_advice = ['Call:0.486','40.8strd:0.0', 'Fold:0.514', 'AllIn:0.0']
        self.assertEqual(expected_advice, test_advice) 

    def tearDown(self):
        print("Destroying test objects ...")
        self.ts = None

if __name__ == "__main__":
    unittest.main()