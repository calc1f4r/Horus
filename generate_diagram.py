#!/usr/bin/env python3
"""Generate Excalidraw architecture diagram — ALL sections stacked vertically, zero overlap."""

import json, random

_id = 100000
def uid():
    global _id; _id += 1; return f"el_{_id}"
def seed():
    return random.randint(100_000_000, 2_000_000_000)

def mk_rect(x, y, w, h, bg="#fff", stroke="#1e1e1e", dash=False, sw=2):
    i = uid()
    return i, {"id":i,"type":"rectangle","x":x,"y":y,"width":w,"height":h,
        "angle":0,"strokeColor":stroke,"backgroundColor":bg,
        "fillStyle":"solid","strokeWidth":sw,
        "strokeStyle":"dashed" if dash else "solid","roughness":0,
        "opacity":100,"groupIds":[],"frameId":None,
        "roundness":{"type":3},"seed":seed(),"version":1,"versionNonce":seed(),
        "isDeleted":False,"boundElements":[],"updated":1771536000000,
        "link":None,"locked":False}

def mk_text(x, y, w, h, txt, sz=14, color="#1e1e1e", align="center", cid=None, bold=False):
    i = uid()
    return i, {"id":i,"type":"text","x":x,"y":y,"width":w,"height":h,
        "angle":0,"strokeColor":color,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":2,"strokeStyle":"solid","roughness":0,
        "opacity":100,"groupIds":[],"frameId":None,"roundness":None,
        "seed":seed(),"version":1,"versionNonce":seed(),
        "isDeleted":False,"boundElements":None,"updated":1771536000000,
        "link":None,"locked":False,
        "text":txt,"fontSize":sz,"fontFamily":3 if bold else 5,
        "textAlign":align,"verticalAlign":"middle",
        "containerId":cid,"originalText":txt,
        "autoResize":True,"lineHeight":1.25}

def mk_arrow(x1, y1, x2, y2, color="#666", sw=2):
    i = uid()
    return [{"id":i,"type":"arrow","x":x1,"y":y1,
        "width":abs(x2-x1),"height":abs(y2-y1),
        "angle":0,"strokeColor":color,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":sw,"strokeStyle":"solid","roughness":0,
        "opacity":100,"groupIds":[],"frameId":None,"roundness":{"type":2},
        "seed":seed(),"version":1,"versionNonce":seed(),
        "isDeleted":False,"boundElements":[],"updated":1771536000000,
        "link":None,"locked":False,
        "points":[[0,0],[x2-x1,y2-y1]],
        "startBinding":None,"endBinding":None,
        "startArrowhead":None,"endArrowhead":"arrow"}]

def box(x, y, w, h, label, bg="#fff", stroke="#1e1e1e", sz=14, color="#1e1e1e", bold=False):
    rid, r = mk_rect(x, y, w, h, bg=bg, stroke=stroke)
    lines = label.count("\n") + 1
    th = lines * sz * 1.25
    tid, t = mk_text(x+5, y+(h-th)/2, w-10, th, label, sz=sz, color=color, cid=rid, bold=bold)
    r["boundElements"] = [{"id":tid,"type":"text"}]
    return [r, t]

def badge(x, y, w, label, bg="#2196F3", color="#fff"):
    rid, r = mk_rect(x, y, w, 30, bg=bg, stroke=bg)
    tid, t = mk_text(x+5, y+3, w-10, 24, label, sz=14, color=color, cid=rid, bold=True)
    r["boundElements"] = [{"id":tid,"type":"text"}]
    return [r, t]

# ═══════════════════════════════════════════════════════════════════
E = []   # all elements
W = 2100
P = 50   # padding
CW = W - 2*P

# ═══════════════════════════════════════════════════════════════════
# A : TITLE   y 10 → 90
# ═══════════════════════════════════════════════════════════════════
E.extend(box(P, 10, CW, 55,
    "VULNERABILITY DATABASE — COMPLETE ARCHITECTURE & AGENTIC WORKFLOW",
    bg="#1a1a2e", stroke="#1a1a2e", sz=24, color="#e0e0ff", bold=True))
_, t = mk_text(P+100, 72, CW-200, 18,
    "4-Tier Search · 11 Manifests · 500+ Patterns · 7-Phase Audit Pipeline · 16 Agents · Parallel Fan-Out",
    sz=13, color="#888")
