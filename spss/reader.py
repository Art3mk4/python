import savReaderWriter
with savReaderWriter.SavReader("reportPoll_479.sav", returnHeader=True) as reader:
    header = next(reader)
    for line in reader:
        print line