#!/usr/bin/env python3
"""Transform the Medusa TEI standOff data into deterministic RDF/Turtle."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TEI = ROOT / "xml" / "medusa.xml"
OUT = ROOT / "rdf" / "medusa.ttl"
NS = {"tei": "http://www.tei-c.org/ns/1.0"}
BASE = "https://w3id.org/medusaProject/"

PREFIXES = """@prefix medusa: <https://w3id.org/medusaProject/> .
@prefix person: <https://w3id.org/medusaProject/person/> .
@prefix place: <https://w3id.org/medusaProject/place/> .
@prefix org: <https://w3id.org/medusaProject/org/> .
@prefix item: <https://w3id.org/medusaProject/item/> .
@prefix event: <https://w3id.org/medusaProject/event/> .
@prefix concept: <https://w3id.org/medusaProject/concept/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix frbroo: <http://erlangen-crm.org/efrbroo/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""

def literal(text):
    return '"' + " ".join(text.split()).replace("\\", "\\\\").replace('"', '\\"') + '"'

XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

def local_name(node):
    return node.tag.rsplit("}", 1)[-1]

def qname(node):
    ident = node.get(XML_ID)
    tag = local_name(node)
    if tag == "person": return f"person:{ident}"
    if tag == "place": return f"place:{ident}"
    if tag == "org": return f"org:{ident}"
    if tag == "item": return f"concept:{ident}"
    if tag in {"bibl", "object"}: return f"item:{ident}"
    if tag == "event": return f"event:{ident}"
    return f"medusa:{ident}"

def label(node):
    for tag in ("persName", "placeName", "orgName", "title", "objectName", "label"):
        found = node.find(f"tei:{tag}", NS)
        if found is not None:
            return " ".join("".join(found.itertext()).split())
    return node.get(XML_ID, "")

def rdf_type(node):
    tag = local_name(node)
    if tag == "person":
        return "frbroo:F38_Character" if node.get("role") == "mythologicalCharacter" else "crm:E21_Person"
    if tag == "event" and node.get("type") == "production": return "crm:E12_Production"
    return {"place":"crm:E53_Place","org":"crm:E74_Group","bibl":"frbroo:F1_Work","object":"crm:E22_Human-Made_Object","event":"crm:E5_Event","item":"skos:Concept"}.get(tag, "crm:E1_CRM_Entity")

tree = ET.parse(TEI)
stand_off = tree.find(".//tei:standOff", NS)
allowed = {"person", "place", "org", "bibl", "object", "event", "item"}
nodes = [n for n in stand_off.iter() if n.get(XML_ID) and local_name(n) in allowed]
idmap = {n.get(XML_ID): qname(n) for n in nodes}
lines = [PREFIXES, "medusa: a owl:Ontology ;", '  dcterms:title "Medusa Across Literary and Artistic Sources" ;', '  dcterms:license <https://creativecommons.org/licenses/by/4.0/> .', ""]
for node in nodes:
    lines.append(f"{qname(node)} a {rdf_type(node)} ;")
    props = [f"  rdfs:label {literal(label(node))}"]
    if node.get("sameAs"): props.append(f"  owl:sameAs <{node.get('sameAs')}>")
    desc_node = node.find("tei:desc", NS)
    if desc_node is None:
        desc_node = node.find("tei:note", NS)
    desc = " ".join("".join(desc_node.itertext()).split()) if desc_node is not None else ""
    if desc: props.append(f"  dcterms:description {literal(desc)}")
    lines.append(" ;\n".join(props) + " .\n")

for rel in tree.findall(".//tei:listRelation/tei:relation", NS):
    prop = rel.get("name")
    for active in rel.get("active").split():
        for passive in rel.get("passive").split():
            a, p = active.lstrip("#"), passive.lstrip("#")
            if a in idmap and p in idmap:
                lines.append(f"{idmap[a]} {prop} {idmap[p]} .")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {OUT}")
