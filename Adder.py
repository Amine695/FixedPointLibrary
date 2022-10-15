from typing import Optional


W_CARRY = 1
WO_CARRY = 2
TRUNCATE = 3
WRAP_AROUND = 4
SATURATE = 5
WRAP = 6


class Adder:
    def __init__(self, w: int=None,
                 mode: int=None,
                 rounding: Optional[int]=None,
                 overflow: int=None) -> None:
        if type(w) is int and w > 1:
            self._w = w
        else:
            raise ValueError("Please input the correct 'w' format :\
                              w must be an integer and strictly\
                              superior than 1")
        if mode == W_CARRY or mode == WO_CARRY:
            self._mode = mode
        else:
            raise ValueError("Please input the correct 'mode' format :\
                              mode must be 'W_CARRY' or 'WO_CARRY'")
        if rounding in [TRUNCATE, WRAP]:  # A COMPLÉTER
            self._rounding = rounding
        else:
            raise ValueError("Please input the correct\
                             'rounding' format")
        if overflow in [WRAP_AROUND, SATURATE, WRAP]:  # A COMPLÉTER
            self._overflow = overflow
        else:
            raise ValueError("Please input the correct\
                             'overflow' format")
            # ALIGNEMENT DE FORMAT

    def add(self, op1, op2):
        """
        FxPVar x FxPVar -> FxPVar
        Returns op1 + op2
        """

        if op1.wl>self._w or op2.wl>self._w:
            raise ValueError("op1 and op2 should have less than w bits")

        if op1.msb==op2.msb and op1.msb==op2.msb: # same format = no arroundi necessary
            val=op1.FxPValue+op2.FxPValue # op1.FxPValue and op1.fxpvalue have the same value

            if val<=2**(op1.msb+1)-1 and val>=2**op1.lsb: # no overflow mode required
                res=FxPVar(format=(op1.msb,op1.lsb)) # res for result
                res.initValue(value=val,round=True) 
                res.FxPValue
                return res

            else: # overflow methods to be applied
                if self._overflow==WRAP_AROUND:
                    pass

                elif self._overflow==SATURATE:
                    pass
                    

                elif self._overflow==WRAP:
                    pass

            
        else : # different format
            # final format corresponds to the format with the largest msb
            if op1.msb>op2.msb:
                res=FxPVar(format=(op1.msb,op1.lsb))
                # change the op2 format to be able to do the calculation and round up if necessary with a rounding method


            else: #op1.msb<=op2.msb
                res=FxPVar(format=(op2.msb,op2.lsb))
                # change the op1 format to be able to do the calculation and round up if necessary with a rounding method
                
        return res



class ctx:
	"""Context class. GLOBAL list containing the current used adders.
	/!\ LIFO /!\
	"""
	def __init__(self) -> None:
	"""
	Contains the context stack.
	"""
		self._ctxLst = []

	def append_adder(self, adder: Adder) -> None:
		"""
		Adder -> None
		Appends a new adder.
		"""
		if not type(adder) is Adder:
			raise ValueError("Context handles only adders")
		self._ctxLst.append(adder)

	def pop_adder(self) -> Adder:
		"""
		None -> Adder
		Removes the last adder that was added. If the context is empty, raises an error.
		"""
		if not len(self._ctxLst):
			raise IndexError("No adder was added to context")
		return self._ctxLst.pop()

	@property
	def current_adder(self) -> Adder:
		"""
		None -> Adder
		Returns the last adder added to context. /!\ DOES NOT REMOVE THE LAST ADDER /!\
		In order to remove the last adder, use pop_adder() instead.
		If no adder was added it raises an error.
		"""
		if not len(self._ctxLst):
			raise IndexError("No adder was added to context")
		return self._ctxLst[-1]


GLOBAL_CONTEXT = ctx()

