---
# Core Classification
protocol: Alligator
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18719
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-03-21-Alligator.md
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
finders_count: 1
finders:
  - Zach Obront
---

## Vulnerability Title

[H-02] Alligator gives gas refunds but does not receive gas refunds

### Overview


The `AlligatorV2.sol` contract has a bug where it cannot receive a refund from the underlying DAO. This is because the contract uses the `castVotesWithReasonBatched()` function to call `Nouns.castVoteWithReason()` instead of the `castRefundableVote()` entry point. As a result, Alligator can only refund users out of its own balance, but will not be refunded by the DAO. To fix this, the `castRefundableVotesWithReasonBatched()` function should be refactored to use the `castRefundableVote()` entry point. This will allow Alligator to receive a refund from the DAO before passing along the refund to the user. The bug was fixed in PR #14. An additional safety measure was added to the proxy to account for other protocols that send gas refunds to `msg.sender` by adding a `receive()` function. This forwards the refund to the caller if funds are received from the `governor`.

### Original Finding Content

The `AlligatorV2.sol` contract has a function `castRefundableVotesWithReasonBatched()` which tracks the gas used and provides a refund to the user. This mirrors the functionality used by `NounsLogicV2` to provide voting refunds.

However, while Alligator can provide refunds, there's no way for it to be refunded by the underlying DAO. This is because Nouns (for example) requires a call to `castRefundableVote()` in order to provide a refund, but Alligator simply calls `castVotesWithReasonBatched()` which calls `Nouns.castVoteWithReason()`:

```solidity
function castRefundableVotesWithReasonBatched(
Rules[] calldata proxyRules,
address[][] calldata authorities,
uint256 proposalId,
uint8 support,
string calldata reason
) external whenNotPaused {
uint256 startGas = gasleft();
castVotesWithReasonBatched(proxyRules, authorities, proposalId, support, reason);
_refundGas(startGas);
}
```

```solidity
function castVotesWithReasonBatched(
Rules[] calldata proxyRules,
address[][] calldata authorities,
uint256 proposalId,
uint8 support,
string calldata reason
) public whenNotPaused {
address[] memory proxies = new address[](authorities.length);
address[] memory authority;
Rules memory rules;

for (uint256 i; i < authorities.length; ) {
authority = authorities[i];
rules = proxyRules[i];
validate(rules, msg.sender, authority, PERMISSION_VOTE, proposalId, support);
proxies[i] = proxyAddress(authority[0], rules);
INounsDAOV2(proxies[i]).castVoteWithReason(proposalId, support, reason);

unchecked {
++i;
}
}

emit VotesCast(proxies, msg.sender, authorities, proposalId, support);
}
```

The result is that Alligator will only refund users out of its own balance, but will not be refunded by the DAO.

**Recommendation**

Refactor `castRefundableVotesWithReasonBatched()` to use the `castRefundableVote()` entry point to the `governor` contract, so that it receives a refund before passing along the refund to the user.

**Review**

Fixed in PR #14.

Nouns gas refunds are sent to `tx.origin` and not `msg.sender`, which allows Alligator to remove all refund functionality and simply call the `castRefundableVoteWithReason()` function to have the refund sent to the caller.

An additional safety measure was added to the proxy to account for other protocols that send gas refunds to `msg.sender`. To account for this case, a `receive()` function was added to the proxy so that, if funds are received from the `governor`, they are forwarded along to the caller.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Alligator |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-03-21-Alligator.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

