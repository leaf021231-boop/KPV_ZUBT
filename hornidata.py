# hornidata.py —— 性压抑模式数据
# 接口和 data.py 完全一致：ATTRIBUTES / ATTR_DESC / ATTR_LONG_DESC /
#                          TALENT_POOL / build_system_prompt
# 其他东西（场景、稀有度、骰子、tier 等）直接从 data.py 复用。

from data import (
    SCENES, GENDERS,
    RARITY_CONFIG, RARITY_WEIGHTS,
    roll_dice, filter_pool, draw_talents,
    ASSET_TIERS, FAME_TIERS, EXPE_TIERS, KNOW_TIERS, # <--- 改这里
    get_tier, parse_ai_json,
    MODE_HORNY_MILD, MODE_HORNY_INTENSE,
    perform_skill_check, apply_skill_check_growth,
    resolve_multi_check, format_check_log,
    build_resolution_prompt,
)

# ============================================================
# 性压抑模式专用属性
# ============================================================
ATTRIBUTES =["STR", "LIB", "TEC", "APP", "END", "SEN", "LOV", "EXP", "CRE"]

ATTR_DESC = {
    "STR": "力量", "LIB": "性欲", "TEC": "体型", "APP": "外貌", "END": "体力",
    "SEN": "敏感", "LOV": "爱情", "EXP": "智力", "CRE": "家境",
}

ATTR_LONG_DESC = {
    "STR": "肌肉强度，不仅影响体力劳动和战斗力，有时也决定了绝对的强制力。",
    "LIB": "天生欲望强度和“硬件”，决定一年里能折腾几次。",
    "TEC": "身材和身高大小。",
    "APP": "外貌，决定能勾搭到什么级别的人。",
    "END": "身体素质，影响耐病、耐疲劳。",
    "SEN": "敏感度，影响体验质量也决定调情难度。",
    "LOV": "感情承载力，决定能不能维系长久关系，还是处处留情。",
    "EXP": "智力和经验，影响学习，思辨和阅历。",
    "CRE": "家境——是的，这玩意永远是核心变量。",
}

# 性压抑模式独立点数池
POINTS_POOL_DEFAULT = 200
POINTS_POOL_INTENSE = 200

