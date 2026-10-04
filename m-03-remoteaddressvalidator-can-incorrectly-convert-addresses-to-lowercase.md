---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28763
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-axelar
source_link: https://code4rena.com/reports/2023-07-axelar
github_link: https://github.com/code-423n4/2023-07-axelar-findings/issues/323

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

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jeiwan
  - Shubham
  - Chom
---

## Vulnerability Title

[M-03] `RemoteAddressValidator` can incorrectly convert addresses to lowercase

### Overview


A bug has been identified in the `validateSender` and `addTrustedAddress` functions of the `RemoteAddressValidator` contract. These functions can incorrectly handle passed address arguments, resulting in false negatives. This is due to the `_lowerCase` function only converting hexadecimal letters (A-F) to lowercase when comparing addresses. This means that addresses from different EVM and non-EVM chains may not be properly compared, resulting in valid sender addresses being invalidated.

To mitigate this issue, the `_lowerCase` function should be updated to convert all alphabetical characters to lowercase. This has been debated amongst the team, with some considering it a QA or Low severity issue, as it only affects non-EVM chains. However, others have maintained a Medium severity rating, as it still prevents the use of non-EVM addresses.

### Original Finding Content


The `validateSender` and `addTrustedAddress` functions of `RemoteAddressValidator` can incorrectly handle the passed address arguments, which will result in false negatives. E.g. a valid sender address may be invalidated.

### Proof of Concept

The [RemoteAddressValidator.\_lowerCase](https://github.com/code-423n4/2023-07-axelar/blob/2f9b234bb8222d5fbe934beafede56bfb4522641/contracts/its/remote-address-validator/RemoteAddressValidator.sol#L54) function is used to convert an address to lowercase. Since the protocol is expected to support different EVM and non-EVM chains, account addresses may have different format, thus the necessity to convert them to strings and to convert the strings to lowercase when comparing them. However, the function only converts the hexadecimal letters, i.e. the characters in ranges A-F:

```solidity
if ((b >= 65) && (b <= 70)) bytes(s)[i] = bytes1(b + uint8(32));
```

Here, `65` corresponds to `A`, and `70` corresponds to `F`. But, since different EVM and non-EVM chains are supported, addresses can contain other characters. For example, [Cosmos uses bech32 addresses](https://docs.cosmos.network/main/spec/addresses/bech32) and [Evmos supports both hexadecimal and bech32 addresses](https://docs.evmos.org/protocol/concepts/accounts#address-formats-for-clients).

If not all alphabetical characters of an address are converted to lowercase, then the address comparison in the [validateSender](https://github.com/code-423n4/2023-07-axelar/blob/2f9b234bb8222d5fbe934beafede56bfb4522641/contracts/its/remote-address-validator/RemoteAddressValidator.sol#L69) can fail and result in a false revert.

### Recommended Mitigation Steps

In the `_lowerCase` function, consider converting all alphabetical characters to lowercase, e.g.:

```diff
diff --git a/contracts/its/remote-address-validator/RemoteAddressValidator.sol b/contracts/its/remote-address-validator/RemoteAddressValidator.sol
index bb101e5..e83431b 100644
--- a/contracts/its/remote-address-validator/RemoteAddressValidator.sol
+++ b/contracts/its/remote-address-validator/RemoteAddressValidator.sol
@@ -55,7 +55,7 @@ contract RemoteAddressValidator is IRemoteAddressValidator, Upgradable {
         uint256 length = bytes(s).length;
         for (uint256 i; i < length; i++) {
             uint8 b = uint8(bytes(s)[i]);
-            if ((b >= 65) && (b <= 70)) bytes(s)[i] = bytes1(b + uint8(32));
+            if ((b >= 65) && (b <= 90)) bytes(s)[i] = bytes1(b + uint8(32));
         }
         return s;
     }
```

**[deanamiel (Axelar) disagreed with severity and commented](https://github.com/code-423n4/2023-07-axelar-findings/issues/323#issuecomment-1695942282):**
> Corrected Severity: QA
>
> This was originally meant to cover the EVM addresses, but we implemented a fix to account for non-EVM addresses as well.
>
> Public PR link:
> https://github.com/axelarnetwork/interchain-token-service/pull/96

**[berndartmueller (judge) commented](https://github.com/code-423n4/2023-07-axelar-findings/issues/323#issuecomment-1702641616):**
 > I'm maintaining the medium severity for this issue as it prevents using any non-EVM addresses.

**[milapsheth (Axelar) commented](https://github.com/code-423n4/2023-07-axelar-findings/issues/323#issuecomment-1801759103):**
> We consider this finding QA or Low severity since the scope of the implementation is for EVM chains (even though Axelar's cross-chain messaging API is generic). Non EVM chains require further consideration that wasn't the focus for this version.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | Jeiwan, Shubham, Chom |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-axelar
- **GitHub**: https://github.com/code-423n4/2023-07-axelar-findings/issues/323
- **Contest**: https://code4rena.com/reports/2023-07-axelar

### Keywords for Search

`vulnerability`

