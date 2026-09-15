---
# Core Classification
protocol: USDV_2025-03-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57860
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/USDV-security-review_2025-03-06.md
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

[L-07] Cancellations can be blocked for some providers

### Overview

See description below for full details.

### Original Finding Content

```solidity
    function cancelMint(uint256 _id) external mintRequestExist(_id) {
// ..snip
        request.state = State.CANCELLED;
        IERC20 depositedToken = IERC20(request.token);
|>        depositedToken.safeTransfer(request.provider, request.amount);
        emit MintRequestCancelled(_id);
    }
        function cancelBurn(uint256 _id) external burnRequestExist(_id) {
// ..snip
        request.state = State.CANCELLED;
        IERC20 issueToken = IERC20(ISSUE_TOKEN_ADDRESS);
|>        issueToken.safeTransfer(request.provider, request.amount);

        emit BurnRequestCancelled(_id);
    }
```

As seen, the cancellation functions `ExternalRequestsManager::cancelMint()` and `cancelBurn()` directly transfer funds to `msg.sender` using `safeTransfer`:

Now, currently, usd-fun only support USDC/USDT (which are both blacklistable stablecoins), knowing that transfers to blacklisted addresses will revert. This creates an irrecoverable state where:

1. Blacklisted provider, who had initially placed a mint/burn request, attempts to call `cancelMint()/cancelBurn()`
2. `safeTransfer` fails due to blacklist check in token contract
3. Transaction reverts, keeping request in `CREATED` state
4. Protocol cannot process cancellation the cancellation for users

Allow the providers to pass in a recipient, this can be done by attaching a new parameter to the cancellation functions:

```solidity
function cancelMint(uint256 _id, address _recipient) external {
    // ...
    depositedToken.safeTransfer(_recipient, request.amount);
}

function cancelBurn(uint256 _id, address _recipient) external {
    // ...
    issueToken.safeTransfer(_recipient, request.amount);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | USDV_2025-03-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/USDV-security-review_2025-03-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

