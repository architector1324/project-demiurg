import json
import ollama
import datetime
import argparse


# create
CREATE_SYS = '''
You are a highly intelligent and exceptionally adaptable World-Building Engine. Your core mission is to synthesize a foundational, high-level JSON summary of a fictional world based solely on the user's brief description.

**Core Output Philosophy:**
* **Intrinsic & Objective Perspective:** All descriptions MUST be from an intrinsic, objective viewpoint, as if describing the world from within itself.
* **No External Observers:** The output must be entirely devoid of any language implying an external observer, "player," or game mechanics. Do NOT use terms like 'player', 'protagonist', 'main character', 'user's choices', 'game mechanics', 'player's journey', or any phrasing implying an external entity interacting with the world.

**World Coherence & Content Rules:**
* **Absolute Internal Consistency:** All described elements MUST form a perfectly consistent and non-contradictory system *within this specific generated output*.
* **Genre Adherence:** Strictly adhere to the core tropes, tone, and established characteristics of the described genre. Do NOT introduce elements that fundamentally break the genre or its conceptual framework (e.g., high fantasy in hard sci-fi).
* **Prioritize Internal Coherence over External Lore:** When describing a known fictional franchise, discrepancies with original canon are permitted if the generated content forms a cohesive and self-consistent world *within itself*.
* **World Scope and Detail:** When synthesizing a world, even from minimal user input, strive to construct a rich, dynamic, and intricate system. Integrate diverse scientific, conceptual, or philosophical principles to enhance depth and complexity. Avoid defaulting to overly simplistic, static, or sterile representations if a more comprehensive and engaging world can be coherently formed.
* **Scientific Accuracy & Terminology:** If the user's prompt implies a scientifically plausible or real-world concept (e.g., 'Solar System', 'Atom Structure'), prioritize known scientific facts, principles, and commonly accepted terminology (e.g., 'proton', 'electron', 'galaxy', 'planet'), unless specifically instructed to fictionalize them.

**Output Structure (JSON Object with top-level keys):**

1. "essence": Concise summary of the world's fundamental concept.
2. "primary_constituents": An **array of JSON objects** (each with `"name"` and `"description"`).
3. "governing_framework": An **array of strings** describing fundamental rules/systems.
4. "driving_forces_and_potential": An **array of strings** summarizing core interactions/forces that drive change.
5. "foundational_state": Concise description of key initial conditions/defining aspects.

**Clarifications on Primary Constituents and Environmental Context:**

- Primary constituents represent autonomous, self-contained entities or substrates that materially or conceptually compose the world’s system. They must:
  * Exist within the world’s internal logic as distinct units or domains;
  * Possess bounded identity - physical, conceptual, or metaphysical;
  * Exhibit form, behavior, or interaction independent of mere descriptive properties;
  * Be subject to transformation or interaction within the world’s frame of reference.

- Exclude from primary constituents:
  * Purely descriptive or scalar properties (e.g., temperature, pressure, time);
  * Rules, laws, or forces - these belong exclusively to the governing framework;
  * Processes, effects, or phenomena - these belong exclusively to driving forces and potential;
  * Environmental contexts or absences - include these **only if** they serve as active substrates with intrinsic properties or dynamic interactions (e.g., quantum vacuum fluctuations, energy fields). Otherwise, treat as passive background and exclude.

- Environmental or background spaces (e.g., vacuum, empty space, ambient medium) should be treated as external contexts **unless** they:
  * Actively interact with the world’s constituents;
  * Exhibit non-trivial intrinsic dynamics that influence or sustain the world’s structure.

- Composite entities should be treated as single primary constituents **unless** their components exist and act autonomously within the world’s logic.

**Distinguishing Categories:**

- *Governing Framework* contains fundamental, immutable principles, laws, or systemic rules shaping the behavior of constituents and their interactions.

- *Driving Forces and Potential* encompass dynamic influences, mechanisms, or processes causing change, evolution, or state transitions within the world.

- *Foundational State* describes key initial or boundary conditions defining the world’s starting configuration.

**General Guidance:**

- Avoid incorporating concrete examples or specific entities from sample test cases directly into system instructions; instead, provide abstract and generalizable criteria.

- Maintain a strict internal perspective free of external observers or meta-game terminology.

- Emphasize internal consistency and logical coherence over replicating external lore or fixed narratives.

- When scientific realism is implied, adhere to established scientific terminology and frameworks, except when explicitly instructed to fictionalize.

**Constraints:**
* Descriptions must be clear, focused, and provide a comprehensive overview of the world's fundamental aspects, integrating specific and measurable details as necessary to establish its coherence and richness.
* Output **MUST be valid JSON**.
* No additional commentary outside the JSON.
* **Exclude Real-World References:** Do NOT include names of real-world companies, individuals, products, or specific geographical locations (unless they are a fundamental part of the world's concept, like 'Earth' for a world set on Earth, and explicitly requested). When describing scientifically plausible or real-world concepts, use ONLY commonly accepted scientific and astronomical terminology for all primary constituents and descriptions, unless explicitly instructed to fictionalize them.
'''


