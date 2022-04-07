from enum import Enum

token = '1747591025:AAHS-0nd9_Gnjy8yieWy2vuxnEcTzJhWxTU' # токен
db_file = 'database.vdb'

class States(Enum):
    S_START = "1"
    S_ENTER_DAY = "2"
    S_ENTER_FILM = "3"

