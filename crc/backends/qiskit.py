import ast
import astor
from copy import deepcopy, copy
from tatsu.walkers import NodeWalker

MODULE_TEMPLATE = '''
from qiskit import QuantumProgram
'''

FUNCTION_TEMPLATE = '''
class {circuit_name}:
  
  def __call__(self, **kwargs):
    _qp_ = self.program
    _qc_ = _qp_.get_circuit('{circuit_name}')
    {in_reg_name} = _qc_.get_qregs()['{in_reg_name}']
    {out_reg_name} = _qc_.get_cregs()['{out_reg_name}']
    for i in range({out_size}):
      _qc_.measure({in_reg_name}[i], {out_reg_name}[i])
    _result_ = _qp_.execute('{circuit_name}', **kwargs)
    return _result_.get_data('{circuit_name}')

  @property
  def program(self):
    _qp_ = QuantumProgram()
    {in_reg_name} = _qp_.create_quantum_register('{in_reg_name}',{in_size})
    {out_reg_name} = _qp_.create_classical_register('{out_reg_name}',{out_size})
    _qc_ = _qp_.create_circuit('{circuit_name}',[{in_reg_name}],[{out_reg_name}])
    # Contents
    return _qp_

{circuit_name} = {circuit_name}()
'''

class Generator(NodeWalker):
  """Tatsu walker for transforming the CRC AST to a Python3 + qiskit AST."""

  def walk_object(self, node):
    return node

  def walk_str(self, node):
    return ast.Str(node)

  def walk_int(self, node):
    return ast.Num(node)

  def walk_float(self, node):
    return ast.Num(node)

  def walk_Board(self, node):
    module = ast.parse(MODULE_TEMPLATE)
    for circuit in node.circuits:
      module.body.extend(self.walk(circuit))

    return module

  def walk_Circuit(self, node):
    statements = [ self.walk(w) for w in node.wirings ]
    circuit = ast.parse(FUNCTION_TEMPLATE.format(
      circuit_name=node.name,
      in_size=node.signature.input.size,
      out_size=node.signature.output.size,
      in_reg_name=node.signature.input.name,
      out_reg_name=node.signature.output.name
    )).body
    _circuit_method = circuit[0].body[1]
    _circuit_method_body = _circuit_method.body
    _circuit_method.body = [
      *(_circuit_method_body[:-1]),
      *statements,
      *(_circuit_method_body[-1:])
    ]
    return circuit 

  def walk_Wiring(self, node):
    args = [
      *(self.walk(expr) for expr in node.left),
      *(self.walk(expr) for expr in node.right)
    ]
    return self._op(node.op, args)

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