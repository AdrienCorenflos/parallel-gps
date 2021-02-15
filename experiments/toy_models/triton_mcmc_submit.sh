#!/bin/bash parallel-gps

step_size=0.01
n_runs=10

for mcmc in HMC MALA NUTS; do
  for cov in Matern32 Matern52 RBF; do
    sbatch triton_mcmc_PSSGP.sh $step_size $n_runs $mcmc $cov "/gpu:0" --time=05:00:00
    sbatch triton_mcmc_SSGP.sh $step_size $n_runs $mcmc $cov "/cpu:0" --time=02-10
    sbatch triton_mcmc_GP.sh $step_size $n_runs $mcmc $cov "/gpu:0" --time=05:00:00
  done
done