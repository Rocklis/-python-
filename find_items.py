# s = [['001', '南京', '郑州'], ['002', '广州', '南宁'], ['003', '驻马店', '南宁'], ['004', '南京', '北京'], ['005', '广州', '郑州']]

# 找到符合条件的列表，即找到符合条件的航班记录
def find_item1(s: list or tuple, index1: int, one:str):

    selected = []
    for it in s:
        if (it[index1] == one):
            selected.append(it)
    return selected

# 找到航班在列表中的下标
def find_exist(s:list,sno:int):
    index =0
    for it in s:
        if it[0] == sno:
            return index
        index += 1
    return -1
# print(find_exist(s,'001'))
# print(find_exist(s,'006'))

# def find_item2(s: list, index1: int, one, index2: int, two):
#     selected = []
#     selected1 = find_item1(s, index1, one)
#     for it in selected1:
#         if (it[index2] == two):
#             selected.append(it)
#     return selected
#
#
#
# def find_item3(s: list, index1: int, one, index2: int, two, index3: int, three):
#     selected = []
#     selected1 = find_item2(s, index1, one, index2, two)
#     for it in selected1:
#         if (it[index3] == three):
#             selected.append(it)
#     return selected


# find1 = find_item1(s,1,'广州')
# find1 = find_item1(find1,2,'郑州')
# print(find1)
# find2 = find_item2(s, 1, '广州', 2, '南宁')
# print(find2)
# find3 = find_item(s,2,'南宁')
# print(find3)
