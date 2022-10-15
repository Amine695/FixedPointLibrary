# Explicit Fixed-Point arithmetic Python library


## Classes specifications
This is a partial specification (used as a guideline and basis for discussion)
Different classes have to be implemented

### `FxPVar`: fixed-point variable object

- constructor (`__init__`): defines a FxP format
  - `msb`, `lsb`, `wl`, `signedness` (`signedness` is `True` by default, and only 2 of the 3 `msb`, `lsb`, `wl` should be given; if 3, they should be consistent)
  - `format` as a string (Q-notation or P-notation: "Q12.4", "(8,-8)", etc.)
  - `format` as a tuple (msb, lsb)
  - if `format` is given in complement of `msb`..., then its ok *if* it's consistent

- (intern) member variables
  - `_msb`, `_lsb`, `_wl`, `_signedness`: represent the FxP format
  - `_mantissa` (int): mantissa
  - `_value` (float), `_bound` (float): the exact value is in the interval centered in `value` and with `bound` as radius (interval [`value`-`bound`, `value`+`bound`])

- other methods
  - `initValue`: used to initialize the value (could also be put in `__init__`??)
    - `mantissa`: (int) set the mantissa (should be in correct range)
	- `value` (float) should be a value the format can exactly represent
	- `value`, `round=True`, the value is then converted to the FxP format with round-to-nearest (even tie breaking rule)

  - `_setValue`: used by the operator to set the mantissa, value/bound
	- `mantissa` (int), `value` (float), `bound`(float)

  - `msb`, `lsb`, `wl`, `signedness`, `matissa` as properties
  - `FxPValue`: returns the fixed-point value (mantissa*2^lsb)
  - `error`: returns (a bound on) the error between the exact value and the FxP value: (RU(RU(value-FxPValue)+bound)
  - properties for the value and bound ??
  
  - `__add__` and `__mul__`: see adder and multiplier (use the adder/multiplier registered in a context manager)

  


### `FxPConstant`: fixed-point constant (quite similar to `FxPVar`, except that the value is set at construction and cannot be changed)

- constructor (`__init__`): takes a format (as `FxPVar`) and a constant
  - `msb`, `lsb`, `wl`, `signedness` and `format` as for `FxPVar`
  - `value` as string or float: the value will be rounded to the nearest (even tie-breaking rule)
  - constructor can take only `wl` or `lsb` in addition to the constant, since the `msb` is deduced from the constant (see formulas doc FxP.pdf, section 3.6)

- (intern) member variables
  - `_msb`, `_lsb`, `_wl`, `signedness` for the FxP format
  - `_mantissa` (int)
  - `_value` (float) and `_bound` (`_bound` is 0 if a float is given for construction, but may be a float if a string is given, cf with "0.1")

- other methods
  - `error`, `FxPValue` (cf `FxPVar`)
  - `msb`, `lsb`, `wl`, `signedness`, `matissa` as properties

### `Adder`: class for an adder

- constructor (`__init__`):
  - `w` (int>1): word-length of the adder
  - `mode`: with or without carry (the result has `w` or `w+1` bits); create constant like `W_CARRY` et `WO_CARRY` or something more clever
  - `overflow`: overflow mode (`WRAP_AROUND`, `SATURATE`, etc. - names to defined)
  - `rounding`: rounding mode (`TRUNCATION`, etc. - names to defined)

- (intern) member variables
  - `_w`, `_mode`, `_overflow` and `_rounding`

- other methods
  - some properties `w`, `mode`, `overflow` and `rounding` ??
  - `add`: performs the addition of two operands `op1` and `op2`
    - `op1` and `op2` should have less than `w` bits (otherwise an exception is raised)
    - returns the result (an `FxPVar` with `w` or `w+1` bits), with `_mantissa`, `_value` and `_bound` updated...
  - `__enter__` and `__exit__` to make the adder usable with `with` (ie stores the adder in the context for the addition)
  

### Multiplier

- constructor (`__init__`):
  - `w1` and `w2` (int>1): word-length of the two operands
  - `mode`: the result has `w1+w2` or `w1+w2-1` bits; create constant like `W_CARRY` et `WO_CARRY` or something more clever
  - `overflow`: overflow mode  if `w1+w2-1` bits ??
  - other possibility: `res` gives the result's wordlength; a `rounding` mode is required

- (intern) member variables
  - `_w1`, `_w2`, `_mode` ...

- other methods
  - some properties `w1`, `w2`, `mode` ??
  - `mul`: performs the multiplication of two operands `op1` and `op2`
    - `op1` and `op2` should have less than `w1` and `w2` bits (otherwise an exception is raised)
    - returns the result (an `FxPVar` with `w1+w2` or `w1+w2-1` bits), with `_mantissa`, `_value` and `_bound` updated...
  - `__enter__` and `__exit__` to make the multiplier usable with `with` (ie stores the multiplier in the context for the multiplication)

## Examples

```python
# constants
a = FxPConstant(wl=8, value=12.125)
b = FxPConstanr(wl=6, value=-6.666)
c = FxPConstanr(lsb=-6, value=sqrt(2))
# variables
u = FxPVar(wl=8, lsb=-3)
x = FxPVar(format="sQ8.8")
z = FxPVar(format=(8,-6))
# operators
A = Adder(w=8, mode=WO_CARRY, round=TRUNCATE, overflow=WRAP)
M = Multiplier(w1=8, w2=8, res=8, rounding=TRUNCATE, mode=WITH_MSB)
# operation (wrong, I did not check the consistency of the FxP format !)
z = A.add( A.add( M.mul(a,u), M.mul(b,x) ), M.mul(c,z) )
# other way to do
with A, M:
	z = (a*u + b*x) + c*z
```

## How `with` and context manager work
when you have the code
```python
with A:
	z = x + y
```
the method `__enter__` of `A` is first run, then the code inside the `with` and at the end, the method `__exit__` of `A`. The idea in `__enter__` is to tell a "context" that now the adder is `A`. Then, when `x+y` is computed, it runs the method `__add__` of `x`, that will directly run the method `add` of the adder registered to the "context". (same for the multiplier). The following should also work (`A1` and `A2` are adders)
```python
with A1:
	z = x+y
	with A2:
		z = z+x
	z = z+y
```
(here, the 2nd addition is done with adder `A2` while the 1st and 3rd are done with `A1`). It means that the "context" should stack the adder (and multiplier) registered.

### `ctx`: to store the context and the default behavior

an "object" `ctx` can be used to store the "context" (operators registered), but also (maybe - to be discussed)
- for the default overflow and rounding mode ?
- for the behavior in some context:
  - when `FxPVar.initValue` or `FxPConst.__init__` induce an overflow (should be an exception by default) ?
  - when they induce an underflow (should be logged by default, but may raise an exception)
