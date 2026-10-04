---
# Core Classification
protocol: Angle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19194
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Integer Overflow in revokeStableMaster()

### Overview

See description below for full details.

### Original Finding Content

Description
TherevokeStableMaster() function is used to revoke a StableMaster contract from the Core contract,
and therefore removes the related stablecoin from stablecoinList . This function assumes there is always at
least one stablecoin in stablecoinList , as shown in line [ 89].
for (uint256 i = 0; i < stablecoinList . length - 1; i ++) {
If a Governor tries to execute this function where there is no existing stablecoin, there will be a negative integer
overflow, caused by stablecoinList.length - 1 which equals to 0 - 1 in anuint256 variable. Fortunately,
starting from Solidity 0.8.0, integer overflows are mitigated. However, from a user’s perspective, the error mes-
sage is unclear.
Recommendations
Consider adding an extra check inside the revokeStableMaster() function to make sure there is at least one
stablecoin in stablecoinList .
if( stableCoinList . length > 0)
for (uint256 i = 0; i < stablecoinList . length - 1; i ++) {
Resolution
This has been resolved in commit 4cd59ce. The new implementation introduces an additional check to ensure
that there exists at least one item on the list before revoking. Related code from line [ 134-136 ]:
uint256 stablecoinListLength = stablecoinList . length ;
// Checking if ‘stableMaster ‘ is correct and removing the stablecoin from the ‘stablecoinList ‘
require ( stablecoinListLength >= 1, " incorrect stablecoin ");
Page | 28
Angle Protocol Detailed Findings
AGL-15 Governor Must Be a Contract

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Angle |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf

### Keywords for Search

`vulnerability`