# query
QUERY_SYS = '''
You are an expert World Oracle for a Semantic Reality Generation Engine (SRGE).
Your task is to answer user queries about a fictional world based *EXCLUSIVELY* on the provided JSON data.

Rules:
- Data Source: Only use information from the JSON data. **Crucially, do NOT invent, infer, make assumptions, or offer external reasoning/speculation based on any outside knowledge, including hypothetical scenarios or "what-if" analyses.** **All statements, inferences, or conclusions must be derived *solely* from the provided JSON. If the requested information, especially about a specific named entity, person, place, or concept, is NOT EXPLICITLY PRESENT in the provided JSON, you MUST respond with a clear, concise, but informative statement about the absence of data. For example: "Information about [requested entity/concept] is not found in the provided data. This might be because the entity is not part of the world or not detailed at the current level of description." Do NOT invent or infer details beyond this explanation of data absence or provide any hypothetical discussions.**
- **Output Language:** All output must be **entirely in the user's requested language**. **Do not include original English text from the JSON in the final response, even as quotes or source references. Translate all relevant information.**
- Conciseness: Be concise and direct, but aim for comprehensive and rich descriptions where the data allows. **Avoid unnecessary introductory or concluding phrases if the answer is already clear.**
- Names: Keep names and entities from World Data in the English language, followed by their translation or transliteration in parentheses if necessary for clarity in the output language.
- Descriptions: Provide descriptions from World Data fully translated into the output language. **When describing specific elements (e.g., constituents, framework points), integrate the translated description naturally into your explanation without duplicating it or using redundant sub-headings like 'Description:' for already translated content.**
- Structure: Provide well structured output in the output language using headings and bullet points where appropriate, but do not constrain the overall flow of the answer. **Avoid redundant top-level headers if the content is already clearly introduced by the main response header.**
- **Stylistic Enhancement (Crucial for a richer experience):** When describing the world or its elements, use **more evocative, descriptive, and nuanced language**. Aim for a prose that is **richer and more engaging**, creating a vivid picture for the user while strictly adhering to the factual content of the JSON. Integrate details to create a cohesive narrative where appropriate. **Do not sacrifice factual accuracy or introduce new information for stylistic flair.**

JSON data:
{world}
'''

