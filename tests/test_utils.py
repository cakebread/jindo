
from jindo.utils import sinsert, camel_to_human

def sinsert(original, new, pos):
    '''Inserts new string inside original string at pos'''
    return original[:pos] + new + original[pos:]


def camel_to_human(original):
#Index where capital letters are
    i = 0
    for s in original:
        if s.isupper():
            original = sinsert(original, " ", i)
            i += 1
        i += 1
    original = original.capitalize()
    return original


def test_camel_to_human():
    assert camel_to_human("thisWasCamelCase") == "This was camel case"
    assert camel_to_human("thisIsCamelCase") == "This is camel case"
    assert camel_to_human("oneTwo") == "One two"
    assert camel_to_human("oneTwoThree") == "One two three"

