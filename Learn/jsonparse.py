class Rooms:
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            print(k, v)

Rooms(
room_infos = {
'Courtyard' : {
    'description'  : 'This is a courtyard',
    'directions'   : {'North' : 'Entrance'},
    'items'        : ['item1', 'item2'],
    'monsters'     : ['monster1', 'monster2']
    },

'Entrance' : {
    'description'  : 'This is a entrance',
    'directions'   : {'North' : "Corridor", 'South' : 'Courtyard'},
    'items'        : ['item1', 'item2'],
    'monsters'     : ['monster1', 'monster2']},

'Corridor': {
    'description'  : 'This is a corridor',
    'directions'   : {'South' : 'Entrance'},
    'items'        : ['item1', 'item2'],
    'monsters'     : ['monster1', 'monster2']}
})
