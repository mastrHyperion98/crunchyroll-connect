"""
Created by: Steven Smith (aka mastr_hyperion98)

This is the main script used for examples and testing the request calls. A
Crunchyroll schema/object will be created under the util and schema directories

"""
from crunchyroll_connect.utils.server import CrunchyrollServer, RequestType

creds = {
    'account': 'steven.smith1998@hotmail.com',
    'password': 'hQ3CR3thn392itgkslD%QIOxu+zg5U4F'

}

if __name__ == "__main__":
    server = CrunchyrollServer()
    url = server.getUrl(RequestType.LOGIN)

    session = server.start_session()
    print(session.json()['data']['session_id'])
    #response = server.login(creds['account'], creds['password'], 'b4f5822ed36ec2757f92385253d1b184')
    #print(response.text)