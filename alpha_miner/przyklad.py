# from pm4py.objects.log.importer.xes import factory as xes_import_factory
# from file_path import get_file_path

# #path = get_file_path()
# log = xes_import_factory.apply('C:/Studia/VII semestr (inz)/Modelowanie_i_analiza_procesow_biznesowych/event-logs-process-mining-book-examples/Chapter_1/running-example.xes')
# #print(path)
# print()
# print(log) #prints the first trace of the log
# print()

# for i in log[0]:
#     print(i["concept:name"]," ", type(i["time:timestamp"]))
# print()
# print(log[0][1])

tab = [[1,2,3,4,5],[1,2,3,4,5]]
tab2= [120, 151]

for i in range(0,len(tab)):
    print(i)
    for j in range(0, len(tab[i])):
        print(tab[i][j], end="")
    print()
