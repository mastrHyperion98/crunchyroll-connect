"""
Created by: Steven Smith (aka mastr_hyperion98)

This is the main script used for examples and testing the request calls. A
Crunchyroll schema/object will be created under the util and schema directories

"""
from crunchyroll_connect.utils.server import CrunchyrollServer

creds = {
    'account': 'steven.smith1998@hotmail.com',
    'password': 'hQ3CR3thn392itgkslD%QIOxu+zg5U4F'

}

if __name__ == "__main__":
    server = CrunchyrollServer()

    session = server.start_session()

    response = server.login(creds['account'], creds['password'])
    logout = server.logout()
    server.end_session()
