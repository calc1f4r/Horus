---
# Core Classification
protocol: Bucket Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63379
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
source_link: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
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
finders_count: 3
finders:
  - Hamed Mohammadi
  - Adrian Koegl
  - Rabib Islam
---

## Vulnerability Title

Security Level Constraint Can Be Circumvented

### Overview


The bug report states that there is an issue with the `update_position()` function in the `bucket_cdp/sources/vault.move` file. This function is supposed to restrict certain actions based on the user's operation and the vault's security level. However, it is possible for a user to bypass this security level by including a deposit amount with their call of `update_position()`. The recommendation is to change the code to use independent `if` statements instead of an `if-else` condition. This will ensure that the security level access control is not circumvented. The bug has been fixed by the client and the code changes can be found in `49f5916fb915743b929b5c5d28d2647a0e24d14e`.

### Original Finding Content

**Update**
Fixed by the client as per recommendation. Addressed in: `49f5916fb915743b929b5c5d28d2647a0e24d14e`.

**File(s) affected:**`bucket_cdp/sources/vault.move`

**Description:** The `update_position()` function throws an error depending on the user's operation and the vault's security level. It is _intended_ that if the user wants to deposit collateral, the user is allowed if the security level is 0 or 2; if the user wants to withdraw collateral, repay a debt, or borrow, the security level must be 0. This behavior is based on the following code block:

```
// check security by actions
    if(request.deposit_amount() > 0) {
        // deposit actions will only be blocked when security level equals to 1
        vault.check_secutiry_level(1);
    }else{
        // borrow; repay; witdraw;
        vault.check_secutiry_level(2);
    };
```

However, it is possible to withdraw collateral, repay a debt, or borrow even if the security level is 2: the user simply needs to include a deposit amount with their call of `update_position()`. This way, the security level access control is circumvented.

**Recommendation:** Instead of an `if - else` condition, implement independent `if` statements that depend on inputs to `update_position()`, since several operations are supported at once in `update_position()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Bucket Protocol V2 |
| Report Date | N/A |
| Finders | Hamed Mohammadi, Adrian Koegl, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/bucket-protocol-v-2/abd312d6-1a5e-45c5-963b-a6856daf6621/index.html

### Keywords for Search

`vulnerability`

