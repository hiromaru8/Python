from abc import ABC, abstractmethod
from typing import List

import pandas as pd

class ConcatStrategy(ABC):
    @abstractmethod
    def concat(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        """複数のDataFrameを結合する戦略"""
        pass
