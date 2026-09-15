---
# Core Classification
protocol: Buffer Finance
chain: everychain
category: reentrancy
vulnerability_type: reentrancy

# Attack Vector Details
attack_type: reentrancy
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3627
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/24
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/130

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - reentrancy
  - erc777
  - cei

protocol_categories:
  - dexes
  - yield
  - services
  - yield_aggregator
  - options_vault

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - KingNFT
  - HonorLt
  - bin2chen
---

## Vulnerability Title

M-1: resolveQueuedTrades() ERC777 re-enter to steal funds

### Overview


This bug report concerns a vulnerability in the _openQueuedTrade() function of the BufferRouter.sol smart contract. It was found by bin2chen, HonorLt, and KingNFT and is related to the “Checks Effects Interactions” principle. If a tokenX is an ERC777 token, a malicious user could re-enter the cancelQueuedTrade() function to get the token back, as the queuedTrade.isQueued variable would still be true. This could result in the malicious user stealing tokenX.

The code snippet provided in the report shows the original code and the recommended code changes. The original code calls tokenX.transfer() before setting queuedTrade.isQueued to false. In the recommended code, queuedTrade.isQueued is set to false before the tokenX transfer.

The impact of this vulnerability is that if tokenX is an ERC777 token, a malicious user could steal it. The tool used to detect this vulnerability was manual review. The recommendation is to follow the “Checks Effects Interactions” principle when writing code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/130 

## Found by 
bin2chen, HonorLt, KingNFT

## Summary
_openQueuedTrade() does not follow the “Checks Effects Interactions” principle and may lead to re-entry to steal the funds

https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html

## Vulnerability Detail
The prerequisite is that tokenX is ERC777 e.g. “sushi”
1. resolveQueuedTrades() call _openQueuedTrade()
2. in _openQueuedTrade() call "tokenX.transfer(queuedTrade.user)" if (revisedFee < queuedTrade.totalFee) before set queuedTrade.isQueued = false; 
```solidity
    function _openQueuedTrade(uint256 queueId, uint256 price) internal {
...
        if (revisedFee < queuedTrade.totalFee) {
            tokenX.transfer( //***@audit call transfer , if ERC777 , can re-enter ***/
                queuedTrade.user,
                queuedTrade.totalFee - revisedFee
            );
        }

        queuedTrade.isQueued = false;  //****@audit  change state****/
    }
```
3.if ERC777 re-enter to #cancelQueuedTrade() to get tokenX back,it can close,  because queuedTrade.isQueued still equal true
4. back to _openQueuedTrade()  set queuedTrade.isQueued = false
5.so steal tokenX
## Impact
if tokenX equal ERC777 can steal token
## Code Snippet
https://github.com/sherlock-audit/2022-11-buffer/blob/main/contracts/contracts/core/BufferRouter.sol#L350

## Tool used

Manual Review

## Recommendation

follow “Checks Effects Interactions” 

```solidity
    function _openQueuedTrade(uint256 queueId, uint256 price) internal {
...
+      queuedTrade.isQueued = false; 
        // Transfer the fee to the target options contract
        IERC20 tokenX = IERC20(optionsContract.tokenX());
        tokenX.transfer(queuedTrade.targetContract, revisedFee);

-       queuedTrade.isQueued = false; 
        emit OpenTrade(queuedTrade.user, queueId, optionId);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Buffer Finance |
| Report Date | N/A |
| Finders | KingNFT, HonorLt, bin2chen |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/130
- **Contest**: https://app.sherlock.xyz/audits/contests/24

### Keywords for Search

`Reentrancy, ERC777, CEI`

