use itertools::Itertools;
use factorial::Factorial;
use ndarray::Array1;
use ndarray::Array2;
use ndarray::arr1;

pub struct ICMSolver {
    pub stacks: Vec<f64>,
    pub prob_matrix: Array2<f64>,
    pub payouts: Vec<f64>,
    pub icm_values: Vec<f64>,
}

impl ICMSolver {
    pub fn new(stacks: Vec<f64>, payouts: Vec<f64>) -> Self {
        let prob_matrix = Self::calc_prob_matrix(&stacks);
        let icm_values = prob_matrix.dot(&arr1(&payouts)).to_vec();
        Self { stacks, prob_matrix, payouts, icm_values}
    }

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

    fn calc_prob_matrix(stacks: &Vec<f64>) -> Array2<f64> {
        let total = stacks.iter().sum::<f64>();
        let stack_orderings: Vec<_> = Self::make_stack_orderings(stacks.clone());
        let mut prob_matrix = Array2::zeros((stacks.len(), stacks.len()));
    
        for j in 0..prob_matrix.ncols() {
            for i in 0..prob_matrix.nrows() {
                let cutted_perms = Self::cut_perms(&stack_orderings[i], j, stacks.len());
                prob_matrix[[i, j]] = cutted_perms.iter().map(|perm| Self::calc_prob(perm, total)).sum::<f64>();
            }
        }
        prob_matrix
    }
}

pub struct RiskPremium {
    pub stacks: Vec<f64>,
    pub payouts: Vec<f64>,
    pub neutral_icm: Array1<f64>,
    pub win_matrix: Array2<f64>,
    pub lose_matrix: Array2<f64>,
    pub rp_matrix: Array2<f64>,
}

impl RiskPremium {
    pub fn new(stacks: Vec<f64>, payouts: Vec<f64>) -> Self {
        let icm_solver = ICMSolver::new(stacks.clone(), payouts.clone());
        let neutral_icm = arr1(&icm_solver.icm_values);
        let mut rp = Self {
            stacks,
            payouts,
            neutral_icm,
            win_matrix: Array2::zeros((0, 0)), // temporary values
            lose_matrix: Array2::zeros((0, 0)), // temporary values
            rp_matrix: Array2::zeros((0, 0)), // temporary values
        };
        let (win_matrix, lose_matrix) = rp.calc_stackoff_matrix();
        rp.win_matrix = win_matrix;
        rp.lose_matrix = lose_matrix;
        rp.rp_matrix = rp.calc_rp_matrix();
        rp
    }

    fn calc_stackoff_matrix(&mut self) -> (Array2<f64>, Array2<f64>) {
        let len = self.stacks.len();
        let mut a = Array2::zeros((len, len));
        let mut b = Array2::zeros((len, len));
        for i in 0..len {
            for j in 0..len {
                let mut new_stacks = self.stacks.clone();
                if i == j {
                    a[[i, i]] = self.neutral_icm[i];
                } else {
                    let loser_stack = f64::max(0.000000001, new_stacks[j] - new_stacks[i]);
                    let winner_stack = f64::min(new_stacks[j] + new_stacks[i], 2.0 * new_stacks[i]);
                    new_stacks[i] = winner_stack;
                    new_stacks[j] = loser_stack;
                    let icm_solver = ICMSolver::new(new_stacks, self.payouts.clone());
                    a[[i, j]] = icm_solver.icm_values[i];
                    b[[j, i]] = icm_solver.icm_values[j];
                }
            }
        }
        (a, b)
    }

    fn calc_rp_matrix(&self) -> Array2<f64> {
        let neutral_matrix = (self.neutral_icm.clone() * Array2::<f64>::ones((self.stacks.len(), self.stacks.len()))).reversed_axes();
        let numerator = &neutral_matrix - &self.lose_matrix;
        let denominator = &self.win_matrix - &self.lose_matrix;
        (&numerator / &denominator - 0.5 * Array2::eye(self.stacks.len()) - 0.5 * Array2::ones((self.stacks.len(), self.stacks.len()))) * 100.0
    }
}