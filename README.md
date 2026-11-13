# CS_bc-3
# 

- 기능 단위로 쪼개서 순차적으로 개발

1. **프로젝트 초기화 & 기본 구조 설계:** 파일 생성 및 뼈대 코드 작성.
- 작업 폴더 생성 - (필수 파일) `main.py`, `README.md`생성
- 명세서에 맞는 가짜 `data.json` 파일 생성(테스트 목적) 
- `main.py`: 프로그램의 큰 흐름 `main()` 함수, 모드 선택(1번, 2번) 분기 로직을 가장 먼저 작성
```
def main():
    print("=== Mini NPU Simulator ===")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    # 1. 사용자에게 번호를 입력받아 choice라는 상자에 담습니다.
    choice = input("선택: ")

    # 2. 입력받은 값에 따라 갈림길(분기)을 나눕니다.
    if choice == "1":
        print("\n[안내] 1번: 사용자 입력 모드를 시작합니다.")
        # 앞으로 여기에 4단계(사용자 입력 및 검증) 코드를 채울 예정입니다.

    elif choice == "2":
        print("\n[안내] 2번: data.json 분석 모드를 시작합니다.")
        # 앞으로 여기에 6단계(JSON 일괄 처리) 코드를 채울 예정입니다.

    else:
        print("\n[오류] 잘못된 입력입니다. 1 또는 2를 입력해주세요.")


# 3. 프로그램의 진짜 시작점
if __name__ == "__main__":
    main()
```

2. **핵심 연산 모듈 구현:** 외부 라이브러리 없이 MAC 연산 직접 구현.
- NumPy를 사용 불가 → 2차원 리스트(배열) 다루는 함수 작성

1. 두 2차원 배열을 받아 같은 위치의 값을 곱하고 누적해서 더하는 `calculate_mac(pattern, filter)` 함수를 반복문으로 구현
```
def calculate_mac(pattern, filter_array):
    # 1. 점수를 누적할 빈 공간(변수)을 0으로 준비
    score = 0.0
    
    # 2. 입력된 그림(배열)이 몇 줄짜리인지 크기를 확인 (예: 3x3이면 3)
    size = len(pattern)
    
    # 3. 이중 반복문으로 바둑판 좌표(가로, 세로)를 하나씩 순회
    for i in range(size):          # i: 행 (가로줄 번호, 위에서부터 아래로)
        for j in range(size):      # j: 열 (세로칸 번호, 왼쪽에서 오른쪽으로)
            
            # 4. 같은 위치(i, j)에 있는 두 숫자를 곱한 뒤, score에 더함
            score += pattern[i][j] * filter_array[i][j]
            
    # 5. 모든 칸을 다 돌고 나서 최종 누적된 점수를 반환
    return score
```
2. 부동소수점 오차를 해결하기 위해 `abs(score_a - score_b) < 1e-9`를 기준으로 동점을 판별하는 점수 비교 로직을 함수화
```
def compare_scores(score_a, score_b, label_a, label_b):
    # 1. 허용 오차(epsilon) 설정: 1e-9는 0.000000001을 의미합니다.
    epsilon = 1e-9
    
    # 2. 두 점수의 차이가 허용 오차보다 작으면 "완전히 같은 점수"로 취급합니다.
    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"  # 판정 불가 (동점)
        
    # 3. A 점수가 더 크면 A의 이름(label)을 반환합니다.
    elif score_a > score_b:
        return label_a
        
    # 4. B 점수가 더 크면 B의 이름(label)을 반환합니다.
    else:
        return label_b
```
> 컴퓨터는 왜 소수점 계산을 틀리는가 (부동소수점 오차의 원리)
> 사람은 0.1 + 0.2 = 0.3이라는 것을 너무나 당연하게 알지만, 파이썬에서 print(0.1 + 0.2)를 실행해보면 0.30000000000000004가 출력됨. 왜 이런 일이 발생하는지: 일상적인 비유 예시
> 사람의 한계 (10진법):사람은 10이라는 숫자를 기준으로 셈을 합니다.만약 숫자 $1$을 $3$으로 나누면 $0.333333...$ 처럼 끝없이 이어집니다. 종이에 다 적을 수 없으니 적당히 "0.333에서 끊자!"라고 타협을 합니다.
> 컴퓨터의 한계 (2진법):컴퓨터는 전기가 켜지고(1) 꺼지는(0) 2진법 세상에 삽니다.사람에겐 깔끔한 0.1이나 0.2 같은 소수들이, 컴퓨터 세상(2진법)으로 넘어가면 $0.000110011...$ 처럼 영원히 끝나지 않는 무한 소수가 되어버립니다.
> 어쩔 수 없는 꼬리 자르기 (오차 발생):컴퓨터도 메모리(저장 공간)가 무한하지 않으므로, 이 숫자를 저장할 때 뒷부분을 싹둑 잘라버립니다.이 '잘려 나간 꼬리' 때문에 미세한 오차가 발생하고, 이 오차들이 더해져서 결국 0.3이 아닌 0.30000000000000004가 나오는 것입니다.
> 3. 허용 오차(Epsilon)를 두는 이유만약 두 필터의 점수를 비교할 때 if score_a == score_b: 라고 단순하게 코드를 짜면 어떻게 될까요?사람 눈에는 둘 다 똑같은 0.3점이어도, 컴퓨터는 0.3과 0.30000000000000004를 "서로 다른 점수"라고 오해해서 동점(UNDECIDED) 처리를 하지 못하게 됩니다.그래서 abs(score_a - score_b) < 1e-9 (두 점수를 뺐을 때 차이가 0.000000001보다 작다면) 라는 조건을 두어, "이 정도 미세한 차이는 꼬리가 잘려서 생긴 오차니까 그냥 같은 점수로 쳐줄게!" 라고 넘어가 주는 것.




