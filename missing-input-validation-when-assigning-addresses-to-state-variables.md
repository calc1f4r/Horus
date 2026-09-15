---
# Core Classification
protocol: Qoda DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51678
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/steadily-consulting-inc/qoda-dao
source_link: https://www.halborn.com/audits/steadily-consulting-inc/qoda-dao
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
  - Halborn
---

## Vulnerability Title

Missing input validation when assigning addresses to state variables

### Overview

See description below for full details.

### Original Finding Content

##### Description

In Solidity, it is essential to ensure the integrity and security of your smart contract by validating inputs before assigning them to state variables. One common oversight is the lack of input validation when assigning addresses to state variables, which can potentially lead to unintended consequences or security vulnerabilities.

By implementing proper input validation for addresses, you can prevent the assignment of invalid or malicious addresses to state variables, thereby reducing the risk of unexpected behavior in your smart contract.

  

**- src/QodaToken.sol [Line: 110]**

```
	        tokenAddress = tokenAddress_;
```

  

**- src/QodaToken.sol [Line: 143]**

```
	        revStream1Wallet = revStream1Wallet_; // set as revStream1 wallet
```

  

**- src/QodaToken.sol [Line: 144]**

```
	        revStream2Wallet = revStream2Wallet_; // set as revStream2 wallet
```

  

**- src/QodaToken.sol [Line: 241]**

```
	        revStream1Wallet = newRevStream1Wallet;
```

  

**- src/QodaToken.sol [Line: 246]**

```
	        revStream2Wallet = newWallet;
```

  

**- src/RewardDistributor.sol [Line: 80]**

```
	        token = token_;
```

  

**- src/RewardDistributor.sol [Line: 81]**

```
	        veToken = veToken_;
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

Implement proper input validation for addresses assigned to state variables by using `require` or `if` statements.

  

### Remediation Plan

**SOLVED:** The issue was addressed as recommended. The commit hash is `144cab46e7b09ac62604dd83996db4e6a2c5f083`.

##### Remediation Hash

<https://github.com/GoSteadily/qoda-dao/commit/144cab46e7b09ac62604dd83996db4e6a2c5f083>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Qoda DAO |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/steadily-consulting-inc/qoda-dao
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/steadily-consulting-inc/qoda-dao

### Keywords for Search

`vulnerability`

