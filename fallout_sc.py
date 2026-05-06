# scenario_1920s.py —— 模块化情景数据模板
# 包含：情景基础设定，以及该情景在 Normal, Intense, Store 三个模式下的专属天赋。

# ============================================================
# 1. 情景基础设定 (Scenario Definition)
# 将会被导入到 data.py 的 SCENES 列表中
# ============================================================
SCENARIO_DEF = {
    "id": "fallout",               # 唯一 ID
    "name": "末日废土",           # UI 显示的名称
    "scenario_tag": "dyingamber", # 核心 Tag！用于过滤该情景的专属天赋
    "has_edu": False,                    # 是否拥有义务教育/近代教育体系
    "desc": "这个世界正在死去，她的孩子们还活着，地铁中文明的火种依然燃烧。"
}

# ============================================================
# 2. 模式专属天赋池 (Talent Pools)
# ============================================================

# ------------------------------------------------------------
# [A] 普通模式 (Normal) 天赋
# 属性池: STR, CON, POW, DEX, APP, SIZ, INT, CRE
# ------------------------------------------------------------
TALENT_POOL_NORMAL = [
    # ============================================================
    # NEGATIVE (10个) - 总属性损失不超过 1d2
    # ============================================================
    {"name": "辐射儿", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你出生时,母亲所在的避难所刚刚发生过一次泄漏。",
     "modifiers": [("CON", "-1d2*5")],
     "narrative": "盖革计数器在你身边总是响得比别人快一些。医生说你能活到成年已经是奇迹。"},
    
    {"name": "营养不良", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "蘑菇汤和老鼠肉构成了你童年的全部。",
     "modifiers": [("SIZ", "-1d2*5")],
     "narrative": "你比同龄人矮一个头。地铁站里的医生说,这辈子也长不回来了。"},
    
    {"name": "畸变胎记", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你的脖子和手臂上有一片不寻常的色斑。",
     "modifiers": [("CON", "+1d1*5"), ("APP", "-1d3*5")],
     "narrative": "迷信的人说这是辐射的痕迹,会带来厄运。母亲教你永远穿长袖。"},
    
    {"name": "孤儿配给", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "父母在你记事前就死于一次地表任务。",
     "modifiers": [("INT", "+1d1*5"), ("CON", "-1d3*5")],
     "narrative": "孤儿院的配给比正常家庭少一半。你学会了在通风管道里偷面包,也学会了不哭。"},
    
    {"name": "听力受损", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "童年一次坍塌事故让你的右耳几乎失聪。",
     "modifiers": [("INT", "+1d1*5"), ("DEX", "-1d3*5")],
     "narrative": "黑暗中你比别人晚一秒听到怪物的脚步声——而在这个世界,一秒就是生死。"},
    
    {"name": "瘟疫幸存者", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你在那场地铁瘟疫中活了下来,但身体再也不是从前的样子。",
     "modifiers": [("CON", "-1d2*5")],
     "narrative": "整个车站只有你和另外三个孩子活了下来。你记得焚化炉烧了整整一个星期。"},
    
    {"name": "氡气童年", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你长大的那一段隧道有不该有的东西在墙缝里渗出。",
     "modifiers": [("STR", "-1d2*5")],
     "narrative": "那一段隧道现在已经被封死了。你这一辈的孩子,活下来的不到一半。"},
    
    {"name": "异变接触", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你曾在地表见过不该见的东西,从此再也不能直视黑暗。",
     "modifiers": [("DEX", "+1d1*5"), ("POW", "-1d3*5")],
     "narrative": "你睡觉时永远要留一盏灯。同伴们嘲笑你,直到他们也亲眼见过那东西。"},
    
    {"name": "派系世仇", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你出生在错误的车站,有错误的姓氏。",
     "modifiers": [("STR", "+1d1*5"), ("APP", "-1d3*5")],
     "narrative": "你六岁就学会了在邻站的徽章面前低头快走。你的脸是你父辈罪孽的活证据。"},
    
    {"name": "近视", "rarity": "negative", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "在终年昏暗的地铁里长大,你的眼睛出了问题。",
     "modifiers": [("INT", "+1d1*5"), ("DEX", "-1d3*5")],
     "narrative": "战前的眼镜是稀世珍宝。你戴的这一副镜片裂了两道,但已经让你比一半同龄人看得清楚。"},

    # ============================================================
    # COMMON (15个) - 净值零或大致平衡
    # ============================================================
    {"name": "蘑菇农工家庭", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "父母在地铁深处的菌类农场里劳作了一辈子。",
     "modifiers": [("CON", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "你的指甲缝里永远嵌着孢子,身上有一股潮湿的甜腥味。但你这一代人几乎没有挨过饿。"},
    
    {"name": "猪倌之子", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "家里养着站里仅有的几头猪。",
     "modifiers": [("STR", "+1d2*5"), ("INT", "-1d2*5")],
     "narrative": "你比谁都清楚一头猪的价值——能换一支手枪,或者一个月的子弹。"},
    
    {"name": "巡逻队学徒", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你跟着大人在隧道里巡过几次逻。",
     "modifiers": [("DEX", "+1d2*5"), ("CON", "-1d2*5")],
     "narrative": "你学会了看脚印分辨突变体的种类。这门手艺迟早会救你的命。"},
    
    {"name": "工程师之女/子", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "父母维持着车站的发电机。",
     "modifiers": [("INT", "+1d2*5"), ("STR", "-1d2*5")],
     "narrative": "你听着柴油发电机的轰鸣入睡。十岁就能独立修好一台变压器。"},
    
    {"name": "走私贩家庭", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你的家族跑黑市生意已经两代人。",
     "modifiers": [("CRE", "+1d2*5"), ("POW", "-1d2*5")],
     "narrative": "你五岁就学会了三个车站的方言,以及每一个的手势暗号。"},
    
    {"name": "前哨站长大", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你出生的地方靠近地表,听得见外面的风声。",
     "modifiers": [("CON", "+1d1*5"), ("DEX", "+1d1*5"), ("INT", "-1d2*5")],
     "narrative": "你比深处车站的孩子更早学会射击,也更早见过死亡。"},
    
    {"name": "传教士抚养", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "末日教派的修士把你养大。",
     "modifiers": [("POW", "+1d2*5"), ("CRE", "-1d2*5")],
     "narrative": "他们告诉你这个世界是被惩罚的,而你是少数被选中的。你不太相信,但那些经文你都背得下来。"},
    
    {"name": "图书馆员后代", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你家是车站里少数还保留着战前书籍的家庭。",
     "modifiers": [("INT", "+1d2*5"), ("CON", "-1d2*5")],
     "narrative": "你读过《战争与和平》——至少读过其中没被霉变吃掉的那三百页。"},
    
    {"name": "搬运工出身", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你十岁就开始扛水桶和弹药箱。",
     "modifiers": [("STR", "+1d2*5"), ("DEX", "-1d2*5")],
     "narrative": "你的肩膀宽得不像青少年,但弹奏过老吉他的手指头早就僵了。"},
    
    {"name": "医务室孩子", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你的亲人是车站里少数懂得医术的人。",
     "modifiers": [("INT", "+1d1*5"), ("DEX", "+1d1*5"), ("STR", "-1d2*5")],
     "narrative": "你认得每一种止血植物,也认得每一种骗钱的假药。"},
    
    {"name": "拾荒者血统", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "父辈靠着上地表捡破烂养活了一家人。",
     "modifiers": [("CRE", "+1d1*5"), ("DEX", "+1d1*5"), ("CON", "-1d2*5")],
     "narrative": "他们大多数没活到老。你继承了父亲的防毒面具——以及他咳嗽的方式。"},
    
    {"name": "茶馆老板之家", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你家在月台开着一间小店,听过太多故事。",
     "modifiers": [("CRE", "+1d1*5"), ("INT", "+1d1*5"), ("STR", "-1d2*5")],
     "narrative": "你认得每一个常客的脸,以及他们每一个人欠的账。"},
    
    {"name": "讲故事人传承", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "祖父辈记得世界还没死的时候。",
     "modifiers": [("CRE", "+1d2*5"), ("CON", "-1d2*5")],
     "narrative": "你听过关于'天空'和'海洋'的传说,但你不确定那些是真实的还是寓言。"},
    
    {"name": "守卫之家", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "家族世代为车站站口看门。",
     "modifiers": [("STR", "+1d1*5"), ("CON", "+1d1*5"), ("INT", "-1d2*5")],
     "narrative": "你听着子弹上膛的声音入睡。这是你听过最安心的摇篮曲。"},
    
    {"name": "普通隧道居民", "rarity": "common", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "没什么特别的,你和这个站里大多数人一样。",
     "modifiers": [],
     "narrative": "你出生,你长大,你可能死在这里——除非你决定不这样。"},

    # ============================================================
    # RARE (8个) - 总属性增益不超过 1d2
    # ============================================================
    {"name": "天生方向感", "rarity": "rare", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你在隧道里从不迷路。",
     "modifiers": [("INT", "+1d1*5"), ("DEX", "+1d1*5")],
     "narrative": "黑暗、转弯、岔道——别人会发疯的地方,你的脑子里始终有一张清晰的地图。"},
    
    {"name": "黑暗适应", "rarity": "rare", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你的眼睛在黑暗中看得比常人远。",
     "modifiers": [("DEX", "+1d2*5")],
     "narrative": "也许是隧道孩子的进化,也许只是运气。你不在乎原因。"},
    
    {"name": "辐射抗性", "rarity": "rare", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你似乎对辐射有某种天然的抵抗。",
     "modifiers": [("CON", "+1d2*5")],
     "narrative": "在别人会病倒的地方,你只是觉得有点头晕。医生想研究你,你拒绝了。"},
    
    {"name": "异常听觉", "rarity": "rare", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你能听见别人听不见的声音。",
     "modifiers": [("INT", "+1d1*5"), ("DEX", "+1d1*5")],
     "narrative": "隧道里的'低语'对你来说总是清晰一些。你不告诉别人,因为你不确定那是天赋还是诅咒。"},
    
    {"name": "稀有学者", "rarity": "rare", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "战前的某位老先生选你做了徒弟。",
     "modifiers": [("INT", "+1d2*5")],
     "narrative": "他教你读旧世界的文字,直到他咳血咳得停不下来。临终前他把那本书塞给了你。"},
    
    {"name": "天生的手", "rarity": "rare", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你修东西有种说不出的天赋。",
     "modifiers": [("DEX", "+1d2*5")],
     "narrative": "拆开任何机器,你的手指像是认得它们一样。"},
    
    {"name": "高个子", "rarity": "rare", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "在这个营养不良成为常态的世界,你长得比同龄人都高大。",
     "modifiers": [("STR", "+1d1*5"), ("SIZ", "+1d1*5")],
     "narrative": "战前的相片里,大家都和你一般高。但在这里,你站在哪儿都显眼。"},
    
    {"name": "罕见的健康", "rarity": "rare", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你似乎从来没有真正生过病。",
     "modifiers": [("CON", "+1d1*5"), ("STR", "+1d1*5")],
     "narrative": "瘟疫流行的那一年,整条隧道只有你没有发烧。母亲偷偷哭了——也许是高兴,也许是害怕。"},

    # ============================================================
    # LEGENDARY (4个) - 总属性增益不超过 3d3
    # ============================================================
    {"name": "黑色车站的最后血脉", "rarity": "legendary", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "传说中那个被诅咒的车站,你是少数活着离开的婴儿。",
     "modifiers": [("POW", "+1d3*5"), ("INT", "+1d3*5"), ("CON", "+1d3*5")],
     "narrative": "母亲临终前告诉你那个地方的真相。你的梦境里偶尔出现那些不该存在的几何形状,而你听得懂它们在说什么。"},
    
    {"name": "战前科学家后裔", "rarity": "legendary", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你的祖父是参与过那项秘密计划的科学家之一。",
     "modifiers": [("INT", "+1d3*5"), ("CRE", "+1d3*5"), ("DEX", "+1d3*5")],
     "narrative": "你继承的不仅是他的笔记本,还有他在世界毁灭前留给后代的某种忏悔——以及某种使命。"},
    
    {"name": "完美的基因", "rarity": "legendary", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "在这个畸变成为常态的世界,你的身体几乎是不真实的。",
     "modifiers": [("STR", "+1d3*5"), ("APP", "+1d3*5"), ("CON", "+1d3*5")],
     "narrative": "助产士看到你的第一眼差点跪下来。'战前的孩子',她颤抖着说。你不知道这是祝福还是诅咒。"},
    
    {"name": "神秘车站的孩子", "rarity": "legendary", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你来自地图上不存在的那个站台。",
     "modifiers": [("POW", "+1d3*5"), ("INT", "+1d3*5"), ("CRE", "+1d3*5")],
     "narrative": "母亲背着你走了三天三夜的隧道才到达现在的家。她从不告诉你来时的路,但你的梦里始终有一扇蓝色的门。"},

    # ============================================================
    # WILDCARD (3个)
    # ============================================================
    {"name": "辐射祝福", "rarity": "wildcard", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "辐射没有杀死你,反而改变了你。",
     "modifiers": [("CON", "+1d3*5"), ("STR", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "你的皮肤在某些角度会发出微弱的光。教派的人说你是被选中的,科学家想抽你的血。你只想找一个不被注视的地方。"},
    
    {"name": "异灵者", "rarity": "wildcard", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "母亲在地表分娩时,有什么东西看着她。",
     "modifiers": [("POW", "+1d3*5"), ("INT", "+1d3*5"), ("CON", "-1d3*5")],
     "narrative": "你能听见隧道深处的'东西'在说话——而它们偶尔也回应你。母亲临终前求你永远不要回应它们。你做不到。"},
    
    {"name": "末世遗孤", "rarity": "wildcard", "mode": "Normal", "scenarios": ["dyingamber"],
     "desc": "你被发现时,蜷缩在一个无人的车厢里,身边没有任何线索。",
     "modifiers": [("INT", "+1d3*5"), ("DEX", "+1d3*5"), ("POW", "-1d3*5")],
     "narrative": "没人知道你的来历,你自己也想不起来。但你会说一种没人听过的语言,而当你画画时,你画的是一座完整的、明亮的、不属于这个时代的城市。"},
]

# ------------------------------------------------------------
# [B] 极致性压抑模式 (Horny Intense) 天赋
# 属性池: STR, LIB(性欲), TEC(身材), APP, END(体力), SEN(敏感), LOV(爱情), POW(意志), CRE
# ------------------------------------------------------------
TALENT_POOL_INTENSE = [
    # ============================================================
    # NEGATIVE (8个)
    # ============================================================
    {"name": "辐射性体寒", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "童年的低剂量辐射让你的身体永远比别人凉一度。",
     "modifiers": [("END", "-1d2*5"), ("APP", "+1d1*5")],
     "narrative": "苍白的皮肤在油灯下像月光,但被人抱住时,对方总会忍不住问一句你不冷吗。"},
    
    {"name": "瘟疫后遗症", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "童年那场瘟疫在你身上留下了痕迹。",
     "modifiers": [("END", "-1d3*5"), ("SEN", "+1d1*5")],
     "narrative": "你的颈侧有一片永远褪不掉的红斑。被吻到那里时,你会比别人更轻易地颤抖。"},
    
    {"name": "饥馑成长", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "蘑菇汤喂大的身体永远长不出该有的曲线。",
     "modifiers": [("TEC", "-1d3*5"), ("APP", "+1d1*5")],
     "narrative": "锁骨太突出,胸脯太平坦,但有些人就是偏爱这种弱不禁风的样子。"},
    
    {"name": "幽闭后遗症", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "一次塌方让你再也无法忍受被压制。",
     "modifiers": [("LOV", "-1d2*5"), ("POW", "+1d1*5")],
     "narrative": "被压在身下时你会先窒息再反抗,大多数追求者都被吓退了——除了那些把这反应当作另一种乐趣的人。"},
    
    {"name": "辐射伤疤", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你的腰间和大腿内侧有一片色素沉淀。",
     "modifiers": [("APP", "-1d2*5"), ("SEN", "+1d1*5")],
     "narrative": "你从不在亮处脱衣,但黑暗里被指尖摸到那片皮肤时,你会下意识地缩起腰。"},
    
    {"name": "童年契约新娘", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你十二岁就被家里许配给了某个站长的儿子。",
     "modifiers": [("LOV", "-1d3*5"), ("APP", "+1d1*5")],
     "narrative": "婚约因为对方在一次任务中死去而作废。你松了一口气,却也再也学不会真正期待爱情。"},
    
    {"name": "营养性贫血", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你站起来太快就会眼前发黑。",
     "modifiers": [("END", "-1d3*5"), ("APP", "+1d1*5")],
     "narrative": "唇色淡得像没血,这让某些人觉得你格外需要被喂饱。"},
    
    {"name": "畸变恐惧症", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你见过太多畸变体,从此对任何不寻常的触感都会本能逃避。",
     "modifiers": [("LIB", "-1d2*5"), ("POW", "+1d1*5")],
     "narrative": "粗糙的手掌、过长的指甲、不寻常的体温——这些都会让你浑身僵硬。但温柔的、干净的接触会让你格外渴求。"},

    # ============================================================
    # COMMON (12个)
    # ============================================================
    {"name": "蘑菇农场少女", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你从小在潮湿的菌房里长大。",
     "modifiers": [("END", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你的指甲缝里总有洗不掉的孢子味。但工头家的儿子说,他就喜欢这股味道。"},
    
    {"name": "月台舞女", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你曾在车站的小酒馆里跳过舞。",
     "modifiers": [("APP", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "醉醺醺的雇佣兵塞给你的子弹够买三天的食物。你学会了怎么收下钱又不让他们碰到你——大部分时候。"},
    
    {"name": "茶馆服务员", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你在月台上的茶馆里端过茶。",
     "modifiers": [("APP", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "你听过太多男人的故事,也学会了怎么在他们手伸过界时不动声色地后退半步。"},
    
    {"name": "巡逻队员之妹", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "哥哥的战友们经常来家里吃饭。",
     "modifiers": [("LOV", "+1d1*5"), ("POW", "-1d1*5")],
     "narrative": "你看着他们一个个从男孩变成男人,也看着他们的目光从把你当妹妹变成别的东西。"},
    
    {"name": "走私贩子的女儿", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "父亲跑黑市,你跟着学会了怎么和形形色色的男人打交道。",
     "modifiers": [("POW", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "你十四岁就知道怎么用一个微笑换两发子弹的折扣,也知道怎么用一记耳光让对方明白界限。"},
    
    {"name": "传教士的养女", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "末日教派把你抚养成人,告诉你身体是污秽之物。",
     "modifiers": [("POW", "+1d2*5"), ("LIB", "-1d2*5")],
     "narrative": "你能背诵关于贞洁的所有经文。只是夜深人静时,你会偷偷思考为什么神要造一个有这种感觉的身体。"},
    
    {"name": "孤儿院出身", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你在车站孤儿院里长大,从小学会了用身体取暖。",
     "modifiers": [("END", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "拥抱对你来说是生存技巧,而不是情感表达。你区分得很清楚——清楚得让人心疼。"},
    
    {"name": "纸质书藏家", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你藏了几本战前的小说,在被子里读到深夜。",
     "modifiers": [("CRE", "+1d2*5"), ("STR", "-1d2*5")],
     "narrative": "那些写着旧世界爱情的文字让你心痒。你不知道香槟是什么味道,但你想象过无数次。"},
    
    {"name": "搬运工女儿", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "父亲的力气没遗传给你多少,但他干活的同事们都看着你长大。",
     "modifiers": [("STR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你的肩膀比同龄女孩都宽,但你的手指依然纤细。这种矛盾让某些人着迷。"},
    
    {"name": "守门员的私生女", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你的母亲是月台名妓,父亲是某个守卫——具体是哪一个,谁也说不清。",
     "modifiers": [("APP", "+1d1*5"), ("LOV", "-1d1*5")],
     "narrative": "你继承了母亲的容貌,但你发誓不会继承她的命运。至少你这么告诉自己。"},
    
    {"name": "工程师之女", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "父母在车站的发电机房工作,你从小被教导要务实。",
     "modifiers": [("POW", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你能修好一台老式步枪,但梳头时还是会偷偷照很久镜子。"},
    
    {"name": "普通隧道女孩", "rarity": "common", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你和大多数女孩一样长大。",
     "modifiers": [],
     "narrative": "你不算多漂亮,也不算多聪明。但你活到了现在——在这个世界这就是一种成就。"},

    # ============================================================
    # CORRUPTION RARE (2个)
    # ============================================================
    {"name": "末世享乐者", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "既然世界已经死了,何不痛快地活。",
     "modifiers": [("LIB", "+1d1*5"), ("APP", "+1d1*5")],
     "narrative": "你比同龄人更早学会了“今朝有酒今朝醉”的道理。明天可能塌方,可能瘟疫,那今晚就把今晚过完。"},
    
    {"name": "禁忌之书", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你偷读过教派禁止的那本战前小说。",
     "modifiers": [("LIB", "+1d2*5"), ("LOV", "-1d1*5")],
     "narrative": "书里的描写让你第一次知道身体可以那样反应。从那以后,你看每个男人的眼神都不一样了。"},

    # ============================================================
    # ADDICTION RARE (2个)
    # ============================================================
    {"name": "亲密缺失症", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "在这个谁也不敢靠近谁的世界,你格外渴望被触碰。",
     "modifiers": [("SEN", "+1d2*5")],
     "narrative": "巡逻队员擦过你肩膀的瞬间,你一整夜都睡不着。你不知道这是不是病,但你不想治。"},
    
    {"name": "吗啡甜梦", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你尝过医务室那种白色液体的滋味。",
     "modifiers": [("SEN", "+1d1*5"), ("LIB", "+1d1*5")],
     "narrative": "针管推下去的那一刻,所有的痛和冷都被另一种感觉取代。从那以后,你理解了什么叫做“被填满”。"},

    # ============================================================
    # MASOCHIST RARE (2个)
    # ============================================================
    {"name": "服从生存术", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你在派系冲突中学会了低头。",
     "modifiers": [("LOV", "+1d1*5"), ("SEN", "+1d1*5")],
     "narrative": "跪着的姿势对你来说不是耻辱,是肌肉记忆。你的身体记得这是怎么活下来的。"},
    
    {"name": "战利品幻想", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "听着哥哥们讲述抢掠故事长大,你对“被夺走”有种说不清的情结。",
     "modifiers": [("SEN", "+1d2*5"), ("POW", "-1d1*5")],
     "narrative": "你想象过无数次被反抗派系的士兵掳走的情景。羞耻让你的脸滚烫,但身体诚实得多。"},

    # ============================================================
    # SADIST RARE (2个)
    # ============================================================
    {"name": "派系小姐脾气", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你父亲是站台的头面人物,你从小习惯了别人低头。",
     "modifiers": [("POW", "+1d2*5")],
     "narrative": "你说话从不抬高音量,但车站里没人敢不听。看着男人们为你紧张,是你最早学会的快乐。"},
    
    {"name": "猎人之眼", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你跟哥哥学过怎么追踪和捕杀突变体。",
     "modifiers": [("POW", "+1d1*5"), ("STR", "+1d1*5")],
     "narrative": "你看男人的眼神和瞄准猎物时一模一样。有些人被你看得心慌——那正是你想要的。"},

    # ============================================================
    # NORMAL RARE (6个)
    # ============================================================
    {"name": "辐射祝福", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "辐射没有伤害你,反而让你的皮肤透出微光。",
     "modifiers": [("APP", "+1d2*5")],
     "narrative": "教派认为你是被选中的,但你只想要一面像样的镜子。"},
    
    {"name": "天生敏感体质", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你的神经末梢比别人密。",
     "modifiers": [("SEN", "+1d2*5")],
     "narrative": "隧道里穿堂风扫过后颈,你的腿就会发软。这种身体在这个世界生存得格外艰难。"},
    
    {"name": "意志钢铁", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "末世淬炼出了你不肯弯折的脊梁。",
     "modifiers": [("POW", "+1d2*5")],
     "narrative": "三个雇佣兵围住你那次,你的眼神没动一下。后来他们让开了——他们说你看人的样子不像猎物。"},
    
    {"name": "战前美貌", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "在这个营养不良的时代,你的容貌像从战前画报里走出来。",
     "modifiers": [("APP", "+1d2*5")],
     "narrative": "老人们看着你叹气,说你长得像他们记忆里某个不存在的明星。"},
    
    {"name": "丰盈躯体", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你的家境够好,身体长成了在这世界少见的样子。",
     "modifiers": [("TEC", "+1d2*5")],
     "narrative": "汗衫紧绷在你身上的弧线,是男人们在隧道深处也会想起的画面。"},
    
    {"name": "金币世家", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "家族的弹药存量在车站数一数二。",
     "modifiers": [("APP", "+1d1*5"), ("POW", "+1d1*5")],
     "narrative": "你不需要为子弹折腰,这让你眉宇间有一种隧道里少见的从容。许多男人就是被这从容勾住的。"},

    # ============================================================
    # LEGENDARY (3个)
    # ============================================================
    {"name": "末世女神", "rarity": "legendary", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "在这个普遍畸变的世界,你的存在本身就是一种亵渎。",
     "modifiers": [("APP", "+1d3*5"), ("TEC", "+1d2*5"), ("LIB", "+1d2*5")],
     "narrative": "助产士看到你的第一眼跪了下来。教派想把你封为圣女,派系想把你献给最高指挥官。所有人都想得到你——除了真正爱你的那个。"},
    
    {"name": "钢铁玫瑰", "rarity": "legendary", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "末世淬炼出了一个外柔内刚的灵魂。",
     "modifiers": [("POW", "+1d3*5"), ("END", "+1d2*5"), ("APP", "+1d2*5")],
     "narrative": "你能在三秒内拆装一支步枪,也能在十秒内让最铁石心肠的男人移开目光。两种能力你都用得很纯熟。"},
    
    {"name": "辐射圣女", "rarity": "legendary", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你的身体和神经被辐射重塑成了某种近乎超凡的存在。",
     "modifiers": [("SEN", "+1d3*5"), ("END", "+1d2*5"), ("APP", "+1d2*5")],
     "narrative": "你能感觉到隧道里所有的振动,听到墙后心跳的频率。当有人触碰你时,你能感觉到他每一个想法的温度——这是诅咒,也是天赋。"},

    # ============================================================
    # WILDCARD (3个)
    # ============================================================
    {"name": "黑色车站的女儿", "rarity": "wildcard", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你来自地图上不存在的那个站。",
     "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d2*5"), ("LOV", "-1d3*5"), ("POW", "-1d2*5")],
     "narrative": "母亲背着襁褓中的你穿过三天的隧道。你不知道父亲是谁,也不知道为什么你的梦里总有不属于人类的耳语——那些声音让你的身体在睡梦中潮湿。"},
    
    {"name": "末日新娘契约", "rarity": "wildcard", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你在某个仪式中被许配给了“地下的存在”。",
     "modifiers": [("SEN", "+1d3*5"), ("LIB", "+1d2*5"), ("END", "-1d3*5"), ("LOV", "-1d2*5")],
     "narrative": "教派的长老在你额头点了一滴黑色的油。从那以后你再也分不清梦境和现实,但你的皮肤记得每一次“造访”——而你害怕地发现,你开始期待那些夜晚。"},
    
    {"name": "异变血统", "rarity": "wildcard", "mode": "HorniIntense", "scenarios": ["dyingamber"],
     "desc": "你的身体里流淌着不完全是人类的东西。",
     "modifiers": [("APP", "+1d3*5"), ("END", "+1d3*5"), ("SEN", "+1d3*5"), ("LOV", "-1d3*5")],
     "narrative": "你在月经初潮那夜照镜子,瞳孔里有一闪而过的金色。你比同龄人愈合得更快,感受得更深,也更难真正爱上一个会死的人。母亲临终前对你说了一句话:“千万别让人发现”。"},
]
# ------------------------------------------------------------
# [C] 通马桶模拟器模式 (Store Mode) 天赋
# 属性池: STR, CRE, HMR(人脉), INT, APP, END
# ------------------------------------------------------------
TALENT_POOL_STORE = [
    # ============================================================
    # NEGATIVE (10个)
    # ============================================================
    {"name": "黑肺", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "多年呼吸地铁的霉气,你的肺已经不行了。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你说话之前总要先咳两声。客户们已经习惯了——这是你独特的开场白。"},
    
    {"name": "辐射病晚期", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "上一次去地表的旅程让你付出了代价。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "你头发掉了一半,但生意做得比以前更狠。你知道自己时间不多了。"},
    
    {"name": "断腿商人", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "一次塌方让你失去了一条腿,从此只能在站台里做生意。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "你不能再亲自跑货,但所有跑货的人都欠你人情。"},
    
    {"name": "被通缉的小偷", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "几个站的悬赏令上有你的脸。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你戴着的那条围巾不是装饰,是为了挡住下半张脸。"},
    
    {"name": "瘾君子", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你离不开那种地表来的白粉。",
     "modifiers": [("END", "-1d2*5"), ("CRE", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "你认识所有的供应商——因为你是他们最大的客户之一。"},
    
    {"name": "破产清算", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "上一次大单子让你彻底清空。",
     "modifiers": [("CRE", "-1d3*5")],
     "narrative": "那批货卡在了红线区。你押上了所有积蓄,而商队再也没有回来。"},
    
    {"name": "派系叛徒", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你曾经背叛过自己的车站,大家都还记得。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "你赚到了钱,失去了家。每年清明节,你都不知道该往哪个方向上香。"},
    
    {"name": "辐射性早衰", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你看起来比实际年龄老二十岁。",
     "modifiers": [("APP", "-1d3*5"), ("INT", "+1d1*5")],
     "narrative": "客户们叫你'老头/老太'。但你比他们都年轻——只是这个世界对你不太客气。"},
    
    {"name": "失语症", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "一次创伤后,你说话变得很困难。",
     "modifiers": [("APP", "-1d3*5")],
     "narrative": "你用纸条和手势谈生意。客户们最初不耐烦,后来发现你的报价从不食言。"},
    
    {"name": "畸变恐惧症", "rarity": "negative", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "童年见过的东西让你再也不敢上地表。",
     "modifiers": [("END", "-1d2*5"), ("HMR", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "你的生意全靠别人替你跑。利润分一半出去,但你能在自己的床上睡到老。"},

    # ============================================================
    # COMMON (15个)
    # ============================================================
    {"name": "前拾荒者", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你年轻时上过地表很多次。",
     "modifiers": [("STR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你的左手少了两根手指,但你认得地表大多数的路标。"},
    
    {"name": "弹壳商人", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你倒卖过子弹这种硬通货。",
     "modifiers": [("CRE", "+1d2*5"), ("HMR", "-1d2*5")],
     "narrative": "你能从子弹的声响里听出真假。这门手艺让你赚到了第一笔本钱。"},
    
    {"name": "蘑菇商贩", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你做过菌类批发的中间商。",
     "modifiers": [("HMR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "你认得三个农场的所有种植员,以及他们家里所有人的名字。"},
    
    {"name": "前巡逻队员", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你曾经为车站站岗放哨。",
     "modifiers": [("STR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "你退役时分到了一支老旧的步枪。它现在挂在你店铺的墙上,不卖。"},
    
    {"name": "隧道向导", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你曾经带商队穿过危险路段。",
     "modifiers": [("END", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你脑子里有一张活地图。但现在你更愿意坐着收过路费。"},
    
    {"name": "茶馆老板", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你开过一家小店,听过太多故事。",
     "modifiers": [("HMR", "+1d2*5"), ("STR", "-1d2*5")],
     "narrative": "你比任何记者都更清楚地铁里发生了什么——只是这里没有报纸。"},
    
    {"name": "黑市掮客", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你做过给人牵线搭桥的生意。",
     "modifiers": [("HMR", "+1d2*5"), ("APP", "-1d2*5")],
     "narrative": "你不亲自买卖,只赚中间差价。你认得每一个站的'那种人'。"},
    
    {"name": "维修匠人", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你修过的枪比别人见过的还多。",
     "modifiers": [("INT", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "客户们排队等你修枪。你慢工出细活——主要是因为你的手指现在不太灵活了。"},
    
    {"name": "二手医生", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你不是真正的医生,但你卖药。",
     "modifiers": [("INT", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你认得每一种止痛药的真假。也认得哪些是糖水兑的。"},
    
    {"name": "老兵商人", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "派系战争结束后,你转行做了生意。",
     "modifiers": [("STR", "+1d1*5"), ("HMR", "+1d1*5"), ("END", "-1d2*5")],
     "narrative": "你身上的伤疤是最好的广告——客户知道你不是软柿子。"},
    
    {"name": "讲故事人", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你用故事换饭吃,走遍了大半地铁。",
     "modifiers": [("HMR", "+1d2*5"), ("STR", "-1d2*5")],
     "narrative": "你讲一个战前的故事,可以换三天的饭和床位。"},
    
    {"name": "走私小贩", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你倒过几次封锁线两边的货。",
     "modifiers": [("CRE", "+1d1*5"), ("END", "+1d1*5"), ("APP", "-1d2*5")],
     "narrative": "你认得每一段隧道的暗道,以及每一个守卫能用什么打发。"},
    
    {"name": "搬运工出身", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你扛了二十年的箱子,现在终于自己开店。",
     "modifiers": [("STR", "+1d2*5"), ("INT", "-1d2*5")],
     "narrative": "你的脊柱已经不像年轻时那么直了,但握手时的力道依然让客户记忆犹新。"},
    
    {"name": "地下商会会员", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你交过会费,得到过一些保护。",
     "modifiers": [("HMR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "他们不是黑帮——他们坚持说自己不是。但你交的钱也不算便宜。"},
    
    {"name": "普通月台商人", "rarity": "common", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你和大多数月台商贩一样。",
     "modifiers": [],
     "narrative": "你卖你能搞到的东西,赚你能赚的钱。这就是你的生活。"},

    # ============================================================
    # RARE (8个)
    # ============================================================
    {"name": "商队队长", "rarity": "rare", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你带过商队跨越多个站台。",
     "modifiers": [("HMR", "+1d2*5"), ("CRE", "+1d1*5")],
     "narrative": "你的商队从未失踪过——这在地铁里几乎是个传说。"},
    
    {"name": "战前博物学家", "rarity": "rare", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你专门收集战前的文物和书籍。",
     "modifiers": [("INT", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "你的店铺像一座小博物馆。富人和教派都来找你买东西。"},
    
    {"name": "毒舌谈判家", "rarity": "rare", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你能从最铁公鸡身上薅下毛来。",
     "modifiers": [("APP", "+1d2*5"), ("INT", "+1d1*5")],
     "narrative": "客户们怕和你谈判,但他们还是来——因为你的货确实是最好的。"},
    
    {"name": "地表生还者", "rarity": "rare", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你曾在地表独自活了一个月,带回来了珍贵货物。",
     "modifiers": [("END", "+1d2*5"), ("STR", "+1d1*5")],
     "narrative": "没人知道你那一个月里经历了什么。你也不愿意说。但从此你的货架上总有别人搞不到的东西。"},
    
    {"name": "信誉卓著", "rarity": "rare", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "在这个谁也不信谁的世界,你的话有分量。",
     "modifiers": [("HMR", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "'XX说的'已经成了一句口头禅。你的名字本身就是担保。"},
    
    {"name": "弹药积蓄", "rarity": "rare", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你存下了相当数量的子弹。",
     "modifiers": [("CRE", "+1d2*5"), ("END", "+1d1*5")],
     "narrative": "你的金库不在银行——这里也没有银行。你的金库在墙缝、在床下、在三个不同的藏身处。"},
    
    {"name": "派系交叉中介", "rarity": "rare", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你能同时和几个敌对派系做生意。",
     "modifiers": [("HMR", "+1d2*5"), ("INT", "+1d1*5")],
     "narrative": "红线和汉萨都欢迎你的商队进入。这是少数人才有的特权。"},
    
    {"name": "突变体猎人", "rarity": "rare", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你做过几次猎杀异变生物的生意。",
     "modifiers": [("STR", "+1d2*5"), ("END", "+1d1*5")],
     "narrative": "你出售的'怪物牙齿'项链都是真品。每一颗都来自你亲手猎杀的东西。"},

    # ============================================================
    # LEGENDARY (4个)
    # ============================================================
    {"name": "汉萨同盟商人", "rarity": "legendary", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你拥有汉萨同盟的正式商人身份。",
     "modifiers": [("HMR", "+2d3*5"), ("CRE", "+1d3*5")],
     "narrative": "环线上的每一个站都对你开放。你的话甚至能影响某些站的政策——只要你愿意付出代价。"},
    
    {"name": "传说中的老商人", "rarity": "legendary", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "整条地铁的孩子都听过关于你的故事。",
     "modifiers": [("HMR", "+2d3*5"), ("INT", "+1d3*5")],
     "narrative": "据说你曾经一个人徒步穿越了红线区。据说你认识所有车站的站长。据说你有一支战前的录音。这些故事大部分是真的。"},
    
    {"name": "战前货仓持有者", "rarity": "legendary", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你发现了一个未被发掘的战前仓库。",
     "modifiers": [("CRE", "+2d3*5"), ("INT", "+1d3*5")],
     "narrative": "那个仓库的位置只有你知道。每隔几个月你去取一些货,谨慎地不让任何人跟踪你。这是你最大的秘密——也是最危险的。"},
    
    {"name": "钢铁意志的幸存者", "rarity": "legendary", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你死里逃生的次数超过了大多数人尝过苹果的次数。",
     "modifiers": [("STR", "+2d2*5"), ("END", "+1d3*5"), ("HMR", "+1d2*5")],
     "narrative": "辐射、突变体、派系战争、瘟疫——你都从中走了出来。客户们认为你是被神保佑的,你认为自己只是运气太好——好得有些诡异。"},

    # ============================================================
    # WILDCARD (3个)
    # ============================================================
    {"name": "黑市占卜师", "rarity": "wildcard", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你卖的不是货物,是关于未来的'预言'。",
     "modifiers": [("CRE", "+1d3*5"), ("HMR", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "你的预言准确率高得不正常。教派想烧死你,派系领袖想雇佣你。你只是想安静地做生意——但每说出一个预言,你都觉得身体里有什么东西在被掏空。"},
    
    {"name": "不该存在的中间人", "rarity": "wildcard", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你和地铁深处的'某些东西'达成了贸易协议。",
     "modifiers": [("CRE", "+1d3*5"), ("INT", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "你拿出的某些货物没人能解释来源。你不告诉任何人交换的代价是什么——但你的影子在某些光线下,看起来不太对劲。"},
    
    {"name": "被记住的名字", "rarity": "wildcard", "mode": "Store", "scenarios": ["dyingamber"],
     "desc": "你曾经做过一件事,改变了某个站台的命运。",
     "modifiers": [("HMR", "+1d3*5"), ("APP", "+1d3*5"), ("CRE", "-1d3*5")],
     "narrative": "有人为你立了雕像,有人发誓要杀了你。你拒绝在任何一边表态,继续做你的生意——但每一笔交易背后都跟着无形的目光。"},
]