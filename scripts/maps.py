#!/bin/python3

import requests
import json
from rdflib import Graph, SKOS, RDF


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

# This is what we want an example vocab redirect to RVA to look like
"""
# https://linked.data.gov.au/def/climate-glossary
RewriteRule ^/def/climate-glossary(|/.+)\.ttl$         https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.ttl?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteCond %{QUERY_STRING} ^_mediatype=text/turtle$ [OR]
RewriteCond %{QUERY_STRING} ^_format=text/turtle$ [OR]
RewriteCond %{HTTP:Accept} text/turtle [NC]
RewriteRule ^/def/climate-glossary($|/.*$)             https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.ttl?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteRule ^/def/climate-glossary(|/.+)\.rdf$         https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.rdf?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteCond %{QUERY_STRING} ^_mediatype=application/rdf\+xml$ [OR]
RewriteCond %{QUERY_STRING} ^_format=application/rdf\+xml$ [OR]
RewriteCond %{HTTP:Accept} application/rdf\+xml [NC]
RewriteRule ^/def/climate-glossary($|/.*$)             https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.rdf?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteRule ^/def/climate-glossary(|/.+)\.xml$         https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.xml?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteCond %{QUERY_STRING} ^_mediatype=application/xml$ [OR]
RewriteCond %{QUERY_STRING} ^_format=application/xml$ [OR]
RewriteCond %{HTTP:Accept} application/xml [NC]
RewriteRule ^/def/climate-glossary($|/.*$)             https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.xml?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
# Note, RVA JSON endpoint is _not_ JSON-LD, RVA _does not support_ accept:application/ld+json
RewriteRule ^/def/climate-glossary(|/.+)\.json$        https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.json?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteCond %{QUERY_STRING} ^_mediatype=application/json$ [OR]
RewriteCond %{QUERY_STRING} ^_format=application/json$ [OR]
RewriteCond %{HTTP:Accept} application/json [NC]
RewriteRule ^/def/climate-glossary($|/.*$)             https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.json?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteRule ^/def/climate-glossary(|/.+)\.text$        https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.text?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteRule ^/def/climate-glossary(|/.+)\.txt$         https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.text?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteCond %{QUERY_STRING} ^_mediatype=text/plain$ [OR]
RewriteCond %{QUERY_STRING} ^_format=text/plain$ [OR]
RewriteCond %{HTTP:Accept} text/plain [NC]
RewriteRule ^/def/climate-glossary($|/.*$)             https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.text?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteRule ^/def/climate-glossary(|/.+)\.html$        https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.html?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
RewriteCond %{QUERY_STRING} ^_mediatype=text/html$ [OR]
RewriteCond %{QUERY_STRING} ^_format=text/html$ [OR]
RewriteCond %{HTTP:Accept} text/html [NC]
RewriteRule ^/def/climate-glossary($|/.*$)             https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.html?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
# Catch all remaining matches as generalised resource
RewriteRule ^/def/climate-glossary($|/.*$)             https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource?uri=https://linked.data.gov.au/def/climate-glossary$1 [R=302,QSA,L]
"""

rewrite_turtle_template = """\
RewriteRule ^/def/{agldwg_def}(|/.+)\.ttl$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.ttl?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
RewriteCond %{{QUERY_STRING}} ^_mediatype=text/turtle$ [OR]
RewriteCond %{{QUERY_STRING}} ^_format=text/turtle$ [OR]
RewriteCond %{{HTTP:Accept}} text/turtle [NC]
RewriteRule ^/def/{agldwg_def}/?(|/.+)$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.ttl?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
"""
def make_turtle_rewrite(agldwg_def, rva_def, rva_version):
    return str.format(rewrite_turtle_template, RVA_LDAPI=RVA_LDAPI, agldwg_def=agldwg_def, rva_def=rva_def, rva_version=rva_version)

