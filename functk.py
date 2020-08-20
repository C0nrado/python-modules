from inspect import signature
from functools import partial
from copy import deepcopy
import itertools

class IterCloner():
    def __init__(self, iterator, n=2):
        self.iters = iter(itertools.tee(iterator, n))
    def __call__(self):
        try:
            return next(self.iters)
        except StopIteration:
            raise StopIteration('clone iterator exhausted')

def clone_iter(iterator, n_clones):
    return IterCloner(iterator, n_clones)

def copy_iter(clone_container, n_copies):
    return [deepcopy(clone_container) for _ in range(n_copies)]

def curry(func):
	def curried(*args, func=func, **kwargs):
		func_params = signature(func).parameters
		n_params = len([k for k,val in func_params.items()
					if val.default == val.empty])
		assert n_params >= 1
		if n_params == 1:
			return func(*args, **kwargs)
		else:
			func = partial(func, *args, **kwargs)
			return curry(func)
	return curried

def compose(*functions):
     def composed(functions, arg):
         assert len(functions) >= 1
         if len(functions) == 1:
             return functions[0](arg)
         else:
             func = functions[-1]
             arg = func(arg)
             return composed(functions[:-1], arg)
     return partial(composed, functions)