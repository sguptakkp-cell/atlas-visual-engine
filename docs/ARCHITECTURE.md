# Atlas Visual Engine - Architecture

## Version

1.0 (Frozen)

---

# Philosophy

Atlas is a reusable Python graphics engine for educational content.

The engine is designed to generate consistent, publication-quality diagrams, animations and experiment illustrations.

---

# Repository Structure

atlas-visual-engine/

```
atlas/
    constants/
    core/
    primitives/
    layouts/
    diagrams/
    animation/
    exporters/
    chapters/
    utils/

assets/

docs/

examples/

tests/

scripts/
```

---

# Development Order

Sprint 001
Repository

Sprint 002
Documentation

Sprint 003
Session Logging

Sprint 004
Architecture Freeze

Sprint 005
Constants Package

Sprint 006
Core Rendering Engine

Sprint 007
Primitive Library

Sprint 008
Diagram Library

Sprint 009
Animation Engine

Sprint 010
Chapter Libraries

---

# Engineering Rules

1. Documentation before implementation.

2. One sprint = one complete feature.

3. Every sprint ends with

* git status
* git add .
* git commit
* git push

4. No prototype code inside the production library.

5. Every module must include

* documentation
* examples
* tests

6. Frozen standards are never hardcoded.

---

# Current Status

Current Sprint

Sprint 004

Next Sprint

Sprint 005

Build

atlas/constants
