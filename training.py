import time

def decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start
        print(end)
        return result
    return wrapper




@decorator
def anagram(first: str, second: str):
    # Создаем пустые словари
    dict_first = {}
    dict_second = {}
    # Перебираем строку
    for i in first:
        #Если в словаре есть символ, то меняем значение на +1
        if i in dict_first:
            dict_first[i] += 1
            # Иначе добавляем в словарь со значением 1
        else:
            dict_first[i] = 1
    for j in second:
        if j in dict_second:
            dict_second[j] += 1
        else:
            dict_second[j] = 1
    print(dict_first, dict_second)
    time.sleep(.1)
    return dict_first == dict_second


s1 = 'aa'
s2 = 'a'
result = anagram(s1, s2)
print(result)

@decorator
def palindrome(stroka):
    result = ''.join(reversed(stroka))
    time.sleep(.1)
    if (result == stroka):
        return True
    else:
        return False


s3 = 'qwertytrewq'
res_palin = palindrome(s3)
print(res_palin)


@decorator
# Итеративный метод, если проверять первый и последний символ и находить несовпадение, то False
def palindrome2(stroka):
    time.sleep(.1)
    for i in range(0, len(stroka)//2):
        if stroka[i] != stroka[len(stroka)-i-1]:
            return False
    return True

s4 = 'asdfdsa'
r = palindrome2(s4)
print(r)

