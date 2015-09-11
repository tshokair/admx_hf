#!/bin/sh

# sendtotext.sh
#
#
# Created by Tim Shokair on 3/22/11.
# Copyright 2011 University of Pennsylvania. All rights reserved.

#FILES =/bkupData*
#rm p_spectra.txt
cd /admx/admx-hf_data/testStandData/2015/07/31/
for f in *.psa
do
f=${f%.psa}
echo $f >>../p_spectra.txt

done