from rdflib import Graph
from rdflib.namespace import RDF, SKOS
from pathlib import Path


def update_format():
    for f in Path(Path(__file__).parent.parent / "vocabs").glob("*.ttl"):
        print(f"parsing {f}")
        g = Graph().parse(f)
        print("reformatting")
        g.serialize(f, format="longturtle")


def cs_iri():
    for f in Path(Path(__file__).parent.parent / "vocabs").glob("*.ttl"):
        g = Graph().parse(f)
        cs_iri = None
        for cs in g.subjects(RDF.type, SKOS.ConceptScheme):
            # print(cs)
            cs_iri = str(cs)
            print(f'{f.name:>70} {str(cs).split("/")[-1].lower()}')
        data = f.read_text().replace(cs_iri, "https://linked.data.gov.au/def/" + cs_iri.split("/")[-1].lower())
        f.write_text()


if __name__ == "__main__":
    cs_iri()
    # update_format()
