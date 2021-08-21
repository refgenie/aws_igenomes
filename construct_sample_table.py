#!/usr/bin/env python3

"""
This script is used to generate a table of assets to build, recipe input files and genome descriptions based on this file: 
https://raw.githubusercontent.com/ewels/AWS-iGenomes/master/ngi-igenomes_file_manifest.txt
"""

from rich.progress import track

assets = {
    "bismark_bt1_index": {},
    "bismark_bt2_index": {},
    "blacklist": {},
    "bowtie2_index": {},
    "bwa_index": {},
    "cellranger_reference": {},
    "dbnsfp": {},
    "dbsnp": {},
    "ensembl_gtf": {},
    "ensembl_rb": {},
    "epilog_index": {},
    "fasta": {
        "fasta": "{bucket}/{org}/{src}/{build}/Sequence/WholeGenomeFasta/genome.fa"
    },
    "fasta_txome": {},
    "feat_annotation": {},
    "gtf": {"gtf": "{bucket}/{org}/{src}/{build}/Annotation/Genes/genes.gtf"},
    "kallisto_index": {},
    "refgene_anno": {},
    "salmon_index": {},
    "salmon_partial_sa_index": {},
    "salmon_sa_index": {},
    "star_index": {},
    "suffixerator_index": {},
    "tallymer_index": {},
    "tgMap": {},
    "bowtie2_index_extra": {},
}

bucket = "s3://ngi-igenomes/igenomes"

desc_templ = "The {org} ({build}) reference sequence from {src}"

# read txt file
with open("ngi-igenomes_file_manifest.txt", "r") as in_file:
    txt_lines = in_file.readlines()

build_prev = None
org_prev = None
src_prev = None
# open csv file
with open("asset_pep/assets_auto.csv", "w") as out_file, open(
    "asset_pep/recipe_inputs_auto.csv", "w"
) as out_file2, open("asset_pep/genome_descriptions_auto.csv", "w") as out_file3:
    out_file.write("genome,asset\n")
    out_file2.write("sample_name,input_id,input_value,input_type,md5\n")
    out_file3.write("sample_name,genome_description\n")
    for line in track(txt_lines, "Processing genomes"):
        l = line.split("/")
        org = l[4]
        src = l[5]
        build = l[6]
        if src == src_prev and org == org_prev and build == build_prev:
            continue
        for asset, inputs in assets.items():
            # creates lines like this: organism-source-build,asset
            genome = "-".join(l[4:7]).lower()
            out_file.write(f"{genome},{asset}\n")
            if inputs:
                for input_key, input_templ in inputs.items():
                    out_file2.write(
                        f"{genome},{input_key},{input_templ.format(bucket=bucket, org=org, src=src, build=build)},\n"
                    )
            if asset == "fasta":
                out_file3.write(
                    f"{genome}-{asset},{desc_templ.format(org=org.replace('_', ' ').title(), build=build, src=src)}\n"
                )
        build_prev = build
        org_prev = org
        src_prev = src

# TODO: manually curate the output file. Not all assets can be built for each genome.
