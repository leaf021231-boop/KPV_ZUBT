# data.py —— 普通模式的数据与工具函数
import random
import re
import json
import os

# ============================================================
# 模式常量（main.py 也会 import 这些）
# ============================================================
MODE_NORMAL        = "normal"
MODE_TEST          = "test"
MODE_IRONMAN       = "ironman"
MODE_FAST          = "fast"            # 40 岁结束
MODE_HORNY_MILD    = "horny_mild"      # 我有爱压抑😡，0岁开始
MODE_HORNY_INTENSE = "horny_intense"   # 我真的有爱压抑😢，18岁开始

HORNY_MODES = (MODE_HORNY_MILD, MODE_HORNY_INTENSE)

# ============================================================
# 八大属性（普通模式）
# ============================================================
ATTRIBUTES = ["STR", "CON", "POW", "DEX", "APP", "SIZ", "INT", "CRE"]

ATTR_DESC = {
    "STR": "力量", "CON": "体质", "POW": "意志",
    "DEX": "敏捷", "APP": "外貌", "SIZ": "体型",
    "INT": "智力", "CRE": "家境",
}

ATTR_LONG_DESC = {
    "STR": "肌肉强度，影响体力劳动、战斗力。",
    "CON": "身体素质，影响耐病、耐疲劳。",
    "POW": "意志力，影响精神抗性、专注力。",
    "DEX": "敏捷度，影响反应、灵巧度。",
    "APP": "外貌，影响第一印象、社交。",
    "SIZ": "体型，影响存在感、力量与生命。",
    "INT": "智力，影响学习与思辨。",
    "CRE": "家境，与角色自身财富无关，AI 据此判定起点。",
}

# 初始可分配点数池
POINTS_POOL_DEFAULT = 180
POINTS_POOL_INTENSE = 200   # 我真的有爱压抑😢

# ============================================================
# 场景：scenario_tag 用来过滤天赋
# ============================================================
SCENES = [
    {"id": "modern",  "name": "现代都市", "scenario_tag": "citywalk",
     "has_edu": True,
     "desc": "21世纪的繁华都市，钢筋水泥的丛林中藏着无数故事。"},
    {"id": "xianxia", "name": "九洲仙域", "scenario_tag": "flyaway",
     "has_edu": False,
     "desc": "飞剑御空，仙凡有别。修仙者的世界。"},
    {"id": "fantasy", "name": "剑与魔法", "scenario_tag": "dragonfire",
     "has_edu": False,
     "desc": "巨龙、法师、骑士、国王与冒险者。"},
    {"id": "warrior", "name": "唐宋江湖", "scenario_tag": "loneblade",
     "has_edu": False,
     "desc": "醉饮浩荡英雄气，餐尽九洲快哉风。"},
    {"id": "custom",  "name": "自定义世界", "scenario_tag": "citywalk",
     "has_edu": False,    # 默认无义务教育，由 UI toggle 决定
     "desc": "由你描述的世界设定，AI将为你量身打造。"},
]

GENDERS = ["男", "女", "武装直升机", "购物袋", "奶龙", "钝角", "自定义"]

# ============================================================
# 稀有度
# ============================================================
RARITY_CONFIG = {
    "negative":  {"label": "负面", "color": "#E74C3C", "bg": "#FDECEA"},
    "common":    {"label": "普通", "color": "#2C3E50", "bg": "#F4F6F7"},
    "rare":      {"label": "稀有", "color": "#2980B9", "bg": "#EAF3FB"},
    "legendary": {"label": "传奇", "color": "#A19336", "bg": "#F5ECF8"},
    "wildcard": {"label": "特殊", "color": "#FF4592", "bg": "#F5ECF8"},
}
RARITY_WEIGHTS = {"negative": 20, "common": 35, "rare": 25, "legendary": 12, "wildcard": 8}

