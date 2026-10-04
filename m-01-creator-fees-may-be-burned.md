---
# Core Classification
protocol: Foundation
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3164
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-foundation-drop-contest
source_link: https://code4rena.com/reports/2022-08-foundation
github_link: https://github.com/code-423n4/2022-08-foundation-findings/issues/31

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Lambda
---

## Vulnerability Title

[M-01] Creator fees may be burned

### Overview


This bug report is about a vulnerability in the code of a website that could cause ETH amounts to be sent to an address of 0, which would result in the ETH being burned and lost. This vulnerability is present in the code located at the given URL. 

The impact of this bug is that the functions `royaltyInfo`, `getRoyalties`, or `getFeeRecipients` may return the address 0 as the recipient address. While the value 0 is correctly handled for the royalties, it is not for the address, resulting in the ETH being sent to address 0 and burned. 

The recommended mitigation steps for this bug are to treat address 0 as if no recipient was returned in the logic for determining the recipients, so that the other priorities or methods take over. This will prevent the ETH from being sent to address 0 and being burned.

### Original Finding Content

_Submitted by Lambda_

`royaltyInfo`, `getRoyalties`, or `getFeeRecipients` may return `address(0)` as the recipient address. While the value 0 is correctly handled for the royalties itself, it is not for the address. In such a case, the ETH amount will be sent to `address(0)`, i.e. it is burned and lost.

### Recommended Mitigation Steps

In your logic for determining the recipients, treat `address(0)` as if no recipient was returned such that the other priorities / methods take over.


**[HardlyDifficult (Foundation) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2022-08-foundation-findings/issues/31#issuecomment-1220570897):**
 > We are looking into options here to improve.
> 
> We believe this is Medium risk, burning a percent of the sale revenue is a form of leaking value. Otherwise the sale works as expected and the collector does get the NFT they purchased.
> 
> The royalty APIs we use are meant to specific which addresses should receive payments and how much they each should receive. As the warden noted, we try to ignore entries which specify a 0 amount... but did not filter out address(0) recipients with >0 requested. Originally we were thinking this was a way of requesting that a portion of the sale be burned since that seems to be what the data is proposing.
> 
> However we agree that this is more likely a configuration error. Since our market uses ETH and not ERC20 tokens, it's unlikely that creators would actually want a portion of the proceeds burned. We are exploring a change to send the additional revenue to the seller instead of burning the funds in this scenario.

**[HickupHH3 (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-08-foundation-findings/issues/31#issuecomment-1226890842):**
 > Case of protocol leaked value: Medium severity is appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Foundation |
| Report Date | N/A |
| Finders | Lambda |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-foundation
- **GitHub**: https://github.com/code-423n4/2022-08-foundation-findings/issues/31
- **Contest**: https://code4rena.com/contests/2022-08-foundation-drop-contest

### Keywords for Search

`Validation`

