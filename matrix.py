import numpy as np

def generate_and_verify_magic_square():
    print("=== 153生日密碼 5x5 生日幻方 (附詳細驗證) ===")

    try:
        # 1. 使用者輸入
        date_input = input("請輸入生日 (YYYY/MM/DD): ")  # 例如 1975/11/03
##        target_sum = int(input("請輸入目標總和: "))      # 例如 153
        target_sum = 153

        # 2. 解析日期
        year_parts, mm, dd = date_input.split('/')
        cc = int(year_parts[:2])
        yy = int(year_parts[2:])
        mm, dd = int(mm), int(dd)

        # 3. 構造第一行並計算補數 S
        s = target_sum - (dd + mm + cc + yy)
        base_row = [dd, mm, cc, yy, s]

        # 4. 生成幻方 (使用對角線平衡位移序列: 0, 2, 4, 1, 3)
        shifts = [0, 2, 4, 1, 3]
        ms = np.zeros((5, 5), dtype=int)
        for i, shift in enumerate(shifts):
            for j in range(5):
                ms[i, j] = base_row[(j + shift) % 5]

        # 5. 呈現幻方矩陣
        print("\n【 生成的幻方矩陣 】")
        print("-" * 25)
        for row in ms:
            print("  ".join(f"{num:3d}" for num in row))
        print("-" * 25)

        # 6. 詳細呈現驗證過程
        print("\n【 數學驗證過程 】")

        # 驗證行 (Rows)
        print("\n--- 橫列加總 ---")
        for i, row in enumerate(ms):
            process = " + ".join(f"{n:2d}" for n in row)
            print(f"Row {i+1}: {process} = {sum(row)}")

        # 驗證列 (Columns)
        print("\n--- 直欄加總 ---")
        for j in range(5):
            col = ms[:, j]
            process = " + ".join(f"{n:2d}" for n in col)
            print(f"Col {j+1}: {process} = {sum(col)}")

        # 驗證對角線 (Diagonals)
        print("\n--- 對角線加總 ---")
        d1 = np.diag(ms)
        d2 = np.diag(np.fliplr(ms))

        process1 = " + ".join(f"{n:2d}" for n in d1)
        print(f"主對角線 (左上到右下): {process1} = {sum(d1)}")

        process2 = " + ".join(f"{n:2d}" for n in d2)
        print(f"副對角線 (右上到左下): {process2} = {sum(d2)}")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}，請檢查輸入格式。")

if __name__ == "__main__":
    generate_and_verify_magic_square()
