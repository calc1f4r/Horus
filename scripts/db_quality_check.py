#!/usr/bin/env python3
"""DB Quality Monitor - Comprehensive health check script."""
import os, re, json, shutil, subprocess, sys
from collections import Counter
from pathlib import Path

from horus_retrieval.documents import DBDocument, parse_frontmatter_with_errors
from horus_retrieval.protocol_context import PROTOCOL_CONTEXTS

DB_ROOT = "DB/"
MANIFESTS_DIR = "DB/manifests/"
HUNTCARDS_DIR = "DB/manifests/huntcards/"
BUNDLES_DIR = "DB/manifests/bundles/"
IGNORED_ENTRY_DIRS = {"manifests", "graphify-out", "_drafts", "_telemetry"}
GENERATOR_PATH = Path("scripts/generate_manifests.py")
DB_GRAPH_PATH = Path("DB/graphify-out/graph.json")

REQUIRED_FM_FIELDS = ['protocol', 'category', 'vulnerability_type', 'attack_type', 'affected_component', 'severity', 'impact']
VALID_SEVERITY = ['critical', 'high', 'medium', 'low']

ROOT_CAUSE_RE = re.compile(
    r"(?:^|\n)\s*(?:[-*]\s*)?(?:#{2,6}\s*)?(?:\*\*)?"
    r"(?:Root\s*Cause(?:\s*(?:Statement|Categories|Analysis))?|Fundamental\s*Issue)"
    r"(?:\*\*)?\s*(?::|\n)",
    re.I,
)
VULNERABLE_EXAMPLE_RE = re.compile(
    r"(?:❌|"
    r"(?:^|\n)\s*#{2,6}\s*(?:Vulnerable\s+(?:Pattern\s+|Code\s+)?(?:Examples?|Patterns?)|"
    r"Vulnerability\s+Examples?|Real-World\s+Examples?)|"
    r"\bVULNERABLE\s*:|"
    r"//\s*VULNERABLE\b)",
    re.I,
)
SECURE_GUIDANCE_RE = re.compile(
    r"(?:✅|"
    r"(?:^|\n)\s*#{2,6}\s*(?:Secure\s+(?:Pattern|Code|Implementation)|"
    r"Recommended\s+Fix|Remediation|Mitigation|False\s+Positive(?:\s+Guards?|\s+Detail)?)|"
    r"\bSafe\s+if\s*:|"
    r"\bNot\s+this\s+bug\s+when\s*:)",
    re.I,
)
KEYWORDS_RE = re.compile(
    r"(?:^|\n)\s*#{2,6}\s*(?:Keywords|Code\s+Keywords|Search\s+Keywords)\b|"
    r"\bHigh-signal\s+code\s+keywords\s*:",
    re.I,
)

