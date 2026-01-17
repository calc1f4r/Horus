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
solodit_id: 41349
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

[C-01] Uniswap v3 launch can be enabled without raising enough ETH

### Overview


This bug report discusses an issue with the `enableUniswapV3Launch` function in a smart contract. This function can only be used if a certain amount of ETH has been paid to purchase the token, but it has been found that users can purchase a lower amount of tokens than needed to meet this requirement. This can lead to the contract becoming insolvent and unable to launch Uniswap v3. The recommended solution is to limit the use of `enableUniswapV3Launch` based on the total number of tokens purchased to ensure enough ETH has been paid.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

`enableUniswapV3Launch` can only be executed if `unitPrice >= config.thresholdPrice`, which is implicitly intended to enforce that at least `config.token1Amount` ETH has been paid to purchase the given token. It's important that enough ETH has been paid so that we have enough to supply liquidity. However, users only need to buy ~8,200,000 tokens for the `unitPrice` to meet the `thresholdPrice`, which is ~155,000 tokens less than we need to sell to have sufficient ETH. We can prove this with the following test:

```solidity
function testLaunchToUniswapV3() public {
    bytes32 message = keccak256(abi.encodePacked(address(this), "Telegram WIF Coin", "WIF"));
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(0xbeef, message.toEthSignedMessageHash());
    bytes memory signature = abi.encodePacked(r, s, v);

    (bytes32 salt,) = factory.generateSalt(address(this), "Telegram WIF Coin", "WIF");
    uint256 newToken = factory.launchGroupCoin("Telegram WIF Coin", "WIF", signature, salt, 0);
    uint256 price = factory.getBuyPriceAfterFee(newToken, 8_357_142);

    vm.deal(User01, price);
    vm.startPrank(User01);

    factory.buy{ value: price }(newToken, 8_200_000);

    factory.enableUniswapV3Launch(newToken);
}
```

Since it's not possible to `buy` more tokens after a launch is committed, the only way to successfully launch Uniswap v3 after an early commit like this is to use additional ETH in the contract raised by other tokens, if available, making the contract insolvent.

## Recommendations

The best solution to this is likely to gate `enableUniswapV3Launch` according to the `totalSupply` of the token such that we can be certain that enough ETH has been paid to buy the tokens.

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

