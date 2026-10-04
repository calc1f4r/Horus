---
# Core Classification
protocol: UXD Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6591
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/33
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/250

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - services
  - derivatives
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - csanuragjain
  - 0x52
  - Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/250
---

## Vulnerability Title

H-4: USDC deposited to PerpDepository.sol are irretrievable and effectively causes UDX to become undercollateralized

### Overview


In this bug report, it is stated that USDC which is deposited to PerpDepository.sol are irretrievable and it causes UDX to become undercollateralized. It was found by 0x52 and csanuragjain. This is caused by the fact that the only way to remove USDC from the system is positive PNL rebalancing which has now been deactivated and the owner can remove the USDC via withdrawInsurance. However, withdrawInsurance cannot actually redeem any USDC as it is impossible for more USDC to be withdrawn then was originally deposited. This means that the USDC is inaccessible, leading to UDX becoming undercollateralized. The impact of this is that the ecosystem will spiral out of control. A fix was proposed by hrishibhat and IAm0x52 which was accepted. The fix enabled quote redeeming and removed the redundant onlyController modifier on _processQuoteRedeem.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/250 

## Found by 
0x52, csanuragjain

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

## Discussion

**hrishibhat**

Fix: https://github.com/UXDProtocol/uxd-evm/pull/32

**IAm0x52**

Fix looks good. Quote redeeming has been enabled. I would recommend removing redundant onlyController modifier on _processQuoteRedeem

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | UXD Protocol |
| Report Date | N/A |
| Finders | csanuragjain, 0x52, Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/250 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/250
- **Contest**: https://app.sherlock.xyz/audits/contests/33

### Keywords for Search

`vulnerability`

