# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 13:39:31 2023

@author: jackl
"""

import os
import pickle

def cacheDecorator(name):
    fn = f"{name}_stored.pkl"
    def decorator(function):
        def wrapper():
            if os.path.exists(fn):
                print(f"Loading {fn}")
                with open(fn,'rb') as fh:
                    results = pickle.load(fh)
            else:
                print(f"Creating {fn}")
                results = function()
                with open(fn,'wb') as fh:
                    pickle.dump(results,fh)
            return results
        return wrapper
    return decorator

if __name__ == "__main__":
    @cacheDecorator('test')    
    def someFunc():
        a = 1
        b = "test"
        return a,b
    a,b = someFunc()