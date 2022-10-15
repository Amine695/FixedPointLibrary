from typing import Union, Optional, Tuple
import re
from math import floor

formatRegex = re.compile(r'^(u|s)?Q([+-]?\d+)\.([+-]?\d+)$|\(([+-]?\d+)\,([+-]?\d+)\)$')


class FxPVar:
	"""Fixed point variable. NOT A CONSTANT."""
	def __init__(self, msb: Optional[int]=None, lsb: Optional[int]=None,
                 wl: Optional[int]=None, signedness: bool=True,
				 value: Union[float, None]=None,
				 format: Union[str, Tuple[int, int], None]=None) -> None:
		"""
		format of the variable:
			1) msb: Optional[int] = most significant bit
			2) lsb: Optional[int] = least significant bit
		wl: Optional[int] = word length, i.e the bit length of the number: wl = msb-lsb+1 (1 bit for the sign)
		value: Union[float, None] = the float value of the variable
		format: Union[str, Tuple[int, int], None] = the format of the variable (not given separately like msb, lsb)
		"""
		# check the format
		if format is not None:
			if type(format) is tuple:
				if not isinstance(format[0], type(format[1])) or type(format[0]) is not int:
					raise TypeError("msb and lsb must be integers")
				msb, lsb = format
			else:
				# check for string format ("s/u/_Qxx.xx")
				res = formatRegex.findall(format)
				if not res:
					raise ValueError("The format is not correct: %s", format)
				if res[0][0] == 'u':
					signedness = False
				try:
					msb, lsb = [int(i) for i in res[0][1:] if not i == '']
				except ValueError:
					raise ValueError("The format is not correct: %s", format)

		# if msb and lsb are given
		if (msb is not None) and (lsb is not None):
			if msb <= lsb:
				raise ValueError("msb must be greater than lsb")
			if wl is not None:
				if msb-lsb+1 != wl:
					raise ValueError("wl must be equal to msb-lsb+1")
			else:
				wl = msb-lsb+1

		# if wl is given
		if wl is not None:
			if msb is not None:
				lsb = msb-wl+1
			if lsb is not None:
				msb = wl+lsb-1

		# declaration and initialisation of class variables
		self._msb = msb
		self._lsb = lsb
		self._wl = wl
		self._signedness = signedness
		self._value = value
		self._mantissa = None

	# class methods and properties
	def initValue(self, mantissa: Optional[int]=None, value: Optional[float]=None, rounded: bool=False) -> None:
		"""
		Optional[int] x Optional[float] x bool -> None
		Sets the value of self._mantissa and self._value.
		"""
		# if mantissa is not None or mantissa is not an int
		if not isinstance(mantissa, int) and mantissa is not None:
			raise TypeError("a mantissa must be an integer")

		if mantissa is None and value is None:
			raise ValueError("a float value or a mantissa value must be entered as function parameters")

		if self._signedness == True : # or maybe just "if self._signedness:"
			# if mantissa and value are given

			if mantissa is not None and value is not None:
				if mantissa*2**self._lsb != value:
					raise ValueError("value must be equal to mantissa*2**self.lsb")

				if -2**(self._lsb+self._wl-1)>value or value>2**(self._lsb)*(2**(self._wl-1)-1):
					raise ValueError("The value is not correct on the indicated format")

				if -2**(self._wl-1)> mantissa or mantissa > 2**(self._wl-1)-1:
					raise ValueError("The mantissa is not correct on the indicated format")			

			# if only mantissa is given
			elif mantissa is not None:
				value = mantissa*2**self._lsb

			# if only value is given	
			elif value is not None:
				# test if value is in [-2**(self._lsb+self._wl-1), 2**(self._lsb)*(2**(self._wl-1)-1)] (mathematical notation)
				if -2**(self._lsb+self._wl-1) <= value <= 2**(self._lsb)*(2**(self._wl-1)-1):
				
					# test whether the value is exactly representable on the format or not 
					if value%(2**self._lsb) == 0:
						mantissa=value*2**(-self._lsb)

					else: # if the value is not exactly representable on the format, it must be rounded to make it so
						if rounded is False:
							raise ValueError("The value is not exactly representable on the indicated format, put `rounded=True` in function parameters")
						else:
							# rounding i.e rounded = True
							value=round(value*2**(-self._lsb))*2**self._lsb

							mantissa=value*2**(-self._lsb)
						
				else: # value is not in [-2**(self._lsb+self._wl-1), 2**(self._lsb)*(2**(self._wl-1)-1)]
					raise ValueError("value must be included in the format entered")

			if -2**(self._wl-1)> mantissa or mantissa > 2**(self._wl-1)-1: # correct place in the code ?
				raise ValueError("The mantissa is not correct on the indicated format")

		else: # self._signedness == False (i.e. unsigned case)

			# if mantissa and value are given
			if mantissa is not None and value is not None:
				if mantissa*2**self._lsb != value:
					raise ValueError("value must be equal to mantissa*2**self.lsb")

				if value<0 or value>2**(self._lsb)*(2**(self._wl)-1):
					raise ValueError("The value is not correct on the indicated format")

				if mantissa<0 or mantissa > 2**(self._wl)-1:
					raise ValueError("The mantissa is not correct on the indicated format")	


			# if only mantissa is given
			elif mantissa is not None:
				value = mantissa*2**self._lsb

			# if only value is given	
			elif value is not None:
				# test if value is in [0, 2**(self._lsb)*(2**(self._wl)-1)] (mathematical notation)
				if 0 <= value <= 2**(self._lsb)*(2**(self._wl)-1):
				
					# test whether the value is exactly representable on the format or not 
					if value%(2**self._lsb) == 0:
						mantissa=value*2**(-self._lsb)

					else: # if the value is not exactly representable on the format, it must be rounded to make it so
						if rounded is False:
							raise ValueError("The value is not exactly representable on the indicated format, put `rounded=True` in function parameters")
						else:
							# rounding i.e rounded = True
							value=round(value*2**(-self._lsb))*2**self._lsb

							mantissa=value*2**(-self._lsb)
						
				else: # value is not in [0, 2**(self._lsb)*(2**(self._wl)-1)]
					raise ValueError("value must be included in the format entered")

			if mantissa<0 or mantissa > 2**(self._wl)-1:
					raise ValueError("The mantissa is not correct on the indicated format")	

		self._mantissa=mantissa
		self._value=value


	@property
	def FxPValue(self) -> Union[float, None]:
		"""
		None -> Union[float, None]
		Returns the value of self._fxpvalue.
		"""
		if self._mantissa is not None:
			return self._mantissa*2**self._lsb
		

	
	@property
	def msb(self) -> int:
		"""
		None -> int
		Returns the msb position.
		"""
		return self._msb

	@property
	def lsb(self) -> int:
		"""
		None -> int
		Returns the lsb position.
		"""
		return self._lsb

	@property
	def wl(self) -> int:
		"""
		None -> int
		Returns the word-length.
		"""
		return self._wl

	@property
	def signedness(self) -> bool:
		"""
		None -> bool
		Returns the value of signedness.
		"""
		return self._signedness

	@property
	def mantissa(self) -> int:
		"""
		None -> int
		Returns the value of msb.
		"""
		return self._mantissa
