
# Todo
- [ ] Add payment processing
- [ ] Implement rate limiting for free users
- [ ] Add read history for users
- [ ] Add a mechanism to merge local read history and user preferences to remote server
- [ ] Implement Glossary feature
- [ ] Implement Sentences feature
- [ ] Implement Word-to-last-read-sentences feature


## stripe local webhook
Setting webhook on Stripe: https://dashboard.stripe.com/webhooks

Then:
```bash
brew install stripe/stripe-cli/stripe
stripe login

stripe listen --forward-to localhost:9000/bill/webhook

```