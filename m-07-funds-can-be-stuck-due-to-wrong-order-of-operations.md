---
# Core Classification
protocol: RabbitHole
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8858
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest
source_link: https://code4rena.com/reports/2023-01-rabbithole
github_link: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/122

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - carrotsmuggler
  - HollaDieWaldfee
  - omis
  - bin2chen
  - ElKu
---

## Vulnerability Title

[M-07] Funds can be stuck due to wrong order of operations

### Overview


This bug report is about the contract ERC20Quest.sol which is responsible for transferring out the fee amount and recovering the remaining tokens in the contract which haven't been claimed yet. The two functions of interest here are `withdrawFee()` and `withdrawRemainingTokens()`. If the owner calls `withdrawFee()` before calling the function `withdrawRemainingTokens()`, the fee will be paid out by the first call, but the same fee amount will still be kept in the contract after the second function call, leading to loss of funds of the owner. This bug is classified as high severity since it is an easy mistake to make. Hardhat was used as the tool for testing. The recommended mitigation step is to only allow fee to be withdrawn after the owner has withdrawn the funds. This can be done by declaring a boolean to check if recovery has happened and setting it to true after the recovery function is called.

### Original Finding Content


<https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Erc20Quest.sol#L102-L104><br>
<https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/Erc20Quest.sol#L81-L87>

The contract `ERC20Quest.sol` has two functions of interest here. The first is `withdrawFee()`, which is responsible for transferring out the fee amount from the contract once endTime has been passed, and the second is `withdrawRemainingTokens()` which recovers the remaining tokens in the contract which haven't been claimed yet.

Function `withdrawRemainingTokens()`:

```solidity
function withdrawRemainingTokens(address to_) public override onlyOwner {
        super.withdrawRemainingTokens(to_);

        uint unclaimedTokens = (receiptRedeemers() - redeemedTokens) * rewardAmountInWeiOrTokenId;
        uint256 nonClaimableTokens = IERC20(rewardToken).balanceOf(address(this)) - protocolFee() - unclaimedTokens;
        IERC20(rewardToken).safeTransfer(to_, nonClaimableTokens);
    }
```

As evident from this excerpt, calling this recovery function subtracts the tokens which are already assigned to someone who completed the quest, and the fee, and returns the rest. However, there is no check for whether the fee has already been paid or not. The owner is expected to first call `withdrawRemainingTokens()`, and then call `withdrawFee()`.

However, if the owner calls `withdrawFee()` before calling the function `withdrawRemainingTokens()`, the fee will be paid out by the first call, but the same fee amount will still be kept in the contract after the second function call, basically making it unrecoverable. Since there are no checks in place to prevent this, this is classified as a high severity since it is an easy mistake to make and leads to loss of funds of the owner.

### Proof of Concept

This can be demonstrated with this test

```javascript
describe('Funds stuck due to wrong order of function calls', async () => {
    it('should trap funds', async () => {
      await deployedFactoryContract.connect(firstAddress).mintReceipt(questId, messageHash, signature)
      await deployedQuestContract.start()
      await ethers.provider.send('evm_increaseTime', [86400])
      await deployedQuestContract.connect(firstAddress).claim()

      await ethers.provider.send('evm_increaseTime', [100001])
      await deployedQuestContract.withdrawFee()
      await deployedQuestContract.withdrawRemainingTokens(owner.address)

      expect(await deployedSampleErc20Contract.balanceOf(deployedQuestContract.address)).to.equal(200)
      expect(await deployedSampleErc20Contract.balanceOf(owner.address)).to.be.lessThan(
        totalRewardsPlusFee * 100 - 1 * 1000 - 200
      )
      await ethers.provider.send('evm_increaseTime', [-100001])
      await ethers.provider.send('evm_increaseTime', [-86400])
    })
  })
```

Even though the fee is paid, the contract still retains the fee amount. The owner receives less than the expected amount. This test is a modification of the test `should transfer non-claimable rewards back to owner` already present in `ERC20Quest.spec.ts`.

### Tools Used

Hardhat

### Recommended Mitigation Steps

Only allow fee to be withdrawn after the owner has withdrawn the funds.

```solidity
// Declare a boolean to check if recovery happened
bool recoveryDone;

function withdrawRemainingTokens(address to_) public override onlyOwner {
        super.withdrawRemainingTokens(to_);

        uint unclaimedTokens = (receiptRedeemers() - redeemedTokens) * rewardAmountInWeiOrTokenId;
        uint256 nonClaimableTokens = IERC20(rewardToken).balanceOf(address(this)) - protocolFee() - unclaimedTokens;
        IERC20(rewardToken).safeTransfer(to_, nonClaimableTokens);
   
        // Set recovery bool
        recoveryDone = true;
    }
function withdrawFee() public onlyAdminWithdrawAfterEnd {
        // Check recovery
        require(recoveryDone,"Recover tokens before withdrawing Fees");
        IERC20(rewardToken).safeTransfer(protocolFeeRecipient, protocolFee());
    }
```

**[waynehoover (RabbitHole) disagreed with severity and commented](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/122#issuecomment-1440966653):**
 > I agree that this is an issue, but not a high risk issue. I expect high risk issues to be issues that can be called by anyone, not owners.
> 
> As owners there are plenty of ways we can sabotage our contracts (for example via the set* functions) it is an issue for an owner.
> 
> The owner understands how these functions work, so they can be sure to call them in the right order.

**[kirk-baird (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-01-rabbithole-findings/issues/122#issuecomment-1442582881):**
 > I agree with the sponsor that since this is an `onlyOwner` function that medium severity is more appropriate.
> 
> The likelihood of this issue is reduced as it can only be called by the owner.
> 
> Note: the ineffective `onlyAdminWithdrawAfterEnd` modifier not validating admin is raised in another issue.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | RabbitHole |
| Report Date | N/A |
| Finders | carrotsmuggler, HollaDieWaldfee, omis, bin2chen, ElKu, evan, hansfriese, peanuts, hl_, KmanOfficial, Iurii3, adriro, AkshaySrivastav, mert_eren |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-rabbithole
- **GitHub**: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/122
- **Contest**: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest

### Keywords for Search

`vulnerability`

