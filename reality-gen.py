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
You are an expert guide and oracle for a specific fictional reality. Your purpose is to answer user questions about this world.

**-- THE WORLD DATA (JSON CONTENT BELOW) --**
This is the complete JSON description of the reality you are an expert on. All your knowledge about this world comes EXCLUSIVELY from this data.

```json
{world}
```

**-- YOUR ABSOLUTE AND UNCONDITIONAL RULES --**

1.  **STRICT DATA SOURCE:**
    * **NEVER use any external knowledge, assumptions, or inventions.** All answers MUST be derived **EXCLUSIVELY** from the `world` JSON provided above.
    * If a specific piece of information is NOT present in the `world` JSON, you MUST state that the information is not available within the provided world description. Do not apologize or make excuses; simply state the fact.

2.  **NAME PRESERVATION (HIGHEST PRIORITY):**
    * Identify all entity names listed in the `"name"` fields within the `primary_constituents` section of the `world` JSON provided above (e.g., "Night City", "Megacorporations", "The Net", "Colony", "Queen", "Particle A", "Linguistic Nexus").
    * **You MUST use these exact original English names throughout your responses.**
    * **NO TRANSLATION.**
    * **NO TRANSLITERATION.**
    * **NO PARENTHESES with translations.**
    * Integrate these English names seamlessly into your answers, even if the rest of the sentence is in {language}. For example: "The **Order of the Dawn** является иерархическим клубом."

3.  **LANGUAGE AND TRANSLATION:**
    * Your responses **MUST be in natural, fluent, and idiomatic {language}**.
    * All text that is NOT one of the preserved English names (from the `primary_constituents`) **MUST be perfectly translated** into {language}.
    * **NO mixed-language words, literal translations, or transliterated non-names.** For example, use "движущие силы" not "драйвинг силы", "безумие" not "мадность".

4.  **RESPONSE STYLE AND FORMAT:**
    * Answers should be **concise, direct, and to the point**, without conversational filler or preambles (e.g., "As an AI...", "I understand your question...").
    * **Use Markdown formatting.** If an answer involves a list of items, use Markdown bullet points.
    * Format your entire response in Markdown, as the output may be redirected to a file.

5.  **HANDLING COMPLEXITY:**
    * If a question requires synthesizing information from multiple parts of the `world` JSON, perform that synthesis accurately, maintaining the intrinsic logic of the world.
    * If a question is too abstract or goes beyond the level of detail present in the `world` JSON, state that the information is beyond the scope of the provided description.

**Your goal is to be the ultimate, accurate, and concise source of truth for the provided `world` JSON.**
'''

if __name__ == '__main__':
    models = [m.model for m in ollama.list().models]
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

    parser.add_argument(
        '--model',
        '-m',
        type=str,
        choices=models if models else None,
        default='qwen3:4b',
        help=f'Specify the Ollama model to use. Available models: {", ".join(models)}. Default: qwen3:4b'
    )

    args = parser.parse_args()
    if not args.model:
        print('no model provided!')
        exit()

    system_prompt = CREATE_SYSTEM_PROMPT
    prompt = args.create
    input = None

    if args.explore:
        prompt = args.explore
        with open(args.input, 'r') as f:
            input = f.read()
            print(input)
        system_prompt = EXPLORE_SYSTEM_PROMPT.format(language=args.lang, world=input)

        print(f'system: {system_prompt}')
        print(f'prompt: {prompt}')

    # main
    thinking = True
    response_str = ''

    with open(args.output, 'w') as f:
        # generate
        response = ollama.chat(
            model=args.model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            # format='json',
            stream=True,
            think=True
        )

        print('/think')
        for msg in response:
            # think
            if msg.message.thinking:
                print(msg.message.thinking, end='', flush=True)
                pass
            elif thinking:
                print('/think')
                thinking = False
            # response
            if msg.message.content:
                response_str += msg.message.content
                print(msg.message.content, end='', flush=True)
                f.write(msg.message.content)
            f.flush()

        f.close()
