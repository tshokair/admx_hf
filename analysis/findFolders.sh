#!/bin/bash

# findFolders.sh
# Lists all available folders in a text file to be read in python
# Last updated 03/02/16

rm dates_avail.txt
cd /mnt/nfs/admx/admx-hf_data/experimentData/
#echo $PWD

#echo */ >> ~/analysis/admx_hf/analysis/dates_avail.txt
for d in */;
do
echo $d >> ~/analysis/admx_hf/analysis/dates_avail.txt
done

sed -i 's/.$//' ~/analysis/admx_hf/analysis/dates_avail.txt
