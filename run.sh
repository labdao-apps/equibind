#!/bin/bash

# this script wrapps the multiligand inference function to run more easily with bacalhau based IO
# preparing an input and output directory
mkdir -p tmp/dummy
mkdir out

# moving files to a temporary directory - required for bacalhaus IO which does not tolerate changes to the input directory
cp $1 tmp
cp $2 tmp

# renaming protein and ligand files
mv tmp/$1 tmp/dummy/protein_$1
mv tmp/$2 tmp/dummy/ligands_$2


# running the inference
echo running
python inference_VS-2.py -i tmp -o out --multi_ligand=True

echo run finished
mv out/dummy/* out
rm -r out/dummy
