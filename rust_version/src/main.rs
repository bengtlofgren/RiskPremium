mod icm;
use icm::ICMSolver;
use icm::RiskPremium;

fn main() {
    let stacks = vec![1000.0, 200.0, 100.0, 390.0, 72.0, 50.0, 30.0, 20.0, 10.0];
    let payouts = vec![2000.0, 800.0, 400.0, 100.0, 50.0, 0.0, 0.0, 0.0, 0.0];
    let c = ICMSolver::new(stacks.clone(), payouts.clone());
    let rp = RiskPremium::new(stacks, payouts);
    println!("{:?}", rp.rp_matrix);
}