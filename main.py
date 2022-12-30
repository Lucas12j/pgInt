import pgint, time, yaml, datetime

with open('conf.yaml','r') as file:
    conf = yaml.full_load(file)

def infoLog(message):
    with open('info.log','a') as file:
        file.write(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')+" ----- "+message+"\n")

pgint = pgint.PgInt(conf)


while True:
    a = time.time()
    try:

        for i in pgint.getDownSensors():
            if pgint.ticketVerify( "999"+str(i['objid_raw']) ):
                pgint.addFollowUp(
                    "999"+str(i['objid_raw']),  
                    i['message_raw']
                )
            else:
                pgint.createTicket(
                    "999"+str(i['objid_raw']), 
                    "2", 
                    i['group_raw']+" - "+i['device_raw']+" - "+i['sensor_raw'],
                    i['message_raw'],
                    i['priority_raw'],
                    "1",
                    "1"
                    )

        infoLog("Successful Process")

        time.sleep(conf['Check-Interval'])

    except Exception as e:
        infoLog(repr(e))
        time.sleep(conf['Retry-Interval'])

   

