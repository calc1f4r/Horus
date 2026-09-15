---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5735
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/275

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - jayphbee
  - cccz
  - corerouter
  - trustindistrust
  - catchup
---

## Vulnerability Title

[M-06] User can free from liquidation fee if its escrow balance is less than the calculated liquidation fee

### Overview


This bug report is about a vulnerability found in the code of the Market.sol file on the GitHub repository code-423n4/2022-10-inverse. The vulnerability allows users to be exempt from the liquidation fee if the escrow balance is less than the calculated liquidation fee. This was discovered through manual review.

The impact of this vulnerability is that the government will not receive the liquidation fee if the user's escrow balance is less than the calculated liquidation fee. The proof of concept for this vulnerability is the code snippet found on lines 605 to 610 of the Market.sol file.

The recommended mitigation steps for this vulnerability is for the user to pay the remaining escrow balance if the calculated liquidation fee is greater than the escrow balance. The code snippet for this recommended mitigation step is included in the bug report.

### Original Finding Content


User can free from liquidation fee if its escrow balance less than the calculated liquidation fee.

### Proof of Concept

If the `liquidationFeeBps` is enabled, the `gov` should receive the liquidation fee. But if user's escrow balance is less than the calculated liquidation fee, `gov` got nothing.<br>
<https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L605-L610>

```solidity
        if(liquidationFeeBps > 0) {
            uint liquidationFee = repaidDebt * 1 ether / price * liquidationFeeBps / 10000;
            if(escrow.balance() >= liquidationFee) {
                escrow.pay(gov, liquidationFee);
            }
        }
```

### Recommended Mitigation Steps

User should pay all the remaining escrow balance if the calculated liquidation fee is greater than its escrow balance.

```solidity
        if(liquidationFeeBps > 0) {
            uint liquidationFee = repaidDebt * 1 ether / price * liquidationFeeBps / 10000;
            if(escrow.balance() >= liquidationFee) {
                escrow.pay(gov, liquidationFee);
            } else {
                escrow.pay(gov, escrow.balance());
            }
        }
```

**[0xean (judge) commented](https://github.com/code-423n4/2022-10-inverse-findings/issues/275#issuecomment-1304642370):**
 > This should amount to dust. 

**[08xmt (Inverse) confirmed and commented](https://github.com/code-423n4/2022-10-inverse-findings/issues/275#issuecomment-1308193523):**
 > Fixed in https://github.com/InverseFinance/FrontierV2/pull/15.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | jayphbee, cccz, corerouter, trustindistrust, catchup |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/275
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Business Logic`

