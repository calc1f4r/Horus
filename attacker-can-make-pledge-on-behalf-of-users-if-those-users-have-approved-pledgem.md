---
# Core Classification
protocol: Remora Pledge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61175
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - Stalin
---

## Vulnerability Title

Attacker can make pledge on behalf of users if those users have approved `PledgeManager` to spend their tokens

### Overview


The PledgeManager is a feature that allows users to make pledges with their tokens. In order to make pledges, users must first approve the PledgeManager to spend their tokens. This can be done either by using a special function called `IERC20Permit::permit` or by manually calling `IERC20::approve`. However, a bug has been discovered where if a user uses the manual method and leaves an open token approval, an attacker can make pledges on behalf of the user without their permission. This can result in the user's tokens being spent without their knowledge. To fix this issue, it is recommended to add a check in the `PledgeManager::pledge` function to ensure that the caller is the same as the signer. This bug has been fixed by the Remora team in their latest commit and has been verified by the Cyfrin team.

### Original Finding Content

**Description:** `PledgeManager` requires users to approve it to spend their tokens in order to make pledges. Users can do this by either:
1) using `IERC20Permit::permit` which enforces a nonce for the signer, deadline and domain separator
2) manually by calling `IERC20::approve`

If users use the manual method 2) and leave an open token approval, an attacker can call `PledgeManager::pledge` to make a pledge on their behalf since this function never enforces that `msg.sender == data.signer`.

**Impact:** Attacker can make pledges on behalf of innocent users which spends those users' tokens. It is common for users to have max approvals for protocols they use often, even though they don't intend to spend all their tokens with that protocol.

**Recommended Mitigation:** In `PledgeManager::pledge`, when not using `IERC20Permit::permit` enforce that `msg.sender == data.signer`:
```diff
        if (data.usePermit) {
            IERC20Permit(stablecoin).permit(
                signer,
                address(this),
                finalStablecoinAmount,
                block.timestamp + 300,
                data.permitV,
                data.permitR,
                data.permitS
            );
        }
+       else if(msg.sender != signer) revert MsgSenderNotSigner();
```

Alternatively always use `msg.sender` similar to how `PledgeManager::refundTokens` works.

**Remora:** Fixed in commit [e3bda7c](https://github.com/remora-projects/remora-smart-contracts/commit/e3bda7c78321febb0e2f37b29912ba24c9e04343) by always using `msg.sender` and also removed the permit method.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Remora Pledge |
| Report Date | N/A |
| Finders | Dacian, Stalin |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

