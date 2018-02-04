
CRC
===

CRC is an experimental programming language for creating quantum circuits. CRC resembles `QASM`_ although it is totally unrelated. Contrary to QASM, the goal for CRC is to evolve into a high level language.

.. _QASM: https://github.com/QISKit/openqasm

CRC is also a Python 3.5+ for importing CRC like any other Python module. After importing ``crc``, any module refering to a ``*.crc`` file is compiled on the fly.

Installing CRC
--------------

Use ``pip install -e`` along the ``git`` URL to install from the repository. It is too soon to uploaded to PyPI_ yet::

    $ pip install -e git+git@github.com:delapuente/crc.git#egg=crc 

.. _PyPI: https://pypi.python.org/pypi

Using a circuit
---------------

Prerequisites
~~~~~~~~~~~~~

The compiled Python imports and uses Qiskit_ to perform the quantum operations so you need to satisfy this dependency::
 
     $ pip install qiskit

.. _Qiskit: https://www.qiskit.org/

Importing circuits
~~~~~~~~~~~~~~~~~~

Consider the following file tree::

    .
    ├── circuits.crc
    └── main.py

To enable on-the-fly compilation, start importing the `crc` module. Then import the ``.crc`` modules you want and the circuits will be available as callables::

    # main.py
    import crc
    from circuits import bell
    bell()
    
    # circuits.crc
    crc bell q[2] -> c[2]:
      - :h > q
      - q > cx > q1
    end

Interfacing with Qiskit
~~~~~~~~~~~~~~~~~~~~~~~

A CRC circuit returns a Qiskit |QuantumProgram|_ instance when accessing the ``program`` property. Two successive access to ``program`` will return two different ``QuantumProgram`` instances with the same internal configuration. The programs holds only one circuit with the same name of the callable object::

    import crc
    from circuits import bell
    bell.program is not bell.program # different objects
    circuit = bell.program.get_circuit('bell')
    
.. |QuantumProgram| replace:: ``QuantumProgram``
.. _QuantumProgram: https://www.qiskit.org/documentation/_autodoc/qiskit.QuantumProgram.html

Executing the program performs a measurement on as many qubits as the size of the classical registers and displays the results immediately. To execute the program you call the circuit::

    bell()
    
To configure the execution of the program, the parameters of the |QuantumProgram.execute()|_ method are available::

    bell(seed=1)

.. |QuantumProgram.execute()| replace:: ``QuantumProgram.execute()``
.. _QuantumProgram.execute(): https://www.qiskit.org/documentation/_autodoc/qiskit.QuantumProgram.html#qiskit.QuantumProgram.execute

Writing a circuit
-----------------

A circuit consists into a name and a quantum and classic registers of a given size::

    crc bell q[2] -> c[2]
      # Here you set the quantum gates
    end
    
This defines the circuit ``bell`` with the quantum register ``q`` and the classical register ``c``, both of size 2.

Writing a quantum program consists in altering the qubits with quantum gates. Gates are named, examples are |h|_ (Hadamard) and |cx|_ (CNOT), and act on one or more qubits. The most straightforward way of apply a gate to a set of qubits is to use the function-like syntax::

    crc bell q[2] -> c[2]
      - :h: q0
      - :cx: q0 q1
    end

.. |h| replace:: ``h``
.. _h: https://en.wikipedia.org/wiki/Quantum_gate#Hadamard_(H)_gate

.. |cx| replace:: ``cx``
.. _cx: https://en.wikipedia.org/wiki/Quantum_gate#Controlled_(cX_cY_cZ)_gates

The line mark `-` introduces the circuit alteration. And the colons `:` encloses the gate name. List of parameters are separated by spaces and they are always passed from left to right. Enclosing the gate name between colons allow straighforward infix notation::

    crc bell q[2] -> c[2]
      - :h: q0
      - q0 :cx: q1
    end
    
The colons are called hints; hints have no meaning but they are intended to remind the developer about the nature of the gate and the relationship between its parameters. Any combination of ``<``, ``>``, ``{``, ``}`` and ``:`` is a valid hint::

    crc bell q[2] -> c[2]
      - :h > q0
      - q0 > cx > q1
    end
    
*Hints are an exerimental feature and can dissapear.*

For a full list of all the named gates, refer to the Qiskit docs of the |QuantumCircuit class|_.

.. |QuantumCircuit class| replace:: ``QuantumCircuit`` class
.. _QuantumCircuit class: https://www.qiskit.org/documentation/_autodoc/qiskit.QuantumCircuit.html
