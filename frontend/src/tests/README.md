# Browser smoke scenarios

## Current browser observations

- `/courses` renders the catalog, course filters, search field, and cards. Selecting a card opens its detail route; the detail page's back link returns to the catalog.
- `/signup` submits the name, email, and password to the backend and signs the account in when registration succeeds. `/login` authenticates an existing email account. Kakao OAuth remains available as another sign-in option.
- Opening checkout or selecting a paid course while signed out redirects to `/login`.
- The 100 KRW PortOne test course is catalog data for payment integration checks.

## Authenticated payment scenario

Use a test Kakao account and proceed only when the PortOne channel is confirmed to be a sandbox/test channel. Complete checkout and confirm the success page and enrollment. Do not authorize a payment against a live channel.
