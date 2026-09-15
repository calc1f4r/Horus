---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17938
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

Setting collateral values manually is error-prone

### Overview


This bug report is about the ManualTokenTrackerAMO.sol contract in the Frax Solidity team. During the audit, it was found that collateral located on non-mainnet chains was included in FRAX.globalCollateralValue in the FRAXStablecoin contract on the Ethereum mainnet. This collateral cannot be redeemed by users, and a script is used to aggregate the collateral prices from multiple chains and contracts and post the data to ManualTokenTrackerAMO. This process needs to be reviewed, as it increases the attack surface of the protocol and the likelihood of a hazard. The correctness of the script used to calculate the data has not been reviewed, and the reliability of the script is unknown. Furthermore, the role is not explained in the documentation or contracts. As of December 20, 2021, collatDollarBalance has not been updated since November 13, 2021, and is equivalent to fraxDollarBalanceStored, indicating that FRAX.globalCollateralValue is both out of date and incorrectly counts FRAX as collateral. The recommendations are to include only collateral that can be valued natively on the Ethereum mainnet and to document and follow rigorous processes that limit risk and provide confidence to users.

### Original Finding Content

## Target: ManualTokenTrackerAMO.sol

## Description

During the audit, the Frax Solidity team indicated that collateral located on non-mainnet chains is included in `FRAX.globalCollateralValue` in `FRAXStablecoin`, the Ethereum mainnet contract. (As indicated in TOB-FRSOL-023, this collateral cannot currently be redeemed by users.) 

Using a script, the team aggregates collateral prices from across multiple chains and contracts and then posts that data to `ManualTokenTrackerAMO` by calling `setDollarBalances`. Since we did not have the opportunity to review the script and these contracts were out of scope, we cannot speak to the security of this area of the system. Other issues with collateral accounting and pricing indicate that this process needs review. 

Furthermore, considering the following issues, this privileged role and architecture significantly increases the attack surface of the protocol and the likelihood of a hazard:

- The correctness of the script used to calculate the data has not been reviewed, and users cannot audit or verify this data for themselves.
- The configuration of the Frax Protocol is highly complex, and we are not aware of how these interactions are tracked. It is possible that collateral can be mistakenly counted more than once or not at all.
- The reliability of the script and the frequency with which it is run is unknown. In times of market volatility, it is not clear whether the script will function as anticipated and be able to post updates to the mainnet.
- This role is not explained in the documentation or contracts, and it is not clear what guarantees users have regarding the collateralization of FRAX (i.e., what is included and updated).

As of December 20, 2021, `collatDollarBalance` has not been updated since November 13, 2021, and is equivalent to `fraxDollarBalanceStored`. This indicates that `FRAX.globalCollateralValue` is both out of date and incorrectly counts FRAX as collateral (see TOB-FRSOL-024).

## Recommendations

Short term, include only collateral that can be valued natively on the Ethereum mainnet and do not include collateral that cannot be redeemed in `FRAX.globalCollateralValue`.

Long term, document and follow rigorous processes that limit risk and provide confidence to users.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`

