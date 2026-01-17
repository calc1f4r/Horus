---
# Core Classification
protocol: Sentiment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3361
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1
source_link: none
github_link: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/035-M

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
finders_count: 7
finders:
  - IllIllI
  - PwnPatrol
  - xiaoming90
  - Lambda
  - ellahi
---

## Vulnerability Title

M-5: Balances of rebasing tokens aren't properly tracked

### Overview


This bug report is about a vulnerability in the Sentiment platform which is not properly tracking balance changes while rebasing tokens are in the borrower's account. This means that the lender will miss out on gains that should have accrued to them while the asset was lent out. The code snippet from the report shows that the Lending tracks shares of the LToken but repayment assumes that shares are equal to the same amount, regardless of which address held them. This is not true for airdrops. The team recommends that the admins should adjust share amounts when the account balance doesn't match the share conversion calculation when taking into account gains made by the borrower. The admins should also make sure not to interact with fee-on-transfer tokens and should not add rebasing/fee-on-transfer tokens to any allowed lists.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/035-M 
## Found by 
Lambda, JohnSmith, PwnPatrol, IllIllI, xiaoming90, ellahi, bytehat

## Summary
Rebasing tokens are tokens where `balanceOf()` returns larger amounts over time, due to the addition of interest to each account, or due to airdrops

## Vulnerability Detail
Sentiment doesn't properly track balance changes while rebasing tokens are in the borrower's account

## Impact
The lender will miss out on gains that should have accrued to them while the asset was lent out. While market-based price corrections may be able to handle interest that is accrued to everyone, market approaches won't work when only subsets of token addresses are given rewards, e.g. an airdrop based on a snapshot of activity that happened prior to the token being lent.

## Code Snippet
Lending tracks shares of the LToken:
https://github.com/sherlock-audit/2022-08-sentiment/blob/main/protocol/src/tokens/LToken.sol#L140-L143

But repayment assumes that shares are equal to the same amount, regardless of which address held them, which is not true for airdrops:
https://github.com/sherlock-audit/2022-08-sentiment/blob/main/protocol/src/tokens/LToken.sol#L160-L163

Rebasing tokens are supported, since Aave is a rebasing token:
https://github.com/sherlock-audit/2022-08-sentiment/blob/main/controller/src/aave/AaveEthController.sol#L28
## Tool used

Manual Review

## Recommendation
Adjust share amounts when the account balance doesn't match the share conversion calculation when taking into account gains made by the borrower

## Sentiment Team
We'll make sure to not interact with fee-on-transfer tokens. This can be ensured by the admins.

## Lead Senior Watson
Note: The admins should not add rebasing/fee-on-transfer tokens to any allowed lists.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment |
| Report Date | N/A |
| Finders | IllIllI, PwnPatrol, xiaoming90, Lambda, ellahi, bytehat, JohnSmith |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/035-M
- **Contest**: https://app.sherlock.xyz/audits/contests/1

### Keywords for Search

`vulnerability`

