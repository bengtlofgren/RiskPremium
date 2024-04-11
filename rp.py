import numpy as np
import itertools

stacks = [1000, 500, 499, 10, 5, 4, 3, 2, 1,]
payouts = np.array([2000, 800, 400, 100, 50, 0, 0, 0, 0])
stacks = [1000, 200, 100, 390, 72, 50, 30, 20, 10]
payouts = np.array([2000, 800, 400, 100, 50, 0, 0, 0, 0])

class ICMSolver:
    def __init__(self, stacks, payouts = None):
        self.stacks = stacks
        self.prob_matrix = self.calc_prob_matrix(stacks)
        self.payouts = payouts
        self.icm_values = self.prob_matrix @ payouts

    def make_perms(self, stacks):
        all_perms = list(list(a) for a in itertools.permutations(stacks))
        split = len(all_perms)//len(stacks)
        stack_dict = {i : all_perms[i*split:(i+1)*split] for i in range(len(stacks))}
        return stack_dict

    def calc_prob(self, current, total):
        prob = 1
        for i, stack in enumerate(current):
            if i == 0 :
                prob *= stack / total
            else:
                total -= stack
                prob *= stack / total
        return prob

    def cut_perms(self, perms, n, stack_length=6):
        repeat_len = np.math.factorial(stack_length - n - 1)
        cut_size = len(perms)//repeat_len
        cut_list = [repeat_len*i for i in range(cut_size)]
        return [perms[cut_index][:n+1] for cut_index in cut_list]

    def calc_prob_matrix(self, stacks):
        prob_matrix = np.zeros((len(stacks), len(stacks)))
        total = sum(stacks)
        stack_orderings = self.make_perms(stacks)

        for j in range(prob_matrix.shape[1]):
            for i in range(prob_matrix.shape[0]):
                cutted_perms = self.cut_perms(stack_orderings[i], j, len(stacks))
                prob_matrix[i, j] = sum(self.calc_prob(cutted_perms[l], total) for l in range(len(cutted_perms)))
        return prob_matrix
    

class RP:
    def __init__(self, stacks, payouts = None):
        self.stacks = stacks
        self.payouts = payouts
        self.neutral_icm = ICMSolver(stacks, payouts).icm_values
        self.win_matrix, self.lose_matrix = self.calc_stackoff_matrix()
        self.rp_matrix = self.calc_rp_matrix()

    def calc_stackoff_matrix(self):
        # winning matrix = a
        a = np.zeros((len(self.stacks), len(self.stacks)))
        # losing matrix = b
        b = np.zeros((len(self.stacks), len(self.stacks)))
        for i in range(a.shape[0]):
            # print(f"player {i}'s turn")
            for j in range(a.shape[1]):
                new_stacks = self.stacks.copy()
                # print("player {} shoves, player {} calls".format(i, j))
                if i == j:
                    a[i,i] = self.neutral_icm[i]
                else:
                    loser_stack = max(0.000000001, new_stacks[j] - new_stacks[i])
                    winner_stack = min(new_stacks[j] + new_stacks[i], 2*new_stacks[i])
                    new_stacks[i] = winner_stack
                    new_stacks[j] = loser_stack
                    # print("new stacks are {}".format(new_stacks))
                    icm_solver = ICMSolver(new_stacks, self.payouts)
                    # print(f"player {i}'s probability matrix is :")
                    # print(icm_solver.prob_matrix[i])
                    # print(f"player {j}'s probability matrix is :")
                    # print(icm_solver.prob_matrix[j])
                    # print(f"new icm values are {icm_solver.icm_values}")
                    # Add the ev of the winning player's shove
                    a[i, j] = icm_solver.icm_values[i]
                    # Add the ev of the losing player's shove
                    b[j, i] = icm_solver.icm_values[j]
                    # print('-----------------------------------')
        return a,b
    def calc_rp_matrix(self):
        neutral_matrix = (self.neutral_icm * np.ones_like(self.win_matrix)).T
        numerator = neutral_matrix - self.lose_matrix
        denominator = self.win_matrix - self.lose_matrix
        return (numerator / denominator - 0.5* np.eye(len(self.stacks)) - 0.5*np.ones_like(self.win_matrix))*100
    

stacks = stacks
payouts = payouts
icm_solver = ICMSolver(stacks, payouts)

# print(icm_solver.prob_matrix)
# print(icm_solver.icm_values)

rp_instance = RP(stacks, payouts)
win_matrix = rp_instance.win_matrix
lose_matrix = rp_instance.lose_matrix
rp_matrix = rp_instance.rp_matrix

print(rp_matrix)

