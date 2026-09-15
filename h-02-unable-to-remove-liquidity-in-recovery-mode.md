---
# Core Classification
protocol: Malt Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1092
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-malt-finance-contest
source_link: https://code4rena.com/reports/2021-11-malt
github_link: https://github.com/code-423n4/2021-11-malt-findings/issues/323

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 1

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - gzeon
---

## Vulnerability Title

[H-02] Unable to remove liquidity in Recovery Mode

### Overview


This bug report is about the Malt protocol, which is a protocol for trading on decentralized exchanges. The bug is that when the Malt price TWAP drops below a certain threshold, the protocol will revert any transaction that tries to remove Malt from the AMM pool. The recommended mitigation step is to have liquidity removed to the UniswapHandler contract, and then the proceed is sent to msg.sender. This will ensure that the transaction will not be reverted.

### Original Finding Content

_Submitted by gzeon_

According to <https://github.com/code-423n4/2021-11-malt#high-level-overview-of-the-malt-protocol>

> When the Malt price TWAP drops below a specified threshold (eg 2% below peg) then the protocol will revert any transaction that tries to remove Malt from the AMM pool (ie buying Malt or removing liquidity). Users wanting to remove liquidity can still do so via the UniswapHandler contract that is whitelisted in recovery mode.

However, in <https://github.com/code-423n4/2021-11-malt/blob/c3a204a2c0f7c653c6c2dda9f4563fd1dc1cecf3/src/contracts/DexHandlers/UniswapHandler.sol#L236>
liquidity removed is directly sent to msg.sender, which would revert if it is not whitelisted
<https://github.com/code-423n4/2021-11-malt/blob/c3a204a2c0f7c653c6c2dda9f4563fd1dc1cecf3/src/contracts/PoolTransferVerification.sol#L53>

#### Recommended Mitigation Steps

Liquidity should be removed to UniswapHandler contract, then the proceed is sent to msg.sender


**[0xScotch (sponsor) confirmed](https://github.com/code-423n4/2021-11-malt-findings/issues/323)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-11-malt-findings/issues/323#issuecomment-1010448871):**
 > I believe this finding to be correct, because of the whitelisting on `verifyTransfer`, during recovery mode the removal of liquidity from UniSwapV2Pair will perform safeTransfers: https://github.com/Uniswap/v2-core/blob/4dd59067c76dea4a0e8e4bfdda41877a6b16dedc/contracts/UniswapV2Pair.sol#L148
> 
> This means that the `_beforeTokenTransfer` will be called which eventually will call `verifyTransfer` which, if the price is below peg will revert.
> 
> Transfering the funds to the whitelisted contract should avoid this issue.
> 
> 
> I'd like to remind the sponsor that anyone could deploy similar swapping contracts (or different ones such as curve), so if a person is motivate enough, all the whitelisting could technically be sidestepped.
> 
> That said, given the condition of LPing on Uniswap, the check and the current system would make it impossible to withdraw funds.
> 
> Because this does indeed compromises the availability of funds (effectively requiring the admin to unstock them manually via Whitelisting each user), I agree with High Severity





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 1/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Finance |
| Report Date | N/A |
| Finders | gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-malt
- **GitHub**: https://github.com/code-423n4/2021-11-malt-findings/issues/323
- **Contest**: https://code4rena.com/contests/2021-11-malt-finance-contest

### Keywords for Search

`vulnerability`

