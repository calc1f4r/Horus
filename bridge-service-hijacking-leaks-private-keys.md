---
# Core Classification
protocol: Auro Mobile Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46881
audit_firm: OtterSec
contest_link: https://www.aurowallet.com/
source_link: https://www.aurowallet.com/
github_link: https://github.com/aurowallet/auro-wallet-mobile-app

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
  - Caue Obici
  - Robert Chen
---

## Vulnerability Title

Bridge Service Hijacking Leaks Private Keys

### Overview


The report discusses a bug in the bridge service, which is a javascript bundle used in a headless webview. The mobile app creates a local web server to retrieve the javascript file, but the algorithm used to find an available port can lead to security issues. If no port is available, the function will still succeed by using the default port (8080), which could allow a malicious app to create a TCP listener and serve a malicious javascript bundle to the webview. This could potentially expose sensitive information such as private keys and lead to its leakage. The suggested solution is to remove the local web server and use static asset loading instead. The issue has been fixed by loading the asset statically from the assets directory.

### Original Finding Content

## Bridge Service Security Vulnerability

The bridge service is a JavaScript bundle executed inside a headless webview. To pull the JavaScript file, the mobile app creates a local web server by trying to locate an available port from the range 8000 to 8200, as demonstrated below:

```dart
// LocalWebviewServer.dart
int _currentPort = 8080;
final int _portRangeStart = 8000;
final int _portRangeEnd = 8200;

Future<String> startLocalServer() async {
    if (await _isPortAvailable(_currentPort)) {
        await _startServerOnPort(_currentPort);
    } else {
        for (int port = _portRangeStart; port <= _portRangeEnd; port++) {
            if (await _isPortAvailable(port)) {
                _currentPort = port;
                await _startServerOnPort(port);
                break;
            }
        }
    }
    return serverUrl;
}
```

The issue with this algorithm is that if no port is available, the function will still succeed by returning the `serverUrl` with the default port (8080). If a malicious app is present on the device, it could create TCP listeners on all those ports and host an attacker-controlled web server on port 8080. This setup allows the attacker to serve a malicious JavaScript bundle to the bridge service’s webview. Since the webview is used to derive private keys from mnemonics and generate signatures, the malicious bundle could expose this sensitive information, leading to its leakage.

## Remediation

Remove the usage of `LocalWebServer` and use static asset loading instead. Here is the official documentation of `WebViewAssetLoader`.

## Patch

Fixed in e27f14c by removing the usage of the local webserver and loading the asset statically from the assets directory.

```diff
// lib/service/webview/bridgeWebView.dart
- controller.loadUrl(
-   urlRequest: URLRequest(
-     url: WebUri(localServerUrl + "assets/webview/bridge.html")));
+ // https://github.com/pichillilorenzo/flutter_inappwebview/issues/586
+ await controller.loadFile(
+   assetFilePath: "assets/webview/bridge.html");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Auro Mobile Wallet |
| Report Date | N/A |
| Finders | Caue Obici, Robert Chen |

### Source Links

- **Source**: https://www.aurowallet.com/
- **GitHub**: https://github.com/aurowallet/auro-wallet-mobile-app
- **Contest**: https://www.aurowallet.com/

### Keywords for Search

`vulnerability`

