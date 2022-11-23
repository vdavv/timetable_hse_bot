import requests
import json
import datetime as dt
from datetime import datetime

today_v = datetime.today().strftime('%Y-%m-%d')
today_plus7_v = (dt.datetime.now() + dt.timedelta(days=7)).strftime('%Y-%m-%d')


# https://ruz.hse.ru/api/schedule/group/129742?start=2022.11.21&finish=2022.11.27&lng=1
def get_schedule_by_group(group='129742', start=today_v, finish=today_plus7_v):
    to_json = []
    schedule_api = "https://ruz.hse.ru/api/schedule/group/{}?start={}&finish={}&lng=1"
    response = requests.get(schedule_api.format(group, start, finish))
    content = json.loads(response.content)
    for lesson in content:
        lesson_module = {
            'auditorium': lesson.get('auditorium'),
            'url1': lesson.get('url1'),
            'beginLesson': lesson.get('beginLesson'),
            'lessonNumberStart': lesson.get('lessonNumberStart'),
            'building': lesson.get('building'),
            'date': lesson.get('date'),
            'dayOfWeekString': lesson.get('dayOfWeekString'),
            'discipline': lesson.get('discipline'),
            'endLesson': lesson.get('endLesson'),
            'lessonNumberEnd': lesson.get('lessonNumberEnd'),
            'group': lesson.get('group'),
            'groupOid': lesson.get('groupOid'),
            'groupUID': lesson.get('groupUID'),
            'group_facultyname': lesson.get('group_facultyname'),
            'group_facultyoid': lesson.get('group_facultyoid'),
            'kindOfWork': lesson.get('kindOfWork'),
            'lecturer_rank': lesson.get('lecturer_rank'),
            'lecturer_title': lesson.get('lecturer_title'),
            'lecturerEmail': lesson.get('lecturerEmail'),
            'lecturerOid': lesson.get('lecturerOid'),
            'lecturerUID': lesson.get('lecturerUID'),
            'author': lesson.get('author')
        }
        to_json.append(lesson_module)
    json_object = json.dumps({'data': to_json}, indent=12, ensure_ascii=False)
    # 'data{n}.json' - file where vacancy cards are parsed, n - arbitrary number
    with open("data.json", "w", encoding='utf8') as outfile:
        outfile.write(json_object)


# https://ruz.hse.ru/api/search?term=БПАД22&type=group
def get_group_by_name(group_name='БПАД222'):
    group_api = 'https://ruz.hse.ru/api/search?term={}&type=group'
    response = requests.get(group_api.format(group_name))
    content = response.json()
    if not content:
        return None
    return content[0].get('id')


"""if __name__ == '__main__':
    print(get_group_by_name('БПАД222'))"""

get_schedule_by_group('129742', today_v, today_plus7_v)
