# scenario_1920s.py —— 模块化情景数据模板
# 包含：情景基础设定，以及该情景在 Normal, Intense, Store 三个模式下的专属天赋。

# ============================================================
# 1. 情景基础设定 (Scenario Definition)
# 将会被导入到 data.py 的 SCENES 列表中
# ============================================================
SCENARIO_DEF = {
    "id": "1920s",               # 唯一 ID
    "name": "传奇一代",           # UI 显示的名称
    "scenario_tag": "betweentheworlds", # 核心 Tag！用于过滤该情景的专属天赋
    "has_edu": False,                    # 是否拥有义务教育/近代教育体系
    "desc": "两次大战之间的1920s，表面平静，暗流涌动。"
}

# ============================================================
# 2. 模式专属天赋池 (Talent Pools)
# ============================================================

# ------------------------------------------------------------
# [A] 普通模式 (Normal) 天赋
# 属性池: STR, CON, POW, DEX, APP, SIZ, INT, CRE
# ------------------------------------------------------------
# ============================================================
# TALENT_POOL_NORMAL - 传奇一代 (1920s) 普通模式天赋
# 属性池: STR, CON, POW, DEX, APP, SIZ, INT, CRE
# ============================================================
# ============================================================
# TALENT_POOL_NORMAL - 传奇一代 (1920s) 普通模式天赋
# 属性池: STR, CON, POW, DEX, APP, SIZ, INT, CRE
# ============================================================
TALENT_POOL_NORMAL = [
    # ============================================================
    # [负面天赋 NEGATIVE] - 10个 (Red)
    # 总属性损失不超过 1d2
    # ============================================================
    {
        "name": "战争遗孤",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的父亲倒在了索姆河，母亲在西班牙流感中离世。",
        "modifiers": [("CON", "-1d2*5")],
        "narrative": "你被辗转送到亲戚家寄养，从小就明白这个世界欠你的，永远讨不回来。"
    },
    {
        "name": "贫民窟出身",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你出生在城市最阴暗的角落，营养不良是常态。",
        "modifiers": [("SIZ", "-1d2*5")],
        "narrative": "煤烟熏黑了你家的墙壁，廉价杜松子酒的气味浸透了你童年的每一个夜晚。"
    },
    {
        "name": "佝偻病史",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "童年时期缺乏阳光与营养，留下了身体上的痕迹。",
        "modifiers": [("STR", "-1d2*5")],
        "narrative": "医生说你需要鱼肝油和阳光，但你家两样都没有。"
    },
    {
        "name": "西班牙流感后遗症",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你在那场大流行中活了下来，但肺部从未完全恢复。",
        "modifiers": [("CON", "+1d1*5"), ("STR", "-1d3*5")],
        "narrative": "你记得母亲戴着纱布口罩抱着你的样子，那是你对她最后的记忆。"
    },
    {
        "name": "孤儿院长大",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "在严苛的修女管教下长大，从未感受过真正的温暖。",
        "modifiers": [("APP", "+1d1*5"), ("POW", "-1d3*5")],
        "narrative": "你学会了在被发现哭泣前迅速擦干眼泪，也学会了不再期待任何人。"
    },
    {
        "name": "毒气受害者之子",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "父亲在战壕里吸入了芥子气，你继承了他的虚弱。",
        "modifiers": [("CON", "-1d2*5")],
        "narrative": "你听着父亲夜复一夜的咳嗽长大，那声音成了你梦中挥之不去的背景音。"
    },
    {
        "name": "童工岁月",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "六岁就在纺织厂里做工，机器轰鸣偷走了你的童年。",
        "modifiers": [("DEX", "+1d1*5"), ("SIZ", "-1d3*5")],
        "narrative": "你的小手最适合钻进机器底下捡线头——直到隔壁的小姑娘没能及时缩回来。"
    },
    {
        "name": "酗酒家庭",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "禁酒令？那不过是让你父亲喝得更凶的借口罢了。",
        "modifiers": [("POW", "-1d2*5")],
        "narrative": "你学会了在父亲回家前藏起母亲的针线盒，因为那里面藏着家里仅剩的几枚硬币。"
    },
    {
        "name": "天生面斑",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "脸上的胎记让你从小被当作怪物。",
        "modifiers": [("INT", "+1d1*5"), ("APP", "-1d3*5")],
        "narrative": "镜子是你最不愿意面对的东西，你学会了在书本中寻找另一个世界。"
    },
    {
        "name": "破产家庭",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "家族在战后的经济动荡中一败涂地。",
        "modifiers": [("APP", "+1d1*5"), ("CON", "-1d3*5")],
        "narrative": "你穿着合身但已经磨损的旧西装，在邻居们怜悯的目光中长大。"
    },

    # ============================================================
    # [普通天赋 COMMON] - 15个 (Black)
    # 净值为零，互有得失
    # ============================================================
    {
        "name": "传教士之女",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "在远东的传教站长大，见识了与故乡完全不同的世界。",
        "modifiers": [("INT", "+1d2*5"), ("APP", "-1d2*5")],
        "narrative": "你说着流利的官话，却在回到伦敦后被同龄人嘲笑像个野孩子。"
    },
    {
        "name": "码头工人之子",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "在港口的吊车与汽笛声中长大。",
        "modifiers": [("STR", "+1d2*5"), ("INT", "-1d2*5")],
        "narrative": "你十岁就能扛起一袋面粉,但学校的拉丁文课总让你昏昏欲睡。"
    },
    {
        "name": "马戏团出身",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的家族跟着流动马戏团走遍了半个国家。",
        "modifiers": [("DEX", "+1d2*5"), ("CON", "-1d2*5")],
        "narrative": "三岁学走钢丝,五岁学驯兽,但流浪的生活让你比同龄人瘦弱许多。"
    },
    {
        "name": "乡村医生家庭",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "父亲是小镇上唯一的医生,你从小耳濡目染。",
        "modifiers": [("INT", "+1d2*5"), ("STR", "-1d2*5")],
        "narrative": "你认得每一种草药的拉丁学名,但从未真正下过田。"
    },
    {
        "name": "钟表匠的学徒",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "祖父的工坊里,你学会了最精细的活计。",
        "modifiers": [("DEX", "+1d2*5"), ("STR", "-1d2*5")],
        "narrative": "齿轮与发条的世界比外面的喧嚣更让你安心。"
    },
    {
        "name": "教师子女",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "母亲是村里小学的女教师,书是你最熟悉的玩具。",
        "modifiers": [("INT", "+1d1*5"), ("APP", "+1d1*5"), ("CON", "-1d2*5")],
        "narrative": "你六岁就能背诵丁尼生的诗,但从未在田野里疯跑过。"
    },
    {
        "name": "渔民之家",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "海风与咸味是你最早的记忆。",
        "modifiers": [("CON", "+1d2*5"), ("CRE", "-1d2*5")],
        "narrative": "你能凭海浪的颜色判断明天的天气,但对城里人的弯弯绕绕一窍不通。"
    },
    {
        "name": "铁匠铺的孩子",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "在炉火与铁砧的轰鸣声中长大。",
        "modifiers": [("STR", "+1d2*5"), ("DEX", "-1d2*5")],
        "narrative": "你的肩膀比同龄人宽阔,但握笔时总显得笨拙。"
    },
    {
        "name": "戏院后台长大",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "母亲是戏院的服装师,你在舞台幕后度过童年。",
        "modifiers": [("APP", "+1d2*5"), ("POW", "-1d2*5")],
        "narrative": "你见过太多浓妆下的真实面孔,也学会了如何用妆容隐藏自己。"
    },
    {
        "name": "贵族落魄旁支",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "家族的徽章还在,但金库早已空空如也。",
        "modifiers": [("APP", "+1d2*5"), ("CON", "-1d2*5")],
        "narrative": "你被教导要挺直腰板,即使午餐只有一片冷面包。"
    },
    {
        "name": "图书馆员之子",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "在书架的迷宫中度过童年。",
        "modifiers": [("INT", "+1d2*5"), ("STR", "-1d2*5")],
        "narrative": "羊皮纸与旧墨水的气味是你心目中最安全的味道。"
    },
    {
        "name": "邮差之女",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "父亲跑遍了整个郡的乡间小路。",
        "modifiers": [("CON", "+1d1*5"), ("DEX", "+1d1*5"), ("INT", "-1d2*5")],
        "narrative": "你跟着父亲的自行车跑过无数个清晨,认得每一户人家的狗。"
    },
    {
        "name": "屠夫家庭",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "在血腥味中习惯了死亡。",
        "modifiers": [("STR", "+1d1*5"), ("CON", "+1d1*5"), ("APP", "-1d2*5")],
        "narrative": "你比同龄女孩更懂得分辨肉的部位,但她们似乎并不欣赏这种本事。"
    },
    {
        "name": "印刷厂学徒",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "油墨与铅字塑造了你的手指与思想。",
        "modifiers": [("INT", "+1d1*5"), ("DEX", "+1d1*5"), ("STR", "-1d2*5")],
        "narrative": "你比城里大多数大学生都早一步读到新出的小说。"
    },
    {
        "name": "牧师之子",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "在教堂的钟声与圣咏中长大。",
        "modifiers": [("POW", "+1d2*5"), ("CRE", "-1d2*5")],
        "narrative": "你比同龄人更早思考关于灵魂的问题,但对世俗的乐趣总是格格不入。"
    },

    # ============================================================
    # [稀有天赋 RARE] - 8个 (Blue)
    # 总属性增益不超过 1d2
    # ============================================================
    {
        "name": "天生美声",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的嗓音从小就让邻里惊叹。",
        "modifiers": [("APP", "+1d2*5")],
        "narrative": "教堂的唱诗班指挥说,这是上帝赐予的礼物。"
    },
    {
        "name": "工程师血统",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "祖父参与过铁路建设,机械的天赋流淌在你的血液里。",
        "modifiers": [("INT", "+1d1*5"), ("DEX", "+1d1*5")],
        "narrative": "你拆开第一个怀表时,只有四岁。"
    },
    {
        "name": "运动天才",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的身体协调性让所有教练都侧目。",
        "modifiers": [("STR", "+1d1*5"), ("DEX", "+1d1*5")],
        "narrative": "学校的板球队长第一眼就看中了你。"
    },
    {
        "name": "外交官之女",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "童年随父亲辗转于欧洲各国大使馆。",
        "modifiers": [("INT", "+1d1*5"), ("APP", "+1d1*5")],
        "narrative": "你能用三种语言点菜,也见过未来将改写历史的几张面孔。"
    },
    {
        "name": "艺术世家",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "在画家、诗人与音乐家的沙龙中长大。",
        "modifiers": [("CRE", "+1d2*5")],
        "narrative": "你五岁就坐在毕加索的膝上听他讲故事——虽然你当时只觉得他烟味很重。"
    },
    {
        "name": "童年神童",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的智力在很小的时候就显露出来。",
        "modifiers": [("INT", "+1d2*5")],
        "narrative": "八岁时,你已经能和父亲讨论达尔文与赫胥黎的争论。"
    },
    {
        "name": "强健体魄",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你天生就比同龄人壮实。",
        "modifiers": [("STR", "+1d1*5"), ("CON", "+1d1*5")],
        "narrative": "镇上的老人说你像是从中世纪走出来的小骑士。"
    },
    {
        "name": "灵巧双手",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的手指仿佛拥有独立的意志。",
        "modifiers": [("DEX", "+1d2*5")],
        "narrative": "无论是弹钢琴还是拆锁,你都比别人快上一截。"
    },

    # ============================================================
    # [传奇天赋 LEGENDARY] - 4个 (Purple)
    # 总属性增益不超过 3d3
    # ============================================================
    {
        "name": "罗曼诺夫家族的远亲",
        "rarity": "legendary",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "革命的烈火中,你的家族带着秘密与黄金逃亡西方。",
        "modifiers": [("APP", "+1d3*5"), ("INT", "+1d3*5"), ("POW", "+1d3*5")],
        "narrative": "母亲临终前给了你一枚法贝热彩蛋,告诉你这只是开始。你不知道远房表亲中是否真有人在叶卡捷琳堡那栋房子里活下来了。"
    },
    {
        "name": "被遗忘的圣徒血脉",
        "rarity": "legendary",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的家族世代守护着一个不能言说的秘密。",
        "modifiers": [("POW", "+1d3*5"), ("CON", "+1d3*5"), ("INT", "+1d3*5")],
        "narrative": "祖母在你十岁生日时给你看了那本书。从那以后,你的梦境再也不曾平静,但你的眼神也变得与众不同。"
    },
    {
        "name": "完美的造物",
        "rarity": "legendary",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "上帝在创造你时,似乎格外用心。",
        "modifiers": [("APP", "+1d3*5"), ("STR", "+1d3*5"), ("DEX", "+1d3*5")],
        "narrative": "助产士看到你的第一眼就划了十字。镇上的老人们说,这种孩子要么成为传奇,要么早早夭折。"
    },
    {
        "name": "工业巨擘的私生子",
        "rarity": "legendary",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的母亲是某位钢铁大王的情人,你从未被正式承认。",
        "modifiers": [("INT", "+1d3*5"), ("APP", "+1d3*5"), ("CRE", "+1d3*5")],
        "narrative": "每月一笔丰厚的汇款匿名寄到母亲手中。你继承了那个男人的眼睛、头脑,以及某种说不清的野心。"
    },

    # ============================================================
    # [万能牌 WILDCARD] - 3个 (Pink)
    # 大喜大悲,大起大落
    # ============================================================
    {
        "name": "瓜分遗产的唯一继承人",
        "rarity": "wildcard",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "一位素未谋面的远房叔叔留下了一切,以及他的诅咒。",
        "modifiers": [("INT", "+1d3*5"), ("APP", "+1d3*5"), ("CON", "-1d3*5")],
        "narrative": "律师送来的信件附带着一把钥匙和一份警告。家族中有人说,那位叔叔最后是在精神病院里咬断舌头死的。"
    },
    {
        "name": "降神会中诞生",
        "rarity": "wildcard",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的母亲在一场降神会上临盆,据说有什么东西在那一刻附在了你身上。",
        "modifiers": [("POW", "+1d3*5"), ("CRE", "+1d3*5"), ("APP", "-1d3*5")],
        "narrative": "灵媒当场惊叫着逃出房间。母亲此后再也不愿提起那个夜晚,但你偶尔会做一些不属于自己的梦。"
    },
    {
        "name": "战壕里的奇迹",
        "rarity": "wildcard",
        "mode": "Normal",
        "scenarios": ["betweentheworlds"],
        "desc": "你的父亲在凡尔登的弹坑中幸存,母亲说那是天使的眷顾,你继承了这份眷顾——和代价。",
        "modifiers": [("STR", "+1d3*5"), ("CON", "+1d3*5"), ("POW", "-1d3*5")],
        "narrative": "父亲带回来的不仅是一枚勋章,还有他从战场上捡到的一块奇怪的金属碎片。他说当他握着它的时候,所有的子弹都偏开了。现在它挂在你的脖子上。"
    },
]
# ------------------------------------------------------------
# [B] 极致性压抑模式 (Horny Intense) 天赋
# 属性池: STR, LIB(性欲), TEC(身材), APP, END(体力), SEN(敏感), LOV(爱情), POW(意志), CRE
# ------------------------------------------------------------
TALENT_POOL_INTENSE = [
    # ============================================================
    # NEGATIVE (2个)
    # ============================================================
    {"name": "维多利亚遗毒", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "母亲那一代的禁欲教育在你身上留下了深刻烙印。",
     "modifiers": [("LIB", "-1d2*5"), ("SEN", "-1d1*5"), ("POW", "+1d1*5")],
     "narrative": "你能在最香艳的场合面不改色——但夜深人静时,镜子里的自己让你陌生。"},
    
    {"name": "梅毒阴影", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "盘尼西林尚未问世的年代,有些病只能小心翼翼地避开。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "你见过太多朋友以那种方式结束。每一次心动之前,你都先想起那些疯人院里的面孔。"},

    # ============================================================
    # NORMAL/COMMON (4个)
    # ============================================================
    {"name": "飞女郎", "rarity": "common", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "短发,短裙,长烟杆——你是新时代的代言人。",
     "modifiers": [("APP", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "你拒绝当任何人的妻子。婚姻是上一代人的牢笼,你只想要今晚的香槟和明早的自由。"},
    
    {"name": "战时护士情结", "rarity": "common", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "在战地医院的经历改变了你对身体的看法。",
     "modifiers": [("SEN", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "你见过太多年轻的身体被撕裂。从那以后,完整的、温暖的、活着的肉体在你眼中神圣得近乎荒谬。"},
    
    {"name": "查尔斯顿舞者", "rarity": "common", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "你能跳一整夜不停。",
     "modifiers": [("END", "+1d1*5"), ("TEC", "+1d1*5"), ("LOV", "-1d2*5")],
     "narrative": "舞池里你属于所有人,也不属于任何人。"},
    
    {"name": "诗人的情人", "rarity": "common", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "你出现在某位迷失世代作家的作品里。",
     "modifiers": [("APP", "+1d2*5"), ("POW", "-1d2*5")],
     "narrative": "他在巴黎写你,在马德里也写你。你读着自己被印成铅字的样子,分不清哪个才是真的自己。"},

    # ============================================================
    # RARE (2个)
    # ============================================================
    {"name": "地下爵士名伶", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "你是纸醉金迷的化身。",
     "modifiers": [("APP", "+1d2*5"), ("LIB", "+1d1*5")],
     "narrative": "在烟雾缭绕的地下酒吧里,你的歌声和身段是所有人欲念的焦点。"},
    
    {"name": "神秘学狂热", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "对禁忌知识的渴望扭曲了你的欲望。",
     "modifiers": [("LIB", "+1d2*5"), ("SEN", "+1d1*5")],
     "narrative": "阅读那些不该存在的古籍时,你感到的不是恐惧,而是一种病态的、令人颤抖的兴奋。"},

    # ============================================================
    # LEGENDARY (1个)
    # ============================================================
    {"name": "巴黎沙龙女王", "rarity": "legendary", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "塞纳河左岸的每一位艺术家都为你写过点什么。",
     "modifiers": [("APP", "+2d3*5"), ("LIB", "+1d2*5"), ("CRE", "+1d2*5")],
     "narrative": "毕加索画过你的肩膀,海明威写过你的笑声,科莱特亲吻过你的指尖。你的客厅是二十世纪艺术的诞生地之一——以及更多更私密事物的发生地。"},

    # ============================================================
    # WILDCARD (1个)
    # ============================================================
    {"name": "希腊神祇的化身", "rarity": "wildcard", "mode": "HorniIntense", "scenarios": ["betweentheworlds"],
     "desc": "某个春天的夜晚,你在德尔斐的废墟上做了一个梦,从此你不再完全是你自己。",
     "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d3*5"), ("LOV", "-1d3*5")],
     "narrative": "你能让任何人为你疯狂——但你再也无法真正爱上任何凡人。镜子里的眼睛偶尔会闪烁着不属于这个时代的金色。"},
]

# ------------------------------------------------------------
# [C] 通马桶模拟器模式 (Store Mode) 天赋
# 属性池: STR, CRE, HMR(人脉), INT, APP, END
# ------------------------------------------------------------
TALENT_POOL_STORE = [
    # ============================================================
    # NEGATIVE (10个) - 总属性损失不超过 1d2
    # ============================================================
    {"name": "战壕咳", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "毒气在你肺里留下了永久的纪念。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "每个老兵酒馆里都有人认得这种咳嗽。你们点头，干杯,然后假装没事。"},
    
    {"name": "禁酒令前科", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你蹲过号子,联邦档案里有你的名字。",
     "modifiers": [("APP", "-1d2*5"), ("CRE", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "正经银行不会贷款给你,但有些人就喜欢和有案底的人做生意。"},
    
    {"name": "鸦片债务", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在唐人街的某间屋子里欠下了不该欠的账。",
     "modifiers": [("CRE", "-1d2*5"), ("END", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "那位面带微笑的老板每个月都派人来'问候'一次。"},
    
    {"name": "弹震症", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "凡尔登的炮声还在你耳朵里响。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("STR", "+1d1*5")],
     "narrative": "突如其来的声响会让你瞬间瘫倒在地。但当真的危险来临时,你比谁反应都快。"},
    
    {"name": "黑名单常客", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "几家大商会联合把你列进了不来往名单。",
     "modifiers": [("HMR", "-1d2*5"), ("CRE", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你做错了什么?也许什么都没做,只是挡了某位先生的财路。"},
    
    {"name": "吗啡瘾君子", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "战地医院给你打的针让你再也离不开它。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "你穿长袖是有原因的。生意做得再大,每天那一针不能少。"},
    
    {"name": "爵士夜生活", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "夜总会和地下酒吧消耗了你的身体和钱包。",
     "modifiers": [("END", "-1d2*5"), ("CRE", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "你认得每一个爵士乐手的名字。代价是你的肝脏和银行存款。"},
    
    {"name": "赤色嫌疑人", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "帕尔默大搜捕之后,你的名字进了某些档案。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你只是参加过几次工人集会。但在这个年头,这就够了。"},
    
    {"name": "战争创伤面孔", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "弹片削去了你半张脸,你戴着锡制面具谈生意。",
     "modifiers": [("APP", "-1d3*5"), ("INT", "+1d1*5")],
     "narrative": "客户们最初不敢直视你。但他们很快发现,看不到表情的对手最难谈判。"},
    
    {"name": "遗孀的诅咒", "rarity": "negative", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你欠了某位战死战友的妻子一个解释。",
     "modifiers": [("CRE", "-1d2*5"), ("HMR", "-1d1*5"), ("END", "+1d1*5")],
     "narrative": "她每个月按时收到匿名汇款。她以为是政府寄的,其实是你。"},

    # ============================================================
    # COMMON (15个) - 净值零或大致平衡
    # ============================================================
    {"name": "前线传令兵", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在战壕之间跑了四年。",
     "modifiers": [("END", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "你学会的第一件事是低头快跑,第二件事是不要看身边倒下的人。"},
    
    {"name": "码头装卸工出身", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你从纽约港的搬运工干起。",
     "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "你知道哪些箱子值得'掉到地上一次',也知道哪些工头能用一瓶威士忌打发。"},
    
    {"name": "退役军官", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你曾经佩戴过中尉的军衔。",
     "modifiers": [("HMR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "退伍证书让你能进某些俱乐部的门,但付不起里面的酒钱。"},
    
    {"name": "禁酒令贩私酒", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你做过几趟加拿大边境的生意。",
     "modifiers": [("CRE", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "你赚了第一桶金,也赚到了几个不该认识的敌人。"},
    
    {"name": "汽车推销员", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你卖过福特T型车。",
     "modifiers": [("APP", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "你向农夫和银行家用同一套话术,而且都奏效。"},
    
    {"name": "速记打字员", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "战时妇女进入办公室,你是其中之一。",
     "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "你比老板更清楚他的生意——这是优势,也是隐患。"},
    
    {"name": "舞女出身", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你曾在百老汇的合唱团里踢腿。",
     "modifiers": [("APP", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "你的膝盖记得每一场夜戏。但你也记得每一位送花的绅士。"},
    
    {"name": "工厂领班", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你管过五十个流水线工人。",
     "modifiers": [("HMR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你既不被工人喜欢,也不被老板信任。但两边都需要你。"},
    
    {"name": "战地记者", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你给报社写过通讯。",
     "modifiers": [("INT", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "你知道哪些故事能登报,哪些只能在酒桌上讲。"},
    
    {"name": "铁路推销员", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在卧铺车厢里度过了大半人生。",
     "modifiers": [("HMR", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "从芝加哥到旧金山,每个站台你都认得搬运工。"},
    
    {"name": "退伍残废", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你少了几根手指,但学会了别的本事。",
     "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "残废金每月按时到账。你用它做了第一笔投资。"},
    
    {"name": "保险推销员", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你挨家挨户敲过门。",
     "modifiers": [("APP", "+1d1*5"), ("HMR", "+1d1*5"), ("END", "-1d2*5")],
     "narrative": "你比任何人都清楚:让人花钱预防最坏的情况,需要的不是逻辑而是表演。"},
    
    {"name": "新移民", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在埃利斯岛上岸的时间不算太久。",
     "modifiers": [("END", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "你的口音让客户起初轻视你,但也让某些同胞愿意只和你做生意。"},
    
    {"name": "退役护士", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在战地医院见过最坏的一切。",
     "modifiers": [("INT", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "经历过那些之后,商场上的尔虞我诈让你觉得几乎滑稽。"},
    
    {"name": "市井出身", "rarity": "common", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在下东区的公寓楼里长大。",
     "modifiers": [],
     "narrative": "你说四种街头黑话,认得三个区的房东,但银行家面前你依然紧张。"},

    # ============================================================
    # RARE (8个) - 总属性增益不超过 1d2
    # ============================================================
    {"name": "走私船船长", "rarity": "rare", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在朗姆酒巷上跑过私货。",
     "modifiers": [("CRE", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "海岸警卫队认得你的船,但他们也认得你给的封口费。"},
    
    {"name": "爵士酒馆老板", "rarity": "rare", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你开过一间地下酒吧。",
     "modifiers": [("HMR", "+1d2*5"), ("CRE", "+1d1*5")],
     "narrative": "市长、警长、黑帮老大都来过你的店。他们不知道彼此都是常客。"},
    
    {"name": "华尔街操盘手", "rarity": "rare", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在牛市里赚了一笔。",
     "modifiers": [("CRE", "+1d2*5"), ("INT", "+1d1*5")],
     "narrative": "钱来得快得不像真的。你心里清楚这盛宴不会永远继续——但你也不知道音乐什么时候会停。"},
    
    {"name": "阿卡姆古董商", "rarity": "rare", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你总能淘到一些带着诡异传说的旧物件。",
     "modifiers": [("INT", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "你的店面开在迷雾笼罩的街角,来往的客人多半戴着压低帽檐的软呢帽。"},
    
    {"name": "好莱坞掮客", "rarity": "rare", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在新生的电影业里拉皮条牵线。",
     "modifiers": [("APP", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "你认识三个明星,五个导演,以及他们所有人都不愿意公开的秘密。"},
    
    {"name": "退役战斗机飞行员", "rarity": "rare", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你在西线的天空中击落过敌机。",
     "modifiers": [("END", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "报纸把你写成英雄。你只记得僚机起火坠落时,飞行员朝你挥手的样子。"},
    
    {"name": "黑帮顾问", "rarity": "rare", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "某些'家族'生意上有问题会咨询你。",
     "modifiers": [("HMR", "+1d2*5"), ("INT", "+1d1*5")],
     "narrative": "你从不动手,从不出席,但每个月有一笔可观的'咨询费'存进你的账户。"},
    
    {"name": "通灵会主持", "rarity": "rare", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "战后的丧亲者愿意为一句来自彼岸的话付出一切。",
     "modifiers": [("CRE", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "你不知道你召唤的到底是不是骗局——有时候,水晶球真的会自己亮起来。"},

    # ============================================================
    # LEGENDARY (4个) - 总属性增益不超过 3d3
    # ============================================================
    {"name": "禁酒帝国之王", "rarity": "legendary", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "在某个城市,提到酒就要提到你。",
     "modifiers": [("HMR", "+2d3*5"), ("CRE", "+1d3*5")],
     "narrative": "警长在你婚礼上致辞,市长的连任靠你的钱。卡彭曾派人来谈过合作——你拒绝了,他居然没有报复。"},
    
    {"name": "迷失世代的缪斯", "rarity": "legendary", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "海明威为你写过一段,菲茨杰拉德为你写过一章。",
     "modifiers": [("APP", "+2d3*5"), ("HMR", "+1d3*5")],
     "narrative": "巴黎左岸的咖啡馆里,有三个传世之作的主角是同一个人。这件事只有你和那三位作家知道。"},
    
    {"name": "战争英雄勋章持有者", "rarity": "legendary", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "国会荣誉勋章,或维多利亚十字勋章——你拥有其中之一。",
     "modifiers": [("STR", "+2d2*5"), ("END", "+1d3*5"), ("HMR", "+1d2*5")],
     "narrative": "你不愿意谈起那一天发生的事。但每当你走进退伍军人协会,所有人都会自动起立。"},
    
    {"name": "金融大亨的私人秘书", "rarity": "legendary", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你曾经为J.P.摩根级别的人物管理过日程。",
     "modifiers": [("INT", "+2d3*5"), ("HMR", "+1d3*5")],
     "narrative": "你知道哪几位参议员收过谁的钱,哪几次股灾是被人为制造的。这些知识是你最值钱的资产——也是最危险的负担。"},

    # ============================================================
    # WILDCARD (3个)
    # ============================================================
    {"name": "黑色弥撒幸存者", "rarity": "wildcard", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你曾在某个上流社会的'仪式'上看到了不该看的东西。",
     "modifiers": [("CRE", "+1d3*5"), ("HMR", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "你逃了出来,带走了那本名册。从此每一位成员都按时给你寄钱——但你从此再也没睡过整觉。"},
    
    {"name": "神秘合伙人", "rarity": "wildcard", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你与某个从未露面的存在签订了商业合约。",
     "modifiers": [("CRE", "+1d3*5"), ("INT", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "汇款准时,建议精准,客户络绎不绝。你只在合约上见过他用红色墨水签的名字——那个名字不属于任何已知的语言。"},
    
    {"name": "凡尔赛之后的密使", "rarity": "wildcard", "mode": "Store", "scenarios": ["betweentheworlds"],
     "desc": "你曾经替某国政府传递过一份文件,改变了战后欧洲的格局。",
     "modifiers": [("INT", "+1d3*5"), ("HMR", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "你以为事情结束了。直到某天你在报纸上看到那位部长被暗杀的消息——你立刻明白,清单上下一个就是你。"},
]