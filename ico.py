# file = open('./favicon.ico')
# total = file.__str__()
# fileType = file.read()
# currentPosition = file.tell()
# result += (currentPosition)
# file.close()


def bytesToInt(bytes: bytes, byteorder='little'):
    return int.from_bytes(bytes, byteorder)


def countColors(a: int):
    if a == 0:
        return 'полноцветное'
    else:
        return f'имеет {a} цветов'


def icoFromFilename(filename: str):
    try:
        file = open(filename, 'rb')
        result = ''

        file.seek(2, 0)
        if (fileType := bytesToInt(file.read(2))) == 1:
            fileType = 'Это значок\n'
        else:
            fileType = 'Это курсор\n'

        file.seek(4, 0)
        imageCount = bytesToInt(file.read(2))

        file.seek(7, 0)
        width = bytesToInt(file.read(1))

        file.seek(8, 0)
        if (height := bytesToInt(file.read(1))) == 0:
            height = width

        file.seek(9, 0)
        colors = bytesToInt(file.read(1))

        file.seek(14, 0)
        size = bytesToInt(file.read(4))

        file.seek(18, 0)
        imageoffset = bytesToInt(file.read(4))

        result += fileType
        result += f'Всего изображений в файле: {imageCount}\n'
        result += f'Ширина изображения: {width}\n'
        result += f'Высота изображения: {height}\n'
        result += f'Изображение {countColors(colors)}\n'
        result += f'Изображение весит {size} байтов\n'
        result += f'Изображение начинается с {hex(imageoffset)}'

        return result

        file.close()
    except OSError as ose:
        result += (f'OSError: {ose}')


def icoFromBytes(file: bytes):
    result = ''

    if (fileType := bytesToInt(file[2:5])):
        fileType = 'Это значок\n'
    else:
        fileType = 'Это курсор\n'

    imageCount = bytesToInt(file[4:6])

    width = bytesToInt(file[7:8])

    if (height := bytesToInt(file[8:9])) == 0:
        height = width

    colors = bytesToInt(file[9:10])

    size = bytesToInt(file[14:18])

    imageoffset = bytesToInt(file[18:22])

    result += fileType
    result += f'Всего изображений в файле: {imageCount}\n'
    result += f'Ширина изображения: {width}\n'
    result += f'Высота изображения: {height}\n'
    result += f'Изображение {countColors(colors)}\n'
    result += f'Изображение весит {size} байтов\n'
    result += f'Изображение начинается с {hex(imageoffset)}\n'

    return result
