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
            if parts[p] is not None:
                res[p] = int(parts[p])
        return datetime.now() + timedelta(**res)

    elif pattern == 1:  # Date
        parts = date_regex.match(text)
        if parts is None:
            raise SyntaxError("시각 파싱 에러")
        parts = parts.groupdict()
        res = {}
        keys = list(parts.keys())
        for i in range(len(keys)):
            if parts[keys[i]] is not None:
                res[keys[i]] = int(parts[keys[i]])
                for j in range(i, len(keys)):
                    res[keys[j]] = 0
        return datetime.today().replace(**res)


def parse_message(text: str, pattern: int) -> str:
    pass


def main():
    '''
    global queue
    queue.append(parse(input()))
    queue = sorted(queue)
    '''
    parse_time('2일 22시간 100초', 0)

if __name__ == '__main__':
    main()
