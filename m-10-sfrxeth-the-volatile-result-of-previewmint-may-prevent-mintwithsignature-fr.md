---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25447
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-frax
source_link: https://code4rena.com/reports/2022-09-frax
github_link: https://github.com/code-423n4/2022-09-frax-findings/issues/35

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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-10] sfrxETH: The volatile result of previewMint() may prevent mintWithSignature from working

### Overview


This bug report is about the sfrxETH contracts, which are used in Frax, a decentralized finance protocol. The bug is related to the `previewMint()` function, which changes its result with the state of the contract. This causes the value of amount to be volatile in the mintWithSignature function when approveMax is false. This means that when using the mintWithSignature function, which requires the user to sign for an accurate amount value, if the amount used differs from the result of previewMint(), mintWithSignature will not work.

To illustrate this, consider the following scenario: User A signs using amount = 1000 and calls the mintWithSignature function. During execution, the previous transaction in the same block changes the state of the contract so that previewMint(shares) == 1001, so the transaction is reverted due to a signature check failure.

The recommended mitigation steps for this bug are to consider that in the mintWithSignature function, the user provides a maxAmount, and then requires maxAmount >= previewMint(shares) and uses maxAmount to verify the signature. FortisFortuna (Frax) acknowledged this bug and commented that they will allow user-defined slippage on the UI. 0xean (judge) commented that they don't believe the UI will be able to assist with this issue unless modifications are made to the smart contracts. 

In conclusion, this bug report is about the sfrxETH contracts, which are used in Frax, a decentralized finance protocol. The bug is related to the `previewMint()` function, which changes its result with the state of the contract, causing the value of amount to be volatile in the mintWithSignature function when approveMax is false. The recommended mitigation steps are to consider that in the mintWithSignature function, the user provides a maxAmount, and then requires maxAmount >= previewMint(shares) and uses maxAmount to verify the signature.

### Original Finding Content

_Submitted by cccz, also found by rotcivegaf, Trust, and wagmi_

In sfrxETH contracts, the result of `previewMint()` changes with the state of the contract, which causes the value of amount to be volatile in the mintWithSignature function when approveMax is false.

And when using the mintWithSignature function, which requires the user to sign for an accurate amount value, when the amount used differs from the result of previewMint(), mintWithSignature will not work.

Consider the following scenarios.

User A signs using amount = 1000 and calls the mintWithSignature function.

During execution, the previous transaction in the same block changes the state of the contract so that previewMint(shares) == 1001, so the transaction is reverted due to a signature check failure.

### Proof of Concept

<https://github.com/code-423n4/2022-09-frax/blob/55ea6b1ef3857a277e2f47d42029bc0f3d6f9173/src/sfrxETH.sol#L75-L87>

<https://github.com/transmissions11/solmate/blob/bff24e835192470ed38bf15dbed6084c2d723ace/src/mixins/ERC4626.sol#L140-L144>

### Recommended Mitigation Steps

Consider that in the mintWithSignature function, the user provides a maxAmount, and then requires maxAmount >= previewMint(shares) and uses maxAmount to verify the signature.

**[FortisFortuna (Frax) acknowledged and commented](https://github.com/code-423n4/2022-09-frax-findings/issues/35#issuecomment-1257310689):**
 > Technically correct, though in practice, we will allow user-defined slippage on the UI.

**[0xean (judge) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/35#issuecomment-1276247147):**
 > I don't believe the UI will be able to assist with this issue unless modifications are made to the smart contracts. The signature will become invalidated due to the return value of `previewMint()` changing while the transaction is waiting to be included in a block.  



***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-frax
- **GitHub**: https://github.com/code-423n4/2022-09-frax-findings/issues/35
- **Contest**: https://code4rena.com/reports/2022-09-frax

### Keywords for Search

`vulnerability`