# ============================================================
# 性压抑模式天赋池（你自己慢慢补；下面放几条样例）
# ============================================================
TALENT_POOL = [
# ========== Horni·citywalk 天赋 ==========
    #============= NEGATIVE (10) =============
    {"name": "早产儿", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "未足月落地，先天发育滞后。", "modifiers": [("END", "-1d2*5")],
     "narrative": "保温箱是你的第一个家。"},
    {"name": "城中弃子", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "被家庭遗忘在都市角落。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "福利院的老铁门是你记忆的起点。"},
    {"name": "过敏体质", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "对无数东西过敏，活得小心翼翼。", "modifiers": [("END", "-1d2*5")],
     "narrative": "别的小孩舔冰淇淋时，你只能闻奶香。"},
    {"name": "社恐倾向", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "天生的内向，面对生人浑身不自在。", "modifiers": [("LOV", "-1d2*5")],
     "narrative": "家里来客人，你永远是躲在门后的那个。"},
    {"name": "留守烙印", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "父母长期缺席，资源与关爱双缺。", "modifiers": [("LOV", "-1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "年三十的鞭炮声里，你握着老人机等了整夜。"},
    {"name": "家道中落", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "出生时家运已败，债台高筑。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "你喝的第一口奶粉都是赊来的。"},
    {"name": "灾厄孪生", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "带着晦气出生，见者皆嫌。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "街坊邻居悄悄议论，让你家换个地方住。"},
    {"name": "城市蝼蚁", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "出身于最底层的棚户区。", "modifiers": [("TEC", "-1d2*5")],
     "narrative": "你的童年背景是拆迁标语和垃圾堆积。"},
    {"name": "玻璃骨骼", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "先天骨质脆弱，极易骨折。", "modifiers": [("END", "-1d2*5")],
     "narrative": "别的小朋友玩滑梯，你只能在旁边看着。"},
    {"name": "福薄之光", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "貌美却耗损了身体元气。", "modifiers": [("APP", "+1d1*5"), ("END", "-1d3*5")],
     "narrative": "像个精美易碎的瓷娃娃，让人心疼。"},

    #============= COMMON (15) =============
    {"name": "中产之家", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "家境平稳，无冻饿之虞。", "modifiers": [],
     "narrative": "不奢华，也从未为吃穿发过愁。"},
    {"name": "小镇青年根", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "县城或小镇出生，视野有限但家境稳定。", "modifiers": [("CRE", "+1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "去趟省城都要兴奋三天，但家里从不断粮。"},
    {"name": "隔代亲", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "老人带大，宠溺有加，但略有娇纵。", "modifiers": [("APP", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "奶奶总觉得你穿少了，零花钱永远管够。"},
    {"name": "学区房儿", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "家旁边就是好学校，但背负期望。", "modifiers": [("EXP", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "走五分钟进校门，背后是爸妈满满的计划表。"},
    {"name": "新闻联播娃", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "父母是体制内基层，生活规律而保守。", "modifiers": [("CRE", "+1d1*5"), ("LIB", "-1d1*5")],
     "narrative": "每天7点全家准时坐在电视机前，你从不敢爬高。"},
    {"name": "电子原住民", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "从小接触屏幕，视力损耗但信息敏感。", "modifiers": [("EXP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "三岁就会划手机，但早早戴上了眼镜。"},
    {"name": "菜市场之家", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "父母摆摊做小生意，你打小嘴甜手快。", "modifiers": [("APP", "+1d2*5"), ("EXP", "-1d2*5")],
     "narrative": "在吆喝声里长大，算账找零比大人还麻利。"},
    {"name": "厂区子弟", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "国营厂区长大，体格不错但生活单调。", "modifiers": [("END", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "球场、澡堂、大食堂，你的地盘就这么大。"},
    {"name": "双语环境", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "家里说方言或外语，语言天赋早开，略有口音。", "modifiers": [("EXP", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "一张嘴别人就知你从哪来，但英语课永远第一。"},
    {"name": "拆迁幸运儿", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "幼时赶上拆迁，家境陡然而富但根基虚浮。", "modifiers": [("CRE", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "突然搬进电梯楼，可爸妈总念叨当年院子里的无花果。"},
    {"name": "单亲公寓", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "跟一位家长挤在小公寓，亲密但有经济压力。", "modifiers": [("LOV", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "饭桌上永远只有两副碗筷，但笑从不缺席。"},
    {"name": "健身成瘾之家", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "父母是健身狂魔，你的身体底子好，但学业被轻忽。", "modifiers": [("END", "+1d2*5"), ("EXP", "-1d2*5")],
     "narrative": "会走路就被带进健身房，蛋白质粉比奶粉先认识。"},
    {"name": "文化割裂", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "移民二代，双语思维但两边都不全然认同。", "modifiers": [("EXP", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "过春节想穿旗袍，出门又觉得太扎眼。"},
    {"name": "二次元世家", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "年轻的父母是资深二次元，审美拔群但社交圈怪。", "modifiers": [("APP", "+1d1*5"), ("TEC", "-1d1*5")],
     "narrative": "你的胎教是动画OP，满月抓周摆的是手办。"},
    {"name": "朋友圈育儿", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "父母按育儿博主的方式养你，时而科学，时而折腾。", "modifiers": [("END", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "辅食精确到克，早教卡按月龄换，你成了实验田。"},

    #============= RARE (8) =============
    {"name": "精英教育预备", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "高知家庭，早教资源顶尖。", "modifiers": [("EXP", "+1d2*5")],
     "narrative": "钢琴、编程、马术，你的周末比CEO还满。"},
    {"name": "名校血统", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "祖辈父母皆名校毕业，书香浸骨。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "家里的书架从地板顶到天花板，胎教是西哲史。"},
    {"name": "天生网红脸", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "在这个看脸的时代占尽先机。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "幼儿园毕业照就有人在网上打听这是谁家的孩子。"},
    {"name": "电竞圣体", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "反应速度和手脑协调性天赋异禀。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "四岁第一次握鼠标，光标轨迹就让大人看呆。"},
    {"name": "城市运动健将", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "身体素质拔尖，注定属于运动场。", "modifiers": [("END", "+1d1*5"), ("LIB", "+1d1*5")],
     "narrative": "在小区广场打闹都能看出惊人的爆发力。"},
    {"name": "富庶安稳", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "家境殷实，从不必为钱发愁。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "保姆车接送，兴趣课随便挑，你只负责快乐。"},
    {"name": "情感早熟", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "对人际情绪有超乎年龄的洞察力。", "modifiers": [("LOV", "+1d2*5")],
     "narrative": "幼儿园老师吵架，你能精准说出谁先委屈了谁。"},
    {"name": "模特胚子", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "高挑的骨架和独特的五官，天生衣架。", "modifiers": [("TEC", "+1d2*5")],
     "narrative": "抱着你在公园走，总有人问要不要拍童装广告。"},

    #============= LEGENDARY (4) =============
    {"name": "豪门继承人", "rarity": "legendary", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "生在财富顶端，且继承了优良基因。", "modifiers": [("CRE", "+1d3*5"), ("APP", "+1d2*5"), ("EXP", "+1d2*5")],
     "narrative": "你的满月酒登上了本地新闻，礼物用卡车装。"},
    {"name": "天生领跑者", "rarity": "legendary", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "健康、活力、聪慧，像被都市选中的代表。", "modifiers": [("END", "+1d3*5"), ("LIB", "+1d2*5"), ("SEN", "+1d2*5")],
     "narrative": "幼儿园运动会，你一个人拿了三分之一的金星。"},
    {"name": "智颜双绝", "rarity": "legendary", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "智商超群，面容无瑕，完美得不像话。", "modifiers": [("EXP", "+1d3*5"), ("APP", "+1d3*5"), ("CRE", "+1d2*5")],
     "narrative": "刚出生，护士就在猜测这孩子将来要上几回热搜。"},
    {"name": "时代烙印", "rarity": "legendary", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "你的降生恰逢世纪之交的祥瑞时刻。", "modifiers": [("LOV", "+1d3*5"), ("CRE", "+1d3*5"), ("EXP", "+1d2*5")],
     "narrative": "千禧年的钟声为你而鸣，全家都觉着这孩子非同小可。"},

    #============= WILDCARD (3) =============
    {"name": "重生者", "rarity": "wildcard", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "带着隐约的前世记忆，早熟得骇人，却与周围格格不入。", "modifiers": [("EXP", "+1d3*5"), ("LOV", "-1d3*5")],
     "narrative": "你总盯着某个橱窗发呆，嘴里嘟囔着“以前不是这样”。"},
    {"name": "预知梦", "rarity": "wildcard", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "梦境时常与现实交叠，魂不守舍。", "modifiers": [("SEN", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "好几次你说中还没发生的事，然后大病一场。"},
    {"name": "异界之触", "rarity": "wildcard", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "感官能捕捉城市缝隙里的灵异，代价是精神的孤寂。", "modifiers": [("SEN", "+1d3*5"), ("TEC", "-1d3*5")],
     "narrative": "地铁广告牌上的人脸，你说它们在动。"},
# ========== Horni·any 天赋 ==========
    #============= NEGATIVE (10) =============
    {"name": "胎带弱症", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "先天不足，器官功能偏弱。", "modifiers": [("END", "-1d2*5")],
     "narrative": "从第一声啼哭起，就比别的婴儿费心费力。"},
    {"name": "其貌不扬", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "面容组合颇为遗憾。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "在人群中你习惯低头，很少被人第一眼看见。"},
    {"name": "体弱多病", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "童年常驻医院。", "modifiers": [("END", "-1d2*5")],
     "narrative": "消毒水的气味是你的童年基调。"},
    {"name": "愚钝根骨", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "接受新事物总是慢半拍。", "modifiers": [("EXP", "-1d2*5")],
     "narrative": "同样的东西，你要比别人多花一倍时间理解。"},
    {"name": "情感淡漠", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "天生共情能力薄弱，难以与人建立深层联结。", "modifiers": [("LOV", "-1d2*5")],
     "narrative": "亲人离世，你比所有人都先停下哭泣。"},
    {"name": "感官迟钝", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "神经反应天生迟缓，对触觉冷热都模糊。", "modifiers": [("SEN", "-1d2*5")],
     "narrative": "被烫到了往往要过一会儿才喊出声。"},
    {"name": "矮小瘦削", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "骨架纤小，怎么吃都不长肉。", "modifiers": [("TEC", "-1d2*5")],
     "narrative": "人群里你总被挡住视线，外套永远买最小码。"},
    {"name": "气若游丝", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "先天肺活量不足，体力极差。", "modifiers": [("END", "-1d2*5")],
     "narrative": "跑两步就喘，重物与你无缘。"},
    {"name": "家徒四壁", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "出生在最贫瘠的屋檐下。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "你的摇篮是补丁摞补丁的旧衣裳。"},
    {"name": "先天乏力", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "激素水平偏低，活力缺缺。", "modifiers": [("LIB", "-1d2*5")],
     "narrative": "别的小孩满地跑闹，你能在沙发上发呆一下午。"},

    #============= COMMON (15) =============
    {"name": "寻常人家", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "既不富裕也不拮据，温饱有余。", "modifiers": [],
     "narrative": "你的童年没有太多意外，平平淡淡长大。"},
    {"name": "五官端正", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "相貌说不上惊艳，但干净耐看。", "modifiers": [],
     "narrative": "镜子里的脸，不会让任何人皱眉。"},
    {"name": "平和心境", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "天生的情绪稳定器。", "modifiers": [("LOV", "+1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "火烧眉毛也不急，对人心冷暖却异常敏感。"},
    {"name": "脚力过人", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "腿部肌肉发达，但上身力量平平。", "modifiers": [("END", "+1d1*5"), ("SEN", "-1d1*5")],
     "narrative": "从小就能跑擅跳，但被人拍肩半天才回头。"},
    {"name": "鹰隼目力", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "视力绝佳，但听觉稍钝。", "modifiers": [("EXP", "+1d1*5"), ("SEN", "-1d1*5")],
     "narrative": "远处的细节你一眼看清，却常听漏耳边的低语。"},
    {"name": "大骨架", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "天生块头大，行动略笨重。", "modifiers": [("TEC", "+1d2*5"), ("SEN", "-1d2*5")],
     "narrative": "站在那就占地方，穿门时总要侧身。"},
    {"name": "皮实耐造", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "免疫力不错，但小伤小痛不断。", "modifiers": [("END", "+1d2*5"), ("TEC", "-1d1*5")],
     "narrative": "淋雨不感冒，但膝盖总是旧的痂没掉又添新的。"},
    {"name": "早慧早衰", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "幼时聪明过人，体质却提前消耗。", "modifiers": [("EXP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "三岁识字、五岁吟诗，可药罐子几乎没离过手。"},
    {"name": "流浪者之子", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "家族行踪不定，见多识广但根基浅薄。", "modifiers": [("EXP", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "你在马背上学会说话，却从不与谁交心。"},
    {"name": "匠人血脉", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "家里世代靠手艺吃饭，你天生手巧但眼界受限。", "modifiers": [("SEN", "+1d2*5"), ("EXP", "-1d2*5")],
     "narrative": "七岁就能做木工小件，但书本字句像在跳舞。"},
    {"name": "天生笑面", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "亲和力拉满，却少了点威严。", "modifiers": [("APP", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "谁见了这张脸都软了三分，可凶也凶不起来。"},
    {"name": "耐饿体质", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "肠胃功能特别，但长得缓慢。", "modifiers": [("END", "+1d1*5"), ("TEC", "-1d1*5")],
     "narrative": "一天一顿也能活蹦乱跳，就是个子迟迟不窜。"},
    {"name": "单亲扶持", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "只有一方长辈抚养，关爱加倍但资源减半。", "modifiers": [("LOV", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "母亲/父亲一人撑起你的天，你早早学会了心疼人。"},
    {"name": "幼年变故", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "一次大病或意外，重塑了你的神经。", "modifiers": [("LOV", "+1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "那场高烧之后，你看人的眼神比同龄孩子都柔和。"},
    {"name": "中庸之资", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "各方面均衡，毫无短板也无突出。", "modifiers": [],
     "narrative": "放在人堆里最让人放心的那种孩子。"},

    #============= RARE (8) =============
    {"name": "天生丽质", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "容貌出众，令人一见难忘。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "从满月开始，抱你的人就络绎不绝。"},
    {"name": "铁打之躯", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "先天抵抗力极强，几乎不生病。", "modifiers": [("END", "+1d2*5")],
     "narrative": "别的小孩发烧哭闹时，你正在泥地里打滚。"},
    {"name": "过目不忘", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "记忆力堪称奇迹。", "modifiers": [("EXP", "+1d2*5")],
     "narrative": "三岁时听过的故事，隔年还能一字不差复述。"},
    {"name": "情深似海", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "天生的共情能力，能轻易体察他人情绪。", "modifiers": [("LOV", "+1d2*5")],
     "narrative": "母亲心情低落时，你总是第一个爬到她膝边。"},
    {"name": "灵敏感知", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "五感天生敏锐，神经反射超群。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "蚊子在屋角嗡嗡，你能精准指出方位。"},
    {"name": "名门之后", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "家族声望提供了天然的起跑线。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "你的名字就是一块敲门砖。"},
    {"name": "活力充沛", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "天生精力旺盛，仿佛有用不完的劲。", "modifiers": [("LIB", "+1d2*5")],
     "narrative": "全家午睡时，只有你还在客厅里咯咯笑着乱爬。"},
    {"name": "魁梧体格", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "身形高大强壮，注定不凡。", "modifiers": [("TEC", "+1d2*5")],
     "narrative": "在同龄人里永远高出一头，像个小巨人。"},

    #============= LEGENDARY (4) =============
    {"name": "天选之子", "rarity": "legendary", "mode": "Horni", "scenarios": ["any"],
     "desc": "命运的宠儿，几项能力同时绽放。", "modifiers": [("LOV", "+1d3*5"), ("EXP", "+1d2*5"), ("APP", "+1d2*5")],
     "narrative": "你天生就比别人多几分运气与从容。"},
    {"name": "麒麟儿", "rarity": "legendary", "mode": "Horni", "scenarios": ["any"],
     "desc": "智勇双全，体格与头脑兼得。", "modifiers": [("END", "+1d3*5"), ("EXP", "+1d2*5"), ("LIB", "+1d2*5")],
     "narrative": "自古逢人说麟儿，你便是那传说。"},
    {"name": "星辰之眷", "rarity": "legendary", "mode": "Horni", "scenarios": ["any"],
     "desc": "美貌、敏锐与温柔集于一身。", "modifiers": [("APP", "+1d3*5"), ("SEN", "+1d2*5"), ("LOV", "+1d2*5")],
     "narrative": "仿佛星辉洒落的婴孩，引动四方惊异。"},
    {"name": "太古遗血", "rarity": "legendary", "mode": "Horni", "scenarios": ["any"],
     "desc": "远古祖先的血脉在你身上觉醒。", "modifiers": [("LIB", "+1d3*5"), ("TEC", "+1d3*5"), ("END", "+1d2*5")],
     "narrative": "你的啼声洪亮到不像初生儿，护士手一抖。"},

    #============= WILDCARD (3) =============
    {"name": "双魂共生", "rarity": "wildcard", "mode": "Horni", "scenarios": ["any"],
     "desc": "身体里藏着另一个意识，感知力异变。", "modifiers": [("SEN", "+1d3*5"), ("LOV", "-1d3*5")],
     "narrative": "有时你对着虚空说话，表情判若两人，亲近的人也认不出你。"},
    {"name": "气运吞噬", "rarity": "wildcard", "mode": "Horni", "scenarios": ["any"],
     "desc": "能汲取周遭气运，但自身家运凋零。", "modifiers": [("EXP", "+1d3*5"), ("APP", "+1d2*5"), ("CRE", "-1d3*5")],
     "narrative": "你出生那年，祖宅的槐树突然枯了一半。"},
    {"name": "时间沙漏", "rarity": "wildcard", "mode": "Horni", "scenarios": ["any"],
     "desc": "感知时间的流逝异于常人，代价是体型停滞。", "modifiers": [("SEN", "+1d3*5"), ("TEC", "-1d3*5")],
     "narrative": "七岁了，看身形还像四岁，但躲闪的动作快得离奇。"},

     # ========== Horni 专属·citywalk 天赋（15） ==========
    #============= NEGATIVE (3) =============
    {"name": "宗教家庭", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "父母信仰极度保守，从小灌输禁欲观念。", "modifiers": [("LIB", "-1d2*5")],
     "narrative": "电视上一出亲热镜头，遥控器立刻被夺走，全家人面无表情。"},
    {"name": "童年阴影", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "幼年目睹了某些不该看的画面，从此心存芥蒂。", "modifiers": [("LOV", "-1d2*5")],
     "narrative": "那扇门没关严实的夜晚，至今仍偶尔出现在你的梦里。"},
    {"name": "发育迟缓", "rarity": "negative", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "青春期来得比同龄人晚得多，常被取笑。", "modifiers": [("LIB", "-1d1*5"), ("TEC", "-1d1*5")],
     "narrative": "更衣室里你永远是最后一个长开的那位，缩在角落换衣服。"},

    #============= COMMON (5) =============
    {"name": "耳濡目染", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "家里有亲戚从事风俗或夜场行业，你比同龄人早熟得多。", "modifiers": [("EXP", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "小姨化妆时你蹲在旁边看，五岁就听懂了她讲电话时的潜台词。"},
    {"name": "网络早教", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "童年误入了不该看的网站，知识面广而杂。", "modifiers": [("EXP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "小学课间你比男生还会讲段子，但晚上常常做奇怪的梦。"},
    {"name": "豆蔻早熟", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "比同龄人提前进入发育期，外形抢眼但心智跟不上。", "modifiers": [("APP", "+1d2*5"), ("EXP", "-1d2*5")],
     "narrative": "小学六年级你已经被错认成中学姐，可数学题还停留在三年级水平。"},
    {"name": "夜店区长大", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "家在城市灯红酒绿地带，对成年世界见怪不怪。", "modifiers": [("LIB", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "凌晨两点的霓虹灯是你的童年夜灯，邻居姐姐们的高跟鞋声哄你入睡。"},
    {"name": "纯情体质", "rarity": "common", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "脸红心跳第一名。", "modifiers": [("LOV", "+1d3*5"), ("EXP", "-1d2*5")],
     "narrative": "光是被牵手都能心跳过速三分钟。"},

    #============= RARE (4) =============
    {"name": "明星基因", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "父母中有人从事娱乐行业，颜值与气场拔群。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "幼儿园来选广告童星的星探，第一眼就锁定了你。"},
    {"name": "舞蹈世家", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "母亲是舞者或瑜伽教练，柔韧度从小被开发到位。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "三岁能劈一字马，幼儿园老师惊叹这孩子骨头是橡皮做的吗。"},
    {"name": "都市精致基因", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "父母都极度注重自我管理，遗传给你的体型令人艳羡。", "modifiers": [("TEC", "+1d2*5")],
     "narrative": "全家福里没有一个普通身材，邻居都叫你们家“衣架家族”。"},
    {"name": "欲望旺盛", "rarity": "rare", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "城市快节奏激发出旺盛的活力与冲劲。", "modifiers": [("LIB", "+1d2*5")],
     "narrative": "幼儿园同伴还在午睡，你已经爬上滑梯把自己滑得满头大汗。"},

    #============= LEGENDARY (2) =============
    {"name": "都市维纳斯", "rarity": "legendary", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "钢筋森林中诞生的奇迹，颜值、身材、敏感俱佳。", "modifiers": [("APP", "+1d3*5"), ("TEC", "+1d2*5"), ("SEN", "+1d2*5")],
     "narrative": "你的满月照被摄影师拿去当样片，工作室生意火了三年。"},
    {"name": "名媛/公子血脉", "rarity": "legendary", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "出身上流社交圈，从小被教导礼仪、品味与魅力。", "modifiers": [("CRE", "+1d3*5"), ("APP", "+1d2*5"), ("LOV", "+1d2*5")],
     "narrative": "三岁的生日宴上，你已经能用三国语言向客人道谢。"},

    #============= WILDCARD (1) =============
    {"name": "风月遗孤", "rarity": "wildcard", "mode": "Horni", "scenarios": ["citywalk"],
     "desc": "母亲是某位红极一时的交际花，你继承了她惊人的魅力却也背负流言。", "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d2*5"), ("CRE", "-1d3*5")],
     "narrative": "户口本上父亲那栏空着，可镜子里的脸总能让人愣三秒，街坊背后议论你的身世。"},

     # ========== Horni 专属·any 天赋（15） ==========
    #============= NEGATIVE (3) =============
    {"name": "天生冷感", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "神经末梢天生迟钝，对触觉刺激反应微弱。", "modifiers": [("SEN", "-1d2*5")],
     "narrative": "小时候挠痒痒别人笑得打滚，你只是疑惑地看着对方。"},
    {"name": "情窦未开", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "激素分泌天生偏弱，对人无端起的悸动几乎不曾有过。", "modifiers": [("LIB", "-1d2*5")],
     "narrative": "同龄人开始偷偷传纸条时，你只觉得他们大惊小怪。"},
    {"name": "迟钝之心", "rarity": "negative", "mode": "Horni", "scenarios": ["any"],
     "desc": "对他人的好感与暧昧后知后觉，常错失感情。", "modifiers": [("LOV", "-1d1*5"), ("SEN", "-1d1*5")],
     "narrative": "多年以后才反应过来，原来当年那个总分糖给你的同桌是喜欢你。"},

    #============= COMMON (5) =============
    {"name": "潜力惊人", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "身材或“硬件”比例远超寻常，但伴随发育期的烦恼。", "modifiers": [("LIB", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "校医检查时挑了挑眉，从此体育课你总是第一个被点名做示范。"},
    {"name": "易动情体质", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "对感情投入很快很深，但敏锐度有所欠缺。", "modifiers": [("LOV", "+1d2*5"), ("SEN", "-1d2*5")],
     "narrative": "幼儿园的“小新娘”仪式你都记到现在，至今认真。"},
    {"name": "钝感少年", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "天性憨直，懂得多但不开窍。", "modifiers": [("EXP", "+1d1*5"), ("LIB", "-1d1*5")],
     "narrative": "同伴讲的荤段子你笑得最大声，可压根没听懂笑点。"},
    {"name": "外热内冷", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "外貌有侵略性，内心却淡如止水。", "modifiers": [("APP", "+1d2*5"), ("LIB", "-1d2*5")],
     "narrative": "走在街上回头率惊人，你自己却毫无察觉，心如古井。"},
    {"name": "敏感纤弱", "rarity": "common", "mode": "Horni", "scenarios": ["any"],
     "desc": "感官天生纤细，但骨架瘦小。", "modifiers": [("SEN", "+1d2*5"), ("TEC", "-1d2*5")],
     "narrative": "一片落叶蹭到脖子都能让你打颤，体重永远是班里倒数。"},

    #============= RARE (4) =============
    {"name": "天赋异禀", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "天生硬件条件出众，发育期来得早且彻底。", "modifiers": [("LIB", "+1d2*5")],
     "narrative": "亲戚见面总要意味深长地拍拍你的肩，说“这孩子像样”。"},
    {"name": "玲珑感官", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "全身神经如蛛网般敏锐。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "盲人摸象都没你摸得准，闭眼能数出风从哪几个方向吹来。"},
    {"name": "深情种子", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "天生重情重义，一旦认定便难撼动。", "modifiers": [("LOV", "+1d2*5")],
     "narrative": "幼时养的小狗死了，你为它守了三天坟。"},
    {"name": "妩媚胚子", "rarity": "rare", "mode": "Horni", "scenarios": ["any"],
     "desc": "眉眼之间天生带着勾人的弧度，无需修饰。", "modifiers": [("APP", "+1d1*5"), ("SEN", "+1d1*5")],
     "narrative": "一个不经意的回眸，能让街角的大爷愣住三秒。"},

    #============= LEGENDARY (2) =============
    {"name": "天生尤物", "rarity": "legendary", "mode": "Horni", "scenarios": ["any"],
     "desc": "颜值、身材、敏感度三位一体，仿佛被造物主特别眷顾。", "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d2*5"), ("SEN", "+1d2*5")],
     "narrative": "亲戚抱起你时面面相觑，谁都没见过这样精致的小婴儿。"},
    {"name": "情圣血脉", "rarity": "legendary", "mode": "Horni", "scenarios": ["any"],
     "desc": "你的祖上盛传是某位风流人物，基因里就带着惑人的气质与深情。", "modifiers": [("LOV", "+1d3*5"), ("APP", "+1d2*5"), ("EXP", "+1d2*5")],
     "narrative": "外婆翻出泛黄的家谱，意味深长地说：“这家的孩子，向来动情。”"},

    #============= WILDCARD (1) =============
    {"name": "魅魔之吻", "rarity": "wildcard", "mode": "Horni", "scenarios": ["any"],
     "desc": "天生散发难以言喻的吸引力，但身体承受着对应的代价。", "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d2*5"), ("END", "-1d3*5")],
     "narrative": "婴儿时期就让陌生人忍不住停下脚步多看几眼，可你三天两头发烧不退。"},


     # ========== Horni·flyaway 日常天赋（40） ==========
    #============= NEGATIVE (10) =============
    {"name": "凡骨之资", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "经脉堵塞，灵气难通。", "modifiers": [("EXP", "-1d2*5")],
     "narrative": "测灵石在你手里如死石一块，人群中传来压抑的笑声。"},
    {"name": "天弃之相", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "五官怪异，被视为不祥。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "接生婆只看一眼就惊得把你扔到地上。"},
    {"name": "先天体弱", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "元气亏空，风一吹就倒。", "modifiers": [("END", "-1d2*5")],
     "narrative": "别家娃子摸爬滚打时，你只能裹在棉被里喝药。"},
    {"name": "孽缘缠身", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "易招惹邪祟，道心不坚。", "modifiers": [("LOV", "-1d2*5")],
     "narrative": "你睡觉时总睁着半只眼，仿佛在和什么东西对视。"},
    {"name": "破落宗门之后", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "家族衰败，资源全无。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "祖上阔过的证据，就是柴房里那把生锈的断剑。"},
    {"name": "痴愚之资", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "悟性极差，学什么都慢如老牛。", "modifiers": [("EXP", "-1d2*5")],
     "narrative": "一篇口诀，别的师兄念三遍，你磕磕绊绊三百遍。"},
    {"name": "气运淡薄", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "运气差，出身也微寒。", "modifiers": [("LOV", "-1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "抓周时你握了块石头，父亲的脸立刻黑了。"},
    {"name": "神识蒙昧", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "神识天生迟钝，对天地灵气几无感应。", "modifiers": [("SEN", "-1d2*5")],
     "narrative": "灵兽路过身后你都察觉不到，被师兄笑作睁眼瞎。"},
    {"name": "血咒之体", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "家族被诅咒，体魄会逐渐消逝。", "modifiers": [("END", "-1d2*5")],
     "narrative": "你出生时，爷爷在你手臂上发现一圈诡异的黑纹。"},
    {"name": "厄运之子", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "生来瘦小，难以长大。", "modifiers": [("TEC", "-1d2*5")],
     "narrative": "六岁了还像个三岁娃娃，村里都叫你小土豆。"},

    #============= COMMON (15) =============
    {"name": "平凡农家", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "日出而作，日入而息。", "modifiers": [],
     "narrative": "你的童年带着稻香和牛粪味儿，梦里才见过仙人。"},
    {"name": "商贾之后", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "家里开杂货铺，有些积蓄但欠缺气魄。", "modifiers": [("CRE", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "算盘你打得比谁都响，可一见血就腿软。"},
    {"name": "猎户之勇", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "从小随父打猎，体格好，识字不多。", "modifiers": [("END", "+1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "你能徒手放倒一头野猪，但书本上的字像蚊蝇。"},
    {"name": "书香门第", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "祖上出过举人，家中藏书不少。", "modifiers": [("EXP", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "三岁吟诗，五岁作对，可惜手无缚鸡之力。"},
    {"name": "微末灵根", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "有一丝木灵根，但身体受不住灵力滋养。", "modifiers": [("EXP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "你会让种子发芽得比别家快，代价是每月必发一次高烧。"},
    {"name": "半妖遗孤", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "体内流着一丝狐妖的血，容貌魅惑但身形娇小。", "modifiers": [("APP", "+1d2*5"), ("TEC", "-1d2*5")],
     "narrative": "镇上的人一边骂你狐媚子，一边偷偷多看你几眼。"},
    {"name": "剑修遗腹子", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "父亲是散修剑客，留给你的只有一本剑谱和贫穷。", "modifiers": [("SEN", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "你拿树枝当剑，在泥地上把一招'白虹贯日'练了几万遍。"},
    {"name": "丹药童子", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "父母为丹师试药，拿你当药罐子，百毒不侵却脑子不太灵光。", "modifiers": [("END", "+1d2*5"), ("EXP", "-1d2*5")],
     "narrative": "你吃过的毒丹比饭还多，浑身是宝但反应总慢半拍。"},
    {"name": "阵道启蒙", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "天生对符纹敏感，但手脚笨拙。", "modifiers": [("EXP", "+1d1*5"), ("SEN", "-1d1*5")],
     "narrative": "你能一眼看出阵眼，可画符时总歪歪扭扭。"},
    {"name": "佛寺俗家", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "父母是寺庙信徒，自小吃斋念佛，心志坚定，身形清瘦。", "modifiers": [("LOV", "+1d2*5"), ("TEC", "-1d2*5")],
     "narrative": "别的孩子抢糖时，你已在盘坐入定，一盏青灯为伴。"},
    {"name": "灵脉矿工之子", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "家旁有废弃灵矿，灵气淬炼了精神，矿尘损害了肺腑。", "modifiers": [("LOV", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "你呼吸时肺里有风声，可赌石从没输过。"},
    {"name": "绝世琴师血脉", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "母亲是乐坊花魁，继承了好相貌和柔弱的身体。", "modifiers": [("APP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "手指细长，天生是弹奏的料，可惜扛不动任何重物。"},
    {"name": "炼器学徒", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "在炼器铺长大，手巧但家贫。", "modifiers": [("SEN", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "七岁就会修灵锄，补锅手艺一流，可买不起一把属于自己的飞剑。"},
    {"name": "父母一凡一修", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "父亲是外门弟子，母亲是村妇，留了点微薄家底却少了磨练。", "modifiers": [("CRE", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "你有几颗灵石零花钱，可一遇事儿就哭着找娘。"},
    {"name": "被弃养后收养", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "襁褓中被丢在路边，被好心人捡回，性子坚毅但相貌遭过损。", "modifiers": [("LOV", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "左脸有道小小的疤，据说是被野狗舔的，但你笑起来比谁都暖。"},

    #============= RARE (8) =============
    {"name": "天灵根", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "单一属性灵根极为纯粹。", "modifiers": [("EXP", "+1d2*5")],
     "narrative": "入门测试时，水晶球亮成一颗小太阳。"},
    {"name": "天生剑骨", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "骨骼清奇，如同为剑而生。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "第一次握剑，剑身便发出清越鸣响。"},
    {"name": "道体仙姿", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "仙风道骨，气质出尘。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "长辈说，你像是从古画里走出来的仙童。"},
    {"name": "凤凰血脉", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "稀薄的凤凰血脉，恢复力极强。", "modifiers": [("END", "+1d2*5")],
     "narrative": "高烧四十度，一觉睡醒又活蹦乱跳，令赤脚医生瞠目。"},
    {"name": "仙门嫡系", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "出生在某个中等仙门之内，资源不愁。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "你的摇篮是个低阶法器，铃铛都是下品灵石镶的。"},
    {"name": "通明道心", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "心志澄澈，不易被外物动摇。", "modifiers": [("LOV", "+1d2*5")],
     "narrative": "不论外界多嘈杂，你的剑意总是纹丝不动。"},
    {"name": "龙血传承", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "遥远的真龙血脉，让生机远超同龄人。", "modifiers": [("LIB", "+1d2*5")],
     "narrative": "三岁举石锁，吓得族长连喊祖宗。"},
    {"name": "慧根深种", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "悟性惊人，举一反三。", "modifiers": [("EXP", "+1d2*5")],
     "narrative": "长老讲道，其余弟子尚在困惑，你已颔首微笑。"},

    #============= LEGENDARY (4) =============
    {"name": "真仙转世", "rarity": "legendary", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "传说中的仙人重新投胎。", "modifiers": [("LOV", "+1d3*5"), ("EXP", "+1d2*5"), ("APP", "+1d2*5")],
     "narrative": "出生那夜，紫气东来三千里，一只仙鹤落在你家屋檐。"},
    {"name": "圣体道胎", "rarity": "legendary", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "天生的修道圣体，万法不侵。", "modifiers": [("END", "+1d3*5"), ("LIB", "+1d2*5"), ("EXP", "+1d2*5")],
     "narrative": "皮肤光洁如玉，蚊虫不叮，寒暑不侵。"},
    {"name": "九脉天资", "rarity": "legendary", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "身轻如燕，家学渊源。", "modifiers": [("SEN", "+1d3*5"), ("EXP", "+1d2*5"), ("CRE", "+1d2*5")],
     "narrative": "八大世家的拜帖在你满月当天就送到了。"},
    {"name": "混沌灵根", "rarity": "legendary", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "亿万年不遇的混沌灵根，包容万象。", "modifiers": [("EXP", "+1d3*5"), ("LOV", "+1d3*5"), ("END", "+1d2*5")],
     "narrative": "任何法术你只看一遍，灵气在你体内如臂使指。"},

    #============= WILDCARD (3) =============
    {"name": "魔种寄生", "rarity": "wildcard", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "丹田内有一颗魔种，赋予强大精神力量，但时刻吞噬生机。", "modifiers": [("LOV", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "你常在梦里与那个魔影对话，醒来时吐的黑血能把床单蚀出洞。"},
    {"name": "逆天改命", "rarity": "wildcard", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "天资绝世，但出生在乞丐窝。", "modifiers": [("EXP", "+1d3*5"), ("CRE", "-1d3*5")],
     "narrative": "靠听墙角学会认字，三岁出口成章，可身上只有破麻袋御寒。"},
    {"name": "妖皇血醒", "rarity": "wildcard", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "上古妖皇血脉觉醒，生机充沛，相貌却兽化。", "modifiers": [("LIB", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "头上长着两只小角，臂有鳞片，同龄人怕你，野兽却亲近你。"},

    #============= NEGATIVE (3) =============
    {"name": "断情绝爱", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "天生命格主孤，七情六欲都比常人淡薄三分。", "modifiers": [("LOV", "-1d2*5")],
     "narrative": "算命瞎子摸过你的额头，叹气说这孩子注定与红尘缘浅。"},
    {"name": "童子之命", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "命格清正过头，欲望天生淡漠。", "modifiers": [("LIB", "-1d2*5")],
     "narrative": "庙里的老和尚见你便道：此子有童子相，怕是难落红尘。"},
    {"name": "煞气缠体", "rarity": "negative", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "出生时煞气过重，体魄羸弱且令人心生畏惧。", "modifiers": [("LIB", "-1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你哭一声，邻居家的鸡狗就跟着哀鸣，村人远远见你便绕道。"},

    #============= COMMON (5) =============
    {"name": "采补世家", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "家族世代修炼采补功法，体质特殊但根基浮躁。", "modifiers": [("LIB", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "母亲怀你时整宿翻书，姑姑们看你的眼神意味深长。"},
    {"name": "情蛊之子", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "母亲是苗疆蛊师，从小给你养了一只情蛊作伴。", "modifiers": [("SEN", "+1d2*5"), ("EXP", "-1d2*5")],
     "narrative": "你能感知到方圆百步内每一颗动情的心，可寻常学问总是看不进去。"},
    {"name": "乐坊出身", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "母亲是乐坊红牌，自幼习得歌舞媚术，姿色出众。", "modifiers": [("APP", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "你三岁就会捏着兰花指唱小调，逗得满堂喝彩，可谁都知道你母亲的身份。"},
    {"name": "媚骨天成", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "天生骨相妖娆，举手投足间自带勾人韵味。", "modifiers": [("APP", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "走路时腰肢自然摆动，让村妇们看着就心生戒备。"},
    {"name": "双修之缘", "rarity": "common", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "命格中带有双修之兆，与人共修事半功倍但情根易动。", "modifiers": [("LIB", "+1d2*5"), ("EXP", "-1d2*5")],
     "narrative": "测命时长老沉吟良久：此子日后修道，怕是离不开有缘人。"},

    #============= RARE (4) =============
    {"name": "纯阳/纯阴之体", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "极致单极的天生体质，是双修者求而不得的至宝。", "modifiers": [("LIB", "+1d2*5")],
     "narrative": "母亲怀你时反季开花，老仙长断言此子体质百年难遇。"},
    {"name": "九窍玲珑", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "神识与体感天生开窍，对外界一切都极其敏锐。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "蚊虫落上手背你能察觉到它正在搓腿，师兄妹都觉得你像只猫。"},
    {"name": "倾城仙姿", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "与生俱来的勾魂之美，行走时连花草都倾向你。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "孩童时代街上卖花的老妪非要把整篮花送你，说这是花儿自己想跟你走。"},
    {"name": "情根深种", "rarity": "rare", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "前世今生情缘绵长，对感情格外执着。", "modifiers": [("LOV", "+1d2*5")],
     "narrative": "幼时一只小兔死了，你为它修了座小坟，每年清明都去添土。"},

    #============= LEGENDARY (2) =============
    {"name": "玉女转世", "rarity": "legendary", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "瑶池玉女或天庭仙官转世，姿色与灵慧并存。", "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d2*5"), ("SEN", "+1d2*5")],
     "narrative": "你出生时屋外百花同时开放，老仙人感叹道：这是天上人下凡了。"},
    {"name": "情缘宿命", "rarity": "legendary", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "三生石上有名，命中注定情缘缠绕，同时承载道心与情根。", "modifiers": [("LOV", "+1d3*5"), ("APP", "+1d2*5"), ("EXP", "+1d2*5")],
     "narrative": "测命师傅推算你的姻缘签时手都抖了，断言此命格三生三世皆有相伴。"},

    #============= WILDCARD (1) =============
    {"name": "魔门遗珠", "rarity": "wildcard", "mode": "Horni", "scenarios": ["flyaway"],
     "desc": "继承魔门血脉的妖异之美，魅惑非凡，却背负着正道追杀的命运。", "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d2*5"), ("CRE", "-1d3*5")],
     "narrative": "你的瞳孔在月圆夜会泛出微微紫光，养父养母从不让你出村，远远便听见追兵的马蹄声。"},
     # ========== Horni·dragonfire 天赋（40 正常） ==========
    #============= NEGATIVE (10) =============
    {"name": "农奴之子", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "世代为奴，没有自由。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "你人生的第一件玩具，是领主儿子丢掉的马鞭。"},
    {"name": "黑暗诅咒", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "被黑巫师施了咒，体质极虚。", "modifiers": [("END", "-1d2*5")],
     "narrative": "你的影子比别人的淡，老人们看见都绕道走。"},
    {"name": "狰狞面容", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "长的像是兽人混血失败品。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "母亲第一次喂奶时，差点尖叫出来。"},
    {"name": "战乱遗孤", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "在炮火中出生，极度缺乏安全感。", "modifiers": [("LOV", "-1d2*5")],
     "narrative": "一听到马蹄声，你就条件反射地躲进床底。"},
    {"name": "痴呆儿", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "脑子天生不灵光。", "modifiers": [("EXP", "-1d2*5")],
     "narrative": "五岁才会说一句完整的话，村童们叫你傻大个。"},
    {"name": "跛子", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "右腿天生短一截，行动不便。", "modifiers": [("SEN", "-1d2*5")],
     "narrative": "别的孩子追逐打闹时，你在一旁用树棍刻小人。"},
    {"name": "遭歧视的半兽人", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "兽人血统在身上太明显了。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "酒馆门上总贴着‘半兽人与狗不得入内’。"},
    {"name": "饥荒烙印", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "大饥荒中出生，从没吃饱过。", "modifiers": [("END", "-1d2*5")],
     "narrative": "胃是无底洞，可永远填不满胳膊上的肉。"},
    {"name": "流浪儿", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "从小在街头流浪，瘦骨嶙峋。", "modifiers": [("TEC", "-1d2*5")],
     "narrative": "老鼠是你的蛋白质来源，桥洞是你的卧室。"},
    {"name": "厄运缠身", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "出生弄塌了房子，被视为扫把星。", "modifiers": [("CRE", "-1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "同村的人凑钱把你送得越远越好。"},

    #============= COMMON (15) =============
    {"name": "平民子弟", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "城镇中的普通一员。", "modifiers": [],
     "narrative": "爸爸是面包师，妈妈洗衣，你负责在巷子里疯玩。"},
    {"name": "商人家族", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "家里开杂货铺，有些积蓄但缺乏锻炼。", "modifiers": [("CRE", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "数钱很快，可搬一袋面粉就喘。"},
    {"name": "佣兵养子", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "被佣兵团的大老粗们带大，能打不太能想。", "modifiers": [("END", "+1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "你会用匕首削水果，但不会写自己的名字。"},
    {"name": "没落贵族", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "有贵族头衔而无实财，自尊极高却内心脆弱。", "modifiers": [("CRE", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "你还穿着祖父的丝绸衬衣，但肘部已磨破。"},
    {"name": "矮人混血", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "矮人血脉让你壮实耐造，但动作有些笨重。", "modifiers": [("END", "+1d2*5"), ("SEN", "-1d2*5")],
     "narrative": "骨头硬得像铁，可跳舞时总踩舞伴的脚。"},
    {"name": "精灵遗孤", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "被遗弃的半精灵，美貌柔弱。", "modifiers": [("APP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "耳朵尖尖的，皮肤白得透明，感冒从没好利索过。"},
    {"name": "法师学徒之子", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "父亲是低阶法师，从小看书，长得瘦小。", "modifiers": [("EXP", "+1d1*5"), ("TEC", "-1d1*5")],
     "narrative": "四岁就能点燃蜡烛，但还没扫帚高。"},
    {"name": "狼孩", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "被野狼养了几年，野性强韧，但举止粗鲁。", "modifiers": [("LIB", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "闻到生肉就咽口水，花了三年才学会用刀叉。"},
    {"name": "马戏团小丑之子", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "在马戏团长大的你，身法灵活，但口袋空空。", "modifiers": [("SEN", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "三米高的独轮车骑得飞起，却买不起一双新鞋。"},
    {"name": "教会长大的孤儿", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "在唱诗班长大的你，信仰坚定，但性观念被压抑。", "modifiers": [("LOV", "+1d1*5"), ("LIB", "-1d1*5")],
     "narrative": "能背诵整本圣典，听到男女私会的故事会立刻红耳朵。"},
    {"name": "猎人后裔", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "父辈是护林人，熟悉森林，但不通文墨。", "modifiers": [("END", "+1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "能分辨五十种动物足迹，却分不清字母b和d。"},
    {"name": "半身人血脉", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "半身人远亲，个子极小但异常灵巧。", "modifiers": [("TEC", "-1d2*5"), ("SEN", "+1d2*5")],
     "narrative": "比同龄人矮了两个头，但偷苹果的本事一等一。"},
    {"name": "破落骑士世家", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "家里唯一的财产是一套生锈的铠甲。", "modifiers": [("END", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "从小举着比自己还重的大剑练习，吃的却是黑面包屑。"},
    {"name": "龙裔远亲", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "血脉里有一点龙族血统，活力略大，皮肤略粗。", "modifiers": [("LIB", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "手背上有几片小鳞片，总下意识藏进袖子。"},
    {"name": "学士之后", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "父母是皇家图书馆管理员，博学但久坐体弱。", "modifiers": [("EXP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "七岁就通读大陆通史，可跑几步路就脸色发白。"},

    #============= RARE (8) =============
    {"name": "纯血贵族", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "古老家族的嫡系血脉。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "摇篮边挂满了封地纹章。"},
    {"name": "天生魔力", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "自然魔力亲和，念咒自带加成。", "modifiers": [("EXP", "+1d2*5")],
     "narrative": "儿歌念着念着，床头的玩偶就飘起来了。"},
    {"name": "巨龙血统", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "激活了龙血，活力旺盛。", "modifiers": [("LIB", "+1d2*5")],
     "narrative": "拔出萝卜带出个大坑，这股劲头让农夫们张大了嘴。"},
    {"name": "精灵公主的馈赠", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "超凡脱俗的美貌。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "连街边的野猫都会过来蹭你的裙摆。"},
    {"name": "圣骑士祝福", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "受光明神祝福，情感纯净而坚定。", "modifiers": [("LOV", "+1d2*5")],
     "narrative": "直视邪异之物时，它们竟畏缩后退。"},
    {"name": "大天使之息", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "体质被圣光洗炼，百病不生。", "modifiers": [("END", "+1d2*5")],
     "narrative": "那次瘟疫肆虐，全城只有你还在广场喂鸽子。"},
    {"name": "矮人大师天赋", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "极致的巧手与敏锐，仿佛铁与火之子。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "三岁拼好的机械鸟，翅膀能扑腾好几下。"},
    {"name": "贤者转世", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "脑海里偶尔闪现不属于现世的知识。", "modifiers": [("EXP", "+1d2*5")],
     "narrative": "说起上古魔法原理时，老法师的水晶球裂了条缝。"},

    #============= LEGENDARY (4) =============
    {"name": "神之后裔", "rarity": "legendary", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "祖先是某位次级神祇。", "modifiers": [("LOV", "+1d3*5"), ("APP", "+1d2*5"), ("EXP", "+1d2*5")],
     "narrative": "出生那刻，教堂的圣钟不撞自鸣，白鸽盘旋不散。"},
    {"name": "泰坦血脉", "rarity": "legendary", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "远古泰坦的巨力在体内流淌。", "modifiers": [("LIB", "+1d3*5"), ("END", "+1d2*5"), ("TEC", "+1d2*5")],
     "narrative": "第一次打喷嚏，把奶妈吹出了三米远。"},
    {"name": "龙血王族", "rarity": "legendary", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "红龙血脉与王族结合的后代。", "modifiers": [("LIB", "+1d3*5"), ("END", "+1d2*5"), ("CRE", "+1d2*5")],
     "narrative": "瞳孔是竖立的金色，国王在你满月时亲自封地。"},
    {"name": "元素之子", "rarity": "legendary", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "受四大元素祝福的宠儿。", "modifiers": [("SEN", "+1d2*5"), ("EXP", "+1d3*5"), ("END", "+1d2*5")],
     "narrative": "一哭屋外就下雨，一笑彩虹跨过城堡。"},

    #============= WILDCARD (3) =============
    {"name": "被诅咒的狼人", "rarity": "wildcard", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "月圆之夜会变身为狂暴狼人。", "modifiers": [("LIB", "+1d3*5"), ("EXP", "-1d3*5")],
     "narrative": "你随时可能失控，变身后能徒手撕碎板甲，家人在你屋里钉满了银器。"},
    {"name": "亡灵低语者", "rarity": "wildcard", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "能与死者对话，周身缠绕着阴冷气息。", "modifiers": [("LOV", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "坟地的骷髅会向你问好，活人却都害怕你的死寂眼神。"},
    {"name": "命运骰子", "rarity": "wildcard", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "你的命运是一枚两面骰，能扭转局面，却遭家运反噬。", "modifiers": [("LOV", "+1d3*5"), ("CRE", "-1d3*5")],
     "narrative": "踩到狗屎能捡到金币，但你家当天就会遭窃，平衡得令人发毛。"},

     # ========== Horni 专属·dragonfire 天赋（15） ==========
    #============= NEGATIVE (3) =============
    {"name": "圣女遗训", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "出生即被献给某位贞洁女神，从小被严格管束。", "modifiers": [("LIB", "-1d2*5")],
     "narrative": "嬷嬷的戒尺时刻悬在头顶，连看一眼男仆都要做忏悔。"},
    {"name": "炼狱印记", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "胎记长在身上某处隐秘位置，使你对亲密接触无比敏感却抗拒。", "modifiers": [("LOV", "-1d1*5"), ("SEN", "-1d1*5")],
     "narrative": "母亲一边给你换尿布一边偷偷抹泪，说这印记是恶魔留的。"},
    {"name": "禁欲修道院", "rarity": "negative", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "被送入修道院抚养，从小诵读戒律。", "modifiers": [("LIB", "-1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "你会背的第一句话是‘肉体是罪’，玩具是磨光了棱的木十字架。"},

    #============= COMMON (5) =============
    {"name": "魅魔远祖", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "祖辈与魅魔有过一段情史，血脉中残留着诱惑的气质，但被族人忌惮。", "modifiers": [("APP", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "你婴儿时就让奶妈接连辞职，族中长老连看你都要划十字。"},
    {"name": "酒馆养大", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "母亲是酒馆老板娘，你从小看尽风月人情。", "modifiers": [("EXP", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "三岁就能听出酒客谎话里的破绽，七岁会替母亲挡走冒失的咸猪手。"},
    {"name": "森林精灵教养", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "被精灵族抚养过几年，自然观开放，性观念也极其松弛。", "modifiers": [("LIB", "+1d1*5"), ("APP", "+1d1*5")],
     "narrative": "精灵母亲教你万物皆有爱，你回到人类世界后总让保守的婶婶尖叫。"},
    {"name": "舞姬之女", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "母亲是宫廷舞姬，你身段柔软但身世存疑。", "modifiers": [("SEN", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "你能像猫一样在屋顶行走，可没人愿意告诉你父亲是谁。"},
    {"name": "兽人血统苏醒", "rarity": "common", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "兽人血让你欲望旺盛，体格惊人，但也带来粗野的外表。", "modifiers": [("LIB", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "你一岁就能掀翻饭桌，獠牙萌出时把奶妈吓得弃职而逃。"},

    #============= RARE (4) =============
    {"name": "魅魔血脉", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "祖辈的诱惑天赋在你身上完整觉醒。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "婴儿时哭一声，能让整个庄园的男仆放下手里的活全奔过来。"},
    {"name": "森林之歌", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "精灵血脉让你的肌肤如同上等丝绸般敏锐细腻。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "风从耳边吹过，你都能精准说出风带来的方位与气味。"},
    {"name": "巨龙之欲", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "龙血让你天生精力远超常人。", "modifiers": [("LIB", "+1d2*5")],
     "narrative": "保姆排了班轮流照看，因为你似乎从不需要睡觉。"},
    {"name": "维纳斯雕像", "rarity": "rare", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "天生骨架完美，注定长成大陆人人传颂的体态。", "modifiers": [("TEC", "+1d2*5")],
     "narrative": "雕塑师抱起你看了一眼，回家立刻砸碎了刚做完的女神像。"},

    #============= LEGENDARY (2) =============
    {"name": "爱与美之神选民", "rarity": "legendary", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "降生那刻，爱与美之神在你额头印下祝福之吻。", "modifiers": [("APP", "+1d3*5"), ("LOV", "+1d2*5"), ("SEN", "+1d2*5")],
     "narrative": "助产士声称看见房间里飘着玫瑰花瓣，神殿连夜派人来寻你。"},
    {"name": "暗夜女王血脉", "rarity": "legendary", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "传说中的暗夜魅魔女王是你的远祖，遗传给你致命的魅力与旺盛欲望。", "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d3*5"), ("EXP", "+1d2*5")],
     "narrative": "你的瞳孔在月夜下会泛起淡淡的紫光，老巫医一见便跪地不起。"},

    #============= WILDCARD (1) =============
    {"name": "魅魔契约", "rarity": "wildcard", "mode": "Horni", "scenarios": ["dragonfire"],
     "desc": "出生时父母与魅魔签下契约，换来你超凡的魅力，但寿元被悄悄抵押。", "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "你哭声里都带着勾魂的颤音，可每晚的咳嗽让母亲在床边偷偷祈祷。"},

     # ========== Horni·loneblade 日常天赋（40） ==========
    #============= NEGATIVE (10) =============
    {"name": "先天残脉", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "经脉天生受损，气血不足。", "modifiers": [("END", "-1d2*5")],
     "narrative": "师父替你摸骨时眉头越皱越紧，最后只叹了口气。"},
    {"name": "弃婴", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "被遗弃在荒郊野外的婴孩。", "modifiers": [("CRE", "-1d2*5")],
     "narrative": "连亲生父母是谁都不知道，襁褓里只有半块冷硬的饼。"},
    {"name": "面相凶煞", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "天生一副恶人相，让人避之不及。", "modifiers": [("APP", "-1d2*5")],
     "narrative": "婴孩时，抱过你的人都说这娃娃眉目带煞。"},
    {"name": "痨病鬼", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "先天肺气不足，动则咳喘。", "modifiers": [("END", "-1d2*5")],
     "narrative": "屋子里常年飘着药味儿，同门都怕被你染上。"},
    {"name": "心眼俱钝", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "学武的悟性差得惊人。", "modifiers": [("EXP", "-1d2*5")],
     "narrative": "一招最粗浅的入门拳法，旁人三月小成，你练了一年还走样。"},
    {"name": "胆小如鼠", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "生来怯懦，见血就晕。", "modifiers": [("LOV", "-1d2*5")],
     "narrative": "杀鸡的场面让你做了整月噩梦，醒来枕巾湿了大半。"},
    {"name": "跛足", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "一条腿天生使不上力，下盘飘浮。", "modifiers": [("SEN", "-1d2*5")],
     "narrative": "别的孩童追跑打闹，你走快些都要扶着墙喘。"},
    {"name": "力弱如鸡", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "臂力孱弱，连同龄女娃都比不过。", "modifiers": [("END", "-1d2*5")],
     "narrative": "提桶水都晃得满身湿，被村里顽童笑作纸片人。"},
    {"name": "侏儒之身", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "身形矮小得异于常人。", "modifiers": [("TEC", "-1d2*5")],
     "narrative": "七岁还不及五岁小儿高，总被错认为更小的孩童。"},
    {"name": "仇家遗腹", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "全家被仇敌灭门，仅你被藏在地窖躲过一劫。", "modifiers": [("CRE", "-1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "你是从血泊里被扒出来的，哭得嗓子彻底哑了。"},

    #============= COMMON (15) =============
    {"name": "农家子弟", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "生在寻常农户，本分老实。", "modifiers": [],
     "narrative": "爹娘只盼你早日下地干活，江湖不过说书人口中故事。"},
    {"name": "镖局之后", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "家里开着间小镖局，有些功夫底子却没读过书。", "modifiers": [("END", "+1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "三岁骑木马，五岁耍花枪，可三字经到七岁还背不全。"},
    {"name": "书香门第", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "祖上是秀才，满腹诗书却手无缚鸡之力。", "modifiers": [("EXP", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "小小年纪作得一手好诗，可被邻家娃子一推就倒。"},
    {"name": "渔家儿女", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "在水边长大，水性极佳，身形匀称但见识短浅。", "modifiers": [("SEN", "+1d1*5"), ("EXP", "-1d1*5")],
     "narrative": "能在水里憋气一盏茶，可出了渔村就分不清东南西北。"},
    {"name": "铁匠之子", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "从小抡锤打铁，膂力过人但反应偏慢。", "modifiers": [("END", "+1d2*5"), ("SEN", "-1d2*5")],
     "narrative": "八岁就能挥八斤小锤，可躲沙包时总被砸个正着。"},
    {"name": "戏班出身", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "父母是草台班子的伶人，你身段柔软但身份低贱。", "modifiers": [("SEN", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "翻筋斗劈叉信手拈来，可正经人家都瞧不起你这出身。"},
    {"name": "医馆药童", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "在药铺里泡大，懂些医理但身子骨没打熬好。", "modifiers": [("EXP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "闻闻味就知什么药材，可扛麻袋走不了半条街。"},
    {"name": "丐帮边缘", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "父母是丐帮底层弟子，练就一副厚脸皮和硬命。", "modifiers": [("LOV", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "乞食时被泼泔水也不哭，但粗粝日子磨糙了脸。"},
    {"name": "猎户之后", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "深山里长大，耳聪目明却不懂人情世故。", "modifiers": [("SEN", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "追踪野兔比追人还准，可进了镇子连问路都脸红。"},
    {"name": "武馆杂役", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "爹娘是武馆的烧火佣人，你偷师学了些三脚猫功夫。", "modifiers": [("SEN", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "蹲在墙角比划人家练拳，竟也学得几分样子。"},
    {"name": "官差家眷", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "父辈是衙门小吏，规矩森严，养出些威势但缺少历练。", "modifiers": [("LOV", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "说话自带三分官腔，可淋场雨就发三天烧。"},
    {"name": "绣娘之后", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "母亲是刺绣巧手，你的手指灵巧但性子软和。", "modifiers": [("SEN", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "穿针引线比耍刀弄枪更顺手，见人争吵心里先怯了。"},
    {"name": "走镖遗孤", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "父亲走镖丧命，母亲含辛茹苦，你懂事早却难免心重。", "modifiers": [("LOV", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "比同龄孩子更知冷暖，可衣裳上的补丁总摞得格外厚。"},
    {"name": "番邦后裔", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "高鼻深目，身形壮硕但遭中原人排挤。", "modifiers": [("TEC", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "骨架比汉家娃子大一圈，可巷子里总有人冲你扔石子。"},
    {"name": "佃户之子", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "租种地主薄田，挨饿是常事，练就了耐饿的肠胃。", "modifiers": [("END", "+1d1*5"), ("TEC", "-1d1*5")],
     "narrative": "饿上两顿照样满地跑，就是个子总窜不起来。"},

    #============= RARE (8) =============
    {"name": "天生神力", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "膂力自娘胎里便远超常人。", "modifiers": [("END", "+1d2*5")],
     "narrative": "五岁举石锁，九岁能抱着一头小牛犊走半里地。"},
    {"name": "根骨奇佳", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "天生一副练武的好胚子，铜皮铁骨。", "modifiers": [("END", "+1d2*5")],
     "narrative": "棍棒打在身上竟能反震开，教头连声称奇。"},
    {"name": "悟性超群", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "看过的招式一遍就能模仿七八分。", "modifiers": [("EXP", "+1d2*5")],
     "narrative": "师父演示完尚未开口，你已在旁比划得有模有样。"},
    {"name": "玉树临风", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "朗眉星目，风姿俊秀。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "逢年过节，媒婆快把你家门槛踏平了。"},
    {"name": "铁骨丹心", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "性子坚毅果敢，生来有一股侠气。", "modifiers": [("LOV", "+1d2*5")],
     "narrative": "路见不平，哪怕对方高你一头也敢上前理论。"},
    {"name": "身轻如燕", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "柔韧与轻盈仿佛是刻在骨头里的。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "捉迷藏从未被找到过，爬树攀墙如履平地。"},
    {"name": "名门之后", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "出身武林世家，自幼耳濡目染。", "modifiers": [("CRE", "+1d2*5")],
     "narrative": "抓阄时满地兵器谱和拳经，长辈们的笑声比爆竹还响。"},
    {"name": "虎背熊腰", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "骨架宽大，身形伟岸，天生猛将胚子。", "modifiers": [("TEC", "+1d2*5")],
     "narrative": "襁褓时就比别家婴孩重上一倍，接生婆差点没抱住。"},

    #============= LEGENDARY (4) =============
    {"name": "武曲降世", "rarity": "legendary", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "传说中武曲星君转世，奇经八脉先天自通。", "modifiers": [("END", "+1d3*5"), ("LIB", "+1d2*5"), ("LOV", "+1d2*5")],
     "narrative": "出生时屋内亮如白昼，房上瓦片被一股气劲冲开。"},
    {"name": "谪仙之姿", "rarity": "legendary", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "形貌气质不似凡间俗子，且兼灵台清明。", "modifiers": [("APP", "+1d3*5"), ("SEN", "+1d2*5"), ("EXP", "+1d2*5")],
     "narrative": "都说你投错胎，该去天上做神仙才是。"},
    {"name": "侠魁血脉", "rarity": "legendary", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "父系是前代武林盟主，血脉与家学皆属顶尖。", "modifiers": [("LOV", "+1d3*5"), ("CRE", "+1d2*5"), ("EXP", "+1d2*5")],
     "narrative": "满月宴上，各大派掌门竟亲自送来贺礼。"},
    {"name": "九阳之体", "rarity": "legendary", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "纯阳体质，气血旺盛，天生硬件出众。", "modifiers": [("END", "+1d3*5"), ("LIB", "+1d3*5"), ("EXP", "+1d2*5")],
     "narrative": "大雪天你单衣在外面玩，抱回来时浑身还冒着热气。"},

    #============= WILDCARD (3) =============
    {"name": "血仇之种", "rarity": "wildcard", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "全家被魔教屠戮，仇恨淬炼出惊人意志，却摧毁了天真。", "modifiers": [("LOV", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "那双眼睛里没有童真，只有烧不尽的火，笑时比哭更让人怕。"},
    {"name": "回光蛊", "rarity": "wildcard", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "自幼被种下奇蛊，濒死时会爆发巨力，平时却在啃噬生机。", "modifiers": [("END", "+1d3*5"), ("LIB", "-1d3*5")],
     "narrative": "你时常胸口绞痛苦着醒来，可上一次差点死时，硬生生把一头豹子撕成两半。"},
    {"name": "盗圣之子", "rarity": "wildcard", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "父亲是天下第一神偷，你继承了他的巧手，也继承了他的恶名。", "modifiers": [("SEN", "+1d3*5"), ("CRE", "-1d3*5")],
     "narrative": "当年偷遍大内的本事仿佛流在血里，可走到何处衙门的捕快都盯着你。"},
     # ========== Horni 专属·loneblade 天赋（15） ==========

    #============= NEGATIVE (3) =============
    {"name": "童子功世家", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "父辈练的是需终生持戒的童子功，自你落地便定下禁律。", "modifiers": [("LIB", "-1d2*5")],
     "narrative": "满月酒上爷爷当众立誓，你这辈子不得近女色——你连‘女色’是什么都还不懂。"},
    {"name": "寒玉体质", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "天生体寒，气血虚浮，对情欲毫无感知。", "modifiers": [("SEN", "-1d2*5")],
     "narrative": "冬天光着脚在雪地里跑也不觉凉，旁人挠你脚心你只是呆呆地看。"},
    {"name": "尼姑庵遗孤", "rarity": "negative", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "在庵堂或寺庙长大，自小受清规戒律熏陶。", "modifiers": [("LIB", "-1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "师太一有旁人亲近便用戒尺敲你手背，你至今见人拉手都下意识缩一下。"},

    #============= COMMON (5) =============
    {"name": "青楼养女", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "自小在烟花之地长大，眼观六路耳听八方。", "modifiers": [("APP", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "七岁就能分辨几位姐姐的客人脾性，替她们传话从不出错。"},
    {"name": "骨相风流", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "眉眼之间天生带着勾人的气韵，但体质偏虚。", "modifiers": [("APP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "街头算命瞎子摸过你的脸，连连摇头：‘这孩子是副招蜂引蝶的骨头。’"},
    {"name": "师父偏疼", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "被师门长辈格外溺爱，情感早慧但体魄欠磨。", "modifiers": [("LOV", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "别的师兄扎马步扎到腿抖，你被师父抱在膝上喂糖葫芦。"},
    {"name": "春宫秘本", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "幼时偶然翻到家中藏的春宫图，早熟得让人发笑。", "modifiers": [("EXP", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "六岁那年你捧着一本线装书看得入神，娘一进门就掀了桌。"},
    {"name": "药膳世家", "rarity": "common", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "祖辈以壮阳补身的药膳闻名，自幼随餐进补。", "modifiers": [("LIB", "+1d2*5"), ("EXP", "-1d2*5")],
     "narrative": "别人喝白米粥，你从小喝人参鹿茸汤，气血充盈得让大夫都咋舌。"},

    #============= RARE (4) =============
    {"name": "倾城倾国", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "容貌艳若桃李，举手投足皆是风情。", "modifiers": [("APP", "+1d2*5")],
     "narrative": "坊间说书人都拿你家的孩子当故事素材，说是王昭君转世。"},
    {"name": "灵台通窍", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "感知敏锐得异常，一丝风吹草动都能察觉。", "modifiers": [("SEN", "+1d2*5")],
     "narrative": "师父在你背后轻挥拂尘，你立即转头——他终于承认这孩子是块练剑的料。"},
    {"name": "阳气充沛", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "先天阳气旺盛，气血如泉涌。", "modifiers": [("LIB", "+1d2*5")],
     "narrative": "三更半夜你还在院里打拳，爹娘看着只摇头：‘这娃子的劲儿使不完哟。’"},
    {"name": "销魂掌世家", "rarity": "rare", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "祖辈精通点穴之术，掌下柔劲天赋异禀。", "modifiers": [("SEN", "+1d1*5"), ("APP", "+1d1*5")],
     "narrative": "你家传绝学讲究以柔克刚，你小小年纪指尖按穴已有几分功力。"},

    #============= LEGENDARY (2) =============
    {"name": "魅姬血脉", "rarity": "legendary", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "祖上是前朝倾城美人，家传媚骨与聪慧一并流到你身上。", "modifiers": [("APP", "+1d3*5"), ("SEN", "+1d2*5"), ("EXP", "+1d2*5")],
     "narrative": "外婆翻出旧时画像，画中人眉眼与你如出一辙——她曾让半壁江山为她倾倒。"},
    {"name": "纯阳童子", "rarity": "legendary", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "罕见的先天纯阳之体，气血旺盛至神异。", "modifiers": [("LIB", "+1d3*5"), ("END", "+1d2*5"), ("APP", "+1d2*5")],
     "narrative": "高僧途经村落，摸过你的头顶长叹：‘此子一身阳气，世间少见——可惜了。’"},

    #============= WILDCARD (1) =============
    {"name": "采阴之咒", "rarity": "wildcard", "mode": "Horni", "scenarios": ["loneblade"],
     "desc": "家族秘法将你塑成天生的勾魂体，魅力惊人却伴随生机损耗。", "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d2*5"), ("END", "-1d3*5")],
     "narrative": "族长在你满月时用朱砂在你眉心点了一滴——从此你比同龄人漂亮得多，也体弱得多。"},
]


# ============================================================
# Helper Pattern for the Skill Block
# ============================================================
def get_skill_block(c):
    if c.get("skill_checks_enabled", True):
        return """
【🎲检定系统（重要选择由骰子决定）】
本游戏中，有失败可能的选择由程序投骰判定，你不再决定胜负。
- 你可以要求判定这 13 个属性：（STR, LIB, TEC, APP, END, SEN, LOV, EXP, CRE, LUCK, ASSET, FAME, EXPE, KNOW）。
- choices.checks 填 1 和少数情况下最多 2 个属性键，difficulty 填 "easy"/"normal"/"hard"。
- 纯偏好选择不填 checks。
- 不困难的行动也不填checks。
- 你不需要每次都输出各一个easy/normal/hard。记住你首先需要保证代入感而不是做一个无情的鉴定机器。
- 记住checks本身就代表这个行为有一定难度。作为参考：
主角决定晚上去找某个人- no check
主角决定和某个人在正常的情况下搭话 - no check
深夜的房子安静无声，主角将耳朵贴在门上。（因为环境安静）- easy DEX + INT
主角需要翻过一堵约两米高的砖墙，墙面有些凸起的砖块可作为支撑点，但下着小雨略显湿滑。- normal DEX
主角试图说服旅馆老板透露昨晚那位神秘客人的房间号，对方有些警惕但并非完全敌对。- normal APP
对面坐着的是一位老练的政客，他面带微笑、语气平和，每一句话都滴水不漏。主角想要看穿他背后的意图- hard INT
"""
    else:
        return """
【🎭 无鉴定模式】
本局游戏不使用骰子鉴定。所有选择的结果由你根据角色属性、天赋和故事逻辑自行决定。
请在叙事中自然地赋予成功或失败，保持故事的戏剧性。
"""


# ============================================================
# system prompt（性压抑专用）
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
    
    intense = (c.get("mode") == MODE_HORNY_INTENSE) # Make sure MODE_HORNY_INTENSE is defined!
    start_age_block = ""
    if intense:
        start_age_block = (
            "\n【⚠️ 加强版：18 岁起开局】\n"
            "玩家选择了「我真的有爱压抑😢！」模式，从 18 岁开始游戏。\n"
            "属性已经由背景故事生成，请把 18 岁之前的经历当作既成事实，"
            "在 narrative 中可以以回忆形式偶尔提及。\n"
            "未成年阶段已跳过，所有情色内容**不再有年龄限制**。"
        )

    # CALL THE HELPER FUNCTION HERE
    skill_block = get_skill_block(c)
    max_hp = max(1, (attrs.get("END", 50) + attrs.get("LIB", 50)) // 10)
    
    return f"""你是"AI人生重开手账·性压抑特别版"的叙事AI。这是一个**成人向**的人生模拟游戏，你需要为玩家推演ta的一生，并在合适的年龄显著加重情色、暧昧、亲密关系、欲望挣扎、情感纠葛等元素。
【世界设定】
{c['scene_name']}：{c['scene_desc']}
【角色基本信息】
性别：{c['gender']}　种族：{c['race']}{extra}{backstory}
【角色属性（与正常模式不同，按情色向重新设计）】
{attr_text}
最大生命/精力 HP_MAX = (END + LIB) // 10 = {max_hp}
【天赋】
{talents_text}
{start_age_block}
【🌶️ 主题指引】
- 你应当大胆描写：暧昧邂逅、性张力、身体描写、初恋初吻、情欲冲突、桃色事件、身体觉醒、情感纠葛、风流韵事、艳遇、出轨、痴恋、露骨场景。
- 描写可以直白、煽情、香艳，但必须服务于人物塑造与故事推进，不要无意义的色情堆砌。
- 高 APP / TEC / LIB 的角色更易遭遇桃色事件；低属性者也可有自己挣扎、暗恋、苦恋的故事线。
- 适当展现欲望与情感的冲突、占有与失去、耻感与解放。
- 选项 has_choice=true 时可加入与情感/欲望相关的关键抉择。
- **道德底线**：禁止出现未成年人卷入的露骨情节；禁止任何形式的真实违法内容。
- 当天赋给出的背景和属性冲突时，以属性为准，但要在背景中找补。
- 14 岁以下：仅做情感萌芽、暗恋、青涩描写，绝无性内容。
- 14~17 岁：可有亲吻、暧昧、青春期觉醒，**不写性器官与性行为细节**。
- 18 岁起：放开。
【⛔ 规则：核心属性与派生属性（基于 1-100 制）】
- 核心八大属性出生即固定，不得改动。
- 派生属性包含：ASSET(资产)、FAME(名气)、EXPE(经验)、KNOW(知识)。
- 严禁直接加派生属性！如果因为剧情需要提升，请在 adjustments 里使用后缀 `_GROWTH` 给予检定。例如：`"FAME_GROWTH": 2`。
- 直接扣减是允许的：如果角色破产被骗，可输出 `"ASSET": -20`。
【❤️ HP】
- HP_MAX = (SIZ + CON) // 10 = {max_hp}。系统每年自然恢复 1 HP。
- 普通感冒 0~-1，濒死/重大灾难 -5~-10。HP ≤ 0 即死亡。
- 在此模式下里，过量/实在过于刺激的体验可以酌情扣除1-2点HP。
【其他派生】
- ASSET / FAME / KNOWLEDGE 整数变化。
- EDU 1~18 岁系统自动 +1（intense 模式已经是 18），辍学等可给负数。
{skill_block}
【输出格式】（严格 JSON，只输出 JSON）
{{
  "narrative": "本年事件描述（一句话到 400 字之间，可以露骨但要有文笔）",
  "has_choice": false,
  "choices": {{
    "A": {{"text": "选项A描述", "checks": ["LIB"], "difficulty": "normal"}},
    "B": {{"text": "选项B描述", "checks": ["APP","SEN"], "difficulty": "hard"}},
    "C": {{"text": "选项C描述（纯偏好）", "checks": [], "difficulty": null}}
  }},
  "adjustments": {{"HP": -1, "ASSET": 0, "FAME": 0, "KNOWLEDGE": 0, "EDU": 0}},
  "alive": true,
  "cause_of_death": null
}}
"""


def build_intense_init_prompt(c):
    """我真的有爱压抑😢 模式：让 AI 根据背景故事生成 18 岁初始角色。"""
    
    # CALL THE HELPER FUNCTION HERE AGAIN TO PREVENT NameError!
    skill_block = get_skill_block(c)
    
    return f"""玩家选择了「我真的有爱压抑😢！」模式，需要你为这个 18 岁的角色生成初始数据。
【世界设定】{c['scene_name']}：{c['scene_desc']}
【性别】{c['gender']}　【种族】{c['race']}
【额外设定】{c.get('extra_info','（无）')}
【背景故事】{c.get('backstory','（玩家未填，请自由编）')}
请为该角色生成：
1. 8 个属性数值，**总和必须正好为 400** (平均50*8)，每个属性范围 10~90，整数。
   属性键名固定为：LIB, TEC, APP, END, SEN, LOV, EXP, CRE。
2. 三条天赋（自由发挥，要符合背景故事），每条包含 name / desc / narrative / rarity（negative/common/rare/legendary）。
3. 一段 100~200 字的"开场旁白"（18 岁这一年的现状），写在 narrative 里。

{skill_block}
【输出格式】（严格 JSON，只输出 JSON）
{{
  "attributes": {{
    "LIB": 50, "TEC": 50, "APP": 50, "END": 50, 
    "SEN": 50, "LOV": 50, "EXP": 50, "CRE": 50
  }},
  "talents": [
    {{"name": "天赋名", "desc": "作用效果", "narrative": "背景描述", "rarity": "common"}}
  ],
  "narrative": "18岁开场旁白：这一年...",
  "has_choice": true,
  "choices": {{
    "A": {{"text": "第一天去上学...", "checks": ["APP"], "difficulty": "easy"}},
    "B": {{"text": "在家休息...", "checks": ["END"], "difficulty": "normal"}},
    "C": {{"text": "偷偷溜出去...", "checks": [], "difficulty": null}}
  }},
  "adjustments": {{"HP": 0, "ASSET": 0, "FAME": 0, "KNOWLEDGE": 0, "EDU": 0}},
  "alive": true,
  "cause_of_death": null
}}
"""

# ============================================================
# v0.5 expandable mode interface
# ============================================================

MODE_ID = "horny_mild"
MODE_LABEL = "性压抑模式"
MODE_DESCRIPTION = "成人向人生模拟模式。"
TALENT_MODE_TAG = "Horni"

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
    "assets": {"label": "资产", "adjustment_key": "ASSET", "initial": 1, "tiers": ASSET_TIERS, "unlock_age": 4, "locked_text": "（未成年）"},
    "fame":   {"label": "名声", "adjustment_key": "FAME", "initial": 10, "tiers": FAME_TIERS},
    "expe":   {"label": "经验", "adjustment_key": "EXPE", "initial": 1, "tiers": EXPE_TIERS, "unlock_age": 4, "locked_text": "（未成年）"},
    "know":   {"label": "知识", "adjustment_key": "KNOW", "initial": 1, "tiers": KNOW_TIERS},
}

# 引入 data 的成长挂载逻辑
from data import apply_turn_start_effects, apply_tracker_adjustment, init_trackers



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
    return max(1, (final_attributes.get("END", 50) + final_attributes.get("LIB", 50)) // 10)


def build_action_check_prompt(c, action_text):
    """性压抑模式版本：用 LIB/TEC/APP/END/SEN/LOV/EXP/CRE/LUCK/ASSET/FAME/EXPE/KNOW。"""
    attrs_text = "、".join(ATTRIBUTES + ["LUCK"])
    return f"""玩家想在当前时间点主动做一件事。你只需要判断需要哪些属性鉴定。
玩家行动：{action_text}
可用属性：{attrs_text}

判定原则：
- 简单的小事 → 1 个属性，难度 easy。
- 一般行动 → 1 个属性，难度 normal。
- 涉及多种能力或非常困难的事 → 2 个属性，难度 normal 或 hard。
- 纯偏好选择 → checks: []。
- 鉴定本身已代表"有难度的事"，**只在真正棘手时用 hard**。

严格只返回如下 JSON：
{{
  "checks": ["LIB"],
  "difficulty": "normal",
  "reasoning": "一句话理由"
}}
"""