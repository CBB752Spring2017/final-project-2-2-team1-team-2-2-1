#!/usr/bin/python

__author__ = "Jiawei Wang"
__copyright__ = "Copyright 2017"
__credits__ = ["Jiawei Wang"]
__license__ = "GPL"
__version__ = "1.2.2"
__maintainer__ = "Jiawei Wang"
__email__ = "jiawei.wang@yale.edu"

### Usage:      python final2-2.2.2.py -i <input folder> -m <mutation file>
### Example:    python final2-2.2.2.py -i Genome_GRCh37 -m zids.pickle
### Note:       Statistics of chromosome-wise effect of SNPs on NGG sites

import argparse
import numpy as np
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
import pandas as pd
import os
import pickle
#from spyderlib.utils.iofuncs import load_dictionary

# os.chdir('C:/Users/wangj/Documents/Biology/Yale-CSC/Studies/CBB752 Biomedical Data Analysis $ Mining & Modeling/FinalProjects/Project2.2')
### This is one way to read in arguments in Python. We need to read input folder and mutation file.
parser = argparse.ArgumentParser(description='CRISPR sites recognition')
parser.add_argument('-i', '--ifolder', help='input folder', required=True)
parser.add_argument('-m', '--mutfile', help='mutation file', required=True)
args = parser.parse_args()

def runCSR(ifolder, mutfile):
    # os.chdir(ifolder)
    # zids = getZmut(mutfile)

    ## Here Zimmerome SNP information is previously generated and stored in zids.pickle
    with open(mutfile, 'rb') as handle:
        zids = pickle.load(handle)
    savestat = 'ZSNPS_stats.txt' ## save the statistics to ZSNPS_stats.txt
    with open (savestat, 'w') as fs:
        fs.write('\t'.join(['chr','reference','zimmerome','gained','%gained','lost','%lost'])+'\n')
        paths = os.listdir(ifolder)
        for chrom in ['Y','X']:
            path = [p for p in paths if 'chr'+str(chrom)+'.fa' in p][0]
            path = os.path.join(ifolder, path)
            with open(path, 'r') as fi:
                seqs = fi.readlines()
            seqs = [i.strip() for i in seqs]
            seq = ''.join(seqs[1:]).upper() ##concatenate the segmented sequences together
            pos = findPos(seq, 'GG') ## find the 'NGG' or literally 'GG' sites

            ### swtiched to Zimmerome
            zchrom = zids[chrom]
            zeq = includeMut(seq, zchrom) ##includeMut generates the sequences with SNPs
            # if zeq:
            zos = findPos(zeq, 'GG')
            ## first: example Manhatan plot of first 100 nucleotides
            # plt.ioff()
        #     f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        #     pos_sel = pos[0:100]
        #     ax1.scatter(pos_sel, np.ones(len(pos_sel)))
        #     ax1.set_xlabel('Position on chr '+str(chrom))
        # #    ax1.set_ylabel('if there is \'NGG\'')
        #     ax1.set_title('Chr '+str(chrom)+'reference')
        #     zos_sel = zos[0:100]
        #     ax2.scatter(zos_sel, np.ones(len(zos_sel)))
        #     ax2.set_xlabel('Position on chr '+str(chrom))
        #     ax2.set_ylabel('if there is \'NGG\'')
        #     ax2.set_title('Chr '+str(chrom)+', Zimmerome')
        #     plt.savefig('SamplePlot_chr'+str(chrom)+'.png')
        #     # plt.close(f)
        #
        #     # second: histogram
        #     f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        #     ax1.hist(pos, bins=100, normed=True)
        #     ax1.set_xlabel('Position on chr '+str(chrom))
        # #    plt.ylabel('Frequency of \'NGG\'s')
        #     ax1.set_title('Chr '+str(chrom)+', reference')
        #     ax2.hist(zos, bins=100, normed=True)
        #     ax2.set_xlabel('Position on chr '+str(chrom))
        #     ax2.set_ylabel('Frequency of \'NGG\'s')
        #     ax2.set_title('Chr '+str(chrom)+', Zimmerome')
        #     plt.savefig('Histogram_chr'+str(chrom)+'.png')
        #     # plt.close(f)
        
        #     ## third: scatterplot of histogram of NGG site rates on different positions
        #     n1,bins1,patches1 = plt.hist(pos, bins=10000, normed=True)
        #     n2,bins2,patches2 = plt.hist(zos, bins=10000, normed=True)
        #     f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        #     bins_mean1 = [0.5 * (bins1[i] + bins1[i+1]) for i in range(len(n1))]
        #     ax1.scatter(bins_mean1, n1, s=1)
        #     ax1.set_ylim((0, max(n1)*1.25))
        #     ax1.set_xlabel('Position on chr '+str(chrom))
        #     ax1.set_title('Chr '+str(chrom)+', Zimmerome')
        #     bins_mean2 = [0.5 * (bins2[i] + bins2[i+1]) for i in range(len(n2))]
        #     ax2.scatter(bins_mean2, n2, s=1)
        # #    ax2.set_ylim((0, max(n1)*1.25))
        #     ax2.set_xlabel('Position on chr '+str(chrom))
        #     ax2.set_ylabel('Frequency of \'NGG\'s')
        #     ax2.set_title('Chr '+str(chrom)+', Zimmerome')
        #     plt.savefig('ScatterHist_chr'+str(chrom)+'.png')
        #     # plt.close(f)

            ### summary statistics for Zimmerome SNPs on NGG
            difz = sorted(list(set(zos)-set(pos))) ##gained 'NGG' sites
            difp = sorted(list(set(pos)-set(zos))) ##lost 'NGG' sites
            gained = float(len(difz))/len(pos) ##percentage of gained sites compared to original
            lost = float(len(difp))/len(pos) ##percentage of lost sites compated to original
            fs.write('\t'.join([str(chrom),str(len(pos)),str(len(zos)),str(len(difz)),\
                str(gained),str(len(difp)),str(lost)])+'\n')
            # with open('Difference_chr'+str(chrom)+'.txt','w') as f:
            #     f.write('chrom\tpos\tchange\n')
            #     for iz in range(len(difz)):
            #         f.write('\t'.join([str(chrom),str(difz[iz]),'gained'])+'\n')
            #     for ip in range(len(difp)):
            #         f.write('\t'.join([str(chrom),str(difp[ip]),'lost'])+'\n')

