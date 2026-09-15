---
# Core Classification
protocol: Sei DB
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47499
audit_firm: OtterSec
contest_link: https://www.sei.io/
source_link: https://www.sei.io/
github_link: https://github.com/sei-protocol/sei-db

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Naoya Okanami
  - James
  - Tuyết
---

## Vulnerability Title

LoadVersion Failure On History Queries

### Overview

A bug has been reported in the scStore function of the DB instance. The issue arises when the DB options do not include the Readonly flag, causing the LockFile to be locked by the DB instance opened for cms. This results in the LoadVersion function always failing alongside the queries. To fix this issue, the scStore should be loaded in ReadOnly mode for queries. The bug has been fixed in P.R. #62 and P.R. #482.

### Original Finding Content

## Query Attempt to Load a New Instance of scStore for Historical Queries that Require a Proof

> _store v2/rootmulti/store.gogo

```go
func (rs *Store) Query(req abci.RequestQuery) abci.ResponseQuery {
    [...]
    if !req.Prove && version < rs.lastCommitInfo.Version && rs.ssStore != nil {
        [...]
    } else if version < rs.lastCommitInfo.Version {
        // Serve abci query from historical sc store if proofs needed
        scStore, err := rs.scStore.LoadVersion(version, true)
        [...]
    } else {
        [...]
    }
}
```

When DB options do not include the Readonly flag, `OpenDB` will attempt to lock `LockFile`.

> _sc/memiavl/db.gogo

```go
func OpenDB(logger logger.Logger, targetVersion int64, opts Options) (*DB, error) {
    [...]
    if !opts.ReadOnly {
        fileLock, err = LockFile(filepath.Join(opts.Dir, LockFileName))
        if err != nil {
            return nil, fmt.Errorf("fail to lock db: %w", err)
        }
        [...]
    }
    [...]
}
```

The issue arises from `rs.scStore` defaulting to writable mode, and the `LockFile` will already be locked by the `DB` instance opened for CMS. This results in `LoadVersion` always failing alongside the queries.

## Remediation

Load `scStore` in ReadOnly mode for Query.

---

© 2024 Otter Audits LLC. All Rights Reserved. 13/24

## Sei DBAudit 04 — Vulnerabilities

## Patch

Fixed in PR #62 and PR #482.

---

© 2024 Otter Audits LLC. All Rights Reserved. 14/24

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sei DB |
| Report Date | N/A |
| Finders | Naoya Okanami, James, Tuyết |

### Source Links

- **Source**: https://www.sei.io/
- **GitHub**: https://github.com/sei-protocol/sei-db
- **Contest**: https://www.sei.io/

### Keywords for Search

`vulnerability`

