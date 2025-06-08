# Semantic Reality Generation Engine (SRGE)

**Semantic engine for generating internally coherent fictional realities - from quantum voids to dreaming cities, using prompt-driven LLM world synthesis.**

## Overview

**SRGE** is a tool that transforms natural language prompts into **self-sufficient, structured fictional realities**. By leveraging a highly specialized **system prompt** and local **Large Language Models (LLMs)** via Ollama, it generates semantic JSON outputs that don't just describe, but also **lay the foundation for the existence and evolution of complex worlds according to their own intrinsic logic.**

Whether you're building a simulation, a narrative universe, or an abstract conceptual model, SRGE provides a foundational structure grounded in pure semantic meaning.

## Motivation / Philosophy

SRGE was born from the desire to explore the true capabilities of Large Language Models beyond mere conversation or data retrieval. It represents an **ontological experiment** - a quest to harness LLMs as semantic engines capable of constructing self-contained, internally consistent realities. My aim is to demonstrate that even smaller, locally runnable models can serve as a "semantic core," enabling the creation and simulation of complex worlds at arbitrary levels of detail, entirely independent of external human interpretation. This project challenges the very notion of what constitutes a "reality" and how it can be synthetically generated.

## Core Features

SRGE offers a powerful set of capabilities designed to bring complex realities to life:

  * **Prompt-Driven Reality Synthesis:** Simply provide a short text prompt, and SRGE will generate a unique, detailed fictional reality, tailored to your vision.
  * **Deep Ontological Structure:** Each generated world comes as a **structured JSON output**, meticulously defining its existence across five core dimensions. This isn't just text; it's a blueprint for a living world:
      * `world_essence`: The fundamental nature and defining concept of the reality.
      * `primary_constituents`: The core entities, elements, or principles that form its very fabric.
      * `governing_framework`: The intrinsic laws and rules that dictate how the world functions.
      * `driving_forces_and_potential`: The dynamic elements that propel change, evolution, and narrative possibilities.
      * `foundational_state`: The initial conditions and primordial state from which the reality emerges.
  * **Unparalleled Consistency & Versatility:** SRGE delivers **genre-agnostic** and **internally consistent** semantic synthesis. Whether you're exploring the intricacies of quantum physics or the gritty depths of cyberpunk, the generated realities will always adhere to their own logical framework.
  * **Pure Intrinsic Logic:** Unlike typical game or narrative engines, SRGE focuses solely on the **intrinsic logic of the world itself**. There's no "player framing" – the reality exists independently, driven by its own internal dynamics.
  * **Reality as Observation:** Worlds created by SRGE are, in essence, infinitely complex. However, akin to the principles of quantum mechanics, their details "materialize" only upon observation. The LLM acts as a **"revealer" of inherent complexity**, unfolding subsequent levels of detail within the world that are already intrinsic to its foundational semantic structure, rather than generating new content arbitrarily. This ensures that even with deep exploration, the world remains absolutely internally consistent and true to its initial laws.
  * **Local & Autonomous:** Run SRGE entirely on your machine without an internet connection. Powered by Ollama, it provides a self-contained environment for reality generation and exploration.


## Installation

To run SRGE locally, you'll need **Ollama** installed and configured, along with the `qwen3:4b` model.

1.  **Install Ollama:** Follow the official instructions at [ollama.com](https://ollama.com/) to install Ollama on your system.

2.  **Pull the `qwen3:4b` model:**

    ```bash
    ollama pull qwen3:4b
    ```

3.  **Clone the SRGE repository:**

    ```bash
    git clone https://github.com/architector1324/semantic-reality-generation-engine
    ```

4.  **Install Python dependencies (if any)::**

    ```bash
    pip install ollama
    ```


## Commands

| Command   | Description                                                                                                                                                             | Status       |
| :--- | :- | :- |
| `--create`   | Generate a completely new, high-level reality from a short prompt.                                                                                                      | **Ready** |
| `--explore` | Investigate the existing reality based on its already generated JSON, allowing Q\&A or factual extraction. **This command does not alter the world's state.** | **Ready** |
| `--deep`  | Dive into a specific constituent or subsystem of an existing world and semantically elaborate its details recursively. **The world automatically elaborates, revealing its inherent complexity.** | *In Progress* |
| `--live`  | Experimental: Simulate dynamic evolution and events within a generated world based on its internal forces and rules.                                                    | *Planned* |



## Usage Examples

To generate a new world (using the `--create` command):

#### Fundamental physics ontology:

```bash
python reality-gen.py --model qwen3:4b --think --create "Two particles in a vacuum"
```

The output will be a structured JSON representing the generated reality, similar to this:

```json
{
  "world_essence": "A universe defined by the interaction of two fundamental particles within an empty spatial expanse, governed by the laws of quantum mechanics and relativistic physics.",
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
  "world_essence": "A realm where magic flows through the fabric of existence, governed by the interplay of light and shadow. Knights serve as guardians of balance, while dark forces seek to unravel the world's harmony.",
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


## Manifesto: The Vision Behind SRGE

SRGE is more than just a world generator; it's an **engine for creating autonomous, living, self-contained realities**. These worlds exist by their own internal laws, not for the sake of a player or an observer.

  * **Semantic Core:** We use language to forge miniature universes, with the LLM serving as their very breath.
  * **Ontos, Not Text:** This is not merely text; it's an **ontos** – an ordered collection of entities and their relationships, where "word becomes flesh, and JSON its substance."
  * **Witness, Not Author:** You are not the author, player, or god; you are a **witness to an alien reality**, observing worlds where events unfold for their own internal reasons, not for or because of us.
  * **LLM as Law:** The world lives by itself. The LLM acts as the **physical law governing its existence**.
  * **Challenging Reality:** This is an **ontological experiment in a pocket-sized format**, designed to reveal the true capabilities of language models – even small ones – and to push the boundaries of what constitutes "reality."