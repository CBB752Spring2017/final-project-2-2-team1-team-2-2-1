---
layout: page
title: CBB752 Spring 2017
tagline: Final Project
---

Project Title
------------------


Table of Contents
-----------------------




**Contributors**
 -Writing:
 -Coding: Jiawei Wang
 -Pipeline:

### Introduction:





### Writing:








### Coding:
Propose a tool that finds PAM sites in the human reference genome as well as Carl’s genome and compares the similarity of the two sets.
Here final2-2.a.py is the integrated version, and final2-2.2.1.py and final2-2.2.2.py are functionally separate versions.

#### Documentation:
##### final2-2.0.py
Version 0. A general framework for the work. Find the NGG sites with or without Zimmerome SNPs on reference genome. Give three plots:
  1. Sample PAM sites distribution (plot out first 100 PAM sites of the two genomes against chromosome position)
  2. Histogram of PAM sites distribution on different parts of genomes, 100 bins
  3. Scatterplot of PAM sites distribution on differetn parts of genomes, 10000 points

##### final2-2.1.0.py
Version 1.0. Besides generating plots, it generates the changed PAM sites as well. An alignment check procedure is added, too.

##### final2-2.1.py
Version 1.2. The changed PAM sites are written in a more readable and standard format.

##### final2-2.2.py
Version 2.0. Version 2.x is for command line running (others may be tuned in Spyder). So this is an integrated version to run through all chromosomes based on version 1.2.

##### final2-2.2.1.py
Version 2.1. Previous versions import the exported Spyder data format zids.spydata to include Zimmerome SNP information (to save time). Here it uses .pickle format data to allow automatic read-in.

##### final2-2.2.2.py
Version 2.2. This version generates a statistic sheet of number, and changed number and rate due to SNPs of two genomes.

##### final2-2.3.py
Version 3.2. Basically the same with version 2.2, but run on different platforms.

##### final2-2.a.py
Version 4/a. This file basically integrates all the previous code together.

##### Usage
The most useful version is version 2.1, 2.2.

Command line example of final2-2.2.1.py:
> python final2-2.2.1.py -i <input folder> -m <mutation file> ###USAGE

> python final2-2.2.1.py -i Genome_GRCh37 -m zids.pickle ###EXAMPLE

> ###generate mutation site figures and changed sites.

##### Requirement
Here I use Python 2.7. 
Files needed include Zimmerome SNP file (Z.variantCall.SNPs.vcf, but its comment was removed to generate a readable table), 
reference genome sequence (here I use GRCh37 downloaded).

#### Results:
Results include 3 parts:
  1. Sample PAM sites distribution (plot out first 100 PAM sites of the two genomes against chromosome position): SamplePlot_chr*.png
  2. Histogram of PAM sites distribution on different parts of genomes, 100 bins: Histogram_chr*.png
  3. Scatterplot of PAM sites distribution on differetn parts of genomes, 10000 points: ScatterHist_chr*.png
  4. List of gained and lost PAM sites due to Zimmerome SNPs by each chromosome: Difference_*.txt
  5. Summary results of the effect of Zimmerome SNPs, including number of #PAM sites, #gained, %gained, #lost and %lost: ZSNPs_stats.txt

They are in folder coding_results.


### Pipeline:


#### Documentation:


#### Results:









#### Conclusions:








#### References:

 References can be included here or at the end of each relevant section.
 
 
