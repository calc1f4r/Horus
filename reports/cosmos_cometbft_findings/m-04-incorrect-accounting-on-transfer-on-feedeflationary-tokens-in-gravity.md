---
# Core Classification
protocol: Althea Gravity Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42280
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-08-gravitybridge
source_link: https://code4rena.com/reports/2021-08-gravitybridge
github_link: https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/62

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
  - dexes
  - bridge
  - cdp
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] Incorrect accounting on transfer-on-fee/deflationary tokens in `Gravity`

### Overview


The `sendToCosmos` function of `Gravity` has a bug which can result in users receiving less tokens than they deposited. This happens because the amount of tokens transferred may be less than the amount specified due to deflationary tokens. This can cause issues on the Cosmos side where it will think more tokens are locked on the Ethereum side. To fix this, the recommended solution is to calculate the difference in token balance before and after the transfer. This issue has been confirmed by a member of the Althea team and has been classified as a high severity issue as it can result in the theft of tokens.

### Original Finding Content

_Submitted by shw_

#### Impact
The `sendToCosmos` function of `Gravity` transfers `_amount` of `_tokenContract` from the sender using the function `transferFrom`. If the transferred token is a transfer-on-fee/deflationary token, the actually received amount could be less than `_amount`. However, since `_amount` is passed as a parameter of the `SendToCosmosEvent` event, the Cosmos side will think more tokens are locked on the Ethereum side.

#### Proof of Concept
Referenced code:
* [Gravity.sol#L535](https://github.com/althea-net/cosmos-gravity-bridge/blob/92d0e12cea813305e6472851beeb80bd2eaf858d/solidity/contracts/Gravity.sol#L535)
* [Gravity.sol#L541](https://github.com/althea-net/cosmos-gravity-bridge/blob/92d0e12cea813305e6472851beeb80bd2eaf858d/solidity/contracts/Gravity.sol#L541)

#### Recommended Mitigation Steps

Consider getting the received amount by calculating the difference of token balance (using `balanceOf`) before and after the `transferFrom`.

**[jkilpatr (Althea) confirmed](https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/62#issuecomment-916196186):**
 > This is a valid issue, it does present the ability to 'steal' tokens from the bridge, so I think that justifies the severity.
>
> If user (A) deposits a deflationary token and gets slightly more vouchers than where actually deposited into the bridge upon withdraw they could steal tokens from user (B) who had also deposited.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Althea Gravity Bridge |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-gravitybridge
- **GitHub**: https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/62
- **Contest**: https://code4rena.com/reports/2021-08-gravitybridge

### Keywords for Search

`vulnerability`

