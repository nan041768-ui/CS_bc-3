import time
import json


def calculate_mac(pattern, filter_array):
    score = 0.0
    size = len(pattern)
    for i in range(size):  
        for j in range(size):  
            score += pattern[i][j] * filter_array[i][j]
    return score


def compare_scores(score_a, score_b, label_a, label_b):
    epsilon = 1e-9
    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"  
    elif score_a > score_b:
        return label_a
    else:
        return label_b


def normalize_label(label):
    lower_label = label.lower()
    if lower_label in ["+", "cross"]:
        return "Cross"  
    elif lower_label in ["x"]:
        return "X"  
    else:
        return label  


def get_matrix_input(prompt_name):
    while True:
        print(f"\n{prompt_name} (3줄 입력, 공백 구분)")
        matrix = []  
        error_flag = False  

        for i in range(3):
            line = input()  
            str_numbers = line.split()  

            if len(str_numbers) != 3:
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                error_flag = True  
                break  

            row = []  
            for text in str_numbers:
                try:
                    num = float(text)  
                    row.append(num)  
                except ValueError:
                    print("입력 형식 오류: 숫자가 아닌 값이 포함되어 있습니다.")
                    error_flag = True  
                    break  

            if error_flag == True:
                break

            matrix.append(row)

        if error_flag == False:
            return matrix  


