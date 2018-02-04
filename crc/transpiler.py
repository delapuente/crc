import ast
import tatsu

GRAMMAR = '''
    @@grammar::Calc

    start::Board = circuits:{ circuit } $ ;

    circuit::Circuit =
      'crc' name:identifier signature:spec ':' wirings:{ wiring } 'end' ;

    spec::Spec = input:input '->' output:output ;

    input = register ;

    output = register ;

    register::TRegister = name:identifier '[' size:number ']' ;

    wiring::Wiring = target:wire '=' source:unit ';' ;

    unit =
         | binary
         | monary
         ;

    binary::BinaryUnit = first:wire '!' second:wire ;

    monary::MonaryUnit = op:/[\/]/ first:wire ;

    wire::Wire = name:identifier index:number ;

    number::int = /\d+/ ;

    identifier = /[_$a-zA-Z]+/ ;
'''

def translate(source):
    from .backends.qiskit import Generator as QiskitGen

    model = tatsu.compile(GRAMMAR, asmodel=True)
    crc_ast = model.parse(source)
    return ast.fix_missing_locations(QiskitGen().walk(crc_ast))

def translate_file(path):
    import os
    import astor

    with open(os.path.abspath(path)) as f:
        return astor.to_source(translate(f.read()))