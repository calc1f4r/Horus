---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7308
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic
  - validation
  - eip-4626
  - erc4626

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

WithdrawProxy allows redemptions before PublicVault callstransferWithdrawReserve

### Overview


This bug report is about the WithdrawProxy.sol#L172-L175. It states that if anyone transfers WETH to the contract, totalAssets() will become greater than 0, and if someone attempts to redeem their shares then they will receive a smaller share than they are owed. It then explains the exploit scenario and provides two recommendations. 

The first recommendation is to consider being explicit in opening the WithdrawProxy for redemptions by requiring s.withdrawReserveReceived to be a non-zero value. The second recommendation is to explicitly mark the withdraws as open when it is both safe to withdraw and the vault has claimed its share. 

In conclusion, this bug report is about a vulnerability in the WithdrawProxy.sol#L172-L175 that can lead to a malicious actor manipulating the totalAssets() and resulting in users receiving a smaller share than they are owed. It provides two recommendations to fix the issue.

### Original Finding Content

## Severity: High Risk

## Context
`WithdrawProxy.sol#L172-L175`

## Description
Anytime there is a withdrawal pending (i.e., someone holds WithdrawProxy shares), shares may be redeemed as long as `totalAssets() > 0` and `s.finalAuctionEnd == 0`. Under normal operating conditions, `totalAssets()` becomes greater than 0 when the `PublicVault` calls `transferWithdrawReserve`. 

`totalAssets()` can also be increased to a non-zero value by anyone transferring WETH to the contract. If this occurs and a user attempts to redeem, they will receive a smaller share than they are owed.

### Exploit Scenario
- Depositor redeems from `PublicVault` and receives WithdrawProxy shares.
- Malicious actor deposits a small amount of WETH into the WithdrawProxy.
- Depositor accidentally redeems, or is tricked into redeeming, from the WithdrawProxy while `totalAssets()` is smaller than it should be.
- `PublicVault` properly processes epoch and full `withdrawReserve` is sent to the WithdrawProxy.
- All remaining holders of WithdrawProxy shares receive an outsized share as the previous shares were redeemed for the incorrect value.

## Recommendation

### Option 1
Consider being explicit in opening the WithdrawProxy for redemptions (`redeem/withdraw`) by requiring `s.withdrawReserveReceived` to be a non-zero value:

```solidity
if (s.finalAuctionEnd != 0) {
    // Updated condition
    if (s.finalAuctionEnd != 0 || s.withdrawReserveReceived == 0) {
        // if finalAuctionEnd is 0, no auctions were added
        revert InvalidState(InvalidStates.NOT_CLAIMED);
    }
}
```
Astaria notes there is a second scenario where funds are sent to the WithdrawProxy: auction payouts. For the above recommendation to be complete, auction payouts or claiming MUST also set `withdrawReserveReceived`.

### Option 2
Instead of inferring when it is safe to withdraw based on `finalAuctionEnd` and `withdrawReserveReceived`, consider explicitly marking the withdrawals as open when it is both safe to withdraw (i.e., expected funds deposited) and the vault has claimed its share.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic, Validation, EIP-4626, ERC4626`

