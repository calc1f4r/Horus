---
# Core Classification
protocol: UXD Protocol
chain: everychain
category: logic
vulnerability_type: overflow/underflow

# Attack Vector Details
attack_type: overflow/underflow
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6256
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/33
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/250

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.53
financial_impact: high

# Scoring
quality_score: 2.6666666666666665
rarity_score: 4

# Context Tags
tags:
  - overflow/underflow
  - business_logic

protocol_categories:
  - liquid_staking
  - services
  - derivatives
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - csanuragjain
  - 0x52
---

## Vulnerability Title

H-5: USDC deposited to PerpDepository.sol are irretrievable and effectively causes UDX to become undercollateralized

### Overview


This bug report is about the USDC deposited to PerpDepository.sol being irretrievable and causing UDX to become undercollateralized. It was found by csanuragjain and 0x52. The problem is related to the functions `_processQuoteMint`, `_rebalanceNegativePnlWithSwap` and `_rebalanceNegativePnlLite`, which all add USDC collateral to the system. There were originally two ways in which USDC could be removed from the system, but the first was deactivated and the second, `withdrawInsurance`, cannot actually redeem any USDC due to the fact that insuranceDeposited is a uint256 and is decremented by the withdraw. This means that the USDC can never be redeemed, leading to the system becoming undercollateralized over time. The impact of this bug is that UDX will become undercollateralized and the ecosystem will spiral out of control. The code snippets related to this bug can be found at the given links. The tool used for finding this bug was Manual Review. The recommendation for this bug is to allow all USDC now deposited into the insurance fund to be redeemed 1:1.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/250 

## Found by 
csanuragjain, 0x52

## Summary

PerpDepository rebalances negative PNL into USDC holdings. This preserves the delta neutrality of the system by exchanging base to quote. This is problematic though as once it is in the vault as USDC it can never be withdrawn. The effect is that the delta neutral position can never be liquidated but the USDC is inaccessible so UDX is effectively undercollateralized. 

## Vulnerability Detail

`_processQuoteMint`, `_rebalanceNegativePnlWithSwap` and `_rebalanceNegativePnlLite` all add USDC collateral to the system. There were originally two ways in which USDC could be removed from the system. The first was positive PNL rebalancing, which has now been deactivated. The second is for the owner to remove the USDC via `withdrawInsurance`.

    function withdrawInsurance(uint256 amount, address to)
        external
        nonReentrant
        onlyOwner
    {
        if (amount == 0) {
            revert ZeroAmount();
        }

        insuranceDeposited -= amount;

        vault.withdraw(insuranceToken(), amount);
        IERC20(insuranceToken()).transfer(to, amount);

        emit InsuranceWithdrawn(msg.sender, to, amount);
    }

The issue is that `withdrawInsurance` cannot actually redeem any USDC. Since insuranceDeposited is a uint256 and is decremented by the withdraw, it is impossible for more USDC to be withdrawn then was originally deposited.

The result is that there is no way for the USDC to ever be redeemed and therefore over time will lead to the system becoming undercollateralized due to its inaccessibility.

## Impact

UDX will become undercollateralized and the ecosystem will spiral out of control

## Code Snippet

https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L478-L528

https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L615-L644

https://github.com/sherlock-audit/2023-01-uxd/blob/main/contracts/integrations/perp/PerpDepository.sol#L385-L397

## Tool used

Manual Review

## Recommendation

Allow all USDC now deposited into the insurance fund to be redeemed 1:1

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 2.6666666666666665/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | UXD Protocol |
| Report Date | N/A |
| Finders | csanuragjain, 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/250
- **Contest**: https://app.sherlock.xyz/audits/contests/33

### Keywords for Search

`Overflow/Underflow, Business Logic`

