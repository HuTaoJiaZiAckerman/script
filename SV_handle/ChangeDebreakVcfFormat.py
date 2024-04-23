#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author @caominghao
# Description @ ChangeDebreakVcfFormat.py
# CreateTime @ 2023-09-03 16:38:07

# @Time: 2023/9/3 16:10
# @Author: caominghao
# @File: Debreak2Normal.py
# @Software: PyCharm

import logging, os, sys
import click, re
# 生成日志文件
logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
		format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

# 定义参考基因组
def LoadFasta(File):
	Dict = {}
	seq = ''
	for line in File:
		line = line.strip()
		if line[0] == '>':
			if len(seq) > 0:
				Dict[name] = seq
			name = line.split()[0][1:]
			seq = ''
		else: seq += line
	Dict[name] = seq
	return Dict


# 定义软件的参数
@click.command()
@click.option('-r','--ref',type=click.File('r'),help='input the reference fasta file',required=True)
@click.option('-v','--vcf',type=click.File('r'),help='input the debreak vcf file',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the changed format vcf file',required=True)

def main(ref,vcf,out):
	DelNum,InsNum = 1,1
	FaDict = LoadFasta(ref)
	for line in vcf:
		line = line.strip()
		if line.startswith('#'):
			out.write(f'{line}\n')
		elif 'STRANDBIAS' in line or 'SVTYPE=BND' in line:
			continue
		else:
			line = line.split('\t')
			Chrom,Start = line[0],line[1]
			End = re.findall(r'SVLEN=\w*',line[7])[0].split('=')[1]
			Type = re.findall(r'SVTYPE=\w*',line[7])[0].split('=')[1]
			GT = line[9].split(':')[0]
			if Type == 'DEL':
				if int(Start) + int(End) < 5000000:
					try:
						SVLEN = str(int(End))
						RefSeq = FaDict[Chrom][int(Start)-1:int(End) + int(Start)]
						#RefSeq = ''.join(os.popen(f"~/software/seqkit subseq {ref} --chr {Chrom} -r {Start}:{End} | grep -v '>'").readlines()) #该种方法太慢了
						AltSeq = RefSeq[0]
						out.write(f'{Chrom}\t{Start}\tDB.DEL.{DelNum}\t{RefSeq}\t{AltSeq}\t.\tPASS\tSVTYPE=DEL;SVLEN=-{SVLEN};END={int(Start) + int(End)}\tGT\t{GT}\n')
						DelNum += 1
					except:
						pass
			elif Type == 'INS':
				if len(line[4]) < 5000000:
					try:
						RefSeq = FaDict[Chrom][int(Start) - 1]
						#RefSeq = ''.join(os.popen(f"~/software/seqkit subseq {ref} --chr {Chrom} -r {Start}:{Start} | grep -v '>'").readlines())
						AltSeq = RefSeq + line[4]
						SVLEN = len(line[4])
						out.write(f'{Chrom}\t{Start}\tDB.INS.{InsNum}\t{RefSeq}\t{AltSeq}\t.\tPASS\tSVTYPE=INS;SVLEN={SVLEN};END={int(Start) + int(End)}\tGT\t{GT}\n')
						InsNum += 1
					except:
						pass
			else:
				pass

if __name__ == '__main__':
	main()



