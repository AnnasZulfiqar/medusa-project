#!/usr/bin/env python3
"""Build offline SVG diagrams and an interactive HTML knowledge graph."""
import csv
import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPHS = ROOT / "graphs"

COLORS = {
    "Mythological character": "#d8a7b8", "Person": "#bfd3ec", "Artwork": "#9ec6c2",
    "Literary work": "#9ec6c2", "Event": "#efc777", "Place": "#c9c4dc",
    "Organization": "#b8d8b8", "Concept": "#e8d9aa",
}

def svg_diagram(title, nodes, edges, path, width=1200, height=680):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
             '<style>text{font-family:Arial,sans-serif;fill:#28232a}.title{font:700 28px Georgia,serif}.label{font-size:13px}.edge{font-size:11px;fill:#655a63}.node{stroke:#584652;stroke-width:1.5}</style>',
             '<rect width="100%" height="100%" fill="#f8f5ee"/><text x="40" y="48" class="title">'+html.escape(title)+'</text>']
    for a,b,label in edges:
        x1,y1,_,_,_=nodes[a]; x2,y2,_,_,_=nodes[b]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8a7a84" stroke-width="1.5"/>')
        mx,my=(x1+x2)/2,(y1+y2)/2
        parts.append(f'<text x="{mx}" y="{my-5}" text-anchor="middle" class="edge">{html.escape(label)}</text>')
    for key,(x,y,label,color,shape) in nodes.items():
        if shape=="diamond":
            pts=f"{x},{y-34} {x+70},{y} {x},{y+34} {x-70},{y}"
            parts.append(f'<polygon points="{pts}" fill="{color}" class="node"/>')
        else:
            parts.append(f'<rect x="{x-78}" y="{y-28}" width="156" height="56" rx="14" fill="{color}" class="node"/>')
        parts.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" class="label">{html.escape(label)}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")

theory_nodes = {
 "medusa":(600,320,"Medusa","#d8a7b8","box"), "who":(125,130,"WHO","#ead9df","box"),
 "what":(125,300,"WHAT","#ead9df","box"), "where":(125,470,"WHERE","#ead9df","box"), "when":(125,610,"WHEN","#ead9df","box"),
 "people":(365,130,"Characters & creators","#bfd3ec","box"), "events":(365,300,"Events, texts & art","#efc777","box"),
 "places":(365,470,"Greece, Libya & museums","#c9c4dc","box"), "dates":(365,610,"Antiquity to Baroque","#e8d9aa","box"),
 "ovid":(850,150,"Ovid's Metamorphoses","#9ec6c2","box"), "art":(850,300,"Selected artworks","#9ec6c2","box"),
 "gorgon":(850,450,"Gorgoneion","#e8d9aa","box"), "question":(850,595,"Changing representation","#d8a7b8","box")
}
theory_edges=[("who","people","organizes"),("what","events","organizes"),("where","places","organizes"),("when","dates","organizes"),
 ("people","medusa","acts around"),("events","medusa","transform"),("places","medusa","contextualize"),("dates","medusa","situate"),
 ("medusa","ovid","represented in"),("medusa","art","depicted in"),("medusa","gorgon","symbolized by"),("ovid","question","informs"),("art","question","informs"),("gorgon","question","informs")]
svg_diagram("Theoretical Model: WHO / WHAT / WHERE / WHEN", theory_nodes, theory_edges, GRAPHS/"theoretical-model.svg")

concept_nodes={
 "character":(160,150,"frbroo:F38 Character","#fff2a8","box"),"person":(160,300,"crm:E21 Person","#fff2a8","box"),
 "event":(475,150,"crm:E5 Event","#fff2a8","box"),"production":(475,300,"crm:E12 Production","#fff2a8","box"),
 "artwork":(800,225,"crm:E22 Human-Made Object","#fff2a8","box"),"work":(800,410,"frbroo:F1 Work","#fff2a8","box"),
 "place":(1050,130,"crm:E53 Place","#fff2a8","box"),"time":(1050,300,"crm:E52 Time-Span","#fff2a8","box"),"concept":(1050,470,"skos:Concept","#fff2a8","box")
}
concept_edges=[("event","character","P31 has modified"),("event","person","P14 carried out by"),("production","person","P14 carried out by"),
 ("production","artwork","P108 has produced"),("production","place","P7 took place at"),("production","time","P4 has time-span"),
 ("artwork","character","P62 depicts"),("artwork","event","P62 depicts"),("artwork","place","P55 current location"),("artwork","concept","P2 has type"),
 ("work","character","P67 refers to"),("work","event","P67 refers to"),("work","person","dcterms:creator")]
svg_diagram("Graffoo-Compatible Conceptual Model", concept_nodes, concept_edges, GRAPHS/"conceptual-model.svg",1200,600)

with open(ROOT/"data/entities.csv", newline="", encoding="utf-8") as f:
    all_entities=list(csv.DictReader(f))
