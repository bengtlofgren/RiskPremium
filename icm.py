import numpy as np
import itertools

stacks = [1000, 200, 100, 390, 72, 50]

def calc_prob_places(stacks : list):
    # This matrix (row=i,column=j) represents prob that stack i comes in place j
    prob_matrix = np.zeros((len(stacks), len(stacks)))

    # The first row is probability that stack i comes in first place
    prob_matrix[:,0] = np.array(stacks)/np.sum(stacks)

    sum_stacks = sum(stacks)
    # Second column
    for i in range(len(stacks)):
        prob_matrix[i,1] = sum([stacks[j] * stacks[i]/((sum_stacks - stacks[j])*sum_stacks) for j in range(len(stacks)) if j!= i])
    
    # Third column
    for i in range(len(stacks)):
        prob_matrix[i, 2] = sum([
            stacks[j] * stacks[k] * stacks[i] / ((sum_stacks - stacks[j] - stacks[k]) * (sum_stacks - stacks[j]) * sum_stacks)
            for j in range(len(stacks)) for k in range(len(stacks))
            if j != i and k != j and k != i
        ])

    # Fourth column
    if len(stacks) > 3:
        for i in range(len(stacks)):
            prob_matrix[i,3] = sum([
                stacks[i] * stacks[j] * stacks[k] * stacks[l] / (
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l] ) * 
                    (sum_stacks - stacks[j] - stacks[k]) * 
                    (sum_stacks - stacks[j]) 
                    * sum_stacks
                )
                for j in range(len(stacks)) for k in range(len(stacks)) for l in range(len(stacks))
                if j != i and k != j and k != i and l != k and l != j and l != i
            ])
    
    # Fifth column
    if len(stacks) > 4:
        for i in range(len(stacks)):
            prob_matrix[i,4] = sum([
                stacks[i] * stacks[j] * stacks[k] * stacks[l] * stacks[m] / (
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l] - stacks[m]) * 
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l]) * 
                    (sum_stacks - stacks[j] - stacks[k]) * 
                    (sum_stacks - stacks[j]) 
                    * sum_stacks
                )
                for j in range(len(stacks)) for k in range(len(stacks)) for l in range(len(stacks)) for m in range(len(stacks))
                if j != i and k != j and k != i and l != k and l != j and l != i and m != l and m != k and m != j and m != i
            ])
    
    # Sixth column
    if len(stacks) > 5:
        for i in range(len(stacks)):
            prob_matrix[i,5] = sum([
                stacks[i] * stacks[j] * stacks[k] * stacks[l] * stacks[m] * stacks[n] / (
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l] - stacks[m] - stacks[n]) * 
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l] - stacks[m]) * 
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l]) * 
                    (sum_stacks - stacks[j] - stacks[k]) * 
                    (sum_stacks - stacks[j]) 
                    * sum_stacks
                )
                for j in range(len(stacks)) for k in range(len(stacks)) for l in range(len(stacks)) for m in range(len(stacks)) for n in range(len(stacks))
                if j != i and k != j and k != i and l != k and l != j and l != i and m != l and m != k and m != j and m != i and n != m and n != l and n != k and n != j and n != i
            ])
        
    # Seventh column
    if len(stacks) > 6:
        for i in range(len(stacks)):
            prob_matrix[i,6] = sum([
                stacks[i] * stacks[j] * stacks[k] * stacks[l] * stacks[m] * stacks[n] * stacks[o] / (
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l] - stacks[m] - stacks[n] - stacks[o]) * 
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l] - stacks[m] - stacks[n]) * 
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l] - stacks[m]) * 
                    (sum_stacks - stacks[j] - stacks[k] - stacks[l]) * 
                    (sum_stacks - stacks[j] - stacks[k]) * 
                    (sum_stacks - stacks[j]) 
                    * sum_stacks
                )
                for j in range(len(stacks)) for k in range(len(stacks)) for l in range(len(stacks)) for m in range(len(stacks)) for n in range(len(stacks)) for o in range(len(stacks))
                if j != i and k != j and k != i and l != k and l != j and l != i and m != l and m != k and m != j and m != i and n != m and n != l and n != k and n != j and n != i and o != n and o != m and o != l and o != k and o != j and o != i
            ])
    return prob_matrix

def calc_prob(current, remaining, total, depth=6):
    if len(remaining) == 0:
        prob = 1
        for i, stack in enumerate(current):
            if i == 0 :
                prob *= stack / total
            elif i < depth:
                total -= stack
                prob *= stack / total
        return prob
    else:
        return sum(calc_prob(current + [stack], [r for r in remaining if r != stack], total, depth) for stack in remaining)

def calc_prob_matrix(stacks):
    prob_matrix = np.zeros((len(stacks), len(stacks)))
    total = sum(stacks)

    for j in range(prob_matrix.shape[1]):
        for i in range(len(stacks)):
            prob_matrix[i, j] = calc_prob([stacks[i]], [stack for k, stack in enumerate(stacks) if k != i], total, depth=j+1)
    return prob_matrix

def make_perms(stacks):
    all_perms = list(list(a) for a in itertools.permutations(stacks))
    split = len(all_perms)//len(stacks)
    stack_dict = {i : all_perms[i*split:(i+1)*split] for i in range(len(stacks))}
    return stack_dict

def calc_prob(current, total):
    prob = 1
    for i, stack in enumerate(current):
        if i == 0 :
            prob *= stack / total
        else:
            total -= stack
            prob *= stack / total
    return prob

def cut_perms(perms, n, stack_length=6):
    repeat_len = np.math.factorial(stack_length - n - 1)
    cut_size = len(perms)//repeat_len
    cut_list = [repeat_len*i for i in range(cut_size)]
    return [perms[cut_index][:n+1] for cut_index in cut_list]


def calc_prob_matrix(stacks):
    prob_matrix = np.zeros((len(stacks), len(stacks)))
    total = sum(stacks)
    stack_orderings = make_perms(stacks)

    for j in range(prob_matrix.shape[1]):
        for i in range(prob_matrix.shape[0]):
            cutted_perms = cut_perms(stack_orderings[i], j, len(stacks))
            prob_matrix[i, j] = sum(calc_prob(cutted_perms[l], total) for l in range(len(cutted_perms)))
    return prob_matrix


c = calc_prob_matrix(stacks)
print(c)




