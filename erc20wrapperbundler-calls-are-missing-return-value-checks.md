---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54338
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
github_link: none

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
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - J4X98
---

## Vulnerability Title

ERC20WrapperBundler calls are missing return value checks 

### Overview


This bug report discusses a vulnerability in the ERC20WrapperBundler contract, specifically in the `erc20WrapperDepositFor()` and `erc20WrapperWithdrawTo()` functions. The issue arises when the contract fails to check the boolean return value of the underlying ERC20Wrapper functions. This can lead to a scenario where a user's tokens are left vulnerable to theft if the wrapper fails to transfer them out of the bundler. A proof of concept is provided to demonstrate the issue and a recommendation is made to mitigate it by incorporating return value checks for these functions. 

### Original Finding Content

## ERC20WrapperBundler Vulnerability Report

## Context
- **File**: ERC20WrapperBundler.sol
- **Lines**: L38, L54

## Description
The Morpho Blue bundler offers users the capability to bundle calls, including interactions with contracts that implement the ERC20Wrapper interface. This functionality is facilitated through the `erc20WrapperDepositFor()` and `erc20WrapperWithdrawTo()` functions.

The current implementation presents a vulnerability as it neglects to check the boolean return value of the underlying ERC20Wrapper functions. While the OpenZeppelin implementation returns `true` for successful calls and reverts on errors, alternative implementations may simply return `false` in case of an unsuccessful call, allowing the call to proceed without reverting. 

Given that the documentation specifies the assumption that the wrapper implements the ERC20Wrapper interface without explicitly detailing the OpenZeppelin functionality, variations in implementation are valid. Consequently, this issue may result in a scenario where a user sends tokens for wrapping to the contract, but the wrapper fails to transfer them out of the bundler (e.g., due to a blocklist) and returns `false`. Since the return value is not checked, the execution continues, leaving the user's tokens within the bundler and vulnerable to theft.

This issue can lead to a potential loss of user funds as a user will expect the bundler to revert in the case of any of the transferring functions failing, but instead, the bundler will finish the execution, leaving tokens in the bundler. These tokens could then be stolen by anyone.

## Proof of Concept
To simulate this issue, a simple ERC20Wrapper that returns `false` on an incorrect deposit instead of reverting has been implemented:

```solidity
import {IERC20} from "../../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

contract ERC20WrapperNotReverting {
    IERC20 private immutable _underlying;
    mapping(address => uint256) public balances;

    constructor(IERC20 underlyingToken) {
        _underlying = underlyingToken;
    }

    function underlying() public view returns (IERC20) {
        return _underlying;
    }

    /**
     * @dev Allow a user to deposit underlying tokens and mint the corresponding number of wrapped tokens.
     */
    function depositFor(address account, uint256 amount) public virtual returns (bool) {
        if(msg.sender != address(0x123456)) {
            // Simulating only dedicated users being allowed to call the function
            return false;
        }
        _underlying.transferFrom(msg.sender, address(this), amount);
        balances[account] += amount;
        return true;
    }
}
```

In the following proof of concept, the issue occurs:

```solidity
function testErc20WrapperDepositForNoRevert() public {
    // Deploy the non-reverting mock
    ERC20WrapperNotReverting wrapper2 = new ERC20WrapperNotReverting(loanToken);
    bundle.push(_erc20WrapperDepositFor(address(wrapper2), 100));
    loanToken.setBalance(address(bundler), 100);
    vm.prank(RECEIVER);
    bundler.multicall(bundle);
    // Tokens are still left in the contract but it didn't revert
    assertEq(loanToken.balanceOf(address(bundler)), 100, "loan.balanceOf(bundler)");
    assertEq(loanWrapper.balanceOf(RECEIVER), 0, "loanWrapper.balanceOf(RECEIVER)");
}
```

The testcase can be run by:
1. Adding the `ERC20WrapperNotReverting` contract to the `morpho-blue-bundlers/src/mocks` folder.
2. Importing it using `import {ERC20WrapperNotReverting} from "../../src/mocks/ERC20WrapperNotReverting.sol";`.
3. Adding the testcase to `morpho-blue-bundlers/test/forge/ERC20WrapperBundlerBundlerLocalTest`.
4. Running it using `forge test -vvvv --match-test "testErc20WrapperDepositForNoRevert"`.

## Recommendation
Mitigate this issue by incorporating return value checks for the calls to the functions `ERC20Wrapper(wrapper).depositFor()` and `ERC20Wrapper(wrapper).withdrawTo()`. The recommended adjustments are as follows:

- **Deposit**:
  ```solidity
  bool success = ERC20Wrapper(wrapper).depositFor(initiator(), amount);
  require(success, "Deposit was unsuccessful");
  ```

- **Withdrawal**:
  ```solidity
  bool success = ERC20Wrapper(wrapper).withdrawTo(account, amount);
  require(success, "Withdraw was unsuccessful");
  ```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | J4X98 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad

### Keywords for Search

`vulnerability`

