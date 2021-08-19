FROM databio/refgenieserver:staging

COPY config/refgenie_config_archive.yaml /genome_config.yaml

ENTRYPOINT ["refgenieserver", "serve", "-c", "/genome_config.yaml"]
