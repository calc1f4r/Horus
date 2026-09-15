---
# Core Classification
protocol: Coinflip_2025-02-05
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55501
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-05.md
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

[L-10] The entropyCallback may fail in blacklist transfer edge case

### Overview

See description below for full details.

### Original Finding Content

Pyth entropy [documentation](https://docs.pyth.network/entropy/generate-random-numbers/evm) states:

> The entropyCallback function should never return an error. If it returns an error, the keeper will not be able to invoke the callback.

There can be an unfortunate case where the `entropyCallback` function reverts because the user is blacklisted from receiving his rewards.

When `entropyCallback()` is called in the RandomnessProvider contract, it calls `IGame(info.gameContract).completeGame(info.gameId, random);` which transfers tokens to the player if the player wins:

```
Flip.sol

            if (managerFee > 0) {
                game.token.safeTransfer(manager, managerFee);
            }
            if (stakingFee > 0) {
                game.token.safeTransfer(address(stakingContract), stakingFee);
            }

>           stakingContract.transferPayout(game.token, game.player, netPayout);

Staking.sol

function transferPayout(address token, address recipient, uint256 amount) external nonReentrant returns (bool) {
        require(authorizedGames[msg.sender] || msg.sender == owner(), "Caller not authorized");
        require(acceptedTokens[token], "Token not supported");
        require(amount > 0, "Cannot transfer 0");
>       require(IERC20(token).transfer(recipient, amount), "Payout transfer failed");
        return true;
    }
```

In an edge case, if the user gets blacklisted by the token in the duration of waiting for the callback, the callback will fail since the transfer will fail, and there will be no retry.

For example, a player calls `flip()` with USDC as his token and gets blacklisted immediately after. During the `entropyCallback()`, funds cannot be transferred to the player and `entropyCallback()` will revert.

Recommend having a retry mechanism to ensure maximum fairness, since in this case the player had won. Although the player can call `cancelGame()` to retrieve his tokens after the blacklist has been lifted, it would not be fair to the player.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Coinflip_2025-02-05 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-05.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

