---
# Core Classification
protocol: FOMO Game
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47603
audit_firm: OtterSec
contest_link: https://play.fomosolana.com/
source_link: https://play.fomosolana.com/
github_link: https://github.com/Doge-Capital/FOMO-GAME

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
finders_count: 3
finders:
  - Akash Gurugunti
  - Tamta Topuria
  - OtterSec
---

## Vulnerability Title

Missing Referrer Validation

### Overview


The bug report is about a code that checks if a user has a referrer account and if their authority is different from the buyer's authority. It also checks if the user has already used a referral code and if the referrer's authority matches the stored authority in the user's account. However, the code does not check if the referrer has actually created a referral code or paid the required fee. This could potentially allow users to set any user as their referrer, even if that user has not paid the fee. The suggested solution is to ensure that the referrer has created a referral code before allowing them to be set as the user's referrer. The issue has been resolved in a specific patch.

### Original Finding Content

## Ticket Buying Process

The `buy_ticket` function checks if a referrer account (`referrer_acc`) exists. If it does, the function ensures that the authority of the referrer is not the same as the buyer’s authority. 

Additionally, if the user has already utilized a referral code (`user_acc.is_referral_code_used` is true), the function checks that the referrer’s authority matches the stored referrer authority in the user’s account.

**Important Note:** 
The code does not explicitly check whether the referrer has created a referral code or paid the required referral creation fee. This oversight may allow users to select any user as their referrer, even if that person has not paid the fee to become a referrer.

## Remediation
Ensure the referrer has created a referral code before allowing users to set them as their referrer.

## Patch
Resolved in commit `9af94da`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | FOMO Game |
| Report Date | N/A |
| Finders | Akash Gurugunti, Tamta Topuria, OtterSec |

### Source Links

- **Source**: https://play.fomosolana.com/
- **GitHub**: https://github.com/Doge-Capital/FOMO-GAME
- **Contest**: https://play.fomosolana.com/

### Keywords for Search

`vulnerability`

