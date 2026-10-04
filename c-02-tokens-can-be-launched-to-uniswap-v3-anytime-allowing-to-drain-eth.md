---
# Core Classification
protocol: Groupcoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41350
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Groupcoin-security-review.md
github_link: none

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
  - Pashov Audit Group
---

## Vulnerability Title

[C-02] Tokens can be launched to Uniswap v3 anytime, allowing to drain ETH

### Overview


This bug report describes a high severity bug in the code for GroupcoinFactory. The bug allows attackers to launch tokens to Uniswap v3 without meeting the intended criteria, which can result in them taking ETH from the contract and selling their tokens for a higher price. The report recommends fixing the code by ensuring that a specific value is not unset.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

In `GroupcoinFactory`, we intend to gate launching to Uniswap v3 with a two-step approach. First, the user calls `enableUniswapV3Launch`, which only succeeds if the current buy price for one token is at least the `config.thresholdPrice`. Then, it should only be possible to execute `launchGroupCoinToUniswapV3` if we had successfully executed the previous step. However, due to a logical error, it's possible to execute `launchGroupCoinToUniswapV3` without first executing `enableUniswapV3Launch`.

In `launchGroupCoinToUniswapV3`, the following check is intended to only pass if we have enabled the launch in a previous block:

```solidity
if (block.number <= commitLaunch[tokenId]) {
    revert CantLaunchPoolYet();
}
```

However, since the unset value for `commitLaunch[tokenId]` is 0, this will pass for `tokenId`'s which has not been enabled. We can prove this with the following test:

```solidity
function testLaunchToUniswapV3() public {
    bytes32 message = keccak256(abi.encodePacked(address(this), "Telegram WIF Coin", "WIF"));
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(0xbeef, message.toEthSignedMessageHash());
    bytes memory signature = abi.encodePacked(r, s, v);

    (bytes32 salt,) = factory.generateSalt(address(this), "Telegram WIF Coin", "WIF");
    uint256 newToken = factory.launchGroupCoin("Telegram WIF Coin", "WIF", signature, salt, 0);

    // @audit deal ETH so we can add as liquidity
    vm.deal(address(factory), 2 ether);

    factory.launchGroupCoinToUniswapV3(newToken);
}
```

As we can see above, it's possible to launch a token to Uniswap v3 without first enabling it, which means that it doesn't have to meet the intended criteria to be launched. The impact of this is that attackers can atomically buy tokens at the start of the bonding curve for cheap, then launch the token to Uniswap v3, taking ETH from the contract which would be allocated for other tokens' liquidity positions, and finally sell their cheap tokens at the inflated price.

## Recommendations

We must ensure that `commitLaunch[tokenId]` is not unset, e.g.:

```solidity
if (block.number <= commitLaunch[tokenId] || commitLaunch[tokenId] == 0) {
    revert CantLaunchPoolYet();
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Groupcoin |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Groupcoin-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

