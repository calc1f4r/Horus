---
# Core Classification
protocol: The Standard Auto Redemption
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45056
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
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
  - Giovanni Di Siena
---

## Vulnerability Title

Auto redemption logic can be abused by an attacker due to insufficient access control

### Overview


The bug report discusses an issue with a function called `AutoRedemption::performUpkeep` that is used by a program called the Chainlink Automation DON. The problem is that there is no control over who can use this function, so it can be called by anyone. This can cause problems because the function can be repeatedly used, even after it has already been successful. This can lead to a loss of funds for the program and can also block its functionality. The report recommends fixing this issue by adding access control and using a different method to calculate the amount of funds being repaid. The problem has been fixed by the Standard DAO, but another program called Cyfrin still needs to make some changes.

### Original Finding Content

**Description:** `AutoRedemption::performUpkeep` is exposed for use by the Chainlink Automation DON when upkeep is required:

```solidity
function performUpkeep(bytes calldata performData) external {
    if (lastRequestId == bytes32(0)) {
        triggerRequest();
    }
}
```

However, there is an absence of access control that allows the function to be called by an address. Since `lastRequestId` is reset to `bytes32(0)` at the end of `AutoRedemption::fulfillRequest` execution, this means that upkeep can be repeatedly performed after the previous one has succeeded, regardless the trigger condition.

If `AutoRedemption::fulfillRequest` reverts, the `lastRequestId` state will not be reset which completely blocks all future auto redemptions due to the conditional in `AutoRedemption::performUpkeep` shown above. Combined with the use of `ERC20::balanceOf` within both `SmartVaultV4Legacy::autoRedemption` and `SmartVaultV4::autoRedemption` to determine the amount `USDs` repaid, an attacker can force this DoS condition by sending a small amount of `USDs` directly to the target vault:

```solidity
uint256 _usdsBalance = USDs.balanceOf(address(this));
minted -= _usdsBalance;
```

This causes the vault balance to be inflated above the expected maximum `minted` amount and execution to revert due to underflow. Since the Chainlink Functions DON will not retry failed fulfilment, there will be no way to reset the state and recover core functionality without complete redeployment.

**Impact:** An attacker can repeatedly trigger auto redemption regardless of the trigger condition and without relying on price oracle manipulation. This could amount to a loss of funds to the protocol since the Chainlink subscription will be billed on every fraudulent fulfilment attempt. Alternatively, an attacker could completely block functionality of the auto redemption mechanism if fulfilment is made to revert.

**Recommended Mitigation:** * Re-check the trigger condition within `AutoRedemption::performUpkeep` and also consider adding [access control](https://docs.chain.link/chainlink-automation/guides/forwarder).
* Calculate the amount of `USDs` repaid as the balance diff rather than using the vault balance directly.

**The Standard DAO:** Fixed by commit [5ec532e](https://github.com/the-standard/smart-vault/commit/5ec532e5f3813a865102501dbb91cf13a0813930).

**Cyfrin:** The trigger condition is re-checked and a TWAP has been implemented, however:
* It is recommended to use a substantially large interval (at least 900 seconds, if not 1800 seconds) to protect against manipulation. Note: Uniswap V3 pool oracles are not multi-block MEV resistant.
* The `USDs` repayment amount calculation has not been modified to use balance diffs instead of direct `balanceOf()`.

**The Standard DAO:** Fixed by commit [a8cdc77](https://github.com/the-standard/smart-vault/commit/a8cdc77d1fac9817128e1f3c1c8a1ab57f715513), using the amount out of the swap rather than balance checks.

**Cyfrin:** Verified. The TWAP interval has been increased and the redeemed amount has been modified to use the value output from the swap.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | The Standard Auto Redemption |
| Report Date | N/A |
| Finders | Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

