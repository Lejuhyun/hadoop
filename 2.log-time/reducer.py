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