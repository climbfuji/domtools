#!/bin/sh -l
#PBS -o out.pbs
#PBS -e err.pbs
#PBS -N srh03
#PBS -A P48503002
#PBS -q premium
#PBS -l select=1:ncpus=36:mpiprocs=36
#PBS -l walltime=04:00:00
#PBS -m abe
#PBS -M "dom.heinzeller@noaa.gov"

cd /glade/p/ral/jntp/dheinzel/orion_3km/run_dom_gsd_noah_keep_going_new_2021_with_io

source ./load_modules.sh
ulimit -a

time python srh.py 0  &
time python srh.py 3  &
time python srh.py 6   
time python srh.py 9  &
time python srh.py 12 &
time python srh.py 15  
time python srh.py 18 &
time python srh.py 21 &
time python srh.py 24  
time python srh.py 27 &
time python srh.py 30 &
time python srh.py 33  
time python srh.py 36 &
time python srh.py 39 &
time python srh.py 42  
time python srh.py 45 &
time python srh.py 48 &
time python srh.py 51  
time python srh.py 54 &
time python srh.py 57 &
time python srh.py 60  
time python srh.py 63 &
time python srh.py 66 &
time python srh.py 69  
time python srh.py 72 &
time python srh.py 75 &
time python srh.py 78  
time python srh.py 81 &
time python srh.py 84 &
time python srh.py 87  
time python srh.py 90 &
time python srh.py 93 &
time python srh.py 96
exit

                       