#!/usr/bin/env python
# Usage: drevcomp.py seq1.fa seq2.fa ... seqN.fa
# create by Jingqi
# It takes >=1 fasta files of >=1 fasta entries, concatenates the sequence lines under a specific head and does reverse/complement on the sequence. 
# It outputs the r/c sequences in a fasta file with the suffix .rcfa under the same directory. 
# The input file must be in fasta format.

import sys
import os

# The Nucleotide complementary pair
complement_Nt={"A":"T", "T":"A", "C":"G", "G":"C", "U":"A", "N":"N"}

# The function to tailor the fasta file
def fasta_dict(input_file):
    """fasta_dict takes single fasta file and joins the sequence lines under a specific head; outputs a dictionary."""
    fasta_in = open(input_file, 'r').read().strip().split('\n')
    single_lined_fasta_dict = {}
    for line in fasta_in: 
        # Avoid the empty line
        if len(line) > 0: 
            # fasta head
            if line[0] == '>':
                fasta_head = line
                single_lined_fasta_dict[fasta_head] = ''
            else: 
                # join the sequences in separate rows, have them in upper case.
                single_lined_fasta_dict[fasta_head] += line.upper()
    return single_lined_fasta_dict

# The function doing reverse/complement
def revcomp_dict(head, seq): 
    """revcomp_dict takes a single fasta (one head + one seq) and does reverse/complement; outputs a dictionary of single item."""
    revcomp_dict = {}
    # rename the fasta header for the r/c fasta
    head_rc = head[0] + "RC_" + head[1:]
    # reverse the sequence and fetch the complementary Nt
    seq_rc = "".join([complement_Nt[seq[-i]] for i in range(1,len(seq)+1)])
    # make a dictionary
    revcomp_dict[head_rc] = seq_rc

    return revcomp_dict

# Loop through input
files = sys.argv[1:]
for afile in files: 
    # Reverse/complement the input file
    fasta_input = fasta_dict(afile)
    fasta_output = {}
    for head,seq in fasta_input.items(): 
        fasta_output.update(revcomp_dict(head,seq))

    # Write the output
    file_name = afile.split(".")[0] + ".rcfa"
    file_body = ""
    for head,seq in fasta_output.items():
        file_body += "{}\n{}\n".format(head,seq)
    with open(file_name,'w') as f:
        f.write(file_body)

# END
