---
# Core Classification
protocol: Isomorph
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5690
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/22
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/51

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - access_control
  - business_logic

protocol_categories:
  - liquid_staking
  - yield
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - HollaDieWaldfee
  - 0x52
---

## Vulnerability Title

H-7: User can steal rewards from other users by withdrawing their Velo Deposit NFTs from other users' depositors

### Overview


This bug report discusses an issue where a malicious user can steal rewards from other users by withdrawing their Velo Deposit NFTs from other users' depositors. This vulnerability exists because the `Depositor#withdrawFromGauge` allows any user to withdraw any NFT that was minted by the same `DepositReciept`. This means that a malicious user can deposit to their `Depositor` then withdraw their NFT through the `Depositor` of another user's `Depositor` that uses the same `DepositReciept`. The net effect is that the tokens will remained staked to the attackers `Depositor` allowing them to steal all the other user's rewards. To fix this issue, the code was changed to add checks on lines 82 and 123 that validate any depositReceipt being withdrawn was originally minted by that Depositor contract.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/51 

## Found by 
0x52, HollaDieWaldfee

## Summary

Rewards from staking AMM tokens accumulate to the depositor used to deposit them. The rewards accumulated by a depositor are passed to the owner when they claim. A malicious user to steal the rewards from other users by manipulating other users depositors. Since any NFT of a DepositReceipt can be withdrawn from any depositor with the same DepositReceipt, a malicious user could mint an NFT on their depositor then withdraw in from another user's depositor. The net effect is that that the victims deposits will effectively be in the attackers depositor and they will collect all the rewards.

## Vulnerability Detail

    function withdrawFromGauge(uint256 _NFTId, address[] memory _tokens)  public  {
        uint256 amount = depositReceipt.pooledTokens(_NFTId);
        depositReceipt.burn(_NFTId);
        gauge.getReward(address(this), _tokens);
        gauge.withdraw(amount);
        //AMMToken adheres to ERC20 spec meaning it reverts on failure, no need to check return
        //slither-disable-next-line unchecked-transfer
        AMMToken.transfer(msg.sender, amount);
    }

Every user must create a `Depositor` using `Templater` to interact with vaults and take loans. `Depositor#withdrawFromGauge` allows any user to withdraw any NFT that was minted by the same `DepositReciept`. This is where the issues arises. Since rewards are accumulated to the `Depositor` in which the underlying is staked a user can deposit to their `Depositor` then withdraw their NFT through the `Depositor` of another user's `Depositor` that uses the same `DepositReciept`. The effect is that the tokens will remained staked to the attackers `Depositor` allowing them to steal all the other user's rewards.

Example:
`User A` and `User B` both create a `Depositor` for the same `DepositReciept`. Both users deposit 100 tokens into their respective `Depositors`. `User B` now calls `withdrawFromGauge` on `Depositor A`. `User B` gets their 100 tokens back and `Depositor B` still has 100 tokens deposited in it. `User B` cannot steal these tokens but they are now collecting the yield on all 100 tokens via `Depositor B` and `User A` isn't getting any rewards at all because `Depositor A` no longer has any tokens deposited into Velodrome gauge.

## Impact

Malicious user can steal other user's rewards

## Code Snippet

https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Velo-Deposit-Tokens/contracts/Depositor.sol#L119-L127

## Tool used

Manual Review

## Recommendation

Depositors should only be able to burn NFTs that they minted. Change DepositReciept_Base#burn to enforce this:

        function burn(uint256 _NFTId) external onlyMinter{
    +       //tokens must be burned by the depositor that minted them
    +       address depositor = relatedDepositor[_NFTId];
    +       require(depositor == msg.sender, "Wrong depositor");
            require(_isApprovedOrOwner(msg.sender, _NFTId), "ERC721: caller is not token owner or approved");
            delete pooledTokens[_NFTId];
            delete relatedDepositor[_NFTId];
            _burn(_NFTId);
        }


## Discussion

**kree-dotcom**

Sponsor confirmed, will fix. Appears to be a duplicate of issue #43 's footnote.

**kree-dotcom**

Fixed https://github.com/kree-dotcom/Velo-Deposit-Tokens/commit/23ff5653b555b11c9f4dead7ff5a72d50eac5788

We have taken a different approach to that suggested by the auditor, theirs looked valid though. 
We added the checks on lines 82 and 123 that validate any depositReceipt being withdrawn was originally minted by that Depositor contract. Other lines changed in this commit relate to #47 .

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Isomorph |
| Report Date | N/A |
| Finders | HollaDieWaldfee, 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/51
- **Contest**: https://app.sherlock.xyz/audits/contests/22

### Keywords for Search

`Access Control, Business Logic`

