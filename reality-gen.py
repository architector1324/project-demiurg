import os
import ollama


GEN_SYSTEM_PROMPT = '''
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

INFO_SYSTEM_PROMPT = '''
You are an expert storyteller and world summarizer. Your task is to create a detailed, well-structured summary of the given JSON world description in natural, fluent, and idiomatic {language}.

**-- ABSOLUTE, UNCONDITIONAL, AND HIGHEST PRIORITY RULE --**
**DO NOT TRANSLATE ANY NAMES FROM 'PRIMARY_CONSTITUENTS'.**
From the 'primary_constituents' section of the JSON, identify all "name" fields (e.g., "Order of the Dawn", "Arcane Essence", "Shadow Syndicate", "Spirit Lanes", "Eldertree"). **You MUST use these exact English names throughout the summary.**
* **NO EXCEPTIONS.**
* **NO TRANSLATIONS.**
* **NO TRANSLITERATIONS.**
* **NO PARENTHESES with translations.**
* Integrate them seamlessly into the {language} text *as is*. For example, use "орден Order of the Dawn" or "сущность Arcane Essence".

**-- RULE FOR GENERIC TERMS AND CONCEPTS --**
If a generic term (e.g., "knights", "shadowy forces") is used in 'world_essence' or other sections, and it **directly corresponds** to one of the specific English names from 'primary_constituents' (e.g., "Order of the Dawn", "Shadow Syndicate"), you **MUST use that specific English name**. Do NOT use a translated generic term (e.g., do not say "рыцари" if referring to "Order of the Dawn").

**-- RULE FOR ALL OTHER TEXT --**
All other text (descriptions, verbs, adjectives, general nouns that are NOT the exact English names from 'primary_constituents') **MUST be perfectly translated into natural, idiomatic {language}**.
* **NO mixed-language words.**
* **NO literal translations that sound unnatural.**
* **NO transliterated non-names.**
* Specifically, if a concept like "The Veil" from the original JSON is mentioned, and it refers to an entity like "Aetheric Veil", **always use the full English name, "Aetheric Veil"**, not a translated or invented term like "Ворота".
* Example: Use "движущие силы" instead of "драйвинг силы", "цель" instead of "эйм", "безумие" instead of "мадностью".

Organize the summary into clear sections with headings such as:

- Core essence of the world
- Main entities or characters
- Fundamental laws and principles
- Driving forces or conflicts
- Initial or foundational state

Use accessible language that sparks curiosity and is easy to understand for a general audience in {language}. Avoid overly technical jargon, but do include important details to help the reader fully grasp the world’s nature.

