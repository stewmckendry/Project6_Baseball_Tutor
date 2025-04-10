# ⚾ Knowledge Graph Data Model – Socratic Sports Coach

---

## 🎯 Overview

The Knowledge Graph models baseball game situations, plays, responsibilities, concepts, and reasoning to drive Socratic question generation and feedback.

Each **situation** encodes:
- A game state (outs + runners)
- The position involved
- A triggered play
- Recommended actions (with order)
- Key learning concepts
- An explanation

These are converted into a directed graph of nodes (entities/concepts) and edges (relationships) with attached metadata.

---

## 🧩 Node Types

| Node Type       | Example                         | Metadata Tracked                      |
|----------------|----------------------------------|---------------------------------------|
| Position        | `Shortstop`                     | —                                     |
| Game State      | `0 outs, runners on 1st`        | —                                     |
| Play            | `Grounder to SS`                | `explanation`, `source`, `recommended_action_sequence` |
| Action          | `Throw to 2nd`                  | —                                     |
| Concept         | `Double Play`                   | —                                     |

---

## 🔗 Edge Types

Each edge has a `predicate` (relationship type), and may include metadata like `source` and `order`.

| Predicate              | From → To                        | Meaning                              | Metadata       |
|------------------------|----------------------------------|--------------------------------------|----------------|
| `hasResponsibilityIn`  | Position → Game State            | This position is involved in this situation | `source`        |
| `triggers`             | Game State → Play                | This situation leads to this play    | `source`        |
| `suggests`             | Play → Action                    | This play recommends this action     | `order`, `source` |
| `requiresUnderstandingOf` | Play → Concept               | Understanding this concept is needed | `source`        |

---

## 📋 Situation Attributes (from YAML)

```yaml
- situation_id: "double_play_ss"
  game_state: "0 outs, runners on 1st"
  position: "Shortstop"
  play: "Grounder to SS"
  recommended_actions:
    - "Throw to 2nd"
    - "Throw to 1st"
  key_concepts:
    - "Double Play"
    - "Force Out"
  explanation: "Shortstop should throw to 2nd to start the double play..."
  source: "llm"
```

---

## 🧠 Graph Constraints / Assumptions

- Each game state has one associated play (via one `triggers` edge)
- Plays may suggest multiple actions, which may have an explicit `order`
- Only play nodes have `explanation` and `recommended_action_sequence` metadata
- All strings are assumed unique identifiers (not UUIDs yet)
- The graph is a directed, acyclic network for now (no feedback loops)

---

## 🛠️ Additional Utilities

- `get_rich_context(position, game_state)` retrieves all related info for LLM prompt construction
- Visualizations use `pyvis` with node coloring and highlights
- Actions are optionally ordered using `order` edge metadata