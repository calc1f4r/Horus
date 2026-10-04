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
solodit_id: 41353
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Groupcoin-security-review.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Expected `totalSupply` of 10M tokens not reached after launching to Uniswap v3

### Overview


This bug report discusses an issue with the Groupcoin token after launching it on Uniswap v3. The expected total supply of the token is 10,000,000, but testing has shown that it never reaches this amount. Even when buying the maximum amount of tokens, the total supply is still less than 10M. Additionally, it is possible to launch Uniswap v3 with less than the maximum amount of tokens due to a configuration setting. The report recommends adjusting the code to mint the remaining tokens needed to reach the desired total supply.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

The expected `totalSupply` of Groupcoin after launching to Uniswap v3 is 10,000,000. However, we can validate from testing that we never actually quite reach 10,000,000. We can see from the result of the below test that even if we buy the maximum amount of tokens, we will still have a `totalSupply` of less than 10M:

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

    factory.buy{ value: price }(newToken, 8_357_111);

    factory.enableUniswapV3Launch(newToken);

    vm.roll(block.number + 1);

    factory.launchGroupCoinToUniswapV3(newToken);

    Groupcoin coin = factory.addressOf(newToken);
    assertEq(coin.totalSupply(), 10_000_000 ether);
}
```

Furthermore, we can buy >2000 tokens less than the maximum amount since we will reach the `config.thresholdPrice` before then, allowing us to launch Uniswap v3 regardless:

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

    // @audit we buy less tokens and yet we can still launch
    factory.buy{ value: price }(newToken, 8_355_000);

    factory.enableUniswapV3Launch(newToken);

    vm.roll(block.number + 1);

    factory.launchGroupCoinToUniswapV3(newToken);

    Groupcoin coin = factory.addressOf(newToken);
    assertEq(coin.totalSupply(), 10_000_000 ether);
}
```

In the above test, we only end up with a `totalSupply` of ~9,997,888 Groupcoins.

## Recommendations

In `launchGroupCoinToUniswapV3`, instead of minting a hardcoded amount of Groupcoins, we should mint `10_000_000 ether - token.totalSupply()`, e.g.:

```solidity
token.mint(address(this), 10_000_000 ether - token.totalSupply());
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

