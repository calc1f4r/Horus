---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54163
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55
source_link: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - JCN
  - Anurag Jain
---

## Vulnerability Title

ESynth can restrict borrowers from performing common actions 

### Overview

See description below for full details.

### Original Finding Content

## ESynths and Synthetic Vaults

## Context
(No context files were provided by the reviewer)

## Description
According to code documentation, ESynths are able to be used as collateral in other vaults, but will also be the underlying (i.e. borrowable) asset in Synthetic Vaults. 

Synthetic Vaults include hook contracts that disable deposit related operations for all addresses except for the actual ESynth itself. The owner of the ESynth can deposit ESynth into the Synthetic Vault via `ESynth::allocate`:

### Function: `ESynth::allocate`
```solidity
function allocate(address vault, uint256 amount) external onlyOwner {
    if (IEVault(vault).EVC() != address(evc)) {
        revert E_NotEVCCompatible();
    }
    ignoredForTotalSupply.add(vault);
    _approve(address(this), vault, amount, true); // @audit: approve synthetic vault to handle amount of `ESynth` in `ESynth` contract
    IEVault(vault).deposit(amount, address(this)); // @audit: supply `ESynth` to the Synthetic Vault
}
```

Users can then borrow this ESynth from the Synthetic Vault. However, we will notice that the ESynth contract inherits from the `ERC20Collateral` abstract contract and therefore account status checks are performed for the address whose ESynth balance is decreasing (the "from" address) for transfers and burns:

### Function: `ERC20Collateral::_update`
```solidity
function _update(address from, address to, uint256 value) internal virtual override {
    super._update(from, to, value);
    
    if (from != address(0)) {
        evc.requireAccountStatusCheck(from); // @audit: schedule account status check for the "from"
    }
}
```

The above restrictions are appropriate when the ESynth is used solely as a collateral asset in a vault but can inadvertently restrict borrowers from performing common actions when it is used as a borrowable asset. For example, account health checks are unnecessary to perform during repayment, since this action can only increase an account's health.

### Function: `Borrowing::repay`
```solidity
function repay(uint256 amount, address receiver) public virtual nonReentrant returns (uint256) {
    (VaultCache memory vaultCache, address account) = initOperation(OP_REPAY, CHECKACCOUNT_NONE); // @audit: no account status check scheduled
    // ...
    pullAssets(vaultCache, account, assets);
}
```

As shown above, the EVK correctly does not perform account status checks during a repayment action. On line 89, the underlying asset of the vault is transferred from the account (user initiating the repay) to the Vault.

### Function: `AssetTransfers::pullAssets`
```solidity
function pullAssets(VaultCache memory vaultCache, address from, Assets amount) internal virtual {
    vaultCache.asset.safeTransferFrom(from, address(this), amount.toUint(), permit2);
}
```

For normal underlying assets, such as USDC, there are no additional checks performed at this stage. Repayment via this Vault would therefore allow a borrower to partially repay their unhealthy position and move themselves closer to health, despite their account status potentially remaining unhealthy after the repayment.

However, since ESynth schedules account status checks for the "from" address of all transfers, borrowers who are attempting to partially repay their unhealthy position directly (`account == borrower` and `receiver == borrower`), will not be able to do so if their post-account health remains unhealthy, despite the fact that their position may have gotten healthier.

When the Synthetic Vault has a gap between the `borrowLTV` (80%) and the `liquidationLTV` (90%), there can be multiple honest actions that a borrower can attempt but will revert if, post-action, their account LTV ratio remains somewhere between the `borrowLTV` and the `liquidationLTV` (i.e., they cannot perform new borrows and they are not eligible for liquidation):

