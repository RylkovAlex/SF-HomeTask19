import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir)))

from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply(self):
        assert self.calc.multiply(Calculator(), 2, 2) == 4

    def test_division(self):
        assert self.calc.division(Calculator(), 4, 2) == 2

    def test_division_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.division(Calculator(), 4, 0)

    def test_subtraction(self):
        assert self.calc.subtraction(Calculator(), 0, 1) == -1

    def test_adding(self):
        assert self.calc.adding(Calculator(), 4, 4) == 8
