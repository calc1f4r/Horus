---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25319
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto-v2
source_link: https://code4rena.com/reports/2022-06-canto-v2
github_link: https://github.com/code-423n4/2022-06-NewBlockchain-v2-findings/issues/124

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-04] Oracle `periodSize` is very low allowing the TWAP price to be easily manipulated

### Overview


A bug was reported in the Lending Market V2 contract on GitHub. It was found by several people, including 0x52, &#95;&#95;141345&#95;&#95;, Chom, csanuragjain, and ladboy233. The bug relates to the TWAP oracle being easily manipulated. The proof of concept was that the periodSize was set to 0, meaning that the oracle would take a new observation every single block, which would allow an attacker to easily flood the TWAP oracle and manipulate the price. This was confirmed by nivasan1 (Canto) and Alex the Entreprenerd (judge) commented that the change would end up resulting in a manipulatable quote which will impact getUnderlyingPrice. The recommended mitigation step was to increase periodSize to be greater than 0, 1800 is typically standard.

### Original Finding Content

_Submitted by 0x52, also found by &#95;&#95;141345&#95;&#95;, Chom, csanuragjain, and ladboy233_

<https://github.com/Plex-Engineer/lending-market-v2/blob/ea5840de72eab58bec837bb51986ac73712fcfde/contracts/Stableswap/BaseV1-core.sol#L72>

TWAP oracle easily manipulated.

### Proof of Concept

periodSize is set to 0 meaning that the oracle will take a new observation every single block, which would allow an attacker to easily flood the TWAP oracle and manipulate the price.

### Recommended Mitigation Steps

Increase periodSize to be greater than 0, 1800 is typically standard.

**[nivasan1 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-v2-findings/issues/124)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-v2-findings/issues/124#issuecomment-1216838068):**
 > The warden has identified a constant set to zero for the time in between TWAP observations.
> 
> Because the code change:
> - Is a mistake (evidenced by the comments)
> - Causes the TWAP (already put into question in previous contest) to become a Spot Oracle
> - There's no way to remediate as the variable is constant
> - The change will end up resulting in a manipulatable `quote` which will impact `getUnderlyingPrice`
> 
> I agree with High Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto-v2
- **GitHub**: https://github.com/code-423n4/2022-06-NewBlockchain-v2-findings/issues/124
- **Contest**: https://code4rena.com/reports/2022-06-canto-v2

### Keywords for Search

`vulnerability`

