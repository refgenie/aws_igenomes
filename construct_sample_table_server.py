#!/usr/bin/env python3

"""
This script is used to generate a table of assets to archive based on the populated refgenie config
"""

from refgenconf import RefGenConf, select_genome_config
from rich.progress import track

rgc = RefGenConf(select_genome_config())

with open("asset_pep/assets_auto_server.csv", "w") as out_file:
    out_file.write("genome,asset\n")
    genomes = list(rgc.genomes)
    for genome_id in track(genomes, "Processing genomes"):
        assets_by_genome = rgc.list(genome=genome_id)
        alias = rgc.get_genome_alias(digest=genome_id)
        assert list(assets_by_genome.keys())[0] == alias
        for asset_id in list(assets_by_genome.values())[0]:
            out_file.write(f"{alias},{asset_id}\n")