1. Borrower borrows up to max borrow amount, therefore their account LTV ratio is < `borrowLTV`. Interest accrues and their account LTV ratio becomes >= `borrowLTV`. The borrower is unable to freely utilize their borrowed ESynth until they perform a repayment so that their account LTV ratio drops below the `borrowLTV`. Note that at this point the borrower is not eligible for liquidation and they should only be restricted from withdrawing collateral or performing new borrows.
2. Borrower's account becomes eligible for liquidation (`account LTV ratio >= liquidationLTV`). Borrower does not have enough ESynth on hand to repay an amount that brings their account completely into health (< `borrowLTV`), so they opt to partially repay their unhealthy position to move themselves out of the liquidation zone or lessen their liquidation penalty (improve their account health). I.e., their post account LTV ratio would be > `borrowLTV` & < `liquidationLTV`. However, the ESynth would restrict this borrower from moving their account closer to health. Note that it is also possible for a borrower to be restricted from lessening their liquidation penalty even if `borrowLTV == liquidationLTV`.

## Impact
Borrowers who have a debt position inside of synthetic vaults may not be able to freely utilize their borrowed assets if their post account status remains unhealthy. This can grief the borrower in the best case, but in the worst case, it can result in the borrower being unable to save themselves from liquidation events.

## Technicalities
In regards to the first example from the previous section, the borrower is able to perform a repay to bring their position's LTV ratio below the `borrowLTV` and then freely utilize their borrowed funds. However, this introduces a new restriction on the borrower as they are now forced to perform repayments, which can be seen as an unnecessary additional burden to the borrower that they must remediate before they can utilize their funds.

In regards to the second example from the previous section, the borrower is able to partially repay their position via an alternative account that is healthy. However, seeing as it is likely that borrowers will repay their positions directly (with the same unhealthy account), the borrower in this case would have to transfer their assets to their alternative account, approve that account to operate on behalf of their unhealthy account, and then execute another repay transaction. Thus, the impact for this example can be viewed as griefing since they have to perform multiple additional transactions in order to work around a blocked action.

Additionally, since liquidations are time-sensitive events, a borrower who is partially repaying their unhealthy position via their own account may not have sufficient time to troubleshoot the reason for the initial transaction reversion and perform the alternative actions above. Thus, the borrower in this case would be unable to save themselves from liquidation and will unnecessarily lose funds to a liquidator.

## Proof of Concept
Copy the contents below into the `./test/unit/evault/POC.t.sol` file and run with `forge test --mc POC_Test`:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {EVaultTestBase} from "./EVaultTestBase.t.sol";
import "../../../src/EVault/shared/types/Types.sol";
import "../../../src/EVault/shared/Constants.sol";
import {ESynth} from "../../../src/Synths/ESynth.sol";
import {TestERC20} from "../../mocks/TestERC20.sol";
import {Errors} from "../../../src/EVault/shared/Errors.sol";

