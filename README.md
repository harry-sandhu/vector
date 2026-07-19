# VectorShift — Pipeline Builder

A drag-and-drop pipeline builder (frontend) with a small FastAPI backend that
validates the pipeline graph (counts nodes/edges, checks it's a valid DAG,
checks it's fully connected).

├── backend/          FastAPI app — validates the pipeline
│   ├── main.py            <- the actual API logic lives here
│   ├── requirements.txt   <- Python deps (install these, don't need .venv)
│   └── .env
└── frontend/         React app — the canvas / node editor UI
├── public/
└── src/
├── app/App.jsx              top-level layout (topbar + sidebar + canvas)
├── layout/TopBar.jsx        brand, pipeline title, Submit button
├── layout/Sidebar.jsx       draggable node palette on the left
├── pipeline/
│   ├── PipelineCanvas.jsx        the React Flow canvas
│   ├── DraggableNode.jsx         sidebar icon + tooltip
│   ├── PipelineResultModal.jsx   "Submit" success/warning/error popup
│   ├── PipelineErrorModal.jsx    network-failure popup
│   └── store/pipelineStore.js    zustand store: nodes/edges state
├── nodes/
│   ├── shared/                base building blocks (baseNode, NodeHeader, NodeField, NodeHandle)
│   └── definitions/           one small file per node type (input, output, text, llm, api, database, condition, math, delay)
├── config/
│   ├── nodeRegistry.js       registers every node type (icon, color, category)
│   └── theme/                colors, spacing, radius, typography, etc. — the design system
├── services/pipelineApi.js  calls the backend's /pipelines/parse
└── hooks/                   small reusable hooks (auto-resizing textarea, node drag, etc.)



---

## Running it

You need two terminals — one for the backend, one for the frontend.

### 1. Backend (FastAPI)

```bash
cd backend           
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Runs at `http://localhost:8000`. Leave this terminal running.

### 2. Frontend (React)

```bash
cd frontend            
npm install
npm start
```

Opens at `http://localhost:3000`. The frontend reads the backend URL from
`REACT_APP_API_URL` in its `.env` file (see `src/services/pipelineApi.js`),
defaulting to `http://localhost:8000` if that's not set — so the backend
needs to already be running at whichever URL you configured.

### Using it

1. Drag nodes from the left sidebar onto the canvas.
2. Connect them by dragging from one node's handle (the small dot on its
   edge) to another's.
3. Click **Submit** (top right). This sends the current nodes/edges to the
   backend and shows a popup with:
   - **Nodes / Edges** — counts
   - A status message: pipeline is valid, has a cycle, or has nodes that
     aren't connected to anything.
4. If the backend isn't running, you'll get a "couldn't reach the backend"
   popup instead.

---

## What each part of the assessment lives where

- **Node abstraction** — `src/nodes/shared/baseNode.jsx` + `NodeHeader.jsx` +
  `NodeField.jsx` + `NodeHandle.jsx`. Every node type in
  `src/nodes/definitions/*.js` is just a config object (title, fields,
  handles) passed into the shared base — that's what makes adding a new node
  a ~20-line file instead of copy-pasting a whole component.
- **Styling / design system** — `src/config/theme/*`. Colors, spacing,
  radius, shadows, typography are all defined once and imported everywhere,
  so the whole app reads as one consistent design instead of per-component
  one-offs.
- **Text node logic** (auto-resize + `{{variable}}` → handle) —
  `src/nodes/definitions/textNode.js`, using
  `src/hooks/useAutoResizeTextarea.js` and
  `src/hooks/useTemplateVariables.js`.
- **Backend integration** — `src/services/pipelineApi.js` (frontend call) and
  `backend/main.py`'s `/pipelines/parse` endpoint (DAG + connectivity check),
  surfaced in `src/pipeline/PipelineResultModal.jsx`.

---

