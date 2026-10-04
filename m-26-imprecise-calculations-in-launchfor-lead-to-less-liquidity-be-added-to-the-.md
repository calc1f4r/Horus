---
# Core Classification
protocol: Virtuals Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61853
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-04-virtuals-protocol
source_link: https://code4rena.com/reports/2025-04-virtuals-protocol
github_link: https://code4rena.com/audits/2025-04-virtuals-protocol/submissions/F-278

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
finders_count: 2
finders:
  - Matin
  - codexNature
---

## Vulnerability Title

[M-26] Imprecise calculations in `launchFor()` lead to less liquidity be added to the pair via the router

### Overview


This bug report discusses a problem with the Bonding.sol function in the 2025-04-virtuals-protocol contract. The issue is related to a hidden division before a multiplication in the calculation of the `liquidity` variable, which results in a loss of precision. This can lead to the pool calculating less `liquidity` than intended, with a potential error of up to 25%. The report recommends changing the calculation method or using high precision fixed point math libraries to mitigate the issue. The report also includes a proof of concept and examples of the error in different scenarios. 

### Original Finding Content



<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/main/contracts/fun/Bonding.sol# L215-L216>

### Finding description and impact

Solidity rounds down the result of an integer division, and because of that, it is always recommended to multiply before dividing to avoid that precision loss. The problem arises in the Bonding.sol’s `launchFor()` function where the `liquidity` is calculated:
```

    function launchFor(
        string memory _name,
        string memory _ticker,
        uint8[] memory cores,
        string memory desc,
        string memory img,
        string[4] memory urls,
        uint256 purchaseAmount,
        address creator
    ) public nonReentrant returns (address, address, uint) {

        // code

        uint256 k = ((K * 10000) / assetRate);
        uint256 liquidity = (((k * 10000 ether) / supply) * 1 ether) / 10000;
```

Although this model is implemented to calculate the `k`, we can see there is a hidden division before a multiplication that makes round down the whole expression. This is bad as the precision loss can be significant, which leads to the pool calculating less `liquidity` than actual.

### Recommended mitigation steps

Consider changing the `liquidity` calculation in the way that prioritize the multiplication over division or use the high precision fixed point math libraries (e.g. PRB math lib).

### Proof of Concept
```

    uint256 public constant K = 3_000_000_000_000;

    function testPrecisionLoss(
        uint256 assetRate,
        uint supply
    ) public pure returns (uint256 act, uint256 acc) {
        uint256 k = ((K * 10000) / assetRate);
        act = (((k * 10000 ether) / supply) * 1 ether) / 10000;

        acc = (K * 10000 * 10000 ether * 1 ether) / (assetRate * supply * 10000);
    }
```

For the `assetRate` and `supply` equal to (`7.98e15`, `1.9283e18`):

The result would be:
```

     Current Implementation  1555700000000000000
     Actual Implementation   1949592125831354822
```

This is equal to `~25%` relative error. Also, it is worth to mention that in some cases even the liquidity becomes zero. For the `assetRate` and `supply` equal to (`1e18`, `2e18`), the result would be:
```

     Current Implementation  0
     Actual Implementation   15000000000000000
```

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Virtuals Protocol |
| Report Date | N/A |
| Finders | Matin, codexNature |

### Source Links

- **Source**: https://code4rena.com/reports/2025-04-virtuals-protocol
- **GitHub**: https://code4rena.com/audits/2025-04-virtuals-protocol/submissions/F-278
- **Contest**: https://code4rena.com/reports/2025-04-virtuals-protocol

### Keywords for Search

`vulnerability`

