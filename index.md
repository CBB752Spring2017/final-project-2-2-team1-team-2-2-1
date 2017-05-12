---
layout: page
title: CBB752 Spring 2017
tagline: Final Project
---

Project Title
------------------
CRISPR and personal genomics: The impact of SNPs on sgRNA sets and off target mutations

Table of Contents
-----------------------




**Contributors**

 -Writing: Acer Xu
 
 -Coding: Jiawei Wang
 
 -Pipeline: Jay Stanley

### Introduction:





### Writing:








### Coding:
Propose a tool that finds PAM sites in the human reference genome as well as Carl’s genome and compares the similarity of the two sets.
Here final2-2.a.py is the integrated version, and final2-2.2.1.py and final2-2.2.2.py are functionally separate versions.

#### Documentation:
##### final2-2.2.1.py
Version 2.1. Previous versions import the exported Spyder data format zids.spydata to include Zimmerome SNP information (to save time). Here it uses .pickle format data to allow automatic read-in.

##### final2-2.2.2.py
Version 2.2. This version generates a statistic sheet of number, and changed number and rate due to SNPs of two genomes.

##### final2-2.a.py
Version 4/a. This file basically integrates all the previous code together.

##### Usage
The most useful version is version 2.1, 2.2.

Command line example of final2-2.2.1.py:
> python final2-2.2.1.py -i <input folder> -m <mutation file> ###USAGE

> python final2-2.2.1.py -i Genome_GRCh37 -m Z.variantCall.SNP_filt.vcf #or zids.pickle if generated ###EXAMPLE

> ###generate mutation site figures and changed sites.

##### Requirement
Here I use Python 2.7. 
Files needed include Zimmerome SNP file (Z.variantCall.SNPs.vcf, from https://zimmerome.gersteinlab.org/2016/05/06/part01_gerstein/, but its comment was removed to generate a readable table), 
reference genome sequence (here I use GRCh37 downloaded from UCSC Genome Browser).

#### Results:
Results include 3 parts:
  1. Sample PAM sites distribution (plot out first 100 PAM sites of the two genomes against chromosome position): SamplePlot_chr*.png
  2. Histogram of PAM sites distribution on different parts of genomes, 100 bins: Histogram_chr*.png
  3. Scatterplot of PAM sites distribution on differetn parts of genomes, 10000 points: ScatterHist_chr*.png
  4. List of gained and lost PAM sites due to Zimmerome SNPs by each chromosome: Difference_*.txt
  5. Summary results of the effect of Zimmerome SNPs, including number of #PAM sites, #gained, %gained, #lost and %lost: ZSNPs_stats.txt

They are all in folder ./coding_results. It shows that PAM sites have an uneven distribution on each chromosome, which may reflect chromosomal structure and transcription activity. It also shows that the Zimmerome SNPs have a 0.2% to 0.3% change of PAM sites on each chromosome (both gained and lost sites, except chromsome Y). So if large scale CRISPR experiments are not carried out at the same time, the influence (chance of off-target due to SNPs) should be very low. But the lists of changed PAM sites due to SNPs are generated and stored as well for reference during sgRNA design to avoid possible off-target due to SNPs.


### Pipeline:

Guidescan was used to create a genomic guide RNA library for the Zimmerome and the reference genome.

1. Create a python virtualenv for guidescan.  Source this environment
2. Use pip to acquire all guidescan dependencies in this vitual env
3. Download and install guidescan. http://www.guidescan.com/
4. Download the reference genome guidescan database and BAM index from http://www.guidescan.com/
5. Acquire the human genome annotation http://www.ensembl.org/info/data/ftp/index.html
6. Clean the GFF labels by appending 'chr' using GFFUtil. http://gffutils.readthedocs.io/en/latest/index.html#
7. Convert the GFF to BED format using bedops gff2bed
8. Split the bed file into batches of 1000 using unix `split`
9. Acquire Carl's consensus sequence using `wget http://archive.gersteinlab.org/proj/zimmerome/Shapiro-UCSC/carl.psmc.fq.gz`
10. To extract the reference genome targets, perform the following tasks:
 - Build an output directory tree for the reference guidescan. In the split.bed directory,
 
 ```
 find * | xargs -n 1 -P 32 -I '{}' mkdir output/'{}'
 ```
 
 - Run a batch job of guidescan_guidequery on the split.bed files and the reference genome. 
 
 ```
 find * | xargs -n 1 -P32 -I '{}' guidescan_guidequery -b [PATH_TO_HG38_BAM] --target within --batch '{}' -o test/'{}'/ --output_format bed 
 ```
 
11. Build a guidescan database for the zimmerome using `guidescan_processer -f carl.fasta -t 16 -d 1`
Repeat step 10 for the the Carl BAM that results.
12. Concatenate output files
13. Parse concatenated output files for downstream statistics. `cat *.bed > output.bed`

#### Documentation:

Pybedtools was used to import and manage guidescanned .bed files for comparison.
Matplotlib and numpy were used to perform plotting, binning, and statistics.
#### Results:

The 50mb guide RNA coverage for both genomes is plotted below.

![image](https://raw.githubusercontent.com/CBB752Spring2017/final-project-2-2-team1-team-2-2-1/master/chr1_zimmervshg38.png)

The mean coverage per base for Carl's genome was slightly higher than hg38: 6.7% to 6.0%, respectively.

An intersection between the two sets was performed to identify the average overlap per 50mb of the two sets.


Kullback-leibler distance was also computed, for the coverage maps, however this statistic was not useful due to its trivial result (infinite relative entropy, implying that the coverage maps do not contain any information about each other).


#### Conclusions:

Basic descriptive statistics revealed that Carl's guide RNA library is not much different in coverage than the guide RNA library for hg38.  Early results suggest that the personal genome is slightly more enriched in guides than the draft.


The intersection map exhibits a steep falloff between the first 50mb to the rest of the chromosome.  We hypothesize this trend is linked to conserved structural regions at the end of the chromosome.

The 0.7% difference in coverage between the Zimmerome and the reference genome is intriguing.  Future analysis should be performed to examine specific areas of enrichment in the light of annotations (eg exon versus intron coverage).  However, these are not expected to differ significantly between the two sets, given that the distribution of NGGs is probabilistic.


Finally, new software must be developed for the generation and comparison of large, whole genome guideRNA libraries.

 
 