def includeMut(seq, zchrom):
    keys = sorted(zchrom.keys())
    zeq = list(seq)
    match = []
    kk = [seq[keys[i]-1]==zchrom[keys[i]][0] for i in range(100)]
    if sum(kk)==100:
        match.append(1)
    else:
        match.append(0)
    if sum(match):
        for key in keys:
            zeq[key-1] = zchrom[key][1]
        zeq = ''.join(zeq)
    else:
        zeq = 0
    return(zeq)

def findPos(seq, char):
    n = len(char)
    pos = []
    for i in range(len(seq)):
        if seq[i:(i+n)] == char:
            pos.append(i)
    return(pos)

# def getZmut(mutfile):
#     zmut = pd.read_table(mutfile)
#     zmut = zmut[['#CHROM','POS','REF','ALT']]
#     zx = zmut.index
#     zids = dict()
#     for z in zx:
#         chrom = zmut.loc[z,'#CHROM']
#         if chrom in range(1,23) or ['X','Y']:
#             pos = zmut.loc[z,'POS']
#             ref = zmut.loc[z,'REF']
#             alt = zmut.loc[z,'ALT']
#             if chrom not in zids.keys():
#                 zids[chrom] = dict()
#             if pos not in zids[chrom].keys():
#                 zids[chrom][pos] = [[ref,alt]]
#             else:
#                 zids[chrom][pos].append([ref,alt])
#     return(zids)

runCSR(args.ifolder, args.mutfile)
