# Methodology

## Research design

Medusa was selected because her representation changes substantially across source types: mythological character, victim of transformation, defeated monster, apotropaic emblem, and subject of later art. The research question therefore connects literary transmission with visual interpretation.

## Corpus

The primary corpus is a focused selection from the English Wikipedia article **Medusa**, retrieved on 15 June 2026. It includes mythology, Ovid's influential account, the Gorgoneion, and artistic representation. Scientific-name lists and unrelated popular-culture catalogues were excluded because they do not answer the research question.

Literary evidence comes from Ovid's *Metamorphoses*, Book IV, 753-803, especially uploaded PDF pages 128-130. Only two short quotations are reproduced. Artwork metadata uses museum records where available, particularly the Kunsthistorisches Museum record for Rubens' *Head of Medusa*.

## Entity selection

Entities were selected when they perform at least one of four roles:

1. Participate in Medusa's narrative.
2. Produce, hold, or locate a representation.
3. Constitute a literary or artistic representation.
4. Explain a recurring representational concept.

The resulting dataset exceeds the minimum of ten entities and includes mythological characters, people, groups, places, organizations, events, artworks, a literary work, and concepts.

## Reconciliation

Wikidata and VIAF identify people and mythological characters; GeoNames identifies geographic places; Getty AAT identifies selected concepts and artwork types; museum URLs identify collection objects. Identifiers were omitted where an authority match was uncertain.

## Workflow

1. Record normalized resources in `entities.csv`.
2. Record evidence-based subject-predicate-object statements in `relations.csv`.
3. Encode the corpus and a structured authority register in TEI P5.
4. Transform TEI to readable HTML using XSLT.
5. Transform TEI stand-off entities and relations into RDF/Turtle using Python.
6. Visualize the theoretical model, conceptual model, and dataset as graphs.

This approach makes the TEI document the central scholarly source while retaining CSV tables for transparent inspection.
