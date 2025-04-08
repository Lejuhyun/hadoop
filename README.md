# hadoop command

-`ls` 파일 리스트 확인
    - `hdfs dfs -ls /`
    - hdfs dfs -ls <확인하고 싶은 경로>

-`mkdir` 새로운 디렉토리 생성
    - `hdfs dfs mkdir`
    - hdfs dfs -mkdir <생성하고싶은 폴더 이름>

-`put` 지정 위치에 파일 업로드
    - hdfs dfs -put <업로드할 파일 경로> <업로드할 위치>

-`cat` 파일 출력
    - hdfs dfs -cat <출력하고 싶은 파일 경로>

-`head`, -`tail`
    -hdfs dfs -head <출력하고 싶은 파일 경로>
    -hdfs dfs -tail <출력하고 싶은 파일 경로>

-`rm`
    -hdfs dfs -rm /<삭제하고 싶은 파일 경로>

    -폴더를 삭제할 경우 
    -hdfs dfs -rm -r /<삭제하고 싶은 폴더 경로>
# Map Reduce
## 1. Map(데이터에서 필요한 정보를 뽑아낸다)
- 입력: 한 줄씩 텍스트(데이터)를 받아온다
- 출력: (Key, Value) 형태로 내보냄
## 2. Reducer (같은 Key에 해당하는 value들을 계산해서 결과 출력)

# Word Count

## 1. text.txt 생성하긔
```txt
apple hello world
hello hello apple
world
apple world
hello world
world hello
world
world
apple
```

## 2. mapper.py 생성하긔
```python
import sys

    for line in sys.stdin:
    line = line.strip()
    words = line.split()
    # ['apple', 'hello', 'world']가 words에 담겨있음

    for word in words:
        print(f'{word}\t1')
```
- for line in sys.stdin: 외부에서 들어오는 데이터를 한 줄씩 읽는다
- line.strip(): 공백 문자를 제거해주는 함수
- line.split(): 문장을 띄어쓰기 기준으로 잘라준다
    - "apple banana cherry" => ['apple', 'banana', 'cherry'] 
- f'{word}\t1': 단어가 1번 나왔다는 뜻 
    - apple 1 
    - banana 1
    - cherry 1
- Mapper는 데이터를 → (key, value) 형태로 내보낸다 => Hadoop에서 key를 기준으로 자동으로 정렬해준다!!
- Reducer는 같은 key끼리 모아서 더해준다 => 해당 단어가 총 몇번 나왔는지 세주는 역할

## 3. reducer.py 생성하기

```python
#!/user/bin env python3
import sys

# apple 1
# apple 1
# hello 1
# hello 1
# hello 1
# ...

last_word = None
total_count = 0

for line in sys.stdin:
    word, value = line.split('\t') # hello	1 => "hello" , "1"
    value = int(value)

    if last_word == word:
        total_count += value
    else:
        if last_word is not None:
            print(f'{last_word}\t{total_count}')
        last_word = word
        total_count = value

if last_word == word:
    print(f'{last_word}\t{total_count}') # key 와 value를 구별할 때 tab을 이용하는게 규칙임
```
- 맨 첫 시작 ex) apple 1 
    - => last_word = None 
    - => else의 if문 밖으로 간다 
    - => last_word = apple , total_count = 1
- apple 1인 경우
    - => last word == apple
    - => total_count = 2
- banana 1인 경우
    - => else: 로 간다
    - => apple 2 를 프린트해준다
    - => last word = banana, total_count = 1
- 맨 마지막 ex) cherry 1
    - => for 문 밖으로 나온다
    - => cherry 1 을 프린트 해준다
- **print할때는 {key}\t{value} tab으로 구별해주는게 규칙이다!!**

## 4. 실행 (경로 포함)
- hadoop jar ~/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -input /input/text.txt -output /output/wordcount -mapper /home/ubuntu/damf2/hadoop/0.wordcount/mapper.py  -reducer /home/ubuntu/damf2/hadoop/0.wordcount/reducer.py

- hadoop jar ~/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \: 
    - Hadoop Streaming은 텍스트 데이터를 처리할 수 있도록 해주는 인터페이스, 
    - Hadoop 설치 경로에 있는 Streaming jar 파일
