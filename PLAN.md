# Project Improvement Plan

## Current State
This is a take-home technical assessment submission (VectorShift pipeline
builder: React/Vite frontend + FastAPI backend that validates a node graph
is a connected DAG), not a general portfolio project. 1 commit, public repo
at github.com/harry-sandhu/vector.

## What Is Already Good
- README is detailed and accurate: overview, directory structure, run
  instructions for both backend and frontend, and a "what lives where"
  section mapping assessment requirements to specific files.
- Clear separation of concerns (shared node base components, theme/design
  tokens, hooks, services).

## Issues Found
- `backend/.env` is tracked in git. Its only content is
  `ALLOWED_ORIGINS=http://localhost:3000` — not a real secret, but tracking
  `.env` files is a bad habit worth breaking for future projects. Not removed
  here since (a) the repo is public and already has this in its single
  commit, (b) rewriting history is out of scope/forbidden, and (c) the value
  itself is harmless (a localhost CORS origin).
- There's a broken nested git state under `frontend/` (git recognizes it as
  a submodule gitlink with no corresponding `.gitmodules` entry, and the
  nested `.git` reports "bad object HEAD"). This doesn't affect the pushed
  repo content (the submodule gitlink just points at a commit hash, nothing
  else was broken), but it makes `git status` in the parent repo require
  `--ignore-submodules` to run cleanly. Not fixed here — fixing it safely
  would mean removing/re-adding the submodule entry, which is a structural
  change beyond a documentation pass and risks altering tracked content in a
  public repo's single commit.
- Local working tree has uncommitted changes (`backend/main.py` modified,
  a stale `__pycache__` file removed) — left uncommitted, as this is
  finished assessment work and not something to silently amend.

## Documentation
README classified as **Good** — accurate, detailed, no rewrite performed.

## Code Quality
Not audited beyond what the README already documents; out of scope for a
finished take-home submission.

## Testing
No tests present. Not a priority to add retroactively for a submitted
assessment.

## Security
- `backend/.env` is tracked but contains no real secret (just a localhost
  CORS origin). Flagged for awareness only.
- `frontend/.env` exists locally but is untracked/ignored — correctly kept
  out of git.

## Architecture
Standard two-service layout (React frontend + FastAPI backend) appropriate
for the assessment's scope. No changes recommended.

## GitHub / Open Source Presentation
Public and low priority for the general profile — it's a take-home
assessment submission, not a flagship project. Visibility left unchanged
per instructions.

## Priority Roadmap
### P0 — Critical
- None.

### P1 — Important
- None — this is finished, submitted assessment work; no further investment
  expected.

### P2 — Nice to Have
- If ever reused as a portfolio reference, stop tracking `backend/.env` and
  resolve the stray `frontend` submodule gitlink.

## Recommended Next Steps
Treat as complete. No further action needed; low priority for the public
profile relative to active personal projects.