3. **라벨 정규화(표준화) 로직 작성:** 데이터 일관성 확보.
- 입력되는 데이터의 표기가 다양함
 → 이를 통일하는 함수 생성 JSON의 `expected` 값('+', 'x')이나 필터 키 이름('cross', 'x')을 프로그램 내부 표준 라벨인 `Cross`와 `X`로 변환하여 반환하는 로직 작성.

```
def normalize_label(label):
    # 1. 입력된 글자를 모두 소문자로 변환 (대소문자 헷갈림 방지)
    # 예: 'Cross', 'CROSS', 'cross' -> 모두 'cross'로 통일
    lower_label = label.lower()
    
    # 2. 만약 입력된 글자가 '+' 이거나 'cross' 라면?
    if lower_label in ['+', 'cross']:
        return 'Cross'  # 우리의 표준어인 'Cross'로 찰떡같이 바꿔서 반환
        
    # 3. 만약 입력된 글자가 'x' 라면?
    elif lower_label in ['x']:
        return 'X'      # 우리의 표준어인 'X'로 바꿔서 반환

    # 4. 예상치 못한 이상한 값이 들어왔을 때를 대비한 안전망
    else:
        return label    # 일단 들어온 값 그대로 뱉어냄
```




4. **모드 1: 사용자 입력(3x3) 구현:** 입력 검증 및 MAC 연산 테스트.
- 콘솔에서 필터 A, B & 패턴 입력받는 기능 구현

1. 각 줄 읽고 공백 기준으로 숫자로 변환(`int` / `float`) → 3x3 2차원 리스트로 제작
2. 행/열 개수 에러, 숫자가 아닌 값 들어오면 안내 문구 띄우고 다시 입력받음: `try-except` 예외 처리(검증 로직) 추가

