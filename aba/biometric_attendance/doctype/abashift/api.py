import frappe
import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime , date, time, timedelta

def exc_date(day):
    switcher = {
        "Monday" : 1,
        "Tuesday" : 2,
        "Wednsday" : 3,
        "Thursday" : 4,
        "Friday" : 5,
        "Saturday" : 6,
        "Sunday" : 7,
    }

    return switcher.get(day, 'Invalid coice')

@frappe.whitelist()
def get_attendance_for_all_employee(device,start_date,end_date,start_time,time_to_wait,has_exceptional_day,e_day,e_start_time,e_time_to_wait):
    device_doc = frappe.db.get_value('Device', device, ['ip_address','user_name','password'])


    def attendance(Hikivision_Username,Hikivision_Password,Hikivision_IP,employeeNo,day):
        attendance_url = f"http://{Hikivision_IP}/ISAPI/AccessControl/AcsEvent?format=json"
        payload = json.dumps({
        "AcsEventCond": {
            "searchID": f"{employeeNo}",
            "searchResultPosition": 0,
            "maxResults": 1,
            "major": 5,
            "minor": 38,
            # "startTime": "2024-03-05T06:00:49+03:00",
            # "endTime": "2024-03-05T18:00:49+03:00",
            "startTime": f"{day}T06:00:49+03:00",
            "endTime": f"{day}T18:00:49+03:00",
            "employeeNoString": f"{employeeNo}"
        }
        })
        headers = {
        'Content-Type': 'application/json'
        }

        attendance_response = requests.post(
            attendance_url,
            headers=headers,
            data=payload,
            auth=HTTPDigestAuth(Hikivision_Username,Hikivision_Password)
        )

        print(attendance_response)

        if attendance_response.status_code != 200:
            print("not 200")
            # print(attendance_response.json())
            return False
        
        attendance_data = attendance_response.json()
        checkIn_Time = attendance_data["AcsEvent"]
        return checkIn_Time
    

    count = timedelta(hours = 0)
    # for d in rrule(DAILY, dtstart=start_date, until=end_date):
    delta = timedelta(days=1)
    start_date = datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.strptime(end_date,'%Y-%m-%d')
    # exceptional day

    exception_day = exc_date(e_day)
    weekDay = start_date.weekday() + 1



    while (start_date <= end_date):
    # for d in range(1,8):
        data = attendance(device_doc[1],device_doc[2],device_doc[0],4,datetime.strftime(start_date, '%Y-%m-%d'))
        if data['totalMatches'] != 0:
            data = data["InfoList"][0]["time"]
            if data:
                start_time1 = datetime.strptime(start_time, '%H:%M:%S')
                time_to_wait1 = datetime.strptime(time_to_wait, '%H:%M:%S')
                
                if has_exceptional_day:
                    # To do
                    if weekDay == 7:
                        weekDay = 0
                    if weekDay == exception_day:
                        start_time1 = datetime.strptime(e_start_time, '%H:%M:%S')
                        time_to_wait1 = datetime.strptime(e_time_to_wait, '%H:%M:%S')
                        print(start_time1)
                        print(time_to_wait1)
                        weekDay = weekDay - 7
                    
                    weekDay = weekDay + 1
                    
                compare_Time = start_time1 + (time_to_wait1 - datetime(1900, 1, 1))
                compare_Time = datetime.strftime(compare_Time, '%H:%M:%S')
                compare_Time = datetime.strptime(compare_Time, '%H:%M:%S').time()
                checkIn_Time = datetime.fromisoformat(data).time()
                if checkIn_Time > compare_Time:
                    Scheduled_Time = time(8,0)
                    final = datetime.combine(date.today(), checkIn_Time) - datetime.combine(date.today(), Scheduled_Time)
                    print("final:",final)
                    count = count + final
                    print("count:",count)
                    print("________")
                else:
                    print("on time")
                
                
            else:
                print("error")
                break
        else:
            pass
        start_date += delta
    rounded_count = round(count.total_seconds() / 3600, 1)
    print(rounded_count)
    return rounded_count
    # return True
    