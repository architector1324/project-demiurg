# Semantic Reality Generation Engine (SRGE)

**Semantic engine for generating internally coherent fictional realities - from quantum voids to dreaming cities, using prompt-driven LLM world synthesis.**

## Overview

**SRGE** is a tool that transforms natural language prompts into **self-sufficient, structured fictional realities**. By leveraging a highly specialized **system prompt** and local **Large Language Models (LLMs)** via Ollama, it generates semantic JSON outputs that don't just describe, but also **lay the foundation for the existence and evolution of complex worlds according to their own intrinsic logic.**

Whether you're building a simulation, a narrative universe, or an abstract conceptual model, SRGE provides a foundational structure grounded in pure semantic meaning.

## Motivation / Philosophy

SRGE was born from the desire to explore the true capabilities of Large Language Models beyond mere conversation or data retrieval. It represents an **ontological experiment** - a quest to harness LLMs as semantic engines capable of constructing self-contained, internally consistent realities. My aim is to demonstrate that even smaller, locally runnable models can serve as a "semantic core," enabling the creation and simulation of complex worlds at arbitrary levels of detail, entirely independent of external human interpretation. This project challenges the very notion of what constitutes a "reality" and how it can be synthetically generated.

## Core Features

SRGE offers a powerful set of capabilities designed to bring complex realities to life:

*   **Prompt-Driven Reality Synthesis:** Simply provide a short text prompt, and SRGE will generate a unique, detailed fictional reality, tailored to your vision.
*   **Deep Ontological Structure:** Each generated world comes as a **structured JSON output**, meticulously defining its existence across five core dimensions. This isn't just text; it's a blueprint for a living world:
    *   `essence`: The fundamental nature and defining concept of the reality.
    *   `primary_constituents`: The core entities, elements, or principles that form its very fabric.
    *   `governing_framework`: The intrinsic laws and rules that dictate how the world functions.
    *   `driving_forces_and_potential`: The dynamic elements that propel change, evolution, and narrative possibilities.
    *   `foundational_state`: The initial conditions and primordial state from which the reality emerges.
*   **Unparalleled Consistency & Versatility:** SRGE delivers **genre-agnostic** and **internally consistent** semantic synthesis. Whether you're exploring the intricacies of quantum physics or the gritty depths of cyberpunk, the generated realities will always adhere to their own logical framework.
*   **Pure Intrinsic Logic:** Unlike typical game or narrative engines, SRGE focuses solely on the **intrinsic logic of the world itself**. There's no "player framing" – the reality exists independently, driven by its own internal dynamics.
*   **Reality as Observation:** Worlds created by SRGE are, in essence, infinitely complex and possess the potential for endless detail. However, due to the technical limitations of storing infinitude on a computer, their representation takes on a **quantum nature**: the world's details are initially **undetermined and in a state of potentiality**, akin to the principles of quantum mechanics. They **"materialize" and manifest** only upon targeted **"observation"** or focus from the user (via the `--navigate` command).

    **Important: This does not contradict the declared independence of the world from an external observer.** The LLM acts as a **"revealer" of inherent complexity**, not its arbitrary generator. The external observer, by requesting a deeper dive, does not **alter** the world or its internal laws, nor does it introduce anything external. It merely **prompts the world to "unfold"** that part of its structure which is already intrinsically embedded in its foundational semantic fabric. This process always occurs **strictly according to the internal rules and logic of the reality itself**. Thus, the observer does not create a new reality, but rather **explores** an already existing one, merely shifting to a deeper level of its manifestation. This guarantees that even with deep exploration, the world remains absolutely internally consistent and true to its initial laws.
*   **Local & Autonomous:** Run SRGE entirely on your machine without an internet connection. Powered by Ollama, it provides a self-contained environment for reality generation and exploration.


## Installation

To run SRGE locally, you'll need **Ollama** installed and configured, along with the `qwen3:4b`/`qwen3` models.

