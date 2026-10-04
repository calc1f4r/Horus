---
# Core Classification
protocol: BakerFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33668
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-bakerfi
source_link: https://code4rena.com/reports/2024-05-bakerfi
github_link: https://github.com/code-423n4/2024-05-bakerfi-findings/issues/21

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
  - rvierdiiev
---

## Vulnerability Title

[M-05] Protocol receives less harvest fees

### Overview


This bug report discusses an issue with the calculation of fees in the BakerFi protocol. The protocol is supposed to receive a performance fee when the position has grown, but the current formula used to calculate the amount of shares to mint is causing the protocol to receive a smaller amount of fees than it should. This is because the minting of shares is done later, causing the total supply to increase and resulting in a smaller fee amount. The recommended mitigation step is to adjust the formula to account for the increase in total supply. This bug was reported using VsCode and has been acknowledged by the BakerFi team. 

### Original Finding Content


In case position has grown, then protocol receives performance fee.

<https://github.com/code-423n4/2024-05-bakerfi/blob/main/contracts/core/Vault.sol#L153-L158>

```solidity
                    uint256 feeInEthScaled = uint256(balanceChange) *
                        settings().getPerformanceFee();
                    uint256 sharesToMint = (feeInEthScaled * totalSupply()) /
                        _totalAssets(maxPriceAge) /
                        PERCENTAGE_PRECISION;
                    _mint(settings().getFeeReceiver(), sharesToMint);
```

We will check how shares amount is calculated and why it's less than it should be.

Suppose that `totalSupply() == 100000` and `_totalAssets(maxPriceAge) == 100100`, so we earned 100 eth as additional profit. `balanceChange == 100` and performance fee is 10\%, which is 10 eth.

`sharesToMint = 10 * 100000 / 100100 = 9.99001`

This means that with `9.990001` shares protocol should be able to grab 10 eth fee, which is indeed like that if we convert `9.99001 * 100100 / 100000 = 10`.

The problem is that minting is done later, which means that `totalSupply()` will increase with `9.99001` shares. So if we calculate fees amount now we will get a smaller amount: `9.99001 * 100100 / 100009.99001 = 9.999001`

### Impact

Protocol receives smaller amount of fees.

### Tools Used

VsCode

### Recommended Mitigation Steps

The formula should be adjusted to count increase of total supply.

**[hvasconcelos (BakerFi) acknowledged](https://github.com/code-423n4/2024-05-bakerfi-findings/issues/21#event-13082152004)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BakerFi |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-bakerfi
- **GitHub**: https://github.com/code-423n4/2024-05-bakerfi-findings/issues/21
- **Contest**: https://code4rena.com/reports/2024-05-bakerfi

### Keywords for Search

`vulnerability`

