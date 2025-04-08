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

- mapper.py

```
import sys

    for line in sys.stdin:
    line = line.strip()
    words = line.split()
    # ['apple', 'hello', 'world']가 words에 담겨있음

    for word in words:
        print(f'{word}\t1')
```

- reducer.py

```
import sys

last_word = None
total_count = 0

for line in sys.stdin:
    word, value = line.split('\t')
    value = int(value)

    if last_word == word:
        total_count += value
    else:
        if last_word is not None:
            print(f'{last_word}\t{total_count}')
        last_word = word
        total_count = value

if last_word == word:
    print(f'{last_word}\t{total_count}')
```

실행 (경로 포함)
hadoop jar ~/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -input /input/text.txt -output /output/wordcount -mapper /home/ubuntu/damf2/hadoop/0.wordcount/mapper.py  -reducer /home/ubuntu/damf2/hadoop/0.wordcount/reducer.py

# CHMOD
- rws/rws/rws (owner/group/others)
    - r: 읽기 w: 쓰기 x: execute
    - -rw-r--r-- 1: owner는 읽고 쓰기, group은 읽기, others는 읽기 권한이 있음
    - chmod : 권한을 변경해주는 역할 
    - chmod +x mapper.py: mapper.py에 있는 모든 사람에게 x 권한을 부여해줌
    - chmod -x mapper.py
    - chmod 755 mapper.py(7: rwx, 5: rx, 5: rx) =>  rwxr-xr-x 1 이렇게 바꿔줌
    - chmod 777 maper.py


# Word Count
- hadoop jar ~/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \: 
    - Hadoop Streaming은 텍스트 데이터를 처리할 수 있도록 해주는 인터페이스, 
    - Hadoop 설치 경로에 있는 Streaming jar 파일
-  -input /input/text.txt \: 입력 파일 경로(text.txt를 기준으로 분석 시작)
-  -output /output/wordcount \: 출력 파일 경로 
-  -mapper 'python3 /home/ubuntu/damf2/hadoop/0.wordcount/mapper.py' \: 각 라인을 받아서 원하는 단위로 쪼개는 역할
-  -reducer 'python3 /home/ubuntu/damf2/hadoop/0.wordcount/reducer.py': mapper가 출력한 걸 단어별로 합치는 역할
- ex) text.txt: the cat in the hat => mapper.py: the 1 cat 1 in 1 the 1 hat 1 => reducer.py: the 2 cat 1 in 1 hat 1


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