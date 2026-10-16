# Real-Time Meeting Feedback & AI Sentiment Portal

Participants open a link or scan a QR code, share feedback in under 30 seconds, and leadership sees sentiment, emotion, topics and questions update live on a dashboard.

- **Participant app** (`/e/<CODE>`): anonymous by default, no install, mobile-first. Feedback is saved first; AI analysis runs afterwards.
- **Leadership console** (`/admin`): Supabase Auth login, KPI cards, sentiment and emotion charts, a trend and heatmap, topic cloud, AI meeting pulse, feedback explorer with filters, live mode for a large screen, CSV export.
- **AI layer**: `AIAnalysisService` interface. Providers are selected by configuration. OpenAI, any OpenAI-compatible endpoint (vLLM, LM Studio, Azure proxies) and Ollama work today.

Stack: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS 4, Supabase (Postgres, Auth, Realtime, RLS), Recharts, Lucide icons, Zod, Vercel.

---

## 1. Local development

```bash
npm install
cp .env.example .env.local      # then fill in the values (see section 3)
npm run dev                     # http://localhost:3000
```

Other scripts:

| Command | What it does |
| --- | --- |
| `npm run typecheck` | TypeScript, strict mode |
| `npm run lint` | ESLint (Next.js core-web-vitals + TypeScript rules) |
| `npm test` | Unit tests and database/RLS tests (embedded Postgres, no Supabase needed) |
| `npm run build` | Production build |

---

## 2. Supabase setup

1. **Create a project** at supabase.com. Note the project URL, the `anon` key and the `service_role` key (Project Settings → API).

2. **Apply the schema in order** (SQL editor, or `supabase db push` with the CLI):
   1. `supabase/migrations/20261005000001_schema.sql` (tables, constraints, indexes)
   2. `supabase/migrations/20261005000002_rls.sql` (RLS policies, role helpers, Realtime publication)
   3. `supabase/migrations/20261005000003_analytics.sql` (`feedback_explorer` view and `event_analytics()` function)

3. **Lock down sign-ups.** Authentication → Sign In / Providers: keep Email enabled. Turn off "Allow new users to sign up" so only invited staff can have accounts. Invite staff from Authentication → Users.

4. **Create the first administrator.** After the user exists in Auth, run (replace the email):

   ```sql
   insert into public.profiles (id, email, name, role)
   select id, email, 'Administrator', 'ADMIN'
   from auth.users
   where email = 'admin@cwb.com';
   ```

   Roles: `ADMIN` (everything, including Demo Mode and the audit log), `ORGANIZER` (create and edit events, view feedback, export), `VIEWER` (read-only). Change roles by updating `profiles.role`.

5. **Realtime** is enabled for `feedback`, `feedback_analysis` and `events` by the migration. Confirm under Database → Replication that these tables are listed.

### Security model

- The `anon` role has **no** table access. Participants never query the database directly.
- Participant submissions go through `/api/public/events/<CODE>/feedback`, which runs on the server with the service-role key. That key is only imported by `server-only` modules and never reaches the browser.
- Signed-in staff use the anon key plus their session, so **RLS applies to every staff query**. The admin dashboard and Realtime only see rows the role allows.
- Anonymous events never store a name or employee ID, even if one is sent.
- No IP addresses or device data are stored.
- These admin actions are written to `audit_logs`: event create, update and status change, demo mode changes, demo event creation, CSV export and AI pulse regeneration. Sign-ins and single-response re-analysis are not yet audited.

---

## 3. Environment variables

See `.env.example`. Summary:

