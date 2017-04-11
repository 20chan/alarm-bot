from typing import Tuple
from datetime import datetime, timedelta
import re
import threading
from time import sleep
import tweepy

ck, cs, tk, ts = open('key.txt', encoding='utf-8').read().split()
auth = tweepy.OAuthHandler(ck, cs)
auth.set_access_token(tk, ts)
api = tweepy.API(auth, wait_on_rate_limit=True)

queue = []
delta_regex = re.compile(
    '((?P<days>\d+?)일)?[ ]*((?P<hours>\d+?)(시간?))?[ ]*((?P<minutes>\d+?)분)?[ ]*((?P<seconds>\d+?)초)?')
date_regex = re.compile(
    '((?P<year>\d+?)년)?[ ]*((?P<month>\d+?)월)?[ ]*((?P<day>\d+?)일)?[ ]*'
    '((?P<hour>\d+?)(시간?))?[ ]*((?P<minute>\d+?)분)?[ ]*((?P<second>\d+?)초)?')
msg_regex = re.compile('.*에(?P<msg>.*)')


def parse(text: str) -> Tuple[datetime, str]:
    pat = match(text)
    if 0 <= pat:
        time = parse_time(text, pat)
        msg = parse_message(text)
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
        res = {key: None for key in parts if parts[key]}
        keys = list(parts.keys())
        index = len(keys)
        for key in keys:
            if parts[key]:
                res[key] = int(parts[key])
                index = keys.index(key)
            elif keys.index(key) > index:
                res[key] = 1
        return datetime.today().replace(**res)


def parse_message(text: str) -> str:
    return str.strip(msg_regex.match(text).groupdict()['msg'])


def check_and_say():
    while True:
        if len(queue) > 0:
            if queue[0][0][0] < datetime.now():
                api.update_status('@'+queue[0][1]+' '+queue[0][0][1])
                print('Popped' + queue.pop(0)[0][1])
        sleep(0.5)


class Listener(tweepy.StreamListener):
    def on_status(self, status):
        global queue
        try:
            if status.text.startswith('@dailycommit_bot'):
                print(status.user.screen_name + ' : ' + status.text)
                queue.append((parse(status.text), status.user.screen_name))
                queue = sorted(queue)
        except Exception as ex:
            print(ex)


def main():
    th = threading.Thread(target=check_and_say)
    th.start()
    listener = Listener()
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(track=['dailycommit_bot'])

if __name__ == '__main__':
    main()
