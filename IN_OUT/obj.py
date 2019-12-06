import pandas as pd
from pandas import DataFrame
import csv

def remove_all_element_from_list(ls,el):
     ls1 = ls.copy()
     while el in ls1 : ls1.remove(el)
     return ls1   

def read_data(file_path):
     raw_data = pd.read_csv(file_path,sep=',',keep_default_na=False)
     return raw_data

def convert_list_str_to_int(lst):
    for i in range(len(lst)):
        lst[i] = int(lst[i]) 

    return lst

class shift:
    "Define shift requirement format"

    def __init__(self,B1=0,B2=0,A=0,MC=0,DMM=0):
        "All requirement positions"
        self.B1 = B1
        self.B2 = B2
        self.A  = A
        self.MC = MC
        self.DMM = DMM

    def get_shift_info(self):
        "Get number of each position"
        return [self.B1, self.B2, self.A, self.MC, self.DMM]

    def set_shift_info(self,B1=0,B2=0,A=0,MC=0,DMM=0):
        "Set number of each position"
        self.B1 = B1
        self.B2 = B2
        self.A  = A
        self.MC = MC
        self.DMM = DMM

    def add_shift_info(self,B1=0,B2=0,A=0,MC=0,DMM=0):
        "Add number of each position for each event"
        self.B1 += B1
        self.B2 += B2
        self.A  += A
        self.MC += MC
        self.DMM += DMM


class day:
    "Define day requirement format"

    def __init__(self):
        #Make default value for 2 shifts of daily day
        self.day_shift = shift(1,1,2,2,0)
        self.night_shift = shift(3,2,7,7,1)

    def display_day_info(self):
        day_info = self.day_shift.get_shift_info()
        night_info = self.night_shift.get_shift_info()
        print("Day shift:", day_info) 
        print("Night shift:", night_info)

    def check_day_info(self,ls_event):
        for event in ls_event:
            if event == 'A01':
                self.night_shift.set_shift_info(4,3,7,10,1)
            elif event == 'A02':
                self.night_shift.set_shift_info(5,4,8,10,1)
            elif event == 'EC':
                self.night_shift.add_shift_info(2,1,3,3,0)
            elif event == 'APU':
                self.night_shift.add_shift_info(0,2,0,2,0)


class month:
    "Define day requirement format"

    def __init__(self,path):
        self.month_info, self.days_in_month = self.process_month_info(path)

    def process_month_info(self,path):
        event_days = read_data(path).to_dict()
        del event_days['CRAFT_ID']
        days_in_month = convert_list_str_to_int(list(event_days.copy().keys()))
        no_event_days = []
        for x in event_days.keys():
            event_days[x] = remove_all_element_from_list(list(event_days[x].values()),'DC')
            if event_days[x] == []:
                no_event_days = no_event_days + [x]

        for x in no_event_days:
            del event_days[x]

        month_info = {}
        for i in days_in_month:
            month_info[i] = day()
            if i in event_days.keys():
                month_info[i].check_day_info(event_days[i])
        
        return month_info,days_in_month

    def get_month_info(self):
        return self.month_info

    def get_days_in_month(self):
        return self.days_in_month

    def display_month_info(self):
        print(self.month_info)
        print(self.days_in_month)
        for i in self.month_info.keys():
            print("Day",i)
            print(self.month_info[i].display_day_info())


class staff:
    "Define staff format"
    
    def __init__(self,staff_id=0,staff_level='MC',staff_real_level='MECH',crew_number=0):
        self.staff_id = staff_id
        self.staff_level = staff_level
        self.staff_real_level = staff_real_level
        self.crew_number = crew_number
        self.staff_schedule = None

    def get_staff_info(self):
        return [self.staff_id, self.staff_level, self.crew_number]
    
    def get_staff_schedule(self):
        return self.staff_schedule

    def set_staff_info(self,staff_id=0,staff_level='MC',staff_real_level='MECH',crew_number=0):
        self.staff_id = staff_id
        self.staff_level = staff_level
        self.staff_real_level = staff_real_level
        self.crew_number = crew_number

    def display_staff_info(self):
        print(self.staff_id, self.staff_level, self.staff_real_level, self.crew_number)

    def set_init_staff_schedule(self,day=30): # all day is off
        self.staff_schedule = {}

        for i in range(1,day+1):
            self.staff_schedule[i] = 'O'
        
    def set_staff_schedule(self,day=1,value='O'):    #30 days in months
        self.staff_schedule[day] = value


class crew:
    "Define crew format"

    number_of_crew = 8

    def __init__(self,path):
        self.crew_info, self.crew_members = self.process_crew_info(path)

    def process_crew_info(self,path):
        raw_data = read_data(path).to_dict()
        crew_info = {}
        crew_members = list(raw_data['staff_id'].values())

        for i in raw_data['staff_id'].keys():
            crew_info[raw_data['staff_id'][i]] = staff(
                raw_data['staff_id'][i],
                raw_data['level'][i],
                raw_data['real_level'][i],
                raw_data['crew'][i]
            )
        
        return crew_info, crew_members

    def get_crew_info(self):
        return self.crew_info

    def get_crew_members(self):
        return self.crew_members

    def display_crew_info(self):
        print(self.crew_info)
        print(self.crew_members)
        for i in self.crew_members:
            self.crew_info[i].display_staff_info()

    def set_init_crew_schedule(self,day=30):
        for i in self.crew_members:
            self.crew_info[i].set_init_staff_schedule(day)
        
        for i in range(1,self.number_of_crew+1):    #except crew DMM
            for j in range(1,day+1):
                if j%8 == i%8:
                    schedule_value = 'D'
                elif j%8 in [(i+1)%8,(i+2)%8,(i+3)%8]:
                    schedule_value = 'N'
                else:
                    schedule_value = 'O'

                for k in self.crew_members:
                    if self.crew_info[k].crew_number == i:
                        self.crew_info[k].set_staff_schedule(j,schedule_value)


class roster:       ##no need
    "Define roster schedule format"

    def __init__(self,month_path,staff_path):
        self.roster_info = None #evalueate 
        self.month_info, self.crew_info = process_roster_info(month_path,staff_path)

    def process_roster_info(self,month_path,staff_path):
        month_info = month(month_path)
        crew_info = crew(staff_path)
        return month_info, crew_info












        


