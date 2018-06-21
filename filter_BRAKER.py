import re
import argparse


genes2evi = {}

## Because there are 4 input files and I'll never remember the order, I'm hard coding them

## Strategy:
## keep 

##----------------------------------------------------------
## Get BLAST  to EA
bfile = "../filter_by_EA_support/reciprocal_best_hits.txt"
with open(bfile,'r') as b_in:
	for line in b_in:
		fields = line.split('\t')
		match = fields[0]
		stripend = re.compile("(\w+)\.")
		stripped_match = re.search(stripend, match)
		genes2evi[stripped_match.group(1)] = 'EA'
b_in.close
		
##----------------------------------------------------------
## Get RNASeq file
rfile = "../filter_by_RNASeq/merged_counts.txt"
with open(rfile,'r') as r_in:
	# parse the rest
	for line in r_in:
		fields = line.split()
		#check if read count is over 100
		if int(fields[1]) > 99:
			match = fields[0]
			#print(line)
			# update evidence if it already exist, otherwise add it
			if match in genes2evi:
				genes2evi[match] = 'EA,RNA'
				#print("updating ", match)
			else:
				genes2evi[match] = 'RNA'
r_in.close

##----------------------------------------------------------
## lets print an update on how many genes we've got with evidence

print("Genes with evidence: "+ str(len(genes2evi.keys())))

ea = sum(1 for x in genes2evi.values() if x == 'EA')
print("Genes with EA evidence only: "+ str(ea))

rna = sum(1 for x in genes2evi.values() if x == 'RNA')
print("Genes with RNA evidence only: "+ str(rna))

both = sum(1 for x in genes2evi.values() if x == 'EA,RNA')
print("Genes with EA and RNA evidence: "+ str(both))

#for x in genes2evi:
	#print(x," ", genes2evi[x])



##----------------------------------------------------------
## Time to output our new gffs

gfile = "../../jbrowse_tracks/BRAKER_RNASeqandEA_augustus_060618.hints.gff"

## output files will have the same name as input with the addition of a suffix
gfile_out_evi = gfile + '.hasevidenceMANUAL'
gfile_out_noevi = gfile + '.noevidenceMANUAL'

f_out_E = open(gfile_out_evi, 'w')
f_out_NE = open(gfile_out_noevi, 'w')

# open gff file and use a regex to split the gene entries

with open(gfile,'r') as f_in:
	ftxt = f_in.read()
	myre = re.compile("# start gene")
	genelist = myre.split(ftxt)

	# The first element in the list is some preliminary comments about the gff file
	# lets save it and copy it to both output files
	header = genelist.pop(0)
	f_out_NE.write(header)
	f_out_E.write(header)

	# pull out gene name
	myre2 = re.compile("^ (\w+)")

	# print to the appropriate output file based on the evidence regex
	for gene in genelist:
		match = re.search(myre2, gene)
		gene_name = match.group(1)
		if gene_name in genes2evi:
			f_out_E.write("# start gene "+gene)
			#print("\n#########\nHAS EVIDENCE\n\n")
			#print(gene)
		else:
			f_out_NE.write("# start gene "+gene)
			#print("\n#########\nNO EVIDENCE\n\n")
			#print(gene)


f_in.close