contract POC_Test is EVaultTestBase {
    using TypesLib for uint256;
    
    ESynth esynth;
    TestERC20 assetTSTSynth;
    IEVault eTSTSynth;
    address depositor;
    address borrower;

    function setUp() public override {
        super.setUp();
        
        // Setup ESynth and ESVault
        esynth = ESynth(address(new ESynth(evc, "Test Synth", "TST")));
        assetTSTSynth = TestERC20(address(esynth));
        eTSTSynth = createSynthEVault(address(assetTSTSynth));
        esynth.setCapacity(address(this), type(uint128).max);
        esynth.mint(address(esynth), 100e18);
        esynth.allocate(address(eTSTSynth), 100e18);

        // Actors
        depositor = makeAddr("depositor");
        borrower = makeAddr("borrower");

        // Setup oracles for all vaults
        oracle.setPrice(address(assetTST), unitOfAccount, 1e18);
        oracle.setPrice(address(assetTSTSynth), unitOfAccount, 1e18);
        oracle.setPrice(address(eTST2), unitOfAccount, 1e18);

        // Set borrowLTV to 80% and liquidationLTV to 90%
        eTST.setLTV(address(eTST2), 0.8e4, 0.9e4, 0);
        eTSTSynth.setLTV(address(eTST2), 0.8e4, 0.9e4, 0);
        
        // Depositor for EVault
        vm.startPrank(depositor);
        assetTST.mint(depositor, type(uint256).max);
        assetTST.approve(address(eTST), type(uint256).max);
        eTST.deposit(100e18, depositor);
        vm.stopPrank();

        // Borrower
        vm.startPrank(borrower);
        assetTST2.mint(borrower, type(uint256).max);
        assetTST2.approve(address(eTST2), type(uint256).max);
        vm.stopPrank();
    }

    function test_partially_repay_unhealthy_position_eVault() external {
        _attempt_partial_repay(eTST, assetTST, false);
    }

    function test_partially_repay_unhealthy_position_esVault() external {
        _attempt_partial_repay(eTSTSynth, assetTSTSynth, true);
    }

    function _attempt_partial_repay(IEVault controller, TestERC20 controllerAsset, bool isSynth) internal {
        // Deposit collaterals into collateral vault and enable vaults
        vm.startPrank(borrower);
        eTST2.deposit(10e18, borrower);
        evc.enableCollateral(borrower, address(eTST2));
        evc.enableController(borrower, address(controller));

        // Borrower borrows from controller
        controller.borrow(5e18, borrower);
        assertEq(controllerAsset.balanceOf(borrower), 5e18);
        vm.stopPrank();

        // Borrower's position is healthy (cannot be liquidated)
        (uint256 collateralValue, uint256 debtValue) = controller.accountLiquidity(borrower, true); // check liquidity via liquidationLTV
        assertGt(collateralValue, debtValue);

        // Collateral asset's value falls
        oracle.setPrice(address(eTST2), unitOfAccount, 5e17);

        // Borrower's position is now unhealthy (can be liquidated)
        (collateralValue, debtValue) = controller.accountLiquidity(borrower, true); // check liquidity via liquidationLTV
        assertGt(debtValue, collateralValue);

        // Borrower attempts to partially repay unhealthy position to move out of liquidation zone
        vm.startPrank(borrower);
        controllerAsset.approve(address(controller), 6e17);
        if (isSynth) {
            // Borrower attempts to partially repay position
            vm.expectRevert(Errors.E_AccountLiquidity.selector);
            controller.repay(6e17, borrower); // esVault prevents borrower from moving closer to health as it schedules an account status check
            
            // Borrower's position can still be liquidated
            (collateralValue, debtValue) = controller.accountLiquidity(borrower, true); // check liquidity via liquidationLTV
            assertGt(debtValue, collateralValue);
        } else {
            // Borrower attempts to partially repay position
            controller.repay(6e17, borrower); // eVault allows borrower to move closer to health as it does not schedule an account status check
            
            // Borrower's position can no longer be liquidated
            (collateralValue, debtValue) = controller.accountLiquidity(borrower, true); // check liquidity via liquidationLTV
            assertGt(collateralValue, debtValue);

            // Borrower's position is still unhealthy in regards to the borrowLTV (account status checks would fail)
            (collateralValue, debtValue) = controller.accountLiquidity(borrower, false); // check liquidity via borrowLTV
            assertGt(debtValue, collateralValue);
        }
    }
}
```

## Recommendation
When ESynth is used as a collateral asset in collateral vaults, the functionality of scheduling account status checks for the sender is appropriate since the collateral is actively being used to back a loan. However, when the ESynth is used as a borrowable asset in a controller, this functionality leads to edge cases where borrowers can be griefed when performing repayments and attempting to utilize their borrowed funds.

Below is a possible mitigation that would address the edge case for blocked repayments:
- **Add a config flag** to identify if the vault is a synthetic vault, i.e., if the underlying asset is an ESynth asset. If the underlying asset is an ESynth, then we can forgive the account status check that is scheduled during the `pullAssets` internal function call at the end of the `repay` function.

The edge case for blocking utilization of borrowed funds would require a more fundamental mitigation. This is due to the fact that a borrowed asset should not have the same restrictions as an asset used as collateral. Therefore, an additional abstract contract for Borrowable assets (similar to `ERC20Collateral`) can be created that defines functionality specific to a borrowable asset. This would differentiate between an ESynth that is meant to be used as a collateral asset in collateral vaults and an ESynth that is meant to be used as an underlying asset in a controller.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | JCN, Anurag Jain |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

