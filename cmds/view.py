from discord import Message

from util import analyzer, authors, corpora, memory, parser

def exec(message: Message):
    name = parser.get_arg(message)
    ll = memory.get(name.lower())
    
    if not ll:
        return f'Error: could not find layout `{name}`'    

    author = authors.get_name(ll['user'])

    max_width = max(x['col'] for x in ll['keys'].values()) + 1
    max_height = max(x['row'] for x in ll['keys'].values()) + 1

    matrix = [[' ']*max_width for _ in range(max_height)]
    
    for char, info in ll['keys'].items():
        row = info['row']
        col = info['col']

        matrix[row][col] = char

    for i, row in enumerate(matrix):
        for j, _ in enumerate(row):
            char = matrix[i][j]

            if j == 0:
                matrix[i][j] = '  ' + char
            elif j == 4:
                matrix[i][j] += ' '

    if ll['board'] == 'stagger':
        matrix[1][0] = ' ' + matrix[1][0]
        matrix[2][0] = '  ' + matrix[2][0]
    elif ll['board'] == 'angle':
        matrix[2][0] = ' ' + matrix[2][0]

    data = corpora.trigrams()
    stats = analyzer.trigrams(ll, data)

    matrix_str = '\n'.join(' '.join(x) for x in matrix)

    res = (
        f'```\n'
        f'{ll["name"]} ({author})\n'
        f'{matrix_str}\n'
        f'\n'
        f'{"Alt:":>5} {stats["alternate"]:>6.2%}\n' 
        f'{"Roll:":>5} {stats["roll-in"] + stats["roll-out"]:>6.2%}'
        f'   (In: {stats["roll-in"]:>6.2%} Out: {stats["roll-out"]:>6.2%})\n'
        f'{"One:":>5} {stats["oneh-in"] + stats["oneh-out"]:>6.2%}'
        f'   (In: {stats["oneh-in"]:>6.2%} Out: {stats["oneh-out"]:>6.2%})\n'
        f'{"Red:":>5} {stats["redirect"]:>6.2%}\n'
        '\n'
        f'SFB: {stats["sfb"] / 2:.2%}\n' 
        f'DFB: {stats["dsfb-red"] + stats["dsfb-alt"]:.2%}\n'
        f'```\n'
    )

    return res     

def use():
    return 'view [name]'

def desc():
    return 'see the stats of a layout'