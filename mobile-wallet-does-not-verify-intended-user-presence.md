---
# Core Classification
protocol: ZecWallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17321
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/zecwallet.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/zecwallet.pdf
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
finders_count: 5
finders:
  - 2019: Initial report delivered Final report delivered
  - Changelog April 12
  - 2019: May 7
  - John Dunlap
  - David Pokora
---

## Vulnerability Title

Mobile wallet does not verify intended-user presence

### Overview


This bug report is about the mobile wallet application, ZecWallet, which lacks strong authentication such as TouchID or passwords and short idle timeouts. This means that an attacker that has access to the owner's unlocked phone can potentially steal funds from the wallet. To address this, short-term authentication mechanisms should be implemented to ensure only the intended user can authenticate to the application. Additionally, an appropriate idle timeout should be set. In the long-term, authentication mechanisms should be reviewed to minimize the impact of an unauthorized user with physical access to the devices. Encrypting connection settings or the shared secret key with a required password would require the attacker to authenticate accordingly.

### Original Finding Content

## ZecWallet Product Assessment

## Type
Data Exposure

## Target
DataModel.kt

## Difficulty
Low

## Description
The mobile wallet application assumes that any individual with access to the mobile device should be able to send funds. This assumption introduces risk. Traditionally, mobile payment methods such as ApplePay require strong authentication such as TouchID, to ensure any individual with access to the owner’s unlocked phone cannot also steal funds. Similarly, mobile banking software requires passwords and enforces short idle timeouts.

By lacking such authentication, ZecWallet poses a risk that a user’s funds can be stolen if an attacker could gain unlocked access to the owner’s mobile device. This contrasts to the risk of an attacker gaining access to the desktop machine because mobile devices are more likely to be stolen or lost in public spaces.

## Exploit Scenario
Alice pairs her desktop and mobile devices through the wormhole and brings her mobile device to a public location. Eve is aware of Alice’s large Zcash balance. Eve steals the mobile device while it is in an unlocked state and subsequently withdraws all funds from Alice’s Zcash wallet.

## Recommendation
**Short term:** Implement authentication mechanisms to ensure that only the intended user of the ZecWallet can authenticate to the application. Set an appropriate idle timeout to ensure an authenticated user must reauthenticate after a period of inactivity.

**Long term:** Review authentication mechanisms within the mobile and desktop applications to minimize the impact of an unauthorized user with physical access to these devices. Ensure the authentication methods are required for underlying functionality. For example, disallowing a transition to the next page in the user interface could be bypassed, but encrypting connection settings or the shared secret key with a required password would require the attacker to authenticate accordingly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | ZecWallet |
| Report Date | N/A |
| Finders | 2019: Initial report delivered Final report delivered, Changelog April 12, 2019: May 7, John Dunlap, David Pokora |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/zecwallet.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/zecwallet.pdf

### Keywords for Search

`vulnerability`

