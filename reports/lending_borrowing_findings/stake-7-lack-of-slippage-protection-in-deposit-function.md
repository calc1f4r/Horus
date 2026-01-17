---
# Core Classification
protocol: Stakewise
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62392
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-09-19-StakeWise.md
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
  - Hexens
---

## Vulnerability Title

[STAKE-7] Lack of slippage protection in deposit function

### Overview


The `deposit()` function in the `LeverageStrategy.sol` contract has a bug that could result in users receiving fewer tokens than expected or facing losses without being able to fix it. This is because the function does not have a check for slippage, meaning that if token prices change between when the transaction is submitted and executed, the user may not receive the expected number of tokens. This could negatively impact their strategy. The bug has been acknowledged and the suggested solution is to allow users to specify a minimum number of `osTokenShares` they are willing to accept after leverage calculations.

### Original Finding Content

**Severity:** Medium

**Path:** src/leverage/LeverageStrategy.sol::deposit()#L125-L182

**Description:** The `deposit()` function in the `LeverageStrategy.sol` contract executes several key operations involving token transfers, asset borrowing, and minting, including the potential use of flash loans. However, it lacks slippage protection, meaning that if token prices fluctuate between the time the transaction is submitted and executed, users could receive fewer tokens or face adverse outcomes without the ability to revert or mitigate the loss.

In particular, the function lacks checks to ensure that the actual number of `osTokenShares` minted matches expectations after asset borrowing.

Example:
A user submits a transaction to deposit 100 `osTokenShares`, expecting to leverage them to borrow additional assets. Between the time the transaction is broadcasted and mined, market conditions change (e.g., a large price movement), leading to less favorable borrowing conditions. Since there is no slippage check, the user could end up with fewer minted `osTokenShares` than expected, negatively impacting their strategy.
```
    function deposit(address vault, uint256 osTokenShares) external {
        if (osTokenShares == 0) revert Errors.InvalidShares();

        // fetch strategy proxy
        (address proxy,) = _getOrCreateStrategyProxy(vault, msg.sender);
        if (isStrategyProxyExiting[proxy]) revert Errors.ExitRequestNotProcessed();

        // transfer osToken shares from user to the proxy
        IStrategyProxy(proxy).execute(
            address(_osToken), abi.encodeWithSelector(_osToken.transferFrom.selector, msg.sender, proxy, osTokenShares)
        );

        // fetch vault state and lending protocol state
        (uint256 stakedAssets, uint256 mintedOsTokenShares) = _getVaultState(vault, proxy);
        (uint256 borrowedAssets, uint256 suppliedOsTokenShares) = _getBorrowState(proxy);

        // check whether any of the positions exist
        uint256 leverageOsTokenShares = osTokenShares;
        if (stakedAssets != 0 || mintedOsTokenShares != 0 || borrowedAssets != 0 || suppliedOsTokenShares != 0) {
            // supply osToken shares to the lending protocol
            _supplyOsTokenShares(proxy, osTokenShares);
            suppliedOsTokenShares += osTokenShares;

            // borrow max amount of assets from the lending protocol
            uint256 maxBorrowAssets =
                Math.mulDiv(_osTokenVaultController.convertToAssets(suppliedOsTokenShares), _getBorrowLtv(), _wad);
            if (borrowedAssets >= maxBorrowAssets) {
                // nothing to borrow
                emit Deposited(vault, msg.sender, osTokenShares, 0);
                return;
            }
            uint256 assetsToBorrow;
            unchecked {
                // cannot underflow because maxBorrowAssets > borrowedAssets
                assetsToBorrow = maxBorrowAssets - borrowedAssets;
            }
            _borrowAssets(proxy, assetsToBorrow);

            // mint max possible osToken shares
            leverageOsTokenShares = _mintOsTokenShares(vault, proxy, assetsToBorrow, type(uint256).max);
            if (leverageOsTokenShares == 0) {
                // no osToken shares to leverage
                emit Deposited(vault, msg.sender, osTokenShares, 0);
                return;
            }
        }

        // calculate flash loaned osToken shares
        uint256 flashloanOsTokenShares = _getFlashloanOsTokenShares(vault, leverageOsTokenShares);

        // execute flashloan
        _osTokenFlashLoans.flashLoan(
            address(this), flashloanOsTokenShares, abi.encode(FlashloanAction.Deposit, vault, proxy)
        );

        // emit event
        emit Deposited(vault, msg.sender, osTokenShares, flashloanOsTokenShares);
    }
```

**Remediation:**  Allow users to specify a minimum number of `osTokenShares` they are willing to accept after leverage calculations.

**Status:**  Acknowledged

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Stakewise |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-09-19-StakeWise.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

