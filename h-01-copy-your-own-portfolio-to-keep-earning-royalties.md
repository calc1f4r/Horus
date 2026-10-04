---
# Core Classification
protocol: Nested Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1050
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-nested-finance-contest
source_link: https://code4rena.com/reports/2021-11-nested
github_link: https://github.com/code-423n4/2021-11-nested-findings/issues/30

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
finders_count: 1
finders:
  - jayjonah8
---

## Vulnerability Title

[H-01] Copy your own portfolio to keep earning royalties

### Overview


Jayjonah8 has identified a vulnerability in the NestedFactory.sol code which could allow someone to receive royalty shares for copying their own portfolio and repeating the process over and over again. The proof of concept can be found in the specified Github links. This vulnerability was identified through manual code review. To mitigate this vulnerability, a require statement should be added not allowing users to copy their own portfolios.

### Original Finding Content

_Submitted by jayjonah8_

#### Impact
In `NestedFactory.sol` going through the `create()` function which leads to the `sendFeesWithRoyalties()` => `addShares()` function,  Im not seeing any checks preventing someone from copying their own portfolio and receiving royalty shares for it and simply repeating the process over and over again.

#### Proof of Concept
- [`FeeSplitter.sol` L152](https://github.com/code-423n4/2021-11-nested/blob/main/contracts/FeeSplitter.sol#L152)
- [`FeeSplitter.sol` L220](https://github.com/code-423n4/2021-11-nested/blob/main/contracts/FeeSplitter.sol#L220)
- [`NestedFactory.sol` L103](https://github.com/code-423n4/2021-11-nested/blob/main/contracts/NestedFactory.sol#L103)
- [`NestedAsset.sol` L69](https://github.com/code-423n4/2021-11-nested/blob/main/contracts/NestedAsset.sol#L69)
- [`NestedFactory.sol` L103](https://github.com/code-423n4/2021-11-nested/blob/main/contracts/NestedFactory.sol#L103)
- [`NestedFactory.sol` L491](https://github.com/code-423n4/2021-11-nested/blob/main/contracts/NestedFactory.sol#L491)

#### Tools Used
Manual code review

#### Recommended Mitigation Steps
A require statement should be added not allowing users to copy their own portfolios.

**[maximebrugel (Nested) disagreed with severity](https://github.com/code-423n4/2021-11-nested-findings/issues/30#issuecomment-970388713):**
 > Indeed, a user can copy his own portfolio to reduce the fees, however a require statement won't fix this issue...
>
> This problem cannot be corrected but only mitigated, since the user can use two different wallets.
> Currently the front-end doesn't allow to duplicate a portfolio with the same address.
>
> I don't consider this a "High Risk" since the assets are not really stolen. Maybe "Med Risk" ? This is by design an issue and we tolerate that users can do this (with multiple wallets).
>

**[alcueca (judge) commented](https://github.com/code-423n4/2021-11-nested-findings/issues/30#issuecomment-985642915):**
 > I'm reading that the vulnerability actually lowers fees to zero for a dedicated attacker, since creating a arbitrarily large number of wallets and bypassing the frontend is easy. In theory leaking protocol value would be a severity 2, but since this is effectively disabling a core feature of the protocol (fees), the severity 3 is sustained.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Nested Finance |
| Report Date | N/A |
| Finders | jayjonah8 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-nested
- **GitHub**: https://github.com/code-423n4/2021-11-nested-findings/issues/30
- **Contest**: https://code4rena.com/contests/2021-11-nested-finance-contest

### Keywords for Search

`vulnerability`

