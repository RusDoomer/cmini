from discord import Message

from util import layout, memory, parser

def exec(message: Message):
    name = parser.get_arg(message)
    ll = memory.find(name.lower())
    
    if not ll:
        return f'Error: could not find layout `{name}`'    

    return layout.to_string(ll)     

def use():
    return 'view [name]'

def desc():
    return 'see the stats of a layout'