def iter_text_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from iter_text_values(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_text_values(nested)

def normalized_text(value):
    return re.sub(r"[^a-z0-9]+", "", str(value).lower())

def text_contains_focus(haystack, focus):
    return focus.lower() in haystack or normalized_text(focus) in normalized_text(haystack)

def score_graph_labels(nodes, query):
    terms = [term.lower() for term in query.split() if len(term) > 2]
    scored = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        label = str(node.get("label", "")).lower()
        source = str(node.get("source_file", "")).lower()
        score = sum(1 for term in terms if term in label)
        score += sum(0.5 for term in terms if term in source)
        if score > 0:
            scored.append((score, label))
    return [label for _score, label in sorted(scored, reverse=True)]

def validate_partition_bundle_data(bundle, source="<bundle>"):
    """Validate a generated protocol shard bundle."""
    issues = []

    if not isinstance(bundle, dict):
        return [("CRITICAL", f"{source}: bundle is not a JSON object")]

    meta = bundle.get("meta", {})
    shards = bundle.get("shards", [])
    if not isinstance(meta, dict):
        issues.append(("CRITICAL", f"{source}: meta is not an object"))
        meta = {}
    if not isinstance(shards, list):
        issues.append(("CRITICAL", f"{source}: shards is not a list"))
        return issues

    critical_ids = meta.get("criticalCardIds", [])
    if not isinstance(critical_ids, list):
        issues.append(("CRITICAL", f"{source}: meta.criticalCardIds is not a list"))
        critical_ids = []
    critical_set = set(critical_ids)

    if meta.get("criticalCards") != len(critical_ids):
        issues.append((
            "CRITICAL",
            f"{source}: meta.criticalCards={meta.get('criticalCards')} but criticalCardIds has {len(critical_ids)}",
        ))
    if meta.get("shardCount") != len(shards):
        issues.append((
            "CRITICAL",
            f"{source}: meta.shardCount={meta.get('shardCount')} but shards has {len(shards)}",
        ))
    if meta.get("totalCards", 0) > 0 and not shards:
        issues.append(("CRITICAL", f"{source}: totalCards > 0 but no shards are actionable"))

    regular_ids = []
    duplicate_regular_ids = []
    seen_regular = set()

    for idx, shard in enumerate(shards):
        shard_label = shard.get("id", f"shard[{idx}]") if isinstance(shard, dict) else f"shard[{idx}]"
        if not isinstance(shard, dict):
            issues.append(("CRITICAL", f"{source}: {shard_label} is not an object"))
            continue

        card_ids = shard.get("cardIds", [])
        shard_critical_ids = shard.get("criticalCardIds", [])
        if not isinstance(card_ids, list):
            issues.append(("CRITICAL", f"{source}: {shard_label}.cardIds is not a list"))
            card_ids = []
        if not isinstance(shard_critical_ids, list):
            issues.append(("CRITICAL", f"{source}: {shard_label}.criticalCardIds is not a list"))
            shard_critical_ids = []

        if set(shard_critical_ids) != critical_set:
            issues.append(("CRITICAL", f"{source}: {shard_label} does not carry the full criticalCardIds set"))

        critical_only = bool(shard.get("criticalOnly"))
        if not critical_only:
            overlap = sorted(set(card_ids) & critical_set)
            if overlap:
                issues.append(("CRITICAL", f"{source}: {shard_label}.cardIds includes critical IDs: {overlap[:5]}"))

        expected_regular_count = len(card_ids)
        if shard.get("cardCount") != expected_regular_count:
            issues.append((
                "CRITICAL",
                f"{source}: {shard_label}.cardCount={shard.get('cardCount')} but cardIds has {expected_regular_count}",
            ))
        if shard.get("regularCardCount", expected_regular_count) != expected_regular_count:
            issues.append((
                "CRITICAL",
                f"{source}: {shard_label}.regularCardCount={shard.get('regularCardCount')} but cardIds has {expected_regular_count}",
            ))
        if shard.get("criticalCardCount", len(critical_ids)) != len(critical_ids):
            issues.append((
                "CRITICAL",
                f"{source}: {shard_label}.criticalCardCount={shard.get('criticalCardCount')} but meta has {len(critical_ids)} critical IDs",
            ))
        if shard.get("effectiveCardCount", expected_regular_count + len(critical_ids)) != expected_regular_count + len(critical_ids):
            issues.append((
                "CRITICAL",
                f"{source}: {shard_label}.effectiveCardCount={shard.get('effectiveCardCount')} but expected {expected_regular_count + len(critical_ids)}",
            ))

        for card_id in card_ids:
            if card_id in critical_set and critical_only:
                continue
            if card_id in seen_regular:
                duplicate_regular_ids.append(card_id)
            seen_regular.add(card_id)
            regular_ids.append(card_id)

    if duplicate_regular_ids:
        issues.append(("CRITICAL", f"{source}: duplicate regular card IDs across shards: {sorted(set(duplicate_regular_ids))[:10]}"))

    total_unique = len((set(regular_ids) - critical_set) | critical_set)
    if meta.get("totalCards") != total_unique:
        issues.append((
            "CRITICAL",
            f"{source}: meta.totalCards={meta.get('totalCards')} but regular+critical unique cards total {total_unique}",
        ))

    return issues

def find_entries():
    result = []
    for root, dirs, fnames in os.walk(DB_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_ENTRY_DIRS]
        for fn in fnames:
            if fn.endswith('.md') and fn not in ('README.md', 'SEARCH_GUIDE.md', 'ARTIFACT_INDEX.md'):
                result.append(os.path.join(root, fn))
    result.sort()
    return result

def parse_frontmatter(filepath):
    document = DBDocument.from_path(Path(filepath))
    content = document.content
    lines = content.split('\n')
    total_lines = len(lines)
    fm, fm_errors = parse_frontmatter_with_errors(content)
    fm_for_checks = fm or {}
    
    has_vuln_ex = bool(VULNERABLE_EXAMPLE_RE.search(content))
    has_secure = bool(SECURE_GUIDANCE_RE.search(content))
    has_root_cause = bool(ROOT_CAUSE_RE.search(content))
    has_keywords = bool(
        KEYWORDS_RE.search(content)
        or fm_for_checks.get("code_keywords")
        or fm_for_checks.get("search_keywords")
        or fm_for_checks.get("grep_keywords")
    )
    has_code_blocks = '```' in content
    has_detection = bool(re.search(r'#{2,4}\s*(Detection\s*Pattern|Audit\s*Checklist)', content, re.I))
    has_reference = bool(re.search(r'#{1,3}\s*Reference', content, re.I))
    
    return {
        'file': filepath,
        'lines': total_lines,
        'has_fm': fm is not None,
        'fm': fm,
        'fm_errors': fm_errors,
        'has_vuln_ex': has_vuln_ex, 'has_secure': has_secure,
        'has_root_cause': has_root_cause, 'has_keywords': has_keywords,
        'has_code_blocks': has_code_blocks, 'has_detection': has_detection,
        'has_reference': has_reference,
    }

def skill1():
    """Entry compliance check."""
    print("=" * 60)
    print("SKILL 1: ENTRY COMPLIANCE")
    print("=" * 60)
    files = find_entries()
    total = len(files)
    print(f"Total entries: {total}")
    
    has_fm = 0
    full_compliance = 0
    fm_field_coverage = {f: 0 for f in REQUIRED_FM_FIELDS}
    no_fm_files = []
    stubs = []
    no_code = []
    severity_issues = []
    section_missing = Counter()
    missing_files = []
    
    for fp in files:
        r = parse_frontmatter(fp)
        if r['has_fm']:
            has_fm += 1
            fm = r['fm'] or {}
            for field in REQUIRED_FM_FIELDS:
                if fm.get(field):
                    fm_field_coverage[field] += 1
            sev = str(fm.get('severity', '')).lower()
            if sev and sev not in VALID_SEVERITY:
                severity_issues.append((fp, sev))
        else:
            no_fm_files.append(fp)
        
        if r['lines'] < 50:
            stubs.append((fp, r['lines']))
        if not r['has_code_blocks']:
            no_code.append(fp)
        
        issues = []
        if not r['has_root_cause']: issues.append('no_root_cause')
        if not r['has_vuln_ex']: issues.append('no_vuln_ex')
        if not r['has_secure']: issues.append('no_secure_fix')
        if not r['has_keywords']: issues.append('no_keywords')
        if not r['has_detection']: issues.append('no_detection')
        
        for i in issues:
            section_missing[i] += 1
        
        if issues:
            missing_files.append((fp, issues))
        
        all_ok = r['has_fm'] and not issues and r['has_code_blocks'] and r['lines'] >= 50
        if all_ok:
            full_compliance += 1
    
    print(f"Has frontmatter: {has_fm}/{total} ({100*has_fm//total}%)")
    print(f"Full compliance: {full_compliance}/{total} ({100*full_compliance//total}%)")
    print(f"\nFM field coverage:")
    for f, c in fm_field_coverage.items():
        pct = 100*c//max(has_fm,1)
        status = "✅" if pct >= 80 else "⚠️" if pct >= 50 else "🔴"
        print(f"  {status} {f}: {c}/{has_fm} ({pct}%)")
    
    if no_fm_files:
        print(f"\n🔴 NO FRONTMATTER ({len(no_fm_files)} files):")
        for f in no_fm_files:
            print(f"  - {f}")
    
    if stubs:
        print(f"\n⚠️ STUBS <50 lines ({len(stubs)} files):")
        for f, l in stubs:
            print(f"  - {f} ({l} lines)")
    
    if no_code:
        print(f"\n⚠️ NO CODE BLOCKS ({len(no_code)} files):")
        for f in no_code:
            print(f"  - {f}")
    
    if severity_issues:
        print(f"\n🔴 INVALID SEVERITY ({len(severity_issues)}):")
        for f, s in severity_issues:
            print(f"  - {f}: \"{s}\"")
    
    print(f"\nSection missing counts:")
    for s, c in section_missing.most_common():
        print(f"  {s}: {c}/{total} ({100*c//total}%)")
    
    return {
        'total': total, 'has_fm': has_fm, 'full_compliance': full_compliance,
        'no_fm_files': no_fm_files, 'stubs': stubs, 'no_code': no_code,
        'severity_issues': severity_issues, 'section_missing': dict(section_missing),
        'missing_files': missing_files, 'fm_field_coverage': fm_field_coverage,
    }

def skill2():
    """Manifest integrity."""
    print("\n" + "=" * 60)
    print("SKILL 2: MANIFEST INTEGRITY")
    print("=" * 60)
    
    issues = []
    
    print("Validating generated manifest JSON...")
    
    # Load all manifests and validate
    manifest_files = [f for f in os.listdir(MANIFESTS_DIR) if f.endswith('.json') and f != 'keywords.json']
    manifest_files = [f for f in manifest_files if os.path.isfile(os.path.join(MANIFESTS_DIR, f))]
    
    for mf in sorted(manifest_files):
        path = os.path.join(MANIFESTS_DIR, mf)
        try:
            with open(path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            issues.append(('CRITICAL', f'{mf}: Invalid JSON: {e}'))
            continue
        
        meta = data.get('meta', {})
        files_arr = data.get('files', [])
        
        total_patterns = sum(len(fe.get('patterns', [])) for fe in files_arr)
        claimed = meta.get('totalPatterns', 0)
        if total_patterns != claimed:
            issues.append(('WARNING', f'{mf}: meta.totalPatterns={claimed} but actual={total_patterns}'))
        
        claimed_fc = meta.get('fileCount', 0)
        actual_fc = len(files_arr)
        if claimed_fc != actual_fc:
            issues.append(('WARNING', f'{mf}: meta.fileCount={claimed_fc} but actual={actual_fc}'))
        
        # Check files exist and pattern validity
        pattern_ids = set()
        for fe in files_arr:
            fpath = fe.get('file', '')
            if not os.path.isfile(fpath):
                issues.append(('CRITICAL', f'{mf}: references non-existent file: {fpath}'))
            
            for p in fe.get('patterns', []):
                pid = p.get('id', '')
                if pid in pattern_ids:
                    issues.append(('WARNING', f'{mf}: duplicate pattern ID: {pid}'))
                pattern_ids.add(pid)
                
                if not p.get('title'):
                    issues.append(('WARNING', f'{mf}: pattern {pid} has empty title'))
                
                ls = p.get('lineStart', 0)
                le = p.get('lineEnd', 0)
                if ls >= le:
                    issues.append(('CRITICAL', f'{mf}: pattern {pid} has lineStart({ls}) >= lineEnd({le})'))
    
    for level, msg in issues:
        icon = "🔴" if level == 'CRITICAL' else "⚠️"
        print(f"  {icon} {msg}")
    
    if not issues:
        print("  ✅ All manifests valid")
    
    return issues

def skill3():
    """Hunt card consistency."""
    print("\n" + "=" * 60)
    print("SKILL 3: HUNT CARD CONSISTENCY")  
    print("=" * 60)
    
    issues = []
    
    with open('DB/index.json') as f:
        index = json.load(f)
    
    # Load all-huntcards
    all_hc_path = 'DB/manifests/huntcards/all-huntcards.json'
    if not os.path.isfile(all_hc_path):
        issues.append(('CRITICAL', 'all-huntcards.json missing'))
        print("  🔴 all-huntcards.json missing!")
        return issues
    
    with open(all_hc_path) as f:
        all_cards_data = json.load(f)
    all_cards = all_cards_data.get('cards', []) if isinstance(all_cards_data, dict) else all_cards_data
    
    all_card_count = len(all_cards)
    claimed_total = index.get('huntcards', {}).get('totalCards', 0)
    if all_card_count != claimed_total:
        issues.append(('WARNING', f'index.json claims totalCards={claimed_total} but all-huntcards has {all_card_count}'))
    
    # Per-manifest hunt card checks
    per_manifest_total = 0
    per_manifest_ids = set()
    
    for mname, minfo in index.get('huntcards', {}).get('perManifest', {}).items():
        hc_file = minfo.get('file', '')
        claimed_cards = minfo.get('totalCards', 0)
        
        if not os.path.isfile(hc_file):
            issues.append(('CRITICAL', f'Hunt card file missing: {hc_file}'))
            continue
        
        with open(hc_file) as f:
            cards_data = json.load(f)
        meta = cards_data.get('meta', {}) if isinstance(cards_data, dict) else {}
        cards = cards_data.get('cards', []) if isinstance(cards_data, dict) else cards_data
        
        actual_cards = len(cards)
        per_manifest_total += actual_cards
        
        if actual_cards != claimed_cards:
            issues.append(('WARNING', f'{mname}: index claims {claimed_cards} cards but file has {actual_cards}'))
        meta_total = meta.get('totalCards')
        if meta_total is not None and meta_total != actual_cards:
            issues.append(('WARNING', f'{mname}: huntcard meta.totalCards={meta_total} but file has {actual_cards}'))
        
        # Check card quality
        unknown_severity = 0
        for card in cards:
            cid = card.get('id', '')
            per_manifest_ids.add(cid)
            
            if card.get('severity') not in {'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'}:
                unknown_severity += 1
            if not card.get('grep'):
                issues.append(('WARNING', f'{mname}: card {cid} has empty grep'))
            else:
                try:
                    re.compile(card.get('grep', ''))
                except re.error as exc:
                    issues.append(('CRITICAL', f'{mname}: card {cid} has invalid grep regex: {exc}'))
            if not card.get('ref'):
                issues.append(('CRITICAL', f'{mname}: card {cid} has no ref'))
            elif not os.path.isfile(card.get('ref', '')):
                issues.append(('CRITICAL', f'{mname}: card {cid} ref points to non-existent: {card.get("ref")}'))
            
            lines = card.get('lines', [])
            if len(lines) == 2 and lines[0] >= lines[1]:
                issues.append(('CRITICAL', f'{mname}: card {cid} lines[0]({lines[0]}) >= lines[1]({lines[1]})'))
            if card.get('neverPrune') and card.get('severity') != 'CRITICAL':
                issues.append(('WARNING', f'{mname}: card {cid} is neverPrune but severity={card.get("severity")}'))

        if unknown_severity:
            issues.append(('WARNING', f'{mname}: {unknown_severity} cards have UNKNOWN/untagged severity'))
    
    if per_manifest_total != all_card_count:
        issues.append(('WARNING', f'Sum of per-manifest cards ({per_manifest_total}) != all-huntcards ({all_card_count})'))
    
    # Check all_cards IDs match
    all_ids = {c.get('id', '') for c in all_cards}
    missing_from_all = per_manifest_ids - all_ids
    extra_in_all = all_ids - per_manifest_ids
    if missing_from_all:
        issues.append(('WARNING', f'{len(missing_from_all)} cards in per-manifest files but missing from all-huntcards'))
    if extra_in_all:
        issues.append(('WARNING', f'{len(extra_in_all)} cards in all-huntcards but missing from per-manifest files'))
    
    # neverPrune audit
    never_prune = [c for c in all_cards if c.get('neverPrune')]
    print(f"  neverPrune cards: {len(never_prune)}")
    
    for level, msg in issues:
        icon = "🔴" if level == 'CRITICAL' else "⚠️"
        print(f"  {icon} {msg}")
    
    if not issues:
        print("  ✅ All hunt cards consistent")
    
    return issues

def skill4():
    """Router & index integrity."""
    print("\n" + "=" * 60)
    print("SKILL 4: ROUTER & INDEX INTEGRITY")
    print("=" * 60)
    
    issues = []
    
    with open('DB/index.json') as f:
        index = json.load(f)
    
    # 4A: Manifest listings
    for mname, minfo in index.get('manifests', {}).items():
        mfile = minfo.get('file', '')
        if not os.path.isfile(mfile):
            issues.append(('CRITICAL', f'Manifest {mname}: file {mfile} does not exist'))
            continue
        
        with open(mfile) as f:
            manifest = json.load(f)
        meta = manifest.get('meta', {})
        
        idx_fc = minfo.get('fileCount', 0)
        idx_tp = minfo.get('totalPatterns', 0)
        real_fc = meta.get('fileCount', 0)
        real_tp = meta.get('totalPatterns', 0)
        
        if idx_fc != real_fc:
            issues.append(('WARNING', f'{mname}: index fileCount={idx_fc} vs manifest={real_fc}'))
        if idx_tp != real_tp:
            issues.append(('WARNING', f'{mname}: index totalPatterns={idx_tp} vs manifest={real_tp}'))
    
    # Check for orphan manifests (json files not in index)
    on_disk = set()
    for f in os.listdir(MANIFESTS_DIR):
        if f.endswith('.json') and f != 'keywords.json' and os.path.isfile(os.path.join(MANIFESTS_DIR, f)):
            on_disk.add(f.replace('.json', ''))
    in_index = set(index.get('manifests', {}).keys())
    orphan_manifests = on_disk - in_index
    if orphan_manifests:
        issues.append(('WARNING', f'Orphan manifest files not in index: {orphan_manifests}'))
    
    # 4B: protocolContext
    required_contexts = list(PROTOCOL_CONTEXTS)
    
    present_contexts = list(index.get('protocolContext', {}).get('mappings', {}).keys())
    for ctx in required_contexts:
        if ctx not in present_contexts:
            issues.append(('WARNING', f'Missing protocolContext: {ctx}'))
    
    for ctx, cinfo in index.get('protocolContext', {}).get('mappings', {}).items():
        for m in cinfo.get('manifests', []):
            if m not in in_index:
                issues.append(('CRITICAL', f'protocolContext {ctx} references non-existent manifest: {m}'))

        haystacks = []
        for m in cinfo.get('manifests', []):
            if m not in index.get('manifests', {}):
                continue
            with open(index['manifests'][m]['file']) as f:
                manifest = json.load(f)
            for fe in manifest.get('files', []):
                haystacks.append(' '.join(iter_text_values(fe.get('frontmatter', {}))).lower())
                for pattern in fe.get('patterns', []):
                    fragments = [pattern.get('title', ''), pattern.get('rootCause', '') or '']
                    fragments.extend(pattern.get('codeKeywords', []))
                    fragments.extend(pattern.get('searchKeywords', []))
                    fragments.extend(iter_text_values(pattern.get('graphHints', {})))
                    fragments.extend(iter_text_values(pattern.get('reportEvidence', {})))
                    for subsection in pattern.get('subsections') or []:
                        fragments.append(subsection.get('title', ''))
                        fragments.extend(subsection.get('searchKeywords') or [])
                        fragments.extend(iter_text_values(subsection.get('graphHints', {})))
                    haystacks.append(' '.join(str(fragment) for fragment in fragments if fragment).lower())

        for focus in cinfo.get('focusPatterns', []):
            if haystacks and not any(text_contains_focus(haystack, focus) for haystack in haystacks):
                issues.append(('WARNING', f'protocolContext {ctx} focusPattern "{focus}" is not discoverable from its manifests'))
    
    # 4C: Keyword index
    kw_file = 'DB/manifests/keywords.json'
    if os.path.isfile(kw_file):
        with open(kw_file) as f:
            kw_data = json.load(f)
        # keywords.json has {"description":..., "totalKeywords":N, "mappings":{...}}
        mappings = kw_data.get('mappings', kw_data)
        if isinstance(mappings, dict) and 'mappings' not in mappings:
            actual_kw_count = len(mappings)
        else:
            actual_kw_count = len(mappings)
        claimed_kw = index.get('keywordIndex', {}).get('totalKeywords', 0)
        internal_claimed = kw_data.get('totalKeywords', 0)
        if actual_kw_count != claimed_kw:
            issues.append(('WARNING', f'Keyword count: index claims {claimed_kw}, keywords.json has {actual_kw_count}'))
        if actual_kw_count != internal_claimed:
            issues.append(('WARNING', f'keywords.json internal: claims {internal_claimed}, actual {actual_kw_count}'))
        
        empty_kw = [k for k, v in mappings.items() if not v]
        if empty_kw:
            issues.append(('WARNING', f'{len(empty_kw)} keywords map to empty manifest lists'))
    else:
        issues.append(('CRITICAL', 'keywords.json missing'))
    
    # 4D: huntcard section
    hc = index.get('huntcards', {})
    all_path = hc.get('allInOne', '')
    if not os.path.isfile(all_path):
        issues.append(('CRITICAL', f'allInOne huntcard path does not exist: {all_path}'))
    
    for level, msg in issues:
        icon = "🔴" if level == 'CRITICAL' else "⚠️"
        print(f"  {icon} {msg}")
    
    if not issues:
        print("  ✅ Router & index OK")
    
    return issues

def skill5():
    """Pipeline script health."""
    print("\n" + "=" * 60)
    print("SKILL 5: PIPELINE SCRIPT HEALTH")
    print("=" * 60)
    
    issues = []
    scripts_to_check = ['scripts/grep_prune.py', 'scripts/partition_shards.py', 'scripts/merge_shard_findings.py']
    
    for s in scripts_to_check:
        if os.path.isfile(s):
            print(f"  ✅ {s} exists")
        else:
            issues.append(('WARNING', f'{s} does not exist'))
            print(f"  ⚠️ {s} missing")
    
    if GENERATOR_PATH.is_file():
        print(f"  ✅ {GENERATOR_PATH} exists")
    else:
        issues.append(('CRITICAL', f'{GENERATOR_PATH} missing'))
    
    return issues

def skill6_sample():
    """Line-range accuracy spot check."""
    print("\n" + "=" * 60)
    print("SKILL 6: CONTEXT DELIVERY (sampled)")
    print("=" * 60)
    
    issues = []
    checked = 0
    exact = 0
    wrong = 0
    overflow = 0
    
    manifest_files = [f for f in os.listdir(MANIFESTS_DIR) if f.endswith('.json') and f != 'keywords.json']
    manifest_files = [f for f in manifest_files if os.path.isfile(os.path.join(MANIFESTS_DIR, f))]
    
    for mf in sorted(manifest_files):
        path = os.path.join(MANIFESTS_DIR, mf)
        with open(path) as f:
            data = json.load(f)
        
        count = 0
        for fe in data.get('files', []):
            fpath = fe.get('file', '')
            if not os.path.isfile(fpath):
                continue
            
            with open(fpath, 'r', encoding='utf-8', errors='replace') as ff:
                file_lines = ff.readlines()
            total_file_lines = len(file_lines)
            
            for p in fe.get('patterns', []):
                sev = p.get('severity', [])
                is_high = any(s in ('HIGH', 'CRITICAL') for s in sev) if isinstance(sev, list) else False
                
                # Check all HIGH/CRITICAL, sample 3 per manifest for others
                if not is_high and count >= 3:
                    continue
                count += 1
                checked += 1
                
                pid = p.get('id', '')
                ls = p.get('lineStart', 1)
                le = p.get('lineEnd', 1)
                title = p.get('title', '')
                
                if le > total_file_lines:
                    issues.append(('CRITICAL', f'{mf}/{pid}: lineEnd({le}) > file length ({total_file_lines}) in {fpath}'))
                    overflow += 1
                    continue
                
                if ls < 1 or ls > total_file_lines:
                    issues.append(('CRITICAL', f'{mf}/{pid}: lineStart({ls}) out of range for {fpath} ({total_file_lines} lines)'))
                    wrong += 1
                    continue
                
                first_line = file_lines[ls - 1].strip() if ls <= total_file_lines else ''
                if first_line.startswith('#'):
                    exact += 1
                else:
                    # Check nearby lines for heading
                    found = False
                    for offset in range(-2, 3):
                        idx = ls - 1 + offset
                        if 0 <= idx < total_file_lines and file_lines[idx].strip().startswith('#'):
                            found = True
                            break
                    if found:
                        issues.append(('INFO', f'{mf}/{pid}: lineStart heading off by a few lines'))
                        exact += 1  # close enough
                    else:
                        issues.append(('WARNING', f'{mf}/{pid}: lineStart({ls}) does not point to heading in {fpath}'))
                        wrong += 1
    
    accuracy = 100 * exact // max(checked, 1)
    print(f"  Checked: {checked} patterns")
    print(f"  Exact/close match: {exact} ({accuracy}%)")
    print(f"  Wrong content: {wrong}")
    print(f"  Overflow: {overflow}")
    
    for level, msg in issues:
        if level in ('CRITICAL', 'WARNING'):
            icon = "🔴" if level == 'CRITICAL' else "⚠️"
            print(f"  {icon} {msg}")
    
    return issues

def skill7():
    """Coverage & overlap."""
    print("\n" + "=" * 60)
    print("SKILL 7: COVERAGE & OVERLAP")
    print("=" * 60)
    
    issues = []
    
    # 7B: Orphaned file detection
    all_md = set(find_entries())
    
    manifest_referenced = set()
    manifest_files = [f for f in os.listdir(MANIFESTS_DIR) if f.endswith('.json') and f != 'keywords.json']
    manifest_files = [f for f in manifest_files if os.path.isfile(os.path.join(MANIFESTS_DIR, f))]
    
    for mf in manifest_files:
        path = os.path.join(MANIFESTS_DIR, mf)
        with open(path) as f:
            data = json.load(f)
        for fe in data.get('files', []):
            manifest_referenced.add(fe.get('file', ''))
    
    orphaned = all_md - manifest_referenced
    if orphaned:
        issues.append(('CRITICAL', f'{len(orphaned)} orphaned files not in any manifest'))
        print(f"  🔴 Orphaned files ({len(orphaned)}):")
        for f in sorted(orphaned):
            print(f"    - {f}")
    else:
        print("  ✅ No orphaned files")
    
    # 7D: Severity distribution
    severity_counter = Counter()
    total_patterns = 0
    for mf in manifest_files:
        path = os.path.join(MANIFESTS_DIR, mf)
        with open(path) as f:
            data = json.load(f)
        for fe in data.get('files', []):
            for p in fe.get('patterns', []):
                total_patterns += 1
                sevs = p.get('severity', [])
                if isinstance(sevs, list):
                    for s in sevs:
                        severity_counter[s.upper() if isinstance(s, str) else str(s)] += 1
                    if not sevs:
                        severity_counter['UNTAGGED'] += 1
                else:
                    severity_counter[str(sevs).upper()] += 1
    
    print(f"\n  Severity distribution ({total_patterns} total patterns):")
    for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNTAGGED']:
        c = severity_counter.get(sev, 0)
        pct = 100 * c // max(total_patterns, 1)
        print(f"    {sev}: {c} ({pct}%)")
    
    return issues

def skill8():
    """Graphify artifact health."""
    print("\n" + "=" * 60)
    print("SKILL 8: GRAPHIFY ARTIFACT HEALTH")
    print("=" * 60)

    issues = []

    if not DB_GRAPH_PATH.is_file():
        issues.append(("WARNING", f"DB graph missing: {DB_GRAPH_PATH}"))
        print(f"  ⚠️ DB graph missing: {DB_GRAPH_PATH}")
        return issues

    try:
        with DB_GRAPH_PATH.open("r", encoding="utf-8") as f:
            graph = json.load(f)
    except json.JSONDecodeError as exc:
        issues.append(("CRITICAL", f"{DB_GRAPH_PATH}: invalid JSON: {exc}"))
        graph = None

    if isinstance(graph, dict):
        nodes = graph.get("nodes")
        edges = graph.get("links") if "links" in graph else graph.get("edges")

        if not isinstance(nodes, list) or not nodes:
            issues.append(("CRITICAL", f"{DB_GRAPH_PATH}: missing or empty nodes list"))
            nodes = []
        if not isinstance(edges, list) or not edges:
            issues.append(("CRITICAL", f"{DB_GRAPH_PATH}: missing or empty links/edges list"))
            edges = []

        node_ids = {node.get("id") for node in nodes if isinstance(node, dict)}
        missing_endpoints = 0
        for edge in edges:
            if not isinstance(edge, dict):
                missing_endpoints += 1
                continue
            if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
                missing_endpoints += 1

        if missing_endpoints:
            issues.append(("CRITICAL", f"{DB_GRAPH_PATH}: {missing_endpoints} edges have missing endpoints"))

        node_kinds = {node.get("node_kind") for node in nodes if isinstance(node, dict)}
        required_kinds = {
            "HuntCard",
            "DBEntry",
            "Category",
            "Manifest",
            "ProtocolContext",
            "RootCauseFamily",
            "AttackType",
            "AffectedComponent",
            "GraphHint",
            "ReportEvidence",
            "Severity",
        }
        missing_kinds = sorted(required_kinds - node_kinds)
        if missing_kinds:
            issues.append(("CRITICAL", f"{DB_GRAPH_PATH}: missing semantic node kinds: {missing_kinds}"))

        relation_counts = Counter(edge.get("relation") for edge in edges if isinstance(edge, dict))
        if relation_counts.get("related_variant", 0) == 0:
            issues.append(("CRITICAL", f"{DB_GRAPH_PATH}: missing related_variant edges"))
        if relation_counts.get("has_graph_hint", 0) == 0:
            issues.append(("CRITICAL", f"{DB_GRAPH_PATH}: missing graph hint edges"))
        if relation_counts.get("has_root_cause_family", 0) == 0:
            issues.append(("CRITICAL", f"{DB_GRAPH_PATH}: missing root-cause-family edges"))

        labels = {str(node.get("label", "")).lower() for node in nodes if isinstance(node, dict)}
        expected_label_fragments = [
            "flash loan oracle manipulation",
            "oracle stale price",
            "cross_chain_bridge",
        ]
        for expected in expected_label_fragments:
            if not any(expected in label for label in labels):
                issues.append(("WARNING", f"{DB_GRAPH_PATH}: expected graph label not found: {expected}"))

        relevance_checks = {
            "oracle flash loan": "flash loan oracle manipulation",
            "erc4626 first depositor": "first depositor",
            "cross chain replay": "cross-chain replay",
        }
        for query, expected in relevance_checks.items():
            ranked_labels = score_graph_labels(nodes, query)[:10]
            if not any(expected in label for label in ranked_labels):
                issues.append(("WARNING", f"{DB_GRAPH_PATH}: query '{query}' did not rank '{expected}' in top 10 labels"))

        if not any(level == "CRITICAL" for level, _ in issues):
            print(f"  ✅ Graph JSON shape OK ({len(nodes)} nodes, {len(edges)} edges)")
            print(
                "  ✅ Semantic graph OK "
                f"({len(node_kinds)} node kinds, {relation_counts.get('related_variant', 0)} related_variant edges)"
            )

    graphify_bin = shutil.which("graphify")
    if graphify_bin and not any(level == "CRITICAL" for level, _ in issues):
        try:
            result = subprocess.run(
                [
                    graphify_bin,
                    "query",
                    "oracle staleness",
                    "--graph",
                    str(DB_GRAPH_PATH),
                    "--budget",
                    "200",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20,
                check=False,
            )
            if result.returncode != 0:
                detail = result.stderr.strip() or f"exit code {result.returncode}"
                issues.append(("CRITICAL", f"graphify query failed for {DB_GRAPH_PATH}: {detail}"))
            else:
                print("  ✅ graphify query smoke test OK")
        except subprocess.TimeoutExpired:
            issues.append(("WARNING", f"graphify query timed out for {DB_GRAPH_PATH}"))
    elif not graphify_bin:
        issues.append(("WARNING", "graphify CLI not found; skipped query smoke test"))

    for level, msg in issues:
        icon = "🔴" if level == "CRITICAL" else "⚠️"
        print(f"  {icon} {msg}")

    if not issues:
        print("  ✅ Graphify artifacts OK")

    return issues

def skill9():
    """Partition bundle health."""
    print("\n" + "=" * 60)
    print("SKILL 9: PARTITION BUNDLE HEALTH")
    print("=" * 60)

    issues = []
    bundles_dir = Path(BUNDLES_DIR)
    if not bundles_dir.is_dir():
        issues.append(("WARNING", f"Partition bundles directory missing: {BUNDLES_DIR}"))
    else:
        bundle_files = sorted(bundles_dir.glob("*-shards.json"))
        if not bundle_files:
            issues.append(("WARNING", f"No partition bundle files found in {BUNDLES_DIR}"))

        for bundle_file in bundle_files:
            try:
                with bundle_file.open("r", encoding="utf-8") as f:
                    bundle = json.load(f)
            except json.JSONDecodeError as exc:
                issues.append(("CRITICAL", f"{bundle_file}: invalid JSON: {exc}"))
                continue
            issues.extend(validate_partition_bundle_data(bundle, str(bundle_file)))

        if not any(level == "CRITICAL" for level, _ in issues):
            print(f"  ✅ Partition bundles OK ({len(bundle_files)} bundles)")

    for level, msg in issues:
        icon = "🔴" if level == "CRITICAL" else "⚠️"
        print(f"  {icon} {msg}")

    return issues

if __name__ == '__main__':
    s1 = skill1()
    s2 = skill2()
    s3 = skill3()
    s4 = skill4()
    s5 = skill5()
    s6 = skill6_sample()
    s7 = skill7()
    s8 = skill8()
    s9 = skill9()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_critical = []
    all_warnings = []
    for results in [s2, s3, s4, s5, s6, s7, s8, s9]:
        if isinstance(results, list):
            for level, msg in results:
                if level == 'CRITICAL':
                    all_critical.append(msg)
                elif level == 'WARNING':
                    all_warnings.append(msg)
    
    if s1.get('no_fm_files'):
        all_warnings.append(f"{len(s1['no_fm_files'])} files missing frontmatter")
    if s1.get('severity_issues'):
        all_warnings.append(f"{len(s1['severity_issues'])} files with invalid severity")
    
    print(f"Total entries: {s1['total']}")
    print(f"Frontmatter coverage: {s1['has_fm']}/{s1['total']} ({100*s1['has_fm']//s1['total']}%)")
    print(f"Full compliance: {s1['full_compliance']}/{s1['total']} ({100*s1['full_compliance']//s1['total']}%)")
    print(f"Critical issues: {len(all_critical)}")
    print(f"Warnings: {len(all_warnings)}")
    
    overall = "HEALTHY"
    if all_critical:
        overall = "BROKEN"
    elif len(all_warnings) > 3:
        overall = "DEGRADED"
    
    print(f"Overall: {overall}")
