cd /tmp-inputs/tmp && for f in *.pdb; do mv "$f" "protein_${f}"; done && cd /src
cd /tmp-inputs/tmp && for f in *.sdf *.mol2; do [ -f "$f" ] && mv "$f" "ligand_${f}"; done && cd /src
