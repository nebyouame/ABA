import frappe
import requests
from requests.auth import HTTPDigestAuth
import json
from datetime import datetime, date, time, timedelta

def exc_date(day):
    switcher = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7,
    }

    return switcher.get(day, 'Invalid choice')

@frappe.whitelist()
def update_absent_time_for_employees(device, start_date, end_date, start_time, time_to_wait, has_exceptional_day, e_day, e_start_time, e_time_to_wait, abashift_id):
    device_doc = frappe.db.get_value('Device', device, ['ip_address', 'user_name', 'password'])
    
    # # Retrieve all employees
    employees = frappe.get_all('Employee', filters={'status': 'Active'}, fields=['name', 'attendance_device_id', 'shift_type'])

    for employee in employees:
        if employee['shift_type'] == abashift_id:
        #employee_number = frappe.db.get_value('Employee', employee.first_name, 'attendance_device_id')
            employee_number=employee['attendance_device_id']
            print(employee_number)
            absent_time = calculate_absent_time(device_doc, employee_number, start_date, end_date, start_time, time_to_wait, has_exceptional_day, e_day, e_start_time, e_time_to_wait)
            
            # # Update the specific field in the employee's doctype with the calculated absent time
            frappe.db.set_value('Employee', employee['name'], 'absent_time', absent_time)

def calculate_absent_time(device_doc, employee_number, start_date, end_date, start_time, time_to_wait, has_exceptional_day, e_day, e_start_time, e_time_to_wait):
    def attendance(Hikivision_Username, Hikivision_Password, Hikivision_IP, employeeNo, day):
        attendance_url = f"http://{Hikivision_IP}/ISAPI/AccessControl/AcsEvent?format=json"
        payload = json.dumps({
            "AcsEventCond": {
                "searchID": f"{employeeNo}",
                "searchResultPosition": 0,
                "maxResults": 1,
                "major": 5,
                "minor": 38,
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
            auth=HTTPDigestAuth(Hikivision_Username, Hikivision_Password)
        )

        if attendance_response.status_code != 200:
            return False
        
        attendance_data = attendance_response.json()
        checkIn_Time = attendance_data["AcsEvent"]
        return checkIn_Time

    count = timedelta(hours=0)
    delta = timedelta(days=1)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    exception_day = exc_date(e_day)
    weekDay = start_date.weekday() + 1

    while start_date <= end_date:
        data = attendance(device_doc[1], device_doc[2], device_doc[0], employee_number, datetime.strftime(start_date, '%Y-%m-%d'))
        if data['totalMatches'] != 0:
            data = data["InfoList"][0]["time"]
            if data:
                start_time1 = datetime.strptime(start_time, '%H:%M:%S')
                time_to_wait1 = datetime.strptime(time_to_wait, '%H:%M:%S')
                
                if has_exceptional_day:
                    if weekDay == 7:
                        weekDay = 0
                    if weekDay == exception_day:
                        start_time1 = datetime.strptime(e_start_time, '%H:%M:%S')
                        time_to_wait1 = datetime.strptime(e_time_to_wait, '%H:%M:%S')
                        weekDay = weekDay - 7
                    
                    weekDay = weekDay + 1
                    
                compare_Time = start_time1 + (time_to_wait1 - datetime(1900, 1, 1))
                compare_Time = datetime.strftime(compare_Time, '%H:%M:%S')
                compare_Time = datetime.strptime(compare_Time, '%H:%M:%S').time()
                checkIn_Time = datetime.fromisoformat(data).time()
                if checkIn_Time > compare_Time:
                    Scheduled_Time = time(8,0)
                    final = datetime.combine(date.today(), checkIn_Time) - datetime.combine(date.today(), Scheduled_Time)
                    count = count + final
                else:
                    pass
            else:
                pass
        start_date += delta
    rounded_count = round(count.total_seconds() / 3600, 1)
    print(rounded_count)
    return rounded_count