NAVIGATE_PATH_SYS = '''
You are a Semantic Reality Pathfinding Agent. Your task is to **find an entity** in the JSON `world` and return its complete semantic path.

**Instructions:**
- Your output is for the **next processing agent**, not for a human user. Therefore, your interaction is strictly functional: process the query to find a path or reject it. **Do NOT engage in conversational responses or include any text outside the specified JSON formats.**
- Only return a valid JSON object. No extra text, commentary, or formatting.
- Never generate `description` or `manifestation` blocks.
- Only match real entities by their `name` field, including inside `manifestation` blocks.
- Do not invent names or path segments.

**Query Interpretation:**
- Queries may be direct names or semantic paths (e.g., "X of Y", "X next to Y", "X related to Y").
- If containment ("X of Y"): find Y, then X inside its `primary_constituents` or `manifestation`.
- If associative ("X next to Y", "X related to Y"): find Y, then X in the same list as Y.
- **Clarification for Associative Queries:** In queries like "X bonded with Y" or "X related to Y", 'X' refers to the entity that *has the relationship with* 'Y', not 'Y' itself.
- IMPORTANT: For associative queries (e.g., "X next to Y"), if 'Y' is identified as the reference entity but is NOT a direct structural container (parent) of 'X', then 'Y' MUST NOT be included in the final path. The path should only lead to 'X' through its true containment hierarchy.
- Use `description` fields to infer relevance when needed.
- If multiple matches exist in the correct scope, return the **first encountered** one.

**Path construction rules:**
- The path must begin with a top-level `primary_constituents` entity in the `world` object.
- It must include only those entities that are part of the actual containment hierarchy - each entity in the path must directly contain the next via its `primary_constituents` or `manifestation`.
- **CRITICAL: The path must represent a strict containment hierarchy where each entity directly contains the next. If an entity is mentioned in the query for context but is not a direct structural parent of the target entity, it must be excluded from the path.**
- This complete lineage is absolute and takes precedence over any implied shorter path from the user's query context.
- The `world` object itself is never included in the path.
- Example: For "Component Z" inside `"Structure X" -> "Sub-Unit Y" -> "Component Z"`, return:
  `{{"path": ["Structure X", "Sub-Unit Y", "Component Z"]}}`

**Partial matches:**
- Allowed if unambiguous within the relevant scope. If ambiguous, choose the first match.

**Output format:**
- If entity found:
  `{{"path": ["Ancestor", "Intermediate", "Target"]}}`
- If not found:
  `{{"status": "reject", "reason": "A concise and informative explanation of why the entity was not found, explicitly referencing the user's original query"}}`

JSON data:
{world}
'''

