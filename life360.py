import requests, time, json

def speedProcess(speed):

        if speed < 0:
            return 0.0
        else:
            return speed

def binary_string(data):

    if data == 0:
        return False
    else:
        return True

def convert(data):

    return tuple(x for x in data)

def getAccessToken(username, password):

    headers = {
                'Accept': 'application/json',
                'Authorization': 'Basic U3dlcUFOQWdFVkVoVWt1cGVjcmVrYXN0ZXFhVGVXckFTV2E1dXN3MzpXMnZBV3JlY2hhUHJlZGFoVVJhZ1VYYWZyQW5hbWVqdQ==', #This code seems to change from time to time
                'Content-Type': 'application/x-www-form-urlencoded'
                }
    data = f'username={username}&password={password}&grant_type=password'
        
    return requests.post('https://www.life360.com/v3/oauth2/token', headers=headers, data=data).json()['access_token']
            

class Life360:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.circleID = ''
        self.access_token = getAccessToken(self.username, self.password)
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
            }
    
    def set_circle(self):
        circles = life360.get_circles()['circles']
        circleData = {}
        for circle in circles:
            circleData[circle['name']] = circle['id']
        print(circleData)
        user_input = input('Enter circle name: ')
        self.circleID = circleData[user_input]
        return f'{user_input} has been set as the active cirle'

    def get_me(self):

        return requests.get('https://www.life360.com/v3/users/me', headers=self.headers).json()

    def get_circles(self):
        
        return requests.get('https://www.life360.com/v3/circles.json', headers=self.headers).json()
    
    def get_code(self):
        return requests.get(f'https://www.life360.com/v3/circles/{self.circleID}/code', headers=self.headers).json()

    def get_messages(self):

        return requests.get(f'https://www.life360.com/v3/circles/{self.circleID}/messages', headers=self.headers).json()

    def get_history(self):

        return requests.get(f'https://www.life360.com/v3/circles/{self.circleID}/members/history', headers=self.headers).json()['locations']

    def get_emergency_contacts(self):

        return requests.get(f'https://www.life360.com/v3/circles/{self.circleID}/emergencyContacts', headers=self.headers).json()

    def get_circle_info(self):
        
        users = []

        data = requests.get(f'https://www.life360.com/v3/circles/{self.circleID}', headers=self.headers).json()
        group = {
            'ID': data['id'],
            'Group Name': data['name'],
            'Member Count': data['memberCount'],
            'unreadMessages': data['unreadMessages'],
            'unreadNotification': data['unreadNotifications'],
            'members': data['members']
        }
        for person in group['members']:

            user = {
                'ID': person['id'],
                'First': person['firstName'],
                'Last': person['lastName'],
                'Address1': person['location']['address1'],
                'Address2': person['location']['address2'],
                'Since': time.ctime(person['location']['since']),
                'inTransit': binary_string(person['location']['inTransit']),
                'isDriving': binary_string(person['location']['isDriving']),
                'Speed': speedProcess(person['location']['speed']*2.23),        # 2.23 is an approximation of the conversion rate to MPG
                'Sharing': binary_string(person['features']['shareLocation']),
                'Battery': person['location']['battery'],
                'wifiState': binary_string(person['location']['wifiState']),
                'Phone': person['loginPhone'],
                'Email': person['loginEmail'],
                'Latitde': person['location']['latitude'],
                'Longitude': person['location']['longitude'],
                'createAt': time.ctime(int(person['createdAt']))
            }
            users.append(user)
        return users

    def help(self):
        return '''[COMMANDS]
get_me:\t\t\t\tInformation about account used to login.
get_circles:\t\t\tUsers circle information.
get_code:\t\t\tGet active code if any.
get_messages:\t\t\tGet all messages of the account user to login.
get_history:\t\t\tGet history of users in the circle.
get_emergency_contacts:\t\tGet emergency contact information of account used to login.
get_circle_info:\t\t\tGet current information of all users in the circle.'''

def main():

    function_dict = {'get_me': life360.get_me, 'get_circles': life360.get_circles,
                    'get_code': life360.get_code, 'get_messages': life360.get_messages,
                    'get_history': life360.get_history, 'get_emergency_contacts': life360.get_emergency_contacts,
                    'set_circle': life360.set_circle, 'help': life360.help}

    print("Start by setting the circle you want to track(set_circle).")
    print("Type: 'help' for a list of commands.")

    while True:
        user_input = input('Enter: ')
        user_input.lower()
        if user_input in function_dict:
            print(function_dict[user_input]())
        elif user_input == 'help':
            help()
        elif user_input == 'get_circle_info':
            print('control-c to break loop')
            print('beginning...')
            time.sleep(3)
            try: 
                while True:
                    print(life360.get_circle_info())
            except KeyboardInterrupt:
                print(KeyboardInterrupt)
        else:
            print('Invalid input. Try Again.')

if __name__ == '__main__':
    life360 = Life360('USER_EMAIL', 'USER_PASSWORD')
    main()