---
# Core Classification
protocol: Dopex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29465
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-dopex
source_link: https://code4rena.com/reports/2023-08-dopex
github_link: https://github.com/code-423n4/2023-08-dopex-findings/issues/1956

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
finders_count: 6
finders:
  - ABA
  - peakbolt
  - 0xnev
  - pep7siup
  - zzebra83
---

## Vulnerability Title

[M-03] No mechanism to settle out-of-money put options even after Bond receipt token is redeemed.

### Overview


This bug report concerns the current implementation of the Perpetual Atlantic Vault, which allows for a put option to be purchased by a user when the RDPX-ETH price is 25% out of the money. If the price is still above this point, the option is rolled over to the next epoch and a new premium is calculated and added to the totalFundingForEpoch. The issue is that, as long as the option is out of the money, the funding cost continues to be deducted from the core contract and passed to Atlantic vault LPs, with no check if the underlying bond has been redeemed or not.

The two implications of this issue are that Atlantic vault LPs collateral will be locked for as long as the option is out of the money, as the optionStrikes[strike] never reduces, and that the core contract continues to pay out funding costs for out of the money options that cannot be settled.

The recommended mitigation steps for this issue are to consider settling optionIds that no longer have an underlying bonding, so that put options for such bonds can expire and free up locked collateral in Atlantic Vaults.

### Original Finding Content


<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/perp-vault/PerpetualAtlanticVault.sol#L333> 

<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/core/RdpxV2Core.sol#L800> 

<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/perp-vault/PerpetualAtlanticVault.sol#L376>

In the current implementation of `PerpetualAtlanticVault::settle`, the only way an `optionId` can be burnt is when the option is in-the-money. Note that at the time of bonding, a put option that is 25% out of the money is purchased by user. If the RDPX-ETH price is above this price, the option is rolled over to the next epoch and a new premium is again calculated inside the `PerpetualAtlanticVault::calculateFunding` and added to the `totalFundingForEpoch`.

Effectively, as long as the option is out of money, the funding cost continues to be deducted from core contract and passed to Atlantic vault LPs.  There is no check if the underlying bond for which this put option is minted is redeemed or not.

Not completely sure if this is bug or feature of Perpetual Atlantic Puts but since the utility of these puts is to protect downside price movements of RDPX during bonding, such options should be retired once the underlying bond is redeemed by user. Paying out a premium on a perennial basis to Atlantic LP's does not make sense.

### Impact

There are 2 implications:

1.  Atlantic vault LPs collateral will be locked so long as option is out of money. This is because `optionStrikes[strike]` never reduces so long as the option continues to be OTM.
2.  Core contract continues to pay out funding costs for OTM options that cannot be settled.

### Recommended Mitigation Steps

Consider settling `optionIds` that no longer have an underlying bonding. Put options for such bonds should expire and free up locked collateral in Atlantic Vaults.

**[psytama (Dopex) confirmed](https://github.com/code-423n4/2023-08-dopex-findings/issues/1956#issuecomment-1734300784)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Dopex |
| Report Date | N/A |
| Finders | ABA, peakbolt, 0xnev, pep7siup, zzebra83, 0Kage |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-dopex
- **GitHub**: https://github.com/code-423n4/2023-08-dopex-findings/issues/1956
- **Contest**: https://code4rena.com/reports/2023-08-dopex

### Keywords for Search

`vulnerability`

