# -*- coding: utf-8 -*-
import re
import numpy as np



def readsize(inputstr, recomputeOut = False, outFormat = 'cm'):
    """

    Parameters
    ----------
    inputstr : str
        inputstring which should have format 123x567x789. The string describes
        the size of an item and can include chracters to describe the unit

    recomputeOut : TYPE, optional
        Should Units be converted and values sorted for output. The default is False.
    outFormat : TYPE, optional
        Targetformat of unitconversion and values. The default is 'cm'.

    Raises
    ------
    ValueError
        Wrong type of input

    Returns
    -------
    list
        returns length, width, height as tuple with units

    """

    #Conversionrates
    unitsize = {'mm':1,
                'cm':10,
                'dm':100,
                'm':1000,
                'km':1000000, }

    # Height x Length x Width == 3 Dimensions
    dimensions = 3
    
    #split Input into dimensions
    if len(inputstr.split('x')) == dimensions:
        x = inputstr.split('x')
        
    elif len(inputstr.split('X')) == dimensions:     
        x = inputstr.split('X')
 
    else:
        raise ValueError('Cant read input of Size. Use numberXnumberXnumber Format')
    
    
    #Regex Expressions
    #only digits: ^[0-9]*$
    #digits and commas : ^[-,0-9]+$
    #proper numbers: ^([-+] ?)?[0-9]+(,[0-9]+)?$
    
    #Extract values and clean up
    values = [float(re.sub('[a-zA-Z]','', part)) for part in x]
    inputunits = [re.sub('[0-9]','', part) for part in x]
    units = []
    
    
    
    #recompute values to respective unitsize
    if recomputeOut:
    
        c =  [unitsize[unit]/unitsize[outFormat] if len(unit) !=0 else 1 for unit in inputunits]
        values = np.array(values) * np.array(c)
        inputunits = [outFormat for i in inputunits]
        
        
    #Sort values for their size
    values = np.sort(values)[::-1]
    units = [inputunits[i] for i in np.argsort(values)]
    
    
    from collections import namedtuple
    distance = namedtuple('distance', 'value unit')


    return [distance(value = value, unit = unit) for value, unit in zip(values,units)]