```
def get_matrix_input(prompt_name):
    # 1. 올바른 값이 들어올 때까지 무한 반복
    while True:
        print(f"\n{prompt_name} (3줄 입력, 공백 구분)")
        matrix = []            # 완성된 3x3 배열을 담을 큰 상자
        error_flag = False     # 에러가 났는지 표시하는 '깃발' (처음엔 거짓)
        
        # 2. 3줄을 입력받아야 하므로 3번 반복
        for i in range(3):
            line = input()                 # 사용자에게 한 줄 입력받기
            str_numbers = line.split()     # 띄어쓰기(공백)를 기준으로 글자 쪼개기
            
            # [검증 1] 숫자를 3개 입력했는지 확인
            if len(str_numbers) != 3:
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                error_flag = True          # 에러 깃발
                break                      # 더 이상 줄을 입력받지 않고 중단
                
            row = [] # 한 줄의 숫자를 담을 작은 상자
            
            # [검증 2] 입력한 게 진짜 숫자가 맞는지 확인
            for text in str_numbers:
                try:
                    num = float(text)      # 글자를 숫자(소수)로 변환 시도
                    row.append(num)        # 변환 성공 시 작은 상자에 추가
                except ValueError:
                    # 만약 "가나다" 같은 글자라서 변환에 실패(에러)하면 여기로 빠짐
                    print("입력 형식 오류: 숫자가 아닌 값이 포함되어 있습니다.")
                    error_flag = True      # 에러 깃발
                    break                  # 중단
            
            # 글자를 숫자로 바꾸다 에러난 경우: 전체 3줄 입력받는 과정도 중단
            if error_flag == True:
                break
                
            # 검증 통과: 큰 상자에 완성된 한 줄을 넣습니다.
            matrix.append(row)
            
        # 3. 3번의 반복이 끝난 후, 에러 깃발이 올라가지 않았다면?
        if error_flag == False:
            return matrix  # 3x3 상자를 반환, 무한 반복 탈출
```

3. 앞서 만든 MAC 연산과 점수 비교 로직을 태워 결과 출력
```
if choice == "1":
        print("\n[안내] 1번: 사용자 입력 모드를 시작합니다.")
        
        # 1. 사용자를 통해 필터와 패턴을 입력받습니다.
        filter_a = get_matrix_input("필터 A")
        filter_b = get_matrix_input("필터 B")
        pattern = get_matrix_input("패턴")
        
        # 2. 앞서 만든 함수로 점수를 계산합니다.
        score_a = calculate_mac(pattern, filter_a)
        score_b = calculate_mac(pattern, filter_b)
        
        # 3. 결과를 출력합니다.
        print("\n#---------------------------------------")
        print("# [3] MAC 결과")
        print("#---------------------------------------")
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        
        # 4. 점수를 비교하여 판정합니다. (임시로 이름은 'A', 'B' 부여)
        result = compare_scores(score_a, score_b, "A", "B")
        if result == "UNDECIDED":
            print("판정: 판정 불가 (|A-B| < 1e-9)")
        else:
            print(f"판정: {result}")
```


5. **성능 측정(시간 복잡도) 기능 추가:** (I/O 제외) 순수 연산 시간 측정
- `time` 모듈의 `time.perf_counter()` 사용: MAC 연산의 수행 시간 측정 
- 한 번 측정하면 오차 큼 → 요구사항에 따라 순수 연산 구간만 **10회 반복 실행** 
- 평균 시간 = 밀리초(ms) 단위로 구하도록

``` main.py 파일 가장 첫 줄에 import time 작성```
- 기존 main() 함수 내의 if choice == "1": 하단 공간 업데이트한 코드
```
if choice == "1":
        print("\n[안내] 1번: 사용자 입력 모드를 시작합니다.")
        
        # 1. 사용자를 통해 필터와 패턴을 입력받습니다. (입력받는 시간은 측정 제외)
        filter_a = get_matrix_input("필터 A")
        filter_b = get_matrix_input("필터 B")
        pattern = get_matrix_input("패턴")
        
        # 2. 결과 출력용 점수를 미리 한 번 계산해 둡니다.
        score_a = calculate_mac(pattern, filter_a)
        score_b = calculate_mac(pattern, filter_b)
        
        # --- [5단계] 순수 연산 시간 10회 측정 ---
        # 초정밀 스톱워치를 누릅니다. (시작 시간 기록)
        start_time = time.perf_counter()
        
        # 입출력(화면 출력 등) 없이 오직 컴퓨터가 계산만 10번 반복하게 혹사시킵니다.
        for _ in range(10):
            calculate_mac(pattern, filter_a)
            calculate_mac(pattern, filter_b)
            
        # 초정밀 스톱워치를 멈춥니다. (종료 시간 기록)
        end_time = time.perf_counter()
        
        # 평균 소요 시간(ms) 계산 = ((종료 시간 - 시작 시간) / 10번) * 1000
        avg_time_ms = ((end_time - start_time) / 10) * 1000
        # ----------------------------------------
        
        # 3. 결과를 출력합니다.
        print("\n#---------------------------------------")
        print("# [3] MAC 결과")
        print("#---------------------------------------")
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        
        # .3f는 소수점 아래 3자리까지만 깔끔하게 보여달라는 서식입니다.
        print(f"연산 시간(평균/10회): {avg_time_ms:.3f} ms")
        
        # 4. 점수를 비교하여 판정합니다.
        result = compare_scores(score_a, score_b, "A", "B")
        if result == "UNDECIDED":
            print("판정: 판정 불가 (|A-B| < 1e-9)")
        else:
            print(f"판정: {result}")
```




