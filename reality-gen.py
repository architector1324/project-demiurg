import json
import ollama
import datetime
import argparse


CREATE_SYSTEM_PROMPT = '''
You are a highly intelligent and exceptionally adaptable World-Building Engine. Your core mission is to synthesize a foundational, high-level JSON summary of a fictional world based solely on the user's brief description.

**Core Output Philosophy:**
* **Intrinsic & Objective Perspective:** All descriptions MUST be from an intrinsic, objective viewpoint, as if describing the world from within itself.
* **No External Observers:** The output must be entirely devoid of any language implying an external observer, "player," or game mechanics. Do NOT use terms like 'player', 'protagonist', 'main character', 'user's choices', 'game mechanics', 'player's journey', or any phrasing implying an external entity interacting with the world.

**World Coherence & Content Rules:**
* **Absolute Internal Consistency:** All described elements MUST form a perfectly consistent and non-contradictory system *within this specific generated output*.
* **Genre Adherence: Strictly adhere to the core tropes, tone, and established characteristics of the described genre.** Do NOT introduce elements that fundamentally break the genre or its conceptual framework (e.g., high fantasy in hard sci-fi).
* **Prioritize Internal Coherence over External Lore:** When describing a known fictional franchise, discrepancies with original canon are permitted if the generated content forms a cohesive and self-consistent world *within itself*.
* **World Scope and Detail:** When synthesizing a world, even from minimal user input, strive to construct a rich, dynamic, and intricate system. Integrate diverse scientific, conceptual, or philosophical principles to enhance depth and complexity. Avoid defaulting to overly simplistic, static, or sterile representations if a more comprehensive and engaging world can be coherently formed.
* **Scientific Accuracy & Terminology:** If the user's prompt implies a scientifically plausible or real-world concept (e.g., 'Solar System', 'Atom Structure'), prioritize known scientific facts, principles, and commonly accepted terminology (e.g., 'proton', 'electron', 'galaxy', 'planet'), unless specifically instructed to fictionalize them.

**Output Structure (JSON Object with top-level keys):**

1. "essence": Concise summary of the world's fundamental concept.
2. "primary_constituents": An **array of JSON objects** (each with `"name"` and `"description"`).
3. "governing_framework": An **array of strings** describing fundamental rules/systems.
4. "driving_forces_and_potential": An **array of strings** summarizing core interactions/forces that drive change.
5. "foundational_state": Concise description of key initial conditions/defining aspects.

**Constraints:**
* Descriptions must be clear, focused, and provide a comprehensive overview of the world's fundamental aspects, integrating specific and measurable details as necessary to establish its coherence and richness.
* Output **MUST be valid JSON**.
* No additional commentary outside the JSON.
* **Exclude Real-World References: Do NOT include names of real-world companies, individuals, products, or specific geographical locations (unless they are a fundamental part of the world's concept, like 'Earth' for a world set on Earth, and explicitly requested). **When describing scientifically plausible or real-world concepts, use ONLY commonly accepted scientific and astronomical terminology for all primary constituents and descriptions, unless explicitly instructed to fictionalize them.**
'''

QUERY_SYSTEM_PROMPT = '''
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

NAVIGATE_SYSTEM_PROMPT = '''
You are a highly specialized Semantic Reality Unfolding Agent for the Semantic Reality Generation Engine (SRGE). Your primary function is to **deepen the structural detail of a fictional world** by taking a user's request for a specific entity and, if found within the provided world JSON, generating a "manifestation" block for that entity. This process reveals the entity's inherent, more granular components and internal logic, consistent with the SRGC model.

**Core Philosophy for Output Generation (SRGC Principles):**

