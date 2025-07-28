"""
np.int**データから任意のビットを抽出する。
"""

import numpy as np


def mid_1data_int64(data:np.int64,startposition,totalbitsize)->np.int64:
    """a（np.int64）のstartposition位置からtotalbitsizeビット抽出し、
    右づめでnp.int64として出力する
    """
    
    tmp = np.right_shift(data,64-(startposition+totalbitsize))
    
    result = tmp & (2**totalbitsize-1)
    
    return result

def mid_1data_int64toint32(data:np.int64,startposition,totalbitsize)->np.int32:
    """a（np.int64）のstartposition位置からtotalbitsizeビット抽出し、
    右づめでnp.int32として出力する
    """
    result = mid_1data_int64(data,startposition,totalbitsize)
    
    return np.int32(result)

def mid_1data_int64toint32_ljust(data:np.int64,startposition,totalbitsize)->np.int32:
    """a（np.int64）のstartposition位置からtotalbitsizeビット抽出し、
    左づめでnp.int32として出力する
    """
    tmp    = mid_1data_int64toint32(data,startposition,totalbitsize)
    
    # 左に詰める
    result = np.left_shift(tmp,32-totalbitsize) 
    
    return result


def mid_2data_int64(data_l:np.int64,data_r:np.int64,startposition_l:int,startposition_r:int,totalbitsize:int)->np.int64:
    """
    data_l（np.int64）のstartposition_l位置
    data_r（np.int64）のstartposition_r位置
    から合計totalbitsizeビット抽出し、右づめでnp.int64として出力する
    """
    # tmp_1 : 「totalbitsize - (64(data_lのサイズ) - startposition_l)」左シフト（data_r側のビット分の領域確保）
    #                           -----------------------------------
    #                            data_l側の抽出ビット数
    tmp_l = np.left_shift(data_l,totalbitsize+startposition_l-64)
    # tmp_r : 「64(data_rのサイズ) - (startposition_r + ( totalbitsize - (64(data_lのサイズ) - startposition_l)))」右シフト（data_r側の右側空きビット分）
    #                                ----------------    --------------------------------------------------------
    #                                  data_r側の左空きビット数　　　　　　data_r側の抽出ビット数
    tmp_r = np.right_shift(data_r,128-(totalbitsize+startposition_l+startposition_r))  & (2**(totalbitsize+startposition_l-64)-1)
    
    result = (tmp_l | tmp_r) & (2**totalbitsize-1) & (2**totalbitsize-1)
    
    return result


def mid_2data_int64toint32(data_l:np.int64,data_r:np.int64,startposition_l:int,startposition_r:int,totalbitsize:int)->np.int32:
    """
    data_l（np.int64）のstartposition_l位置
    data_r（np.int64）のstartposition_r位置
    から合計totalbitsizeビット抽出し、右づめでnp.int32として出力する
    
    """
    
    result = mid_2data_int64(data_l,data_r,startposition_l,startposition_r,totalbitsize)
    
    return np.int32(result)