-  -input /input/text.txt \: 입력 파일 경로(text.txt를 기준으로 분석 시작)
-  -output /output/wordcount \: 출력 파일 경로 
-  -mapper 'python3 /home/ubuntu/damf2/hadoop/0.wordcount/mapper.py' \: 각 라인을 받아서 원하는 단위로 쪼개는 역할
-  -reducer 'python3 /home/ubuntu/damf2/hadoop/0.wordcount/reducer.py': mapper가 출력한 걸 단어별로 합치는 역할
- ex) text.txt: the cat in the hat => mapper.py: the 1 cat 1 in 1 the 1 hat 1 => reducer.py: the 2 cat 1 in 1 hat 1

# CHMOD
- rws/rws/rws (owner/group/others)
    - r: 읽기 w: 쓰기 x: execute
    - -rw-r--r-- 1: owner는 읽고 쓰기, group은 읽기, others는 읽기 권한이 있음
    - chmod : 권한을 변경해주는 역할 
    - chmod +x mapper.py: mapper.py에 있는 모든 사람에게 x 권한을 부여해줌
    - chmod -x mapper.py
    - chmod 755 mapper.py(7: rwx, 5: rx, 5: rx) =>  rwxr-xr-x 1 이렇게 바꿔줌
    - chmod 777 maper.py




# 영화데이터 평균 구하기
```shell
cd ~/damf2/data/
hdfs dfs -put ml-25m/ratings.csv /input
```
- localhost:9870에서 hadoop => input => ratings.csv가 올라가 있어야한다

## 1. mapper.py 생성하기
```python
import sys
for line in sys.stdin:
    line = line.strip() # 좌우에 공백이 있으면 공백 제거
    
    fields = line.split(',') # 데이터를 쉼표를 기준으로 split해준다
    # ['1', '296', '5.0', '11133451414'] => movieid와 rating만 필요
    movie_id = fields[1]
    rating = fields[2]

    print(f'{movie_id}\t{rating}') # 출력 
```
- 1. line.strip()
- 2. line.split() => key와 value를 각각 저장
- 3. print 하기 => print(f'{key}\t{value}')

## 2. reducer.py 생성하기
```python
import sys

# '296\t5.0' 이라는 데이터가 들어올것이다
current_movie_id = None
current_sum = 0
current_count = 0

for line in sys.stdin:
    movie_id, rating = line.split() # 빈칸을 기준으로 split해준다

    try:
        rating = float(rating) # 소수로 바꾸어준다
        # 첫번째줄은 어떤 데이터인지 설명해주는거라서 에러가 발생함
    except: # 에러가 발생한다면
        continue # for문을 무시하고 다음 for문으로 넘어가세요      
    # 123, 5.0 
    # 123, 3.5
    # 123, 4.0
    # 234, 4
    # 345, 4

    if current_movie_id == movie_id:
        current_count += 1
        current_sum += rating
    else: 
        if current_movie_id is not None:
            # 다음 영화로 넘어가면 평균을 보여준다
            current_average = current_sum / current_count
            print(f'{current_movie_id}\t{current_average}')

        # sum과 count를 초기화 시키기
        # 처음 시작할 때도 current_movie_id가 1번 영화의 movie_id로 설정이 된다
        current_movie_id = movie_id
        current_count = 1
        current_sum = rating
# 마지막 영화는 비교할게 없음
current_avg = current_sum/ current_count
print(f'{current_movie_id}\t{current_avg}')

```

# log time
## 1. input 데이터 넣기
```shell
hdfs dfs -put access.log /input
```

## 2. mapper.py 작성하기
```python
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
```
- import re : 정규표현식 사용할거다
- re.compile: 문자열 형태의 정규표현식 -> 객체로 생성해줌
- pattern.search: 문자열중에서 정규표현식과 일치하는 부분을 찾아준다



## 3. reducer.py 작성하기
```python
import sys

last_hour = None
total_count = 0

# 03 1
# 03 1
# 04 1
# 05 1
# ....
for line in sys.stdin:
    line = line.strip()

    hour, value = line.split() # 띄어쓰기를 기준으로 나눠서 본다
    value = int(value) # 1은 숫자이므로 int로 바꿔줌

    if last_hour == hour:
        total_count += value
    else:
        if last_hour is not None:
            print(f'{last_hour}\t{total_count}')

        # 초기화 시켜주기
        last_hour = hour
        total_count = value
        
print(f'{last_hour}\t{total_count}')
```