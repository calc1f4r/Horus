---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24662
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-notional
source_link: https://code4rena.com/reports/2022-01-notional
github_link: https://github.com/code-423n4/2022-01-notional-findings/issues/229

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] `sNOTE` Holders Are Not Incetivized To Vote On Proposals To Call `extractTokensForCollateralShortfall`

### Overview


This bug report submitted by leastwood highlights the issue of Notional protocol's inability to detect collateral shortfalls programmatically. This puts the protocol in a state where stakers are unwilling to vote on a proposal to call `extractTokensForCollateralShortfall`, leaving Notional insolvent as stakers continue to dump their holdings.

The proof of concept provided in the report contains the code for the `extractTokensForCollateralShortfall` function, which outlines the mechanism for withdrawing tokens in the event of a collateral shortfall.

The recommended mitigation steps suggest redesigning this mechanism to better align stakers with the health of the protocol. This could involve allocating a percentage of generated fees to an insurance fund which will be used to cover any collateral shortfall events, and staking this fund to generate additional yield.

Jeffywu from Notional acknowledged the issue and commented that there are technical difficulties with programmatic collateral shortfall detection at this moment, and that they will look to develop a method that allows for programmatic detection in the future. Pauliax from the judge commented that this is a hypothetical but valid concern.

### Original Finding Content

_Submitted by leastwood_

As `sNOTE` have governance voting rights equivalent to the token amount in `NOTE`, users who stake their `NOTE` are also able to vote on governance proposals. In the event a majority of `NOTE` is staked in the `sNOTE` contract, it doesn't seem likely that stakers would be willing to vote on a proposal which liquidates a portion of their staked position.

Hence, the protocol may be put into a state where stakers are unwilling to vote on a proposal to call `extractTokensForCollateralShortfall`, leaving Notional insolvent as stakers continue to dump their holdings.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-notional/blob/main/contracts/sNOTE.sol#L99-L129>
```solidity
function extractTokensForCollateralShortfall(uint256 requestedWithdraw) external nonReentrant onlyOwner {
    uint256 bptBalance = BALANCER_POOL_TOKEN.balanceOf(address(this));
    uint256 maxBPTWithdraw = (bptBalance * MAX_SHORTFALL_WITHDRAW) / 100;
    // Do not allow a withdraw of more than the MAX_SHORTFALL_WITHDRAW percentage. Specifically don't
    // revert here since there may be a delay between when governance issues the token amount and when
    // the withdraw actually occurs.
    uint256 bptExitAmount = requestedWithdraw > maxBPTWithdraw ? maxBPTWithdraw : requestedWithdraw;

    IAsset[] memory assets = new IAsset[](2);
    assets[0] = IAsset(address(WETH));
    assets[1] = IAsset(address(NOTE));
    uint256[] memory minAmountsOut = new uint256[](2);
    minAmountsOut[0] = 0;
    minAmountsOut[1] = 0;

    BALANCER_VAULT.exitPool(
        NOTE_ETH_POOL_ID,
        address(this),
        payable(owner), // Owner will receive the NOTE and WETH
        IVault.ExitPoolRequest(
            assets,
            minAmountsOut,
            abi.encode(
                IVault.ExitKind.EXACT_BPT_IN_FOR_TOKENS_OUT,
                bptExitAmount
            ),
            false // Don't use internal balances
        )
    );
}
```

#### Recommended Mitigation Steps

Consider redesigning this mechanism to better align stakers with the health of the protocol. It might be useful to allocate a percentage of generated fees to an insurance fund which will be used to cover any collateral shortfall events. This fund can be staked to generate additional yield.

**[jeffywu (Notional) acknowledged and commented](https://github.com/code-423n4/2022-01-notional-findings/issues/229#issuecomment-1030839281):**
 > Acknowledged, however, there are technical difficulties with programmatic collateral shortfall detection at this moment. We will look to develop a method that allows for programmatic detection in the future (these issues have been discussed with the warden).

**[pauliax (judge) commented](https://github.com/code-423n4/2022-01-notional-findings/issues/229#issuecomment-1041536723):**
 > A hypothetical but valid concern.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Notional |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-notional
- **GitHub**: https://github.com/code-423n4/2022-01-notional-findings/issues/229
- **Contest**: https://code4rena.com/reports/2022-01-notional

### Keywords for Search

`vulnerability`

