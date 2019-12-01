from obj import *

def main():
     path = 'EVENT/EVENT_MAY_2018.csv'
     may_2018 = month(path)
     # a = may_2018.get_month_info()
     day_in_month = may_2018.get_days_in_month()
     # may_2018.display_month_info()
     
     
     path = 'STAFF.csv'
     all_crew = crew(path)
     # a = all_crew.get_crew_info()
     crew_mem = all_crew.get_crew_members()
     # all_crew.display_crew_info()
     all_crew.set_init_crew_schedule(len(day_in_month))
     for i in crew_mem:
          print(i,":",all_crew.crew_info[i].get_staff_schedule())


     

     



main()

