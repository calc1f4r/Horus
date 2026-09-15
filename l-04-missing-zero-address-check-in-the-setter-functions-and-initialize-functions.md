---
# Core Classification
protocol: SKALE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4240
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-skale-contest
source_link: https://code4rena.com/reports/2022-02-skale
github_link: #l-04-missing-zero-address-check-in-the-setter-functions-and-initialize-functions

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - launchpad
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-04] Missing zero-address check in the setter functions and initialize functions

### Overview

See description below for full details.

### Original Finding Content


Missing checks for zero-addresses may lead to infunctional protocol, if the variable addresses are updated incorrectly.

### Proof of Concept

1.  Navigate to the following contracts.

<!---->

    https://github.com/skalenetwork/ima-c4-audit/blob/main/contracts/schain/CommunityLocker.sol#L253

### Recommended Mitigation Steps

Consider adding zero-address checks in the discussed constructors:
require(newAddr != address(0));.

**[DimaStebaev (SKALE) commented](https://github.com/code-423n4/2022-02-skale-findings/issues/67#issuecomment-1066886133):**
 > L-01 and L-02 is described in #2 
> L-02: only SKALE chain owner are able to deploy smart contracts on it's SKALE chain and this actor is assumed as trusted.

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2022-02-skale-findings/issues/67#issuecomment-1118619134):**
> ### L-01 : Front-runnable Initializers
> Agree with finding in lack of any mitigation am marking this valid.
> For the sponsor, this is how you can deploy and set data in one tx: https://github.com/Badger-Finance/badger-strategy-mix-v1/blob/c97eda8cb60d0dcfd62be956a2aab4c86353de65/contracts/proxy/AdminUpgradeabilityProxy.sol#L225
> 
> ### L-02 : Initializer reentrancy may lead to double initialization
> Finding is valid, and mitigation is to upgrade to newer OZ code
> 
> 
> ### L-03 : ERC1155Supply vulnerability in OpenZeppelin Contracts
> Valid
> 
> 
> ### L-04 : Missing zero-address check in the setter functions and initialize functions
> Agree
> 
> e.g. -> Vulnerability in OZ -> See disclosure -> Upgrade to xyz

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2022-02-skale-findings/issues/67#issuecomment-1147571670):**
 > Making this the winner of QA Reports, mostly because it offers some unique findings in a proper QA Format.
> 
> In terms of Findings Kirk-Baird is basically there, I ended up making this report win as it was submitted as QA rather than an aggregate of downgraded findings.
> 
> That said I believe this report could have had a couple extra findings to make it truly a winner.
> 
> L-01: Front-runnable Initializers -> Low
> 
> L-02 : Initializer reentrancy may lead to double initialization -> Low
> 
> L-03 : ERC1155Supply vulnerability in OpenZeppelin Contracts -> Low
> 
> L-04 : Missing zero-address check in the setter functions and initialize functions -> Low




***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | SKALE |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-skale
- **GitHub**: #l-04-missing-zero-address-check-in-the-setter-functions-and-initialize-functions
- **Contest**: https://code4rena.com/contests/2022-02-skale-contest

### Keywords for Search

`vulnerability`

