from typing import Tuple
from datetime import datetime

queue = []
patterns = ["{}후에 {}",
            "{}에 {}"]


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
    :return: 없으면 -1, 있다면 인덱스
    """
    pass


def parse_time(text: str, pattern: int) -> datetime:
    pass


def parse_message(text: str, pattern: int) -> str:
    pass


def main():
    global queue
    queue.append(parse(input()))
    queue = sorted(queue)

if __name__ == '__main__':
    main()
