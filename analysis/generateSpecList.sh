#!/bin/bash

# generateSpecList.sh
# Accepts date input, navigates to folder and generates a list of the .psa files there
# Note: path needs to be modified for location where code is being run.

rm p_spectra.txt
#echo "Chosen date is $1"
cd  /mnt/nfs/admx/admx-hf_data/experimentData/$1
#echo $PWD

for f in *.psa
do
f=${f%.psa}
echo $f >> ~/analysis/admx_hf/analysis/p_spectra.txt
done

