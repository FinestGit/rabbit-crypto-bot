import robin_stocks as r
import datetime

class sessionBot:
    def __init__(self):
        self.__username = ''
        self.__password = ''
        self.__sessionLength = 0
        self.__sessionStartTime = ''
    
    def getUsername(self):
        if self.__username == '':
            print("Session Bot: Username has not been set")
            return ''
        return self.__username
    
    def getSessionLength(self):
        if self.__sessionLength <= 0:
            print("Session Bot: Session Length has not been set")
            return 0
        return self.__sessionLength
    
    def setUsername(self, username):
        if username == '':
            print("Session Bot: Cannot set Username to an empty string")
            return
        self.__username = username
        
    def setPassword(self, password):
        if password == '':
            print("Session Bot: Cannot set Password to an empty string")
            return
        self.__password = password
    
    def setSessionLength(self, sessionLength):
        try:
            i_sessionLength = int(sessionLength)
        except ValueError:
            print("Session Bot: Cannot set Session Length to a value that is not an int")
        if i_sessionLength <= 0:
            print("Session Bot: Cannot set Session Length to a number less than 1")
            return
        self.__sessionLength = i_sessionLength
    
    def isSessionExpired(self):
        if self.__sessionStartTime == '' or self.__sessionLength <= 0:
            print("Session Bot: Session hasn't started, therefore cannot be expired")
            return
        now = datetime.datetime.now()
        dt_sessionStart = datetime.datetime.strptime(self.__sessionStartTime, '%Y-%m-%d %H:%M:%S.%f')
        timeDiffSessionStart = now - dt_sessionStart
        if (timeDiffSessionStart.total_seconds() > self.__sessionLength):
            print("Session Bot: Session has expired")
            self.sessionStart()
        
    def sessionStart(self):
        if (self.__username == '') or (self.__password == '') or (self.__sessionLength <= 0):
            print("Session Bot: Cannot start session, settings not correct")
            return
        try:
            r.logout()
        except:
            print("Session Bot: Session not started, starting new session")
        print("\nSession Starting")
        Result = r.login(self.__username, self.__password, expiresIn=self.__sessionLength, by_sms=True)
        self.__sessionStartTime = str(datetime.datetime.now())
    
    def sessionEnd(self):
        try:
            r.logout()
        except:
            print("Session Bot: Session not started")