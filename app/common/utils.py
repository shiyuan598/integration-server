# 把一个列表转为一个个的key-value
def generateEntries(keys, values):
    try:
        count = len(keys)
        data = []
        for item in values:
            keyValues = {}
            for i in range(count):
                keyValues[keys[i]] = item[i]
            data.append(keyValues)
        return data
    except:
        return []
