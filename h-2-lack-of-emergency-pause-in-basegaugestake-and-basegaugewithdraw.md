---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57141
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 20
finders:
  - 1337web3
  - zegarcao
  - iamephraim
  - theirrationalone
  - mahivasisth
---

## Vulnerability Title

[H-2] Lack of Emergency Pause in `BaseGauge::stake` and `BaseGauge::withdraw

### Overview


The report discusses a bug in the BaseGauge contract that does not properly handle an emergency pause situation. This can lead to significant financial losses if the contract is hacked or exploited. The report provides a proof of concept and recommends applying a modifier to prevent users from staking or withdrawing funds when the contract is paused. The bug was identified through a manual review.

### Original Finding Content

**Description:**\
Staking and withdrawal functions are critical components of a contract’s security, especially in emergency scenarios. If the contract is compromised (e.g., hacked or exploited), it is crucial to **immediately halt staking and withdrawal** to prevent further loss of funds.

While `BaseGauge.sol` includes an `setEmergencyPaused` function to toggle the emergency pause state, this modifier is **not applied** to the `stake` and `withdraw` functions. As a result, even if an emergency pause is triggered, users—including attackers—can still stake or withdraw funds, rendering the emergency mechanism ineffective.

**Impact:**\
In the event of an exploit or malicious activity, the protocol's administrators may attempt to activate `setEmergencyPaused` to stop unauthorized fund movements. However, since `stake` and `withdraw` **do not respect the paused state**, attackers can **continue withdrawing or moving assets**, potentially leading to significant financial losses.

#### **Attack Scenario:**

1. A hacker gains unauthorized access and begins withdrawing large amounts of protocol funds.
2. The `EMERGENCY_ADMIN` detects the exploit and activates `setEmergencyPaused`.
3. Despite this, the hacker **continues withdrawing or staking funds**, since these functions lack the emergency pause restriction.

**Proof of Concept:**

The `stake` and `withdraw` functions lack the emergency pause modifier, allowing them to function even when the contract is paused:

```solidity
function stake(uint256 amount) external nonReentrant updateReward(msg.sender) { 
    //@audit lacks setEmergencyPaused modifier
    if (amount == 0) revert InvalidAmount();
    _totalSupply += amount;
    _balances[msg.sender] += amount;
    stakingToken.safeTransferFrom(msg.sender, address(this), amount);
    emit Staked(msg.sender, amount);
}

function withdraw(uint256 amount) external nonReentrant updateReward(msg.sender) { 
    //@audit lacks setEmergencyPaused modifier
    if (amount == 0) revert InvalidAmount();
    if (_balances[msg.sender] < amount) revert InsufficientBalance();
    _totalSupply -= amount;
    _balances[msg.sender] -= amount;
    stakingToken.safeTransfer(msg.sender, amount);
    emit Withdrawn(msg.sender, amount);
}
```

Meanwhile, the **pause function exists but is not enforced in stake/withdraw**:

```solidity
function setEmergencyPaused(bool paused) external {
    if (!hasRole(EMERGENCY_ADMIN, msg.sender)) revert UnauthorizedCaller();
    if (paused) {
        _pause();
    } else {
        _unpause();
    }
}
```

**Recommended Mitigation:**\
To ensure proper security in emergency scenarios, apply the `whenNotPaused` modifier to both `stake` and `withdraw` functions. This will prevent users—including potential attackers—from performing these actions when the contract is paused.

```diff
+ function stake(uint256 amount) external nonReentrant whenNotPaused updateReward(msg.sender) { 
    ...
+ }

+ function withdraw(uint256 amount) external nonReentrant whenNotPaused updateReward(msg.sender) { 
    ...
+ }
```

**Tools Used:**

* Manual Review

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | 1337web3, zegarcao, iamephraim, theirrationalone, mahivasisth, chista0x, 0xgee001, dobrevaleri, akioniace, i3arba, 0xekkoo, h2134, tigerfrake, pelz, 0xasad97, udogodwin2k22, godwinx, player, topstar, 0xswahili |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

