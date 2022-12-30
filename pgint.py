import requests, time, datetime

class PgInt():

    def __init__(self, conf):

        self.conf = conf
        self.urlGlpi = self.conf['Url-Api-Glpi']
        self.headers =  {
	    			        'Content-Type': self.conf['Content-Type'],
	    			        'App-Token': self.conf['App-Token'],
	    			        'Session-Token': self.conf['Session-Token'] 
	    		        }


    def getDownSensors(self):
        url = self.conf['Url-Api-Prtg']
        r = requests.get(url).json()['sensors']
        return [
					i for i in r if (
										('ES/NO' in i['sensor'].upper()) or 
										('ES/N0' in i['sensor'].upper()) or 
										('JUNIPER' in i['device'].upper())
									) and 
										i['status_raw'] == 5
				]

    def createTicket(self, ticketID, _users_id_requester, name, content, priority, type, itilcategories_id):
        url = self.urlGlpi+"Ticket"
        data = {
	    			"input":{	
	    						"id": ticketID,
	    						"_users_id_requester": _users_id_requester,
	    						"name": name,
	    						"content": datetime.datetime.now().strftime('%d/%m/%Y %H:%M') + "\n\n" + content,
	    						"priority": priority,
	    						"type": type,
	    						"itilcategories_id": itilcategories_id
	    					}
	    		}

        r = requests.post(url=url, headers=self.headers, json=data).json()

    def addFollowUp(self, ticketID, content):

        url = self.urlGlpi+"Ticket/"+ticketID+"/TicketFollowup/"
        data = {
				"input": 
					{
						"tickets_id": ticketID,
						"is_private": "0",
						"requesttypes_id":"6",
						"content": datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "\n\n" + content,
					}
			}
        r = requests.post(url=url, headers=self.headers, json=data).json()

    def ticketVerify(self, ticketID):

        url = self.urlGlpi+"Ticket/"+ticketID
        r = requests.get(url=url, headers=self.headers).json()
        return isinstance(r, dict) 
        

