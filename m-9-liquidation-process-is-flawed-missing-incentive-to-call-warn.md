---
# Core Classification
protocol: Aloe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27671
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/120
source_link: none
github_link: https://github.com/sherlock-audit/2023-10-aloe-judging/issues/145

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
finders_count: 1
finders:
  - 0xReiAyanami
---

## Vulnerability Title

M-9: Liquidation process is flawed. missing incentive to call warn

### Overview


The Aloe Protocol has a Liquidation process which involves a grace period for the Borrower. This means, there is a 'warn' function that has to be called, that is setting a 'unleashLiquidationTime'. A Liquidator can only execute a liquidation when this time is reached. The issue is that there is no incentive for anyone to call the 'warn' function, so the Borrower may not get liquidated at all, leading to a loss of funds for the Lender.

The code snippet provided is from the 'Borrower.sol' file, line 148 to line 173. The issue was found by 0xReiAyanami and the impact is that there is no incentive to call 'warn', leading to a potential loss of funds for the Lender.

The issue was discussed by sherlock-admin2, panprog, MohammedRizwan, and chrisling. The recommendation is to incentivize the call of 'warn', to at least pay a small amount of ETH (similar to the ANTE), to ensure liquidation is going to happen.

The issue was fixed by haydenshively in the 'aloe-ii' pull request 209.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-10-aloe-judging/issues/145 

## Found by 
0xReiAyanami

Aloe´s Liquidation process s flawed in the way, that there is no incentive for Liquidators to call the warn function, which is required before liquidations. 

## Vulnerability Detail

The Aloe protocol has a Liquidation process, which involves a grace period for the Borrower.
This means, there is a `warn` function, that has to be called, that is setting a `unleashLiquidationTime`. A Liquidation can only be executed when this time is reached.

Problem is, there is no incentive for anyone to call the `warn` function. Only the actual `liquidate` function is inventiviced by giving a 5% incentive in Tokens, if there is a swap required, and always giving a small amount of ETH (ANTE) to cover the gas cost.

A Liquidator that calls the warn function has no guarantee, that he is the one, that actually can call liquidate, when the time has come. Therefore it would be a waste of Gas to call the warn function.

This might result in a situation where nobody is willing to call `warn`, and therefore the borrower will not get liquidated at all, which could ultimately lead to a loss of Funds for the Lender, when the Borrower starts to accrue bad Debt. 

## Impact

- No incentive to call `warn` --> Borrower will not get liquidated
- Loss of funds for Lender, because Borrower might accrue bad debt


## Code Snippet

https://github.com/sherlock-audit/2023-10-aloe/blob/main/aloe-ii/core/src/Borrower.sol#L148-L173

## Tool used

Manual Review

## Recommendation

Incentivice the call of warn, to at least pay a small amount of eth (similiar to the ANTE), to ensure liquidation is going to happen.






## Discussion

**sherlock-admin2**

3 comment(s) were left on this issue during the judging contest.

**panprog** commented:
> borderline low/medium, but indeed there is no incentive for anyone to call warn

**MohammedRizwan** commented:
>  valid

**chrisling** commented:
>  the best incentive in this case is that liquidators can liquidate after they call warn. The recommendation will only introduce a lot more issues (e.g. malicious actors exploiting the incentive by spamming warn)



**haydenshively**

Fixed in https://github.com/aloelabs/aloe-ii/pull/209

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Aloe |
| Report Date | N/A |
| Finders | 0xReiAyanami |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-10-aloe-judging/issues/145
- **Contest**: https://app.sherlock.xyz/audits/contests/120

### Keywords for Search

`vulnerability`

