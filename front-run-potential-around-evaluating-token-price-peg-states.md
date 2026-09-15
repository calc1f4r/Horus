---
# Core Classification
protocol: Swaap Finance Safeguard Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60515
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/swaap-finance-safeguard-pool/d304d4d7-05aa-42bd-92ba-7fd7f5e701ac/index.html
source_link: https://certificate.quantstamp.com/full/swaap-finance-safeguard-pool/d304d4d7-05aa-42bd-92ba-7fd7f5e701ac/index.html
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
finders_count: 4
finders:
  - Danny Aksenov
  - Julio Aguliar
  - Rabib Islam
  - Ruben Koch
---

## Vulnerability Title

Front-Run Potential Around Evaluating Token Price Peg States

### Overview


The report discusses a potential issue with a protocol called `SafeguardPool.sol`. This protocol allows for tokens to be pegged to a value of one, which is intended to reduce gas costs for swaps with stablecoins. However, there is a risk that if certain conditions are met, tokens could be drained from the protocol and result in significant losses. The report recommends removing the pegging feature to prevent potential issues.

### Original Finding Content

**Update**
Although we understand that gas is an important point of consideration in protocol design and implementation, we find that assuming the price of any given asset is risky in principle, and we recommend against it.

The client provided the following explanation:

> A lot of conditions must overlap in order to have significant losses if the price oracle peg is on: 1- Quote Signer is malicious or misbehaving 2- balancesSafeguard() deviations are important (set by the pool managers) 3- Price depeg is important and fast (for slow depeg evaluateStablesPegStates() can be used to unpeg the price oracle permissionlessly)

**File(s) affected:**`SafeguardPool.sol`

**Description:** Within `SafeguardPool`, if certain conditions are met, tokens can be pegged to the value of one, which is intended to reduce gas costs for swaps with stablecoins. This pegging can be activated or deactivated in a permissionless manner if it is within or outside, respectively, of a certain price range compared to the Chainlink oracle.

There is a guaranteed profit in frontrunning a successful switch of the `isTokenPegged` flag for an asset in either way (assuming a favorable quote is provided). However, the scenario of frontrunning a removal of a pegging could have severe consequences. If the pegged token's real price is de-pegging in the sub-dollar direction, swaps with the pegged token as the input could be very rewarding. More importantly, the performance and balances safeguard are also performed with the pegged asset value, resulting in the reality of the drained TVL of a swap potentially vastly exceeding `1 - maxTargetDev`.

However, given that the `_balancesSafeguard()` function limits the potential losses in the event of a depegging, the risk associated with (temporary) non-reliance on the oracle price may be considered acceptable.

**Recommendation:** While the change of the pegging flag would be a very rare event, we do believe the protocol is not sufficiently protected. The most secure approach to the issue would be the removal of the pegging feature.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Swaap Finance Safeguard Pool |
| Report Date | N/A |
| Finders | Danny Aksenov, Julio Aguliar, Rabib Islam, Ruben Koch |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/swaap-finance-safeguard-pool/d304d4d7-05aa-42bd-92ba-7fd7f5e701ac/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/swaap-finance-safeguard-pool/d304d4d7-05aa-42bd-92ba-7fd7f5e701ac/index.html

### Keywords for Search

`vulnerability`

