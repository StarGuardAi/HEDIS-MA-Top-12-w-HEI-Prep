# ADR-002: Use Streamlit over React Dashboard

## Status
Accepted

## Context
Portfolio project requirements:
- Fast development timeline (27 hours goal)
- Python-native ML model integration
- Interactive dashboard for demonstration
- No need for complex state management
- Single developer (no frontend team)

## Decision
Use Streamlit for the dashboard instead of React/TypeScript frontend.

## Consequences

**Positive:**
- ✅ Rapid development (production-ready dashboard in 27 hours vs. weeks for React)
- ✅ Python-native (no context switching between Python and JavaScript)
- ✅ Direct ML model integration (no API serialization needed)
- ✅ Built-in data visualization (Plotly, Matplotlib, Seaborn)
- ✅ Simple deployment (Streamlit Cloud, one command)
- ✅ Lower learning curve (Python-only stack)

**Negative:**
- ⚠️ Less customization than React (limited UI control)
- ⚠️ Performance limits at scale (not ideal for 100K+ concurrent users)
- ⚠️ Less flexible state management (session state is basic)
- ⚠️ Not ideal for complex user interactions

## Alternatives Considered

**React + TypeScript + FastAPI:**
- ✅ More customization and flexibility
- ✅ Better performance at scale
- ✅ Professional frontend framework
- ❌ Requires JavaScript/TypeScript knowledge
- ❌ Longer development time (weeks vs. hours)
- ❌ More complex deployment (separate frontend/backend)
- **Decision:** For portfolio demonstration, speed and simplicity outweigh flexibility

**Dash (Plotly):**
- ✅ Python-native like Streamlit
- ✅ More control than Streamlit
- ❌ Steeper learning curve
- ❌ More verbose code
- **Decision:** Streamlit's simplicity better for rapid prototyping

## Implementation Notes
- Created 10-page multi-page Streamlit app
- Used `streamlit_pages/` directory structure
- Implemented session state for user preferences
- Deployed to Streamlit Cloud for live demo
- Achieved production-ready dashboard in 27 hours

## Future Considerations
If this were a production system with:
- 100K+ concurrent users
- Complex user interactions
- Need for custom UI components
- Frontend team available

Then React + TypeScript would be the better choice.

