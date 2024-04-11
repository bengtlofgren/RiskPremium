use factorial::Factorial;
use itertools::Itertools;

fn calc_prob(current: &[f64], total: f64) -> f64 {
    let mut prob = 1.0;
    let mut total = total;
    for (i, &stack) in current.iter().enumerate() {
        if i == 0 {
            prob *= stack / total;
        } else {
            total -= stack;
            prob *= stack / total;
        }
    }
    prob
}

// So the straightforward version is to just create a new permutation for each stack size. 
// A more efficient version would be to create a permutation for the largest stack size and then cut it down to the smaller stack sizes.
// This is a bit more complicated, but it should be more efficient.
fn cut_perms(perms: &[Vec<f64>], n: usize, stack_length: usize) -> Vec<Vec<f64>> {
    let repeat_size = (stack_length - n - 1).factorial();
    let cut_size: usize = perms.len() / repeat_size;
    let cut_list: Vec<usize> = (0..cut_size).map(|i| repeat_size * i).collect();    
    cut_list.iter().map(|&cut_index| perms[cut_index][..=n].to_vec()).collect()
}



fn make_stack_orderings(stacks: Vec<f64>) -> Vec<Vec<Vec<f64>>> {
    let stack_length = stacks.len();
    let stack_orderings: Vec<_> = stacks.iter().cloned().permutations(stack_length).collect();
    let split = stack_orderings.len() as u32 / stacks.len() as u32;
    let mut ordered_stack_orderings = vec![];
    for i in 0..stacks.len() {
        let start = i * split as usize;
        let end = (i + 1) * split as usize;
        ordered_stack_orderings.push(stack_orderings[start..end].to_vec());
    }
    ordered_stack_orderings
}

fn calc_prob_matrix(stacks: &Vec<f64>) -> Vec<Vec<f64>> {
    let total = stacks.iter().sum::<f64>();
    let stack_orderings: Vec<_> = make_stack_orderings(stacks.clone());
    let mut prob_matrix = vec![vec![0.0; stacks.len()]; stacks.len()];

    for j in 0..prob_matrix[0].len() {
        for i in 0..prob_matrix.len() {
            let cutted_perms = cut_perms(&stack_orderings[i], j, stacks.len());
            prob_matrix[i][j] = cutted_perms.iter().map(|perm| calc_prob(perm, total)).sum::<f64>();
        }
    }
    prob_matrix
}

// fn main() {
//     let stacks = vec![1000.0, 200.0, 100.0, 390.0, 72.0, 50.0];
//     let c = calc_prob_matrix(&stacks);
//     println!("{:?}", c);
// }