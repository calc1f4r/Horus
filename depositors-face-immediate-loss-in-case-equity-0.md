---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27637
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ElHaj
---

## Vulnerability Title

depositors face immediate loss in case `equity = 0`

### Overview


This bug report discusses a vulnerability in the `valueToShares` function that exposes users to significant losses in case the equity (currentAllAssetValue - debtBorrowed) becomes zero due to strategy losses. When the equity value is 0, the shares minted to the user equal the deposited value itself. In this scenario, the user immediately incurs a loss, depending on the total supply of `svToken` (shares). To illustrate, if the total supply of `svToken` is 100,000,000 and the equity value drops to zero due to strategy losses and a user deposits 100 USD worth of value, the user is minted 100 shares (100 * 1e18). Consequently, the value the user owns with these shares immediately reduces to 0.001 USD. In this case, the user immediately shares their entire deposited value with these old minted shares and loses their deposit, whereas those old shares should be liquidated some how. 

The impact of this vulnerability is that users face immediate loss of funds in case equity drops to zero. The bug was identified through manual review. A recommendation is to use a liquidation mechanism that burns the shares of all users when equity drops to zero.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXReader.sol#L48">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXReader.sol#L48</a>


## Summary

The vulnerability in the `valueToShares` function exposes users to significant losses in case the equity `(currentAllAssetValue - debtBorrowed)` becomes zero due to strategy losses, users receive disproportionately low shares, and take a loss Immediately.

## Vulnerability Details

- When a user deposits to the contract, the calculation of the shares to be minted depends on the value of equity added to the contract after a successful deposit. In other words:
  - `value` = `equityAfter` - `equityBefore`, while:
  - `equity` = `totalAssetValue` - `totalDebtValue`.
    and we can see that here :

```solidity
   function processDeposit(GMXTypes.Store storage self) external {
        self.depositCache.healthParams.equityAfter = GMXReader.equityValue(self);
>>        self.depositCache.sharesToUser = GMXReader.valueToShares(
            self,
            self.depositCache.healthParams.equityAfter - self.depositCache.healthParams.equityBefore,
            self.depositCache.healthParams.equityBefore
        );

        GMXChecks.afterDepositChecks(self);
    }
    // value to shares function :

     function valueToShares(GMXTypes.Store storage self, uint256 value, uint256 currentEquity)
        public
        view
        returns (uint256)
    {

        uint256 _sharesSupply = IERC20(address(self.vault)).totalSupply() + pendingFee(self); // shares is added
>>        if (_sharesSupply == 0 || currentEquity == 0) return value;
>>        return value * _sharesSupply / currentEquity;
    }
```

- **NOTICE:** When the equity value is `0`, the shares minted to the user equal the deposited value itself. The equity value can become zero due to various factors such as strategy losses or accumulated lending interests... ect
- In this scenario, the user immediately incurs a loss, depending on the total supply of `svToken` (shares).
- Consider the following simplified example:
  - The total supply of `svToken` is (1,000,000 \* 1e18) (indicating users holding these shares).
  - the equity value drops to zero due to strategy losses and a user deposits 100 USD worth of value,
  - Due to the zero equity value, the user is minted 100 shares (100 \* 1e18).
  - Consequently, the value the user owns with these shares immediately reduces to 0.001 USD.
    `100 * 100 * 1e18 / 1,000,000 = 0.001 USD` (value \* equity / totalSupply).
- In this case, the user immediately shares their entire deposited value with these old minted shares and loses their deposit, whereas those old shares should be liquidated some how.
  > Notice: If the total supply is higher, the user loses more value, and vice versa.

## Impact

- users face immediate loss of funds in case equity drops to zero

## Tools Used

manual review

## Recommendations

- use a liquidation mechanism that burns the shares of all users when equity drops to zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | ElHaj |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

