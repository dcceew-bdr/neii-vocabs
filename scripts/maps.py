#!/bin/python3
RVA_LDAPI="https://vocabs.ardc.edu.au/repository/api/lda/"
RVA_resource_suffix = "/resource?uri="
agldwg_pid_to_rva = {
    "https://linked.data.gov.au/def/climate-glossary": ("neii/climate-glossary","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/australian-hydrological-geospatial-fabric": ("neii/australian-hydrological-geospatial-fabric-geofabri","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/australian-landscape-water-balance": ("neii/australian-landscape-water-balance","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/australian-network-of-hydrologic-reference-stations-glossary": ("neii/australian-network-of-hydrologic-reference-station","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/climate-stats-defs-non-rain": ("neii/climate-statistics-definitions-for-daily-elements","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/cloud-cover-observation-measurements": ("neii/cloud-cover-observation-measurements","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/Bioregional-Assessment-Programme-Glossary": ("neii/bioregional-assessment-programme-glossary","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/definitions-for-9am-and-3pm-climate-statistics": ("neii/definitions-for-9am-and-3pm-climate-statistics","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/drought-rainfall-definitions": ("neii/drought-rainfall-definitions","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/neii-data-availability": ("neii/neii-data-availability","version-3-0-agldwg-pid"),
    "https://linked.data.gov.au/def/neii-licencing": ("neii/neii-licencing","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/neii-observation-method": ("neii/neii-observation-method","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/neii-observed-property": ("neii/neii-observed-property","version-3-0-agldwg-pid"),
    "https://linked.data.gov.au/def/neii-sampling-regime": ("neii/neii-sampling-regime","version-3-0-agldwg-pid"),
    "https://linked.data.gov.au/def/neii-site-status": ("neii/neii-site-status","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/neii-srs-name": ("neii/neii-srs-name","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/rainfall-definitions": ("neii/rainfall-definitions","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/reeftemp-next-generation-glossary": ("neii/reeftemp-next-generation-glossary","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/solar-radiation-definitions": ("neii/solar-radiation-definitions","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/temperature-definitions": ("neii/temperature-definitions","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/tidal-terminology": ("neii/tidal-terminology","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/tsunami-glossary-of-terms": ("neii/tsunami-glossary-of-terms","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/water-market-reports": ("neii/water-market-reports-glossary","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/water-regulations-2008-water-information-terms": ("neii/water-regulations-2008-water-information-terms","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/wave-sea-and-swell-terms": ("neii/wave-sea-and-swell-terms","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/australian-groundwater-insight": ("bom/australian-groundwater-insight","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/australian-water-assessment-landscape-model": ("bom/australian-water-assessment-landscape-model","version-2-0-agldwg-pid"),
    "https://linked.data.gov.au/def/groundwater-dependent-ecosystems-atlas": ("bom/groundwater-dependent-ecosystems-atlas","version-3-0-agldwg-pid"),
    "https://linked.data.gov.au/def/national-groundwater-information-system": ("bom/national-groundwater-information-system","version-2-0-agldwg-pid")
}

def make_top_concept_uri(parts):
    return RVA_LDAPI+parts[0]+"/"+parts[1]+"/concept"

top_concept_uris = {ldgau: make_top_concept_uri(parts) for (ldgau, parts) in agldwg_pid_to_rva.items()}
print(top_concept_uris)