# green_ash_genome

Scripts developed in the collaborative project to annotate a reference genome for green ash. These scripts were used to filter BRAKER results.


Step 1. Run BRAKER as directed by the manual and get the final augustus.hints.gff file.

Step 2. Filtering by BLAST. We have a set of European ash gene models, and any gene models similar to this are likely to be true genes. Generate a set of reciprocal best blastp hit pairs between the BRAKER gene models (augustus.hints.aa) and the European ash protein sequences. Place in a file named "reciprocal_best_hits.txt", with the format of the augustus gene model first on each line, followed by a tab and the european ash gene name.

Step 3. Filter RNASeq. We have a set of many RNASeq libraries, and any genes with significant numbers of RNASeq reads are likely to be true genes. Use htseq to generate a count of reads per augustus gene model, in a final file named merged_counts.txt.

Step 4. Filter by repeats. Some gene models still largely overlap annotated repeats, and need to be removed from the list of high quality gene models. Use bedtools and the repeat annotation to generate a list of gene models that significantly overlap with repeats.

Step 5. The filter_BRAKER.py script will accept all gene models with a European ash reciprocal best hit. It will also accept any gene model with at least 100 mapped RNASeq reads, but only if it does not significantly overlap a repetitive region. The filenames are hardcoded in the script and need to be changed there. The script will two new gff files: one with the extension "hasEvidence" and one with the extension "noEvidence"
