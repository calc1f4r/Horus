---
# Core Classification
protocol: Eco Inc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52992
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/cf70074c-8e59-45f6-9745-55523de0394e
source_link: https://cdn.cantina.xyz/reports/cantina_eco_february2025.pdf
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
finders_count: 2
finders:
  - 0xRajeev
  - phaze
---

## Vulnerability Title

Missing route and reward validations allows creating economically non-viable intents 

### Overview

See description below for full details.

### Original Finding Content

## IntentSource Contract Validation Summary

## Context
`IntentSource.sol#L120-L254`

## Summary
The `IntentSource` contract lacks validation for route and reward parameters when creating intents. This allows the creation of intents that provide no economic value to fillers or could result in tokens being unintentionally locked in the inbox contract.

## Description
Several important validations are missing when creating intents, such as:
1. No minimum reward requirement.
2. Route parameters can specify tokens without corresponding calls.

While fillers can validate intent viability off-chain, basic on-chain validations could prevent unintentional user errors like:
- Creating intents with no rewards that would never be filled.
- Transferring tokens to the inbox without corresponding calls to use them.
- Creating intents with mismatched token and call configurations.

## Impact Explanation
The impact is medium. While the protocol remains functional and sophisticated fillers will avoid non-viable intents, the lack of validation could lead to user confusion or locked tokens in edge cases.

## Likelihood Explanation
The likelihood is low as fillers will perform their own economic viability checks before executing intents, and most integrators will implement appropriate validation in their interfaces.

## Recommendation
Add basic sanity checks for intent creation:

```solidity
function validateIntent(Intent memory intent, bool fund) internal pure {
    // Validate chain configuration
    Route calldata route = intent.route;
    Reward calldata reward = intent.reward;
    
    // Basic route validation
    if (route.destination == 0) revert InvalidDestination();
    if (route.inbox == address(0)) revert InvalidInbox();
    if (route.source > type(uint32).max) revert InvalidSourceChain();
    if (fund && route.source != block.chainid) revert InvalidSourceChain();
    
    // Ensure there are calls to execute
    if (route.calls.length == 0) revert NoCalls();
    
    // Validate route tokens have corresponding calls
    if (route.tokens.length > route.calls.length) revert TooManyTokens();
    
    // Ensure there are rewards
    if (reward.tokens.length == 0 && reward.nativeValue == 0) {
        revert NoRewards();
    }
    
    // Validate reward amounts
    for (uint256 i = 0; i < reward.tokens.length; i++) {
        if (reward.tokens[i].amount == 0) revert InvalidRewardAmount();
    }
    
    // Validate timing
    if (reward.deadline <= block.timestamp) {
        revert InvalidDeadline();
    }
}
```

These validations provide basic safety guardrails while keeping in mind that fillers will make their own economic decisions about which intents to execute.

## Eco
Solvers will have to perform their own profitability checks regardless, so there's no reason to have a minimum reward. Solvers are also agnostic to what the user plans to do with the route tokens that are transferred to the inbox; even if they do nothing, the solver will factor into their profit check this net flow of tokens away from their wallet.

## Cantina Managed
The idea is to implement these low-cost sanity checks for the intent creator's sake.

## Eco
I think we are of the opinion that the solver is the best party to deal with maximum amounts of complexity. The more thin the on-chain protections, the less gas for the average user, and the more complex arbitrary stuff the system can do. So I'm okay leaving out the checks for now.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Eco Inc |
| Report Date | N/A |
| Finders | 0xRajeev, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_eco_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/cf70074c-8e59-45f6-9745-55523de0394e

### Keywords for Search

`vulnerability`

