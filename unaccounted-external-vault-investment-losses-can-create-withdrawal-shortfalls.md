---
# Core Classification
protocol: CAP Labs Covered Agent Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61539
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
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
finders_count: 3
finders:
  - Benjamin Samuels
  - Priyanka Bose
  - Nicolas Donboly
---

## Vulnerability Title

Unaccounted external vault investment losses can create withdrawal shortfalls

### Overview


The protocol has a bug where it does not properly account for losses when divesting from external vaults, such as Yearn. This means that when the address of a vault is changed, the protocol may not have enough assets to fulfill later withdrawal requests. This gives an unfair advantage to early withdrawers who are able to receive their full amounts, while later withdrawers may face shortfalls. To fix this, the protocol needs to modify its divestment function to track and account for losses, and implement a risk management system to prevent and compensate for future losses.

### Original Finding Content

## Medium Difficulty Data Validation Issue

## File Location
`contracts/vault/FractionalReserve.sol`

## Description
The protocol invests idle assets in external vaults like Yearn for yield generation, but fails to properly account for losses when divesting. When changing the address of an external vault, the protocol divests from the existing vault regardless of any losses incurred. These losses are not tracked or accounted for in the system. This structure creates an unfair “first out” advantage, allowing early withdrawers to receive their full amounts while later withdrawers may find their requests impossible to fulfill despite the system showing sufficient supply, as the physical assets no longer exist to back those withdrawals.

## Exploit Scenario
The protocol has 100 tokens of Asset A with a total supply recorded as 100 tokens.
1.  90 tokens are invested in a Yearn vault.
2.  The protocol admin changes the vault address, triggering divestment from Yearn.
3.  Due to strategy losses, only 80 tokens are returned.
4.  The protocol still records a total supply of 100 tokens, but physically has only 90 tokens available.

Early users can withdraw their tokens, but later users will be unable to withdraw their full amounts. The protocol has no mechanism to account for this 10-token loss or compensate users, creating a “first out” advantage where early withdrawers receive their full amounts while later withdrawers face shortfalls.

## Recommendations
**Short term:** Modify the divestment function to track and account for any losses when divesting from external vaults, accumulating them as protocol debt that gets paid down using future yield profits before sending excess returns to the fee auction.

**Long term:** Implement a comprehensive risk management system that carefully evaluates external vault strategies, includes safeguards against significant losses, compensates for loss using future profits, and creates a loss-socialization mechanism that fairly distributes any unavoidable losses among all users rather than disadvantaging only the last withdrawers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | CAP Labs Covered Agent Protocol |
| Report Date | N/A |
| Finders | Benjamin Samuels, Priyanka Bose, Nicolas Donboly |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-caplabs-coveredagentprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

