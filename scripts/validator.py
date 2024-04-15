from rdflib import Graph
from rdflib.namespace import RDF, SH, SKOS
from pyshacl import validate

from pathlib import Path


def print_shacl_result_graph(vocab: str, g: Graph):
    st = ""
    count = 0
    for s, res in g.subject_objects(SH.result):
        if g.value(res, SH.resultSeverity) == SH.Violation:
            count += 1
            for p2, o2 in g.predicate_objects(res):
                if p2 == SH.focusNode:
                    st += (f"<{o2}>\n")
            for p2, o2 in g.predicate_objects(res):
                if p2 not in [SH.sourceShape, RDF.type, SH.focusNode]:
                    try:
                        st += f"\t{g.qname(p2)} {g.qname(o2)}\n"
                    except:
                        st += f"\t{g.qname(p2)} {o2}\n"
            st += "\n"

    st = f"{vocab}: {count} violations\n\n" + st
    print(st)


def validate_all():
    vocs = sorted(Path(Path(__file__).parent.parent / "vocabs").glob("*.ttl"))
    for f in vocs:
        print(f"validating {f.name}")
        conforms, results_graph, results_text = validate(Graph().parse(f), shacl_graph="vocpub4.9.ttl", allow_warnings=False)
        if not conforms:
            print(f"{f} is invalid")
            print_shacl_result_graph(f, results_graph)


if __name__ == "__main__":
    validate_all()
