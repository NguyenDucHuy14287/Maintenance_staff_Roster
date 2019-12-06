from obj import *

def main():
     path = 'EVENT/EVENT_MAY_2018.csv'
     may_2018 = month(path)
     # a = may_2018.get_month_info()
     day_in_month = len(may_2018.get_days_in_month())
     # may_2018.display_month_info()
     
     
     path = 'STAFF.csv'
     all_crew = crew(path)
     # a = all_crew.get_crew_info()
     # all_crew.display_crew_info()
     all_crew.set_init_crew_schedule(day_in_month)
     # for i in crew_mem:
     #      print(i,":",all_crew.crew_info[i].get_staff_schedule())
     # print(all_crew.crew_members)
     roster = {'Staff_id':[],'Level':[]}
     for i in range(1,day_in_month+1):
          roster[i] = []

     for i in all_crew.crew_members:
          roster['Staff_id'] += [i]  
          roster['Level'] += [all_crew.crew_info[i].staff_real_level]
          for j in range(1,day_in_month+1):
               roster[j] += [all_crew.crew_info[i].staff_schedule[j]]
     df = DataFrame(roster, columns= list(roster.keys()))
     export_csv = df.to_csv('ROSTER.csv', index = None, header=True)


     print(may_2018.display_month_info())


def test():
     Cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
        'Price': [22000,25000,27000,2]
        }

     df = DataFrame(Cars, columns= ['Brand', 'Price'])
     export_csv = df.to_csv('ROSTER.csv', index = None, header=True)
     print(df)
     print(type(Cars))


main()
# test()
