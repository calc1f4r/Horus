---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6338
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/334

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
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - unforgiven
  - Madalad
  - 0xbepresent
---

## Vulnerability Title

[M-08] GovNFT: maxBridge has no effect

### Overview


This bug report is about GovNFT, a smart contract. In GovNFT, the setMaxBridge function is provided to set a maximum bridge limit, but this variable is not used and does not work. This means that the number of GovNFTs crossing the chain is not limited. A proof of concept is provided in the report. No tools were used to find the bug. 

The recommended mitigation step is to consider applying the maxBridge variable, so that the number of GovNFTs crossing the chain is limited.

### Original Finding Content


In GovNFT, setMaxBridge function is provided to set maxBridge, but this variable is not used, literally it should be used to limit the number of GovNFTs crossing chain, but it doesn't work in GovNFT.

```solidity
    uint256 public maxBridge = 20;
...
    function setMaxBridge(uint256 _max) external onlyOwner {
        maxBridge = _max;
    }
```

### Proof of Concept

<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/GovNFT.sol#L19-L20> 

<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/GovNFT.sol#L311-L313>

### Recommended Mitigation Steps

Consider applying the maxBridge variable.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/334#issuecomment-1399552931):**
> The Warden has shown how, an unused variable, which was meant to cap the amount of tokens bridged per call, could cause a DOS.
> 
> These types of DOS could only be fixed via Governance Operations, and could create further issues, for this reason I agree with Medium Severity.

**[GainsGoblin (Tigris Trade) confirmed and resolved](https://github.com/code-423n4/2022-12-tigris-findings/issues/334#issuecomment-1407515433):**
 > Mitigation: https://github.com/code-423n4/2022-12-tigris/pull/2#issuecomment-1419175169 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | cccz, unforgiven, Madalad, 0xbepresent |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/334
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

