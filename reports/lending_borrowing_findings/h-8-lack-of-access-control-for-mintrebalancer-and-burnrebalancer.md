---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19137
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/777

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 0

# Context Tags
tags:
  - access_control

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 109
finders:
  - J4de
  - Dug
  - 0xSmartContract
  - shaka
  - nobody2018
---

## Vulnerability Title

H-8: Lack of access control for `mintRebalancer()` and `burnRebalancer()`

### Overview


This bug report is about the lack of access control in the `USSD.mintRebalancer()` and `USSD.burnRebalancer()` functions, which can be found in the USSD smart contract. This vulnerability was discovered by a group of security auditors, including 0x2e, 0xAzez, 0xHati, 0xMojito, 0xPkhatri, 0xRobocop, 0xSmartContract, 0xStalin, 0xeix, 0xyPhilic, 14si2o\_Flint, AlexCzm, Angry\_Mustache\_Man, Aymen0909, Bahurum, Bauchibred, Bauer, BlockChomper, Brenzee, BugBusters, BugHunter101, Delvir0, DevABDee, Dug, Fanz, GimelSec, HonorLt, J4de, JohnnyTime, Juntao, Kodyvim, Kose, Lilyjjo, Madalad, Nyx, PokemonAuditSimulator, RaymondFam, Saeedalipoor01988, SanketKogekar, Schpiel, SensoYard, T1MOH, TheNaubit, Tricko, VAD37, Vagner, WATCHPUG, \_\_141345\_\_, anthony, ast3ros, auditsea, berlin-101, blackhole, blockdev, carrotsmuggler, chainNue, chalex.eth, cjm00n, coincoin, coryli, ctf\_sec, curiousapple, dacian, evilakela, georgits, giovannidisiena, immeas, innertia, jah, juancito, kie, kiki\_dev, lil.eth, m4ttm, mahdikarimi, mrpathfindr, n33k, neumo, ni8mare, nobody2018, pavankv241, pengun, qbs, qckhp, qpzm, ravikiran.web3, saidam017, sam\_gmk, sashik\_eth, shaka, shealtielanz, shogoki, simon135, slightscan, smiling\_heretic, tallo

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/777 

## Found by 
0x2e, 0xAzez, 0xHati, 0xMojito, 0xPkhatri, 0xRobocop, 0xSmartContract, 0xStalin, 0xeix, 0xyPhilic, 14si2o\_Flint, AlexCzm, Angry\_Mustache\_Man, Aymen0909, Bahurum, Bauchibred, Bauer, BlockChomper, Brenzee, BugBusters, BugHunter101, Delvir0, DevABDee, Dug, Fanz, GimelSec, HonorLt, J4de, JohnnyTime, Juntao, Kodyvim, Kose, Lilyjjo, Madalad, Nyx, PokemonAuditSimulator, RaymondFam, Saeedalipoor01988, SanketKogekar, Schpiel, SensoYard, T1MOH, TheNaubit, Tricko, VAD37, Vagner, WATCHPUG, \_\_141345\_\_, anthony, ast3ros, auditsea, berlin-101, blackhole, blockdev, carrotsmuggler, chainNue, chalex.eth, cjm00n, coincoin, coryli, ctf\_sec, curiousapple, dacian, evilakela, georgits, giovannidisiena, immeas, innertia, jah, juancito, kie, kiki\_dev, lil.eth, m4ttm, mahdikarimi, mrpathfindr, n33k, neumo, ni8mare, nobody2018, pavankv241, pengun, qbs, qckhp, qpzm, ravikiran.web3, saidam017, sam\_gmk, sashik\_eth, shaka, shealtielanz, shogoki, simon135, slightscan, smiling\_heretic, tallo, theOwl, the\_endless\_sea, toshii, tsvetanovv, tvdung94, twcctop, twicek, vagrant, ver0759, warRoom, whiteh4t9527, ww4tson, yy
## Summary

Lack of access control in `USSD.mintRebalancer()` and `USSD.burnRebalancer()` can lead to a denial-of-service attack and malfunction of the rebalancer as it can alter `totalSupply`, which is used in `rebalancer.SellUSSDBuyCollateral` to calculate `ownval`.

## Vulnerability Detail

Based on the context, `USSD.mintRebalancer()` should be `onlyBalancer` as it should only be allowed to be called by the rebalancer.