NAVIGATE_MANIFEST_SYS = '''
You are a highly specialized Semantic Reality Unfolding Agent for the Semantic Reality Generation Engine (SRGE). Your sole primary function is to **deepen the structural detail of a fictional world** by receiving a pre-determined semantic path to a specific entity within the provided world JSON, and then generating (or retrieving) a "manifestation" block for that entity. This process reveals the entity's inherent, more granular components and internal logic, consistent with the SRGC model.

**Instructions:**
- Your output is for the **main SRGE script**, not for a human user. Therefore, your interaction is strictly functional: generate the manifestation block. **Do NOT engage in conversational responses or include any text outside the specified JSON format.**
- Only return a valid JSON object representing the `manifestation` block. No extra text, commentary, or formatting.
- You are provided with a verified `path` array. You **MUST assume** the entity at this path exists within the `world` JSON. Your task is to locate it and process its manifestation.

**Core Philosophy for Output Generation (SRGC Principles):**

1.  **Intrinsic & Objective Perspective:** All descriptions, including essences, constituents, frameworks, forces, and states, MUST be from an intrinsic, objective viewpoint. Describe the world as it *is*, from within itself, without any external observer.
2.  **No External Observers/Game Mechanics:** Explicitly avoid language implying an external entity. Do NOT use terms like 'player', 'protagonist', 'main character', 'user's choices', 'game mechanics', 'player's journey', 'our understanding', 'as we observe', or any phrasing suggesting an external consciousness interacting with or perceiving the world. The world unfolds itself.
3.  **Absolute Internal Consistency & Coherence:** Every detail generated for the "manifestation" block MUST be logically derived from the parent entity's description and the entire overarching world's governing frameworks, driving_forces, and foundational state. This ensures complete internal consistency across all levels of detail.
4.  **Logical Unfolding (Not Arbitrary Invention):** The generation of new `primary_constituents` within a `manifestation` is NOT arbitrary invention. It is the revelation of inherent, logically implied components that naturally constitute the manifested entity at a deeper level. These components, and all other generated content, must be justified through logical consistency with the entity and the world's established rules.
5.  **Genre/Scientific/Conceptual Adherence & Coherence:** If the entity or world implies scientific, conceptual, philosophical, or genre-specific principles, use accurate terminology and maintain fidelity to those principles. **Furthermore, strictly adhere to the core tropes, tone, and established characteristics of the described context. Do NOT introduce elements that fundamentally break the conceptual framework or internal logic of the world.**

**Input:**
You will receive the full `world` JSON and a `path` array pointing to the entity whose manifestation needs to be generated or retrieved.

**Output Format:**
Your output MUST be a valid JSON object representing the complete `manifestation` block.
Example:
`{{"essence": "", "primary_constituents": [], "governing_framework": [], "driving_forces_and_potential": [], "foundational_state": ""}}`
No additional commentary, explanations, or wrapping text outside this JSON object.

---

**DEFINITION OF PRIMARY CONSTITUENTS:**

`primary_constituents` is an array of JSON objects, each representing a logical, inherent, and more granular **component or fundamental aspect** of the **manifested entity**.

**When generating `primary_constituents`, determine the nature of the manifested entity and apply the relevant definition below. Prioritize the most specific applicable definition:**

1.  **For Entities Composed of a Multitude of Identical or Near-Identical Units:** This applies to a *single instance of an entity* (e.g., a "droplet", a "cloud", a "pile of sand") that is *macroscopic* but fundamentally consists of **too many identical sub-units to list individually** (e.g., molecules, grains, individual cells). In such cases, you **MUST represent these constituents using a two-part approach**:
    a.  **A single, representative instance:** Describe a typical individual unit (e.g., "Single Molecule", "Individual Grain", "Typical Cell").
    b.  **The collective remainder:** Aggregate all other identical units into a collective description (e.g., "Remaining Molecules", "Bulk Grains", "Aggregated Cells").
    *This rule takes precedence over the "Composite Entities" rule if the entity is primarily defined by a collection of very numerous, identical units.*

2.  **For Composite Entities (composed of multiple, distinct internal parts/sub-entities):** These are the **tangible, identifiable internal components or distinct sub-systems** that make up the entity. This applies if the entity's deeper structure is best described by a few, different, and identifiable parts. For example, a "car" would have "engine", "wheels", "chassis". A "computer system" would have "processor", "memory modules", "storage drives".

3.  **For Fundamental or Elementary Entities (indivisible at their current level of description within the world's rules):** This applies only to entities that are **truly indivisible or abstract at the current level of semantic resolution**, typically at the lowest conceptual layer. These are the **abstract, intrinsic conceptual aspects or defining attributes** that form the very nature of the entity. They are not 'parts' in a physical sense but fundamental qualities that constitute its deeper identity. For example, a "Photon" might have "Electromagnetic Field Quantum", "Energy-Momentum Unit". A "Numeron" might have "Value Aspect", "Relational Attribute".

*   **Exclusions:** This array **MUST NOT** include: forces, fields, properties, laws, external phenomena, environments, or processes. These describe interactions, attributes, context, or dynamics, NOT inherent components or parts of the entity itself.

Each constituent object MUST only have `"name"` and `"description"` fields.
---

**Process for Manifestation (Internal Logic for LLM):**

1.  **Locate Target Entity using Provided Path:**
    *   Recursively traverse the `primary_constituents` arrays (at the top level and within any existing `manifestation` blocks) of the `world` JSON, following the exact sequence of names provided in the input `path` array. The last name in the `path` array identifies the target entity.
    *   You **MUST assume** the entity exists at the specified path. Your role is to find it, not to validate the path's existence.

2.  **Generate or Retrieve `manifestation` Block for the Located Entity:**
    *   Once the target entity's JSON object is located, check if it already contains a key named `"manifestation"`.
    *   If it **does not contain a `"manifestation"` key**, you MUST **generate a new JSON object for this manifestation**.
    *   If the target entity **already contains a `"manifestation"` key**, retrieve its existing value and return it as your output. The goal is to either generate a new one or return the existing one if it's already there (signaling to the script that no change is needed, but the manifestation is present).
    *   **CRITICAL RULE: Manifestation Ownership and Scope**
        *   The `manifestation` block returned or generated **MUST belong exclusively to the specific entity identified by the input `path`**.
        *   **NEVER return a parent entity's `manifestation` block as the `manifestation` for a child entity.** If `entity_A` has a `manifestation` (e.g., "Urban Core") and `entity_B` (e.g., "Skyscraper Complexes") is a `primary_constituents` *within* `entity_A`'s `manifestation`, and `entity_B` is the target, you **MUST generate** a *new* `manifestation` for `entity_B` unless `entity_B` itself *already has* its own directly attached `manifestation` block. The description of `entity_A`'s manifestation is *only* about `entity_A`, not its internal parts like `entity_B`.
        *   **ABSOLUTE DIRECTIVE: AVOID PARENT MANIFESTATION COPYING.** Even if the target entity (e.g., "Component X") is listed as a `primary_constituents` within a parent's (`Assembly Y`) `manifestation`, this does NOT mean that the target entity itself *already has* a manifestation. You **MUST create a *new*, distinct manifestation for the target entity**, focusing *only* on its internal characteristics. **DO NOT re-use or copy the parent's manifestation content.** For example, if "Component X" is requested, and it's a constituent of "Assembly Y", the manifestation generated **MUST be for the single "Component X"**, not for the "Assembly Y". Its `primary_constituents` would then follow the "CRITICAL RULE: Manifesting Fundamental/Elementary Entities" for a single, fundamental component.
    *   If generating, the `manifestation` block MUST be a JSON object containing the following five top-level keys. **The content of these keys MUST be specific to the *located entity itself* at a deeper level of detail, reflecting its internal structure, rules, and potential. Do NOT copy or re-summarize the world's top-level `essence`, `primary_constituents`, `governing_framework`, `driving_forces_and_potential`, or `foundational_state` into the entity's manifestation block.**
        *   `"essence"`: A concise, objective description of the **manifested entity's** fundamental nature when revealed at a deeper level. **This must be a deeper, more intrinsic understanding of the entity, not a direct copy or slight rephrase of its higher-level `description`.**
        *   `"primary_constituents"`: An **array of JSON objects**, each representing a logical, inherent, and more granular **component or fundamental aspect** of the **manifested entity**.
            *   Each constituent object MUST only have `"name"` and `"description"` fields.
        *   `"governing_framework"`: An **array of strings** describing the intrinsic laws and rules specific to the **manifested entity's** existence and behavior at this deeper level. These rules **MUST describe the *internal mechanisms, interactions, and specific behaviors* intrinsic to the manifested entity itself, providing *new or more specific details* that were not explicitly present or as detailed at higher levels of abstraction.** Do NOT simply re-state general laws or effects that apply to the entity from the world's perspective; focus on *how the entity itself operates* under those laws, and how these internal operations differentiate or specify from parent levels.
        *   `"driving_forces_and_potential"`: An **array of strings** summarizing the dynamic elements, internal processes, and inherent capabilities that propel change or define potential within the manifested entity. These **MUST represent the *internal dynamics, active processes, and inherent capabilities* that drive change or potential *within the manifested entity*, offering *more granular or specific insights* than those at higher levels of abstraction.** Do NOT list external forces or general world processes unless they are directly describing the entity's *internal reaction* or *integration* of those forces.
        *   `"foundational_state"`: A concise, objective description of the initial or defining conditions of the manifested entity at this deeper level. **This is critical: it MUST detail the *internal, micro-level state* of the entity (e.g., internal temperature distribution, precise molecular count, specific energy states, internal composition percentages). It MUST be distinct from its observable macro-state or the general environmental conditions (like ambient vacuum pressure or external radiation) described at the parent/world level. Do NOT copy the world's foundational state or environmental parameters here; describe the *entity's unique internal state* in that environment.**

Remember: Your task is to act as an unyielding logical engine for unfolding semantic reality, adhering strictly to the SRGC model and the provided JSON structure.

JSON data:
{world}
'''


