---
# Core Classification
protocol: Pyth Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48821
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/pyth-client.

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Potential out-of-bounds read in PD arithmetic

### Overview

See description below for full details.

### Original Finding Content

## pd_adjust Function Overview

The `pd_adjust` function uses a lookup table to multiply the value `v` by a power of ten. However, if the original exponent `n->e_` and target exponent `e` differ too much, the index will exceed the table’s length. This constitutes an out-of-bounds read.

## Code Snippet

```c
pd.h:L68-L79
static inline void pd_adjust( pd_t *n, int e, const int64_t *p )
{
    int64_t v = n->v_;
    int d = n->e_ - e;
    if ( d > 0 ) {
        v *= p[ d ];
    }
    else if ( d < 0 ) {
        v /= p[ -d ];
    }
    pd_new( n, v, e );
}
```

## Remediation

The `pd_adjust` function should perform bounds checks on `d` and return a `bool` to signify whether the adjustment succeeded, similar to the `pd_store` function.

### Code Snippet

```c
pd.h:L35-L60
static inline bool pd_store( int64_t *r, pd_t const *n )
{
    ...
    while ( e > ( 1 << ( EXP_BITS - 1 ) ) - 1 ) {
        v *= 10;
        if ( v < -( 1L << 58 ) || v > ( 1L << 58 ) - 1 ) {
            return false;
        }
        --e;
    }
    *r = ( v << EXP_BITS ) | ( e & EXP_MASK );
    return true;
}
```

## Patch

Pyth Data Association acknowledges the finding, but doesn't believe it has security implications. However, they may deploy a fix to address it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Oracle |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/pyth-client.
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

