# @Time: 2024/3/1 10:38
# @Author: caominghao
# @File: Survivor2Paragraph.py
# @Software: PyCharm

# 这个脚本是用来修改四种方法SRUVIVOR合并后的SV结果，用SURVIVOR合并之后的结果调整，FOTMAT由4列转为1列。
import logging, os, sys
import click, re


logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
		format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")


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

@click.command()
@click.option('-m','--survivor',type=click.File('r'),help='input the final survivor merged vcf file',required=True)
@click.option('-r','--ref',type=click.File('r'),help='input the reference fasta file',required=True)
@click.option('-s','--sample',type=str,help='input the sample name',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the VCF file',required=True)
def main(survivor,ref,sample,out):
	FaDict = LoadFasta(ref)
	DEL_Num,INS_Num = 1,1
	Complex_SV_List = []
	for line in survivor:
		line = line.strip()
		if line.startswith('##'):
			out.write(f'{line}\n')
		elif line.startswith('#CHROM'):
			line = line.split('\t')
			PreINFO = '\t'.join(line[:9])
			out.write(f'{PreINFO}\t{sample}\n')
		else:
			line = line.split('\t')
            INFO = line[7]
            SVLEN = abs(INFO.split(';')[2].split('=')[1])
			for SV_INFO in line[9:]:
				if SV_INFO.split(':')[-1] != 'NAN' and ',' not in SV_INFO.split(':')[-1] and SV_INFO.split(':')[-3] != 'NA':
					SV_TYPE,GT = SV_INFO.split(':')[-5],SV_INFO.split(':')[0]
					if SV_TYPE == "DEL":
						Chrom,Pos = SV_INFO.split(':')[-1].split('-')[0].split('_')[0],line[1]
						End = SV_INFO.split(':')[-1].split('-')[1].split('_')[1]
						if End == Pos:
							End = str(int(Pos) + int(len(REF)))
							REF = str(SV_INFO.split(':')[-3])
							ALT = str(SV_INFO.split(':')[-2])
						else:
							REF = str(SV_INFO.split(':')[-3])
							End = str(int(Pos) + int(int(SVLEN)))
						ALT = str(SV_INFO.split(':')[-2])
						ID = 'DEL.' + str(DEL_Num)
						out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=DEL;SVLEN=-{str(SVLEN)};END={End}\tGT\t{GT}\n')
						DEL_Num += 1
					else:
						Chrom,Pos = SV_INFO.split(':')[-1].split('-')[0].split('_')[0],line[1]
						End = SV_INFO.split(':')[-1].split('-')[1].split('_')[1]
						
					break
				else:
					Complex_SV_List.append(SV_INFO)
			if len(Complex_SV_List) == 10:
				for Complex_SV_INFO in Complex_SV_List:
					if Complex_SV_INFO.split(':')[-1] != 'NAN' and Complex_SV_INFO.split(':')[-3] != 'NA':
						#SV_TYPE = Complex_SV_INFO.split(':')[-4].split('.')[1]
						if len(Complex_SV_INFO.split(':')[-3]) > len(Complex_SV_INFO.split(':')[-2]):
							Chrom,Pos = Complex_SV_INFO.split(':')[-1].split(',')[0].split('-')[0].split('_')[0],Complex_SV_INFO.split(':')[-1].split(',')[0].split('-')[0].split('_')[1]
							End = Complex_SV_INFO.split(':')[-1].split(',')[0].split('-')[1].split('_')[1]
							SVLEN = str(int(End) - int(Pos))
							REF = FaDict[Chrom][int(Pos)-1:int(End)]
							ALT = REF[0]
							ID = 'DEL.' + str(DEL_Num)
							out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=DEL;SVLEN=-{str(SVLEN)};END={End}\tGT\t{GT}\n')
							DEL_Num += 1
						else:
							Chrom,Pos = Complex_SV_INFO.split(':')[-1].split(',')[0].split('-')[0].split('_')[0],Complex_SV_INFO.split(':')[-1].split(',')[0].split('-')[0].split('_')[1]
							REF,ALT = Complex_SV_INFO.split(':')[-3],Complex_SV_INFO.split(':')[-2]
							SVLEN,GT = str(len(ALT) -1),Complex_SV_INFO.split(':')[0]
							ID = 'INS.' + str(INS_Num)
							out.write(f'{Chrom}\t{Pos}\t{ID}\t{REF}\t{ALT}\t.\tPASS\tSVTYPE=INS;SVLEN={str(SVLEN)};END={Pos}\tGT\t{GT}\n')
							INS_Num += 1
						break
			Complex_SV_List = []

if __name__ == '__main__':
	main()

