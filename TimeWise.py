import pandas as pd

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#Collect user data
def collect_user_data():
    # Ask the user for input
    tasks_completed = int(input("Enter the total number of tasks to complete: "))
    breaks_taken = int(input("Enter the total number of breaks you want to take: "))
    preferred_working_hours = int(input("Enter your preferred working hours per day: "))
    distractions = int(input("Enter the total number of distractions you may encounter: "))
    deadlines_missed = int(input("Enter the total number of deadlines you may miss: "))
    hours_slept = int(input("Enter the average number of hours you sleep per night: "))
    mood_level = int(input("Rate your overall mood level (1 to 10): "))


    # for i in range loops
    tasks_completed_data = [tasks_completed - i for i in range(5, 0, -1)]
    breaks_taken_data = [breaks_taken + i for i in range(0, 5)]
    preferred_working_hours_data = [preferred_working_hours - i for i in range(5, 0, -1)]
    distractions_data = [distractions + i for i in range(0, 5)]
    deadlines_missed_data = [deadlines_missed + i for i in range(0, 5)]
    hours_slept_data = [hours_slept - i for i in range(4, -1, -1)]
    mood_level_data = [mood_level - i for i in range(2, -3, -1)]


    # Create a dictionary with user input and generated data
    user_data = {
        'tasks_completed': tasks_completed_data,
        'breaks_taken': breaks_taken_data,
        'preferred_working_hours': preferred_working_hours_data,
        'distractions': distractions_data,
        'deadlines_missed': deadlines_missed_data,
        'hours_slept': hours_slept_data,
        'mood_level': mood_level_data,
        #add more specific data if needed
    }
    return pd.DataFrame(user_data)




# Analyze data and generate recommendations
def generate_recommendations(user_data):
    recommendations = {}


    total_breaks = sum(user_data['breaks_taken'])
    max_tasks_completed = max(user_data['tasks_completed'])
    min_preferred_working_hours = min(user_data['preferred_working_hours'])
    total_distractions = sum(user_data['distractions'])
    total_deadlines_missed = sum(user_data['deadlines_missed'])
    min_hours_slept = min(user_data['hours_slept'])
    mood_variation = max(user_data['mood_level']) - min(user_data['mood_level'])


    if total_breaks < 5:
        recommendations['regular_breaks'] = 'Take a 10-minute break every hour.'
    elif total_breaks >= 5 and total_breaks < 10:
        recommendations['regular_breaks'] = 'Take a 15-minute break every hour.'
    else:
        recommendations['regular_breaks'] = 'Take a 20-minute break every hour.'


    if max_tasks_completed <= 3:
        recommendations['time_limits'] = 'Set a 1-hour time limit for each task.'
    elif max_tasks_completed > 3 and max_tasks_completed <= 6:
        recommendations['time_limits'] = 'Set a 45-minute time limit for each task.'
    else:
        recommendations['time_limits'] = 'Set a 30-minute time limit for each task.'


    if min_preferred_working_hours >= 9:
        recommendations['meeting_optimization'] = 'Optimize meeting durations to 20 minutes.'
    elif min_preferred_working_hours < 9 and min_preferred_working_hours >= 7:
        recommendations['meeting_optimization'] = 'Optimize meeting durations to 30 minutes.'
    else:
        recommendations['meeting_optimization'] = 'Optimize meeting durations to 45 minutes.'


    if total_distractions < 10:
        recommendations['distraction_management'] = 'Implement focus techniques like the Pomodoro Technique.'
    elif total_distractions >= 10 and total_distractions < 20:
        recommendations['distraction_management'] = 'Use noise-canceling headphones to minimize distractions.'
    else:
        recommendations['distraction_management'] = 'Identify and eliminate sources of distractions in your workspace.'


    if total_deadlines_missed == 0:
        recommendations['deadline_management'] = 'Continue managing deadlines effectively.'
    elif total_deadlines_missed > 0 and total_deadlines_missed <= 3:
        recommendations['deadline_management'] = 'Review and adjust your task prioritization strategies.'
    else:
        recommendations['deadline_management'] = 'Implement a task tracking system to ensure timely completion.'


    if min_hours_slept >= 7:
        recommendations['sleep_quality'] = 'Maintain good sleep hygiene for optimal productivity.'
    elif min_hours_slept < 7 and min_hours_slept >= 5:
        recommendations['sleep_quality'] = 'Consider improving your sleep schedule for better cognitive function.'
    else:
        recommendations['sleep_quality'] = 'Prioritize sufficient sleep to avoid cognitive decline.'


    if mood_variation <= 3:
        recommendations['mood_management'] = 'Practice mindfulness techniques to improve mood stability.'
    elif mood_variation > 3 and mood_variation <= 6:
        recommendations['mood_management'] = 'Engage in regular physical activity for mood regulation.'
    else:
        recommendations['mood_management'] = 'Seek professional support to address mood fluctuations.'


    return recommendations


#Display recommendations
def display_recommendations(recommendations):
    for category, recommendation in recommendations.items():
        print(f'{category.capitalize()}: {recommendation}')




def update_calendar(recommendations):
    #credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    #service = build('calendar', API_VERSION, credentials=credentials)

    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
    AP_NAME = 'calendar'
    API_VERSION = 'v3'
    CALENDAR_ID = 'primary'
    CLIENT_SECRET_FILE = 'client-secret.json'

    service = build('calendar', API_VERSION, 'client-secret.json')
    
    event_1 = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

#event_2 = service.events().insert(calendarId='primary', body=event_1).execute()
#print('Event created: %s' % (event_2.get('htmlLink')))
    


def main():
    user_data = collect_user_data()
    recommendations = generate_recommendations(user_data)
    display_recommendations(recommendations)
    update_calendar(recommendations)



# Run  main function
if __name__ == '__main__':
    main()