core_ids={"medusa","perseus","athena","poseidon","pegasus","chrysaor","ovid","caravaggio","rubens","snyders","cellini","metamorphoses","caravaggio_medusa","rubens_medusa","cellini_perseus","transformation","beheading","emergence","production_caravaggio","production_rubens","production_cellini","gorgoneion","petrification","apotropaic","uffizi","khm","loggia"}
entities=[e for e in all_entities if e["id"] in core_ids]
entity_map={e["id"]:e for e in entities}
with open(ROOT/"data/relations.csv", newline="", encoding="utf-8") as f:
    relations=[r for r in csv.DictReader(f) if r["subject"] in entity_map and r["object"] in entity_map]

W,H=1400,900; cx,cy=700,465; radius=350
positions={}
for i,e in enumerate(entities):
    angle=-math.pi/2+2*math.pi*i/len(entities)
    r=0 if e["id"]=="medusa" else radius+(i%3-1)*65
    positions[e["id"]]=(cx+r*math.cos(angle),cy+r*math.sin(angle))
positions["medusa"]=(cx,cy)
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" id="kg" role="img" aria-label="Medusa knowledge graph">',
'<style>.edge{stroke:#a99ba4;stroke-width:1.2}.edge-label{font:10px Arial;fill:#6c6068}.node text{font:11px Arial;fill:#231e22;pointer-events:none}.node circle{stroke:#584652;stroke-width:1.5;cursor:pointer}.node.dim,.edge-group.dim{opacity:.08}.node.active circle{stroke:#161116;stroke-width:4}</style>',
'<rect width="100%" height="100%" fill="#f8f5ee"/>']
for j,r in enumerate(relations):
    x1,y1=positions[r["subject"]]; x2,y2=positions[r["object"]]
    parts.append(f'<g class="edge-group" data-a="{r["subject"]}" data-b="{r["object"]}"><line class="edge" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/><text class="edge-label" x="{(x1+x2)/2:.1f}" y="{(y1+y2)/2:.1f}">{html.escape(r["predicate"])}</text></g>')
for e in entities:
    x,y=positions[e["id"]]; color=COLORS.get(e["type"],"#ddd"); lbl=e["label"]; short=lbl if len(lbl)<24 else lbl[:21]+"..."
    parts.append(f'<g class="node" data-id="{e["id"]}" data-type="{html.escape(e["type"])}" data-label="{html.escape(lbl)}" data-desc="{html.escape(e["description"])}" data-authority="{html.escape(e["authority_uri"])}" transform="translate({x:.1f},{y:.1f})"><circle r="39" fill="{color}"/><text text-anchor="middle" y="4">{html.escape(short)}</text></g>')
parts.append("</svg>")
(GRAPHS/"graph.svg").write_text("\n".join(parts),encoding="utf-8")

graph_html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Interactive Medusa Knowledge Graph</title><link rel="stylesheet" href="../assets/css/style.css"></head><body class="graph-page"><header class="graph-header"><a href="../index.html">← Project home</a><h1>Interactive Knowledge Graph</h1><p>Choose a node to isolate its relationships.</p><button id="reset">Reset graph</button></header><main class="graph-layout"><section class="graph-canvas">''' + (GRAPHS/"graph.svg").read_text(encoding="utf-8") + '''</section><aside id="details"><p class="eyebrow">Selected resource</p><h2>Medusa project graph</h2><p>Select a node to inspect its type, description, and authority record.</p></aside></main><script>
const nodes=[...document.querySelectorAll('.node')], edges=[...document.querySelectorAll('.edge-group')], details=document.querySelector('#details');
function reset(){nodes.forEach(n=>n.classList.remove('dim','active'));edges.forEach(e=>e.classList.remove('dim'));details.innerHTML='<p class="eyebrow">Selected resource</p><h2>Medusa project graph</h2><p>Select a node to inspect its type, description, and authority record.</p>'}
nodes.forEach(n=>n.addEventListener('click',()=>{let id=n.dataset.id, connected=new Set([id]);edges.forEach(e=>{if(e.dataset.a===id||e.dataset.b===id){connected.add(e.dataset.a);connected.add(e.dataset.b);e.classList.remove('dim')}else e.classList.add('dim')});nodes.forEach(x=>{x.classList.toggle('dim',!connected.has(x.dataset.id));x.classList.toggle('active',x===n)});let link=n.dataset.authority?`<a href="${n.dataset.authority}" target="_blank">Open authority record</a>`:'';details.innerHTML=`<p class="eyebrow">${n.dataset.type}</p><h2>${n.dataset.label}</h2><p>${n.dataset.desc}</p>${link}`}));
document.querySelector('#reset').addEventListener('click',reset);
</script></body></html>'''
(GRAPHS/"graph.html").write_text(graph_html,encoding="utf-8")
print("Built graph SVGs and interactive graph")
