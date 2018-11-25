import json


def Datensatz(Id,nameMesswert,listwert,listEinheit,listTime):
    info={'ID':Id,'NameMesswert':nameMesswert,'Wert':listwert,'Einheit':listEinheit,'Zeit':listTime}

    ToSendInfo=json.dumps(info)
    print(ToSendInfo)
    return(ToSendInfo)




A=[2,3,4,5,1,2,5]
E=['m','N','l']
T=[23,5,45,23,65,4,23]
Datensatz(3,'test',A,E,T)