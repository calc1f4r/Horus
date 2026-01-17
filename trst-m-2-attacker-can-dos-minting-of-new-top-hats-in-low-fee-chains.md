---
# Core Classification
protocol: Hats Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18926
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-02-20-Hats Protocol.md
github_link: none

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
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-2 Attacker can DOS minting of new top hats in low-fee chains

### Overview


In the Hats protocol, a function called `mintTopHat()` is used to assign a top hat to anyone. The top hat is structured with the top 32 bits as a domain ID and the lower 224 bits being cleared. As there are only 4 billion possible top hats, once all of them are consumed, the `mintTopHat()` function will always fail. This exposes the project to a DOS vector, where an attacker could mint 4 billion top hats in a loop and make the function unusable, forcing a redeploy of the Hats protocol. This could be achieved on cheaper L2 networks, and as the project will be deployed on a variety of EVM blockchains, the risk is significant. 

To mitigate this issue, it is recommended to require a non-refundable deposit fee (paid in native token) when minting a top hat. The fee should be set so that consuming the 32-bit space is impossible. This could also be used as a revenue stream for the Hats project. The team acknowledged the risk, but elected not to address it in version 1 for several reasons: 1) additional requirement to set & manage authorization for withdrawal; 2) challenge of setting a consistently reasonable fee on chains without stablecoin based native tokens; 3) contract size constraints.

### Original Finding Content

**Description:**
In Hats protocol, anyone can be assigned a top hat via the `mintTopHat()` function. The top 
hats are structured with top 32 bits acting as a domain ID, and the lower 224 bits are 
cleared. There are therefore up to 2^32 = ~ 4 billion top hats. Once they are all consumed, 
`mintTopHat()` will always fail:
```solidity
          // uint32 lastTopHatId will overflow in brackets
             topHatId = uint256(++lastTopHatId) << 224;
```     
This behavior exposes the project to a DOS vector, where an attacker can mint 4 billion top 
hats in a loop and make the function unusable, forcing a redeploy of Hats protocol. This is 
unrealistic on ETH mainnet due to gas consumption, but definitely achievable on the 
cheaper L2 networks. As the project will be deployed on a large variety of EVM blockchains, 
this poses a significant risk.

**Recommended Mitigation:**
Require a non-refundable deposit fee (paid in native token) when minting a top hat. Price it 
so that consuming the 32-bit space will be impossible. This can also serve as a revenue 
stream for the Hats project.

**Team Response:**
Acknowledged; electing not to address in v1 for several reasons:
1. Additional requirement to set & manage authorization for withdrawal
2. Challenge of setting a consistently reasonable fee on chains without stablecoin based native tokens (i.e. all except for Gnosis Chain) / the added complexity and 
centralization risk of making the fee adjustable
3. Contract size constraints

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Hats Protocol |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-02-20-Hats Protocol.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

