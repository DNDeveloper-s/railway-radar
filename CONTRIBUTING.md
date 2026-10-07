# Contributing to Railway Radar

Railway Radar tracks Indian Railways trains in real time on a map. It is also a
learning project: three people build it as if it were a large production system.
Please read this page once before your first pull request.

## Set up

You need Node.js 20 and pnpm (the exact pnpm version is pinned in `package.json`).

```bash
pnpm install
pnpm dev
```

Then open http://localhost:3000.

For the map you need a Mapbox token. Ask Saurabh for it (he sends it through a
self-destructing link), then copy `apps/web/.env.example` to `apps/web/.env.local`
and paste the token there. `.env.local` is ignored by git. Never commit a token.

## How we work

Every change starts from a Jira ticket.

1. Open the ticket in Jira. In the **Development** panel click **Create branch**
   and use exactly the branch name Jira gives you.
2. Commit with the commit message shown in the same panel. It starts with the
   ticket key, for example `SCRUM-26 Add Mapbox env template`.
3. Open a pull request into `main`. Fill in the template.
4. Wait for the checks to pass and for one teammate to approve.
5. Squash and merge. Jira moves the ticket to Done by itself.

One ticket, one branch, one pull request. If you find extra work, ask for a new
ticket instead of adding it to yours.

## Before you open a pull request

```bash
pnpm turbo run lint typecheck test
```

The same command runs on GitHub and must pass before a merge.

## Rules that protect the project

- The frontend never calls RailKit or any other third-party API. Only our own
  backend does.
- Never commit secrets (tokens, keys, `.env` files).
- Keep pull requests small, ideally under about 400 changed lines.
- Be ready to explain every line you wrote or pasted, including code from an AI tool.

## More

- Team rules, definition of done, architecture decisions and the roadmap are in
  our Confluence space: https://dndeveloper.atlassian.net/wiki/spaces/RR
- Start with the page "Working Agreement".
- Stuck for more than 30 minutes? Ask. Comment on the ticket with the exact
  command you ran and the exact error text.