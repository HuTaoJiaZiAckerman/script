#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author @caominghao
# Description @ bimConvert.py
# CreateTime @ 2022-12-11 21:39:53

import click

def stat(infile,outfile):
    with open(infile) as f1:
        with open(outfile, 'w') as f2:
            for line in f1:
                line1=line.strip().split()
                line1[0]=line1[0].replace('chr','')
                line1[0]=line1[0].replace('A','')
                line1[0]=line1[0].replace('B','')
                line1[0]=line1[0].replace('D','')
                f2.write(line1[0] + '\t' + line1[0] + ':' + line1[3] + '\t' + line1[2] + '\t' + line1[3] + '\t' + line1[4] + '\t' + line1[5] + '\n')
@click.command()
@click.argument("infile")
@click.argument("outfile")

def main(infile, outfile):
    stat(infile, outfile)
if __name__ == "__main__":
    main()