def main():
    print("=== Mini NPU Simulator ===")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    choice = input("선택: ")

    if choice == "1":
        print("\n[안내] 1번: 사용자 입력 모드를 시작합니다.")

        filter_a = get_matrix_input("필터 A")
        filter_b = get_matrix_input("필터 B")
        pattern = get_matrix_input("패턴")

        score_a = calculate_mac(pattern, filter_a)
        score_b = calculate_mac(pattern, filter_b)

        start_time = time.perf_counter()  
        for _ in range(10):  
            calculate_mac(pattern, filter_a)
            calculate_mac(pattern, filter_b)
        end_time = time.perf_counter()  

        avg_time_ms = ((end_time - start_time) / 10) * 1000  

        print("\n#---------------------------------------")
        print("# [3] MAC 결과")
        print("#---------------------------------------")
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/10회): {avg_time_ms:.3f} ms")  

        result = compare_scores(score_a, score_b, "A", "B")
        if result == "UNDECIDED":
            print("판정: 판정 불가 (|A-B| < 1e-9)")
        else:
            print(f"판정: {result}")

    elif choice == "2":
        print("\n[안내] 2번: data.json 분석 모드를 시작합니다.")
        
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            filters_data = data.get("filters", {})
            patterns_data = data.get("patterns", {})
            
            print("✓ data.json 로드 완료")
            
            total_tests = 0   
            pass_count = 0    
            fail_count = 0    
            fail_cases = []   
            
            # --- [추가] 크기별로 측정된 시간을 차곡차곡 모아둘 빈 보관함(딕셔너리) ---
            performance_data = {}
            # ----------------------------------------------------------------------
            
            for pattern_key, pattern_info in patterns_data.items():
                print(f"\n--- {pattern_key} ---")
                
                total_tests += 1  
                
                pattern_input = pattern_info.get("input")
                expected_label = pattern_info.get("expected")
                
                parts = pattern_key.split('_')
                n_size = int(parts[1])  
                
                filter_key = f"size_{n_size}"
                if filter_key not in filters_data:
                    print(f"판정 불가 | expected: {expected_label} | FAIL (사유: {filter_key} 필터 없음)")
                    fail_count += 1
                    fail_cases.append(f"{pattern_key}: {filter_key} 필터 없음")
                    continue  
                    
                if len(pattern_input) != n_size or len(pattern_input[0]) != n_size:
                    print(f"판정 불가 | expected: {expected_label} | FAIL (사유: 그림 크기 불일치)")
                    fail_count += 1
                    fail_cases.append(f"{pattern_key}: 그림 크기 불일치")
                    continue  
                    
                target_filters = filters_data[filter_key]
                
                norm_expected = normalize_label(expected_label)
                
                cross_filter = target_filters.get("cross")
                x_filter = target_filters.get("x")
                
                if not cross_filter or not x_filter:
                    print(f"판정 불가 | expected: {norm_expected} | FAIL (사유: 필터 데이터 비어있음)")
                    fail_count += 1
                    fail_cases.append(f"{pattern_key}: 필터 데이터 비어있음")
                    continue
                    
                score_cross = calculate_mac(pattern_input, cross_filter)
                score_x = calculate_mac(pattern_input, x_filter)
                
                result = compare_scores(score_cross, score_x, "Cross", "X")
                
                if result == norm_expected:
                    final_status = "PASS"
                    pass_count += 1
                else:
                    final_status = "FAIL"
                    fail_count += 1
                    if result == "UNDECIDED":
                        fail_cases.append(f"{pattern_key}: 동점(UNDECIDED) 처리 규칙에 따라 FAIL")
                    else:
                        fail_cases.append(f"{pattern_key}: 예측 실패 (예상: {norm_expected}, 결과: {result})")
                    
                print(f"Cross 점수: {score_cross}")
                print(f"X 점수: {score_x}")
                print(f"판정: {result} | expected: {norm_expected} | {final_status}")
                
                # --- [추가] 모드 2 전용 연산 시간 측정 ---
                start_time = time.perf_counter()
                for _ in range(10):  # 10번 혹사시켜서 시간 재기
                    calculate_mac(pattern_input, cross_filter)
                    calculate_mac(pattern_input, x_filter)
                end_time = time.perf_counter()
                
                avg_time_ms = ((end_time - start_time) / 10) * 1000
                
                # 만약 보관함에 5x5 같은 크기(n_size) 서랍이 없다면 새로 만듭니다.
                if n_size not in performance_data:
                    performance_data[n_size] = []
                    
                # 해당 서랍에 방금 잰 평균 시간을 쏙 집어넣습니다.
                performance_data[n_size].append(avg_time_ms)
                # ----------------------------------------
                
            # --- [추가] 성능 분석 표 출력하기 ---
            print("\n#---------------------------------------")
            print("# [3] 성능 분석 (평균/10회)")
            print("#---------------------------------------")
            print("크기       평균 시간(ms)    연산 횟수")
            print("-------------------------------------")
            
            # 작은 크기(5x5)부터 큰 크기(13x13) 순서대로 정렬(sorted)해서 꺼냅니다.
            for size in sorted(performance_data.keys()):
                # 해당 서랍에 들어있는 시간들을 전부 합친 뒤, 개수로 나누어 '진짜 평균'을 구합니다.
                times_list = performance_data[size]
                overall_avg_ms = sum(times_list) / len(times_list)
                
                # 연산 횟수는 N 곱하기 N (N^2) 입니다.
                ops = size * size
                
                # :<7 은 7칸을 확보하고 왼쪽 정렬, :>8.3f는 8칸을 확보하고 소수점 3자리까지 출력하라는 예쁜 정렬 서식입니다.
                print(f"{size}x{size:<7} {overall_avg_ms:>8.3f}           {ops}")
            # ---------------------------------------------
                
            print("\n#---------------------------------------")
            print("# [4] 결과 요약")
            print("#---------------------------------------")
            print(f"총 테스트: {total_tests}개")
            print(f"통과: {pass_count}개")
            print(f"실패: {fail_count}개")
            
            if fail_count > 0:
                print("\n실패 케이스:")
                for case in fail_cases:
                    print(f"- {case}")
            
        except FileNotFoundError:
            print("\n[오류] data.json 파일을 찾을 수 없습니다. 파일 위치를 확인해주세요.")

    else:
        print("\n[오류] 잘못된 입력입니다. 1 또는 2를 입력해주세요.")


if __name__ == "__main__":
   main()