rewrite_rdfxml_template = """\
RewriteRule ^/def/{agldwg_def}(|/.+)\.rdf$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.rdf?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
RewriteCond %{{QUERY_STRING}} ^_mediatype=application/rdf\+xml$ [OR]
RewriteCond %{{QUERY_STRING}} ^_format=application/rdf\+xml$ [OR]
RewriteCond %{{HTTP:Accept}} application/rdf\+xml [NC]
RewriteRule ^/def/{agldwg_def}/?(|/.+)$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.rdf?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
"""
def make_rdfxml_rewrite(agldwg_def, rva_def, rva_version):
    return str.format(rewrite_rdfxml_template, RVA_LDAPI=RVA_LDAPI, agldwg_def=agldwg_def, rva_def=rva_def, rva_version=rva_version)

rewrite_xml_template = """\
RewriteRule ^/def/{agldwg_def}(|/.+)\.xml$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.xml?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
RewriteCond %{{QUERY_STRING}} ^_mediatype=application/xml$ [OR]
RewriteCond %{{QUERY_STRING}} ^_format=application/xml$ [OR]
RewriteCond %{{HTTP:Accept}} application/xml [NC]
RewriteRule ^/def/{agldwg_def}/?(|/.+)$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.xml?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
"""
def make_xml_rewrite(agldwg_def, rva_def, rva_version):
    return str.format(rewrite_xml_template, RVA_LDAPI=RVA_LDAPI, agldwg_def=agldwg_def, rva_def=rva_def, rva_version=rva_version)

rewrite_json_template = """\
RewriteRule ^/def/{agldwg_def}(|/.+)\.json$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.json?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
RewriteCond %{{QUERY_STRING}} ^_mediatype=application/json$ [OR]
RewriteCond %{{QUERY_STRING}} ^_format=application/json$ [OR]
RewriteCond %{{HTTP:Accept}} application/json [NC]
RewriteRule ^/def/{agldwg_def}/?(|/.+)$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.json?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
"""
def make_json_rewrite(agldwg_def, rva_def, rva_version):
    return str.format(rewrite_json_template, RVA_LDAPI=RVA_LDAPI, agldwg_def=agldwg_def, rva_def=rva_def, rva_version=rva_version)

rewrite_text_template = """\
RewriteRule ^/def/{agldwg_def}(|/.+)\.text$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.text?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
RewriteRule ^/def/{agldwg_def}(|/.+)\.txt$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.text?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
RewriteCond %{{QUERY_STRING}} ^_mediatype=text/plain$ [OR]
RewriteCond %{{QUERY_STRING}} ^_format=text/plain$ [OR]
RewriteCond %{{HTTP:Accept}} text/plain [NC]
RewriteRule ^/def/{agldwg_def}/?(|/.+)$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.text?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
"""
def make_text_rewrite(agldwg_def, rva_def, rva_version):
    return str.format(rewrite_text_template, RVA_LDAPI=RVA_LDAPI, agldwg_def=agldwg_def, rva_def=rva_def, rva_version=rva_version)

rewrite_html_template = """\
RewriteRule ^/def/{agldwg_def}(|/.+)\.html$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.html?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
RewriteCond %{{QUERY_STRING}} ^_mediatype=text/html$ [OR]
RewriteCond %{{QUERY_STRING}} ^_format=text/html$ [OR]
RewriteCond %{{HTTP:Accept}} text/html [NC]
RewriteRule ^/def/{agldwg_def}/?(|/.+)$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource.html?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
"""
def make_html_rewrite(agldwg_def, rva_def, rva_version):
    return str.format(rewrite_html_template, RVA_LDAPI=RVA_LDAPI, agldwg_def=agldwg_def, rva_def=rva_def, rva_version=rva_version)

catch_all_template = """\
# Catch all remaining {agldwg_def} matches as generalised RVA vocab LDAPI resource
RewriteRule ^/def/{agldwg_def}/?(|/.+)$\t\t{RVA_LDAPI}{rva_def}/{rva_version}/resource?uri=https://linked.data.gov.au/def/{agldwg_def}$1 [R=302,QSA,L]
"""

def make_catch_all(agldwg_def, rva_def, rva_version):
    return str.format(catch_all_template, RVA_LDAPI=RVA_LDAPI, agldwg_def=agldwg_def, rva_def=rva_def, rva_version=rva_version)


