import ollama
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
* **Scientific Accuracy & Terminology:** If the user's prompt implies a scientifically plausible or real-world concept (e.g., 'Solar System', 'Atom Structure'), prioritize known scientific facts, principles, and commonly accepted terminology (e.g., 'proton', 'electron', 'galaxy', 'planet'), unless specifically instructed to fictionalize them.

**Output Structure (JSON Object with top-level keys):**

1. "world_essence": Concise summary of the world's fundamental concept.
2. "primary_constituents": An **array of JSON objects** (each with `"name"` and `"description"`).
3. "governing_framework": An **array of strings** describing fundamental rules/systems.
4. "driving_forces_and_potential": An **array of strings** summarizing core interactions/forces that drive change.
5. "foundational_state": Concise description of key initial conditions/defining aspects.

**Constraints:**
* Descriptions must be **clear, focused, and high-level**.
* Output **MUST be valid JSON**.
* No additional commentary outside the JSON.
* **Exclude Real-World References: Do NOT include names of real-world companies, individuals, products, or specific geographical locations (unless they are a fundamental part of the world's concept, like 'Earth' for a world set on Earth, and explicitly requested). **When describing scientifically plausible or real-world concepts, use ONLY commonly accepted scientific and astronomical terminology for all primary constituents and descriptions, unless explicitly instructed to fictionalize them.**
'''

EXPLORE_SYSTEM_PROMPT = '''
You are an expert guide and oracle for a fictional world, provide well structured output in {language}. All your knowledge about this world comes EXCLUSIVELY from the provided JSON data.

**World Data**:
```json
{world}
```

**World Data Structure (JSON Object with top-level keys):**
For your reference, here is a breakdown of the JSON structure:
1.  "world_essence": Concise summary of the world's fundamental concept.
2.  "primary_constituents": An **array of JSON objects** (each with `"name"` and `"description"`). These are the core entities, elements, or principles that form the world's very fabric.
3.  "governing_framework": An **array of strings** describing the intrinsic laws and rules that dictate how the world functions.
4.  "driving_forces_and_potential": An **array of strings** summarizing the dynamic elements that propel change, evolution, and narrative possibilities.
5.  "foundational_state": Concise description of the initial conditions and primordial state from which the reality emerges.

**Your Rules:**
1.  **Data Source:** Only use information from the JSON data. Don't invent, infer, or make assumptions. If information isn't in the JSON, state that it's not available.
2.  **Formatting:**
    * Be concise and direct.
    * **Keep names and entities from World Data** in the **English** language.
    * Use Markdown.

Your goal is to be an accurate and concise source of truth for the provided world data.
'''

if __name__ == '__main__':
    models = [m.model.replace(':latest', '') for m in ollama.list().models]
    if not models:
        print('no models provided!')
        exit()

    # parse arguments
    parser = argparse.ArgumentParser(description='Semantic engine for generating internally coherent fictional realities - from quantum voids to dreaming cities, using prompt-driven LLM world synthesis.')

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--create', '-c', type=str, help='Generate a completely new, high-level reality from a short text prompt.')
    action_group.add_argument('--explore', '-e', type=str, help='Investigate an existing reality with a specific query (requires --input).')
    parser.add_argument('--output', '-o',type=str, help='Specify an output file to save the generated or explored reality (e.g., JSON).')
    parser.add_argument('--input', '-i', type=str, default='world.json', help='Specify an input file containing an existing reality (required for --explore).')
    parser.add_argument('--lang', '-l', type=str, default='en', help='Specify the language for reality generation/exploration. Default: "en"')
    parser.add_argument('--think', '-t', action='store_true', help='Specify should model use thinking or not.')

    parser.add_argument(
        '--model',
        '-m',
        type=str,
        choices=models if models else None,
        help=f'Specify the Ollama model to use. Available models: {", ".join(models)}'
    )

    args = parser.parse_args()

    system_prompt = CREATE_SYSTEM_PROMPT
    prompt = args.create
    input = None

    if args.explore:
        prompt = args.explore
        with open(args.input, 'r') as f:
            input = f.read()
            # print(input)
        system_prompt = EXPLORE_SYSTEM_PROMPT.format(language=args.lang, world=input)

    # main
    thinking = True
    response_str = ''

    out = open(args.output, 'w') if args.output else None

    # generate
    response = ollama.chat(
        model=args.model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        # format='json',
        stream=True,
        think=args.think
    )

    if args.think:
        print('/think')

    for msg in response:
        # think
        if msg.message.thinking:
            print(msg.message.thinking, end='', flush=True)
            pass
        elif thinking:
            if args.think:
                print('/think')
            thinking = False
        # response
        if msg.message.content:
            response_str += msg.message.content
            print(msg.message.content, end='', flush=True)
            if out:
                out.write(msg.message.content)
        if out:
            out.flush()

    if out:
        out.close()
