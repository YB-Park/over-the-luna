# P16 Native Host plugin registration, one-shot

This one-shot public GitHub Action publishes the existing Next plugin to a real
VS Code Agent Host via AHP session/activeClientSet and observes the parsed
named agents. It sends no chat turn, uses no Copilot request permission,
no private code, no provider login, no token logging and no release action.

## Correct host-local plugin path

Prior run observed the plugin in loading status, but was publishing a
client-owned file URI without a client filesystem implementation.
Official host-local file scheme is vscode-agent-host-file. This no-turn
probe uses that exact scheme and never requests a model.
