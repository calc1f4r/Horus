---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24646
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-sushitrident
source_link: https://code4rena.com/reports/2021-09-sushitrident
github_link: https://github.com/code-423n4/2021-09-sushitrident-findings/issues/89

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
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] `_depositToBentoBox` sometimes uses both ETH and WETH

### Overview


This bug report focuses on the `TridentRouter._depositToBentoBox` function, which is responsible for transferring ETH and WETH into a Bento Box. The issue is that the function only uses the ETH in the contract if it is higher than the desired underlying amount. If this is not the case, the ETH will be ignored and the user's WETH will be used instead. This can be problematic since the underlying amount is computed from the Bento share price and might increase from the time the transaction is submitted to the time it is included in a block. If this happens, the user can lose their ETH deposit in the contract. 

In order to mitigate this issue, it is recommended that each batch should use the `refundETH` at the end, and that ETH should still be deposited into Bento, even if it is less than the underlying amount, with WETH only being used for the remaining token difference. This bug report has been acknowledged by maxsam4 (Sushi) on Github.

### Original Finding Content

_Submitted by cmichel, also found by 0xRajeev_

The `TridentRouter._depositToBentoBox` function only uses the `ETH` in the contract if it's higher then the desired `underlyingAmount` (`address(this).balance >= underlyingAmount)`).

Otherwise, the ETH is ignored and the function uses WETH from the user.

#### Impact
Note that the `underlyingAmount = bento.toAmount(wETH, amount, true)` is computed from the Bento share price and it might happen that it increases from the time the transaction was submitted to the time the transaction is included in a block.
In that case, it might completely ignore the sent `ETH` balance from the user and in addition transfer the same amount of `WETH` from the user.

The user can lose their `ETH` deposit in the contract.

#### Recommended Mitigation Steps
Each batch must use `refundETH` at the end.

Furthermore, we recommend still depositing `address(this).balance` ETH into Bento and if it's less than `underlyingAmount` use `WETH` only for **the remaining token difference**.

**[maxsam4 (Sushi) acknowledged](https://github.com/code-423n4/2021-09-sushitrident-findings/issues/89)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-sushitrident
- **GitHub**: https://github.com/code-423n4/2021-09-sushitrident-findings/issues/89
- **Contest**: https://code4rena.com/reports/2021-09-sushitrident

### Keywords for Search

`vulnerability`

