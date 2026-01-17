---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49042
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
github_link: https://github.com/code-423n4/2024-07-loopfi-findings/issues/245

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

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - nnez
  - joaovwfreire
  - zhaojohnson
  - pkqs90
  - 0xbepresent
---

## Vulnerability Title

[M-05] `PositionAction4626::increaseLever` will always revert

### Overview



This bug report discusses an issue with the `PositionAction::increaseLever` function in the LoopFi code. This function allows users to increase their positions' leverage by taking a flash loan and doing some swaps. However, the report found that for ERC4626 collateral positions, the function is not working properly. The `_onIncreaseLever` function is both approving and depositing the collateral into the vault under the wrong address, which causes it to always revert and never work. The report also includes a proof of concept to demonstrate the issue. The recommended mitigation step is to replace a line of code in the `_onIncreaseLever` function. The assessed type of this bug is DoS (Denial of Service).

### Original Finding Content


Users can use `PositionAction::increaseLever` to increase their positions' leverage, i.e., increasing both the collateral and debt, by taking a flash loan and doing some swaps. At the end of the process, after swapping "borrow" tokens to underlying tokens they should be returned to the vault under the position's "name".

For ERC20 collateral positions, this is happening in `PositionAction20::_onIncreaseLever` (that gets called in `PositionAction::onFlashLoan`) which approves the vault to spend some amount and then returns the amount to be later sent using the following in `PositionAction::onFlashLoan`:

```solidity
// add collateral and debt
ICDPVault(leverParams.vault).modifyCollateralAndDebt(
    leverParams.position,
    address(this),
    address(this),
    toInt256(collateral),
    toInt256(addDebt)
);
```

However, for ERC4626 collateral positions, `PositionAction4626::_onIncreaseLever` is both approving the amount and depositing it into the vault under `address(this)` which IS NOT the position's proxy but `PositionAction4626` contract as it is the flash loan callback function and isn't delegated like `increaseLever`. When `_onIncreaseLever` finishes, it'll try to deposit the collateral AGAIN in the vault using [this](https://github.com/code-423n4/2024-07-loopfi/blob/main/src/proxy/PositionAction.sol#L416-L422); which will for sure revert, as the approval was spent and no funds are left to make the deposit.

This will cause `PositionAction4626::increaseLever` to always revert and never work, blocking users from leveraging their positions.

### Proof of Concept

<details>

```solidity
contract PositionAction4626_Lever_Test is IntegrationTestBase {
    using SafeERC20 for ERC20;

    PRBProxy userProxy;
    address user;
    uint256 constant userPk = 0x12341234;
    CDPVault vault;
    StakingLPEth stakingLPEth;
    PositionAction4626 positionAction;
    PermitParams emptyPermitParams;
    SwapParams emptySwap;
    PoolActionParams emptyPoolActionParams;

    bytes32[] weightedPoolIdArray;

    function setUp() public override {
        super.setUp();
        setGlobalDebtCeiling(15_000_000 ether);

        stakingLPEth = new StakingLPEth(address(token), "Staking LP ETH", "sLPETH");
        vault = createCDPVault(stakingLPEth, 5_000_000 ether, 0, 1.25 ether, 1.0 ether, 1.05 ether);
        createGaugeAndSetGauge(address(vault));

        gauge.addQuotaToken(address(stakingLPEth), 10, 100);

        user = vm.addr(0x12341234);
        userProxy = PRBProxy(payable(address(prbProxyRegistry.deployFor(user))));

        positionAction = new PositionAction4626(
            address(flashlender),
            address(swapAction),
            address(poolAction),
            address(vaultRegistry)
        );

        oracle.updateSpot(address(token), 1 ether);
        oracle.updateSpot(address(stakingLPEth), 1 ether);
        weightedPoolIdArray.push(weightedUnderlierPoolId);
    }

    function test_increaseLeverDOS() public {
        uint256 amount = 200 ether;

        deal(address(token), user, amount);

        address[] memory assets = new address[](2);
        assets[0] = address(underlyingToken);
        assets[1] = address(token);

        vm.startPrank(user);

        // Approvals
        token.approve(address(stakingLPEth), amount);
        stakingLPEth.approve(address(vault), amount);

        // Deopsit token to get sLPETH
        stakingLPEth.deposit(amount, user);

        // Deposit sLPETH to vault
        vault.deposit(address(userProxy), amount);

        // Borrow underlying tokens
        userProxy.execute(
            address(positionAction),
            abi.encodeWithSelector(
                positionAction.borrow.selector,
                address(userProxy),
                address(vault),
                CreditParams({amount: amount / 2, creditor: user, auxSwap: emptySwap})
            )
        );

        // Increase leverage will always revert
        vm.expectRevert(bytes("ERC20: insufficient allowance"));
        userProxy.execute(
            address(positionAction),
            abi.encodeWithSelector(
                positionAction.increaseLever.selector,
                LeverParams({
                    position: address(userProxy),
                    vault: address(vault),
                    collateralToken: address(stakingLPEth),
                    primarySwap: SwapParams({
                        swapProtocol: SwapProtocol.BALANCER,
                        swapType: SwapType.EXACT_IN,
                        assetIn: address(underlyingToken),
                        amount: amount / 2,
                        limit: 0,
                        recipient: address(positionAction),
                        deadline: block.timestamp,
                        args: abi.encode(weightedPoolIdArray, assets)
                    }),
                    auxSwap: emptySwap,
                    auxAction: emptyPoolActionParams
                }),
                address(0),
                0,
                address(user),
                emptyPermitParams
            )
        );
    }
}
```

</details>

### Recommended Mitigation Steps

In `PositionAction4626::_onIncreaseLever`, replace:

```solidity
return ICDPVault(leverParams.vault).deposit(address(this), addCollateralAmount);
```

with:

```solidity
return addCollateralAmount;
```

### Assessed type

DoS

**[amarcu (LoopFi) confirmed](https://github.com/code-423n4/2024-07-loopfi-findings/issues/245#event-14319528697)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | nnez, joaovwfreire, zhaojohnson, pkqs90, 0xbepresent, Nyx, hash, web3km, 0xAlix2 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: https://github.com/code-423n4/2024-07-loopfi-findings/issues/245
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