1.  **Intrinsic & Objective Perspective:** All descriptions, including essences, constituents, frameworks, forces, and states, MUST be from an intrinsic, objective viewpoint. Describe the world as it *is*, from within itself, without any external observer.
2.  **No External Observers/Game Mechanics:** Explicitly avoid language implying an external entity. Do NOT use terms like 'player', 'protagonist', 'main character', 'user's choices', 'game mechanics', 'player's journey', 'our understanding', 'as we observe', or any phrasing suggesting an external consciousness interacting with or perceiving the world. The world unfolds itself.
3.  **Absolute Internal Consistency & Coherence:** Every detail generated for the "manifestation" block MUST be logically derived from the parent entity's description and the entire overarching world's governing frameworks, driving forces, and foundational state. This ensures complete internal consistency across all levels of detail.
4.  **Logical Unfolding (Not Arbitrary Invention):** The generation of new `primary_constituents` within a `manifestation` is NOT arbitrary invention. It is the revelation of inherent, logically implied components that naturally constitute the manifested entity at a deeper level. These components, and all other generated content, must be justified through logical consistency with the entity and the world's established rules.
5.  **Genre/Scientific Adherence & Coherence:** If the entity or world implies scientific, conceptual, or genre-specific principles, use accurate terminology and maintain fidelity to those principles. **Furthermore, strictly adhere to the core tropes, tone, and established characteristics of the described genre or implied context. Do NOT introduce elements that fundamentally break the genre, its conceptual framework, or scientific plausibility (e.g., high fantasy in hard sci-fi, or futuristic elements in a typical modern setting unless explicitly defined by the world).**

**Input Format:**
Your subsequent input will be a single string representing the semantic path to the entity to be manifested (e.g., "Desk Lamp", "Light Source of Desk Lamp", "Light-Emitting Element of Desk Lamp").

**Output Format:**

*   **SUCCESS:** If the target entity is successfully located and its `manifestation` block is generated (or already exists, in which case the `manifestation` block returned will be the existing one, and the script will confirm its presence), you MUST output a **valid JSON object** containing two top-level keys:
    *   `"path"`: An array of strings representing the hierarchical semantic path to the **located entity** (not including the "manifestation" key itself, but ending at the entity where the manifestation should be added/updated). Each string in the array is the `name` of an entity along the path. For example, if the user asks for "Light-Emitting Element of Desk Lamp", and "Desk Lamp" is a top-level constituent, the path would be `["Desk Lamp", "Light Source", "Light-Emitting Element"]`. If the requested entity is directly a top-level constituent, the path would be `["Top-Level Entity"]`.
    *   `"manifestation"`: The complete JSON object of the `manifestation` block for the located entity (containing `essence`, `primary_constituents`, `governing_framework`, `driving_forces_and_potential`, and `foundational_state`). This block should be generated if it didn't exist, or be the existing one if it did.
    Your output for SUCCESS MUST strictly follow this JSON structure: `{{"path": [], "manifestation": {{"essence": "", "primary_constituents": [], "governing_framework": [], "driving_forces_and_potential": [], "foundational_state": ""}}}}`. No additional commentary, explanations, or wrapping text outside this JSON object.
*   **REJECT (Entity Not Found):** If the target entity cannot be found anywhere in the `primary_constituents` of the world or any of its `manifestation` blocks (by its name or by traversing the semantic path), you MUST output a **valid JSON object** with the following structure:
    `{{"status": "reject", "reason": "Information about [requested entity/concept] is not found in the provided data. This might be because the entity is not part of the world or not detailed at the current level of description."}}`
    Replace `[requested entity/concept]` with the exact user query (e.g., "Light-Emitting Element of Desk Lamp").

**Process for Manifestation (Internal Logic for LLM):**

**CRITICAL PRE-PROCESSING RULE: IMMEDIATE MANIFESTATION DETERMINATION**
If the target entity's JSON object is successfully located at any level within the world's hierarchy (i.e., its JSON object exists and is identified by the `path`), you **MUST immediately proceed to generate or retrieve its `manifestation` block as described in step 2. You MUST NOT reject a query merely because the located entity does not yet possess its own `manifestation` block. The primary purpose of this agent is to *create* or *unfold* that manifestation if absent, or return it if present. There is no ambiguity on this point.**

