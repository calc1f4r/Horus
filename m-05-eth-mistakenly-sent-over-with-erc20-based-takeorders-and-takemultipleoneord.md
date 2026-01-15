---
# Core Classification
protocol: Infinity NFT Marketplace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2782
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-infinity-nft-marketplace-contest
source_link: https://code4rena.com/reports/2022-06-infinity
github_link: https://github.com/code-423n4/2022-06-infinity-findings/issues/346

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
  - dexes
  - cross_chain
  - payments
  - nft_marketplace
  - gaming

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - obtarian
  - VAD37
  - 0xsanson
---

## Vulnerability Title

[M-05] ETH mistakenly sent over with ERC20 based `takeOrders` and `takeMultipleOneOrders` calls will be lost

### Overview


A bug has been identified in the code of the InfinityExchange.sol contract, which could potentially lead to a user permanently losing their ETH funds. This bug occurs when a user attempts to make an order using ETH, and the `currency` passed in the call is a ERC20 token. In this case, the `msg.value` will be permanently frozen within the contract, as the code only checks that `msg.value` is enough to cover the order's `totalPrice`.

The severity of this bug has been set to medium, as it is a permanent fund freeze scenario that is conditional on a user mistake, and the probability of it occurring is deemed high enough as the same functions are used for both ETH and ERC20 orders.

To mitigate this bug, the code should be modified to include a check for `msg.value` to be zero for cases when it is not utilized. The recommended code is provided in the bug report.

### Original Finding Content

_Submitted by obtarian, also found by 0xsanson, cccz, and VAD37_

<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L323-L327>

<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L359-L363>

### Vulnerability details

`takeOrders()` and `takeMultipleOneOrders()` are the main user facing functionality of the protocol. Both require `currency` to be fixed for the call and can have it either as a ERC20 token or ETH. This way, the probability of a user sending over a ETH with the call whose `currency` is a ERC20 token isn't negligible. However, in this case ETH funds of a user will be permanently lost.

Setting the severity to medium as this is permanent fund freeze scenario conditional on a user mistake, which probability can be deemed high enough as the same functions are used for ETH and ERC20 orders.

### Proof of Concept

Both takeOrders() and takeMultipleOneOrders() only check that ETH funds are enough to cover the order's `totalPrice`:

<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L323-L327>

```solidity
    // check to ensure that for ETH orders, enough ETH is sent
    // for non ETH orders, IERC20 safeTransferFrom will throw error if insufficient amount is sent
    if (isMakerSeller && currency == address(0)) {
      require(msg.value >= totalPrice, 'invalid total price');
    }
```

<https://github.com/code-423n4/2022-06-infinity/blob/765376fa238bbccd8b1e2e12897c91098c7e5ac6/contracts/core/InfinityExchange.sol#L359-L363>

```solidity
    // check to ensure that for ETH orders, enough ETH is sent
    // for non ETH orders, IERC20 safeTransferFrom will throw error if insufficient amount is sent
    if (isMakerSeller && currency == address(0)) {
      require(msg.value >= totalPrice, 'invalid total price');
    }
```

When `currency` is some ERC20 token, while `msg.value > 0`, the `msg.value` will be permanently frozen within the contract.

### Recommended Mitigation Steps

Consider adding the check for `msg.value` to be zero for the cases when it is not utilized:

```solidity
    // check to ensure that for ETH orders, enough ETH is sent
    // for non ETH orders, IERC20 safeTransferFrom will throw error if insufficient amount is sent
    if (isMakerSeller && currency == address(0)) {
      require(msg.value >= totalPrice, 'invalid total price');
    } else {
      require(msg.value == 0, 'non-zero ETH value');
    }
```

**[nneverlander (Infinity) confirmed](https://github.com/code-423n4/2022-06-infinity-findings/issues/346)**

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-06-infinity-findings/issues/346#issuecomment-1179723118):**
 > When accepting an order using ERC20 tokens, any ETH included will be accepted as exchange fees instead of reverting the tx or refunding to the user.
> 
> This is a result of user error, but leads to a direct loss of funds. Accepting as a Medium risk submission.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Infinity NFT Marketplace |
| Report Date | N/A |
| Finders | cccz, obtarian, VAD37, 0xsanson |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-infinity
- **GitHub**: https://github.com/code-423n4/2022-06-infinity-findings/issues/346
- **Contest**: https://code4rena.com/contests/2022-06-infinity-nft-marketplace-contest

### Keywords for Search

`vulnerability`

