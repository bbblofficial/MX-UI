# Changelog

## 2.0.0

**Reliability**
- Panel startup no longer waits for Xray validation or boot.
- Xray outbound DNS and connections prefer IPv4 to avoid slow dual-stack
  fallbacks on Railway and similar hosts.
- Kubernetes defaults to one replica because sessions and Xray state are local.

**Panel**
- Rebuilt dashboard: live throughput scope, 24h traffic chart, system VU meters, filterable config list.
- Subscription page redesigned as a boarding-pass card (QR stub, quota gauge, copy-all).
- Logs page with level/source filters and live tail.
- Light and dark themes, keyboard-friendly dialogs, mobile layout.

**Core**
- Enable/disable, expiry, quota and device limits are enforced at the gateway: toggling a config
  no longer restarts Xray and no longer kicks other users.
- Live sessions are cut within ~5 s when a config is disabled, expires or runs out of data.
- Configs are hot-added and removed through the Xray API; full reload is only a fallback.
- Xray is supervised and restarted automatically if it crashes.
- Per-config speed caps apply to both directions (token bucket).
- Xray API calls fixed: `--server` must come right after the sub-command.
- Blocking spawn moved off the event loop.

**Security**
- Passwords stored with PBKDF2 (v1 hashes upgrade on next login).
- Login rate limiting, HttpOnly + SameSite cookies (Secure behind HTTPS), sessions stored hashed.
- Security headers on HTML responses.

**Subscriptions**
- `/sub/<id>` returns the base64 list for VPN clients and the page for browsers (`?raw` forces the list).
- Standard `subscription-userinfo`, `profile-title` and `profile-update-interval` headers.

**Backup**
- Download and restore (merge or replace) a JSON backup from the dashboard.

## 1.0.0
- Initial release.
