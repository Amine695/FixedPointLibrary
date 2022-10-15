from typing import Optional,Tuple,Union
import re
from math import floor

formatRegex = re.compile(r'^(u|s)?Q([+-]?\d+)\.([+-]?\d+)$')



class FxPConstant :
    """Constant FxP Class : takes a format and a constant value"""
    def __init__(self, msb: Optional[int]=None, lsb: Optional[int]=None,
                    wl: Optional[int]=None, signedness: bool=True,
                    value: Union[str, float]=None,
                    format: Union[str,Tuple[int,float], None]=None) -> None:

        #check format 
        if format is not None:
            if type(format) is not str or type(format) is not tuple:
                raise TypeError("Invalid input format: {}".format(type(format)))
            if type(format) is tuple:
                if not isinstance(format[0],int):
                    raise TypeError("{} invalid format, must be an integer".format(format[0]))
                if not isinstance(format[1],float):
                    raise TypeError("{} invalid format, must be a float".format(format[1]))
                msb, lsb = format
            if type(format) is str:
                res = formatRegex.findall(format)
                if not res:
                    raise ValueError("{} invalid format ".format(format))
                if res[0][0] == "u":
                    signedness = False
                 
        #check value 
        if value is not None:
            if type(value) is not str or type(value) is not float:
                raise TypeError("value must be a string or a float")
            #if type(format[0]) is int:
                
                # a compléter
            #if value = str, regex should take all numbers between " "
            if type(value) is str:
                res = formatRegex.findall(value)
                if not res:
                    raise ValueError("Invalid input format :{}".format(value))
                # a compléter
                

# wl doit etre positif
# si value = float, pas besoin de regex
#  wl,value = format or lsb,value = format


        # intern member variables
        self._msb = msb
        self._lsb = lsb
        self._wl = wl
        self._signedness = signedness
        self._mantissa = None
        self._value = None
        self._bound = None


    #Identique à celle de FxPVar pour le moment, voir si modification ?
    @property
    def FxPValue(self) -> float:
        """
        Returns the value of self._fxpvalue.
        """
        if self._mantissa is not None:
            self._fxpvalue=self._value 
        if self._value is not None:
            if (self._value/2**self._lsb)%1==0: 
                self._fxpvalue=self._value

            if (self._value/2**self._lsb)%1!=0:
                if self._round is False:
                    raise ValueError("The value is not exactly representable on the indicated format, put round=True in function parameters")
                else:
                    # rounding i.e round = True
                    self._fxpvalue = floor(self._value)+2**self._lsb
                    while self._fxpvalue<self._value:
                        self._fxpvalue+=2**self._lsb

        return self._fxpvalue 

    @property
    def msb(self) -> int:
        """
        Returns the msb position.
        """
        return self._msb

    @property
    def lsb(self) -> int:
        """
        Returns the lsb position.
        """
        return self._lsb

    @property
    def wl(self) -> int:
        """
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
        Returns the value of msb.
        """
        return self._mantissa

