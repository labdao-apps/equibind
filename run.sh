#!/bin/bash

# this script wrapps the multiligand inference function to run more easily with bacalhau based IO
# preparing an input and output directory
rm -r out
mkdir -p in/dummy
mkdir -p out

# moving protein and ligands into the input directory
mv in/$1 in/dummy/protein_$1
mv in/$2 in/dummy/ligands_$2

echo running
python inference_VS-2.py -i in -o out --multi_ligand=True

echo run finished
mv out/dummy/* out
rm -r out/dummy
