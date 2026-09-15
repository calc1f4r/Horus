---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6657
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/147

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
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - obront
  - koxuan
---

## Vulnerability Title

M-10: HardVault never deposits assets to Compound

### Overview


This bug report is about the HardVault protocol, which is a part of the Sherlock Audit 2023-02-blueberry-judging project. The protocol states that all underlying assets should be deposited to their Compound fork to earn interest. However, when the code in the deposit and withdraw functions was examined, it was found that there was no movement of the assets to Compound, meaning users were not earning yield on their underlying tokens. This bug was found and reported by obront and koxuan.

The code snippet linked in the report can be found at https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/vault/HardVault.sol#L68-L116. The tool used to find the bug was manual review.

The impact of this bug is that users of the HardVault protocol are not earning yield on their underlying tokens. To fix the issue, the Hard Vault should be updated to have the assets pulled from the ERC1155 and deposited to the Compound fork, or the comments and documentation should be changed to make it clear that such underlying assets will not be receiving any yield.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/147 

## Found by 
obront, koxuan

## Summary

While the protocol states that all underlying assets are deposited to their Compound fork to earn interest, it appears this action never happens in `HardVault.sol`.

## Vulnerability Detail

The documentation and comments seem to make clear that all assets deposited to `HardVault.sol` should be deposited to Compound to earn yield:

```solidity
/**
    * @notice Deposit underlying assets on Compound and issue share token
    * @param amount Underlying token amount to deposit
    * @return shareAmount cToken amount
    */
function deposit(address token, uint256 amount) { ... }

/**
    * @notice Withdraw underlying assets from Compound
    * @param shareAmount Amount of cTokens to redeem
    * @return withdrawAmount Amount of underlying assets withdrawn
    */
function withdraw(address token, uint256 shareAmount) { ... }
```
However, if we examine the code in these functions, there is no movement of the assets to Compound. Instead, they sit in the Hard Vault and doesn't earn any yield.

## Impact

Users who may expect to be earning yield on their underlying tokens will not be.

## Code Snippet

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/vault/HardVault.sol#L68-L116

## Tool used

Manual Review

## Recommendation

Either add the functionality to the Hard Vault to have the assets pulled from the ERC1155 and deposited to the Compound fork, or change the comments and docs to be clear that such underlying assets will not be receiving any yield.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | obront, koxuan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/147
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`vulnerability`

