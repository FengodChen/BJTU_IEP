import numpy as np
import base64

def size2str_2D(size_tuple) -> str:
    (h, w) = size_tuple
    size_str = "{}x{}".format(h, w)
    return size_str

def str2size_2D(size_str) -> (int, int):
    [h, w] = size_str.split("x")
    h = int(h)
    w = int(w)
    return (h, w)

def np2str(npArray, dtype=np.uint8) -> (str, str):
    '''
    return (array_string, array_size)
    '''
    npArray_size_str = size2str_2D(npArray.shape)

    npArray_bytes = npArray.tobytes()
    npArray_base64 = base64.encodebytes(npArray_bytes)
    npArray_base64_str = str(npArray_base64, encoding="utf-8")

    return (npArray_base64_str, npArray_size_str)

def str2np(npArray_base64_str, npArray_size_str, dtype=np.uint8) -> np.array:
    '''
    return 2D np.array
    '''
    npArray_size = str2size_2D(npArray_size_str)

    npArray_base64 = bytes(npArray_base64_str, "utf-8")
    npArray_bytes = base64.decodebytes(npArray_base64)
    npArray = np.frombuffer(npArray_bytes, dtype=dtype)

    npArray.resize(npArray_size)

    return npArray
