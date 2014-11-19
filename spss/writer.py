#coding: utf-8
import savReaderWriter

savFileName = 'someFile.sav'
records = [[11, '12.11.2004 23:55', '0'], [12, '02.03.2003 14:24', '1']]
varNames = ['id', 'created', 'q1']
varTypes = {'id': 0, 'created': 255, 'q1': 255}
varLabels = {'id': 'Ид', 'created': 'Создано', 'q1': 'Как дела?'}
formats = {'id' : 'F40', 'created': 'A255', 'q1': 'A255'}
valueLabels = {'q1':{b'0': 'Да', b'1': 'Нет'}}
with savReaderWriter.SavWriter(savFileName, varNames, varTypes, valueLabels, varLabels, formats) as writer:
    for record in records:
        #record[1] = writer.spssDateTime(record[1], '%d.%m.%Y %H:%M')
        writer.writerow(record)