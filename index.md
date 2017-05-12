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
* [Introduction](#introduction)
* [Writing](#writing)
* [Coding](#coding)
* [Pipeline](#pipeline)

**Contributors**

 -Writing: Acer Xu  
 -Coding: Jiawei Wang  
 -Pipeline: Jay Stanley

### Introduction:
How might SNPs in Carl’s genome impact the use of CRISPR as a treatment?  
How to find PAM sites in the human reference genome as well as Carl’s genome and what are their similarities?  
How to calculate the sgRNA libraries for the reference genome and Carl’s genome and different are these two sets?  
This project answers the three basic questions above and more.


### Writing:

Cas9 activity depends on both sgRNA sequence and experimental conditions. While obviously conditions inside the human body are difficult to control, knowledge of sgRNA sequence will greatly impact the effect of CRISPR/Cas9 efficiency. The many SNPs in Carl’s genome may lead to a variety of different off-target effects, mostly negative, which can be alleviated via well thought out application of CRISPR guide RNA selection rules, such as Rule Set 1 and Rule Set 2 as referenced in Doench et. al., as well as well established predictive algorithms to find off-target effects in silico.

Overall, stochastic introduction of SNPs will generate novel NGG sites relative to any guide genome, leading to poor effects from any “generalized” CRISPR therapeutic strategies. Obviously, any CRISPR therapeutics will therefore require an initial genome sequencing to ensure that a full knowledge of potential S. pyogenes CRISPR sites is known. Additionally, any SNPs in guide sequence areas would lead to lower Cas9 cleavage rates at those loci. Base-pair mismatches will lead to decreased affinity in on-target sites, but may also lead to increased affinity in off-target sites. Using techniques such as tru-gRNA (truncated guide RNA) or a gRNA extension could also lead to more specific cleavage, but this again would be affected by SNP changes. Overall, the best way to avoid SNPs causing both undesired off-target effects or decreased therapeutic efficiency is probably through thorough sequencing and screening of the patient-genome prior to construction of CRISPR gRNA sequences. 




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

The corresponding guide libraries for chromosome 1 are included in this repository as `hg38_chr1.bed` and `zimmer_chr1_guides_cleaned.bed`.  The Zimmerome contains 16731494 guides on chromosome 1.  Hg38 contains 14932113 guides on chromosome 1.

Intersecting these libraries revealed 4626338 unique guides for the zimmerome and 3414224 unique guides in hg38.
These intersections are included in this repository as `chr1_unique_zimmer.bed` and `chr1_unique_hg38.bed`.


The 50mb guide RNA coverage for both genomes is plotted below.

![image](https://raw.githubusercontent.com/CBB752Spring2017/final-project-2-2-team1-team-2-2-1/master/chr1_zimmervshg38.png)

The mean coverage per base for Carl's genome was slightly higher than hg38: 6.7% to 6.0%, respectively.

Ln-fold change was calculated for coverage between the Zimmerome and hg38.
![image](https://raw.githubusercontent.com/CBB752Spring2017/final-project-2-2-team1-team-2-2-1/master/coverage_change.png)

Unique guides per 50mb was calculated.

![image](https://github.com/CBB752Spring2017/final-project-2-2-team1-team-2-2-1/blob/master/uniques.png?raw=true)

Kullback-leibler distance was also computed, for the coverage maps, however this statistic was not useful due to its trivial result (infinite relative entropy, implying that the coverage maps do not contain any information about each other).


#### Conclusions:

Basic descriptive statistics revealed that Carl's guide RNA library is not much different in coverage than the guide RNA library for hg38.  Early results suggest that the personal genome is slightly more enriched in guides than the draft.

The 0.7% difference in coverage between the Zimmerome and the reference genome is intriguing.  Future analysis should be performed to examine specific areas of enrichment in the light of annotations (eg exon versus intron coverage).  However, these are not expected to differ significantly between the two sets, given that the distribution of NGGs is probabilistic.

The fold change plot reveals a large spike in coverage of the zimmerome towards the centromere, which is not present in the draft genome.  However, in general, the zimmerome is about as covered as the hg38 genome.



Finally, new software must be developed for the generation and comparison of large, whole genome guideRNA libraries.

 
 
