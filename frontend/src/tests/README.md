# Browser smoke scenarios

## Current browser observations

- `/courses` renders the catalog, course filters, search field, and cards. Selecting a card opens its detail route; the detail page's back link returns to the catalog.
- `/signup` and `/login` render their forms. Submitting the email form displays a notice that email account creation and login are not connected yet. Kakao OAuth is the available account flow.
- Opening checkout or selecting a paid course while signed out redirects to `/login`.
- The 100 KRW PortOne test course is catalog data for payment integration checks.

## Authenticated payment scenario

Use a test Kakao account and proceed only when the PortOne channel is confirmed to be a sandbox/test channel. Complete checkout and confirm the success page and enrollment. Do not authorize a payment against a live channel.
