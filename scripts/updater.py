from rdflib import Graph, Namespace, Literal
from rdflib.namespace import DCTERMS, RDF, SKOS
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
        # cs_iri = g.value(predicate=RDF.type, object=SKOS.ConceptScheme)
        # # g.bind("", Namespace(str(cs_iri) + "/"))
        # g.bind("cs", cs_iri)
        # desc = g.value(subject=cs_iri, predicate=DCTERMS.description)
        # g.remove((cs_iri, DCTERMS.description, desc))
        # g.add((cs_iri, SKOS.definition, desc))

        # for c in g.subjects(RDF.type, SKOS.Concept):
        #     g.add((c, SKOS.inScheme, cs_iri))
        #     # print(cs)
        #     cs_iri = str(cs)
        #     print(f'{f.name:>70} {str(cs).split("/")[-1].lower()}')
        # data = f.read_text().replace(cs_iri, "https://linked.data.gov.au/def/" + cs_iri.split("/")[-1].lower())
        # f.write_text()

        g.serialize(f, format="longturtle")


def note_old_iris():
    for f in Path(Path(__file__).parent.parent / "vocabs").glob("*.ttl"):
        print(f)
        c = f.read_text()
        for line in c.splitlines():
            if line.startswith("PREFIX : "):
                ns = line.replace("PREFIX : <", "").replace(">", "")

        g = Graph().parse(f)
        cs_iri = g.value(predicate=RDF.type, object=SKOS.ConceptScheme)
        # g.add((cs_iri, SKOS.historyNote, Literal(f"2024-04: IRIs changed from {cs_iri} for the ConceptScheme and {ns} for the Concept namespace to linked.data.gov.au-based IRIs")))
        # g.serialize(f, format="longturtle")

        for line in c.splitlines():
            if line.startswith(f"PREFIX cs: <{cs_iri}>"):
                new_cs = line.replace(f"PREFIX cs: <{cs_iri}>", f"PREFIX cs: <{ns.strip('/')}>").replace(">", "")

        print(f"{cs_iri} -> {new_cs}")
        f.write_text(c.replace(f"PREFIX cs: <{cs_iri}>", f"PREFIX cs: <{ns.strip('/')}>").replace(">", ""))


if __name__ == "__main__":
    cs_iri()
    # update_format()
    # note_old_iris()