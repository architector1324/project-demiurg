import sys
import json
import random
import datetime
import argparse

import demi_core


# main
if __name__ == '__main__':
    LLMProcessor = demi_core.OllamaProcessor
    # LLMProcessor = demi_core.OpenAIProcessor

    models = LLMProcessor.get_models()
    if not models:
        print('no models provided!')
        sys.exit()

    # parse arguments
    parser = argparse.ArgumentParser(
        description='Semantic engine for generating internally coherent fictional realities - from quantum voids to dreaming cities, using prompt-driven LLM world synthesis.'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # demi create <prompt> --output <filename> --core <name>
    create_parser = subparsers.add_parser('create', help='Generate a completely new, high-level reality from a short text prompt.')
    create_parser.add_argument('prompt', type=str, help='Short text prompt for reality generation.')
    create_parser.add_argument('--output', '-o', type=str, help='Specify an output file to save the generated reality (e.g., JSON).')
    create_parser.add_argument(
        '--core',
        '-c',
        type=str,
        choices=models if models else None,
        help=f'Specify the Ollama model to use as semantic core. Available models: {", ".join(models)}'
    )
    create_parser.add_argument(
        '--seed',
        '-s',
        type=int,
        default=random.randint(0, 2**32 - 1),
        help='Specify a numerical seed for reproducible reality generation. If not provided, a random seed will be used.'
    )
    create_parser.add_argument(
        '--debug',
        '-d',
        default=False,
        action='store_true',
        help='Enable debug mode to show verbose output and internal workings.'
    )

    # demi query <prompt> --input <filename> --output <filename> --core <name> --win <size>
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
        '--core',
        '-c',
        type=str,
        choices=models if models else None,
        help=f'Specify the Ollama model to use as semantic core. Available models: {", ".join(models)}'
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
    query_parser.add_argument(
        '--debug',
        '-d',
        default=False,
        action='store_true',
        help='Enable debug mode to show verbose output and internal workings.'
    )

    # demi navigate <prompt> --input <filename> --output <filename> --core <name> --win <size>
    navigate_parser = subparsers.add_parser('navigate', help='Dive into a specific constituent or subsystem of an existing world and semantically elaborate its details recursively.')
    navigate_parser.add_argument('prompt', type=str, help='Prompt to guide the navigation and elaboration.')
    navigate_parser.add_argument('--input', '-i', type=str, default='world.json', help='Specify an input file containing an existing reality.')
    navigate_parser.add_argument('--output', '-o', type=str, help='Specify an output file to save the explored reality (e.g., JSON).')
    navigate_parser.add_argument(
        '--win',
        '-w',
        type=int,
        default=6144,
        help='Specify the maximum context window size (in tokens) for the model during this operation.'
    )
    navigate_parser.add_argument(
        '--core',
        '-c',
        type=str,
        choices=models if models else None,
        help=f'Specify the Ollama model to use as semantic core. Available models: {", ".join(models)}'
    )
    navigate_parser.add_argument(
        '--debug',
        '-d',
        default=False,
        action='store_true',
        help='Enable debug mode to show verbose output and internal workings.'
    )

    args = parser.parse_args()

    # main
    result = None

    if args.command == 'create':
        llm_processor = LLMProcessor(core=args.core, world=None, seed=args.seed, think=True, debug=args.debug)
        world = llm_processor.create(prompt=args.prompt)

        res = {
            'discovery': {
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'core': args.core,
                'prompt': args.prompt,
                'seed': args.seed,
            },
            'navigation': {
                'max_depth': 0,
                'history': []
            },
            'world': world
        }
        result = json.dumps(res, indent=2, ensure_ascii=False)

    elif args.command == 'query':
        with open(args.input, 'r') as f:
            meta = json.loads(f.read())
            core = args.core if args.core else meta['discovery']['core']
            llm_processor = LLMProcessor(core=core , world=meta['world'], seed=meta['discovery']['seed'], think=args.think, debug=args.debug)
            result = llm_processor.query(args.prompt, win=args.win)

    elif args.command == 'navigate':
        with open(args.input, 'r') as f:
            meta = json.loads(f.read())
            core = args.core if args.core else meta['discovery']['core']
            meta['navigation']['history'].append({
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'core': core,
                'prompt': args.prompt
            })

            llm_processor = LLMProcessor(core=core, world=meta['world'], seed=meta['discovery']['seed'], think=True, debug=args.debug)

            world = llm_processor.navigate(prompt=args.prompt, win=args.win)
            if world is None:
                sys.exit()

            meta['world'] = world
            meta['navigation']['max_depth'] = llm_processor.calc_max_depth()

            result = json.dumps(meta, indent=2, ensure_ascii=False)

    # ourput
    if args.output and result:
        print(result)
        with open(args.output, 'w', encoding='utf-8') as out:
            out.write(result)
            out.flush()