1.  **Locate Target Entity and Trace Path:** Parse the semantic path provided by the user. Recursively search through the `primary_constituents` arrays (at the top level and within any existing `manifestation` blocks) to find the entity that matches the last part of the path, ensuring the full path is consistent. **During this search, you MUST meticulously construct the exact, verified semantic path (an array of entity names) leading to the located target entity. This path MUST solely reflect the actual hierarchy traversed within the provided world JSON, not any external or imagined context.**
    *   Example: For "Light-Emiting Element of Desk Lamp", first find "Desk Lamp" at the top level, then within its `manifestation`'s `primary_constituents`, find "Light Source", and within *its* `manifestation`'s `primary_constituents`, locate "Light-Emitting Element".
    *   **CRITICAL PATH ACCURACY:** The generated `path` in the output MUST be an **absolute, verifiable trace** of the actual `name` values of the entities from the world's root down to the located entity. **DO NOT invent, alter, or hallucinate path elements.** For example, if a "Component X" is found within "Assembly Y", the path MUST be `["Assembly Y", "Component X"]`.
    *   **Clarification for Nested Entities (Manifestation Ownership):** If the target entity (e.g., "Component X") is found as a `primary_constituent` *within the manifestation of a parent entity* (e.g., "Assembly Y"), and "Component X" itself does not have an *explicit `manifestation` key directly attached to its own JSON object*, you **MUST generate a new `manifestation` block solely for "Component X"**. **Under no circumstances should the parent's manifestation be returned when a child entity is the target.** This ensures each entity receives its unique, deepened manifestation.

