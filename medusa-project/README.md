# Medusa Linked Open Data Project

**Research question:** How is Medusa represented across literary and artistic sources?

This University of Bologna LODLAM project studies Medusa through a focused Wikipedia corpus, Ovid's *Metamorphoses*, and three artworks by Caravaggio, Peter Paul Rubens, and Benvenuto Cellini. It provides TEI P5, RDF/Turtle, authority reconciliation, theoretical and conceptual models, an interactive knowledge graph, and a static academic website.

## Open the project

Open `index.html` in a browser. All project files are linked from the website and work locally.

## Rebuild derived files

From `medusa-project/`:

```bash
xsltproc scripts/tei2html.xsl xml/medusa.xml > html/medusa.html
python3 scripts/tei2rdf.py
python3 scripts/build_graphs.py
```

## Structure

- `data/`: reconciled entities and relations
- `xml/`: TEI P5 source
- `rdf/`: generated Turtle dataset
- `graphs/`: theoretical, conceptual, and knowledge graph outputs
- `docs/`: methodology, ontology, and sources
- `scripts/`: repeatable transformations

## Licenses

Original project data and documentation are released under CC BY 4.0. Wikipedia-derived prose is attributed to Wikipedia contributors and remains under CC BY-SA 4.0. Short Ovid quotations are included for scholarly analysis and attributed to the uploaded A. S. Kline translation.
