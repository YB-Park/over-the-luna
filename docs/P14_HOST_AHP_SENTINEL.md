# P14 Host AHP reachability — one-shot, zero model usage

This trigger authorizes only the authenticated localhost AHP initialize
with official VS Code CLI on GitHub Actions. No model turns or SDK plugin
leaf delegation, provider credentials, tunnels, organization data or writes.

The actual Copilot Host must be distinguished from P5 standalone SDK.

## Compatibility follow-up

First real Host boot succeeded, but the AHP initialize response was an RPC
error. Prefer the Host's own advertised protocolVersion and capture only the
sanitized RPC error code on mismatch. No model calls or access to private data.

## Current protocol compatibility

Official VS Code source supports AHP 1.0.0, 0.9.0 and compatibility 0.10.0.
The preceding Host RPC code -32005 confirmed that earlier offered protocol
versions were incompatible. This no-model run tests corrected handshake.
