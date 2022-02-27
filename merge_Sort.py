"""
arr = [(24,1001),(54,1002),(53,1003),(423,1005)]
"""


def mergeSort(arr, flag):
    import math
    if (len(arr) < 2):
        return arr
    middle = math.floor(len(arr) / 2)  # floor() 返回数字的下舍整数。
    left, right = arr[0:middle], arr[middle:]
    return merge(mergeSort(left, flag), mergeSort(right, flag), flag)


def merge(left, right, flag):
    result = []
    if (flag == False):
        while left and right:
            if float(left[0][0]) <= float(right[0][0]):
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
    else:
        while left and right:
            if float(left[0][0]) >= float(right[0][0]):
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))

    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result
