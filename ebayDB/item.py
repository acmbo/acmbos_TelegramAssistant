# -*- coding: utf-8 -*-

class item(object):
    
    def __init__(self, idx, name):
        """
        Item class, which represents an ebay item, to connect the ebay api to 
        the respective sql database

        Parameters
        ----------
        idx : str,float, int
            Index (in the database) of the item
        name : str
            Name of the item

        Returns
        -------
        None.

        """
        
        self.idx = idx
        self.name = name
        self.size = {}
        self.type = ''
        self.pictures = []
        self.description = ''
        self.origin = ''
        self.ebayid = 0
        self.startprice = 0
        self.listingduration = ''
        
        
    @property
    def idx(self):
        return self.__idx
    
    @idx.setter
    def idx(self, idxinput):
        '''Checks for correct setting of index'''
        if isinstance(idxinput,(float, int, str)) and  len(str(idxinput)) != 0:
             self.__idx = idxinput
        else:       
            raise ValueError('Bad Index')
    
    
    def setsize(self, inputsize, outFormat = 'cm'):
        """
        Adds size attributes to item
        
        Parameters
        ----------
        inputsize : str
                    inputstring which should have format 123x567x789. The string describes
                    the size of an item and can include chracters to describe the unit

        outFormat : TYPE, optional
                    Targetformat of unitconversion and values. The default is 'cm'.


        Returns
        -------
        None.

        """
        from utils.funcs import readsize

        vals = readsize(inputsize, 
                        recomputeOut = bool(outFormat), 
                        outFormat = outFormat)
        
        for attr, val in zip(['length','width','height'], vals):
             setattr(self, attr, val)
             self.size[attr] = val
             
    
    
    def addpic(self,pathtofpicture):
        """
        Adds picturepath to item
        
        Parameters
        ----------
        pathtofpicture : str
                        patht of picture as string on system
        """
        
        self.pictures.append(pathtofpicture)
        
    
    
    