| Variable | Where | Purpose |
| --- | --- | --- |
| `NEXT_PUBLIC_SUPABASE_URL` | client and server | Project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | client and server | Public key, RLS applies |
| `SUPABASE_SERVICE_ROLE_KEY` | **server only** | Bypasses RLS for participant submissions and analysis writes |
| `AI_PROVIDER` | server | `openai`, `openai-compatible` or `ollama` |
| `OPENAI_API_KEY` | server | Required for `openai` |
| `OPENAI_MODEL` | server | Model name, for example `gpt-4o-mini` or `llama3.1` |
| `OPENAI_BASE_URL` | server | Optional. Required for `openai-compatible`. Defaults to Ollama's local endpoint for `ollama` |
| `ANALYSIS_WORKER_SECRET` | server | Bearer token for `POST /api/internal/analysis/process` |
| `NEXT_PUBLIC_APP_URL` | client and server | Public base URL, used in participant links and QR codes |
| `MAX_FEEDBACK_LENGTH` | server | Optional default limit, overridden per event |

Never commit `.env.local`. `.gitignore` already excludes it.

### Choosing an AI provider

```text
AI_PROVIDER=openai             # OPENAI_API_KEY, OPENAI_MODEL
AI_PROVIDER=openai-compatible  # OPENAI_BASE_URL, OPENAI_MODEL, optional OPENAI_API_KEY
AI_PROVIDER=ollama             # OPENAI_MODEL, optional OPENAI_BASE_URL (default http://localhost:11434/v1)
```

Analysis sends each response's text to the provider. Pick a provider your data-processing terms allow. Use `ollama` or a self-hosted endpoint to keep text inside your network.

---

## 4. Deploying to Vercel

The full checklist, with the environment variable table, is in [`docs/DEPLOY-VERCEL.md`](docs/DEPLOY-VERCEL.md). Summary:

- Set the `NEXT_PUBLIC_*` variables in Vercel **before** the first build, because they are compiled into the browser code.
- `.env.local` is never uploaded. Put every value in the Vercel dashboard.
- If a page shows "Setup needed", a variable is missing in Vercel. Add it and redeploy without the build cache.

1. Push the repository to GitHub, GitLab or Bitbucket.
2. In Vercel, **Add New → Project**, import the repository. Framework preset: Next.js. Build command: `npm run build`.
3. Add every variable from section 3 under **Settings → Environment Variables** for Production (and Preview if you want previews to work end-to-end).
4. Deploy. Check `/e/<CODE>` and `/admin/login`.

### Custom domain

1. Project → **Settings → Domains** → add `feedback.company.com`.
2. At your DNS provider, add the record Vercel shows. For a subdomain this is normally a `CNAME` to `cname.vercel-dns.com`.
3. Set `NEXT_PUBLIC_APP_URL=https://feedback.company.com` and redeploy, so QR codes point to the right address.
4. In Supabase → Authentication → URL Configuration, set the Site URL to the same domain.

### Background analysis

Analysis runs right after each submission (`after()`), so most responses are analysed within seconds. If a run fails or the provider is down, the response is still saved with status `failed`. Staff can retry from the dashboard. To retry automatically, call the worker endpoint from any scheduler every few minutes:

```bash
curl -X POST https://feedback.company.com/api/internal/analysis/process \
  -H "Authorization: Bearer $ANALYSIS_WORKER_SECRET"
```

Vercel Cron can do this on a Pro plan. A GitHub Actions schedule or any external cron works on any plan.

---

## 5. Using the app

1. **Create an event** at Admin → Events → New event. Choose the identity mode (anonymous, name optional, name required, employee ID required), the reaction and category options, and the maximum length.
2. **Start the meeting** on the event page (Draft or Scheduled → Live). Feedback is accepted only while the event is Live and before its end time. The database enforces this, so the API cannot bypass it.
   - **End meeting** stops feedback. **Deactivate Event** stops it permanently for that link and shows participants a "Meeting Closed" page.
   - After the end time passes, feedback closes automatically, even if nobody presses End.
3. **Display the QR code** from the event page (Download QR). Participants scan it, or open `https://<domain>/e/<CODE>`.
4. **Watch the dashboard** at Admin → Dashboard. It updates when responses arrive, and the time window control narrows the view to the last 5, 15 or 30 minutes.
5. **Live mode** (`/admin/events/<id>/live`) is a large-screen view with aggregate numbers and emotion tiles. It never shows comment text.
6. **Export** CSV from the dashboard or the event page. Cells that begin with `=`, `+`, `-` or `@` are neutralised to stop spreadsheet formula injection.

