import png
import re
import datetime

adobeRegex = re.compile(r'.*adobe.*', re.IGNORECASE)
packetId = re.compile(r'.*id=\"([\d\w]+)\"\\?.*')
documentId = re.compile(r'.*adobe:docid:photoshop:([\w\-\d]+).*')
originalDocId = re.compile(r'.*xmpMM:OriginalDocumentID=\"([\w\-\d]+)\".*')
software = re.compile(r'.*xmp:CreatorTool=\"([\w\d\(\) ]+)\".*')
creationDate = re.compile(r'.*xmp:CreateDate=\"([\dT\-\:\+]+)\".*')


def pngFromBytes(arrayOfBytes: bytes):
    res = ''
    try:
        file = png.Reader(bytes=arrayOfBytes)
        for chunktype, content in file.chunks():
            if chunktype == b'IHDR':
                width = int.from_bytes(content[0:4], 'big')
                height = int.from_bytes(content[4:8], 'big')
                bit_depth = int.from_bytes(content[8:9], 'little')
                interlace_method = int.from_bytes(content[13:14], 'little')
                if interlace_method == 0:
                    interlace_method = 'Отсутствует'
                else:
                    interlace_method = 'Adam7'

                res += f'Ширина: {width}px\n'
                res += f'Высота: {height}px\n'
                res += f'Глубина цвета: {bit_depth} бит\n'
                res += f'Метод чересстрочной развёртки: {interlace_method}\n'
            elif chunktype == b'iTXt':
                content = content.decode(('utf8'))
                if adobeRegex.match(content):
                    if aid := packetId.match(content):
                        res += f'Packet ID документа: {aid.group(1)}\n'
                    if docid := documentId.match(content):
                        res += f'ID документа: {docid.group(1)}\n'
                    if odocid := originalDocId.match(content):
                        res += f'Оригинальный ID документа: {odocid.group(1)}\n'
                    if sfw := software.match(content):
                        res += f'ПО: {sfw.group(1)}\n'
                    if date := creationDate.match(content):
                        date_obj = datetime.datetime.strptime(date.group(1), '%Y-%m-%dT%H:%M:%S%z')
                        res += ('Дата создания: ' + date_obj.strftime('%d.%m.%Y %T (%z)'))
        return res
    except:
        return 'Ошибка'


def pngFromFile(filename: str):
    res = ''
    try:
        file = png.Reader(filename)
        for chunktype, content in file.chunks():
            if chunktype == b'IHDR':
                width = int.from_bytes(content[0:4], 'big')
                height = int.from_bytes(content[4:8], 'big')
                bit_depth = int.from_bytes(content[8:9], 'little')
                interlace_method = int.from_bytes(content[13:14], 'little')
                if interlace_method == 0:
                    interlace_method = 'Отсутствует'
                else:
                    interlace_method = 'Adam7'

                res += f'Ширина: {width}px\n'
                res += f'Высота: {height}px\n'
                res += f'Глубина цвета: {bit_depth} бит\n'
                res += f'Метод чересстрочной развёртки: {interlace_method}\n'
            elif chunktype == b'iTXt':
                content = content.decode(('utf8'))
                if adobeRegex.match(content):
                    if aid := packetId.match(content):
                        res += f'Packet ID документа: {aid.group(1)}\n'
                    if docid := documentId.match(content):
                        res += f'ID документа: {docid.group(1)}\n'
                    if odocid := originalDocId.match(content):
                        res += f'Оригинальный ID документа: {odocid.group(1)}\n'
                    if sfw := software.match(content):
                        res += f'ПО: {sfw.group(1)}\n'
                    if date := creationDate.match(content):
                        date_obj = datetime.datetime.strptime(date.group(1), '%Y-%m-%dT%H:%M:%S%z')
                        res += ('Дата создания: ' + date_obj.strftime('%d.%m.%Y %T (%z)'))
        return res
    except:
        return 'Ошибка'
