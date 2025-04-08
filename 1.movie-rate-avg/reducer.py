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
