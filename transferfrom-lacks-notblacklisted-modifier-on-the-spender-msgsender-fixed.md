---
# Core Classification
protocol: USDKG
chain: everychain
category: uncategorized
vulnerability_type: blacklisted

# Attack Vector Details
attack_type: blacklisted
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45445
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/01/usdkg/
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
  - blacklisted

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

transferFrom() Lacks notBlackListed Modifier on the Spender msg.sender ✓ Fixed

### Overview


This report talks about a bug in the USDKG token. The token has a feature that allows users to be blacklisted from using it. However, the bug is related to the fact that the `notBlackListed` modifier is only applied to the `msg.sender` in the `transfer()` and `transferFrom()` functions. This means that a malicious or compromised spender can still use the token to exploit vulnerable smart contracts. The recommendation is to also apply the modifier to the spender in the `transferFrom()` function to prevent this from happening. This will also allow the USDKG team to blacklist known phishing or sanctioned contracts. 

### Original Finding Content

#### Resolution

Fixed in [commit 0d22c5326e21541df0c718db98004d5a475aa2ea](https://github.com/USDkg/USDkg/commit/0d22c5326e21541df0c718db98004d5a475aa2ea) by putting the `notBlackListed` modifier on `msg.sender` in the `transferFrom()` function as well.


#### Description

The USDKG token has functionality to blacklist users from using it. For example, a `notBlackListed` modifier exists to verify that a user does not belong to a blacklisted list:

**contracts/USDKG.sol:L86-L92**

```
/**
 * @dev Modifier to make a function callable only when sender is not blacklisted.
 */
modifier notBlackListed(address sender) {
    require(!isBlackListed[sender], "user blacklisted");
    _;
}

```

This is present on functions `transfer()` and `transferFrom()` where it is checking the `msg.sender` and `_from` addresses respectively:

**contracts/USDKG.sol:L103**

```
function transfer(address _to, uint256 _value) public whenNotPaused notBlackListed(msg.sender) returns (bool) {

```

**contracts/USDKG.sol:L122**

```
function transferFrom(address _from, address _to, uint256 _value) public whenNotPaused notBlackListed(_from) returns (bool) {

```

However, in the case of `transferFrom()` it would also be valuable to check blacklisting against the spender, i.e. `msg.sender` as well. That is because a malicious or a compromised spender who received approval from a victim may be identified as an attacker prior to them executing, or perhaps continuing the execution of, exploits. For example, one such compromised spender may be a vulnerable smart contract that has the USDKG token as part of its system, like collateral or a lending asset. An attacker may execute an exploit on such a contract that has approval on it from its victims. The exploit could move the tokens from the victims (the `_from` address) to the vulnerable smart contract (the `msg.sender`) via `transferFrom()`, perform the exploit, and then move the tokens to the attacker via `transfer()`. Blacklisting the attacker themselves wouldn’t be useful as they can simply spin up another account and activate the exploit from there. However, blacklisting the vulnerable smart contract itself would prevent the `transferFrom()` operation from the victim to the contract, thereby stopping the exploit at least as far as the USDKG token is concerned. Moreover, this could be used by the compliance team of the USDKG token to blacklist known phishing contracts or otherwise potentially sanctioned contracts as deemed appropriate by the USDKG team.

Of course, this is contingent on the USDKG compliance team knowing the vulnerable or inappropriate contracts in the first place prior to the malicious activity taking place. This is possible today with monitoring solutions as well.

#### Recommendation

Apply the `notBlacklisted` modifier to the spender in the `transferFrom()` function, i.e. `msg.sender` as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | USDKG |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/01/usdkg/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Blacklisted`

