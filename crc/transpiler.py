import ast
import tatsu

GRAMMAR = '''
    @@grammar::Calc
    @@whitespace::/[\t ]*/

    start::Board = { newline } circuits:{ circuit } { newline }$;

    circuit::Circuit =
      'crc' name:identifier signature:spec ':' { newline }+
      wirings:{ wiring } 'end' { newline };

    spec::Spec = input:input '->' output:output ;

    input = register ;

    output = register ;

    register::TRegister = name:identifier '[' size:int ']' ;

    wiring::Wiring =
        '-' left:{ expression }*
        hint op:identifier hint
        right:{ expression }* { eos }+ ;

    eos = | newline | ';' ;

    newline = {['\\u000C'] ['\\r'] '\\n'}+ ;

    hint = /[<>{}:]+/ ;

    expression =
        | wire
        | float
        ;

    wire::Wire = name:identifier index:int ;

    int::int = /\d+/ ;

    float::float = /\d+(\.\d+)?/ ;

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