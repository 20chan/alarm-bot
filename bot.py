from typing import Tuple
from datetime import datetime, timedelta
import re

queue = []
delta_regex = re.compile(
    '((?P<days>\d+?)일)?[ ]*((?P<hours>\d+?)(시간?))?[ ]*((?P<minutes>\d+?)분)?[ ]*((?P<seconds>\d+?)초)?')
date_regex = re.compile(
    '((?P<year>\d+?)년)?[ ]*((?P<month>\d+?)월)?[ ]*((?P<day>\d+?)일)?[ ]*'
    '((?P<hour>\d+?)(시간?))?[ ]*((?P<minute>\d+?)분)?[ ]*((?P<second>\d+?)초)?')


def parse(text: str) -> Tuple[datetime, str]:
    pat = match(text)
    if 0 <= pat:
        time = parse_time(text, pat)
        msg = parse_message(text, pat)
        return time, msg

    raise SyntaxError("파싱 에러")


def match(text: str) -> int:
    """
    문자열이 패턴과 일치하는지 확인
    :param text: 문자열
    :return: 없으면 -1, Span이라면 0, Date라면 1
    """
    if re.match('.*(뒤에|후에).*', text) is not None:
        return 0
    if re.match('.*에.*', text) is not None:
        return 1
    return -1


def parse_time(text: str, pattern: int) -> datetime:
    if pattern == 0:  # Span
        parts = delta_regex.match(text)
        if parts is None:
            raise SyntaxError("시간 파싱 에러")
        parts = parts.groupdict()
        res = {}
        for p in parts.keys():
            if parts[p]:
                res[p] = int(parts[p])
        return datetime.now() + timedelta(**res)

    elif pattern == 1:  # Date
        parts = date_regex.match(text)
        if parts is None:
            raise SyntaxError("시각 파싱 에러")
        parts = parts.groupdict()
        res = {key: None for key in parts}
        keys = ['year', 'month', 'day', 'hour', 'minute', 'second']
        index = len(keys)
        for key in keys:
            if parts[key]:
                res[key] = parts[key]
                index = keys.index(key)
            elif keys.index(key) > index:
                res[key] = 1
        return datetime.today().replace(**res)


def parse_message(text: str) -> str:
    return str.strip(msg_regex.match(text).groupdict()['msg'])


def check_and_say():
    # global queue
    while True:
        if len(queue) > 0:
            print('와우')
            if queue[0][0] < datetime.now():
                print(queue.pop(0)[1])
        print('자')
        sleep(1)


def main():
    global queue
    th = threading.Thread(target=check_and_say())
    th.daemon = True
    th.start()
    while True:
        print('입력받자')
        queue.append(parse(input()))
        queue = sorted(queue)
        print('길이: ' + str(len(queue)))

if __name__ == '__main__':
    main()