def make_neii_rewrite_conf():
    parts = []
    parts.append("# Automatically generated using the NEII vocabulary rescue scripts found here: https://github.com/dcceew-bdr/neii-vocabs/blob/main/scripts/maps.py\n")
    parts.append("# Note, RVA JSON endpoint is _not_ JSON-LD, RVA _does not support_ application/ld+json\n")
    for (agldwg_uri, (rva_def, rva_version)) in agldwg_pid_to_rva.items():
        parts.append(f"# {agldwg_uri}\n")
        agldwg_def = agldwg_uri.replace("https://linked.data.gov.au/def/", "")
        parts.append(make_turtle_rewrite(agldwg_def, rva_def, rva_version))
        parts.append(make_rdfxml_rewrite(agldwg_def, rva_def, rva_version))
        parts.append(make_xml_rewrite(agldwg_def, rva_def, rva_version))
        parts.append(make_json_rewrite(agldwg_def, rva_def, rva_version))
        parts.append(make_text_rewrite(agldwg_def, rva_def, rva_version))
        parts.append(make_html_rewrite(agldwg_def, rva_def, rva_version))
        parts.append(make_catch_all(agldwg_def, rva_def, rva_version))
        parts.append("\n")
    return "".join(parts)

with open("./neii.conf", "w") as f:
    f.write(make_neii_rewrite_conf())

session = requests.Session()

def get_a_vocab_entry(agldwg_uri, rva_def, rva_version):
    turtle_url = f"{RVA_LDAPI}{rva_def}/{rva_version}/resource.ttl?uri={agldwg_uri}"
    resp = session.get(turtle_url, headers={"Accept": "text/turtle"})
    g = Graph()
    g.parse(data=resp.text, format="text/turtle")
    concept_schemes = list(g.subjects(RDF.type, SKOS.ConceptScheme))
    top_concepts = list(g.objects(concept_schemes[0], SKOS.hasTopConcept))
    first_top_concept = sorted(top_concepts)[0]
    return str(first_top_concept)

# tests should look like this:
"""
{
  "https://linked.data.gov.au/def/climate-glossary": [
    {
      "label": "NEII vocabulary climate-glossary (no headers), no slash",
      "from": "https://linked.data.gov.au/def/climate-glossary",
      "to": "https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource?uri=https://linked.data.gov.au/def/climate-glossary",
      "headers": {}
    },
    {
      "label": "NEII vocabulary climate-glossary (no headers), remove final slash",
      "from": "https://linked.data.gov.au/def/climate-glossary/",
      "to": "https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource?uri=https://linked.data.gov.au/def/climate-glossary",
      "headers": {}
    },
    {
      "label": "NEII vocabulary climate-glossary (TTL ext)",
      "from": "https://linked.data.gov.au/def/climate-glossary.ttl",
      "to": "https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.ttl?uri=https://linked.data.gov.au/def/climate-glossary",
      "headers": {}
    },
    {
      "label": "NEII vocabulary climate-glossary entry (No headers, no ext)",
      "from": "https://linked.data.gov.au/def/climate-glossary/Anomaly",
      "to": "https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource?uri=https://linked.data.gov.au/def/climate-glossary/Anomaly",
      "headers": {}
    },
    {
      "label": "NEII vocabulary climate-glossary entry (TTL ext)",
      "from": "https://linked.data.gov.au/def/climate-glossary/Anomaly.ttl",
      "to": "https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.ttl?uri=https://linked.data.gov.au/def/climate-glossary/Anomaly",
      "headers": {}
    },
    {
      "label": "NEII vocabulary climate-glossary (TTL header), no slash",
      "from": "https://linked.data.gov.au/def/climate-glossary",
      "to": "https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.ttl?uri=https://linked.data.gov.au/def/climate-glossary",
      "headers": {
        "Accept": "text/turtle"
      }
    },
    {
      "label": "NEII vocabulary climate-glossary (TTL header), remove final slash",
      "from": "https://linked.data.gov.au/def/climate-glossary/",
      "to": "https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.ttl?uri=https://linked.data.gov.au/def/climate-glossary",
      "headers": {
        "Accept": "text/turtle"
      }
    },
    {
      "label": "NEII vocabulary climate-glossary entry (TTL header)",
      "from": "https://linked.data.gov.au/def/climate-glossary/Anomaly",
      "to": "https://vocabs.ardc.edu.au/repository/api/lda/neii/climate-glossary/version-2-0-agldwg-pid/resource.ttl?uri=https://linked.data.gov.au/def/climate-glossary/Anomaly",
      "headers": {
        "Accept": "text/turtle"
      }
    },
  ],
}
"""

