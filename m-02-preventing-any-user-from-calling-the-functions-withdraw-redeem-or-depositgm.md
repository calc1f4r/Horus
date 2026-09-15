---
# Core Classification
protocol: Redacted Cartel
chain: everychain
category: uncategorized
vulnerability_type: minout/maxin_validation

# Attack Vector Details
attack_type: minout/maxin_validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6039
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-redacted-cartel-contest
source_link: https://code4rena.com/reports/2022-11-redactedcartel
github_link: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/70

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - minout/maxin_validation
  - swap

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - HE1M
---

## Vulnerability Title

[M-02] Preventing any user from calling the functions `withdraw`, `redeem`, or `depositGmx` in contract `AutoPxGmx`

### Overview


This bug report is about a vulnerability in the contract AutoPxGmx. It is possible for an attacker to prevent any user from calling the functions withdraw, redeem, or depositGmx by manipulating the balance of token gmxBaseReward. Whenever a user calls these functions, the function compound is called, which claims token gmxBaseReward from rewardModule. If the balance of the token gmxBaseReward in custodian of the contract AutoPxGmx is not zero, the token gmxBaseReward will be swapped to token GMX through uniswap V3 by calling the function exactInputSingle. 

The vulnerability is the parameter amountOutMinimum which is equal to 1. This provides an attack surface so that if the balance of token gmxBaseReward in AutoPxGmx is nonzero and small enough that does not worth 1 token GMX, the swap procedure will be reverted. For example, if the balance of gmxBaseReward is equal to 1, then since the value of gmxBaseReward is lower than token GMX, the output amount of GMX after swapping gmxBaseReward will be zero, and as parameter amountOutMinimum is equal to 1, the swap will be reverted, and as a result compound function will be reverted. 

The recommended mitigation step is for the parameter amountOutMinimum to be equal to zero when the function compound is called. This would prevent the attack surface from being exploited.

### Original Finding Content


It is possible that an attacker can prevent any user from calling the functions `withdraw`, `redeem`, or `depositGmx` in contract `AutoPxGmx` by just manipulating the balance of token `gmxBaseReward`, so that during the function `compound` the swap will be reverted.

### Proof of Concept

Whenever a user calls the functions `withdraw`, `redeem`, or `depositGmx` in contract `AutoPxGmx`, the function `compound` is called:

<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L321>

<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L345>

<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L379>

The function `compound` claims token `gmxBaseReward` from `rewardModule`:
<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L262>

Then, if the balance of the token `gmxBaseReward` in custodian of the contract `AutoPxGmx` is not zero, the token `gmxBaseReward` will be swapped to token `GMX` thrrough uniswap V3 by calling the function `exactInputSingle`. Then the total amount of token `GMX` in custodian of the contract `AutoPxGmx` will be deposited in the contract `PirexGmx` to receive token `pxGMX`:

    if (gmxBaseRewardAmountIn != 0) {
                gmxAmountOut = SWAP_ROUTER.exactInputSingle(
                    IV3SwapRouter.ExactInputSingleParams({
                        tokenIn: address(gmxBaseReward),
                        tokenOut: address(gmx),
                        fee: fee,
                        recipient: address(this),
                        amountIn: gmxBaseRewardAmountIn,
                        amountOutMinimum: amountOutMinimum,
                        sqrtPriceLimitX96: sqrtPriceLimitX96
                    })
                );

                // Deposit entire GMX balance for pxGMX, increasing the asset/share amount
                (, pxGmxMintAmount, ) = PirexGmx(platform).depositGmx(
                    gmx.balanceOf(address(this)),
                    address(this)
                );
            }

Whenever the function `compound` is called inside the mentioned functions, the parameters are:
`compound(poolFee, 1, 0, true);`

*   `fee = poolFee`
*   `amountOutMinimum = 1`
*   `sqrtPriceLimitX96 = 0`
*   `optOutIncentive = true`

