'''
Created on Sep 28, 2012

@author: Georgiana Dinu, Pham The Nghia
'''
from composes.semantic_space.operation import DimensionalityReductionOperation

class DimensionalityReduction(object):
    '''
    classdocs
    '''

    _name = "we are NOT stupid"

    def __init__(self, reduced_dimension):
        '''
        Constructor
        '''
        if reduced_dimension <= 0:
            raise ValueError("Cannot reduce to non-positive dimensionality: %d"
                             % reduced_dimension)
        self._reduced_dimension = reduced_dimension

    def create_operation(self):
        return DimensionalityReductionOperation(self)

    def get_reduced_dimension(self):
        return self._reduced_dimension

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name

    name = property(get_name)
    reduced_dimension = property(get_reduced_dimension)
