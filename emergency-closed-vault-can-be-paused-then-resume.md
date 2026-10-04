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
solodit_id: 27599
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
finders_count: 5
finders:
  - marqymarq10
  - kz0213871
  - nmirchev8
  - Giorgio
  - nisedo
---

## Vulnerability Title

Emergency Closed Vault Can Be Paused Then Resume

### Overview


This bug report is about the Emergency Closed Vault, which is a final measure to repay all debts and shut down the vault permanently. However, a pathway exists to effectively reopen the vault after it has been closed using `emergencyClose` by invoking the `emergencyPause` and `emergencyResume` functions. This contradicts the intended irreversible nature of an emergency close and exposes the vault to additional risks. A proof of concept was provided, and two recommendations were made to fix the issue. The first is to implement a permanent state or flag within the vault's storage to irrevocably mark the vault as closed after `emergencyClose` is called. The second is to modify the `emergencyPause` and `emergencyResume` functions to check for this permanent closure flag and revert if the vault has been emergency closed.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L47-L66">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L47-L66</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L72-L91">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L72-L91</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L111-L156">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L111-L156</a>


## Vulnerability Details

The `emergencyClose` function is intended to be a final measure to repay all debts and shut down the vault permanently, as indicated by the function's documentation. This action should be irreversible to ensure the finality and security of the vault's emergency closure process.

```solidity
File: GMXVaul.sol
  /**
    * @notice Repays all debt owed by vault and shut down vault, allowing emergency withdrawals
    * @dev Note that this is a one-way irreversible action
    * @dev Should be called by approved Owner (Timelock + MultiSig)
    * @param deadline Timestamp of swap deadline
  */
  function emergencyClose(uint256 deadline) external onlyOwner {
    GMXEmergency.emergencyClose(_store, deadline);
  }
```

However, a pathway exists to effectively reopen a vault after it has been closed using `emergencyClose` by invoking the `emergencyPause` and `emergencyResume` functions. These functions alter the vault's status, allowing for the resumption of operations which contradicts the intended irreversible nature of an emergency close.

```solidity
File: GMXEmergency.sol
  function emergencyPause(
    GMXTypes.Store storage self
  ) external {
    self.refundee = payable(msg.sender);


    GMXTypes.RemoveLiquidityParams memory _rlp;


    // Remove all of the vault's LP tokens
    _rlp.lpAmt = self.lpToken.balanceOf(address(this));
    _rlp.executionFee = msg.value;


    GMXManager.removeLiquidity(
      self,
      _rlp
    );


    self.status = GMXTypes.Status.Paused;


    emit EmergencyPause();
  }
```
```solidity
File: GMXEmergency.sol
  function emergencyResume(
    GMXTypes.Store storage self
  ) external {
    GMXChecks.beforeEmergencyResumeChecks(self);


    self.status = GMXTypes.Status.Resume;


    self.refundee = payable(msg.sender);


    GMXTypes.AddLiquidityParams memory _alp;


    _alp.tokenAAmt = self.tokenA.balanceOf(address(this));
    _alp.tokenBAmt = self.tokenB.balanceOf(address(this));
    _alp.executionFee = msg.value;


    GMXManager.addLiquidity(
      self,
      _alp
    );
  }
```

## Impact

The impact of this finding is significant, as it undermines the trust model of the emergency close process. Users and stakeholders expect that once a vault is closed in an emergency, it will remain closed as a protective measure. The ability to resume operations after an emergency closure could expose the vault to additional risks and potentially be exploited by malicious actors, especially if the original closure was due to a security threat.

## PoC

Add this to GMXEmergencyTest.t.sol and test with `forge test --mt test_close_then_pause -vv`:
```solidity
  function test_close_then_pause() external {
    // Pause the vault
    vault.emergencyPause();
    console2.log("vault status", uint256(vault.store().status));

    // Close the vault
    vault.emergencyClose(deadline);
    console2.log("vault status", uint256(vault.store().status));

    // Pause the vault again
    vault.emergencyPause();
    console2.log("vault status", uint256(vault.store().status));
    assertEq(uint256(vault.store().status), 10, "vault status not set to paused");

    // Resume the vault
    vault.emergencyResume();
    console2.log("vault status", uint256(vault.store().status));
  }
```

## Recommendations

1. Implement a permanent state or flag within the vault's storage to irrevocably mark the vault as closed after `emergencyClose` is called. This flag should prevent any further state-altering operations.

2. Modify the `emergencyPause` and `emergencyResume` functions to check for this permanent closure flag and revert if the vault has been emergency closed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | marqymarq10, kz0213871, nmirchev8, Giorgio, nisedo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

