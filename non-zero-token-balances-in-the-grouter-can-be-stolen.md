---
# Core Classification
protocol: Growth Labs GSquared
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17347
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Damilola Edwards
  - Gustavo Grieco
  - Anish Naik
  - Michael Colburn
---

## Vulnerability Title

Non-zero token balances in the GRouter can be stolen

### Overview

See description below for full details.

### Original Finding Content

## Security Assessment Report

## Difficulty: High

## Type: Undefined Behavior

## Target: GRouter.sol

### Description
A non-zero balance of 3CRV, DAI, USDC, or USDT in the router contract can be stolen by an attacker. 

The GRouter contract is the entrypoint for deposits into a tranche and withdrawals out of a tranche. A deposit involves depositing a given number of a supported stablecoin (USDC, DAI, or USDT); converting the deposit, through a series of operations, into G3CRV, the protocol’s ERC4626-compatible vault token; and depositing the G3CRV into a tranche.

Similarly, for withdrawals, the user burns their G3CRV that was in the tranche and, after a series of operations, receives back some amount of a supported stablecoin (figure 3.1).

```solidity
ERC20(address(tranche.getTrancheToken(_tranche))).safeTransferFrom();
// withdraw from tranche
// index is zero for ETH mainnet as their is just one yield token
// returns usd value of withdrawal
(uint256 vaultTokenBalance,) = tranche.withdraw(
    function withdrawFromTrancheForCaller(
        msg.sender,
        address(this),
        _amount,
        uint256 _amount,
        uint256 _token_index,
        bool _tranche,
        uint256 _minAmount
    ) internal returns (uint256 amount) {
        _amount,
        0,
        _tranche,
        address(this)
        vaultTokenBalance,
        address(this),
        address(this)
    });
);
```

```solidity
// withdraw underlying from GVault
uint256 underlying = vaultToken.redeem(
    // remove liquidity from 3crv to get desired stable from curve
    threePool.remove_liquidity_one_coin(
        underlying, 
        int128(uint128(_token_index)), // value should always be 0,1,2
        0
    );
    ERC20 stableToken = ERC20(routerOracle.getToken(_token_index));
    amount = stableToken.balanceOf(address(this));
    if (amount < _minAmount) {
        revert Errors.LTMinAmountExpected();
    }
    // send stable to user
    stableToken.safeTransfer(msg.sender, amount);
    emit LogWithdrawal(msg.sender, _amount, _token_index, _tranche, amount);
```

### Figure 3.1: The withdrawFromTrancheForCaller function in GRouter.sol#L421-468
However, notice that during withdrawals the amount of stableTokens that will be transferred back to the user is a function of the current stableToken balance of the contract (see the highlighted line in figure 3.1). In the expected case, the balance should be only the tokens received from the `threePool.remove_liquidity_one_coin` swap (see L450 in figure 3.1). 

However, a non-zero balance could also occur if a user airdrops some tokens or they transfer tokens by mistake instead of calling the expected deposit or withdraw functions. As long as the attacker has at least 1 wei of G3CRV to burn, they are capable of withdrawing the whole balance of stableToken from the contract, regardless of how much was received as part of the threePool swap. A similar situation can happen with deposits. A non-zero balance of G3CRV can be stolen as long as the attacker has at least 1 wei of either DAI, USDC, or USDT.

### Exploit Scenario
Alice mistakenly sends a large amount of DAI to the GRouter contract instead of calling the deposit function. Eve notices that the GRouter contract has a non-zero balance of DAI and calls withdraw with a negligible balance of G3CRV. Eve is able to steal Alice's DAI at a very small cost.

### Recommendations
Short term, consider using the difference between the contract’s pre- and post-balance of stableToken for withdrawals, and depositAmount for deposits, in order to ensure that only the newly received tokens are used for the operations.

Long term, create an external skim function that can be used to skim any excess tokens in the contract. Additionally, ensure that the user documentation highlights that users should not transfer tokens directly to the GRouter and should instead use the web interface or call the deposit and withdraw functions. Finally, ensure that token airdrops or unexpected transfers can only benefit the protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Growth Labs GSquared |
| Report Date | N/A |
| Finders | Damilola Edwards, Gustavo Grieco, Anish Naik, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf

### Keywords for Search

`vulnerability`

