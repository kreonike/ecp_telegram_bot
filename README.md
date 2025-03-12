### Описание проекта

реальный прототип: @gkb12nn_bot

работаю в мед организации в городе Нижний Новгород, у нас используется МИС ЕЦП https://ecp.mznn.ru (работает через vipnet)
истории болезней, анализы, исследования и всё прочее заносится туда, так же через нее записывают пациентов к врачу и оформляют вызов врачыа на дом (что я и реализовал в этом боте). 

по сути это аналог записи к врачу, только через бота, со своими преимуществами (бот может записывать на недоступные через гос услуги бирки)

### Как пользоваться

команды:
```
/start
'ЗАПИСЬ К ВРАЧУ' - запись к врачу
'ВЫЗОВ ВРАЧА НА ДОМ' - вызов врача на дом
'ПРОВЕРКА ЗАПИСИ' - проверка записи к врачу 
'ОТМЕНА ЗАПИСИ К ВРАЧУ' - отмена записи к врачу
```


api основные запросы:
- https://ecp.mznn.ru/api/Polis?Polis_Num={polis}
- https://ecp.mznn.ru/api/Address?Person_id={person_id}
- https://ecp.mznn.ru/api/TimeTableListbyPatient?Person_id={person_id}
- https://ecp.mznn.ru/api/TimeTableGraf/TimeTableGrafWrite?Person_id={person_id}&TimeTableGraf_id={TimeTableGraf_id}
- https://ecp.mznn.ru/api/TimeTableListbyPatient?Person_id={person_id}
- https://ecp.mznn.ru/api/Person?Person_id={person_id}


пример вывода:

`curl https://ecp.mznn.ru/api/Refbook?Refbook_Code=dbo.HomeVisitStatus`

доступна база комант от пользователей: bot_database.db

	
```
error_code	0
data	
0	
id	"1"
OrgType_id	null
Name	"Новый"
Code	"1"
KLRgn_id	null
begDate	null
endDate	null
1	
id	"2"
OrgType_id	null
Name	"Отказ"
Code	"2"
KLRgn_id	null
begDate	null
endDate	null
2	
id	"3"
OrgType_id	null
Name	"Одобрен врачом"
Code	"3"
KLRgn_id	null
begDate	null
endDate	null
3	
id	"4"
OrgType_id	null
Name	"Обслужен"
Code	"4"
KLRgn_id	null
begDate	null
endDate	null
4	
id	"5"
OrgType_id	null
Name	"Отменен"
Code	"5"
KLRgn_id	null
begDate	null
endDate	null
5	
id	"6"
OrgType_id	null
Name	"Назначен врач"
Code	"6"
KLRgn_id	null
begDate	null
endDate	null
```





Основные методы API:

    Поиск человека:

        Метод: GET api/Person
        Параметры: Person_id, PersonSurName_SurName, PersonFirName_FirName, PersonBirthDay_BirthDay, PersonSnils_Snils.
        Описание: Поиск человека по идентификатору или другим параметрам. Если запись не найдена, выполняется параметризированный поиск.
 
    Поиск полиса:

        Метод: GET api/Polis
        Параметры: Person_id, Polis_Ser, Polis_Num.
        Описание: Поиск полиса по идентификатору человека и номеру полиса.     

    Запись пациента на приём:

        Методы: GET api/MedSpecOms/MedSpecOmsByMO, GET api/TimeTableGraf/TimeTableGrafFreeDate & etc
        Параметры: MedSpecOms_id, TimeTableGraf_beg, Person_id, MedStaffFact_id 
        Описание: поиск свободного времени, бирок (времени), и запись пациента на приём.

    Отмена записи:

        & etc        



### Основные функции бота
Запись к врачу: Пользователь может выбрать поликлинику, специальность врача, врача, дату и время приёма, а затем записаться на приём.
Вызов врача на дом: Пользователь может вызвать врача на дом, указав свой полис ОМС, адрес, телефон и причину вызова.
Проверка записи: Пользователь может проверить свои записи к врачу или статус вызова врача на дом.
Отмена записи: Пользователь может отменить запись к врачу или вызов врача на дом.
Информация о поликлиниках: Пользователь может получить информацию о адресах и телефонах поликлиник, а также о режиме их работы.

### Установка и запуск бота
python or python3

- `screen`
- `python -m venv ecp`
- `pip install -r requirements.txt`
- `python main.py`