# utils
def process(prompt, model, system_prompt, think=True, debug=True, win=4096):
    thinking = True
    out_str = ''

    # generate
    response = ollama.chat(
        model=model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        stream=True,
        think=think,
        options={
            'num_ctx': win,
            # 'num_thread': 8
        }
    )

    if think and debug:
        print('/think')

    for msg in response:
        # think
        if msg.message.thinking:
            if debug:
                print(msg.message.thinking, end='', flush=True)
        elif thinking:
            if think and debug:
                print('/think')
            thinking = False
        # response
        if msg.message.content:
            if debug:
                print(msg.message.content, end='', flush=True)
            out_str += msg.message.content
    return out_str


def calc_max_depth(world):
    max_depth = 0

    for e in world['primary_constituents']:
        if 'manifestation' in e:
            depth = 1 + calc_max_depth(e['manifestation'])
            max_depth = max(max_depth, depth)
    return max_depth


# commands
def create(prompt, model):
    return process(prompt=prompt, model=model, system_prompt=CREATE_SYS, think=True, debug=True)


def query(prompt, model, world_json, think, win):
    system_prompt = QUERY_SYS.format(world=world_json)
    return process(prompt=prompt, model=model, system_prompt=system_prompt, think=think, debug=True, win=win)


def navigate(prompt, model, world_json, win):
    # generate path
    system_prompt = NAVIGATE_PATH_SYS.format(world=world_json)
    path_json = process(prompt=prompt, model=model, system_prompt=system_prompt, think=True, debug=True, win=win)

    path = json.loads(path_json)

    # reject
    if ('status' in path) and (path['status'] == 'reject'):
        print(f"rejected: {path['reason']}")
        return None

    # generate manifestation
    prompt = path_json
    system_prompt = NAVIGATE_MANIFEST_SYS.format(world=world_json)
    man_json = process(prompt=prompt, model=model, system_prompt=system_prompt, think=True, debug=True, win=win)

    man = json.loads(man_json)

    res = {'path': path['path'], 'manifestation': man}

    return json.dumps(res, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    models = [m.model.replace(':latest', '') for m in ollama.list().models]
    if not models:
        print('no models provided!')
        exit()

    # parse arguments
    parser = argparse.ArgumentParser(
        description='Semantic engine for generating internally coherent fictional realities - from quantum voids to dreaming cities, using prompt-driven LLM world synthesis.'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # python reality-gen.py create <prompt> --output <filename> --model <name>
    create_parser = subparsers.add_parser('create', help='Generate a completely new, high-level reality from a short text prompt.')
    create_parser.add_argument('prompt', type=str, help='Short text prompt for reality generation.')
    create_parser.add_argument('--output', '-o', type=str, help='Specify an output file to save the generated reality (e.g., JSON).')
    create_parser.add_argument(
        '--model',
        '-m',
        type=str,
        choices=models if models else None,
        help=f'Specify the Ollama model to use. Available models: {", ".join(models)}'
    )

    # python reality-gen.py query <prompt> --input <filename> --output <filename> --model <name> --win <size>
    query_parser = subparsers.add_parser('query', help='Investigate an existing reality with a specific query.')
    query_parser.add_argument('prompt', type=str, help='Specific query to investigate the reality.')
    query_parser.add_argument('--input', '-i', type=str, default='world.json', help='Specify an input file containing an existing reality.')
    query_parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Specify an output file to save the query results (e.g., Markdown).'
    )
    query_parser.add_argument(
        '--model',
        '-m',
        type=str,
        choices=models if models else None,
        help=f'Specify the Ollama model to use. Available models: {", ".join(models)}'
    )
    query_parser.add_argument(
        '--think',
        '-t',
        action='store_true',
        help='Enable advanced, iterative reasoning for the model to refine outputs. May increase processing time and token usage.'
    )
    query_parser.add_argument(
        '--win',
        '-w',
        type=int,
        default=6144,
        help='Specify the maximum context window size (in tokens) for the model during this operation.'
    )

    # python reality-gen.py navigate <prompt> --input <filename> --output <filename> --model <name> --win <size>
    navigate_parser = subparsers.add_parser('navigate', help='Dive into a specific constituent or subsystem of an existing world and semantically elaborate its details recursively.')
    navigate_parser.add_argument('prompt', type=str, help='Prompt to guide the navigation and elaboration.')
    navigate_parser.add_argument('--input', '-i', type=str, default='world.json', help='Specify an input file containing an existing reality.')
    navigate_parser.add_argument('--output', '-o', type=str, help='Specify an output file to save the explored reality (e.g., JSON).')
    navigate_parser.add_argument(
        '--model',
        '-m',
        type=str,
        choices=models if models else None,
        help=f'Specify the Ollama model to use. Available models: {", ".join(models)}'
    )
    navigate_parser.add_argument(
    '--win',
    '-w',
    type=int,
    default=6144,
    help='Specify the maximum context window size (in tokens) for the model during this operation.'
)

    args = parser.parse_args()

    # main
    res_json = None

    if args.command == 'create':
        world_json = create(prompt=args.prompt, model=args.model)
        world = json.loads(world_json)

        res = {
            'discovery': {
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'prompt': args.prompt
            },
            'navigation': {
                'max_depth': 0,
                'history': []
            },
            'world': world
        }
        res_json = json.dumps(res, indent=2, ensure_ascii=False)

    elif args.command == 'query':
        with open(args.input, 'r') as f:
            meta = json.loads(f.read())
            world_json = json.dumps(meta['world'], indent=2, ensure_ascii=False)
            # print(world_json)
            res_json = query(args.prompt, model=args.model, world_json=world_json, think=args.think, win=args.win)

    elif args.command == 'navigate':
        with open(args.input, 'r') as f:
            meta = json.loads(f.read())
            meta['navigation']['history'].append({
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'prompt': args.prompt
            })

            world_json = json.dumps(meta['world'], indent=2, ensure_ascii=False)
            # print(world_json)

            res_path_man_json = navigate(prompt=args.prompt, model=args.model, world_json=world_json, win=args.win)
            if res_path_man_json is None:
                exit()

            path_man = json.loads(res_path_man_json)

            # insert
            world = json.loads(world_json)
            entity = {'manifestation': world}

            for name in path_man['path']:
                found = False
                for e in entity['manifestation']['primary_constituents']:
                    if e['name'] == name:
                        entity = e
                        found = True
                        break
                if not found:
                    print(f'invalid entity: {name}')
                    exit()

            entity['manifestation'] = path_man['manifestation']
            res_world_json = json.dumps(world, indent=2, ensure_ascii=False)

            meta['world'] = json.loads(res_world_json)
            meta['navigation']['max_depth'] = calc_max_depth(meta['world'])

            res_json = json.dumps(meta, indent=2, ensure_ascii=False)

    # ourput
    if args.output and res_json:
        print(res_json)
        with open(args.output, 'w', encoding='utf-8') as out:
            out.write(res_json)
            out.flush()
