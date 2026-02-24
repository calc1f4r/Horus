---
# Core Classification
protocol: Swell Barracuda
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31978
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - Carlitox477
---

## Vulnerability Title

`SwellLib.BOT` can delete active validators when bot methods are paused

### Overview


Report Summary:

The report describes a bug in the SwellLib.BOT function that allows it to still call a specific function even when bot methods are paused. The report suggests adding a check to prevent this from happening or adding a comment to the function stating that it should be callable by SwellLib.BOT even when bot methods are paused. The bug has been fixed in a recent commit and has been verified by Cyfrin.

### Original Finding Content

**Description:** Almost all of the functions callable by `SwellLib.BOT` contain the following check to prevent bot functions from working when bot methods are paused:

```solidity
if (AccessControlManager.botMethodsPaused()) {
  revert SwellLib.BotMethodsPaused();
}
```

The one exception is [`NodeOperatorRegistry::deleteActiveValidators`](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/NodeOperatorRegistry.sol#L417-L423) which is callable by `SwellLib.BOT` even when bot methods are paused. Consider:
* adding a similar check to this function such that `SwellLib.BOT` is not able to call it when bot methods are paused
* alternatively add an explicit comment to this function stating that it should be callable by `SwellLib.BOT` even when bot methods are paused.

One possible implementation for the first solution:
```solidity
bool isBot = AccessControlManager.hasRole(SwellLib.BOT, msg.sender);

// prevent bot from calling this function when bot methods are paused
if(isBot && AccessControlManager.botMethodsPaused()) {
  revert SwellLib.BotMethodsPaused();
}

// function only callable by admin & bot
if (!AccessControlManager.hasRole(SwellLib.PLATFORM_ADMIN, msg.sender) && !isBot) {
  revert OnlyPlatformAdminOrBotCanDeleteActiveValidators();
}
```

**Swell:** Fixed in commit [1a105b7](https://github.com/SwellNetwork/v3-contracts-lst/commit/1a105b76899780e30b1fb88abdede11c0c0586ba).

**Cyfrin:**
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Swell Barracuda |
| Report Date | N/A |
| Finders | Dacian, Carlitox477 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

