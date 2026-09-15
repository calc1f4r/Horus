---
# Core Classification
protocol: COSMOS Fundraiser Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 12117
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/cosmos-fundraiser-audit-7543a57335a4/
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

bitcoin.waitForPayment function callback could be called multiple times

### Overview


The bug report is about the waitForPayment function of the bitcoin.js module in the fundraiser-lib. It states that the function does not handle requests that take longer than 6 seconds correctly, and it could call the callback multiple times. It is suggested that a reentrancy guard should be added, as shown in the sample code provided, which is from the maraoz/fundraiser-lib repository on Github. A reentrancy guard is a mechanism that prevents a function from being called multiple times, which is necessary in this case to prevent the callback from being called multiple times. This bug report is important for anyone working with the bitcoin.js module in the fundraiser-lib, as it could lead to errors and incorrect results.

### Original Finding Content

[waitForPayment function of bitcoin.js module in fundraiser-lib](https://github.com/cosmos/fundraiser-lib/blob/426425dfc296060a9b87830e69e19ae8a6d444c0/src/bitcoin.js#L60) doesn’t handle correctly requests that take longer than 6 seconds, and could call the callback multiple times. Consider adding a reentrancy guard, as shown on this sample code:


 [**maraoz/fundraiser-lib**  

*fundraiser-lib – JS module for participating in Cosmos Fundraiser* github.com](https://github.com/maraoz/fundraiser-lib/blob/audit2/src/bitcoin.js#L60-L79)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | COSMOS Fundraiser Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/cosmos-fundraiser-audit-7543a57335a4/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

