#!/bin/bash
# Pre-tool hook: block Write/Edit operations that contain secrets
# Catches: Stripe keys, private keys (hex), Bearer tokens hardcoded in source

INPUT=$(cat)
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // empty')

if [ -z "$CONTENT" ]; then
  exit 0
fi

# Check for Stripe keys
if echo "$CONTENT" | grep -qE 'sk_(live|test)_[a-zA-Z0-9]{20,}'; then
  echo "BLOCKED: Content contains what looks like a Stripe secret key. Use environment variables instead." >&2
  exit 2
fi

# Check for hex private keys (64 hex chars, common for ETH/Base wallets)
if echo "$CONTENT" | grep -qE '0x[a-fA-F0-9]{64}'; then
  echo "BLOCKED: Content contains what looks like a private key (64 hex chars). Use environment variables instead." >&2
  exit 2
fi

# Check for hardcoded Bearer tokens (more than 20 chars)
if echo "$CONTENT" | grep -qE 'Bearer [a-zA-Z0-9_\-]{20,}'; then
  echo "BLOCKED: Content contains what looks like a hardcoded Bearer token. Use environment variables instead." >&2
  exit 2
fi

exit 0
