a_list = [1,2,5,6,7,8,13,14,15,17,18,24,30,43,56]

def check_out(data, search):
    if not data:
        return False
    head = 0
    tail = len(data)
    mid = (head+tail)//2

    while tail - head != 1:
        mid = (head+tail)//2
        if search < data[mid]:
            tail = mid

        elif search > data[mid]:
            head = mid + 1

        elif search == data[mid]:
            # print(data[mid])
            return mid

    else:
        if search == data[head]:
            return head
        else:
            return False

print(check_out(a_list, 0))