However, both `USSD.mintRebalancer()` and `USSD.burnRebalancer()` lack access control in the current implementation.

## Impact

An attacker can mint an amount of `type(uint256).max - totalSupply()` and cause a denial-of-service attack by preventing anyone else from minting.

Additionally, minting will also change the `totalSupply` which alters the `collateralFactor` and cause the rebalancer to malfunction, as the `SellUSSDBuyCollateral()` function relies on the `USSD.collateralFactor()`.

The `totalSupply` is also used in `rebalancer.SellUSSDBuyCollateral` to calculate the `ownval`.

## Code Snippet

https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSD.sol#L204-L210

```solidity
function mintRebalancer(uint256 amount) public override {
    _mint(address(this), amount);
}

function burnRebalancer(uint256 amount) public override {
    _burn(address(this), amount);
}
```

https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L92-L107

```solidity
    function rebalance() override public {
      uint256 ownval = getOwnValuation();
      (uint256 USSDamount, uint256 DAIamount) = getSupplyProportion();
      if (ownval < 1e6 - threshold) {
        // peg-down recovery
        BuyUSSDSellCollateral((USSDamount - DAIamount / 1e12)/2);
      } else if (ownval > 1e6 + threshold) {
        // mint and buy collateral
        // never sell too much USSD for DAI so it 'overshoots' (becomes more in quantity than DAI on the pool)
        // otherwise could be arbitraged through mint/redeem
        // the execution difference due to fee should be taken into accounting too
        // take 1% safety margin (estimated as 2 x 0.5% fee)
        IUSSD(USSD).mintRebalancer(((DAIamount / 1e12 - USSDamount)/2) * 99 / 100); // mint ourselves amount till balance recover
        SellUSSDBuyCollateral();
      }
    }
```

https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSD.sol#L179-L194

```solidity
function collateralFactor() public view override returns (uint256) {
    uint256 totalAssetsUSD = 0;
    for (uint256 i = 0; i < collateral.length; i++) {
        totalAssetsUSD +=
            (((IERC20Upgradeable(collateral[i].token).balanceOf(
                address(this)
            ) * 1e18) /
                (10 **
                    IERC20MetadataUpgradeable(collateral[i].token)
                        .decimals())) *
                collateral[i].oracle.getPriceUSD()) /
            1e18;
    }

    return (totalAssetsUSD * 1e6) / totalSupply();
}
```

## Tool used

Manual Review

## Recommendation

`USSD.mintRebalancer()` should be `onlyBalancer`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | J4de, Dug, 0xSmartContract, shaka, nobody2018, qbs, lil.eth, smiling\_heretic, Delvir0, giovannidisiena, Juntao, 0xyPhilic, 0xMojito, juancito, slightscan, coryli, the\_endless\_sea, coincoin, BugBusters, Angry\_Mustache\_Man, 0xAzez, ww4tson, twcctop, auditsea, sam\_gmk, pavankv241, m4ttm, Schpiel, blackhole, Lilyjjo, VAD37, shealtielanz, cjm00n, qckhp, SensoYard, immeas, BugHunter101, BlockChomper, Kose, Kodyvim, anthony, kie, ver0759, chalex.eth, tvdung94, mrpathfindr, \_\_141345\_\_, AlexCzm, HonorLt, curiousapple, chainNue, innertia, Nyx, blockdev, WATCHPUG, JohnnyTime, vagrant, ctf\_sec, tallo, saidam017, Vagner, RaymondFam, Aymen0909, 0xRobocop, n33k, neumo, GimelSec, ni8mare, warRoom, toshii, 0xPkhatri, twicek, carrotsmuggler, T1MOH, Brenzee, georgits, Bahurum, simon135, Tricko, Madalad, theOwl, Bauchibred, PokemonAuditSimulator, berlin-101, ravikiran.web3, Fanz, pengun, shogoki, 0x2e, evilakela, sashik\_eth, TheNaubit, yy, 0xStalin, qpzm, dacian, SanketKogekar, 0xeix, 14si2o\_Flint, DevABDee, tsvetanovv, 0xHati, kiki\_dev, jah, mahdikarimi, ast3ros, Bauer, whiteh4t9527, Saeedalipoor01988 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/777
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`Access Control`

