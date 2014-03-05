#/bin/bash
#set -x

if [ $# != 3 ]
then
    echo "USAGE: $0 DATAFILE OUTDIR FORMAT"
    exit 1
fi

DATAFILE=$1
OUTDIR=$2
FORMAT=$3

for CONFIG in configs/*.twg
do
    FNAME=`basename $CONFIG`
    FNAME="${FNAME%.*}"
    OUTFILE="${OUTDIR}/$FNAME.$FORMAT"
    echo "Writing $OUTFILE"

    ./twyg.py -c $CONFIG $DATAFILE $OUTFILE
done

