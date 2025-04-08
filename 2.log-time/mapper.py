import sys
import re # 파이썬 내부에 구현되어있는 정규표현식 : reqular expression

# :03:56:14
time_pattern = re.compile(r':(\d{2}):(\d{2}):(\d{2})') # 정규표현식 => \d: 숫자 들어옴, \d{2}: 숫자가 두칸 들어와야 한다

for line in sys.stdin:
    line = line.strip()

    match = time_pattern.search(line) # 한 줄에 있는 데이터에서 정규표현식과 일치하는 데이터만 match에 저장한다

    if match: # match라는 값이 있으면
        hour = match.group(1) # group(1) : 소괄호로 묶어놓은 그룹 첫번째 => 시간만 추출한다
        print(f'{hour}\t1')