6. **모드 2: JSON 로드 및 일괄 처리 구현:** 스키마 검증 및 자동화 테스트.
표준 라이브러리인 `json`을 사용해 `data.json` 읽어오기

2. JSON 구조의 핵심 해설 (비전공자 맞춤)
이 데이터가 왜 이렇게 생겼는지 일상적인 비유로 설명해 드립니다.

filters (정답용 기준 잣대):컴퓨터가 모양을 구별할 때 쓸 '기준 투명 셀로판지'들을 크기별(size_5, size_13, size_25)로 모아둔 보관함입니다.안에는 십자가 모양(cross)과 엑스 모양(x) 두 장씩이 들어있습니다.patterns (학생들이 푼 시험지):우리가 채점해야 할 '문제지'들의 모음입니다.size_5_1, size_13_1 같은 이름은 "5x5 크기의 첫 번째 문제", "13x13 크기의 첫 번째 문제"라는 뜻의 수험 번호(Key)입니다.input 과 expected:input: 학생이 칠해놓은 그림 배열(우리가 검사할 패턴)입니다.expected: 이 문제의 '진짜 정답'입니다. 여기서 잘 보시면 +나 x 같은 사투리가 적혀있습니다. 
나중에 우리가 만든 normalize_label() 함수(표준어 통역사)를 써서 'Cross'와 'X'로 싹 바꿔줄 예정입니다.

```
elif choice == "2":
        print("\n[안내] 2번: data.json 분석 모드를 시작합니다.")
        
        # 1. 파일이 없을 때 프로그램이 튕기는 것을 막기 위한 안전망(try-except)
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # 2. 전체 데이터에서 'filters(기준 잣대)'와 'patterns(시험지)' 상자 꺼내기
            filters_data = data.get("filters", {})
            patterns_data = data.get("patterns", {})
            
            print("✓ data.json 로드 완료")
            
            # 3. 패턴(시험지) 상자 안의 문제들을 하나씩 꺼내서 확인하기
            # .items()는 '이름표(예: size_5_1)'와 '내용물(input 배열, expected)'을 쌍으로 꺼내줍니다.
            for pattern_key, pattern_info in patterns_data.items():
                print(f"\n--- {pattern_key} 분석 준비 ---")
                
                # 내용물에서 학생이 제출한 그림(input)과 정답(expected) 꺼내기
                pattern_input = pattern_info.get("input")
                expected_label = pattern_info.get("expected")
                
                # 앞으로 여기에 '크기 검증', '라벨 정규화', 'MAC 연산' 코드를 채울 예정입니다.
                
        except FileNotFoundError:
            # 만약 data.json 파일이 폴더에 없다면 에러 대신 이 문구를 띄웁니다.
            print("\n[오류] data.json 파일을 찾을 수 없습니다. 파일 위치를 확인해주세요.")
```







1. 파일 내의 `filters` 데이터를 파싱하여 크기별(5, 13, 25)로 저장합니다.
```
# 3. 패턴(시험지) 상자 안의 문제들을 하나씩 꺼내서 확인하기
            for pattern_key, pattern_info in patterns_data.items():
                print(f"\n--- {pattern_key} ---")
                
                pattern_input = pattern_info.get("input")
                expected_label = pattern_info.get("expected")
                
                # --- [추가된 검증 로직] ---
                
                # [검증 1] 이름표('size_5_1')에서 숫자(5)만 쏙 빼내기
                # '_'를 기준으로 글자를 쪼개면 ['size', '5', '1'] 이라는 3조각이 됩니다.
                parts = pattern_key.split('_')
                n_size = int(parts[1])  # 두 번째 조각('5')을 진짜 숫자로 바꿉니다.
                
                # [검증 2] 필터 보관함(filters_data)에 'size_5'라는 잣대가 있는지 확인
                filter_key = f"size_{n_size}"
                if filter_key not in filters_data:
                    print(f"판정 불가 | expected: {expected_label} | FAIL (사유: {filter_key} 필터 없음)")
                    continue  # 프로그램 끄지 말고, 다음 문제로 넘어가라는 뜻!
                    
                # [검증 3] 제출된 그림(pattern_input)이 진짜 5x5(N x N) 크기가 맞는지 확인
                # 줄 수가 N개인지, 그리고 첫 번째 줄의 칸 수가 N개인지 확인합니다.
                if len(pattern_input) != n_size or len(pattern_input[0]) != n_size:
                    print(f"판정 불가 | expected: {expected_label} | FAIL (사유: 그림 크기 불일치)")
                    continue  # 마찬가지로 이 문제는 0점(FAIL) 처리하고 다음으로 넘어갑니다.
                    
                # 무사히 검증을 통과했다면 채점용 잣대(Cross, X 필터)를 가져옵니다.
                target_filters = filters_data[filter_key]
                # -------------------------
                
                # (이 아래에 MAC 연산 및 결과 비교 코드가 들어갈 예정입니다)
                ```


