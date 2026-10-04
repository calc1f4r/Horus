---
# Core Classification
protocol: Onemind
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57636
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-18-Onemind.md
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
  - zokyo
---

## Vulnerability Title

Royalties might get stuck on the contract.

### Overview


The bug report is about a function in the PlatformAuction.sol file that handles royalties and currency transfers. There is a problem with the check for the receiver address, which can cause the royalty value to be calculated and subtracted from the initial price, but not actually transferred. This can happen if the owner of the NFT collection has renounced their role. The recommendation is to not subtract the fee value if it wasn't transferred due to a zero address. The bug has been resolved, but there was another issue where the result of the transaction was always returned as true even if the royalty was not transferred. This has also been fixed.

### Original Finding Content

**Description**

PlatformAuction.sol: function_handleRoyalties(), _currency Transfer().
There is a check in the_currency Transfer() function that the 'receiver address is not zero address. In case the owner of the NFT collection has renounced the role with standard Ownable functionality, the_calculateRoyalty() function called within the_handleRoyalties() function will return zero address. This way, the royalty value will be calculated and subtracted from the initial price` (Line 150), but it won't be transferred and will get stuck on the auction contract's balance.
A similar situation can also happen in the_handleFee() function in case 'feeConfig.treasury` is set as zero address.

**Recommendation**

Do not subtract the fee value from the price in case the fee value wasn't transferred because of zero address.

**Re-audit comment**

Resolved.

Post-audit:
Paid 'royalty amount is now subtracted from price` in case of a successful royalty transfer. However, in_currency Transfer(), the result flag is initially equal to true. Due to this, the result of the transaction will be returned as true even though, in fact, royalty might not have been transferred.

Post-audit:
The correct result is returned now and no royalties can get stuck.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Onemind |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-18-Onemind.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

