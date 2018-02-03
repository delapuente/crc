import ast
import astor
from copy import deepcopy, copy
from tatsu.walkers import NodeWalker

MODULE_TEMPLATE = '''
from qiskit import QuantumProgram
'''

FUNCTION_TEMPLATE = '''
def {circuit_name}(**kwargs):
  _qp_ = QuantumProgram()
  {in_reg_name} = _qp_.create_quantum_register('{in_reg_name}',{in_size})
  {out_reg_name} = _qp_.create_classical_register('{out_reg_name}',{out_size})
  _qc_ = _qp_.create_circuit('{circuit_name}',[{in_reg_name}],[{out_reg_name}])
  # Content
  for i in range(len({out_reg_name})):
    _qc_.measure({in_reg_name}[i], {out_reg_name}[i])
  _result_ = _qp_.execute('{circuit_name}', **kwargs)
  return _result_.get_data('{circuit_name}')
'''

class Generator(NodeWalker):

  def walk_object(self, node):
    return node

  def walk_str(self, node):
    return ast.Str(node)

  def walk_int(self, node):
    return ast.Num(node)

  def walk_Board(self, node):
    module = ast.parse(MODULE_TEMPLATE)
    module.body += [ self.walk(c) for c in node.circuits ]
    return module

  def walk_Circuit(self, node):
    statements = [ self.walk(w) for w in node.wirings ]
    fn = ast.parse(FUNCTION_TEMPLATE.format(
      circuit_name=node.name,
      in_size=node.signature.input.size,
      out_size=node.signature.output.size,
      in_reg_name=node.signature.input.name,
      out_reg_name=node.signature.output.name
    )).body[0]
    fn.body = [*(fn.body[:4]), *statements, *(fn.body[4:])]
    return ast.parse(fn) 

  def walk_Wiring(self, node):
    return self.walk(node.source)

  def walk_MonaryUnit(self, node):
    return self._op('h', [self.walk(node.first)])

  def walk_BinaryUnit(self, node):
    return self._op('cx', [self.walk(node.first), self.walk(node.second)])

  def walk_Wire(self, node):
    from ast import Subscript, Name, Load, Index
    return Subscript(
      value=Name(id=node.name, ctx=Load()),
      slice=Index(value=self.walk(node.index)), ctx=Load()
    )

  def _op(self, opname, args):
    from ast import Expr, Attribute, Call, Name, Load
    return Expr(
      value=Call(
        func=Attribute(
          value=Name(id='_qc_', ctx=Load()),
          attr=opname,
          ctx=Load()
        ),
        args=args,
        keywords=[]
      )
    )