Format the summary using Markdown syntax: use headings (###), bullet points, and paragraphs to make the text easy to read and visually appealing.

Aim for a rich and engaging description rather than just a brief overview.
'''

# main
model = 'qwen3:4b'

# test_prompts_ru = [
#     # Исторически первые тестовые промпты
#     'Две частицы в вакууме',
#     'Волшебный мир с рыцарями, магией и злодеями',
#     'Язык, через который общаются разные измерения энергии',
#     'Город, построенный внутри голов спящих титанов',

#     # Категория 1: Известные франшизы
#     'Мир Cyberpunk 2077',
#     'Мир The Legend of Zelda: Breath of the Wild',
#     'Мир The Elder Scrolls V: Skyrim',
#     'Мир Minecraft',

#     # Категория 2: Разнообразные жанры и масштабы
#     'Одинокий детектив расследует преступление в дождливом мегаполисе, управляемом мафией и коррумпированными политиками.',
#     'Маленькая деревня, где жители живут в гармонии с природой и магией, а главные проблемы - это поиск пропавшей кошки или лучший рецепт пирога.',
#     'Выжженные пустоши после падения цивилизации, где группы выживших борются за воду и ресурсы, а правосудие вершат немногочисленные странники на заржавевших мотоциклах.',
#     'Галактическая империя на грани краха, где последние герои пытаются предотвратить межзвездную войну и пробуждение древней угрозы, используя артефакты забытых цивилизаций.',
#     'Реальность, состоящая только из одной комнаты',
#     'Муравейник',
#     'Наша Солнечная система',
#     'Устройство атома',

#     # Категория 3/4: Чисто абстрактные и метафизические миры
#     'Абстрактное пространство, где время и пространство меняют свою природу в зависимости от мыслей наблюдателя',
#     'Реальность, построенная на концепции бесконечного фрактала, где каждый элемент повторяется в масштабе',
#     'Мир, где эмоции материализуются в физические объекты, влияя на окружающую среду',
#     'Концептуальное измерение, в котором существа существуют как чистая информация и взаимодействуют через алгоритмы',
#     'Параллельная вселенная, основанная на музыкальных гармониях и ритмах, где музыка формирует физические законы',
#     'Город, существующий одновременно в нескольких измерениях, переплетённых между собой, создавая многослойную реальность',
#     'Виртуальная реальность, которая сама учится и развивается, формируя новые правила и структуры без участия человека',
#     'Мир, состоящий только из чисел и их взаимоотношений.',
#     'Реальность, где само понятие "наличия" является переменной, и объекты могут существовать или не существовать в зависимости от уровня "актуализации".',
# ]

test_prompts = [
    # Historically first test prompts
    # 'Two particles in a vacuum',
    'Magical world with knights, magic, and villains',
    # 'Language through which different energy dimensions communicate',
    # 'City built inside the heads of sleeping titans',

    # # Category 1: Known Franchises
    # 'World of Cyberpunk 2077',
    # 'World of The Legend of Zelda: Breath of the Wild',
    # 'World of The Elder Scrolls V: Skyrim',
    # 'World of Minecraft',

    # # Category 2: Diverse Genres and Scales
    # 'Lone detective investigates a crime in a rainy megacity ruled by the mafia and corrupt politicians.',
    # 'Small village where inhabitants live in harmony with nature and magic, and the main problems are finding a lost cat or the best pie recipe.',
    # 'Scorched wastelands after the fall of civilization, where groups of survivors fight for water and resources, and justice is served by a few wanderers on rusty motorcycles.',
    # 'Galactic empire on the verge of collapse, where the last heroes try to prevent an interstellar war and the awakening of an ancient threat, using artifacts of forgotten civilizations.',
    # 'Reality consisting of only one room',
    # 'Ant colony',
    # 'Our Solar System',
    # 'The structure of an atom',

    # # Category 3/4: Purely Abstract and Metaphysical Worlds
    # 'Abstract space where time and space change their nature depending on the observer\'s thoughts',
    # 'Reality built on the concept of an infinite fractal, where every element repeats itself at scale',
    # 'World where emotions materialize into physical objects, affecting the environment',
    # 'Conceptual dimension in which beings exist as pure information and interact through algorithms',
    # 'Parallel universe based on musical harmonies and rhythms, where music forms the physical laws',
    # 'City existing simultaneously in multiple interwoven dimensions, creating a multilayered reality',
    # 'Virtual reality that learns and evolves on its own, forming new rules and structures without human intervention',
    # 'World consisting only of numbers and their relationships.',
    # 'Reality where the very concept of "presence" is a variable, and objects can exist or not exist depending on their level of "actualization".',
]

for prompt in test_prompts:
    thinking = True
    response_str = ''

    os.mkdir(f'./examples/{prompt}')

    out = open(f'./examples/{prompt}/world.json', 'w')
    out_think = open(f'./examples/{prompt}/think.txt', 'w')
    out_info = open(f'./examples/{prompt}/info.md', 'w')

    # generate
    response = ollama.chat(
        model=model,
        messages=[
            {'role': 'system', 'content': GEN_SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt}
        ],
        # format='json',
        stream=True,
        think=True
    )

    # print('/think')
    for msg in response:
        # think
        if msg.message.thinking:
            # print(msg.message.thinking, end='', flush=True)
            out_think.write(msg.message.thinking)
            pass
        elif thinking:
            # print('/think')
            thinking = False
        # response
        if msg.message.content:
            response_str += msg.message.content
            # print(msg.message.content, end='', flush=True)
            out.write(msg.message.content)
        out.flush()
        out_think.flush()

    # print()
    out_think.write('\n')

    out.flush()
    out_think.flush()

    out.close()

    # summarize
    response = ollama.chat(
        model=model,
        messages=[
            {'role': 'system', 'content': INFO_SYSTEM_PROMPT.format(language='Russian')},
            {'role': 'user', 'content': response_str}
        ],
        # format='json',
        stream=True,
        think=True
    )

    for msg in response:
        # think
        if msg.message.thinking:
            # print(msg.message.thinking, end='', flush=True)
            out_think.write(msg.message.thinking)
            pass
        elif thinking:
            # print('/think')
            thinking = False
        # response
        if msg.message.content:
            response_str += msg.message.content
            # print(msg.message.content, end='', flush=True)
            out_info.write(msg.message.content)
        out_info.flush()
        out_think.flush()

    out_info.flush()
    out_think.flush()

    out_think.close()
    out_info.close()

# parse world
# world = json.loads(response_str)
# print(world)