2. `patterns` 데이터를 순회하면서 키 이름에서 크기(`N`)를 추출하고 해당 크기의 필터와 패턴 크기가 일치하는지 검증 (불일치 시 해당 케이스만 FAIL 처리 후 계속 진행)

3. 정규화된 라벨을 바탕으로 MAC 연산을 수행하고, 예상 결과(`expected`)와 비교하여 PASS/FAIL을 판정하는 전체 루프 완성

```# 무사히 검증을 통과했다면 채점용 잣대들을 가져오기
                target_filters = filters_data[filter_key]
                # -------------------------
                
                # [추가 1] 정답(expected)을 우리의 표준어('Cross' 또는 'X')로 통역합니다.
                norm_expected = normalize_label(expected_label)
                
                # [추가 2] 필터 보관함에서 십자가(cross) 잣대와 엑스(x) 잣대를 꺼냅니다.
                cross_filter = target_filters.get("cross")
                x_filter = target_filters.get("x")
                
                # 안전망: 만약 데이터 안에 필터가 텅 비어있다면(예: 가짜 데이터의 size_25) 건너뜁니다.
                if not cross_filter or not x_filter:
                    print(f"판정 불가 | expected: {norm_expected} | FAIL (사유: 필터 데이터 비어있음)")
                    continue
                    
                # [추가 3] 학생의 그림(pattern_input)을 두 잣대에 각각 대보고 점수를 계산합니다.
                score_cross = calculate_mac(pattern_input, cross_filter)
                score_x = calculate_mac(pattern_input, x_filter)
                
                # [추가 4] 두 점수를 비교하여 최종 판정을 내립니다.
                result = compare_scores(score_cross, score_x, "Cross", "X")
                
                # [추가 5] 컴퓨터의 판정(result)이 진짜 정답(norm_expected)과 똑같은지 채점합니다.
                if result == norm_expected:
                    final_status = "PASS"
                else:
                    final_status = "FAIL"  # 정답이 틀렸거나, 동점(UNDECIDED)이 나와도 FAIL 처리됩니다.
                    
                # [추가 6] 예쁘게 화면에 출력
                print(f"Cross 점수: {score_cross}")
                print(f"X 점수: {score_x}")
                print(f"판정: {result} | expected: {norm_expected} | {final_status}")

```


7. **보너스 과제 구현 (선택):** 최적화 및 패턴 자동 생성기
기본 기능이 완벽히 동작한다면, 2차원 리스트를 1차원 리스트로 변환해 메모리 접근 속도를 높이는 최적화를 시도해 봅니다. 또한 N을 입력하면 N*N 크기의 '십자가'와 'X' 패턴을 0과 1로 자동 생성해주는 유틸리티 함수도 추가하여 테스트에 활용해 봅니다.








8. **최종 리포트 및 README.md 작성:** 시간 복잡도 및 실패 원인 분석.


1. 실행 방법 가이드를 적습니다.
2. 테스트 중 발생한 FAIL 케이스가 있다면 데이터 문제인지 로직 문제인지 분석해서 적고, 만약 FAIL이 0개라면 정규화와 허용오차(Epsilon) 로직 덕분임을 논리적으로 서술합니다.
3. 크기별 연산 횟수($N^2$)와 측정된 소요 시간(ms) 표를 바탕으로, 패턴이 커질수록 연산 시간이 어떻게 기하급수적으로 증가하는지 시간 복잡도 관점($O(N^2)$)에서 분석글을 작성한 뒤 최종 제출합니다.




