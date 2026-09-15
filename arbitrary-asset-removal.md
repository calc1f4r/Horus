---
# Core Classification
protocol: Treehouse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38565
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Arbitrary Asset Removal

### Overview

See description below for full details.

### Original Finding Content

## Description

As part of the intended design, contracts `Converter.sol`, `TreehouseRedemption.sol`, and `TreehouseRouter.sol` all inherit `Rescuable.sol`, allowing the admin to withdraw any Ether or ERC20 tokens from these contracts.

## Recommendations

- While only intended as a fail-safe feature, the team should make end users aware of this functionality.
- Ensure the `_rescuer` address is a multi-sig and is isolated correctly to reduce the risk of malicious behaviour.

## Resolution

The issue was acknowledged by the project team.

## TREE-13 Miscellaneous General Comments

**Asset:** All contracts  
**Status:** Closed: See Resolution  
**Rating:** Informational  

## Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Execution Of Gnosis Transactions Need To Be Refactored For Production**  
   **Related Asset(s):** `execution.py`  
   In the testing environment, for Gnosis transactions, `execution.execute_sequence()` dumps the orders to JSON rather than executing them immediately.  
   When this function is implemented for production, it is necessary to refactor `send_order.py` so that it waits a sufficient amount of time after calling `execute_sequence()` before performing `analyze_state()` as the state will be incorrect if not all relevant transactions have been confirmed.  
   Implement the suggestions above as seen fit.

2. **Ineffective Monitoring Of Lido Stake Rate**  
   **Related Asset(s):** `analyze_state.py`  
   The function `analyze_state.decide_rebal_target()` decides, based on certain metrics, whether rebalancing is necessary.  
   One of the conditions, which sets rebalancing to true, occurs when the Lido stake rate falls below the `LVL_3` threshold of 1.05. The purpose of this condition is so that profit margins are monitored so that they do not fall below the configured threshold.
   ```python
   if lido_stake_rate_alert == f"{LVL_3}_below_lower":
       need_rebal = True
       sta_logger.info("Lido stake rate is below lower bound.")
   ```
   However, this metric cannot be resolved by rebalancing as it is not part of the constraints of the rebalancing model. If this is the only condition which triggered rebalancing, it may result in unnecessary on-chain transactions. If the intention is to provide a warning system to trigger potential manual intervention when the profit margin becomes too thin, consider logging a warning rather than info, similar to when an exit strategy is triggered.
   ```python
   if exit_strat:
       need_rebal = True
       sta_logger.warning(
           "Got exit_strategy signal from price analysis, please adjust the config and rebalance."
       )
   ```

3. **Arithmetic Equations Readability Improvements**  
   **Related Asset(s):** `tETH-offchain/utils/calc_func.py`, `tETH-offchain/utils/rebal_func.py`  
   Consider improving readability of arithmetic equations by implementing parentheses to explicitly indicate order of operations. Otherwise, Python will utilize PEMDAS (parentheses, exponents, multiplication and division, addition and subtraction), in order from left to right for multiplication/division and addition/subtraction.  
   The following expressions have been identified as candidates for readability improvements (note, the list below is not exhaustive):
   - `tETH-offchain/utils/calc_func.py` - lines 27, 57, 113, 153, 205, 229.
   - `tETH-offchain/utils/rebal_func.py` - lines 623, 692, 706.  
   Introduce parentheses in expressions to ensure improved readability.

4. **Hardcoded API Key**  
   **Related Asset(s):** `tETH-offchain/config/thirdparty_config/strat_config_thirdparty.yml`  
   API keys are hardcoded in `BLOCKSCAN_API_KEYS` parameter and stored in plaintext in the config file. Note, from the code comment it appears that the team is aware of it, so this finding is merely a reminder to address it before deployment in production.  
   Do not store sensitive information in plaintext config files.

5. **Make Use of Lido Custom Aave V3 Market**  
   **Related Asset(s):** `strategy/actions/aaveV3/helpers/MainnetAaveV3Addresses.sol`  
   Aave have recently introduced a new market that is specially designed for leveraged lending ETH against wstETH. This market has safer parameters due to being fine-tuned for a single purpose and therefore is better suited for use by Treehouse with tETH.  
   It is recommended to add the new Lido Aave V3 market as another strategy with the same functionality.

6. **Addresses Not Initialised On Construction**  
   **Related Asset(s):** `Vault.sol`, `LidoAPR.sol`, `PnlAccountingHelper.sol`  
   Various contracts have addresses that are required for operation which are not set immediately on construction:
   - Executor in `LidoAPR.sol`
   - Executor in `PnlAccountingHelper.sol`
   - `strategyStorage` in `Vault.sol`  
   Ensure these roles are initialised by calling the correct setters immediately after construction.

7. **Update Logic Not Included In Constructor**  
   **Related Asset(s):** `LidoAPR.sol`  
   A zero check performed in `updateShareRate()` is missing from the constructor when initializing the value.  
   Add the same zero rate check to the constructor for consistency.

8. **Asset Tracking Behaviours**  
   **Related Asset(s):** `NavHelper.sol`, `PnlAccountingHelper.sol`  
   Numerous different approaches are used to list assets related to vaults and strategies.  
   For example, `PnlAccountingHelper.getNavOfStrategy()` hardcodes the tokens it considers relevant for calculating the net asset value to WETH and wstETH. Meanwhile, `NavHelper.getTokensNav()` will always record the value of a contract's ETH despite it not being specified in the list of tokens requested.  
   While no direct impact has been found thus far, as the system intends to expand to more assets and strategies in future, it is advisable to adopt a uniform system for gathering relevant assets.

9. **Confusing Deposit Event Emission**  
   **Related Asset(s):** `TreehouseRouter.sol`  
   The router only rejects zero deposits when made using the stETH token; deposits using ETH, wETH, or wstEth all succeed when the deposit amount is zero. This behaviour is inconsistent and can lead to confusing Deposited events being emitted that may break third-party off-chain tracking.  
   Adopt a universal rejection of zero amount deposits.

10. **Magic Numbers**  
    **Related Asset(s):** `NavHelper.sol`, `TreehouseRouter.sol`  
    Some contracts contain hardcoded numbers or addresses which can make updating the codebase tedious and risk introducing errors by update omission.  
    Replace instances of hardcoded numbers or addresses with named constants.

11. **Asset Addresses Defined Multiple Times**  
    **Related Asset(s):** `strategy/libs/TokenUtils.sol`, `strategy/actions/lido/helpers/MainnetLidoAddresses.sol`, `TreehouseRouter.sol`  
    Several token addresses are defined in multiple contracts; this increases developer overhead when updating these addresses and can lead to bugs in the event where one contract is not updated.  
    For contracts that are needed by multiple contracts, it is best these are defined in one contract and then inherited by all contracts using them.

12. **Equality To Boolean Checks**  
    **Related Asset(s):** `TreehouseRouter.sol`, `Vault.sol`  
    In several places, a boolean return condition is checked for equality to a boolean as follows:
    ```python
    f(x) == False
    ```
    This is unnecessary as this can be replaced with the return of the left-hand side of the assignment only.  
    Remove redundant uses of equality to booleans in the files noted.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The comments above have been acknowledged by the development team, and relevant changes actioned in commit `d8ba5d7` where relevant.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Treehouse |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/treehouse/review.pdf

### Keywords for Search

`vulnerability`

