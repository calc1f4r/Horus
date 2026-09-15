---
# Core Classification
protocol: Malt Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1091
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-malt-finance-contest
source_link: https://code4rena.com/reports/2021-11-malt
github_link: https://github.com/code-423n4/2021-11-malt-findings/issues/263

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - 0x0x0x  gzeon
---

## Vulnerability Title

[H-01] Timelock can be bypassed

### Overview


This bug report is about a Timelock contract, which is meant to put a limit on the privileges of the governor by forcing a two step process with a preset delay time. However, the current implementation allows the governor to execute any transactions without any constraints. This is done by the governor calling the Timelock#setGovernor(address _governor) function and setting a new governor effective immediately, and then the new governor can call Timelock#setDelay() and change the delay to 0, also effective immediately. The new governor then has unrestricted access to privileges, including granting minter role to any address and minting unlimited amounts of MALT.

The recommendation is to consider making the setGovernor and setDelay functions only callable from the Timelock contract itself, by changing the onlyRole(GOVERNOR_ROLE, "Must have timelock role") to require(msg.sender == address(this), "..."), and also changing the _adminSetup(_admin) in Timelock#initialize() to _adminSetup(address(this)). This would ensure that all roles are managed by the timelock itself.

### Original Finding Content

_Submitted by WatchPug, also found by 0x0x0x and gzeon_

The purpose of a Timelock contract is to put a limit on the privileges of the `governor`, by forcing a two step process with a preset delay time.

However, we found that the current implementation actually won't serve that purpose as it allows the `governor` to execute any transactions without any constraints.

To do that, the current governor can call `Timelock#setGovernor(address _governor)` and set a new `governor` effective immediately.

And the new `governor` can then call `Timelock#setDelay()` and change the delay to `0`, also effective immediately.

The new `governor` can now use all the privileges without a delay, including granting minter role to any address and mint unlimited amount of MALT.

In conclusion, a Timelock contract is supposed to guard the protocol from lost private key or malicious actions. The current implementation won't fulfill that mission.

<https://github.com/code-423n4/2021-11-malt/blob/c3a204a2c0f7c653c6c2dda9f4563fd1dc1cecf3/src/contracts/Timelock.sol#L98-L105>

```solidity
  function setGovernor(address _governor)
    public
    onlyRole(GOVERNOR_ROLE, "Must have timelock role")
  {
    _swapRole(_governor, governor, GOVERNOR_ROLE);
    governor = _governor;
    emit NewGovernor(_governor);
  }
```

<https://github.com/code-423n4/2021-11-malt/blob/c3a204a2c0f7c653c6c2dda9f4563fd1dc1cecf3/src/contracts/Timelock.sol#L66-L77>

```solidity
  function setDelay(uint256 _delay)
    public
    onlyRole(GOVERNOR_ROLE, "Must have timelock role")
  {
    require(
      _delay >= 0 && _delay < gracePeriod,
      "Timelock::setDelay: Delay must not be greater equal to zero and less than gracePeriod"
    );
    delay = _delay;

    emit NewDelay(delay);
  }
```

#### Recommendation

Consider making `setGovernor` and `setDelay` only callable from the Timelock contract itself.

Specificaly, changing from `onlyRole(GOVERNOR_ROLE, "Must have timelock role")` to `require(msg.sender == address(this), "...")`.

Also, consider changing `_adminSetup(_admin)` in `Timelock#initialize()` to `_adminSetup(address(this))`, so that all roles are managed by the timelock itself as well.

**[0xScotch (sponsor) confirmed](https://github.com/code-423n4/2021-11-malt-findings/issues/263)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-11-malt-findings/issues/263#issuecomment-1008067115):**
 > The warden has identified an exploit that allows to sidestep the delay for the timelock, effectively bypassing all of the timelock's security guarantees. Because of the gravity of this, I agree with the high risk severity.
> 
> Mitigation can be achieved by ensuring that all operations run under a time delay





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Finance |
| Report Date | N/A |
| Finders | WatchPug, 0x0x0x  gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-malt
- **GitHub**: https://github.com/code-423n4/2021-11-malt-findings/issues/263
- **Contest**: https://code4rena.com/contests/2021-11-malt-finance-contest

### Keywords for Search

`vulnerability`

