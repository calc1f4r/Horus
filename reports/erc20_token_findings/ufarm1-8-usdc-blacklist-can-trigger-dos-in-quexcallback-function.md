---
# Core Classification
protocol: Ufarm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62444
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-06-10-Ufarm.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[UFARM1-8] USDC Blacklist Can Trigger DoS in quexCallback() Function

### Overview


The report describes a bug in the UFarmPool smart contract, which causes all deposit and withdrawal requests to fail if any individual request fails. This can be exploited by an attacker who controls a blacklisted address or implements a malicious hook, resulting in a denial-of-service attack. The bug can be fixed by using a try-catch block in the affected function. The issue has been resolved.

### Original Finding Content

**Severity:** Medium

**Path:** contracts/main/contracts/pool/UFarmPool.sol#L554 

**Description:** The `UFarmPool.quexCallback()` function is responsible for processing all pending deposit and withdrawal requests from users. It iterates through the `depositQueue[]` and `withdrawQueue[]` arrays, handling all requests within a single transaction. However, this design introduces a flaw: if any individual deposit or withdrawal reverts, the entire transaction fails, preventing all other requests from being processed.

This issue becomes particularly problematic in scenarios involving certain token behaviors. Consider a pool where the `valueToken` is USDC, and USDT is also accepted as a whitelisted token. In this setup, users are permitted to deposit and withdraw using either USDC or USDT.

USDC introduces a unique complication due to its blacklist mechanism. Addresses flagged by the USDC issuer cannot receive USDC transfers. An attacker who controls such a blacklisted address can exploit this behavior to disrupt the system:

1. The attacker deposits USDT into the pool to receive shares.

2. They later use those shares to initiate a withdrawal, which receives USDC as the `bearerToken`. 

3. Since the attacker is blacklisted by USDC, the transfer in `_processWithdrawal()` fails on the line 554:
```
IERC20(bearerToken).safeTransfer(investor, burnedAssetsCost);
```
This transfer reverts, and because all deposit and withdrawal logic is processed in a single transaction via `quexCallback()`, all other user requests in that batch are also reverted, even if they were valid.

The same type of denial-of-service vector exists when dealing with ERC777 tokens. An attacker can implement a malicious `tokensReceived` hook that intentionally reverts, thereby sabotaging transfers to their address and causing the entire `quexCallback()` execution to fail.

In summary, the core issue lies in the lack of isolation in request processing - a single failing operation can block the execution of all others, creating a vector for targeted denial-of-service attacks using blacklisted tokens or malicious ERC777 hooks.
```
function _processWithdrawal(
    address investor,
    uint256 sharesToBurn,
    uint256 _totalcost,
    bytes32 withdrawalRequestHash,
    address bearerToken
) private keepWithdrawalHash(withdrawalRequestHash) returns (uint256 burnedAssetsCost) {
    uint256 _totalSupply = totalSupply();
    burnedAssetsCost = (_totalcost * sharesToBurn) / _totalSupply;

    if (IERC20(bearerToken).balanceOf(address(this)) >= burnedAssetsCost) {
        _burn(investor, sharesToBurn);
        
        /// @audit the following line will revert if the bearerToken = USDC and investor is a blacklisted address 
        IERC20(bearerToken).safeTransfer(investor, burnedAssetsCost); 
        emit Withdraw(investor, bearerToken, burnedAssetsCost, withdrawalRequestHash);

        highWaterMark -= highWaterMark > burnedAssetsCost ? burnedAssetsCost : highWaterMark;

        emit WithdrawRequestExecuted(investor, sharesToBurn, withdrawalRequestHash);
    } else {
        burnedAssetsCost = 0;
    }

    return burnedAssetsCost;
}
```


**Remediation:**  Consider using a try-catch block when transferring tokens to the investor in the `_processWithdrawal` function. If an error occurs, do not burn shares and return 0 instead.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Ufarm |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-06-10-Ufarm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

