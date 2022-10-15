from FxPVar import *
from pytest import raises,mark

# msb * 2^(lsb)
# wl = msb - lsb +1

#VALID ASSESSEMENTS !


def test_fxp_FxPFxPValue():
    a = FxPVar(wl=8, lsb=-3) 
    assert a.FxPValue is None
    

def test_special_cases():
    with raises(ValueError):
        FxPVar(msb=12, lsb=0, wl=44)


@mark.parametrize("form", [(12, "toto"), ("titi", -4), (True, 12), ("tot", "jklk")])
def test_wrong_formats1(form):
    with raises(TypeError):
        FxPVar(format=form)


@mark.parametrize("form", [(8, 8), (8, 19), "Q-8.8", "flgkfl", "tQ8.8", (8, 9),"sQ8.8"])
def test_wrong_formats2(form):
    with raises(ValueError):
        FxPVar(format=form)


@mark.parametrize("form", [(8, 10), "Q8.19", "sQ8.12", "uQ-8.0"])
def test_valid_formats_string(form):
    with raises(ValueError):
        FxPVar(format=form)


@mark.parametrize("form,msb,lsb", [("Q5.4", 6, 8),("Q9.3", 9, 11),("(5,3)",5,6),("(8,-8)",5,3)])
def test_Qstring(form, msb, lsb):
    x = FxPVar(format=form)
    assert x.msb != msb or x.lsb != lsb


@mark.parametrize("form,msb,lsb", [("Q5.3", 5,3), ("Q9.3", 9, 3),("(5,3)",5,3),("(8,-8)",8,-8)])
def test_Qstring2(form, msb, lsb):
    x = FxPVar(format=form)
    assert x.msb == msb and x.lsb == lsb


# Format 1

# Tests 
@mark.parametrize("val,tes", [(5.5, 5.5), (5.0, 5.0),(63.5, 63.5),(63.0,63.0),(63,63)]) # tes for test
def test_no_round(val, tes):
    x = FxPVar(format=(6, -1))
    x.initValue(value=val)
    assert x.FxPValue == tes


@mark.parametrize("val,r,tes", [(5.5, True, 5.5), (5.5, False, 5.5), (5.3, True, 5.5),
				  (5.53, True, 5.5), (5.48, True, 5.5), (5.03, True, 5.0), (4.95, True, 5.0)])
def test_round(val, r, tes):
    x = FxPVar(format=(6, -1))
    x.initValue(value=val, rounded=r)
    assert x.FxPValue == tes


# Format 2

# Tests
@mark.parametrize("val", [4.25, 100, 0.0001, 127.5])
def test_non_passable(val):
    x = FxPVar(format=(1, -2))
    with raises(ValueError):
        x.initValue(value=val)


@mark.parametrize("val,r,tes", [(1.25, False, 1.25),(1.243, True, 1.25),(1.261, True, 1.25)])
def test_passable(val, r, tes):
    x = FxPVar(format=(2, -2))
    x.initValue(value=val, rounded=r)
    assert x.FxPValue == tes


# Tests mantissa
# mant for mantissa
@mark.parametrize("mant,r,tes", [(25, False, 12.5), (25, True, 12.5), (3, False, 1.5), (31, False, 15.5)])
def test_mantissa_passable(mant, r, tes):
    x = FxPVar(format=(4, -1))
    x.initValue(mantissa=mant, rounded=r)
    assert x.FxPValue == tes


@mark.parametrize("mant", [4.25, 0.5, 10.0001])
def test_mantissa_non_passable(mant):
    x = FxPVar(format=(4, -2))
    with raises(TypeError):
        x.initValue(mantissa=mant)


# Tests mantissa and value

@mark.parametrize("mant,val,r,tes", [(25, 12.5, False, 12.5), (25, 12.5, True, 12.5), (3, 1.5, False, 1.5)])
def test_mantissa_value_passable(mant, val, r, tes):
    x = FxPVar(format=(4, -1))
    x.initValue(mantissa=mant, value=val, rounded=r)
    assert x.FxPValue == tes


@mark.parametrize("mant,val,r,tes", [(25, 100, False, 12.5), (25, 100, True, 12.5), (3, 2.5, False, 1.5)])
def test_mantissa_value_not_passable(mant, val, r, tes):
    x = FxPVar(format=(4, -1))
    with raises(ValueError):
        x.initValue(mantissa=mant, value=val, rounded=r)