# ============================================================
# 天赋池：每条都加 mode + scenarios
#   mode:      "Normal" / "Horni"  （普通/性压抑）
#   scenarios: ["citywalk", "dragonfire", "flyaway"] 任意组合
#              或写 ["any"] 表示所有场景都能抽到
#
# 下面只放几条示例，你把原来 80 条照样加 mode/scenarios 字段即可：
#     默认大多数原来的天赋： mode="Normal", scenarios=["citywalk"]
# ============================================================
TALENT_POOL = [

    # ---------- ANY ----------
    #============= NEGATIVE (10) =============
  {"name": "胎带弱症", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "先天不足，器官功能偏弱。", "modifiers": [("CON", "-1d2*5")], "narrative": "从第一声啼哭起，就比别的婴儿费心费力。"},
  {"name": "其貌不扬", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "面容组合颇为遗憾。", "modifiers": [("APP", "-1d2*5")], "narrative": "在人群中你习惯低头，很少被人第一眼看见。"},
  {"name": "体弱多病", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "童年常驻医院，身体素质偏弱。", "modifiers": [("CON", "-1d2*5")], "narrative": "消毒水的气味是你的童年基调。"},
  {"name": "愚钝根骨", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "接受新事物总是慢半拍。", "modifiers": [("INT", "-1d2*5")], "narrative": "同样的东西，你要比别人多花一倍时间理解。"},
  {"name": "意志薄脆", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "容易放弃，被困难击倒。", "modifiers": [("POW", "-1d2*5")], "narrative": "一遇挫折，心底就先说“算了吧”。"},
  {"name": "手脚笨拙", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "协调性天生差一截。", "modifiers": [("DEX", "-1d2*5")], "narrative": "系鞋带、接球，这些小事总让你手忙脚乱。"},
  {"name": "矮小瘦削", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "骨架纤小，怎么吃都不长肉。", "modifiers": [("SIZ", "-1d2*5")], "narrative": "人群里你总被挡住视线，外套永远买最小码。"},
  {"name": "气若游丝", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "先天肺活量不足，体力极差。", "modifiers": [("STR", "-1d2*5")], "narrative": "跑两步就喘，重物与你无缘。"},
  {"name": "家徒四壁", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "出生在最贫瘠的屋檐下。", "modifiers": [("CRE", "-1d2*5")], "narrative": "你的摇篮是补丁摞补丁的旧衣裳。"},
  {"name": "不样之兆", "rarity": "negative", "mode": "Normal", "scenarios": ["any"], "desc": "降生时伴随异象，被视为不吉。", "modifiers": [("APP", "-1d1*5"), ("POW", "-1d1*5")], "narrative": "族中老人见你便摇头，目光总带着疏离。"},

  #============= COMMON (15) =============
  {"name": "寻常人家", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "既不富裕也不拮据，温饱有余。", "modifiers": [], "narrative": "你的童年没有太多意外，平平淡淡长大。"},
  {"name": "五官端正", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "相貌说不上惊艳，但干净耐看。", "modifiers": [], "narrative": "镜子里的脸，不会让任何人皱眉。"},
  {"name": "平和心境", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "天生的情绪稳定器。", "modifiers": [("POW", "+1d1*5"), ("INT", "-1d1*5")], "narrative": "火烧眉毛也不急，这份淡定与生俱来，只是偶尔显得反应慢。"},
  {"name": "脚力过人", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "腿部肌肉天生发达，但上身力量平平。", "modifiers": [("DEX", "+1d1*5"), ("STR", "-1d1*5")], "narrative": "从小就能跑擅跳，但掰手腕从没赢过。"},
  {"name": "鹰隼目力", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "视力绝佳，但听觉稍钝。", "modifiers": [("INT", "+1d1*5"), ("POW", "-1d1*5")], "narrative": "远处的细节你一眼看清，却常听漏耳边的低语。"},
  {"name": "大骨架", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "天生块头大，行动略笨重。", "modifiers": [("SIZ", "+1d2*5"), ("DEX", "-1d2*5")], "narrative": "站在那就占地方，穿门时总要侧身。"},
  {"name": "皮实耐造", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "免疫力不错，但小伤小痛不断。", "modifiers": [("CON", "+1d2*5"), ("SIZ", "-1d1*5")], "narrative": "淋雨不感冒，但膝盖总是旧的痂没掉又添新的。"},
  {"name": "早慧早衰", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "幼时聪明过人，体质却提前消耗。", "modifiers": [("INT", "+1d2*5"), ("CON", "-1d2*5")], "narrative": "三岁识字、五岁吟诗，可药罐子几乎没离过手。"},
  {"name": "流浪者之子", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "家族行踪不定，见多识广但根基浅薄。", "modifiers": [("CRE", "+1d1*5"), ("POW", "-1d1*5")], "narrative": "你在马背上学会说话，却不知何处是故乡。"},
  {"name": "匠人血脉", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "家里世代靠手艺吃饭，你天生手巧但眼界受限。", "modifiers": [("DEX", "+1d2*5"), ("INT", "-1d2*5")], "narrative": "七岁就能做木工小件，但书本字句像在跳舞。"},
  {"name": "天生笑面", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "亲和力拉满，却少了点威严。", "modifiers": [("APP", "+1d1*5"), ("STR", "-1d1*5")], "narrative": "谁见了这张脸都软了三分，可凶也凶不起来。"},
  {"name": "耐饿体质", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "肠胃功能特别，但长得缓慢。", "modifiers": [("CON", "+1d1*5"), ("SIZ", "-1d1*5")], "narrative": "一天一顿也能活蹦乱跳，就是个子迟迟不窜。"},
  {"name": "单亲扶持", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "只有一方长辈抚养，关爱加倍但资源减半。", "modifiers": [("POW", "+1d2*5"), ("CRE", "-1d2*5")], "narrative": "母亲/父亲一人撑起你的天，你早早学会了心疼人。"},
  {"name": "幼年变故", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "一次大病或意外，重塑了你的神经。", "modifiers": [("POW", "+1d1*5"), ("INT", "-1d1*5")], "narrative": "那场高烧之后，似乎什么都不怕了，但记忆力差了些。"},
  {"name": "中庸之资", "rarity": "common", "mode": "Normal", "scenarios": ["any"], "desc": "各方面均衡，毫无短板也无突出。", "modifiers": [], "narrative": "放在人堆里最让人放心的那种孩子。"},

  #============= RARE (8) =============
  {"name": "天生丽质", "rarity": "rare", "mode": "Normal", "scenarios": ["any"], "desc": "容貌出众，令人一见难忘。", "modifiers": [("APP", "+1d2*5")], "narrative": "从满月开始，抱你的人就络绎不绝。"},
  {"name": "铁打之躯", "rarity": "rare", "mode": "Normal", "scenarios": ["any"], "desc": "先天抵抗力极强，几乎不生病。", "modifiers": [("CON", "+1d2*5")], "narrative": "别的小孩发烧哭闹时，你正在泥地里打滚。"},
  {"name": "过目不忘", "rarity": "rare", "mode": "Normal", "scenarios": ["any"], "desc": "记忆力堪称奇迹。", "modifiers": [("INT", "+1d2*5")], "narrative": "三岁时听过的故事，隔年还能一字不差复述。"},
  {"name": "顽强意志", "rarity": "rare", "mode": "Normal", "scenarios": ["any"], "desc": "精神如磐石，很难被摧垮。", "modifiers": [("POW", "+1d2*5")], "narrative": "摔倒了从不哭着等人扶，自己就站了起来。"},
  {"name": "敏捷如猫", "rarity": "rare", "mode": "Normal", "scenarios": ["any"], "desc": "神经反应速度天生超群。", "modifiers": [("DEX", "+1d2*5")], "narrative": "抓苍蝇、接飞虫，你的手快得像道影子。"},
  {"name": "名门之后", "rarity": "rare", "mode": "Normal", "scenarios": ["any"], "desc": "家族声望提供了天然的起跑线。", "modifiers": [("CRE", "+1d2*5")], "narrative": "你的名字就是一块敲门砖。"},
  {"name": "天生神力", "rarity": "rare", "mode": "Normal", "scenarios": ["any"], "desc": "肌肉密度远超常人。", "modifiers": [("STR", "+1d2*5")], "narrative": "五岁就能抱起八岁的孩子，力气像是用不完。"},
  {"name": "魁梧体格", "rarity": "rare", "mode": "Normal", "scenarios": ["any"], "desc": "身形高大强壮，注定不凡。", "modifiers": [("SIZ", "+1d2*5")], "narrative": "在同龄人里永远高出一头，像个小巨人。"},

  #============= LEGENDARY (4) =============
  {"name": "天选之子", "rarity": "legendary", "mode": "Normal", "scenarios": ["any"], "desc": "命运的宠儿，几项能力同时绽放。", "modifiers": [("POW", "+1d3*5"), ("INT", "+1d2*5"), ("APP", "+1d2*5")], "narrative": "你天生就比别人多几分运气与从容。"},
  {"name": "麒麟儿", "rarity": "legendary", "mode": "Normal", "scenarios": ["any"], "desc": "智勇双全，体格与头脑兼得。", "modifiers": [("STR", "+1d2*5"), ("INT", "+1d3*5"), ("CON", "+1d2*5")], "narrative": "自古逢人说麟儿，你便是那传说。"},
  {"name": "星辰之眷", "rarity": "legendary", "mode": "Normal", "scenarios": ["any"], "desc": "美貌、智慧与活力集于一身。", "modifiers": [("APP", "+1d3*5"), ("DEX", "+1d2*5"), ("POW", "+1d2*5")], "narrative": "仿佛星辉洒落的婴孩，引动四方惊异。"},
  {"name": "太古遗血", "rarity": "legendary", "mode": "Normal", "scenarios": ["any"], "desc": "远古祖先的血脉在你身上觉醒。", "modifiers": [("POW", "+1d3*5"), ("SIZ", "+1d3*5"), ("CON", "+1d2*5")], "narrative": "你的啼声洪亮到不像初生儿，护士手一抖。"},

  #============= WILDCARD (2) =============
  {"name": "双魂共生", "rarity": "wildcard", "mode": "Normal", "scenarios": ["any"], "desc": "身体里藏着另一个意识，精神力异变。", "modifiers": [("POW", "+1d3*5"), ("APP", "-1d3*5")], "narrative": "有时你对着虚空说话，表情判若两人。"},
  {"name": "气运吞噬", "rarity": "wildcard", "mode": "Normal", "scenarios": ["any"], "desc": "能汲取周遭气运，但自身家运凋零。", "modifiers": [("POW", "+1d3*5"), ("INT", "+1d2*5"), ("CRE", "-1d3*5")], "narrative": "你出生那年，祖宅的槐树突然枯了一半。"},
    # ---------- citywalk · 现代都市 ----------
  #============= NEGATIVE (10) =============
  {"name": "早产儿", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "未足月落地，先天发育滞后。", "modifiers": [("CON", "-1d2*5")], "narrative": "保温箱是你的第一个家。"},
  {"name": "城中弃子", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "被家庭遗忘在都市角落。", "modifiers": [("CRE", "-1d2*5")], "narrative": "福利院的老铁门是你记忆的起点。"},
  {"name": "过敏体质", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "对无数东西过敏，活得小心翼翼。", "modifiers": [("CON", "-1d2*5")], "narrative": "别的小孩舔冰淇淋时，你只能闻奶香。"},
  {"name": "社恐倾向", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "天生的内向，面对生人浑身不自在。", "modifiers": [("APP", "-1d2*5")], "narrative": "家里来客人，你永远是躲在门后的那个。"},
  {"name": "留守烙印", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "父母长期缺席，资源与关爱双缺。", "modifiers": [("POW", "-1d1*5"), ("CRE", "-1d1*5")], "narrative": "年三十的鞭炮声里，你握着老人机等了整夜。"},
  {"name": "家道中落", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "出生时家运已败，债台高筑。", "modifiers": [("CRE", "-1d2*5")], "narrative": "你喝的第一口奶粉都是赊来的。"},
  {"name": "灾厄孪生", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "带着晦气出生，见者皆嫌。", "modifiers": [("APP", "-1d2*5")], "narrative": "街坊邻居悄悄议论，让你家换个地方住。"},
  {"name": "城市蝼蚁", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "出身于最底层的棚户区。", "modifiers": [("SIZ", "-1d2*5")], "narrative": "你的童年背景是拆迁标语和垃圾堆积。"},
  {"name": "玻璃骨骼", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "先天骨质脆弱，极易骨折。", "modifiers": [("STR", "-1d2*5")], "narrative": "别的小朋友玩滑梯，你只能在旁边看着。"},
  {"name": "福薄之光", "rarity": "negative", "mode": "Normal", "scenarios": ["citywalk"], "desc": "貌美却耗损了身体元气。", "modifiers": [("APP", "+1d1*5"), ("CON", "-1d3*5")], "narrative": "像个精美易碎的瓷娃娃，让人心疼。"},

  #============= COMMON (15) =============
  {"name": "中产之家", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "家境平稳，无冻饿之虞。", "modifiers": [], "narrative": "不奢华，也从未为吃穿发过愁。"},
  {"name": "小镇青年根", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "县城或小镇出生，视野有限但家境稳定。", "modifiers": [("CRE", "+1d1*5"), ("INT", "-1d1*5")], "narrative": "去趟省城都要兴奋三天，但家里从不断粮。"},
  {"name": "隔代亲", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "老人带大，宠溺有加，但略有娇纵。", "modifiers": [("POW", "-1d1*5"), ("APP", "+1d1*5")], "narrative": "奶奶总觉得你穿少了，零花钱永远管够。"},
  {"name": "学区房儿", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "家旁边就是好学校，但背负期望。", "modifiers": [("INT", "+1d1*5"), ("POW", "-1d1*5")], "narrative": "走五分钟进校门，背后是爸妈满满的计划表。"},
  {"name": "新闻联播娃", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "父母是体制内基层，生活规律而保守。", "modifiers": [("CRE", "+1d1*5"), ("DEX", "-1d1*5")], "narrative": "每天7点全家准时坐在电视机前，你从不敢爬高。"},
  {"name": "电子原住民", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "从小接触屏幕，视力损耗但信息敏感。", "modifiers": [("INT", "+1d2*5"), ("CON", "-1d2*5")], "narrative": "三岁就会划手机，但早早戴上了眼镜。"},
  {"name": "菜市场之家", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "父母摆摊做小生意，你打小嘴甜手快。", "modifiers": [("APP", "+1d2*5"), ("INT", "-1d2*5")], "narrative": "在吆喝声里长大，算账找零比大人还麻利。"},
  {"name": "厂区子弟", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "国营厂区长大，体格不错但生活单调。", "modifiers": [("CON", "+1d2*5"), ("CRE", "-1d2*5")], "narrative": "球场、澡堂、大食堂，你的地盘就这么大。"},
  {"name": "双语环境", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "家里说方言或外语，语言天赋早开，略有口音。", "modifiers": [("INT", "+1d1*5"), ("APP", "-1d1*5")], "narrative": "一张嘴别人就知你从哪来，但英语课永远第一。"},
  {"name": "拆迁幸运儿", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "幼时赶上拆迁，家境陡然而富但根基虚浮。", "modifiers": [("CRE", "+1d2*5"), ("POW", "-1d2*5")], "narrative": "突然搬进电梯楼，可爸妈总念叨当年院子里的无花果。"},
  {"name": "单亲公寓", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "跟一位家长挤在小公寓，亲密但有经济压力。", "modifiers": [("POW", "+1d1*5"), ("CRE", "-1d1*5")], "narrative": "饭桌上永远只有两副碗筷，但笑从不缺席。"},
  {"name": "健身成瘾之家", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "父母是健身狂魔，你的身体底子好，但学业被轻忽。", "modifiers": [("STR", "+1d2*5"), ("INT", "-1d2*5")], "narrative": "会走路就被带进健身房，蛋白质粉比奶粉先认识。"},
  {"name": "文化割裂", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "移民二代，双语思维但两边都不全然认同。", "modifiers": [("INT", "+1d1*5"), ("POW", "-1d1*5")], "narrative": "过春节想穿旗袍，出门又觉得太扎眼。"},
  {"name": "二次元世家", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "年轻的父母是资深二次元，审美拔群但社交圈怪。", "modifiers": [("APP", "+1d1*5"), ("SIZ", "-1d1*5")], "narrative": "你的胎教是动画OP，满月抓周摆的是手办。"},
  {"name": "朋友圈育儿", "rarity": "common", "mode": "Normal", "scenarios": ["citywalk"], "desc": "父母按育儿博主的方式养你，时而科学，时而折腾。", "modifiers": [("CON", "+1d1*5"), ("POW", "-1d1*5")], "narrative": "辅食精确到克，早教卡按月龄换，你成了实验田。"},

  #============= RARE (8) =============
  {"name": "精英教育预备", "rarity": "rare", "mode": "Normal", "scenarios": ["citywalk"], "desc": "高知家庭，早教资源顶尖。", "modifiers": [("INT", "+1d2*5")], "narrative": "钢琴、编程、马术，你的周末比CEO还满。"},
  {"name": "名校血统", "rarity": "rare", "mode": "Normal", "scenarios": ["citywalk"], "desc": "祖辈父母皆名校毕业，书香浸骨。", "modifiers": [("CRE", "+1d2*5")], "narrative": "家里的书架从地板顶到天花板，胎教是西哲史。"},
  {"name": "天生网红脸", "rarity": "rare", "mode": "Normal", "scenarios": ["citywalk"], "desc": "在这个看脸的时代占尽先机。", "modifiers": [("APP", "+1d2*5")], "narrative": "幼儿园毕业照就有人在网上打听这是谁家的孩子。"},
  {"name": "电竞圣体", "rarity": "rare", "mode": "Normal", "scenarios": ["citywalk"], "desc": "反应速度和手脑协调性天赋异禀。", "modifiers": [("DEX", "+1d2*5")], "narrative": "四岁第一次握鼠标，光标轨迹就让大人看呆。"},
  {"name": "城市运动健将", "rarity": "rare", "mode": "Normal", "scenarios": ["citywalk"], "desc": "身体素质拔尖，注定属于运动场。", "modifiers": [("STR", "+1d1*5"), ("CON", "+1d1*5")], "narrative": "在小区广场打闹都能看出惊人的爆发力。"},
  {"name": "富庶安稳", "rarity": "rare", "mode": "Normal", "scenarios": ["citywalk"], "desc": "家境殷实，从不必为钱发愁。", "modifiers": [("CRE", "+1d2*5")], "narrative": "保姆车接送，兴趣课随便挑，你只负责快乐。"},
  {"name": "超常专注", "rarity": "rare", "mode": "Normal", "scenarios": ["citywalk"], "desc": "对感兴趣的事物能极度沉浸。", "modifiers": [("POW", "+1d2*5")], "narrative": "拼图能拼一下午，谁也叫不动，像个小石佛。"},
  {"name": "模特胚子", "rarity": "rare", "mode": "Normal", "scenarios": ["citywalk"], "desc": "高挑的骨架和独特的五官，天生衣架。", "modifiers": [("SIZ", "+1d2*5")], "narrative": "抱着你在公园走，总有人问要不要拍童装广告。"},

  #============= LEGENDARY (4) =============
  {"name": "豪门继承人", "rarity": "legendary", "mode": "Normal", "scenarios": ["citywalk"], "desc": "生在财富顶端，且继承了优良基因。", "modifiers": [("CRE", "+1d3*5"), ("APP", "+1d2*5"), ("INT", "+1d2*5")], "narrative": "你的满月酒登上了本地新闻，礼物用卡车装。"},
  {"name": "天生领跑者", "rarity": "legendary", "mode": "Normal", "scenarios": ["citywalk"], "desc": "健康、活力、聪慧，像被都市选中的代表。", "modifiers": [("CON", "+1d3*5"), ("DEX", "+1d2*5"), ("POW", "+1d2*5")], "narrative": "幼儿园运动会，你一个人拿了三分之一的金星。"},
  {"name": "智颜双绝", "rarity": "legendary", "mode": "Normal", "scenarios": ["citywalk"], "desc": "智商超群，面容无瑕，完美得不像话。", "modifiers": [("INT", "+1d3*5"), ("APP", "+1d3*5"), ("CRE", "+1d2*5")], "narrative": "刚出生，护士就在猜测这孩子将来要上几回热搜。"},
  {"name": "时代烙印", "rarity": "legendary", "mode": "Normal", "scenarios": ["citywalk"], "desc": "你的降生恰逢世纪之交的祥瑞时刻。", "modifiers": [("POW", "+1d3*5"), ("CRE", "+1d3*5"), ("INT", "+1d2*5")], "narrative": "千禧年的钟声为你而鸣，全家都觉着这孩子非同小可。"},

  #============= WILDCARD (3) =============
  {"name": "重生者", "rarity": "wildcard", "mode": "Normal", "scenarios": ["citywalk"], "desc": "带着隐约的前世记忆，早熟得骇人，却与周围格格不入。", "modifiers": [("INT", "+1d3*5"), ("APP", "-1d3*5")], "narrative": "你总盯着某个橱窗发呆，嘴里嘟囔着“以前不是这样”。"},
  {"name": "预知梦", "rarity": "wildcard", "mode": "Normal", "scenarios": ["citywalk"], "desc": "梦境时常与现实交叠，魂不守舍。", "modifiers": [("POW", "+1d3*5"), ("CON", "-1d3*5")], "narrative": "好几次你说中还没发生的事，然后大病一场。"},
  {"name": "异界之触", "rarity": "wildcard", "mode": "Normal", "scenarios": ["citywalk"], "desc": "感官能捕捉城市缝隙里的灵异，代价是精神的孤寂。", "modifiers": [("POW", "+1d3*5"), ("SIZ", "-1d3*5")], "narrative": "地铁广告牌上的人脸，你说它们在动。"},

 # ========== 仙侠·flyaway 天赋 ==========
    #============= NEGATIVE (10) =============
    {"name": "凡骨之资", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "经脉堵塞，灵气难通。", "modifiers": [("INT", "-1d2*5")],
     "narrative": "测灵石在你手里如死石一块，人群中传来压抑的笑声。"},
    {"name": "天弃之相", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "五官怪异，被视为不祥。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "接生婆只看一眼就惊得把你扔到地上。"},
    {"name": "先天体弱", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "元气亏空，风一吹就倒。", "modifiers": [("CON", "-1d2*5")],
     "narrative": "别家娃子摸爬滚打时，你只能裹在棉被里喝药。"},
    {"name": "孽缘缠身", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "易招惹邪祟，心志不坚。", "modifiers": [("POW", "-1d2*5")],
     "narrative": "你睡觉时总睁着半只眼，仿佛在和什么东西对视。"},
    {"name": "破落宗门之后", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "家族衰败，资源全无。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "祖上阔过的证据，就是柴房里那把生锈的断剑。"},
    {"name": "痴愚之资", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "学什么都慢如老牛。", "modifiers": [("INT", "-1d2*5")],
     "narrative": "一篇口诀，别的师兄念三遍，你磕磕绊绊三百遍。"},
    {"name": "气运淡薄", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "运气差，出身也微寒。", "modifiers": [("POW", "-1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "抓周时你握了块石头，父亲的脸立刻黑了。"},
    {"name": "残肢之身", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "生来缺了一趾，行动不便。", "modifiers": [("DEX", "-1d2*5")],
     "narrative": "你总是跑在队伍最后，握剑的姿势也怪怪的。"},
    {"name": "血咒之体", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "家族被诅咒，力量会逐渐消逝。", "modifiers": [("STR", "-1d2*5")],
     "narrative": "你出生时，爷爷在你手臂上发现一圈诡异的黑纹。"},
    {"name": "厄运之子", "rarity": "negative", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "生来瘦小，难以长大。", "modifiers": [("SIZ", "-1d2*5")],
     "narrative": "六岁了还像个三岁娃娃，村里都叫你小土豆。"},

    #============= COMMON (15) =============
    {"name": "平凡农家", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "日出而作，日入而息。", "modifiers": [],
     "narrative": "你的童年带着稻香和牛粪味儿，梦里才见过仙人。"},
    {"name": "商贾之后", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "家里开杂货铺，有些积蓄但欠缺气魄。", "modifiers": [("CRE", "+1d1*5"), ("POW", "-1d1*5")],
     "narrative": "算盘你打得比谁都响，可一见血就腿软。"},
    {"name": "猎户之勇", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "从小随父打猎，体格好，识字不多。", "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "你能徒手放倒一头野猪，但书本上的字像蚊蝇。"},
    {"name": "书香门第", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "祖上出过举人，家中藏书不少。", "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "三岁吟诗，五岁作对，可惜手无缚鸡之力。"},
    {"name": "微末灵根", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "有一丝木灵根，但身体受不住灵力滋养。", "modifiers": [("INT", "+1d2*5"), ("CON", "-1d2*5")],
     "narrative": "你会让种子发芽得比别家快，代价是每月必发一次高烧。"},
    {"name": "半妖遗孤", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "体内流着一丝狐妖的血，容貌魅惑但身形娇小。", "modifiers": [("APP", "+1d2*5"), ("SIZ", "-1d2*5")],
     "narrative": "镇上的人一边骂你狐媚子，一边偷偷多看你几眼。"},
    {"name": "剑修遗腹子", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "父亲是散修剑客，留给你的只有一本剑谱和贫穷。", "modifiers": [("DEX", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "你拿树枝当剑，在泥地上把一招‘白虹贯日’练了几万遍。"},
    {"name": "丹药童子", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "父母为丹师试药，拿你当药罐子，百毒不侵却脑子不太灵光。", "modifiers": [("CON", "+1d2*5"), ("INT", "-1d2*5")],
     "narrative": "你吃过的毒丹比饭还多，浑身是宝但反应总慢半拍。"},
    {"name": "阵道启蒙", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "天生对符纹敏感，但手脚笨拙。", "modifiers": [("INT", "+1d1*5"), ("DEX", "-1d1*5")],
     "narrative": "你能一眼看出阵眼，可画符时总歪歪扭扭。"},
    {"name": "佛寺俗家", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "父母是寺庙信徒，自小吃斋念佛，心志坚定，身形清瘦。", "modifiers": [("POW", "+1d2*5"), ("SIZ", "-1d2*5")],
     "narrative": "别的孩子抢糖时，你已在盘坐入定，一盏青灯为伴。"},
    {"name": "灵脉矿工之子", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "家旁有废弃灵矿，灵气淬炼了精神，矿尘损害了肺腑。", "modifiers": [("POW", "+1d1*5"), ("CON", "-1d1*5")],
     "narrative": "你呼吸时肺里有风声，可赌石从没输过。"},
    {"name": "绝世琴师血脉", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "母亲是乐坊花魁，继承了好相貌和柔弱的身体。", "modifiers": [("APP", "+1d2*5"), ("STR", "-1d2*5")],
     "narrative": "手指细长，天生是弹奏的料，可惜扛不动任何重物。"},
    {"name": "炼器学徒", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "在炼器铺长大，手巧但家贫。", "modifiers": [("DEX", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "七岁就会修灵锄，补锅手艺一流，可买不起一把属于自己的飞剑。"},
    {"name": "父母一凡一修", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "父亲是外门弟子，母亲是村妇，留了点微薄家底却少了磨练。", "modifiers": [("CRE", "+1d1*5"), ("POW", "-1d1*5")],
     "narrative": "你有几颗灵石零花钱，可一遇事儿就哭着找娘。"},
    {"name": "被弃养后收养", "rarity": "common", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "襁褓中被丢在路边，被好心人捡回，性子坚毅但相貌遭过损。", "modifiers": [("POW", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "左脸有道小小的疤，据说是被野狗舔的，但你笑起来比谁都暖。"},

    #============= RARE (8) =============
    {"name": "天灵根", "rarity": "rare", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "单一属性灵根极为纯粹。", "modifiers": [("INT", "+1d2*5")],
     "narrative": "入门测试时，水晶球亮成一颗小太阳。"},
    {"name": "天生剑骨", "rarity": "rare", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "骨骼清奇，如同为剑而生。", "modifiers": [("DEX", "+1d2*5")],
     "narrative": "第一次握剑，剑身便发出清越鸣响。"},
    {"name": "道体仙姿", "rarity": "rare", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "仙风道骨，气质出尘。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "长辈说，你像是从古画里走出来的仙童。"},
    {"name": "凤凰血脉", "rarity": "rare", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "稀薄的凤凰血脉，恢复力极强。", "modifiers": [("CON", "+1d2*5")],
     "narrative": "高烧四十度，一觉睡醒又活蹦乱跳，令赤脚医生瞠目。"},
    {"name": "仙门嫡系", "rarity": "rare", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "出生在某个中等仙门之内，资源不愁。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "你的摇篮是个低阶法器，铃铛都是下品灵石镶的。"},
    {"name": "通明剑心", "rarity": "rare", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "心志澄澈，不易被外物动摇。", "modifiers": [("POW", "+1d2*5")],
     "narrative": "不论外界多嘈杂，你的剑意总是纹丝不动。"},
    {"name": "龙血传承", "rarity": "rare", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "遥远的真龙血脉，让力气远超同龄人。", "modifiers": [("STR", "+1d2*5")],
     "narrative": "三岁举石锁，吓得族长连喊祖宗。"},
    {"name": "慧根深种", "rarity": "rare", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "悟性惊人，举一反三。", "modifiers": [("INT", "+1d2*5")],
     "narrative": "长老讲道，其余弟子尚在困惑，你已颔首微笑。"},

    #============= LEGENDARY (4) =============
    {"name": "真仙转世", "rarity": "legendary", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "传说中的仙人重新投胎。", "modifiers": [("POW", "+1d3*5"), ("INT", "+1d2*5"), ("APP", "+1d2*5")],
     "narrative": "出生那夜，紫气东来三千里，一只仙鹤落在你家屋檐。"},
    {"name": "圣体道胎", "rarity": "legendary", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "天生的修道圣体，万法不侵。", "modifiers": [("CON", "+1d3*5"), ("STR", "+1d2*5"), ("INT", "+1d2*5")],
     "narrative": "皮肤光洁如玉，蚊虫不叮，寒暑不侵。"},
    {"name": "九脉天资", "rarity": "legendary", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "身轻如燕，家学渊源。", "modifiers": [("DEX", "+1d3*5"), ("INT", "+1d2*5"), ("CRE", "+1d2*5")],
     "narrative": "八大世家的拜帖在你满月当天就送到了。"},
    {"name": "混沌灵根", "rarity": "legendary", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "亿万年不遇的混沌灵根，包容万象。", "modifiers": [("INT", "+1d3*5"), ("POW", "+1d3*5"), ("CON", "+1d2*5")],
     "narrative": "任何法术你只看一遍，灵气在你体内如臂使指。"},

    #============= WILDCARD (3) =============
    {"name": "魔种寄生", "rarity": "wildcard", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "丹田内有一颗魔种，赋予强大精神力量，但时刻吞噬生机。", "modifiers": [("POW", "+1d3*5"), ("CON", "-1d3*5")],
     "narrative": "你常在梦里与那个魔影对话，醒来时吐的黑血能把床单蚀出洞。"},
    {"name": "逆天改命", "rarity": "wildcard", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "天资绝世，但出生在乞丐窝。", "modifiers": [("INT", "+1d3*5"), ("CRE", "-1d3*5")],
     "narrative": "靠听墙角学会认字，三岁出口成章，可身上只有破麻袋御寒。"},
    {"name": "妖皇血醒", "rarity": "wildcard", "mode": "Normal", "scenarios": ["flyaway"],
     "desc": "上古妖皇血脉觉醒，力可扛鼎，相貌却兽化。", "modifiers": [("STR", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "头上长着两只小角，臂有鳞片，同龄人怕你，野兽却亲近你。"},

# ========== 奇幻·dragonfire 天赋 ==========
    #============= NEGATIVE (10) =============
    {"name": "农奴之子", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "世代为奴，没有自由。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "你人生的第一件玩具，是领主儿子丢掉的马鞭。"},
    {"name": "黑暗诅咒", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "被黑巫师施了咒，体质极虚。", "modifiers": [("CON", "-1d2*5")],
     "narrative": "你的影子比别人的淡，老人们看见都绕道走。"},
    {"name": "狰狞面容", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "长的像是兽人混血失败品。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "母亲第一次喂奶时，差点尖叫出来。"},
    {"name": "战乱遗孤", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "在炮火中出生，极度缺乏安全感。", "modifiers": [("POW", "-1d2*5")],
     "narrative": "一听到马蹄声，你就条件反射地躲进床底。"},
    {"name": "痴呆儿", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "脑子天生不灵光。", "modifiers": [("INT", "-1d2*5")],
     "narrative": "五岁才会说一句完整的话，村童们叫你傻大个。"},
    {"name": "跛子", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "右腿天生短一截，行动不便。", "modifiers": [("DEX", "-1d2*5")],
     "narrative": "别的孩子追逐打闹时，你在一旁用树棍刻小人。"},
    {"name": "遭歧视的半兽人", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "兽人血统在身上太明显了。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "酒馆门上总贴着‘半兽人与狗不得入内’。"},
    {"name": "饥荒烙印", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "大饥荒中出生，从没吃饱过。", "modifiers": [("STR", "-1d2*5")],
     "narrative": "胃是无底洞，可永远填不满胳膊上的肉。"},
    {"name": "流浪儿", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "从小在街头流浪，瘦骨嶙峋。", "modifiers": [("SIZ", "-1d2*5")],
     "narrative": "老鼠是你的蛋白质来源，桥洞是你的卧室。"},
    {"name": "厄运缠身", "rarity": "negative", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "出生弄塌了房子，被视为扫把星。", "modifiers": [("CRE", "-1d1*5"), ("POW", "-1d1*5")],
     "narrative": "同村的人凑钱把你送得越远越好。"},

    #============= COMMON (15) =============
    {"name": "平民子弟", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "城镇中的普通一员。", "modifiers": [],
     "narrative": "爸爸是面包师，妈妈洗衣，你负责在巷子里疯玩。"},
    {"name": "商人家族", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "家里开杂货铺，有些积蓄但缺乏锻炼。", "modifiers": [("CRE", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "数钱很快，可搬一袋面粉就喘。"},
    {"name": "佣兵养子", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "被佣兵团的大老粗们带大，能打不太能想。", "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "你会用匕首削水果，但不会写自己的名字。"},
    {"name": "没落贵族", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "有贵族头衔而无实财，自尊极高却内心脆弱。", "modifiers": [("CRE", "+1d2*5"), ("POW", "-1d2*5")],
     "narrative": "你还穿着祖父的丝绸衬衣，但肘部已磨破。"},
    {"name": "矮人混血", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "矮人血脉让你壮实耐造，但动作有些笨重。", "modifiers": [("CON", "+1d2*5"), ("DEX", "-1d2*5")],
     "narrative": "骨头硬得像铁，可跳舞时总踩舞伴的脚。"},
    {"name": "精灵遗孤", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "被遗弃的半精灵，美貌柔弱。", "modifiers": [("APP", "+1d2*5"), ("CON", "-1d2*5")],
     "narrative": "耳朵尖尖的，皮肤白得透明，感冒从没好利索过。"},
    {"name": "法师学徒之子", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "父亲是低阶法师，从小看书，长得瘦小。", "modifiers": [("INT", "+1d1*5"), ("SIZ", "-1d1*5")],
     "narrative": "四岁就能点燃蜡烛，但还没扫帚高。"},
    {"name": "狼孩", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "被野狼养了几年，野性强韧，但举止粗鲁。", "modifiers": [("POW", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "闻到生肉就咽口水，花了三年才学会用刀叉。"},
    {"name": "马戏团小丑之子", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "在马戏团长大的你，身法灵活，但口袋空空。", "modifiers": [("DEX", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "三米高的独轮车骑得飞起，却买不起一双新鞋。"},
    {"name": "教会长大的孤儿", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "在唱诗班长大的你，信仰坚定，但体力劳动少。", "modifiers": [("POW", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "能背诵整本圣典，可劈柴时差点砍掉脚趾头。"},
    {"name": "猎人后裔", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "父辈是护林人，熟悉森林，但不通文墨。", "modifiers": [("CON", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "能分辨五十种动物足迹，却分不清字母b和d。"},
    {"name": "半身人血脉", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "半身人远亲，个子极小但异常灵巧。", "modifiers": [("SIZ", "-1d2*5"), ("DEX", "+1d2*5")],
     "narrative": "比同龄人矮了两个头，但偷苹果的本事一等一。"},
    {"name": "破落骑士世家", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "家里唯一的财产是一套生锈的铠甲。", "modifiers": [("STR", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "从小举着比自己还重的大剑练习，吃的却是黑面包屑。"},
    {"name": "龙裔远亲", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "血脉里有一点龙族血统，力气略大，皮肤略粗。", "modifiers": [("STR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "手背上有几片小鳞片，总下意识藏进袖子。"},
    {"name": "学士之后", "rarity": "common", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "父母是皇家图书馆管理员，博学但久坐体弱。", "modifiers": [("INT", "+1d2*5"), ("CON", "-1d2*5")],
     "narrative": "七岁就通读大陆通史，可跑几步路就脸色发白。"},

    #============= RARE (8) =============
    {"name": "纯血贵族", "rarity": "rare", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "古老家族的嫡系血脉。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "摇篮边挂满了封地纹章。"},
    {"name": "天生魔力", "rarity": "rare", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "自然魔力亲和，念咒自带加成。", "modifiers": [("INT", "+1d2*5")],
     "narrative": "儿歌念着念着，床头的玩偶就飘起来了。"},
    {"name": "巨龙血统", "rarity": "rare", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "激活了龙血，力大无穷。", "modifiers": [("STR", "+1d2*5")],
     "narrative": "拔出萝卜带出个大坑，这把子力气让农夫们张大了嘴。"},
    {"name": "精灵公主的馈赠", "rarity": "rare", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "超凡脱俗的美貌。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "连街边的野猫都会过来蹭你的裙摆。"},
    {"name": "圣骑士祝福", "rarity": "rare", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "受光明神祝福，意志坚如钢。", "modifiers": [("POW", "+1d2*5")],
     "narrative": "直视邪异之物时，它们竟畏缩后退。"},
    {"name": "大天使之息", "rarity": "rare", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "体质被圣光洗炼，百病不生。", "modifiers": [("CON", "+1d2*5")],
     "narrative": "那次瘟疫肆虐，全城只有你还在广场喂鸽子。"},
    {"name": "矮人大师天赋", "rarity": "rare", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "极致的巧手，仿佛铁与火之子。", "modifiers": [("DEX", "+1d2*5")],
     "narrative": "三岁拼好的机械鸟，翅膀能扑腾好几下。"},
    {"name": "贤者转世", "rarity": "rare", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "脑海里偶尔闪现不属于现世的知识。", "modifiers": [("INT", "+1d2*5")],
     "narrative": "说起上古魔法原理时，老法师的水晶球裂了条缝。"},

    #============= LEGENDARY (4) =============
    {"name": "神之后裔", "rarity": "legendary", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "祖先是某位次级神祇。", "modifiers": [("POW", "+1d3*5"), ("APP", "+1d2*5"), ("INT", "+1d2*5")],
     "narrative": "出生那刻，教堂的圣钟不撞自鸣，白鸽盘旋不散。"},
    {"name": "泰坦血脉", "rarity": "legendary", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "远古泰坦的巨力在体内流淌。", "modifiers": [("STR", "+1d3*5"), ("CON", "+1d2*5"), ("SIZ", "+1d2*5")],
     "narrative": "第一次打喷嚏，把奶妈吹出了三米远。"},
    {"name": "龙血王族", "rarity": "legendary", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "红龙血脉与王族结合的后代。", "modifiers": [("POW", "+1d3*5"), ("STR", "+1d2*5"), ("CRE", "+1d2*5")],
     "narrative": "瞳孔是竖立的金色，国王在你满月时亲自封地。"},
    {"name": "元素之子", "rarity": "legendary", "mode": "Normal", "scenarios": ["dragonfire"],
     "desc": "受四大元素祝福的宠儿。", "modifiers": [("DEX", "+1d2*5"), ("INT", "+1d3*5"), ("CON", "+1d2*5")],
     "narrative": "一哭屋外就下雨，一笑彩虹跨过城堡。"},
    # ========== 江湖武侠·loneblade 天赋 ==========
    #============= NEGATIVE (10) =============
    {"name": "先天残脉", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "经脉天生受损，内力流转滞涩。", "modifiers": [("CON", "-1d2*5")],
     "narrative": "师父替你摸骨时眉头越皱越紧，最后只叹了口气。"},
    {"name": "弃婴", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "被遗弃在荒郊野外的婴孩。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "连亲生父母是谁都不知道，襁褓里只有半块冷硬的饼。"},
    {"name": "面相凶煞", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "天生一副恶人相，让人避之不及。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "婴孩时，抱过你的人都说这娃娃眉目带煞。"},
    {"name": "痨病鬼", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "先天肺气不足，动则咳喘。", "modifiers": [("CON", "-1d2*5")],
     "narrative": "屋子里常年飘着药味儿，同门都怕被你染上。"},
    {"name": "心眼俱钝", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "学武的悟性差得惊人。", "modifiers": [("INT", "-1d2*5")],
     "narrative": "一招最粗浅的入门拳法，旁人三月小成，你练了一年还走样。"},
    {"name": "胆小如鼠", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "生来怯懦，见血就晕。", "modifiers": [("POW", "-1d2*5")],
     "narrative": "杀鸡的场面让你做了整月噩梦，醒来枕巾湿了大半。"},
    {"name": "跛足", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "一条腿天生使不上力，下盘飘浮。", "modifiers": [("DEX", "-1d2*5")],
     "narrative": "别的孩童追跑打闹，你走快些都要扶着墙喘。"},
    {"name": "力弱如鸡", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "臂力孱弱，连同龄女娃都比不过。", "modifiers": [("STR", "-1d2*5")],
     "narrative": "提桶水都晃得满身湿，被村里顽童笑作纸片人。"},
    {"name": "侏儒之身", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "身形矮小得异于常人。", "modifiers": [("SIZ", "-1d2*5")],
     "narrative": "七岁还不及五岁小儿高，总被错认为更小的孩童。"},
    {"name": "仇家遗腹", "rarity": "negative", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "全家被仇敌灭门，仅你被藏在地窖躲过一劫。", "modifiers": [("CRE", "-1d1*5"), ("POW", "-1d1*5")],
     "narrative": "你是从血泊里被扒出来的，哭得嗓子彻底哑了。"},

    #============= COMMON (15) =============
    {"name": "农家子弟", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "生在寻常农户，本分老实。", "modifiers": [],
     "narrative": "爹娘只盼你早日下地干活，江湖不过说书人口中故事。"},
    {"name": "镖局之后", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "家里开着间小镖局，有些功夫底子却没读过书。", "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "三岁骑木马，五岁耍花枪，可三字经到七岁还背不全。"},
    {"name": "书香门第", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "祖上是秀才，满腹诗书却手无缚鸡之力。", "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "小小年纪作得一手好诗，可被邻家娃子一推就倒。"},
    {"name": "渔家儿女", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "在水边长大，水性极佳，身形匀称但见识短浅。", "modifiers": [("DEX", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "能在水里憋气一盏茶，可出了渔村就分不清东南西北。"},
    {"name": "铁匠之子", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "从小抡锤打铁，膂力过人但反应偏慢。", "modifiers": [("STR", "+1d2*5"), ("DEX", "-1d2*5")],
     "narrative": "八岁就能挥八斤小锤，可躲沙包时总被砸个正着。"},
    {"name": "戏班出身", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "父母是草台班子的伶人，你身段柔软但身份低贱。", "modifiers": [("DEX", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "翻筋斗劈叉信手拈来，可正经人家都瞧不起你这出身。"},
    {"name": "医馆药童", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "在药铺里泡大，懂些医理但身子骨没打熬好。", "modifiers": [("CON", "+1d2*5"), ("STR", "-1d2*5")],
     "narrative": "闻闻味就知什么药材，可扛麻袋走不了半条街。"},
    {"name": "丐帮边缘", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "父母是丐帮底层弟子，练就一副厚脸皮和硬命。", "modifiers": [("POW", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "乞食时被泼泔水也不哭，但粗粝日子磨糙了脸。"},
    {"name": "猎户之后", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "深山里长大，耳聪目明却不懂人情世故。", "modifiers": [("CON", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "追踪野兔比追人还准，可进了镇子连问路都脸红。"},
    {"name": "武馆杂役", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "爹娘是武馆的烧火佣人，你偷师学了些三脚猫功夫。", "modifiers": [("DEX", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "蹲在墙角比划人家练拳，竟也学得几分样子。"},
    {"name": "官差家眷", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "父辈是衙门小吏，规矩森严，养出些威势但缺少历练。", "modifiers": [("POW", "+1d1*5"), ("CON", "-1d1*5")],
     "narrative": "说话自带三分官腔，可淋场雨就发三天烧。"},
    {"name": "绣娘之后", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "母亲是刺绣巧手，你的手指灵巧但性子软和。", "modifiers": [("DEX", "+1d1*5"), ("POW", "-1d1*5")],
     "narrative": "穿针引线比耍刀弄枪更顺手，见人争吵心里先怯了。"},
    {"name": "走镖遗孤", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "父亲走镖丧命，母亲含辛茹苦，你懂事早却难免心重。", "modifiers": [("POW", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "比同龄孩子更知冷暖，可衣裳上的补丁总摞得格外厚。"},
    {"name": "番邦后裔", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "高鼻深目，身形壮硕但遭中原人排挤。", "modifiers": [("SIZ", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "骨架比汉家娃子大一圈，可巷子里总有人冲你扔石子。"},
    {"name": "佃户之子", "rarity": "common", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "租种地主薄田，挨饿是常事，练就了耐饿的肠胃。", "modifiers": [("CON", "+1d1*5"), ("SIZ", "-1d1*5")],
     "narrative": "饿上两顿照样满地跑，就是个子总窜不起来。"},

    #============= RARE (8) =============
    {"name": "天生神力", "rarity": "rare", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "膂力自娘胎里便远超常人。", "modifiers": [("STR", "+1d2*5")],
     "narrative": "五岁举石锁，九岁能抱着一头小牛犊走半里地。"},
    {"name": "根骨奇佳", "rarity": "rare", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "天生一副练武的好胚子，铜皮铁骨。", "modifiers": [("CON", "+1d2*5")],
     "narrative": "棍棒打在身上竟能反震开，教头连声称奇。"},
    {"name": "悟性超群", "rarity": "rare", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "看过的招式一遍就能模仿七八分。", "modifiers": [("INT", "+1d2*5")],
     "narrative": "师父演示完尚未开口，你已在旁比划得有模有样。"},
    {"name": "玉树临风", "rarity": "rare", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "朗眉星目，风姿俊秀。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "逢年过节，媒婆快把你家门槛踏平了。"},
    {"name": "铁骨丹心", "rarity": "rare", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "性子坚毅果敢，生来有一股侠气。", "modifiers": [("POW", "+1d2*5")],
     "narrative": "路见不平，哪怕对方高你一头也敢上前理论。"},
    {"name": "身轻如燕", "rarity": "rare", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "柔韧与轻盈仿佛是刻在骨头里的。", "modifiers": [("DEX", "+1d2*5")],
     "narrative": "捉迷藏从未被找到过，爬树攀墙如履平地。"},
    {"name": "名门之后", "rarity": "rare", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "出身武林世家，自幼耳濡目染。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "抓阄时满地兵器谱和拳经，长辈们的笑声比爆竹还响。"},
    {"name": "虎背熊腰", "rarity": "rare", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "骨架宽大，身形伟岸，天生猛将胚子。", "modifiers": [("SIZ", "+1d2*5")],
     "narrative": "襁褓时就比别家婴孩重上一倍，接生婆差点没抱住。"},

    #============= LEGENDARY (4) =============
    {"name": "武曲降世", "rarity": "legendary", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "传说中武曲星君转世，奇经八脉先天自通。", "modifiers": [("STR", "+1d3*5"), ("CON", "+1d2*5"), ("POW", "+1d2*5")],
     "narrative": "出生时屋内亮如白昼，房上瓦片被一股气劲冲开。"},
    {"name": "谪仙之姿", "rarity": "legendary", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "形貌气质不似凡间俗子，且兼灵台清明。", "modifiers": [("APP", "+1d3*5"), ("DEX", "+1d2*5"), ("INT", "+1d2*5")],
     "narrative": "都说你投错胎，该去天上做神仙才是。"},
    {"name": "侠魁血脉", "rarity": "legendary", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "父系是前代武林盟主，血脉与家学皆属顶尖。", "modifiers": [("POW", "+1d3*5"), ("CRE", "+1d2*5"), ("INT", "+1d2*5")],
     "narrative": "满月宴上，各大派掌门竟亲自送来贺礼。"},
    {"name": "九阳之体", "rarity": "legendary", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "纯阳体质，内力修行一年可抵旁人十年。", "modifiers": [("CON", "+1d3*5"), ("INT", "+1d2*5"), ("STR", "+1d2*5")],
     "narrative": "大雪天你单衣在外面玩，抱回来时浑身还冒着热气。"},

    #============= WILDCARD (3) =============
    {"name": "血仇之种", "rarity": "wildcard", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "全家被魔教屠戮，仇恨淬炼出惊人意志，却摧毁了天真。", "modifiers": [("POW", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "那双眼睛里没有童真，只有烧不尽的火，笑时比哭更让人怕。"},
    {"name": "回光蛊", "rarity": "wildcard", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "自幼被种下奇蛊，濒死时会爆发巨力，平时却在啃噬生机。", "modifiers": [("STR", "+1d3*5"), ("CON", "-1d3*5")],
     "narrative": "你时常胸口绞痛苦着醒来，可上一次差点死时，硬生生把一头豹子撕成两半。"},
    {"name": "盗圣之子", "rarity": "wildcard", "mode": "Normal", "scenarios": ["loneblade"],
     "desc": "父亲是天下第一神偷，你继承了他的巧手，也继承了他的恶名。", "modifiers": [("DEX", "+1d3*5"), ("CRE", "-1d3*5")],
     "narrative": "当年偷遍大内的本事仿佛流在血里，可走到何处衙门的捕快都盯着你。"}

    # ====== 把你原来那一大堆都按这个结构补全 ======
    # 大多数现代题材的天赋，加上：
    #   "mode": "Normal", "scenarios": ["citywalk"],
    # 通用一点的（健身爱好者、平平无奇等），加上：
    #   "mode": "Normal", "scenarios": ["any"],
]

# ============================================================
# 骰子
# ============================================================
def roll_dice(expr):
    if isinstance(expr, (int, float)):
        return int(expr)
    expr = str(expr).strip()
    def _replace(m):
        n = int(m.group(1)) if m.group(1) else 1
        s = int(m.group(2))
        return str(sum(random.randint(1, s) for _ in range(n)))
    rolled = re.sub(r'(\d*)d(\d+)', _replace, expr)
    if rolled.startswith('+'):
        rolled = rolled[1:]
    return int(eval(rolled))


def filter_pool(pool, scenario_tag, mode_tag):
    """根据当前场景 + 模式过滤天赋池。"""
    out = []
    for t in pool:
        if t.get("mode", "Normal") != mode_tag:
            continue
        scs = t.get("scenarios", ["any"])
        if "any" in scs or scenario_tag in scs:
            out.append(t)
    return out


def draw_talents(pool, scenario_tag, mode_tag, n=3):
    candidates = filter_pool(pool, scenario_tag, mode_tag)
    if not candidates:
        return []
    weights = [RARITY_WEIGHTS.get(t.get("rarity", "common"), 50)
               for t in candidates]
    chosen = []
    pool_copy = list(candidates)
    while pool_copy and len(chosen) < n:
        idx = random.choices(range(len(pool_copy)), weights=weights)[0]
        chosen.append(pool_copy.pop(idx))
        weights.pop(idx)
    return chosen

# ============================================================
# 派生属性等级
# ============================================================
ASSET_TIERS = [
    (-5, "负债累累"), (2, "身无分文"), (5, "贫穷"), (10, "小康"),
    (20, "中产"), (50, "富裕"), (float('inf'), "天龙人"),
]
FAME_TIERS = [
    (-10, "恶名昭著"), (-1, "小有恶名"), (10, "默默无闻"),
    (20, "小有名气"), (50, "扬名在外"), (float('inf'), "四海皆知"),
]
KNOWLEDGE_TIERS = [
    (2, "蒙昧"), (4, "愚钝"), (15, "正常"),
    (30, "见多识广"), (50, "博古通今"), (float('inf'), "当世大儒"),
]
EDU_TIERS = [
    (1, "丈育"), (4, "基本文盲"), (12, "识文断字"), (15, "等同初中"),
    (18, "等同高中"), (22, "等同本科"), (25, "等同硕士"), (float('inf'), "等同博士及以上"),
]


def get_tier(value, tiers):
    for threshold, name in tiers:
        if value < threshold:
            return name
    return tiers[-1][1]

# ============================================================
# system prompt
# ============================================================
def build_system_prompt(c):
    talents_text = "\n".join(
        f"  - 【{RARITY_CONFIG.get(t.get('rarity','common'),{}).get('label','')}】"
        f"{t['name']}：{t.get('narrative', t.get('desc',''))}"
        for t in c["talents"]
    ) or "  （无）"
    attrs = c["final_attributes"]
    attr_text = "  ".join(f"{k}={v}" for k, v in attrs.items())
    extra = f"\n额外设定：{c['extra_info']}" if c.get('extra_info') else ""
    backstory = (f"\n背景故事：{c['backstory']}" if c.get('backstory')
                 else "\n背景故事：（请你根据属性自行编排）")
    max_hp = (attrs.get("SIZ", 50) + attrs.get("CON", 50)) // 10
    
    # --- Check for Edu Block ---
    if c.get("has_compulsory_edu"):
        edu_block = (
            "- EDU（受教育程度，年）：\n"
            "  · **1~18 岁系统会自动每年 +1**（代表正常成长 / 上学），你**不要**主动加 EDU。\n"
            "  · 但如果某年因重大原因（重病、家变、辍学、战乱、监禁等）影响学业，"
            "请在 adjustments 中给一个负 EDU（-1 ~ -3），整段 1-18 岁累计扣减系统会限制在 -10 以内。\n"
            "  · **19 岁及以后 EDU 完全由你掌握**：上大学时 +1/年；研究生 +1/年；提前毕业、辍学、重读等都自由发挥。"
        )
    else:
        edu_block = (
            "- EDU（受教育/修为/历练）：\n"
            "  · 该世界没有义务教育制度, EDU 不会自动增长，**完全由你掌握**。\n"
            "  · 你可以把 EDU 理解为角色的历练程度——拜师、开蒙、读书、闯荡、传授等剧情都可以给正向 EDU。\n"
            "  · 懒散、错过机缘、被废修为、被禁锢等可以给负向 EDU。\n"
            "  · 等级显示参考：1=蒙昧 6=学龄前/略识字 12=小学/识文断字 15=初中 18=高中/秀才 22=本科/举人 25=硕士/进士 25+=博士及以上/翰林。"
        )
        
    # --- Check for Fast Mode ---
    fast_block = ""
    if c.get("fast_mode"):
        fast_block = (
            "\n【⚡快速模式】游戏将在角色 40 岁时结束，"
            "请在剧情节奏上让 0~40 岁的人生密度合理（前期成长、中期高潮）。"
        )
        
    # --- Check for Skill Check Mode (MOVED HERE) ---
    if c.get("skill_checks_enabled", True):
        # Assuming ATTRIBUTES is defined globally (e.g., ATTRIBUTES = ["STR", "CON", ...])
        # If it's not, you can replace the {', '.join(...)} block with hardcoded stats.
        skill_block = f"""
【🎲 鉴定系统（重要选择由骰子决定）】
本游戏中，**有失败可能的选择**由程序投 1d100 vs 属性来判定，**你不再决定胜负**。
- 你给出的每个选项可以包含两个可选字段：`checks` 和 `difficulty`。
- checks: 1-2 个属性键（STR, CON, POW, DEX, APP, SIZ, INT, CRE, LUCK）。
- difficulty: "easy" / "normal" / "hard"。
  · easy   = 双骰取优（更容易过）
  · normal = 单骰
  · hard   = 双骰取劣（极难，**只用在真正棘手的情境**）
- 如果选项是纯偏好选择（比如"选什么大学专业"），省略 checks（设为 []）或不写。
- 一次给玩家的 3 个选项里，建议 1-2 个有 checks、1 个左右是纯偏好。
- 鉴定本身已代表"有难度的事"，hard 必须节制使用。
- 程序投完后会发回"完胜/险胜/完败"，你**只负责按结果写故事**。
"""
    else:
        skill_block = """
【🎭 无鉴定模式】
本局游戏不使用骰子鉴定。所有选择的结果由你根据角色属性、天赋和故事逻辑自行决定。
请在叙事中自然地赋予成功或失败，保持故事的戏剧性。
"""
    
    # Now, return the compiled prompt
    return f"""你是"AI人生重开手账"游戏的叙事AI。你需要根据角色设定和属性推演ta的人生事件，生动、有戏剧性地讲述每一年发生的故事。
    
【世界设定】
{c['scene_name']}：{c['scene_desc']}
【角色基本信息】
性别：{c['gender']}　种族：{c['race']}{extra}{backstory}
【角色出生时属性（已锁定，不可改动）】
{attr_text}
最大生命值 HP_MAX = (SIZ + CON) // 10 = {max_hp}
【天赋】
{talents_text}
{fast_block}
【⛔ 严格规则——基础属性已锁定】
- STR/CON/POW/DEX/APP/SIZ/INT/CRE/LUCK 这些**基础属性出生时就已固定**，**除非是惊人的其余，否则不应改动它们**。
- 基础属性代表的是该角色在同龄人中的相对水平。50为普普通通，30为常规意义下的最差（通过特质可以跌破30，那就是出奇的差），70以上为常规意义上的极好，90+（通过特质达到）就是超凡脱俗。
- 作为确认补充："STR": "肌肉强度，影响体力劳动、战斗力。",
    "CON": "身体素质，影响耐病、耐疲劳。",
    "POW": "意志力，影响精神抗性、专注力。",
    "DEX": "敏捷度，影响反应、灵巧度。",
    "APP": "外貌，影响第一印象、社交。",
    "SIZ": "体型，影响存在感、力量与生命。",
    "INT": "智力，影响学习与思辨。",
    "CRE": "家境，与角色自身财富无关，AI 据此判定起点。",
- adjustments 中几乎不会出现这些键。一生可能会有一次或两次改变。
- 你能改的只有：HP / ASSET / FAME / KNOWLEDGE / EDU。
【❤️ HP】
- HP_MAX = (SIZ + CON) // 10 = {max_hp}。系统每年自然恢复 1 HP。
- 普通感冒 0~-1，重感冒/小事故 -1~-2，重病/重伤 -3~-5，濒死/重大灾难 -5~-10。
- HP ≤ 0 即死亡；突发意外死亡也可直接 alive=false。
【其他派生】
- ASSET、FAME、KNOWLEDGE 整数变化。FAME如果为负则代表恶名远扬，为正则代表好名声。如果什么都不做的话FAME需要控制在-2-2之间。同时每一点大约等于在正常情况下，普通人全身心投入这方面一年之后的成果。（例如，普通人花一整年攒钱就只等于ASSET+1，花一整年学习等于EDU+1）
- KNOWLEDGE和EDU的区别在于一个是综合经验和学识，一个是学术成就。
{edu_block}
【叙事】
1. 事件要符合属性、天赋、家境、世界观。
2. 当天赋给出的背景和属性冲突时，以属性为准，但要在背景中找补。（e.g. 天赋是家庭富裕但实际CRE只有30？你出生的时候家里破产了。）
3. has_choice 大约每5-8年一次重要决定。给出的三个选择要利用到角色的不同属性（但不要明说）。同时特别重要的剧情节点可以适当采用同年多次has_choice的做法以确保剧情合理，但谨慎使用此功能。
4. narrative 不要包含"第X年"前缀。
{skill_block}
【输出格式】（严格 JSON，只输出 JSON）
{{
  "narrative": "本年事件描述（一句话到 300 字之间）",
  "has_choice": false,
  "choices": {{
    "A": {{"text": "选项A描述", "checks": ["STR"], "difficulty": "normal"}},
    "B": {{"text": "选项B描述", "checks": ["INT","POW"], "difficulty": "hard"}},
    "C": {{"text": "选项C描述（纯偏好选择）", "checks": [], "difficulty": null}}
  }},
  "adjustments": {{"HP": -2, "ASSET": 1, "FAME": -3, "KNOWLEDGE": 1, "EDU": -1}},
  "alive": true,
  "cause_of_death": null
}}
"""

def parse_ai_json(text):
    text = text.strip()
    m = re.search(r'```(?:json)?\s*(\{.*\})\s*```', text, re.DOTALL)
    if m:
        text = m.group(1)
    else:
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            text = m.group(0)
    return json.loads(text)

# ============================================================
# 配置文件
# ============================================================
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".ai_life_remake_config.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(data):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def clear_config():
    try:
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
    except Exception:
        pass

# ============================================================
# v0.5 expandable mode interface
# main.py will prefer these functions/settings if present.
# ============================================================

MODE_ID = "normal"
MODE_LABEL = "普通人生"
MODE_DESCRIPTION = "标准人生模拟。"
TALENT_MODE_TAG = "Normal"

# One click = one timestamp.
# Base mode: year 0, age 0. One click = +1 year, +1 age.
TIME_CONFIG = {
    "tick_key": "time_tick",
    "age_key": "age_value",
    "tick_label": "年",
    "age_label": "岁",
    "start_tick": 0,
    "start_age": 0,
    "tick_step": 1,
    "age_step": 1,
}

TRACKERS = {
    "assets": {
        "label": "资产",
        "adjustment_key": "ASSET",
        "initial": 0,
        "tiers": ASSET_TIERS,
        "unlock_age": 12,
        "locked_text": "（未解锁）",
    },
    "fame": {
        "label": "名气",
        "adjustment_key": "FAME",
        "initial": 0,
        "tiers": FAME_TIERS,
    },
    "knowledge": {
        "label": "知识",
        "adjustment_key": "KNOWLEDGE",
        "initial": 0,
        "tiers": KNOWLEDGE_TIERS,
        "unlock_age": 4,
        "locked_text": "（未解锁）",
    },
    "edu": {
        "label": "学历",
        "adjustment_key": "EDU",
        "initial": 0,
        "tiers": EDU_TIERS,
    },
}

EDU_AUTO_START_AGE = 1
EDU_AUTO_END_AGE = 18
EDU_DEDUCT_CAP = 10


def get_time_config(c):
    cfg = dict(TIME_CONFIG)
    override = c.get("time_config_override") or {}
    cfg.update(override)
    return cfg


def init_time_state(c):
    cfg = get_time_config(c)
    c[cfg["tick_key"]] = cfg["start_tick"]
    c[cfg["age_key"]] = cfg["start_age"]


def advance_time(c):
    cfg = get_time_config(c)
    c[cfg["tick_key"]] = c.get(cfg["tick_key"], cfg["start_tick"]) + cfg["tick_step"]
    c[cfg["age_key"]] = c.get(cfg["age_key"], cfg["start_age"]) + cfg["age_step"]


def get_character_age(c):
    cfg = get_time_config(c)
    return c.get(cfg["age_key"], cfg["start_age"])


def get_time_tick(c):
    cfg = get_time_config(c)
    return c.get(cfg["tick_key"], cfg["start_tick"])


def _fmt_num(x):
    try:
        if float(x).is_integer():
            return str(int(x))
        return f"{float(x):.2f}".rstrip("0").rstrip(".")
    except Exception:
        return str(x)


def format_time(c):
    cfg = get_time_config(c)
    tick = _fmt_num(get_time_tick(c))
    age = _fmt_num(get_character_age(c))
    return f"第 {tick} {cfg['tick_label']} · {age} {cfg['age_label']}"


def format_history_header(c):
    cfg = get_time_config(c)
    tick = _fmt_num(get_time_tick(c))
    age = _fmt_num(get_character_age(c))
    return f"第{tick}{cfg['tick_label']}（{age}{cfg['age_label']}）"


def init_trackers(c):
    for key, cfg in TRACKERS.items():
        c[key] = cfg.get("initial", 0)
    c["edu_disrupted"] = 0


def calculate_max_hp(final_attributes):
    return max(1, (final_attributes.get("SIZ", 50) + final_attributes.get("CON", 50)) // 10)


def apply_turn_start_effects(c):
    """
    Called once at the beginning of each timestamp.
    Returns a list of short log strings.
    """
    logs = []

    # HP natural recovery
    if c.get("hp", 0) < c.get("max_hp", 0):
        old = c["hp"]
        c["hp"] = min(c["max_hp"], c["hp"] + 1)
        if c["hp"] != old:
            logs.append(f"❤️HP +{c['hp'] - old}")

    # Compulsory education auto +1
    age = int(get_character_age(c))
    if c.get("has_compulsory_edu") and EDU_AUTO_START_AGE <= age <= EDU_AUTO_END_AGE:
        c["edu"] = c.get("edu", 0) + 1
        logs.append("学历 +1")

    return logs


def apply_tracker_adjustment(c, adjustment_key, value):
    """
    Applies non-HP tracker adjustment.
    Returns display log string or None.
    """
    value = int(value)

    for tracker_key, cfg in TRACKERS.items():
        if cfg.get("adjustment_key") != adjustment_key:
            continue

        # EDU special protection during compulsory education years
        if tracker_key == "edu":
            age = int(get_character_age(c))
            if value < 0 and c.get("has_compulsory_edu") and EDU_AUTO_START_AGE <= age <= EDU_AUTO_END_AGE:
                remaining_cap = EDU_DEDUCT_CAP - c.get("edu_disrupted", 0)
                actual = max(value, -remaining_cap)
                if actual == 0:
                    return None
                c[tracker_key] = c.get(tracker_key, 0) + actual
                c["edu_disrupted"] = c.get("edu_disrupted", 0) + (-actual)
                return f"{cfg['label']} {actual:+d}"

        c[tracker_key] = c.get(tracker_key, 0) + value
        return f"{cfg['label']} {value:+d}"

    return None
# ============================================================
# 共享鉴定系统（所有模式都用同一套）
# ============================================================

def perform_skill_check(c, attr_name, difficulty="normal", advantage_override=None):
    """1d100 vs 属性。"""
    attrs = c.get("final_attributes", {})
    attr_value = attrs.get(attr_name, 50)

    if advantage_override == "advantage":
        rule = "advantage"
    elif advantage_override == "disadvantage":
        rule = "disadvantage"
    elif difficulty == "easy":
        rule = "advantage"
    elif difficulty == "hard":
        rule = "disadvantage"
    else:
        rule = "normal"

    if rule == "advantage":
        rolls = [random.randint(1, 100), random.randint(1, 100)]
        kept = min(rolls)
    elif rule == "disadvantage":
        rolls = [random.randint(1, 100), random.randint(1, 100)]
        kept = max(rolls)
    else:
        rolls = [random.randint(1, 100)]
        kept = rolls[0]

    success = kept <= attr_value

    growth = 0
    if success:
        gain = roll_dice("1d6")
        if attr_value >= 90:
            gain = 0
        elif attr_value >= 70:
            gain = max(1, gain // 3)
        elif attr_value >= 50:
            gain = max(1, gain // 2)
        growth = gain

    return {
        "attribute": attr_name,
        "value": attr_value,
        "rolls": rolls,
        "kept": kept,
        "rule": rule,
        "success": success,
        "growth": growth,
    }


def apply_skill_check_growth(c, check_result, locked_attrs=None):
    if not check_result.get("success"):
        return None
    g = check_result.get("growth", 0)
    if g <= 0:
        return None
    attr = check_result["attribute"]
    if locked_attrs and attr in locked_attrs:
        return None
    attrs = c.setdefault("final_attributes", {})
    attrs[attr] = min(99, attrs.get(attr, 50) + g)
    return f"{attr} +{g}"


def resolve_multi_check(check_results):
    if not check_results:
        return "full_failure"
    s = sum(1 for r in check_results if r["success"])
    if s == len(check_results):
        return "full_success"
    if s == 0:
        return "full_failure"
    return "partial_success"


def format_check_log(check_result):
    rule_zh = {"advantage": "（优）", "disadvantage": "（劣）",
               "normal": ""}[check_result["rule"]]
    rolls_text = "+".join(str(x) for x in check_result["rolls"])
    mark = "✅" if check_result["success"] else "❌"
    return (f"🎲 {check_result['attribute']} 鉴定 {check_result['value']} "
            f"vs [{rolls_text}]{rule_zh} 取 {check_result['kept']} {mark}")


def build_action_check_prompt(c, action_text):
    """普通模式版本：用 STR/CON/POW/DEX/APP/SIZ/INT/CRE/LUCK。"""
    attrs_text = "、".join(ATTRIBUTES + ["LUCK"])
    return f"""玩家想在当前时间点主动做一件事。你只需要判断需要哪些属性鉴定。
玩家行动：{action_text}
可用属性：{attrs_text}

判定原则：
- 相对简单的小事 → 1 个属性，难度 easy。
- 一般行动 → 1 个属性，难度 normal。
- 涉及多种能力或非常困难的事 → 2 个属性，难度 normal 或 hard。
- 如果是纯偏好/无失败可能（比如"选择主修文学还是数学"）→ checks: []。
- "鉴定"本身已代表事情有难度，**只在真正棘手时用 hard**。

严格只返回如下 JSON：
{{
  "checks": ["STR"],
  "difficulty": "normal",
  "reasoning": "一句话理由"
}}
"""


def build_resolution_prompt(c, action_summary, check_results, **kwargs):
    """通用结果叙事 prompt。"""
    overall = resolve_multi_check(check_results)

    lines = []
    for r in check_results:
        rule_zh = {"advantage": "（双骰取优）",
                   "disadvantage": "（双骰取劣）",
                   "normal": ""}[r["rule"]]
        rolls_text = "+".join(str(x) for x in r["rolls"])
        mark = "✅成功" if r["success"] else "❌失败"
        lines.append(f"  - {r['attribute']} 鉴定（属性值 {r['value']}）{rule_zh}："
                     f"投出 [{rolls_text}]，采用 {r['kept']} → {mark}")
    check_text = "\n".join(lines)

    overall_zh = {
        "full_success": "完胜（所有鉴定都通过）",
        "partial_success": "险胜（有部分鉴定失败，必须付出代价才能办成）",
        "full_failure": "完败（鉴定都失败）",
    }[overall]

    extra_context = kwargs.get("extra_context", "")

    return f"""玩家这一次的行动是：{action_summary}

【鉴定结果】
{check_text}

【综合判定】{overall_zh}

请基于以上结果写一段叙事（200~400字）。要求：
- 叙事必须吻合判定结果。完胜不能写失败，完败不能写成功。
- 险胜：办成了，但要付明显代价（HP / ASSET / FAME / KNOWLEDGE 之一显著损失）。
- 完败：失利。可以扣 HP 或资源；如果是日常事件，扣得克制一些。
- 如果之后剧情还有续，可以 has_choice=true 给后续选项。
- 否则 has_choice=false。
{extra_context}
"""