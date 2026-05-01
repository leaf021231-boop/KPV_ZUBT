import random

def roll_100():
    """生成 1-100 的随机数"""
    return random.randint(1, 100)

def roll_dice(num, sides):
    """投掷 num 个 sides 面的骰子"""
    return sum(random.randint(1, sides) for _ in range(num))

def check(stat):
    """普通判定：1d100 <= 属性值"""
    return roll_100() <= stat

def growth_check(current_value):
    """成长检定 (COC规则)：1d100 > 当前值"""
    # 如果当前值已经 >= 100，则无法自然成长
    if current_value >= 100:
        return False
    return roll_100() > current_value

def penalty_check(stat):
    """惩罚骰判定 (模拟COC7版：投两次取较差/较高的结果)"""
    return max(roll_100(), roll_100()) <= stat

def bonus_check(stat):
    """奖励骰判定 (模拟COC7版：投两次取较好/较低的结果)"""
    return min(roll_100(), roll_100()) <= stat

class Character:
    def __init__(self, CRE, INT, has_compulsory_edu=True):
        self.CRE = CRE
        self.INT = INT
        self.has_compulsory_edu = has_compulsory_edu
        
        self.ASSET = 1
        self.EXPE = 1
        self.KNOW = 1
        
    def simulate_life(self):
        # 1岁到18岁循环
        for age in range(1, 19):
            
            # --- ASSET (4-18岁) ---
            if age >= 4:
                if check(self.CRE):  # CRE判定
                    if growth_check(self.ASSET):  # ASSET成长检定
                        self.ASSET += roll_dice(1, 8)
                        
            # --- EXPE (4-18岁) ---
            if age >= 4:
                if check(self.INT):  # INT判定
                    self.EXPE += roll_dice(1, 4)
                    if growth_check(self.EXPE):  # EXPE成长检定
                        self.EXPE += roll_dice(1, 4)
                        
            # --- KNOW (学龄前 2-8岁) ---
            if 2 <= age <= 8:
                passed_cre = False
                # 为避免重复计算，拆分年龄段：2-3岁, 4-5岁, 6-8岁
                if age in [2, 3]:
                    passed_cre = penalty_check(self.CRE)
                elif age in [4, 5]:
                    passed_cre = check(self.CRE)
                elif age in [6, 7, 8]:
                    passed_cre = bonus_check(self.CRE)
                    
                if passed_cre:
                    if growth_check(self.KNOW):
                        self.KNOW += roll_dice(1, 6)
                        if check(self.INT): # INT检定带动额外成长
                            self.KNOW += roll_dice(1, 6)
                            
            # --- KNOW (学龄期 9-18岁) ---
            if 9 <= age <= 18:
                if self.has_compulsory_edu:
                    # 有义务教育模式
                    # 必定进行 KNOW成长检定 (义务教育强制送的)
                    if growth_check(self.KNOW):
                        self.KNOW += roll_dice(2, 2) # 保底成长
                        
                        if check(self.INT): # 成功成长带动INT判定
                            self.KNOW += roll_dice(1, 6)
                            
                        if check(self.CRE): # 补习班额外检定
                            self.KNOW += roll_dice(1, 2)
                else:
                    # 无义务教育模式 (私人教育)
                    if check(self.CRE): # 先过家里有钱关
                        if growth_check(self.KNOW):
                            self.KNOW += roll_dice(1, 6)
                            if check(self.INT): # 成功成长带动INT判定
                                self.KNOW += roll_dice(1, 4)
                    elif penalty_check(self.INT):
                        if growth_check(self.KNOW):
                            self.KNOW += roll_dice(1, 4)


def run_simulation(CRE, INT, iterations=1000):
    print(f"==================================================")
    print(f"开始模拟: 角色设定 [CRE: {CRE}, INT: {INT}] - 运行 {iterations} 次")
    print(f"==================================================")
    
    # 记录总和以计算平均值
    stats_compulsory = {"ASSET": 0, "EXPE": 0, "KNOW": 0}
    stats_no_compulsory = {"ASSET": 0, "EXPE": 0, "KNOW": 0}
    
    for _ in range(iterations):
        # 测试：有义务教育
        char_comp = Character(CRE, INT, has_compulsory_edu=True)
        char_comp.simulate_life()
        stats_compulsory["ASSET"] += char_comp.ASSET
        stats_compulsory["EXPE"] += char_comp.EXPE
        stats_compulsory["KNOW"] += char_comp.KNOW
        
        # 测试：无义务教育 (ASSET 和 EXPE 不受影响，主要是为了对比 KNOW)
        char_no_comp = Character(CRE, INT, has_compulsory_edu=False)
        char_no_comp.simulate_life()
        stats_no_compulsory["KNOW"] += char_no_comp.KNOW

    # 输出平均结果
    print(f"【所有模式通用属性】(平均值)")
    print(f" > ASSET (资产): {stats_compulsory['ASSET'] / iterations:.1f}")
    print(f" > EXPE  (经验): {stats_compulsory['EXPE'] / iterations:.1f}")
    print(f"")
    print(f"【KNOW 知识属性对比】(平均值)")
    print(f" > KNOW (有义务教育): {stats_compulsory['KNOW'] / iterations:.1f}  <-- 现代背景推荐")
    print(f" > KNOW (无义务教育): {stats_no_compulsory['KNOW'] / iterations:.1f}  <-- 古代/中世纪背景")
    print(f"==================================================\n")


# === 测试用例输入区 ===

# 测试 1: 普通人 (家境普通，智力普通)
run_simulation(CRE=50, INT=50)

# 测试 2: 贫困天才 (家境极差，智力极高)
run_simulation(CRE=15, INT=85)

# 测试 3: 富二代学渣 (家境极好，智力偏低)
run_simulation(CRE=85, INT=30)

run_simulation(CRE=70, INT=40)

run_simulation(CRE=50, INT=85)

run_simulation(CRE=85, INT=85)  # 天胡开局
run_simulation(CRE=15, INT=15)  # 地狱开局