The vulnerability is the parameter ` amountOutMinimum  ` which is equal to 1. This provides an attack surface so that if the balance of token `gmxBaseReward` in `AutoPxGmx` is nonzero and small enough that does not worth 1 token `GMX`, the swap procedure will be reverted.

For example, if the balance of `gmxBaseReward` is equal to 1, then since the value of `gmxBaseReward` is lower than token `GMX`, the output amount of `GMX` after swapping `gmxBaseReward` will be zero, and as parameter `amountOutMinimum` is equal to 1, the swap will be reverted, and as a result, the compound function will be reverted.

#### Attack Scenario:

Suppose, recently the function compound was called, so the balance of token `gmxBaseReward` in contract `AutoPxGmx` is equal to zero. Later, Alice (honest user) would like to withdraw. So, she calls the function `withdraw(...)`.

    function withdraw(
            uint256 assets,
            address receiver,
            address owner
        ) public override returns (uint256 shares) {
            // Compound rewards and ensure they are properly accounted for prior to withdrawal calculation
            compound(poolFee, 1, 0, true);

            shares = previewWithdraw(assets); // No need to check for rounding error, previewWithdraw rounds up.

            if (msg.sender != owner) {
                uint256 allowed = allowance[owner][msg.sender]; // Saves gas for limited approvals.

                if (allowed != type(uint256).max)
                    allowance[owner][msg.sender] = allowed - shares;
            }

            _burn(owner, shares);

            emit Withdraw(msg.sender, receiver, owner, assets, shares);

            asset.safeTransfer(receiver, assets);
        }

<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L315>

In a normal situation, the function `compound` will be called, and since the balance of `gmxBaseReward` is zero, no swap will be executed in uniswap V3, and the rest of the code logic will be executed.

But in this scenario, before Alice's transaction, Bob transfers 1 token `gmxBaseReward` directly to contract `AutoPxGmx` . So, when Alice's transaction is going to be executed, inside the function `compound` the swap function will be called (because the balance `gmxBaseReward` is equal to 1 now). In the function `exactInputSingle` in uniswap V3, there is a check:
`require(amountOut >= params.amountOutMinimum, 'Too little received');`
<https://etherscan.io/address/0xe592427a0aece92de3edee1f18e0157c05861564#code#F1#L128>

This check will be reverted, because 1 token of `gmxBaseReward` is worth less than 1 token of  `GMX`, so the amount out will be zero which is smaller than `amountOutMinimum`.

In summary, an attacker before user's deposit, checks the balance of token `gmxBaseReward` in `AutoPxGmx`. If this balance is equal to zero, the attacker transfers 1 token `gmxBaseReward` to contract `AutoPxGmx`, so the user's transaction will be reverted, and user should wait until this balance reaches to the amount that worth more than or equal to 1 token `GMX`.

### Recommended Mitigation Steps

The parameter `amountOutMinimum` should be equal to zero when the function `compound` is called.
`compound(poolFee, 0, 0, true);`

**[Picodes (judge) decreased severity to Medium and  commented](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/70#issuecomment-1336256838):**
 > The attack is unlikely: there is no real reason to do it as the attacker would have to pay gas, you need conditions on the price, and conditions on the reward amounts, as if rewards are accruing you won't be able to do it, so downgrading to Medium severity.
>
 > However it's true that it may be good to set a minimum amount for the swaps that depends on the `amountIn`, or remove entirely the `minAmountOut` requirement.

**[kphed (Redacted Cartel) commented](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/70#issuecomment-1341222030):**
 > Hi @Picodes, this is going to be resolved as a side effect of issue [#321](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/321) being fixed (i.e. `compound` will be updated to consider token balances w/o dependence on external factors to prevent DoS'ing of users). Wanted to flag it for your attention but ultimately up to you re: awarding. Thanks for your help ser.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Redacted Cartel |
| Report Date | N/A |
| Finders | HE1M |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-redactedcartel
- **GitHub**: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/70
- **Contest**: https://code4rena.com/contests/2022-11-redacted-cartel-contest

### Keywords for Search

`MinOut/MaxIn Validation, Swap`

