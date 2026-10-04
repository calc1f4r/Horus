---
# Core Classification
protocol: ENS
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5556
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-ens-contest
source_link: https://code4rena.com/reports/2022-07-ens
github_link: https://github.com/code-423n4/2022-07-ens-findings/issues/179

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
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - zzzitron
---

## Vulnerability Title

[M-12] `ERC1155Fuse`: `_transfer` does not revert when sent to the old owner

### Overview


A bug has been identified in the ERC1155Fuse.sol contract, which is used to implement the ERC1155 standard. This bug affects the `safeTransferFrom` function, which is used to transfer tokens from one address to another. The bug causes the function to not comply with the ERC1155 standard, as it does not revert when the balance of the sender is lower than the amount sent. This can cause problems for other contracts that rely on the token being transferred if the `safeTransferFrom` does not revert. To mitigate this issue, it is recommended to revert even if the `to` address already owns the token.

### Original Finding Content


The `safeTransferFrom` does not comply with the ERC1155 standard when the token is sent to the old owner.

### Proof of Concept

According to the EIP-1155 standard for the `safeTransferFrom`:

> MUST revert if balance of holder for token `_id` is lower than the `_value` sent.

Let's say `alice` does not hold any token of `tokenId`, and `bob` holds one token of `tokenId`. Then alice tries to send one token of `tokenId` to bob with `safeTranferFrom(alice, bob, tokenId, 1, "")`.  In this case, even though alice's balance (= 0) is lower than the amount (= 1) sent, the `safeTransferFrom` will not revert. Thus, violating the EIP-1155 standard.<br>
It can cause problems for other contracts using this token, since they assume the token was transferred if the `safeTransferFrom` does not revert. However, in the example above, no token was actually transferred.

```solidity
// https://github.com/code-423n4/2022-07-ens/blob/ff6e59b9415d0ead7daf31c2ed06e86d9061ae22/contracts/wrapper/ERC1155Fuse.sol#L274-L284
// wrapper/ERC1155Fuse.sol::_transfer
// ERC1155Fuse::safeTransferFrom uses _transfer

274     function _transfer(
275         address from,
276         address to,
277         uint256 id,
278         uint256 amount,
279         bytes memory data
280     ) internal {
281         (address oldOwner, uint32 fuses, uint64 expiry) = getData(id);
282         if (oldOwner == to) {
283             return;
284         }
```

### Recommended Mitigation Steps

Revert even if the `to` address already owns the token.

**[jefflau (ENS) confirmed and commented](https://github.com/code-423n4/2022-07-ens-findings/issues/179#issuecomment-1196491844):**
 > Recommend severity QA.

**[LSDan (judge) commented](https://github.com/code-423n4/2022-07-ens-findings/issues/179#issuecomment-1205864807):**
 > I'm going to leave this as Medium. This issue could definitely impact other protocols and potentially cause a loss of funds given external factors.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ENS |
| Report Date | N/A |
| Finders | zzzitron |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-ens
- **GitHub**: https://github.com/code-423n4/2022-07-ens-findings/issues/179
- **Contest**: https://code4rena.com/contests/2022-07-ens-contest

### Keywords for Search

`vulnerability`

