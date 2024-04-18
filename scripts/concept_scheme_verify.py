from rdflib import Graph
from rdflib.namespace import RDF, SH, SKOS

from pathlib import Path


def check_all():
    vocs = sorted(Path(Path(__file__).parent.parent / "vocabs").glob("*.ttl"))
    for f in vocs:
        g = Graph()
        g.parse(location=f, format="turtle")
        
        ConceptSchemes = list(g.subjects(RDF.type, SKOS.ConceptScheme))
        if len(ConceptSchemes) > 1:
            raise RuntimeError(f"File {f} has more than one ConceptScheme.")
        elif len(ConceptSchemes) < 1:
            raise RuntimeError(f"File {f} does not have a ConceptScheme.")
        ConceptScheme = ConceptSchemes[0]
        hasTopConcepts = list(g.objects(ConceptScheme, SKOS.hasTopConcept))
        for tc in hasTopConcepts:
            broader = list(g.objects(tc, SKOS.broader))
            for obj in broader:
                if obj in hasTopConcepts:
                    print(f"File {f}: TopConcept {tc} has broader concept in the same ConceptScheme: {obj}")


if __name__ == "__main__":
    check_all()