E.append(t)

# ═══════════════════════════════════════════════════════════════════
# B : DATA SOURCES   y 120 → 530
# ═══════════════════════════════════════════════════════════════════
BY = 120; BH = 410
rid, r = mk_rect(P, BY, CW, BH, stroke="#43A047", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, BY-13, 350, "① DATA SOURCES & INGESTION", bg="#43A047"))

# Row 1  –  4 sources
bw = (CW - 200) // 4
for i, s in enumerate([
    "Solodit API\n(Cyfrin Audit Reports)",
    "DeFiHackLabs\n(Real-World Exploits)",
    "Manual Audit Reports\n(reports/ directory)",
    "Variant Analysis\n(Semgrep / CodeQL)"]):
    sx = P+40 + i*(bw+40)
    E.extend(box(sx, BY+45, bw, 65, s, bg="#c8e6c9", sz=13))
    E.extend(mk_arrow(sx+bw//2, BY+110, sx+bw//2, BY+155, "#43A047"))

# Row 2  –  3 ingestion agents
E.extend(badge(P+40, BY+152, 200, "Ingestion Agents", bg="#66BB6A"))
abw = (CW - 160) // 3
for i, a in enumerate([
    "🔍 solodit-fetching Agent",
    "📦 defihacklabs-indexer Agent",
    "✍️ variant-template-writer Agent"]):
    ax = P+40 + i*(abw+40)
    E.extend(box(ax, BY+190, abw, 45, a, bg="#e8f5e9", sz=13))
    E.extend(mk_arrow(ax+abw//2, BY+235, ax+abw//2, BY+275, "#43A047"))

# Row 3  –  4 scripts
E.extend(badge(P+40, BY+272, 200, "Processing Scripts", bg="#66BB6A"))
for i, s in enumerate([
    "solodit_fetcher.py\n(API Fetcher)",
    "classify_and_group.py\n(Classifier)",
    "generate_entries.py\n(Entry Generator)",
    "generate_manifests.py\n(Manifest Builder)"]):
    sx = P+40 + i*(bw+40)
    E.extend(box(sx, BY+310, bw, 55, s, bg="#fff3e0", sz=12))

# ═══════════════════════════════════════════════════════════════════
# C : 4-TIER DB   y 570 → 980
# ═══════════════════════════════════════════════════════════════════
CY2 = 570; CH2 = 410
rid, r = mk_rect(P, CY2, CW, CH2, stroke="#1976D2", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, CY2-13, 450, "② VULNERABILITY DATABASE — 4-TIER SEARCH", bg="#1976D2"))

TW = 550
for i, (lbl, bg2, desc) in enumerate([
    ("TIER 1 → Router  (DB/index.json)",          "#BBDEFB",
     "~330 lines — protocolContext, manifest list, keyword index, audit checklist"),
    ("TIER 1.5 → Hunt Cards  (huntcards/*.json)",  "#90CAF9",
     "451 compressed cards (~55K tokens) — grep patterns, micro-directives, neverPrune"),
    ("TIER 2 → Manifests  (manifests/*.json)",     "#64B5F6",
     "11 manifests — pattern indexes with lineStart/lineEnd, codeKeywords, rootCause"),
    ("TIER 3 → Entries  (DB/**/*.md)",             "#42A5F5",
     "Full vuln content — YAML frontmatter, vulnerable/secure patterns, targeted reads only"),
]):
    ty = CY2+40 + i*90
    tc = "#fff" if i==3 else "#1e1e1e"
    E.extend(box(P+30, ty, TW, 50, lbl, bg=bg2, stroke="#1976D2", sz=14, color=tc, bold=True))
    _, t = mk_text(P+30, ty+52, TW, 16, desc, sz=11, color="#555", align="left"); E.append(t)
    if i > 0:
        E.extend(mk_arrow(P+305, ty-20, P+305, ty, "#1976D2", sw=3))

# Manifest list (right side)
MX = P + TW + 80
E.extend(badge(MX, CY2+30, 240, "11 Manifest Categories", bg="#42A5F5"))
mw = CW - TW - 110
for i, m in enumerate([
    "oracle (39) — Chainlink, Pyth, price manipulation",
    "amm (65) — Concentrated liquidity, constant product",
    "bridge (32) — LayerZero, Wormhole, Hyperlane, CCIP",
    "tokens (33) — ERC20, ERC4626, ERC721",
    "cosmos (26) — Cosmos SDK, IBC, staking",
    "solana (38) — Solana programs, Token-2022",
    "general-security (31) — Access control, signatures",
    "general-defi (115) — Flash loans, vaults, precision",
    "general-infrastructure (41) — Proxies, reentrancy",
    "general-governance (56) — Governance, stablecoins, MEV",
    "unique (59) — Protocol-specific exploits",
]):
    E.extend(box(MX, CY2+67+i*30, mw, 27, m,
        bg="#E3F2FD" if i%2==0 else "#FFF", stroke="#90CAF9", sz=11))

# ═══════════════════════════════════════════════════════════════════
# D : 7-PHASE PIPELINE   y 1020 → 1920
# ═══════════════════════════════════════════════════════════════════
DY = 1020; DH = 900
rid, r = mk_rect(P, DY, CW, DH, stroke="#E65100", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, DY-13, 540, "③ 7-PHASE AUDIT PIPELINE — AGENTIC WORKFLOW", bg="#E65100"))

# Orchestrator
E.extend(box(P+500, DY+30, 1000, 55,
    "🎯 AUDIT-ORCHESTRATOR  —  @audit-orchestrator <codebase-path> [protocol-hint]  —  ENTRY POINT",
    bg="#FF6F00", stroke="#E65100", sz=16, color="#fff", bold=True))
_, t = mk_text(P+500, DY+90, 1000, 16,
    "Orchestrates entire pipeline · Spawns sub-agents per phase · Manages data flow between phases",
    sz=12, color="#BF360C")
E.append(t)

# Phase rows — each is:  [ phase_box  |  description_text  |  agent_badge ]
# All laid out in a single column, no overlap possible
PY0 = DY + 125
PG  = 90   # gap
PW  = 220  # phase box width
PH  = 65   # phase box height

phases = [
   #  label                         bg        description                                                                              agent
    ("Phase 1\nReconnaissance",      "#FFF3E0", "Protocol detection → Scope definition → Manifest resolution",                          "(self — orchestrator)"),
    ("Phase 2\nContext Building",    "#FFF3E0", "Deep line-by-line codebase analysis → produces 01-context.md",                          "🤖 audit-context-building"),
    ("Phase 3\nInvariant Extraction","#FFF3E0", "Extract all system invariants from context → produces 02-invariants.md",                "🤖 invariant-writer"),
    ("Phase 4\nDB-Powered Hunting",  "#FFECB3", "Grep-prune hunt cards → Partition shards → Parallel scan → 03-findings-raw.md",        "🤖 N × invariant-catcher  (→ see ⑤)"),
    ("Phase 4a\nReasoning Discovery","#FFECB3", "Domain decomposition → Spawns domain sub-agents → 04a-reasoning-findings.md",          "🤖 protocol-reasoning-agent"),
    ("Phase 5\nValidation Gaps",     "#FFF3E0", "Specialized input validation scanning → 04-validation-findings.md",                    "🤖 missing-validation-reasoning"),
    ("Phase 6\nTriage & PoC",        "#FFCCBC", "Severity scoring + Exploit PoC writing → 05-findings-triaged.md",                      "🤖 poc-writing"),
    ("Phase 7\nDownstream Gen",      "#FFCCBC", "Fuzzing · Formal verification · Severity validation against contest criteria",         "🤖 medusa · certora · sherlock · cantina"),
]

prev_bot = None
for i, (label, bg, desc, agent) in enumerate(phases):
    py = PY0 + i * PG
    # Phase box
    E.extend(box(P+40, py, PW, PH, label, bg=bg, stroke="#E65100", sz=13, bold=True))
    # Description
    _, t = mk_text(P+40+PW+25, py+12, 700, 18, desc, sz=12, color="#555", align="left"); E.append(t)
    # Agent badge
    abg = "#E8EAF6" if "context" in agent.lower() or "invariant" in agent.lower() else \
          "#F3E5F5" if "reasoning" in agent.lower() else \
          "#E0F2F1" if "validation" in agent.lower() else "#FCE4EC"
    E.extend(box(P+40+PW+750, py+10, 450, 30, agent, bg=abg, stroke="#7E57C2", sz=12))
    # Arrow from prev
    if prev_bot is not None:
        E.extend(mk_arrow(P+40+PW//2, prev_bot, P+40+PW//2, py, "#E65100", sw=2))
    prev_bot = py + PH

# Arrow from orchestrator to Phase 1
E.extend(mk_arrow(P+1000, DY+85, P+40+PW//2, PY0, "#E65100", sw=3))

# Final report
RPT_Y = PY0 + 8 * PG
E.extend(box(P+40, RPT_Y, CW-100, 50,
    "📄 FINAL → audit-output/AUDIT-REPORT.md  —  Consolidated report with all findings, PoCs, severity validations",
    bg="#1B5E20", stroke="#1B5E20", sz=14, color="#fff", bold=True))
E.extend(mk_arrow(P+40+PW//2, prev_bot, P+40+PW//2, RPT_Y, "#1B5E20", sw=3))

# ═══════════════════════════════════════════════════════════════════
# E : POST-TRIAGE AGENTS   y 1960 → 2520
# ═══════════════════════════════════════════════════════════════════
EY = 1960; EH = 560
rid, r = mk_rect(P, EY, CW, EH, stroke="#C62828", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, EY-13, 380, "④ POST-TRIAGE & DOWNSTREAM AGENTS", bg="#C62828"))

post = [
    ("🧪 poc-writing Agent",         "Writes compilable Foundry/Hardhat exploit PoCs\nfor CRITICAL/HIGH findings",   "→ pocs/F-NNN-poc.t.sol",      "#FFEBEE","#C62828"),
    ("✏️ issue-writer Agent",         "Polishes raw findings into platform-ready\nsubmission format",                "→ Formatted issue markdown",   "#FFEBEE","#C62828"),
    ("🏛️ sherlock-judging Agent",     "Validates findings against Sherlock\njudging criteria",                       "→ 06-sherlock-validation.md",  "#E8EAF6","#283593"),
    ("⚖️ cantina-judge Agent",        "Validates findings against Cantina\ncontest standards",                       "→ 07-cantina-validation.md",   "#E8EAF6","#283593"),
    ("🔬 medusa-fuzzing Agent",       "Generates Medusa stateful fuzzing\nharnesses from invariant specs",           "→ fuzzing/ directory",         "#E0F7FA","#00695C"),
    ("📐 certora-verification Agent", "Generates Certora CVL formal\nverification specs",                           "→ certora/ directory",         "#E0F7FA","#00695C"),
]
col_w = (CW - 100) // 2
for i, (name, desc, out, bg, sc) in enumerate(post):
    col = i % 2
    row = i // 2
    px = P+30 + col*(col_w+40)
    py = EY+45 + row*170
    E.extend(box(px, py, col_w, 145, f"{name}\n\n{desc}\n\n{out}", bg=bg, stroke=sc, sz=13))

# ═══════════════════════════════════════════════════════════════════
# F : FAN-OUT DETAIL   y 2560 → 3120
# ═══════════════════════════════════════════════════════════════════
FY = 2560; FH = 560
rid, r = mk_rect(P, FY, CW, FH, stroke="#7E57C2", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, FY-13, 510, "⑤ PHASE 4 DETAIL — PARALLEL FAN-OUT HUNTING", bg="#7E57C2"))

# Steps 1-3 stacked vertically
steps = [
    ("Step 1 → Load Hunt Cards  (all-huntcards.json · 451 cards · ~55K tokens)",
     "Each card: { id, title, cat, grep, check[], antipattern, securePattern, ref, lines, neverPrune }"),
    ("Step 2 → Grep-Prune Target Code  (grep_prune.py · removes ~60-80% of cards)",
     "grep -rn \"card.grep\" <target_path> — cards with zero hits removed (except neverPrune=true)"),
    ("Step 3 → Partition into Shards  (partition_shards.py · 50-80 cards per shard)",
     "Group surviving cards by category tag — neverPrune cards duplicated into EVERY shard"),
]
for i, (lbl, desc) in enumerate(steps):
    sy = FY+40 + i*80
    E.extend(box(P+40, sy, 700, 45, lbl, bg="#EDE7F6", stroke="#7E57C2", sz=13, bold=True))
    _, t = mk_text(P+760, sy+8, 550, 30, desc, sz=11, color="#666", align="left"); E.append(t)
    if i > 0:
        E.extend(mk_arrow(P+390, sy-35, P+390, sy, "#7E57C2", sw=2))

# Shard boxes
SHY = FY + 290
num = 5
shw = (CW - 80 - (num-1)*30) // num
for i in range(num):
    sx = P+40 + i*(shw+30)
    lbl = f"Shard {i+1}" if i < 4 else "Shard N"
    E.extend(box(sx, SHY, shw, 50, f"🤖 invariant-catcher\n{lbl}",
        bg="#D1C4E9", stroke="#7E57C2", sz=12, bold=True))
    E.extend(mk_arrow(P+390, FY+40+2*80+45, sx+shw//2, SHY, "#7E57C2", sw=2))

# Warning
_, t = mk_text(P+40, SHY+58, CW-80, 16,
    "⚠️ neverPrune=true cards duplicated into EVERY shard — CRITICAL safety net for must-check patterns",
    sz=12, color="#D32F2F")
E.append(t)

# Two passes
PSY = SHY + 90
hw = (CW-100)//2
E.extend(box(P+40, PSY, hw, 40,
    "PASS 1 → Execute micro-directives  (grep → hit? → run card.check steps)",
    bg="#F3E5F5", stroke="#9575CD", sz=12))
E.extend(box(P+40+hw+20, PSY, hw, 40,
    "PASS 2 → Evidence lookup & classification  (true / likely / false positive)",
    bg="#F3E5F5", stroke="#9575CD", sz=12))
E.extend(mk_arrow(P+40+hw, PSY+20, P+40+hw+20, PSY+20, "#9575CD", sw=2))

# Merge
MY2 = PSY + 65
E.extend(box(P+40, MY2, CW-80, 45,
    "Step 4 → Merge All Shard Findings  (merge_shard_findings.py)  →  Deduplicate by root cause  →  03-findings-raw.md",
    bg="#B39DDB", stroke="#5E35B1", sz=13, color="#fff", bold=True))
E.extend(mk_arrow(P+CW//4, PSY+40, P+CW//4, MY2, "#5E35B1", sw=2))
E.extend(mk_arrow(P+3*CW//4, PSY+40, P+3*CW//4, MY2, "#5E35B1", sw=2))

# ═══════════════════════════════════════════════════════════════════
# G : DATA ARTIFACTS   y 3160 → 3470
# ═══════════════════════════════════════════════════════════════════
GY2 = 3160; GH2 = 310
rid, r = mk_rect(P, GY2, CW, GH2, stroke="#37474F", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, GY2-13, 380, "⑥ DATA PIPELINE — ARTIFACT FLOW", bg="#37474F"))

arts = [
    ("00-scope.md\nSCOPE",          "#E3F2FD"),
    ("01-context.md\nCONTEXT",      "#E8F5E9"),
    ("02-invariants.md\nINVARIANTS","#FFF9C4"),
    ("03-findings.md\nRAW FINDINGS","#FFECB3"),
    ("04-validation.md\nVALIDATION","#FFE0B2"),
    ("04a-reasoning.md\nREASONING", "#F3E5F5"),
    ("05-triaged.md\nTRIAGED",     "#FFCCBC"),
    ("AUDIT-REPORT.md\nFINAL",     "#C8E6C9"),
]
aw = (CW - 80 - 7*15) // 8
for i, (lbl, bg) in enumerate(arts):
    ax = P+40 + i*(aw+15)
    E.extend(box(ax, GY2+40, aw, 60, lbl, bg=bg, stroke="#78909C", sz=12, bold=True))
    if i > 0:
        E.extend(mk_arrow(ax-15, GY2+70, ax, GY2+70, "#546E7A", sw=2))

_, t = mk_text(P+40, GY2+120, CW-80, 160,
    "Producer → Consumer Chain:\n\n"
    "• orchestrator → 00-scope.md → audit-context-building → 01-context.md\n"
    "• invariant-writer consumes context → 02-invariants.md\n"
    "• N × invariant-catcher shards + hunt cards → 03-findings-shard-<id>.md → merged → 03-findings-raw.md\n"
    "• missing-validation-reasoning → 04-validation-findings.md\n"
    "• protocol-reasoning-agent → 04a-reasoning-findings.md\n"
    "• orchestrator triages → 05-findings-triaged.md\n"
    "• poc-writing + issue-writer + sherlock/cantina → AUDIT-REPORT.md",
    sz=11, color="#546E7A", align="left")
E.append(t)

# ═══════════════════════════════════════════════════════════════════
# H : AGENT RESOURCES   y 3510 → 3750
# ═══════════════════════════════════════════════════════════════════
HY2 = 3510; HH2 = 240
rid, r = mk_rect(P, HY2, CW, HH2, stroke="#5D4037", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, HY2-13, 360, "⑦ AGENT RESOURCES & REFERENCES", bg="#5D4037"))

rw2 = (CW - 100) // 2
for i, rl in enumerate([
    "inter-agent-data-format.md — Data contracts between pipeline phases",
    "protocol-detection.md — Auto-classification decision tree for codebases",
    "audit-report-template.md — Final report structure + quality checklist",
    "orchestration-pipeline.md — 7-phase pipeline spec with error handling",
    "reasoning-skills.md — Core reasoning framework for deep analysis",
    "domain-decomposition.md — Domain decomposition strategy",
    "db-hunting-workflow.md — Hunt card workflow reference document",
    "poc-templates.md — Foundry / Hardhat PoC templates + harnesses",
]):
    col = i % 2
    row = i // 2
    E.extend(box(P+40+col*(rw2+20), HY2+35+row*50, rw2, 42, rl, bg="#EFEBE9", stroke="#8D6E63", sz=12))

# ═══════════════════════════════════════════════════════════════════
# I : DB ENTRY STRUCTURE   y 3790 → 4020
# ═══════════════════════════════════════════════════════════════════
IY2 = 3790; IH2 = 230
rid, r = mk_rect(P, IY2, CW, IH2, stroke="#006064", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, IY2-13, 380, "⑧ DB ENTRY STRUCTURE (TEMPLATE.md)", bg="#006064"))

ew2 = (CW - 80 - 60) // 4
for i, (lbl, bg) in enumerate([
    ("YAML Frontmatter\n\nprotocol · chain · category\nseverity · impact · tags\nexploitability · version",  "#E0F7FA"),
    ("Vulnerability Description\n\nRoot Cause analysis\nAttack Scenario steps\nVulnerable Pattern examples", "#B2EBF2"),
    ("Secure Implementation\n\nRecommended fix examples\nAlternative approaches\nBest practices",             "#80DEEA"),
    ("Detection & Search\n\nCode smell patterns\nAudit checklist items\nKeywords for vector search",          "#4DD0E1"),
]):
    ex = P+40 + i*(ew2+20)
    E.extend(box(ex, IY2+35, ew2, 155, lbl, bg=bg, stroke="#00838F", sz=13))
    if i > 0:
        E.extend(mk_arrow(ex-20, IY2+112, ex, IY2+112, "#00838F", sw=2))

# ═══════════════════════════════════════════════════════════════════
# J : LEGEND   y 4060 → 4200
# ═══════════════════════════════════════════════════════════════════
JY2 = 4060; JH2 = 140
rid, r = mk_rect(P, JY2, CW, JH2, stroke="#9E9E9E", dash=True, bg="transparent"); E.append(r)
E.extend(badge(P+5, JY2-13, 120, "LEGEND", bg="#616161"))

for i, (bg, lbl) in enumerate([
    ("#c8e6c9","Data Source"), ("#fff3e0","Processing Script"),
    ("#E8EAF6","AI Agent"),   ("#BBDEFB","DB Tier / Search"),
    ("#FFECB3","Pipeline Phase"), ("#FFCCBC","Triage / Output"),
    ("#EDE7F6","Fan-Out Component"), ("#EFEBE9","Resource File"),
]):
    col = i % 4
    row = i // 4
    E.extend(box(P+40+col*270, JY2+25+row*50, 230, 38, lbl, bg=bg, stroke="#BDBDBD", sz=13))


# ═══════════════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════════════
diagram = {
    "type": "excalidraw", "version": 2,
    "source": "https://excalidraw.com",
    "elements": E,
    "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
    "files": {}
}

out = "/home/calc1f4r/vuln-database/Architecture-Diagram.excalidraw"
with open(out, "w") as f:
    json.dump(diagram, f, indent=2)

print(f"✅ {out}")
print(f"   Elements: {len(E)}")
print(f"   Canvas: {W} × 4200 px")
print(f"   10 sections, ALL vertically stacked")
