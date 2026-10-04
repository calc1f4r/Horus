---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6814
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Denis Milicevic
  - Gerard Persoon
---

## Vulnerability Title

Admin Can Always Update lscales Levels

### Overview


This bug report is about the Divider.sol#511-547 and Divider.sol#L466-468 code which allows an administrator of the protocol to arbitrarily set the lscales levels of users at any moment. This directly impacts the amount that can be collected in the collect() function. The update of lscales levels can be done by setting the adapter to off, which will allow the require in backfillScale() to continue. Following this, a call to backfillScale() should be done to set arbitrary values to the lscales. Finally, set the adapter back to on.

The recommendation given is to double check the circumstances under which an administrator can perform such updates. It was decided to keep this ability for admins for edge cases, instead of removing it. It will be clearly mentioned in the documentation and processes will be run to ensure that the community has visibility into the thought processes. Internally, the team is still discussing this.

### Original Finding Content

## Severity: Medium Risk

## Context
- Divider.sol#511-547
- Divider.sol#L466-468

## Situation
An administrator of the protocol can arbitrarily set the `lscales` levels of users at any moment. This directly impacts the amount that can be collected in the `collect()` function. 

The update of `lscales` levels can be done by setting the adapter to off, which will allow the `require` in `backfillScale()` to continue. Following this, a call to `backfillScale()` should be made to set arbitrary values to the `lscales`. Finally, the adapter should be set back to on.

Although this is protected by `requiresTrust`, it is probably best to limit this possibility.

```solidity
function setAdapter(address adapter, bool isOn) public requiresTrust {
    _setAdapter(adapter, isOn);
}

function backfillScale(..., address[] calldata _usrs, uint256[] calldata _lscales) external requiresTrust {
    ...
    // continues when adapters[adapter] == false
    require(!adapters[adapter] || block.timestamp > cutoff, ...);
    /* Set user's last scale values the Series
    (needed for the `collect` method) */
    for (uint256 i = 0; i < _usrs.length; i++) {
        lscales[adapter][maturity][_usrs[i]] = _lscales[i];
    }
    ...
}
```

## Recommendation
Double-check the circumstances under which an administrator can perform such updates.

## Sense
We’ve decided to keep this ability for admins for edge cases. Instead of removing it, it’ll be clearly mentioned in the documentation, and we’ll run disclosure processes to ensure that the community has insight into our thought processes. That said, we are still discussing this internally.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sense |
| Report Date | N/A |
| Finders | Max Goodman, Denis Milicevic, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

