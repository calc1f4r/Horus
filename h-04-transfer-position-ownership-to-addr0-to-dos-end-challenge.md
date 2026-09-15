---
# Core Classification
protocol: Frankencoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20019
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-frankencoin
source_link: https://code4rena.com/reports/2023-04-frankencoin
github_link: https://github.com/code-423n4/2023-04-frankencoin-findings/issues/670

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - \_\_141345\_\_
---

## Vulnerability Title

[H-04] Transfer position ownership to `addr(0)` to DoS `end()` challenge

### Overview


This bug report is about a potential Denial of Service (DoS) attack in the `end()` call of the challenge in the Position smart contract. If the position owner is about to incur an unavoidable loss, they can transfer the position ownership to `addr(0)` and fail the `end()` call of the challenge, resulting in the successful bidder losing their bid fund and the challenger's collateral being locked and losing the challenge reward. This is possible because the `transfer` in line 268 of the MintingHub.sol will revert due to the requirement in zchf (inherited from `ERC20.sol`) to not transfer to the zero address.

The recommended mitigation steps to prevent this attack is to disallow transferring position ownership to `addr(0)`. This need to prevent transferring to the zero address was already mentioned in the automated findings and was reported by `#935`, however the impact demonstrated in this report is much more severe than the low severity impact identified by other reports and therefore a separate finding is needed.

### Original Finding Content


If some challenge is about to succeed, the position owner will lose the collateral. Seeing the unavoidable loss, the owner can transfer the position ownership to `addr(0)`, fail the `end()` call of the challenge. At the end, the DoS in `end()` will have these impacts:

*   the successful bidder will lose bid fund.
*   the challenger's collateral will be locked, and lose the challenge reward.

### Proof of Concept

Assuming, the position has `minimumCollateral` of 600 zchf, the position owner minted 1,000 zchf against some collateral worth of 1,100 zchf, the highest bid for the collateral was 1,060 zchf, the challenge reward being 50. Then in `Position.sol#notifyChallengeSucceeded()`, the `repayment` will be 1,000, but `effectiveBid` worth of 1,060. The `fundNeeded` will be 1,000 + 50 = 1,050, and results in excess of 1,060 - 1,050 = 10 to refund the position owner in line 268 `MintingHub.sol`. In addition, due to the `minimumCollateral` limit, this challenge cannot be split into smaller ones.

```solidity
File: contracts/MintingHub.sol
252:     function end(uint256 _challengeNumber, bool postponeCollateralReturn) public {

260:         (address owner, uint256 effectiveBid, uint256 volume, uint256 repayment, uint32 reservePPM) = challenge.position.notifyChallengeSucceeded(recipient, challenge.bid, challenge.size);
261:         if (effectiveBid < challenge.bid) {
262:             // overbid, return excess amount
263:             IERC20(zchf).transfer(challenge.bidder, challenge.bid - effectiveBid);
264:         }
265:         uint256 reward = (volume * CHALLENGER_REWARD) / 1000_000;
266:         uint256 fundsNeeded = reward + repayment;
267:         if (effectiveBid > fundsNeeded){
268:             zchf.transfer(owner, effectiveBid - fundsNeeded);

File: contracts/Position.sol
329:     function notifyChallengeSucceeded(address _bidder, uint256 _bid, uint256 _size) external onlyHub returns (address, uint256, uint256, uint256, uint32) {

349:         uint256 repayment = minted < volumeZCHF ? minted : volumeZCHF; // how much must be burned to make things even
350: 
351:         notifyRepaidInternal(repayment); // we assume the caller takes care of the actual repayment
352:         internalWithdrawCollateral(_bidder, _size); // transfer collateral to the bidder and emit update
353:         return (owner, _bid, volumeZCHF, repayment, reserveContribution);
354:     }
```

From the position owner's point of view, the position is on auction and has incurred loss already, only 10 zchf refund left. The owner can give up the tiny amount, and transfer the ownership to `addr(0)` to DoS the `end()` call.

When the position `owner` is `addr(0)`, the transfer in line 268 `MintingHub.sol` will revert, due to the requirement in zchf (inherited from `ERC20.sol`):

```solidity
File: contracts/ERC20.sol
151:     function _transfer(address sender, address recipient, uint256 amount) internal virtual {
152:         require(recipient != address(0));
```

Now the successful bidder can no longer call `end()`. The bid fund will be lost. Also the challenger will lose the collateral because the return call encounter DoS too.

### Recommended Mitigation Steps

Disallow transferring position ownership to `addr(0)`

**[0xA5DF (lookout) commented](https://github.com/code-423n4/2023-04-frankencoin-findings/issues/670#issuecomment-1515987516):**
 > The need to prevent transferring to the zero address is already mentioned in the automated findings and was reported by [`#935`](https://github.com/code-423n4/2023-04-frankencoin-findings/issues/935), however the impact demonstrated in this report is much more severe than the low severity impact identified by other reports and therefore I believe it should be a separate finding.

**[luziusmeisser (Frankencoin) confirmed](https://github.com/code-423n4/2023-04-frankencoin-findings/issues/670#issuecomment-1529044039)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frankencoin |
| Report Date | N/A |
| Finders | \_\_141345\_\_ |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-frankencoin
- **GitHub**: https://github.com/code-423n4/2023-04-frankencoin-findings/issues/670
- **Contest**: https://code4rena.com/reports/2023-04-frankencoin

### Keywords for Search

`vulnerability`

