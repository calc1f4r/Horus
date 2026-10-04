---
# Core Classification
protocol: Dopex
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29454
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-dopex
source_link: https://code4rena.com/reports/2023-08-dopex
github_link: https://github.com/code-423n4/2023-08-dopex-findings/issues/2083

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
  - decimals

# Audit Details
report_date: unknown
finders_count: 22
finders:
  - qpzm
  - Jiamin
  - circlelooper
  - Qeew
  - Juntao
---

## Vulnerability Title

[H-01] Improper precision of strike price calculation can result in broken protocol

### Overview


A bug has been identified in the `RdpxV2Core` and `PerpetualAtlanticVault` contracts of the dpxETH protocol. This bug results in the calculated strike price for a PUT option for rDPX not being guaranteed to be 25% OTM, which breaks core assumptions around protecting downside price movement of the rDPX which makes up part of the collateral for dpxETH and not overpaying for PUT option protection.

The issue is due to the `roundUp` function of the `PerpetualAtlanticVault` contract, which effectively imposes a minimum value of `1e6`. This means that when the current price of rDPX is `1e6` (in 8 decimals of precision), the strike price calculated by the `calculateBondCost` function of the `RdpxV2Core` contract will be rounded up to `1e6` as well. This is not 25% OTM, and since it is an ITM option, the premium imposed will be significantly higher.

To mitigate this issue, the value of the `roundingPrecision` should be decreased. This has been confirmed by psytama (Dopex).

### Original Finding Content


<https://github.com/code-423n4/2023-08-dopex/blob/main/contracts/core/RdpxV2Core.sol#L1189-L1190> 

<https://github.com/code-423n4/2023-08-dopex/blob/main/contracts/perp-vault/PerpetualAtlanticVault.sol#L576-L583>

Due to a lack of adequate precision, the calculated strike price for a PUT option for rDPX is not guaranteed to be 25% OTM, which breaks core assumptions around (1) protecting downside price movement of the rDPX which makes up part of the collateral for dpxETH & (2) not overpaying for PUT option protection.

More specifically, the price of rDPX as used in the `calculateBondCost` function of the RdpxV2Core contract is represented as ETH / rDPX, and is given in 8 decimals of precision. To calculate the strike price which is 25% OTM based on the current price, the logic calls the `roundUp` function on what is effectively 75% of the current spot rDPX price. The issue is with the `roundUp` function of the PerpetualAtlanticVault contract, which effectively imposes a minimum value of 1e6.

Considering approximate recent market prices of `$`2000/ETH and `$`20/rDPX, the current price of rDPX in 8 decimals of precision would be exactly 1e6. Then to calculate the 25% OTM strike price, we would arrive at a strike price of `1e6 * 0.75 = 75e4`. The `roundUp` function will then round up this value to `1e6` as the strike price, and issue the PUT option using that invalid strike price. Obviously this strike price is not 25% OTM, and since its an ITM option, the premium imposed will be significantly higher. Additionally this does not match the implementation as outlined in the docs.

### Proof of Concept

When a user calls the `bond` function of the RdpxV2Core contract, it will calculate the `rdpxRequired` and `wethRequired` required by the user in order to mint a specific `_amount` of dpxETH, which is calculated using the `calculateBondCost` function:

```solidity
function bond(
  uint256 _amount,
  uint256 rdpxBondId,
  address _to
) public returns (uint256 receiptTokenAmount) {
  _whenNotPaused();
  // Validate amount
  _validate(_amount > 0, 4);

  // Compute the bond cost
  (uint256 rdpxRequired, uint256 wethRequired) = calculateBondCost(
    _amount,
    rdpxBondId
  );
  ...
}
```

Along with the collateral requirements, the `wethRequired` will also include the ETH premium required to mint the PUT option. The amount of premium is calculated based on a strike price which represents 75% of the current price of rDPX (25% OTM PUT option). In the `calculateBondCost` function:

```solidity
function calculateBondCost(
  uint256 _amount,
  uint256 _rdpxBondId
) public view returns (uint256 rdpxRequired, uint256 wethRequired) {
  uint256 rdpxPrice = getRdpxPrice();

  ...

  uint256 strike = IPerpetualAtlanticVault(addresses.perpetualAtlanticVault)
    .roundUp(rdpxPrice - (rdpxPrice / 4)); // 25% below the current price

  uint256 timeToExpiry = IPerpetualAtlanticVault(
    addresses.perpetualAtlanticVault
  ).nextFundingPaymentTimestamp() - block.timestamp;
  if (putOptionsRequired) {
    wethRequired += IPerpetualAtlanticVault(addresses.perpetualAtlanticVault)
      .calculatePremium(strike, rdpxRequired, timeToExpiry, 0);
  }
}
```

As shown, the strike price is calculated as:

```solidity
uint256 strike = IPerpetualAtlanticVault(addresses.perpetualAtlanticVault).roundUp(rdpxPrice - (rdpxPrice / 4));
```

It uses the `roundUp` function of the PerpetualAtlanticVault contract which is defined as follows:

```solidity
function roundUp(uint256 _strike) public view returns (uint256 strike) {
  uint256 remainder = _strike % roundingPrecision;
  if (remainder == 0) {
    return _strike;
  } else {
    return _strike - remainder + roundingPrecision;
  }
}
```

In this contract `roundingPrecision` is set to `1e6`, and this is where the problem arises. As I mentioned earlier, take the following approximate market prices: `$`2000/ETH and `$`20/rDPX. This means the `rdpxPrice`, which is represented as ETH/rDPX in 8 decimals of precision, will be `1e6`. To calculate the strike price, we get the following: `1e6 * 0.75 = 75e4`. However this value is fed into the `roundUp` function which will convert the `75e4` to `1e6`. This value of `1e6` is then used to calculate the premium, which is completely wrong. Not only is `1e6` not 25% OTM, but it is actually ITM, meaning the premium will be significantly higher than was intended by the protocol design.

### Recommended Mitigation Steps

The value of the `roundingPrecision` is too high considering reasonable market prices of ETH and rDPX. Consider decreasing it.

**[psytama (Dopex) confirmed](https://github.com/code-423n4/2023-08-dopex-findings/issues/2083#issuecomment-1734091528)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Dopex |
| Report Date | N/A |
| Finders | qpzm, Jiamin, circlelooper, Qeew, Juntao, visualbits, piyushshukla, Matin, deadrxsezzz, catwhiskeys, 0xDING99YA, Cosine, eeshenggoh, Topmark, peakbolt, 0x3b, crunch, pep7siup, 1, 2, 0xmystery, Toshii |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-dopex
- **GitHub**: https://github.com/code-423n4/2023-08-dopex-findings/issues/2083
- **Contest**: https://code4rena.com/reports/2023-08-dopex

### Keywords for Search

`Decimals`

