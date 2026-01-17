---
# Core Classification
protocol: Optimistic Finality
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46876
audit_firm: OtterSec
contest_link: https://www.synonym.finance/
source_link: https://www.synonym.finance/
github_link: https://github.com/SynonymFinance/smart-contracts

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
  - Robert Chen
  - Woosun Song
---

## Vulnerability Title

Unaccounted Amount Trimming

### Overview


The report describes a bug in the Spoke.instantActions code that causes assets to become stuck in the WormholeTunnel and renders the spoke in a pending state. This is due to the code not accounting for the trimming behavior of the Wormhole token bridge, which normalizes token amounts to 8 decimals. As a result, any extra decimal places are removed, but the code fails to account for this and the dust remains in the WormholeTunnel. This accumulation of dust is undesirable and can cause cross-chain transaction failures. The bug has been fixed in the latest patch.

### Original Finding Content

## Analysis of Spoke.instantActions and Wormhole Token Bridge

Spoke.instantActions does not account for Wormhole token bridge’s token amount trimming behavior. This oversight results in stuck assets in the WormholeTunnel and renders the spoke stuck in a pending state.

Wormhole normalizes token amounts to 8 decimals to standardize cross-chain transfers. This results in tokens with more than eight decimals having their extra decimal places truncated. For example, a token transfer with 18 decimals and an amount of `1e10 + 1` will be normalized to `1e10`, and the extra `1 wei` will be removed as dust. However, Spoke.instantActions and WormholeTunnel fail to account for this behavior of dust trimming. As a result, any trimmed dust remains in WormholeTunnel. By design, all tokens passing through WormholeTunnel are assumed to be transient. Therefore, the accumulation of dust in this contract is an undesirable outcome.

## Code Reference
> _wormhole/ethereum/contracts/bridge/Bridge.sol solidity
> 
> ```solidity
> function _transferTokens(address token, uint256 amount, uint256 arbiterFee) internal returns
> → (BridgeStructs.TransferResult memory transferResult) {
> /* ... */
> // query tokens decimals
> (,bytes memory queriedDecimals) = token.staticcall(abi.encodeWithSignature("decimals()"));
> uint8 decimals = abi.decode(queriedDecimals, (uint8));
> // don't deposit dust that cannot be bridged due to the decimal shift
> amount = deNormalizeAmount(normalizeAmount(amount, decimals), decimals);
> if (tokenChain == chainId()) {
> /* ... */
> } else {
> SafeERC20.safeTransferFrom(IERC20(token), msg.sender, address(this), amount);
> TokenImplementation(token).burn(address(this), amount);
> }
> /* ... */
> }
> ```

Furthermore, it results in a late stage revert that prevents the hub from finalizing the spoke’s credit. When depositing assets, the spoke sends two cross-chain messages, each with INSTANT and FINAL confirmation levels, where the latter is responsible for forwarding tokens and releasing the credit granted in the spoke. Due to dust trimming in WormholeTunnel, the FINAL confirmation fails, rendering the granted credit unreleased. This locks the spoke in a pending state and disrupts the entire cross-chain operation.

While this vulnerability does not allow for the theft of funds, it is still classified as high severity as it results in cross-chain transaction failures upon spoke overflow events.

## Remediation
Ensure to trim dust on the forwarded amount.

## Patch
Fixed in commit `6698cfa`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Optimistic Finality |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song |

### Source Links

- **Source**: https://www.synonym.finance/
- **GitHub**: https://github.com/SynonymFinance/smart-contracts
- **Contest**: https://www.synonym.finance/

### Keywords for Search

`vulnerability`

