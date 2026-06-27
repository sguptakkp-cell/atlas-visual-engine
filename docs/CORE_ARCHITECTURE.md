# Atlas Visual Engine

# Core Architecture

Version: 1.0 (Frozen)

---

# Purpose

The Core Engine provides the foundation of the Atlas Visual Engine.

Every diagram, animation, experiment, and visualization is built on top of the Core Engine.

The Core Engine itself should remain independent of any specific subject such as Physics, Chemistry, or Mathematics.

---

# Architecture Layers

```
Educational Libraries
        │
        ▼
Physics / Chemistry / Mathematics
        │
        ▼
Diagram Library
        │
        ▼
Primitive Library
        │
        ▼
Core Rendering Engine
        │
        ▼
Constants
        │
        ▼
Matplotlib
```

Dependencies always flow downward.

Lower layers must never depend on higher layers.

---

# Core Modules

## canvas.py

Responsible for:

* Creating figures
* Creating axes
* Managing canvas size
* Background color
* Grid
* Axis visibility

This is the entry point for every diagram.

---

## renderer.py

Responsible for rendering drawable objects.

The renderer never creates objects.

It only draws them.

---

## scene.py

Stores drawable objects.

Example:

* Line
* Arrow
* Circle
* Rectangle
* Text

A Scene knows what to draw.

The Renderer knows how to draw.

---

## figure.py

Responsible for

* Saving figures
* Exporting
* Closing figures
* Figure lifecycle

---

## theme.py

Responsible for

* Colors
* Fonts
* Line styles
* Themes

---

# Rendering Pipeline

```
Create Canvas

↓

Create Scene

↓

Add Primitives

↓

Render Scene

↓

Export Figure
```

---

# Design Principles

1. One responsibility per module.

2. No duplicated code.

3. Constants never hardcoded.

4. Reusable components.

5. Public API should remain simple.

---

# Public API Goal

The long-term user experience should be as simple as:

```python
from atlas import Canvas

canvas = Canvas()

canvas.add(Line(...))

canvas.save("figure.png")
```

Users should not need to know the internal architecture.

---

# Status

Architecture Status

Frozen

Ready for Sprint 006 Implementation.
