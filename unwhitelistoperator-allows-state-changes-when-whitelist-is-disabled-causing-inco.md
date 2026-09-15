---
# Core Classification
protocol: Symbiotic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64343
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
github_link: none

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
finders_count: 4
finders:
  - 0kage
  - Aleph-v
  - ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3
  - Farouk
---

## Vulnerability Title

`unwhitelistOperator` allows state changes when whitelist Is disabled, causing inconsistent operator state

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `unwhitelistOperator` function performs state changes (removing an operator from the whitelist and potentially unregistering them) even when the whitelist feature is **disabled**. This violates the expected behavior that **whitelist enforcement should only be active when explicitly enabled**.

Unwhitelisting an operator while the whitelist is disabled silently alters the contract’s state. Later, when the whitelist is re-enabled, the operator is unexpectedly no longer whitelisted — even though no whitelist-related logic was supposed to be active when they were removed.

**Impact:** When the whitelist feature is disabled, `unwhitelistOperator` silently processes changes, leading to an inconsistent state. If the whitelist is re-enabled, an operator who was unwhitelisted, remains registered, leading to inconsistent state.

**Recommended Mitigation:** Consider preventing `unwhitelistOperator` from executing when whitelist is disabled. Either revert explicitly or skip execution:

```solidity
function unwhitelistOperator(address operator) public virtual checkPermission {
    if (!isWhitelistEnabled()) {
        revert OperatorsWhitelist_WhitelistDisabled( );
    }

    _getOperatorsWhitelistStorage()._whitelisted[operator] = false;

    if (isOperatorRegistered(operator)) {
        _unregisterOperator(operator);
    }

    emit UnwhitelistOperator(operator);
}
```
**Symbiotic:** Fixed in [32bea5e](https://github.com/symbioticfi/relay-contracts/pull/36/commits/32bea5ee73a1085f68645ef460f8c411c96cfcbe).

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Symbiotic |
| Report Date | N/A |
| Finders | 0kage, Aleph-v, ChainDefenders](https://x.com/DefendersAudits) ([@1337web3](https://x.com/1337web3) & [@PeterSRWeb3, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

