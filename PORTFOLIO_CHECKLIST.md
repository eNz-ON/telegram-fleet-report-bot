# Publishing checklist

- Revoke the Telegram token that was previously stored in source code.
- Keep the replacement token only in `.env`.
- Verify that `service_account.json` is untracked.
- Remove all real people, phone numbers, Telegram IDs, plates, insurance details, addresses, and company data.
- Add screenshots using demo data only.
- Run `git status` before the first push.
