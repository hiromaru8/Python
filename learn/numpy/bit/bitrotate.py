import numpy as np

def rotate_left_inRrange(data : np.int64, shiftsize : int,effective_size:int)->np.int64:
    """
    dataの右側effective_sizeビット数内で左ローテート
    """

    tmp_l = np.left_shift(data,shiftsize)
    
    tmp_r = np.right_shift(data,effective_size-shiftsize)
    
    result = (tmp_l | tmp_r) & (2**effective_size-1)
    
    return result


def rotate_right_inRrange(data : np.int64, shiftsize : int,effective_size:int)->np.int64:
    """
    dataの右側effective_sizeビット数内で右ローテート
    """

    tmp_l = np.left_shift(data,effective_size-shiftsize) & (2**effective_size-1)
    
    tmp_r = np.right_shift(data,shiftsize) & (2**(effective_size-shiftsize)-1)
    
    result = (tmp_l | tmp_r) 
    
    return result