TEST_EXT_KINDS = [
    ("Turtle", ".ttl", "text/turtle"),
    ("RDF", ".rdf", "application/rdf+xml"),
    ("XML", ".xml", "application/xml"),
    ("JSON", ".json", "application/json"),
    ("Plain Text", ".text", "text/plain"),
    ("HTML", ".html", "text/html"),
]

def make_vocab_tests(agldwg_uri, agldwg_def, rva_def, rva_version):
    test_list = []
    test_list.append({
        "label": f"NEII vocabulary {agldwg_def}, no headers, no ext, no slash",
        "from": agldwg_uri,
        "to": f"{RVA_LDAPI}{rva_def}/{rva_version}/resource?uri={agldwg_uri}",
        "headers": {}
        })
    test_list.append({
        "label": f"NEII vocabulary {agldwg_def}, no headers, no ext, remove final slash",
        "from": agldwg_uri+"/",
        "to": f"{RVA_LDAPI}{rva_def}/{rva_version}/resource?uri={agldwg_uri}",
        "headers": {}
        }) 
    for (kind_label, kind_ext, kind_header) in TEST_EXT_KINDS:
        test_list.append({
            "label": f"NEII vocabulary {agldwg_def}, no headers, {kind_label} ext",
            "from": agldwg_uri+kind_ext,
            "to": f"{RVA_LDAPI}{rva_def}/{rva_version}/resource{kind_ext}?uri={agldwg_uri}",
            "headers": {}
            })
        test_list.append({
            "label": f"NEII vocabulary {agldwg_def}, {kind_label} headers, no ext, no slash",
            "from": agldwg_uri,
            "to": f"{RVA_LDAPI}{rva_def}/{rva_version}/resource{kind_ext}?uri={agldwg_uri}",
            "headers": {"Accept": kind_header}
            })
        test_list.append({
            "label": f"NEII vocabulary {agldwg_def}, {kind_label} headers, no ext, remove final slash",
            "from": agldwg_uri+"/",
            "to": f"{RVA_LDAPI}{rva_def}/{rva_version}/resource{kind_ext}?uri={agldwg_uri}",
            "headers": {"Accept": kind_header}
            })
    return test_list

def make_vocab_entry_tests(entry_uri, agldwg_def, rva_def, rva_version):
    test_list = []
    test_list.append({
        "label": f"NEII vocabulary {agldwg_def} concept entry, no headers, no ext",
        "from": entry_uri,
        "to": f"{RVA_LDAPI}{rva_def}/{rva_version}/resource?uri={entry_uri}",
        "headers": {}
        })
    for (kind_label, kind_ext, kind_header) in TEST_EXT_KINDS:
        test_list.append({
            "label": f"NEII vocabulary {agldwg_def} concept entry, no headers, {kind_label} ext",
            "from": entry_uri+kind_ext,
            "to": f"{RVA_LDAPI}{rva_def}/{rva_version}/resource{kind_ext}?uri={entry_uri}",
            "headers": {}
            })
        test_list.append({
            "label": f"NEII vocabulary {agldwg_def} concept entry, {kind_label} headers, no ext",
            "from": entry_uri,
            "to": f"{RVA_LDAPI}{rva_def}/{rva_version}/resource{kind_ext}?uri={entry_uri}",
            "headers": {"Accept": kind_header}
            })
    return test_list

def make_neii_rewrite_tests():
    tests_dict = {}
    for (agldwg_uri, (rva_def, rva_version)) in agldwg_pid_to_rva.items():
        tests_dict[agldwg_uri] = tests_list = []
        agldwg_def = agldwg_uri.replace("https://linked.data.gov.au/def/", "")
        entry = get_a_vocab_entry(agldwg_uri, rva_def, rva_version)
        tests_list.extend(make_vocab_tests(agldwg_uri, agldwg_def, rva_def, rva_version))
        tests_list.extend(make_vocab_entry_tests(entry, agldwg_def, rva_def, rva_version))
    with open("neii.json", "w") as f:
        f.write(json.dumps(tests_dict, indent=4))

make_neii_rewrite_tests()