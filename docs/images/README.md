# Architecture Diagrams

This directory contains visual architecture diagrams for the HEDIS Portfolio Optimizer project.

## Available Diagrams

### 1. High-Level System Architecture
**File**: `architecture-high-level.png`  
**Description**: Shows the complete system architecture with three main layers:
- User Interface Layer (Streamlit, FastAPI, Mobile)
- Application Layer (Context Engineering, Agentic RAG, Security)
- Data Layer (PostgreSQL, ChromaDB, Ollama)

**Referenced in**:
- `docs/ARCHITECTURE.md`
- `Artifacts/project/phase4_dashboard/ARCHITECTURE.md`

### 2. RAG Architecture
**File**: `architecture-rag.png`  
**Description**: Illustrates the RAG implementation architecture showing:
- Context Engineering Layer (3-layer hierarchical)
- Agentic RAG Layer (Planning, Execution, Synthesis)
- Joint Context-Agentic Layer

**Referenced in**:
- `Artifacts/project/docs/technical/RAG_IMPLEMENTATION.md`

### 3. Production Architecture Layers
**File**: `architecture-production-layers.png`  
**Description**: Clean architecture layers:
- Presentation Layer (UI)
- Application Layer (Services)
- Domain Layer (Business Logic)
- Infrastructure Layer (Technical)

**Referenced in**:
- `Artifacts/project/phase4_dashboard/PRODUCTION_ARCHITECTURE.md`

### 4. Query Processing Data Flow
**File**: `architecture-data-flow.png`  
**Description**: Shows the complete query processing flow from user query to response:
1. User Query
2. PHI Validation
3. Context Engineering
4. Agentic RAG Planning
5. Tool Execution
6. Self-Correction
7. Response Synthesis
8. PHI Validation
9. Audit Logging
10. User Response

**Referenced in**:
- `docs/ARCHITECTURE.md`

### 5. Security Architecture
**File**: `architecture-security.png`  
**Description**: Zero external API exposure architecture showing:
- Local Embedding Model (Ollama)
- Local Vector Store (ChromaDB)
- Local SQL Generation (LLM)
- Internal Database Query
- All processing on-premises

**Referenced in**:
- `docs/SECURITY_ARCHITECTURE.md`
- `Artifacts/project/phase4_dashboard/COMPLIANCE_ARCHITECTURE.md`

## Usage

These diagrams are automatically referenced in the documentation files. To update a diagram:

1. Regenerate the image using the same filename
2. Replace the existing file in this directory
3. The documentation will automatically display the updated diagram

## Image Format

- **Format**: PNG
- **Style**: Professional architecture diagrams
- **Colors**: Healthcare AI theme with HIPAA compliance indicators
- **Resolution**: High-resolution for clear display in documentation

## Notes

- All diagrams are generated from ASCII art diagrams in the documentation
- Diagrams maintain consistency with the text-based architecture descriptions
- Diagrams include security and compliance indicators where relevant