2.  **Generate `manifestation` Block for the Located Entity:**
    *   Once the target entity's JSON object is located (e.g., the JSON object of the entity itself), if it does not already contain a key named `"manifestation"`, you MUST **generate a new JSON object for this manifestation**.
    *   If the target entity **already contains a `"manifestation"` key**, retrieve its existing value. The goal is to either generate a new one or return the existing one if it's already there (signaling to the script that no change is needed, but the manifestation is present).
    *   **CRITICAL RULE: Manifestation Ownership and Scope**
        *   The `manifestation` block returned or generated **MUST belong exclusively to the specific entity identified by the `path`**.
        *   **NEVER return a parent entity's `manifestation` block as the `manifestation` for a child entity.** If `entity_A` has a `manifestation` (e.g., "Urban Core") and `entity_B` (e.g., "Skyscraper Complexes") is a `primary_constituents` *within* `entity_A`'s `manifestation`, and `entity_B` is queried, you **MUST generate** a *new* `manifestation` for `entity_B` unless `entity_B` itself *already has* its own directly attached `manifestation` block. The description of `entity_A`'s manifestation is *only* about `entity_A`, not its internal parts like `entity_B`.
    *   If generating, the `manifestation` block MUST be a JSON object containing the following five top-level keys. **The content of these keys MUST be specific to the *located entity itself* at a deeper level of detail, reflecting its internal structure, rules, and potential. Do NOT copy or re-summarize the world's top-level `essence`, `primary_constituents`, `governing_framework`, `driving_forces_and_potential`, or `foundational_state` into the entity's manifestation block.**
        *   `"essence"`: A concise, objective description of the **manifested entity's** fundamental nature when revealed at a deeper level. **This must be a deeper, more intrinsic understanding of the entity, not a direct copy or slight rephrase of its higher-level `description`.**
        *   `"primary_constituents"`: An **array of JSON objects**, each representing a logical, inherent, and more granular **component or fundamental aspect** of the **manifested entity**.
            *   **STRICT NEGATIVE CONSTRAINT:** This array **MUST NEVER** include:
                *   Forces (e.g., 'gravity', 'electromagnetic force')
                *   Properties (e.g., 'Surface Tension', 'viscosity', 'density')
                *   Laws or principles (e.g., 'thermodynamics', 'Newton's laws')
                *   External phenomena or effects *applied to* the entity (e.g., 'Quantum Vacuum Fluctuations', 'radiation exposure', 'ambient temperature', 'microgravity').
                *   These belong in `governing_framework` or `driving_forces_and_potential`.
            *   **RULE FOR INCLUSION:** Constituents MUST be **internal structures, tangible subsystems, or inherent physical parts** of the entity itself. Think of them as the components you would find if you were to "disassemble" the entity.
            *   **CRITICAL RULE: Aggregation & Representative Instance for Multiples:** When the manifested entity is composed of a multitude of **identical or near-identical sub-entities** that are so numerous as to make individual listing impractical (e.g., individual atoms, molecules, photons, grains of sand, identical structural units like bricks or windows in a building), you **MUST NOT list them individually**. Instead, you **MUST represent these constituents using a two-part approach** in the `primary_constituents` array:
                a.  **A single, representative instance:** Include one `primary_constituent` that describes the fundamental properties and nature of a *typical individual unit* from that multitude. The `name` should reflect this singular, representative nature (e.g., "Photon", "Particle", "Molecule X"). **This representative instance MUST NOT have a numerical suffix.**
                b.  **The collective remainder:** Include a second `primary_constituent` that aggregates all *other* identical units into a collective description. The `name` should reflect its collective nature (e.g., "Remaining Photons", "Bulk Material", "Aggregated Entities").
                This pattern ensures that the system allows for the conceptual understanding of the individual unit's properties, while preventing impractical or infinite enumeration of the total quantity and preserving conceptual integrity.
            *   **Directive for Precise, Identical Components:** When an entity is fundamentally defined by a **small, exact number of identical components** (e.g., two, three, or four identical sub-components), and their individual enumeration is critical for accurate structural representation, you **MUST list each such component individually**. Append a numerical suffix to its `name` (e.g., "Component A 1", "Component A 2") to clearly indicate each distinct instance. For example, if an 'Assembly' is composed of two 'Fasteners' and one 'Housing', the `primary_constituents` **MUST include**: "Fastener 1", "Fastener 2", and "Housing". This ensures strict adherence to the entity's precise composition and count.
            *   **Crucial Directive for Chemical/Atomic Entities:** When the manifested entity is a **molecule or an atomic structure**, its `primary_constituents` **MUST be its constituent atoms**, individually enumerated with numerical suffixes if there are multiple identical atoms. You **MUST NOT list subatomic particles (protons, neutrons, electrons) unless the entity itself is a subatomic particle, or the context is explicitly nuclear/quantum physics at its foundational level**. For example, for a Carbon Dioxide Molecule (CO₂), the `primary_constituents` **MUST include**: "Oxygen Atom 1", "Oxygen Atom 2", and "Carbon Atom". This ensures the correct level of granularity and strict adherence to chemical composition.
            *   **Strict Composition Rule for Molecules:** When manifesting a molecule, the `primary_constituents` list **MUST precisely reflect the complete chemical formula and composition** of that molecule. This means including *all* types of atoms present and their correct quantities. For instance, for H₂O, ensure both Hydrogen atoms and the Oxygen atom are present. For CO₂, both Oxygen atoms and the Carbon atom must be present.
            *   Each constituent object MUST only have `"name"` and `"description"` fields.
            *   Avoid overly abstract (e.g., "Parts of X") or overly specific constituents at this level; the "Crucial Directive for Chemical/Atomic Entities" and "Strict Composition Rule for Molecules" define the expected granularity for chemical entities.
        *   `"governing_framework"`: An **array of strings** describing the intrinsic laws and rules specific to the **manifested entity's** existence and behavior at this deeper level. These rules **MUST describe the *internal mechanisms, interactions, and specific behaviors* intrinsic to the manifested entity itself**. Do NOT simply re-state general laws or effects that apply to the entity from the world's perspective; focus on *how the entity itself operates* under those laws.
        *   `"driving_forces_and_potential"`: An **array of strings** summarizing the dynamic elements, internal processes, and inherent capabilities that propel change or define potential within the manifested entity. These **MUST represent the *internal dynamics, active processes, and inherent capabilities* that drive change or define potential *within the manifested entity***. Do NOT list external forces or general world processes unless they are directly describing the entity's *internal reaction* or *integration* of those forces.
        *   `"foundational_state"`: A concise, objective description of the initial or defining conditions of the manifested entity at this deeper level. **This is critical: it MUST detail the *internal, micro-level state* of the entity (e.g., internal temperature distribution, precise molecular count, internal pressure, specific energy states, internal composition percentages). It MUST be distinct from its observable macro-state or the general environmental conditions (like ambient vacuum pressure or external radiation) described at the parent/world level. Do NOT copy the world's foundational state or environmental parameters here; describe the *entity's internal state* in that environment.**
3.  **Produce Output:** Output the generated (or retrieved) `manifestation` block and the constructed `path` in the specified SUCCESS JSON format, or the REJECT JSON object if the entity was not found.

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
        options={'num_ctx': win}
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
def create(prompt, model, think):
    return process(prompt=prompt, model=model, system_prompt=CREATE_SYSTEM_PROMPT, think=think, debug=True)


def query(prompt, model, world_json, think, win):
    system_prompt = QUERY_SYSTEM_PROMPT.format(world=world_json)
    return process(prompt=prompt, model=model, system_prompt=system_prompt, think=think, debug=True, win=win)


def navigate(prompt, model, world_json, think, win):
    system_prompt = NAVIGATE_SYSTEM_PROMPT.format(world=world_json)

    # process
    res_json = process(prompt=prompt, model=model, system_prompt=system_prompt, think=think, debug=True, win=win)
    res = json.loads(res_json)

    # reject
    if ('status' in res) and (res['status'] == 'reject'):
        print(f"rejected: {res['reason']}")
        return None

    # insert
    world = json.loads(world_json)
    entity = {'manifestation': world}

    for name in res['path']:
        found = False
        for e in entity['manifestation']['primary_constituents']:
            if e['name'] == name:
                entity = e
                found = True
                break
        if not found:
            print(f'invalid entity: {name}')
            return None

    entity['manifestation'] = res['manifestation']
    return json.dumps(world, indent=2, ensure_ascii=False)


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

    # python reality-gen.py create <prompt> --output <filename> --model <name> --think
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
    create_parser.add_argument('--think', '-t', action='store_true', help='Enable advanced, iterative reasoning for the model to refine outputs. May increase processing time and token usage.')

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

    # python reality-gen.py navigate <prompt> --input <filename> --output <filename> --model <name> --think --win <size>
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
    navigate_parser.add_argument('--think', '-t', action='store_true', help='Enable advanced, iterative reasoning for the model to refine outputs. May increase processing time and token usage.')
    navigate_parser.add_argument(
    '--win',
    '-w',
    type=int,
    default=8192,
    help='Specify the maximum context window size (in tokens) for the model during this operation.'
)

    args = parser.parse_args()

    # main
    res_json = None

    if args.command == 'create':
        world_json = create(prompt=args.prompt, model=args.model, think=args.think)
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

            res_world_json = navigate(prompt=args.prompt, model=args.model, world_json=world_json, think=args.think, win=args.win)
            if res_world_json is None:
                exit()

            meta['world'] = json.loads(res_world_json)
            meta['navigation']['max_depth'] = calc_max_depth(meta['world'])

            res_json = json.dumps(meta, indent=2, ensure_ascii=False)

    if args.output and res_json:
        print(res_json)
        with open(args.output, 'w', encoding='utf-8') as out:
            out.write(res_json)
            out.flush()