1.  **Install Ollama:** Follow the official instructions at [ollama.com](https://ollama.com/) to install Ollama on your system.

2.  **Pull the models:**

    ```bash
    ollama pull qwen3:4b
    ollama pull qwen3
    ```

3.  **Clone the SRGE repository:**

    ```bash
    git clone [https://github.com/architector1324/semantic-reality-generation-engine](https://github.com/architector1324/semantic-reality-generation-engine)
    ```

4.  **Install Python dependencies (if any)::**

    ```bash
    pip install ollama
    ```


## Commands

| Command     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Status        |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------ |
| `--create`  | Generate a completely new, high-level reality from a short prompt.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | **Ready**     |
| `--query` | Interrogate a generated world through semantic Q&A. Answers are inferred purely from the world's internal ontology and logic - not guessed or invented.                                                                                                                                                                                                                                                                                                                                                                                        | **Ready**     |
| `--navigate`| Traverse and semantically unfold the inherent, granular details of an existing world. This is not arbitrary generation; the world automatically reveals its pre-existing complexity and structure upon focused "observation," strictly adhering to its internal logic.                                                                                                                                                                                                                                                                  | **Ready**     |
| `--live`    | Simulate dynamic evolution and events within a generated world based on its internal forces and rules.                                                                                                                                                                                                                                                                                                                                                                                                                                            | *Planned*     |

---

## Semantic Navigation (Unfolding Reality)

The `--navigate` command is a core mechanism for **exploring and revealing the inherent, granular layers** of an already generated reality. It embodies the principle of **"Reality as Observation"**: where the details of a world exist in a state of potentiality and **materialize (unfold)** upon focused intent. This is not arbitrary generation; instead, it is a **semantic unfolding** of pre-existing, intrinsic complexity, logically derived from the parent entity and the overarching laws of the world.

Imagine a vast, multi-dimensional map where only the major continents are initially visible. `--navigate` acts like a zoom function, progressively revealing cities, then streets, then individual buildings. All these details **already existed** on the map; they were simply not "rendered" at that specific level of granularity.

When invoking `--navigate`, the user specifies a point of focus or a conceptual path (e.g., "Water Droplet", "Woman at a table"). The system (the LLM guided by the system prompt) acts as a **sophisticated semantic lens, interpreting the query and revealing the corresponding hierarchical layers.** This process then adds granular `"manifestation"` objects to the world's JSON structure.

Each newly revealed layer or entity always remains **strictly consistent** with its parent entity and the world's overarching laws.

**Key Features:**

*   **Hierarchical Consistency:** All elements within the `manifestation` (its internal constituents, laws, and forces) are direct, more specific **consequences or deeper manifestations** of the parent entity's description and the parent world's governing structure, ensuring continuous logical coherence.
*   **Semantic Pathfinding and Unfolding:** The LLM does not require an exact name match. It **interprets** the user's query within the existing ontology and **semantically determines the logical path** to the specified focus. If the requested entity is deeply nested, the model **recursively unfolds the entire chain of manifestation**, revealing the necessary intermediate `manifestation` levels.
    *   Example: If the user requests `--navigate 'woman at a table in a restaurant'` when the world is described down to "New York City", the model will unfold the chain: `City -> District -> Building -> Restaurant -> Table -> Woman`, adding new `manifestation` objects at each level.
*   **Focus-Oriented Detailing:** For larger entities, the command intelligently focuses on the most relevant sub-components, aggregating the vast majority of other parts into a single representative entity (e.g., `"Other [Entity Name] Components"`), preventing excessive data proliferation.
*   **Internal and Objective:** In line with SRGE's core philosophy, the output is entirely devoid of an external observational frame, describing the world purely from within itself. The user does not *create* a new reality, but rather *explores* and *observes* the unfolding of an already existing one, merely shifting to a deeper level of its manifestation.

The command returns the **complete, modified world JSON**, where the selected constituent element is updated or created with its new, deeper manifestation. This allows for recursive exploration, building an increasingly detailed ontological map of your fictional reality.

> Example:
> `python reality-gen.py --model qwen3 --navigate 'Sand' --input world.json`

## Usage Examples

To generate a new world (using the `--create` command):

#### Fundamental physics ontology:

```bash
python reality-gen.py --model qwen3:4b --think --create "Two particles in a vacuum"
```

The output will be a structured JSON representing the generated reality, similar to this:

```json
{
  "essence": "A universe defined by the interaction of two fundamental particles within an empty spatial expanse, governed by the laws of quantum mechanics and relativistic physics.",
  "primary_constituents": [
    {
      "name": "Particle A",
      "description": "A subatomic entity with a net positive charge, existing in a quantum superposition of states within the vacuum."
    },
    {
      "name": "Particle B",
      "description": "A subatomic entity with a net negative charge, oscillating between energy levels in response to interactions with Particle A."
    }
  ],
  "governing_framework": [
    "Quantum field theory dictates that particles emerge from and annihilate into the vacuum's zero-point energy.",
    "Electromagnetic force mediates interactions between the charged particles, altering their energy states.",
    "Conservation of momentum ensures that any exchange of momentum between the particles is balanced.",
    "Vacuum fluctuations introduce temporary virtual particles that may influence the particles' trajectories."
  ],
  "driving_forces_and_potential": [
    "Electromagnetic attraction between the particles creates a potential well that can trap them in stable configurations.",
    "Quantum tunneling allows the particles to overcome energy barriers, leading to transient bound states.",
    "Gravitational effects, though negligible, contribute to the curvature of spacetime around the particles.",
    "Uncertainty principles impose limits on the precision of measurements of their positions and momenta."
  ],
  "foundational_state": "The particles are initially separated by a distance equivalent to the Bohr radius, with Particle A in an excited energy state and Particle B in a ground state, surrounded by a dynamic vacuum containing virtual particle-antiparticle pairs."
}
```

#### High-fantasy realm:

```bash
python reality-gen.py --model qwen3:4b --think --create "A magical world with knights, magic, and villains"
```

```json
{
  "essence": "A realm where magic flows through the fabric of existence, governed by the interplay of light and shadow. Knights serve as guardians of balance, while dark forces seek to unravel the world's harmony.",
  "primary_constituents": [
    {
      "name": "Aetherion",
      "description": "The magical realm where energy from the Celestial Core sustains life, and the boundaries between reality and illusion are thin."
    },
    {
      "name": "Order of the Starlight",
      "description": "Knights who channel pure light magic to protect Aetherion, bound by ancient oaths to maintain the world's equilibrium."
    },
    {
      "name": "Shadow Syndicate",
      "description": "A network of villains who harness forbidden dark magic to exploit the world's vulnerabilities, seeking to dominate the Celestial Core."
    },
    {
      "name": "Crystal Spire",
      "description": "A towering crystalline structure that channels the Celestial Core's energy, serving as both a source of light magic and a target for dark forces."
    },
    {
      "name": "Void Nexus",
      "description": "A primordial void where dark magic originates, its power fluctuating in cycles that influence the stability of Aetherion."
    }
  ],
  "governing_framework": [
    "Magic is drawn from the Celestial Core, with light magic requiring alignment with the world's natural rhythms and dark magic demanding corruption of its essence.",
    "Knights must undergo trials of purity to wield light magic, while villains must betray their own essence to channel dark magic.",
    "The Crystal Spire's energy fluctuates with the Cycle of Shadows, a natural phenomenon that intensifies the Void Nexus's influence every 333 years.",
    "Balance between light and dark magic is maintained by the world's sentient energy, which manifests as the Aetherial Current."
  ],
  "driving_forces_and_potential": [
    "The eternal struggle between the Order of the Starlight and the Shadow Syndicate to control the Celestial Core's energy.",
    "The Cycle of Shadows, which could trigger a collapse of the Aetherial Current if the Void Nexus's power overwhelms the Crystal Spire.",
    "The potential for a knight to succumb to dark magic, becoming a twisted version of themselves known as a Shadowblade.",
    "The possibility of the Celestial Core itself being a sentient entity, capable of reshaping Aetherion's laws of magic."
  ],
  "foundational_state": "The Crystal Spire currently sustains the Aetherial Current, but the Shadow Syndicate has begun to corrupt the void around the Void Nexus, threatening to disrupt the Cycle of Shadows. The Order of the Starlight remains vigilant, preparing for the impending crisis."
}
```

### **Semantic Navigation in Action: Unfolding the Woman in New York**

This example showcases the **true power of Semantic Navigation (Unfolding)** - not merely detailing entities, but **recursively revealing logical hierarchies** in response to a query, and brilliantly embodying the **"Reality as Observation"** principle where world details manifest upon user focus.

**Initial World State (abbreviated, `world.json`):**
```json
{
    "essence": "A bustling metropolis...",
    "primary_constituents": [
      {
        "name": "New York City",
        "description": "A vast urban landscape spanning five boroughs..."
      }
    ],
    // ... rest
}
```

**Navigation Query:**
```bash
python reality-gen.py --model qwen3 --navigate 'A woman sitting at a table in a restaurant in New York City.' --input world.json
```

**Result (schematic representation of the unfolded reality, demonstrating the manifestation chain):**
*(Only the key unfolding chain is shown. The full, corrected JSON version with complete details is available [here](./examples/New%20York/A%20woman%20sitting%20at%20a%20table%20in%20a%20restaurant%20in%20New%20York/world.json).)*

```json
{
  "essence": "...", // Top-level essence of the metropolis
  "primary_constituents": [
    {
      "name": "New York City",
      "description": "...",
      "manifestation": { // New York City unfolds...
        "essence": "The intricate social and spatial fabric...",
        "primary_constituents": [
          {
            "name": "Restaurant",
            "description": "A dedicated space for dining...",
            "manifestation": { // Restaurant unfolds...
              "essence": "A curated environment...",
              "primary_constituents": [
                {
                  "name": "Table",
                  "description": "A surface for dining...",
                  "manifestation": { // Table unfolds...
                    "essence": "A focal point for social interaction...",
                    "primary_constituents": [
                      {
                        "name": "Woman",
                        "description": "An individual engaged in the act of dining...",
                        "manifestation": { // Woman unfolds into her observable and inherent details...
                          "essence": "A dynamic entity navigating...",
                          "primary_constituents": [
                            {
                              "name": "Physical Form",
                              "description": "The corporeal structure of the woman...",
                              "manifestation": { // Physical Form further unfolds into specific physical attributes
                                "essence": "A manifestation of biological and cultural attributes...",
                                "primary_constituents": [
                                  { "name": "Posture", "description": "..." },
                                  { "name": "Attire", "description": "..." },
                                  { "name": "Gestures", "description": "..." }
                                  // ... and other details specific to Gestures, Attire, Posture
                                ]
                              }
                            },
                            { "name": "Sociocultural Identity", "description": "..." }
                            // ... and other details specific to Woman
                          ]
                        }
                      }
                      // ... and other details specific to Table
                    ]
                  }
                }
                // ... and other details specific to Restaurant
              ]
            }
          }
          // ... and other details specific to New York City
        ]
      }
    }
  ]
  // ... rest
}
```

**What this outstanding example demonstrates:**
*   **Hierarchical Unfolding:** The model successfully built the manifestation chain `New York City` → `Restaurant` → `Table` → `Woman`, revealing the necessary `manifestation` objects at each level. This shows how SRGE unveils nested, logically connected entities.
*   **Context-Aware Revelation:** The "Woman" entity was detailed not only to abstract states (`Physical Form`, `Sociocultural Identity`), but also to concrete, observable attributes (`Posture`, `Attire`, `Gestures`). This perfectly aligns with the request for a "detailed description" in this context, demonstrating the model's intelligent understanding of the world.
*   **Ontological Autonomy:** The model independently determined the relevance and depth of detailing, strictly adhering to the world's internal logic, without external instructions or level constraints. SRGE does not "invent" but rather "manifests" what already semantically exists.
*   **Confirmation of "Reality as Observation":** The user's query served as an act of "observation" that compelled the world to "unfold" and reveal its internal complexity along the specified path, without creating new entities outside its inherent logic. The world unravels, it is not created.

## Manifesto: The Vision Behind SRGE

SRGE is more than just a world generator; it's an **engine for creating autonomous, living, self-contained realities**. These worlds exist by their own internal laws, not for the sake of a player or an observer.

*   **Semantic Core:** We use language to forge miniature universes, with the LLM serving as their very breath.
*   **Ontos, Not Text:** This is not merely text; it's an **ontos** – an ordered collection of entities and their relationships, where "word becomes flesh, and JSON its substance."
*   **Witness, Not Author:** You are not the author, player, or god; you are a **witness to an alien reality**, observing worlds where events unfold for their own internal reasons, not for or because of us.
*   **LLM as Law:** The world lives by itself. The LLM acts as the **physical law governing its existence**.
*   **Challenging Reality:** This is an **ontological experiment in a pocket-sized format**, designed to reveal the true capabilities of language models – even small ones – and to push the boundaries of what constitutes "reality."
