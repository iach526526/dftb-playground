#!/bin/sh
#SBATCH --account=ACD114087
#SBATCH --partition=development
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --cpus-per-task=2
#SBATCH --time=00:30:00
#SBATCH --output=run-dftb-64bit-task.out

set -euo pipefail
echo "Starting job on $(date)"
echo "HOST=$(hostname)"
echo "CPUS=${SLURM_CPUS_PER_TASK:-unknown}"
JOBS=${SLURM_CPUS_PER_TASK:-1}

# load package
spack load intel-oneapi-vtune
spack load dftbplus

# set param dir
export DFTBPLUS_PARAM_DIR=~/opt/slakos
VTUNE_RESULT=vtune_result_${SLURM_JOB_ID}
#vtune \
 # -collect hotspots \
  #-result-dir ${VTUNE_RESULT} \
 # -- \
 # dftb+
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export OMP_PROC_BIND=close
export OMP_PLACES=cores

#aps --result-dir=./aps_result dftb+

APS_RESULT="aps_${SLURM_JOB_ID}"
#mpirun aps --result-dir="./${APS_RESULT}" dftb+
aps --result-dir="./${APS_RESULT}" -- \
  srun --mpi=pmix -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=cores \
  dftb+
