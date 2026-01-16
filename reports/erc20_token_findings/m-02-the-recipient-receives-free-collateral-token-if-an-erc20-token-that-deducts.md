---
# Core Classification
protocol: prePO
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6064
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-prepo-contest
source_link: https://code4rena.com/reports/2022-12-prepo
github_link: https://github.com/code-423n4/2022-12-prepo-findings/issues/52

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - fee_on_transfer
  - rebasing_tokens

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - haku
  - Koolex
  - KingNFT
  - SmartSek
  - idkwhatimdoing
---

## Vulnerability Title

[M-02] The recipient receives free collateral token if an ERC20 token that deducts a fee on transfer used as baseToken

### Overview


This bug report is about a vulnerability in the Collateral.sol, DepositHook.sol, and WithdrawHook.sol contracts. The vulnerability occurs when an ERC20 token that deducts a fee on every transfer call is used as the baseToken in the contracts. The vulnerability causes the user to receive more collateral token than they should when depositing, the DepositRecord contract to track wrong user deposit amounts and wrong globalNetDepositAmount, the user to receive less baseToken amount than they should when withdrawing, and the treasury to receive less fee and the user to receive more PPO tokens.

The recommended mitigation steps are to consider calculating the actual amount by recording the balance before and after and then using the actualAmount instead of _amount to perform any further calculations or external calls. This should be applied to the DepositHook and WithdrawHook contracts as well.

### Original Finding Content


<https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/Collateral.sol#L45-L61>

<https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/Collateral.sol#L64-L78>

<https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/DepositHook.sol#L49-L50>

<https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/WithdrawHook.sol#L76-L77>

### Impact

*   There are some ERC20 tokens that deduct a fee on every transfer call. If these tokens are used as baseToken then:
    1.  When depositing into the **Collateral** contract, the recipient will receive collateral token more than what they should receive.

    2.  The **DepositRecord** contract will track wrong user deposit amounts and wrong globalNetDepositAmount as the added amount to both will be always more than what was actually deposited.

    3.  When withdrawing from the **Collateral** contract, the user will receive less baseToken amount than what they should receive.

    4.  The treasury will receive less fee and the user will receive more `PPO` tokens that occur in **DepositHook**  and **WithdrawHook**.

### Proof of Concept

Given:
* baseToken is an ERC20 token that deduct a fee on every transfer call.
* **FoT** is the deducted fee on transfer.

1.  The user deposits baseToken to the **Collateral** contract by calling `deposit` function passing **`\_amount`** as 100e18.
2.  `baseToken.transferFrom` is called to transfer the amount from the user to the contract.
    *   <https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/Collateral.sol#L49>
3.  The contract receives the ``\_amount` - **FoT**. Let's assume the FoT percentage is 1%. Therefore, the actual amount received is 99e18.
4.  When the **DepositHook** is called. the **`\_amount`** passed is 100e18 which is wrong as it should be the actual amount 99e18.
    *   <https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/Collateral.sol#L53>
5.  Calculating **collateralMintAmount** is based on the **`\_amount`**  (100e18- the fee for treasury) which will give the recipient additional collateral token that they shouldn't receive.
    *   <https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/Collateral.sol#L57>

### Recommended Mitigation Steps

1.  Consider calculating the actual amount by recording the balance before and after.

    *   For example:

```sh
uint256 balanceBefore = baseToken.balanceOf(address(this));
baseToken.transferFrom(msg.sender, address(this), _amount);
uint256 balanceAfter = baseToken.balanceOf(address(this));
uint256 actualAmount = balanceAfter - balanceBefore;
```

2.  Then use **actualAmount** instead of **`\_amount`** to perform any further calculations or external calls.

Note: apply the same logic for **DepositHook** and **WithdrawHook** as well at:

*   <https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/DepositHook.sol#L49-L50>

*   <https://github.com/prepo-io/prepo-monorepo/blob/feat/2022-12-prepo/apps/smart-contracts/core/contracts/WithdrawHook.sol#L76-L77>

**[ramenforbreakfast (prePO) confirmed](https://github.com/code-423n4/2022-12-prepo-findings/issues/332)** 

**[Picodes (judge) decreased severity to Medium](https://github.com/code-423n4/2022-12-prepo-findings/issues/52)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | prePO |
| Report Date | N/A |
| Finders | haku, Koolex, KingNFT, SmartSek, idkwhatimdoing, adriro, pavankv |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-prepo
- **GitHub**: https://github.com/code-423n4/2022-12-prepo-findings/issues/52
- **Contest**: https://code4rena.com/contests/2022-12-prepo-contest

### Keywords for Search

`Fee On Transfer, Rebasing Tokens`

