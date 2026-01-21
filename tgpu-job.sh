#!/bin/bash
#SBATCH --job-name=SiC_Profile_Final
#SBATCH --account=ACD114087
#SBATCH --partition=gp1d
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --output=test_run6.log


export DFTBPLUS_PARAM_DIR=~/opt/slakos/
export OMP_NUM_THREADS=4
spack load intel-oneapi-vtune
spack load dftbplus



mpirun -np 1 vtune \
    -collect threading \
    -r ./vtune_result_final \
    dftb+
if [ -d "./vtune_result_final" ]; then
    vtune -report summary -r ./vtune_result_final -format html -report-output vtune_report_final.html
	#vtune -collect hotspots -knob sampling-mode=sw -r "${VTUNE_RES}" -- \
	 # 	srun --mpi=pmix -n ${SLURM_NTASKS} -c ${SLURM_CPUS_PER_TASK} --cpu-bind=cores dftb+
    echo "-> Success! Report generated: vtune_report_final.html"
else
    echo "-> Error: VTune collection failed."
fi

echo "Done!"
