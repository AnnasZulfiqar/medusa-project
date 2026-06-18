# Ontology and Modeling Decisions

## Modeling approach

The project uses an event-centered CIDOC-CRM model inspired by the Venus/MythLOD example. Instead of encoding only simple statements such as "Perseus killed Medusa," the model treats transformation, beheading, emergence, and artwork creation as events that connect actors, objects, times, places, and evidence.

## Reused ontologies

| Domain | Class or property | Use |
|---|---|---|
| Mythological characters | `frbroo:F38_Character` | Medusa, Perseus, Athena, and related figures |
| Historical people | `crm:E21_Person` | Ovid and artists |
| Groups and museums | `crm:E74_Group` | Gorgons and holding institutions |
| Places | `crm:E53_Place` | Countries, cities, and artwork locations |
| Narrative events | `crm:E5_Event` | Transformation, beheading, and emergence |
| Artworks | `crm:E22_Human-Made_Object` | Selected paintings and sculpture |
| Literary work | `frbroo:F1_Work` | *Metamorphoses* |
| Concepts | `skos:Concept` | Petrification, Gorgoneion, apotropaic protection |
| Attribution | `crm:P14_carried_out_by` | Connects works/events to responsible actors |
| Depiction | `crm:P62_depicts` | Connects artworks to Medusa, Perseus, or events |
| Reference | `crm:P67_refers_to` | Connects texts/artworks to narrative subjects |
| Creation | `crm:P94_has_created` | Connects the emergence event to Pegasus and Chrysaor |
| Modification | `crm:P31_has_modified` | Connects transformation and beheading to Medusa |
| Reconciliation | `owl:sameAs`, `skos:exactMatch` | Links local resources to authority records |

## Key decisions

- Mythological figures are modeled as FRBRoo characters rather than historical people.
- Artwork production is represented through responsibility statements in this compact dataset; the conceptual model shows how these may be expanded into `crm:E12_Production` events.
- Athena/Minerva and Poseidon/Neptune each use one local resource with alternate names because the corpus compares Greek and Roman naming traditions without treating them as separate characters.
- The relation between Poseidon/Neptune and Medusa is expressed cautiously as presence in the transformation event. This avoids reducing a contested narrative to an unqualified romantic association.
- Museum records take precedence over secondary summaries. Rubens' *Head of Medusa* is dated approximately 1613, following the Kunsthistorisches Museum.
- Authority links are alignments, not replacements for local meaningful URIs.

## URI policy

Local resources use stable, readable paths under:

```text
https://w3id.org/medusaProject/
```

Examples:

```text
https://w3id.org/medusaProject/person/medusa
https://w3id.org/medusaProject/event/beheading
https://w3id.org/medusaProject/item/rubens_medusa
```
