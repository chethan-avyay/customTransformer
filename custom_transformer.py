import marshal
from types import FunctionType
from sklearn.base import BaseEstimator, TransformerMixin

class MyFunctionTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, f):
        self.func = f
    def __call__(self, X):
        return self.func(X)
    def __getstate__(self):
        self.func_name = self.func.__name__
        self.func_code = marshal.dumps(self.func.__code__)
        del self.func
        return self.__dict__
    def __setstate__(self, d):
        d["func"] = FunctionType(marshal.loads(d["func_code"]), globals(), d["func_name"])
        del d["func_name"]
        del d["func_code"]
        self.__dict__ = d
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return self.func(X)