### Demo Mode

Off by default. Admin → Settings → turn on Demo Mode. The Events page then offers **Create demo event**, which creates a clearly labelled `DEMO` event with 12 sample responses. Production events never receive generated data.

---

## 6. How the pieces fit

```text
Participant ──POST──► /api/public/events/<CODE>/feedback
                         │ validate · honeypot · idempotency key · identity rules
                         ▼
                    feedback (status: received, analysis: pending)  ──► response 201
                         │ after()
                         ▼
                 AIAnalysisService.analyzeFeedback()   ◄── provider from AI_PROVIDER
                         │ validated JSON only; failures stored, never lost
                         ▼
                 feedback_analysis (+ analysis: completed)
                         │ Supabase Realtime (RLS applied per subscriber)
                         ▼
Admin dashboard ──► /api/events/<id>/analytics   (event_analytics() SQL aggregates)
                ──► /api/events/<id>/feedback    (feedback_explorer view, paged)
```

Code layout:

```text
src/
  app/
    page.tsx                       participant landing (redirects to the live event)
    e/[code]/                      participant event page
    admin/login/                   sign-in
    admin/(console)/               authenticated console (layout guards the routes)
      dashboard/ events/ settings/
    api/public/events/[code]/feedback   public submission
    api/events/[id]/analytics|feedback|export|pulse|analysis/retry
    api/feedback/[id]/analyze
    api/internal/analysis/process       worker endpoint (bearer token)
  components/
    participant/                   feedback form
    admin/                         dashboard, charts, explorer, live mode, forms
  hooks/                           Realtime refresh with debounce and fallback polling
  lib/                             constants, validation (Zod), env, errors, CSV, logger
  services/
    ai/                            AIAnalysisService, prompts, output schema, providers
    analytics/                     aggregates, explorer, export, AI pulse
    events/ feedback/ demo/ audit/ QR, event and feedback persistence
    supabase/                      server, browser and admin clients, guards
  proxy.ts                         session refresh and /admin route guard (Next 16)
supabase/migrations/               schema, RLS, analytics
tests/                             database/RLS tests and unit tests
```

### Adding an AI provider

Implement `AIAnalysisService` (`src/services/ai/types.ts`) with `analyzeFeedback` and `summarizeEvent`, return results through `output-schema.ts` so they are validated, and add a case to `createAIAnalysisService` in `src/services/ai/index.ts`. `OllamaProvider` is a short subclass of `OpenAIAnalysisProvider` and shows the pattern.

---

## 7. Known limitations

These are real gaps in this release. Check them before go-live.

- **Not run against a live Supabase project.** The migrations and RLS policies are tested against an embedded Postgres with Supabase's `anon`/`authenticated` roles and `auth.uid()` stubbed. Sign-in, Realtime delivery and Vercel runtime behaviour still need a smoke test in your own project.
- **Browser layout not verified on real devices.** The participant form is designed mobile-first, but it has not been checked on phones or tablets.
- **Rate limiting** is limited to a honeypot field and request size caps. Add Vercel Firewall rules or a store-backed limiter before a large public event.
- **Exports:** CSV only. Excel and PDF reports are not built.
- **Data retention** is not automated. Responses are kept until deleted in Supabase. A purge job is a good next step.
- **Settings:** AI provider and model are read-only on the Settings page and set through environment variables. Per-event options live on the event form.
- **Organisations:** the schema has an `organizations` table and `organization_id` columns, but RLS is not yet scoped by organisation. Do not add a second organisation until that is done.
- **SSO** and **dark mode** are not implemented. Auth is Supabase email and password.
- **Dashboard date filter:** not included. Each event is already scoped to its own date.
- **Analysis cost and privacy:** each response is sent to the configured AI provider. Summaries send up to 60 recent responses, with participant names and IDs never included.

For the full checklist of what was verified, see `docs/TEST_PLAN.md`.
