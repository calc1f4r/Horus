---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7282
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
  - validation

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

validateStack allows any stack to be used with collateral with no liens

### Overview


A critical risk was discovered in the LienToken.sol#L225-232 code which affects the validateStack modifier. This modifier is used to confirm that a stack entered by a user matches the stateHash in storage. The code was found to revert under certain conditions, allowing any collateral with stateHash == bytes32(0) to accept any provided stack as valid. This could be exploited in a number of harmful ways, such as creating liens, making payments, or buying out liens.

To fix this issue, a new condition was added to the validateStack modifier to check if the stateHash is equal to bytes32(0) and the stack length is not equal to 0. If this is the case, the code will revert with the InvalidStates.EMPTY_STATE. Additionally, the InvalidStates.EMPTY_STATE was added to the enum. Astaria and Spearbit have confirmed that this fix has been implemented in PR 194.

### Original Finding Content

## Severity: Critical Risk

## Context
LienToken.sol#L225-232

## Description
The `validateStack` modifier is used to confirm that a stack entered by a user matches the `stateHash` in storage. However, the function reverts under the following conditions:

```solidity
if (stateHash != bytes32(0) && keccak256(abi.encode(stack)) != stateHash) {
    revert InvalidState(InvalidStates.INVALID_HASH);
}
```

The result is that any collateral with `stateHash == bytes32(0)` (which is all collateral without any liens taken against it yet) will accept any provided stack as valid. This can be used in a number of harmful ways. Examples of vulnerable endpoints are:

- **createLien**: If we create the first lien but pass a stack with other liens, those liens will automatically be included in the stack going forward, which means that the collateral holder will owe money they didn't receive.
  
- **makePayment**: If we make a payment on behalf of a collateral with no liens, but include a stack with many liens (all owed to me), the result will be that the collateral will be left with the remaining liens continuing to be owed.
  
- **buyoutLien**: Anyone can call `buyoutLien(...)` and provide parameters that are spoofed but satisfy some constraints so that the call would not revert. This is currently possible due to the issue in this context. As a consequence, the caller can:
    - _mint any unminted liens which can DoS the system.
    - _burn lienIds that they don't have the right to remove.
    - manipulate any public vault's storage (if it has been set as a payee for a lien) through its `handleBuyoutLien`. It seems like this endpoint might have been meant to be a restricted endpoint that only registered vaults can call into. And the caller/user is supposed to only call into here from `VaultImplementation.buyoutLien`.

## Recommendation
```solidity
modifier validateStack(uint256 collateralId, Stack[] memory stack) {
    LienStorage storage s = _loadLienStorageSlot();
    bytes32 stateHash = s.collateralStateHash[collateralId];
    
    if (stateHash == bytes32(0) && stack.length != 0) {
        revert InvalidState(InvalidStates.EMPTY_STATE);
    }
    
    if (stateHash != bytes32(0) && keccak256(abi.encode(stack)) != stateHash) {
        revert InvalidState(InvalidStates.INVALID_HASH);
    }
    _;
}
```
This will also require adding the `InvalidStates.EMPTY_STATE` to the enum.

## Astaria
PR 194.

## Spearbit
Confirmed that this is fixed in the following PR 194.

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

`Validation`

