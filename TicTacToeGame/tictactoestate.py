from basegamestate import BaseGameState
import random

class TicTacToeState(BaseGameState):


    winning_states = {
        1: ['X', 'X', 'X', None, None, None, None, None, None],
        2: [None, None, None, 'X', 'X', 'X', None, None, None],
        3: [None, None, None, None, None, None, 'X', 'X', 'X'],
        4: ['X', None, None, 'x', None, None, 'X', None, None],
        5: [None, 'X', None, None, 'X', None, None, 'X', None],
        6: [None, None, 'X', None, None, 'X', None, None, 'X'],
        7: ['X', None, None, None, 'X', None, None, None, 'X'],
        8: [None, None, 'X', None, 'X', None, 'X', None, None],
        9: ['O', 'O', 'O', None, None, None, None, None, None],
        10: [None, None, None, 'O', 'O', 'O', None, None, None],
        11: [None, None, None, None, None, None, 'O', 'O', 'O'],
        12: ['O', None, None, 'O', None, None, 'O', None, None],
        13: [None, 'O', None, None, 'O', None, None, 'O', None],
        14: [None, None, 'O', None, None, 'O', None, None, 'O'],
        15: ['O', None, None, None, 'O', None, None, None, 'O'],
        16: [None, None, 'O', None, 'O', None, 'O', None, None]

    }

    def __init__(self, state_list, parent=None, children=None):
        self.state_list = state_list
        self.moves_so_far = sum([1 for el in self.state_list if el])
        self.current_player = self.moves_so_far % 2
        agg_fn = (min, max)[self.current_player]
        super(TicTacToeState, self).__init__(parent=parent, agg_fn=agg_fn, children=children)
        self.string_rep =''
        self._static_score = None

    @property
    def children(self):
        if self._children:
            return self._children

        if self.is_end_game:
            return []

        move = ('X', 'O')[self.current_player]

        for index in range(len(self.state_list)):
            if self.state_list[index] is None:
                temp_state = list(self.state_list)
                temp_state[index] = move
                self._children.append(TicTacToeState(temp_state))

        return self._children

    @property
    def monte_carlo_moveset(self, num_moves=4):
        if self._monte_carlo_moveset:
            return self._monte_carlo_moveset

        if self.is_end_game:
            self._monte_carlo_moveset = []

        move = ('X', 'O')[self.current_player]
        indices = []
        index = random.randint(0,8)

        for i in range(min(num_moves, 9 - self.moves_so_far)):
            while(self.state_list[index] is not None or index in indices):
                index = random.randint(0,8)
            temp_state = list(self.state_list)
            temp_state[index] = move
            self._monte_carlo_moveset.append(TicTacToeState(temp_state))
            indices.append(index)

        return self._monte_carlo_moveset


    @property
    def static_score(self):
        pass

    @property
    def state(self):
        return self.state_list

    #@property
    def is_end_game(self):
        if self.moves_so_far == 9:
            return True

        x_list = self.isolate_x()
        o_list = self.isolate_o()
        winner = self.find_winner(x_list, o_list)

        if winner == 'X' or winner == 'O':
            return True

        return False


    def find_winner(self, x_list, o_list):
        for i in range(0, 9):
            temp_win = self.winning_states.get(i)
            if x_list == temp_win:
                return 'X'
        for i in range(9, 17):
            temp_win = self.winning_states.get(i)
            if o_list == temp_win:
                return 'O'


    def isolate_x(self):
        x_list = [el for el in self.state_list]
        for i in range(len(self.state_list)):
            if x_list[i] == 'O':
                x_list[i] = None
        return x_list

    def isolate_o(self):
        o_list = [el for el in self.state_list]
        for i in range(len(self.state_list)):
            if o_list[i] == 'X':
                o_list[i] = None
        return o_list

    #@property
    def winning_player(self):
        if self.is_end_game:
            x_list = self.isolate_x()
            o_list = self.isolate_o()
            winner = self.find_winner(x_list, o_list)
            if winner == 'X':
                return 1
            elif winner == 'O':
                return -1
            else:
                return 0
        return None



    def make_random_move(self):
        temp_state = list(self.state_list)
        move = ('X', 'O')[self.current_player]
        index = random.randint(0,8)

        while (self.state_list[index] is not None):
            index = random.randint(0,8)

        temp_state[index] = move
        child = TicTacToeState(temp_state)

        return child

    def __str__(self):
        if self.string_rep:
            return self.string_rep

        for row in range(3):
            for col in range(3):
                if self.state_list[3*row + col]:
                    self.string_rep += str(self.state_list[3*row + col])
                else:
                    self.string_rep += ' '

            self.string_rep += '\n'
        return self.string_rep

if __name__ == '__main__':
    test_obj = TicTacToeState(['X', None, None, 'O', 'X', None, 'O', None, 'X'])
    test_obj2 = TicTacToeState(['O', 'O', 'O', 'X', None, 'O', None, 'O', None])
    #print (test_obj, end='\n')
    #print ('\n'.join([str(child) for child in test_obj.monte_carlo_moveset]), end='')
    print(test_obj2.is_end_game())
    print(test_obj2.winning_player())
