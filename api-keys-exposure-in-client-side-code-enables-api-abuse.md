---
# Core Classification
protocol: Gemini Smart Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62124
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-08-gemini-smartwallet-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-08-gemini-smartwallet-securityreview.pdf
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
finders_count: 2
finders:
  - Coriolan Pinhas Trail of Bits PUBLIC
  - Anish Naik
---

## Vulnerability Title

API keys exposure in client-side code enables API abuse

### Overview


This bug report discusses a security issue where the API keys are exposed in the client-side code, making it easy for malicious users to access and potentially abuse them. This can lead to unexpected costs for the service. The report recommends implementing security measures such as using different keys for debug and production builds, rotating keys regularly, and enabling rate-limiting or monitoring. In the long term, it suggests implementing an API gateway pattern to prevent abuse, but notes that this may slow down the connection.

### Original Finding Content

## Security Analysis Report

## Difficulty: Low

## Type: Data Validation

## Description
The API keys are exposed in client-side code, allowing malicious users to extract and abuse them. The API keys are used to create a Pimlico client for bundling transactions and to get on-chain information using Alchemy. However, the API key is currently being sent to the client browser, where it can be accessed through browser developer tools. This enables unauthorized users to make API calls using Gemini’s API key, potentially exhausting the API quota or incurring unexpected costs.

```javascript
// Create Pimlico configuration for bundling transactions
const pimlicoUrl =
`https://api.pimlico.io/v2/${chainId}/rpc?apikey=${process.env.NEXT_PUBLIC_PIMLICO_API_KEY}`;
const pimlicoTransport = http(pimlicoUrl);
```

![Figure 4.1](https://example.com/pimlico_url) The Pimlico URL containing the API key is shared with the client.  
![Figure 4.2](https://example.com/chrome_dev_tools) Chrome developer tool on the client side.

## Exploit Scenario
A malicious user connects to the Gemini wallet and inspects the network requests or browser developer tools. They extract the Pimlico API key from the client-side code. Using this key, they can make direct API calls to Pimlico’s services, potentially exhausting the API quota or incurring unexpected costs for the Gemini wallet service.

## Recommendations
### Short Term
The following security measures should be implemented:
- Keys should have minimal privileges, if possible.
- Use different keys for debug and production builds.
- Rotate keys regularly.
- Enable rate-limiting or monitoring.

### Long Term
Implement a proper API gateway pattern where all third-party API calls are proxied through the SDK server, with appropriate rate limiting and monitoring to prevent abuse. Note that this recommendation has the side effect of slowing down the connection.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Gemini Smart Wallet |
| Report Date | N/A |
| Finders | Coriolan Pinhas Trail of Bits PUBLIC, Anish Naik |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-08-gemini-smartwallet-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-08-gemini-smartwallet-securityreview.pdf

### Keywords for Search

`vulnerability`

