---
# Core Classification
protocol: Virtuals Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61847
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-04-virtuals-protocol
source_link: https://code4rena.com/reports/2025-04-virtuals-protocol
github_link: https://code4rena.com/audits/2025-04-virtuals-protocol/submissions/F-129

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
finders_count: 3
finders:
  - nnamdi0482
  - yaractf
  - Ishenxx
---

## Vulnerability Title

[M-20] Delegation not revoked on withdrawal allows reward and voting power inflation post-maturity

### Overview


Summary:

The bug report discusses an issue in the code of the 2025-04-virtuals-protocol, where the `withdraw()` function does not clean up delegations when a user fully withdraws their stake. This allows malicious users to exploit the system by staking and immediately withdrawing multiple times, leaving delegation entries intact while reducing their staked balance to zero. This results in unfair distribution of rewards and governance power. The recommended mitigation step is to update the `withdraw()` function to automatically clear a user's delegation when their token balance drops to zero.

### Original Finding Content



<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/28e93273daec5a9c73c438e216dde04c084be452/contracts/virtualPersona/AgentVeToken.sol# L102>

<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/28e93273daec5a9c73c438e216dde04c084be452/contracts/AgentRewardV3.sol# L264>

### Finding description and impact

Stakers delegate their voting power using the `stake()` function, which internally calls `_delegate(receiver, delegatee)` and records the delegatee via checkpointing at the current `clock()` (block number). Upon maturity (`matureAt`), the `withdraw()` function allows full withdrawal of tokens, including by the stakers.

<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/28e93273daec5a9c73c438e216dde04c084be452/contracts/virtualPersona/AgentVeToken.sol# L80>
```

    function stake(uint256 amount, address receiver, address delegatee) public {
        require(canStake || totalSupply() == 0, "Staking is disabled for private agent"); // Either public or first staker

        address sender = _msgSender();
        require(amount > 0, "Cannot stake 0");
        require(IERC20(assetToken).balanceOf(sender) >= amount, "Insufficient asset token balance");
        require(IERC20(assetToken).allowance(sender, address(this)) >= amount, "Insufficient asset token allowance");

        IAgentNft registry = IAgentNft(agentNft);
        uint256 virtualId = registry.stakingTokenToVirtualId(address(this));

        require(!registry.isBlacklisted(virtualId), "Agent Blacklisted");

        if (totalSupply() == 0) {
            initialLock = amount;
        }

        registry.addValidator(virtualId, delegatee);

        IERC20(assetToken).safeTransferFrom(sender, address(this), amount);
        _mint(receiver, amount);
@>      _delegate(receiver, delegatee);
        _balanceCheckpoints[receiver].push(clock(), SafeCast.toUint208(balanceOf(receiver)));
    }
```

However, the `withdraw()` function does not call `_delegate(sender, address(0))` to clean up delegations when a user fully withdraws their stake. This leaves the previous delegation entry active, even though the staker now has zero voting power.

<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/28e93273daec5a9c73c438e216dde04c084be452/contracts/virtualPersona/AgentVeToken.sol# L95>
```

    function withdraw(uint256 amount) public noReentrant {
        address sender = _msgSender();
        require(balanceOf(sender) >= amount, "Insufficient balance");

        if ((sender == founder) && ((balanceOf(sender) - amount) < initialLock)) {
            require(block.timestamp >= matureAt, "Not mature yet");
        }
@>
        _burn(sender, amount);
        _balanceCheckpoints[sender].push(clock(), SafeCast.toUint208(balanceOf(sender)));

        IERC20(assetToken).safeTransfer(sender, amount);
    }
```

Once maturity is reached, a malicious user can exploit this flaw by:

* The user stakes tokens and delegates.
* Then immediately withdraws them when maturity.
* Repeats the cycle multiple times, possibly in the same block.

Each cycle leaves delegation entries intact while reducing the actual staked balance to zero.

The system uses `getPastDelegates()` in reward logic to compute historical rewards based on:

<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/28e93273daec5a9c73c438e216dde04c084be452/contracts/AgentRewardV3.sol# L204>
```

    function getClaimableStakerRewards(
        address account,
        uint256 virtualId
    ) public view returns (uint256 totalClaimable, uint256 numRewards) {
        Claim memory claim = _stakerClaims[account][virtualId];
        numRewards = Math.min(LOOP_LIMIT + claim.rewardCount, getAgentRewardCount(virtualId));
        IAgentVeToken veToken = IAgentVeToken(IAgentNft(agentNft).virtualLP(virtualId).veToken);
        IAgentDAO dao = IAgentDAO(IAgentNft(agentNft).virtualInfo(virtualId).dao);
        for (uint i = claim.rewardCount; i < numRewards; i++) {
            AgentReward memory agentReward = getAgentReward(virtualId, i);
            Reward memory reward = getReward(agentReward.rewardIndex);
@>          address delegatee = veToken.getPastDelegates(account, reward.blockNumber);
            uint256 uptime = dao.getPastScore(delegatee, reward.blockNumber);
            uint256 stakedAmount = veToken.getPastBalanceOf(account, reward.blockNumber);
            uint256 stakerReward = (agentReward.stakerAmount * stakedAmount) / agentReward.totalStaked;
            stakerReward = (stakerReward * uptime) / agentReward.totalProposals;

            totalClaimable += stakerReward;
        }
    }
```

As a result, repeated delegation records combined with zeroed balances allow the delegatee to appear historically more active, and to receive inflated uptime-based rewards; even though the stake was not present at the time.

### Impact

* Reward distribution becomes exploitable by staking and undelegating rapidly after maturity.
* Delegatees receive excessive rewards due to inflated uptime scores based on `getPastDelegates()`.
* Governance power and monetary reward flows become decoupled from actual stake and participation.
* Fairness of the protocol is compromised; malicious users can game the system at the expense of honest stakers and voters.

### Recommended mitigation steps

Update the `withdraw()` function to automatically clear a user’s delegation when their token balance drops to zero. This prevents the retention of voting power or reward eligibility after the staker has exited.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Virtuals Protocol |
| Report Date | N/A |
| Finders | nnamdi0482, yaractf, Ishenxx |

### Source Links

- **Source**: https://code4rena.com/reports/2025-04-virtuals-protocol
- **GitHub**: https://code4rena.com/audits/2025-04-virtuals-protocol/submissions/F-129
- **Contest**: https://code4rena.com/reports/2025-04-virtuals-protocol

### Keywords for Search

`vulnerability`

