---
# Core Classification
protocol: Buffer Finance
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3630
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/24
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/76

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 5

# Context Tags
tags:
  - fee_on_transfer
  - erc20

protocol_categories:
  - dexes
  - yield
  - services
  - yield_aggregator
  - options_vault

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - supernova
  - pashov
  - Deivitto
  - cccz
  - KingNFT
---

## Vulnerability Title

M-4: Insufficient support for fee-on-transfer tokens

### Overview


This bug report is about the ```BufferBinaryPool.sol``` and ```BufferRouter.sol``` not supporting fee-on-transfer tokens. Fee-on-transfer tokens are tokens that take a fee from the amount sent by the user, meaning the contract receives less than the amount specified in the transfer. This could lead to the protocol and users suffering a loss of funds.

The issue was found by a team of 10 people, and the code snippets linked in the report were reviewed manually. The recommendation is to check the balance of the contract before and after token transfers. It is not intended to support fee-on-transfer tokens for now.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/76 

## Found by 
eierina, dipp, KingNFT, rvierdiiev, cccz, supernova, Deivitto, \_\_141345\_\_, jonatascm, pashov

## Summary

The ```BufferBinaryPool.sol``` and ```BufferRouter.sol``` do not support fee-on-transfer tokens. If ```tokenX``` is a fee-on-transfer token, tokens received from users could be less than the amount specified in the transfer.

## Vulnerability Detail

The ```initiateTrade``` function in ```BufferRouter.sol``` receives tokens from the user with amount set to ```initiateTrade```'s ```totalFee``` input. If tokenX is a fee-on-transfer token then the actual amount received by ```BufferRouter.sol``` is less than ```totalFee```. When a trade is opened, the protocol will [send a settlementFee to ```settlementFeeDisbursalContract```](https://github.com/sherlock-audit/2022-11-buffer/blob/main/contracts/contracts/core/BufferBinaryOptions.sol#L137-L141) and a [premium to ```BufferBinaryPool.sol```](), where the settlementFee is calculated using the incorrect, inflated totalFee amount. When the totalFee is greater than the fee required [the user is reimbursed the difference](https://github.com/sherlock-audit/2022-11-buffer/blob/main/contracts/contracts/core/BufferRouter.sol#L333-L339). Since the settlementFee is greater than it should be the user receives less reimbursement.

In ```BufferBinaryPool.sol```'s ```lock``` function, the premium for the order is sent from the Options contract to the Pool. The totalPremium state variable would be updated incorrectly if fee-on-transfer tokens were used.

The ```_provide``` function in ```BufferBinaryPool.sol```receives tokenXAmount of tokenX tokens from the user and calculates the amount of shares to mint using the tokenXAmount. If fee-on-transfer tokens are used then the user would receive more shares than they should.

## Impact

The protocol and users could suffer a loss of funds.

## Code Snippet

[BufferRouter.sol#L86-L90](https://github.com/sherlock-audit/2022-11-buffer/blob/main/contracts/contracts/core/BufferRouter.sol#L86-L90)

[BufferBinaryPool.sol#L161](https://github.com/sherlock-audit/2022-11-buffer/blob/main/contracts/contracts/core/BufferBinaryPool.sol#L161)

[BufferBinaryPool.sol#L236-L240](https://github.com/sherlock-audit/2022-11-buffer/blob/main/contracts/contracts/core/BufferBinaryPool.sol#L161)

## Tool used

Manual Review

## Recommendation

Consider checking the balance of the contract before and after token transfers and using instead of the amount specified in the contract.

## Discussion

**0x00052**

Only an issue if project intends to support fee-on-transfer tokens as underlying

**bufferfinance**

Not supporting fee-on-transfer tokens for now.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Buffer Finance |
| Report Date | N/A |
| Finders | supernova, pashov, Deivitto, cccz, KingNFT, dipp, \_\_141345\_\_, rvierdiiev, jonatascm, eierina |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/76
- **Contest**: https://app.sherlock.xyz/audits/contests/24

### Keywords for Search

`Fee On Transfer, ERC20`

