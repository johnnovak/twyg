#/bin/bash

if [ $# != 3 ]
then
    echo "USAGE: $0 DATAFILE OUTDIR FORMAT"
    exit 1
fi

DATAFILE=$1
OUTDIR=$2
FORMAT=$3

for CONFIG in twyg/configs/*.twg
do
    D=`basename $DATAFILE`
    D="${D%.*}"
    C=`basename $CONFIG`
    C="${C%.*}"
    OUTFILE="${OUTDIR}/${D}-${C}.${FORMAT}"
    echo "Writing $OUTFILE"

    twyg -c $CONFIG $DATAFILE $OUTFILE
done

