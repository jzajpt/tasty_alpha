import pytest
import numpy as np
from tasty_alpha.utils import ewma

# 1 2 3 4 5 6 7 8 9 10
# - - - - -
#   - - - - -
#     - - - - -
#       - - - - -
#         - - - - -
#           - - - - -

def test_ewma_size():
    values = np.linspace(1, 10, 10)
    ewma_values = ewma(values, 5)
    assert len(ewma_values) == 6

