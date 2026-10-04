---
# Core Classification
protocol: Lombard Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46317
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/3a1c4f65-6ef7-4d26-97f4-480f8093801d
source_link: https://cdn.cantina.xyz/reports/cantina_lombard_december2024.pdf
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
finders_count: 3
finders:
  - Haxatron
  - dontonka
  - Bernd
---

## Vulnerability Title

Possible to approve babylon request with invalid ﬁnality provider public key 

### Overview

See description below for full details.

### Original Finding Content

## Finality Provider Issue in Babylon Requests

## Context
* File: `finality_providers.go#L12-L24`
* Description: Possible to approve Babylon request with invalid finality provider public key.

Whenever a Babylon request is processed, it will go through a series of validations, one of which is `validateFinalityProviderPks` (`common.go#L252-L271`). The validation of Babylon's request happens in the following functions:

- `babylon_deposit.go#L62`: `validateBabylonDepositRequest (staking)`
- `babylon_early_unbond.go#L50`: `validateBabylonEarlyUnbondRequest (unbond)`
- `babylon_timelock_withdraw.go#L54`: `validateBabylonTimelockWithdrawRequest (withdraw)`

### Code Example
```go
func (c *cubistCustodianManager) validateFinalityProviderPks(finalityProviderPk string) error {
    var isWhitelistedFpPk bool
    whitelistedFpPks, err := c.babylonService.GetFinalityProviderPks()
    if err != nil {
        return errors.Wrap(err, "error getting Babylon finality providers")
    }
    for _, pk := range whitelistedFpPks {
        if strings.EqualFold(pk, finalityProviderPk) {
            isWhitelistedFpPk = true
        }
    }
    if !isWhitelistedFpPk {
        return errors.Errorf(" ` finality_provider_pk ` (%s) is not whitelisted", finalityProviderPk)
    }
    return nil
}
```

1. We can observe that it will reach the Babylon staking API to confirm that the finality provider supported by the approver is actually valid, returning an array of supported keys.
2. It will then try to confirm (`isWhitelistedFpPk = true`) if the request's finality provider key is present in that returned array.

### Problem Origin
The problematic situation originates from the Babylon internal service `GetFinalityProviderPks` (`service.go#L61-L73`), which lacks proper validation for a specific case. Whenever a key from the config doesn't exist (i.e., not found by the Babylon Staking API), it will still be counted as a valid key, as this will not return an error. This unexpected behavior will allow the approver service to accept requests with potentially invalid finality provider keys.

### Code Example
```go
func (s *service) GetFinalityProviderPks() ([]string, error) {
    res := make([]string, 0)
    for _, fpPk := range s.config.FinalityProviderPks {
        _, err := s.client.FinalityProviders(fpPk)
        if err != nil {
            return nil, err
        }
        res = append(res, fpPk)
    }
    return res, nil
}
```

## Proof of Concept
Create a file `internal/babylon/client/finality_providers_test.go` and paste the following content. All tests will pass, except the test case for a well-formed key that is not found, confirming this report since it is not returning an error as it should.

### Test Code
```go
package client

import (
    "io"
    "net/http"
    "net/http/httptest"
    "net/url"
    "testing"
    "time"

    v1 "github.com/lombard-finance/approver/internal/babylon/api/v1"
    "github.com/sirupsen/logrus"
    "github.com/stretchr/testify/assert"
)

func TestFinalityProviders(t *testing.T) {
    // Test cases
    tests := []struct {
        name         string
        fpPk        string
        serverStatus int
        serverResp   string
        expectedResp *v1.FinalityProvidersResponse
        expectError  bool
    }{
        {
            name:         "successful_response - single",
            fpPk:        "02c7e138bff86a4cc33e6871ce9c907482795653e58a30305400c0da3226a6d611",
            serverStatus: http.StatusOK,
            serverResp: ` {
                "data": [{
                "description": {
                    "moniker": "test-fp",
                    "identity": "test-identity",
                    "website": "test.com",
                    "security_contact": "security@test.com",
                    "details": "test details"
                },
                "commission": "0.1",
                "btc_pk": "02c7e138bff86a4cc33e6871ce9c907482795653e58a30305400c0da3226a6d611",
                "active_tvl": 1000000,
                "total_tvl": 2000000,
                "active_delegations": 10,
                "total_delegations": 20
                }]
            }`,
            expectedResp: &v1.FinalityProvidersResponse{
                Data: []v1.FinalityProvider{
                    {
                        Description: v1.FinalityProviderDescription{
                            Moniker:       "test-fp",
                            Identity:      "test-identity",
                            Website:       "test.com",
                            SecurityContact: "security@test.com",
                            Details:       "test details",
                        },
                        Commission:      "0.1",
                        BtcPk:          "02c7e138bff86a4cc33e6871ce9c907482795653e58a30305400c0da3226a6d611\n",
                        ActiveTVL:      1000000,
                        TotalTVL:       2000000,
                        ActiveDelegations: 10,
                        TotalDelegations: 20,
                    },
                },
            },
            expectError: false,
        },
        // Additional test cases...
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Create test server
            server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
                // Verify request method
                assert.Equal(t, http.MethodGet, r.Method)
                // Verify path and query parameters
                assert.Contains(t, r.URL.Path, "/v1/finality-providers")
                assert.Equal(t, tt.fpPk, r.URL.Query().Get("fp_btc_pk"))
                // Set response
                w.WriteHeader(tt.serverStatus)
                w.Header().Set("Content-Type", "application/json")
                _, err := io.WriteString(w, tt.serverResp)
                assert.NoError(t, err)
            }))
            defer server.Close()
            // Create client
            serverURL, err := url.Parse(server.URL)
            assert.NoError(t, err)
            client := &Client{
                logger: logrus.NewEntry(logrus.New()),
                base: serverURL,
                client: server.Client(),
                timeout: 30 * time.Second,
            }
            // Call FinalityProviders
            resp, err := client.FinalityProviders(tt.fpPk)
            if tt.expectError {
                assert.Error(t, err)
                assert.Nil(t, resp)
            } else {
                assert.NoError(t, err)
                assert.Equal(t, tt.expectedResp, resp)
            }
        })
    }
}
```

## Recommendation
When the finality provider key is not found, it should return an error to prevent approval requests with non-existent finality provider keys.

### Suggested Code Change
```go
func (cli *Client) FinalityProviders(fpPk string) (*v1.FinalityProvidersResponse, error) {
    response, err := cli.get(fmt.Sprintf("/v1/finality-providers?fp_btc_pk=%s", url.PathEscape(fpPk)))
    if err != nil {
        return nil, errors.Wrap(err, "request GetFinalityProviders")
    }
    decoded, err := utils.DecodeJSONResponse[v1.FinalityProvidersResponse](response)
    if err != nil {
        return nil, errors.Wrap(err, "decode FinalityProvidersResponse")
    }
    
    if len(decoded.Data) == 0 {
        return nil, errors.New("Key not found!")
    }
    
    return &decoded, nil
}
```

## Status
- Lombard: Fixed in PR 68.
- Cantina Managed: Fix looks good.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Lombard Finance |
| Report Date | N/A |
| Finders | Haxatron, dontonka, Bernd |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_lombard_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/3a1c4f65-6ef7-4d26-97f4-480f8093801d

### Keywords for Search

`vulnerability`

