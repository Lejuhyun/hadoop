import sys
for line in sys.stdin:
    line = line.strip() # 좌우에 공백이 있으면 공백 제거
    
    fields = line.split(',') # 데이터를 쉼표를 기준으로 split해준다
    # ['1', '296', '5.0', '11133451414'] => movieid와 rating만 필요
    movie_id = fields[1]
    rating = fields[2]

    print(f'{movie_id}\t{rating}') # 출력 