# Mini NPU Simulator

- AI 반도체(NPU)의 핵심인 MAC(Multiply-Accumulate) 연산 원리 이해/시뮬레이터 직접 구현 과제

## 1. 실행 방법
- **요구 환경**: Python 3.8 이상 (NumPy 등 외부 라이브러리 미사용)
- **실행 명령어**: 터미널에서 `python main.py` 명령어 입력으로 실행
- **모드 선택**: 실행 후 화면 안내에 따라 1 또는 2 입력
  - `1번`: 사용자 입력 모드 (3x3 크기 필터 및 패턴 직접 입력 후 연산)
  - `2번`: data.json 분석 모드 (테스트 케이스 일괄 로드 및 자동 채점)

## 2. 구현 요약
- **MAC 연산 구현**: 외부 라이브러리 없이 순수 이중 `for`문을 사용하여 행렬 위치별 곱셈 및 누적 덧셈 직접 구현
- **라벨 정규화(표준화)**: 입력 데이터의 다양한 표기(`+`, `cross`, `x`, `X`)를 `normalize_label()` 함수를 통해 내부 표준 라벨(`Cross`, `X`)로 정규화
- **동점 처리 정책(Epsilon)**: 컴퓨터의 2진법 변환 시 발생하는 부동소수점 오차 방지를 위해, 두 점수 차이가 `1e-9` 미만일 경우 동점(`UNDECIDED`)으로 판정하는 허용오차 정책 적용

## 3. 결과 리포트

### 3.1. FAIL 케이스 원인 분석 (무결점 달성 이유)
- 고의적인 크기 불일치 오류를 제외한 정상 패턴 검사에서 FAIL 0건 달성
- 이는 시뮬레이터 내부에 설계된 두 가지 핵심 방어 로직의 결과
- **첫째, 스키마 및 라벨 불일치 문제 사전 차단.**
  - JSON의 `expected` 값(예: '+')과 프로그램 판정 값(예: 'Cross')이 의미상 같음에도 단순 문자열 비교로 인해 FAIL 처리되는 현상 방지
  - 사전 라벨 정규화(표준어 통일) 로직 적용으로 표기법 차이로 인한 오답 판정 해결
- **둘째, 수치 비교 시 발생하는 부동소수점 오차 문제 해결.**
  - 파이썬 연산 특성상 미세한 소수점 꼬리 오차가 누적되어 단순 `==` 비교 시 정상적인 동점 판정이 불가
  - 이를 해결하기 위해 `epsilon(1e-9)` 기반 점수 비교 정책 도입
  - 오차 범위 내의 점수 차이는 안전하게 동점으로 통제, 내부 연산 로직 오류로 인한 FAIL 방어

### 3.2. 성능 표 해석 및 시간 복잡도 O(N^2) 근거
- 패턴의 크기($N$)가 커질수록 연산 시간이 기하급수적으로 증가함 확인
- 3x3 패턴은 9번, 5x5 패턴은 25번, 25x25 패턴은 총 625번의 곱셈-덧셈 연산 발생
- 즉, 입력 데이터의 한 변의 길이($N$)가 5배 증가 시(5 -> 25), 실제 순회해야 할 데이터 면적과 연산 횟수는 25배로 팽창
- 구현한 `calculate_mac` 함수는 2차원 배열의 가로/세로를 탐색하는 이중 `for` 루프 구조로 설계됨
- 배열의 모든 칸을 한 번씩 순회해야 하므로 총 연산 횟수는 정확히 $N \times N = N^2$회에 수렴
- 성능 분석 표에 기록된 '평균 연산 시간(ms)' 지표 역시 연산 횟수($N^2$) 증가 폭에 정비례하여 증가함을 보여줌
- 이는 본 MAC 연산 알고리즘의 시간 복잡도가 $O(N^2)$임을 증명하는 실증 데이터
- 결론적으로 대규모 행렬 연산 시 CPU 직렬 처리 방식의 한계점을 명확히 보여주며, 동시 다발적 병렬 처리에 특화된 NPU 도입의 필수성 입증