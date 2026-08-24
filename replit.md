# gTTS Text-to-Speech

Command-line Python app that converts text into MP3 speech with gTTS.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string
- `python main.py "Text to speak"` — generate `output.mp3`
- `python main.py --help` — show text-to-speech options
- `streamlit run app.py --server.port 3000` — run the FRIDAY web UI

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)
- Python: 3.11 with gTTS, managed through `pyproject.toml`
- Streamlit: interactive FRIDAY chat UI with Gemini responses and MP3 playback

## Where things live

- `main.py` — CLI entry point and speech generation
- `pyproject.toml` / `uv.lock` — Python dependency source of truth
- `README.md` — usage examples
- `app.py` — Streamlit chat interface

## Architecture decisions

- gTTS is used directly so the app stays small and produces standard MP3 files.
- Text can come from a command argument, interactive prompt, or UTF-8 file.
- The web UI reuses the same Gemini chat and gTTS logic as the CLI.

## Product

Chat with FRIDAY through the terminal or Streamlit, generate Gemini responses,
and listen to or download the latest MP3 response.

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

_Populate as you build — sharp edges, "always run X before Y" rules._

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
