data = {
    "channels": [
        {
            "channel": "canal1",
            "owner": "pedro",
            "color": "badge-secondary",
            "messages": [
                {
                    "sender": "sergio",
                    "date": "17/3/2020 19:20",
                    "message": "hola!"
                },
                {
                    "sender": "francisco",
                    "date": "17/3/2020 19:21",
                    "message": "todo bien y vos?"
                }
            ]
        },
        {
            "channel": "canal2",
            "owner": "juan",
            "color": "badge-primary",
            "messages": [
                {
                    "sender": "santiago",
                    "date": "12/3/2020 11:10",
                    "message": "buenas!"
                },
                {
                    "sender": "ernesto",
                    "date": "12/3/2020 11:11",
                    "message": "aca andamos"
                }
            ]
        }
    ]
}

newchannel = "canal3"
# channels = []
# for e in data["channels"]: 
#     channels.append(e['channel'])
# if newchannel in channels:
#     print('yes')
# else:
#     print('no')

encontrado = False
for e in data["channels"]:
    if newchannel == e['channel']:
        # print('encontrado')
        encontrado = True
        # break
print(encontrado)


# print(type(data))
# print(type(data["channels"]))
newlist = sorted(my_list, key=lambda k: k['name'])
my_list = sorted(my_list, key=lambda k: k['name'])
