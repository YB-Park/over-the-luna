# P15 authentic AHP Copilot session initialization — no model

This one-time, public GitHub Actions task checks whether a real VS Code
Copilot Agent Host can create and dispose a session over authenticated
AHP. It never sends a chat turn, has no copilot-requests write permission,
and does not access company data or external provider keys.

## Approved GitHub-only credential diagnostic

The first no-token session was accepted but not ready. This iteration
uses only the job-scoped GitHub Actions token with GitHub Copilot request
permission for native session initialization, still with zero chat turns.
It records lifecycle state and does not send model requests.
