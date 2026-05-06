# scenario_1920s.py —— 模块化情景数据模板
# 包含：情景基础设定，以及该情景在 Normal, Intense, Store 三个模式下的专属天赋。

# ============================================================
# 1. 情景基础设定 (Scenario Definition)
# 将会被导入到 data.py 的 SCENES 列表中
# ============================================================
SCENARIO_DEF = {
    "id": "1920s_cn",               # 唯一 ID
    "name": "传奇一代(CN)",           # UI 显示的名称
    "scenario_tag": "distantshore", # 核心 Tag！用于过滤该情景的专属天赋
    "has_edu": False,                    # 是否拥有义务教育/近代教育体系
    "desc": "北洋时代。军阀；革命党；戴着眼镜的洋学生；求神拜佛的农民。"
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
    {
        "name": "鸦片家族",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你家三代人都倒在烟榻上。",
        "modifiers": [("CON", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
        "narrative": "祖父抽掉了田,父亲抽掉了房子,你出生时家里只剩下烟枪和债主。"
    },
    {
        "name": "饥荒幸存者",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "民国初年的几场大饥荒,你家死了一半人。",
        "modifiers": [("SIZ", "-1d2*5"), ("CON", "-1d1*5"), ("CRE", "+1d1*5")],
        "narrative": "你六岁那年吃过观音土。哥哥姐姐没能挺过去,你不知道为什么自己活了下来。"
    },
    {
        "name": "革命党遗孤",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "父亲在某次起义中被枭首示众,母亲带你东躲西藏。",
        "modifiers": [("POW", "+1d1*5"), ("CON", "-1d3*5")],
        "narrative": "你从小就知道'清算'两个字怎么写。母亲的眼睛永远盯着门外。"
    },
    {
        "name": "梅毒之家",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你父亲在外面染了脏病,殃及全家。",
        "modifiers": [("APP", "-1d2*5"), ("CON", "-1d1*5"), ("INT", "+1d1*5")],
        "narrative": "母亲临终前还在咒骂那些勾引父亲的女人。但你早就明白,真正该骂的是谁。"
    },
    {
        "name": "兵荒马乱",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "军阀混战时,你家的村子被洗劫了三遍。",
        "modifiers": [("DEX", "+1d1*5"), ("CON", "-1d3*5")],
        "narrative": "你学会了听马蹄声辨别是哪支队伍——直军、奉军、还是土匪,反应慢一拍就是命。"
    },
    {
        "name": "破落旗人",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "辛亥之后,皇粮断了,家族再也没缓过来。",
        "modifiers": [("APP", "+1d1*5"), ("STR", "-1d3*5")],
        "narrative": "你穿着改小的旧袍子,坐在卖光了家具的空屋里,听祖母讲'当年'。"
    },
    {
        "name": "教案遗孤",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "义和团运动期间,你家因信教被同乡屠杀。",
        "modifiers": [("INT", "+1d1*5"), ("POW", "-1d3*5")],
        "narrative": "传教士把你从血泊中带走。你至今分不清,该恨那些挥刀的乡亲,还是恨那本让你成为异类的圣经。"
    },
    {
        "name": "瘟疫烙印",
        "rarity": "negative",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "1918年的大流感席卷东北,你脸上至今留着印记。",
        "modifiers": [("APP", "-1d3*5"), ("CON", "+1d1*5")],
        "narrative": "麻坑遍布的脸让媒婆望而却步,但活下来本身已经是一种胜利。"
    },

    # ============================================================
    # COMMON (15个) - 净值零或大致平衡
    # ============================================================
    {
        "name": "私塾出身",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你从小跟着村里的老秀才念《论语》。",
        "modifiers": [("INT", "+1d2*5"), ("CRE", "-1d2*5")],
        "narrative": "你能背《孟子》全本,但老师说'子曰'之外的一切都是邪说。"
    },
    {
        "name": "教会学校",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "传教士开办的学堂里,你接触到了另一个世界。",
        "modifiers": [("INT", "+1d1*5"), ("APP", "+1d1*5"), ("CON", "-1d2*5")],
        "narrative": "你能用英文背圣经,也能用中文写八股,但两边都不把你当自己人。"
    },
    {
        "name": "佃农之子",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "祖辈替地主种了三代田。",
        "modifiers": [("CON", "+1d2*5"), ("INT", "-1d2*5")],
        "narrative": "你认得每一种庄稼,但不认得自己的名字怎么写。"
    },
    {
        "name": "茶馆跑堂",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你从小在茶馆里端壶送水,听遍了天下事。",
        "modifiers": [("DEX", "+1d2*5"), ("STR", "-1d2*5")],
        "narrative": "袁世凯称帝、张勋复辟、五四学潮——你都是从茶客嘴里第一手听来的。"
    },
    {
        "name": "戏班学徒",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你从小被卖到戏班子里,挨打吊嗓子。",
        "modifiers": [("APP", "+1d2*5"), ("POW", "-1d2*5")],
        "narrative": "师父说'打出来的角儿'。你的扮相确实漂亮——代价是脊背上那些再也消不掉的印子。"
    },
    {
        "name": "买办家庭",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "父亲在洋行里给英国人当差。",
        "modifiers": [("INT", "+1d2*5"), ("STR", "-1d2*5")],
        "narrative": "你穿西装吃西餐,但走在街上,左边骂你'假洋鬼子',右边骂你'东亚病夫'。"
    },
    {
        "name": "土郎中之子",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "父亲背着药箱走街串巷。",
        "modifiers": [("INT", "+1d1*5"), ("DEX", "+1d1*5"), ("APP", "-1d2*5")],
        "narrative": "你十岁就能辨认百种草药。父亲说,西医那一套不过是哄洋鬼子的把戏。"
    },
    {
        "name": "船家子弟",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你家的船在长江上漂了三代。",
        "modifiers": [("STR", "+1d2*5"), ("INT", "-1d2*5")],
        "narrative": "你不识字,但你能凭水声判断暗礁的方位。"
    },
    {
        "name": "镖局学徒",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你跟着镖头走过北方的官道。",
        "modifiers": [("STR", "+1d2*5"), ("CRE", "-1d2*5")],
        "narrative": "你会几招拳脚,认得绿林黑话。可惜火车通了之后,这门手艺已经不太值钱了。"
    },
    {
        "name": "缝纫工",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "上海的纱厂里,你十二岁就开始踩缝纫机。",
        "modifiers": [("DEX", "+1d2*5"), ("CON", "-1d2*5")],
        "narrative": "工头的鞭子打在背上,机器的针扎在指尖。你学会了在所有疼痛之上继续干活。"
    },
    {
        "name": "学堂新生",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你赶上了新式学堂的第一批。",
        "modifiers": [("INT", "+1d2*5"), ("POW", "-1d2*5")],
        "narrative": "数学、地理、博物——这些新词让你头疼,但比起背《三字经》总是有趣些。"
    },
    {
        "name": "厨师之家",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你家是城里有名的馆子。",
        "modifiers": [("DEX", "+1d1*5"), ("APP", "+1d1*5"), ("STR", "-1d2*5")],
        "narrative": "你尝得出师父汤里少放了几粒花椒,但你父亲希望你别走他的老路。"
    },
    {
        "name": "码头脚夫",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你十三岁就在天津港扛麻袋。",
        "modifiers": [("STR", "+1d2*5"), ("APP", "-1d2*5")],
        "narrative": "你的肩膀比同龄人厚实,但每天回到家,母亲都要给你擦上跌打药酒。"
    },
    {
        "name": "庙祝之子",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你在香火缭绕中长大。",
        "modifiers": [("POW", "+1d2*5"), ("INT", "-1d2*5")],
        "narrative": "你认得每一尊神的来历,但你也偶尔怀疑——这些泥塑木雕真的听得见祈祷吗?"
    },
    {
        "name": "私塾先生之后",
        "rarity": "common",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "父亲是个不得志的老秀才,把希望寄托在你身上。",
        "modifiers": [("INT", "+1d1*5"), ("CRE", "+1d1*5"), ("CON", "-1d2*5")],
        "narrative": "他偷偷教你读书写字,但每当媒婆上门,他又叮嘱你藏起所有的笔。"
    },

    # ============================================================
    # RARE (8个) - 总属性增益不超过 1d2
    # ============================================================
    {
        "name": "海归留学生家庭",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "父亲是庚款留美的第一批。",
        "modifiers": [("INT", "+1d2*5")],
        "narrative": "家里的书架上一半是康德,一半是朱熹。你从小听着两种语言争吵长大。"
    },
    {
        "name": "武术世家",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "祖传的功夫在你身上得到了延续。",
        "modifiers": [("STR", "+1d1*5"), ("DEX", "+1d1*5")],
        "narrative": "祖父打过义和团,父亲守过擂台。如今洋枪已经普及,但你父亲说,功夫还有功夫的用处。"
    },
    {
        "name": "京剧名伶之后",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你的母亲是京城里有名的角儿。",
        "modifiers": [("APP", "+1d2*5")],
        "narrative": "你继承了她的相貌,也继承了她身上那种说不清的、让人移不开眼的东西。"
    },
    {
        "name": "革命党新血",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你的家族是同盟会的元老。",
        "modifiers": [("POW", "+1d1*5"), ("INT", "+1d1*5")],
        "narrative": "孙先生来过你家吃饭。父亲让你管他叫'孙叔叔'。"
    },
    {
        "name": "天生神童",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你三岁识字,五岁能诗。",
        "modifiers": [("INT", "+1d2*5")],
        "narrative": "私塾先生说你是文曲星下凡。父亲既骄傲又担忧——这个时代,神童的命未必好。"
    },
    {
        "name": "蒙古王公血脉",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你的母亲来自内蒙古的王府。",
        "modifiers": [("STR", "+1d1*5"), ("CON", "+1d1*5")],
        "narrative": "你身上流着草原的血。每年夏天,你会被送回外祖父家学骑马射箭。"
    },
    {
        "name": "巨贾之家",
        "rarity": "rare",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "祖父是晋商票号的大掌柜。",
        "modifiers": [("INT", "+1d1*5"), ("APP", "+1d1*5")],
        "narrative": "钱庄虽然在民国新银行的冲击下日渐衰落,但家底还在。你从小见惯了银票流水。"
    },

    # ============================================================
    # LEGENDARY (4个) - 总属性增益不超过 3d3
    # ============================================================
    {
        "name": "末代皇家",
        "rarity": "legendary",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你是某位铁帽子王的子女,大清亡了,但血脉还在。",
        "modifiers": [("APP", "+1d3*5"), ("INT", "+1d3*5"), ("POW", "+1d3*5")],
        "narrative": "父亲把家里的玉器一件件当掉,只为让你继续上贵族学堂。他说,身段不能塌。"
    },
    {
        "name": "军阀私生女",
        "rarity": "legendary",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你的生父手握一省兵权,但他不能公开承认你。",
        "modifiers": [("APP", "+1d3*5"), ("CON", "+1d3*5"), ("STR", "+1d3*5")],
        "narrative": "每月都有便衣来送钱送物,但'父亲'两个字你只在睡梦中喊过。母亲说,这样反而是保护——他正房太太死了好几个对手了。"
    },
    {
        "name": "天人之姿",
        "rarity": "legendary",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你出生时,接生婆说她接生四十年没见过这样的孩子。",
        "modifiers": [("APP", "+1d3*5"), ("DEX", "+1d3*5"), ("CRE", "+1d3*5")],
        "narrative": "村里的算命先生说你是'倾国之相',要么大富大贵,要么红/蓝颜薄命。母亲哭了三天,既怕也喜。"
    },
    {
        "name": "南洋华侨富商之后",
        "rarity": "legendary",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "祖父在新加坡发家,你是回国寻根的那一支。",
        "modifiers": [("INT", "+1d3*5"), ("APP", "+1d3*5"), ("CON", "+1d3*5")],
        "narrative": "你说话夹着马来语和闽南话。家族在槟城有橡胶园,在上海有洋行,在广州有学校——但回到祖籍村里,你还是要给祠堂磕头。"
    },

    # ============================================================
    # WILDCARD (3个) - 大喜大悲
    # ============================================================
    {
        "name": "白莲教遗脉",
        "rarity": "wildcard",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你的家族世代守护着一个被官府剿了三百年的秘密。",
        "modifiers": [("POW", "+1d3*5"), ("CRE", "+1d3*5"), ("CON", "-1d3*5")],
        "narrative": "祖母在你十二岁那年让你跪在祖宗牌位前,告诉你那本黄绫包着的经书的来历。从那以后,你偶尔会做一些不属于这个时代的梦——梦里有红巾,有刀光,有一个反复呼唤你某个陌生名字的声音。"
    },
    {
        "name": "湘西赶尸人之后",
        "rarity": "wildcard",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "祖父曾经是湘西山里那行当的一员。",
        "modifiers": [("POW", "+1d3*5"), ("DEX", "+1d3*5"), ("APP", "-1d3*5")],
        "narrative": "祖父临终前传给你一个铜铃和一本符书。他说不到万不得已,千万别摇那个铃——因为它会唤醒的,不只是死人。"
    },
    {
        "name": "义和团之子",
        "rarity": "wildcard",
        "mode": "Normal",
        "scenarios": ["distantshore"],
        "desc": "你父亲曾是大师兄,自称刀枪不入。八国联军来时,他活了下来——但带回来的不只是他自己。",
        "modifiers": [("STR", "+1d3*5"), ("CON", "+1d3*5"), ("INT", "-1d3*5")],
        "narrative": "父亲身上有一道枪伤,从胸口穿到背后,但他活了。他说是关老爷附体救了他。每年农历五月,他会把你关进祠堂三天三夜——他说你也'有那个根器'。"
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
    {"name": "礼教束缚", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "'男女授受不亲'的训诫从小刻在你骨子里。",
     "modifiers": [("LIB", "-1d2*5"), ("SEN", "-1d1*5"), ("POW", "+1d1*5")],
     "narrative": "新派的同学说要'恋爱自由',你嘴上附和,但心里那道墙怎么也拆不掉。"},
    
    {"name": "脏病阴影", "rarity": "negative", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "西医还不普及的年代,有些病一沾上就是一辈子。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("POW", "+1d1*5")],
     "narrative": "你见过太多花柳巷里出来的人最后的下场。每一次心动之前,你都先想起那些。"},

    # ============================================================
    # COMMON (4个)
    # ============================================================
    {"name": "新派学生", "rarity": "common", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "你读过《新青年》,信奉'恋爱自由'。",
     "modifiers": [("APP", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "你拒绝父母安排的婚事。你要找的是灵魂的伴侣——可灵魂这东西,在这个年代太奢侈了。"},
    
    {"name": "戏班子出身", "rarity": "common", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "从小练功练出来的身段,在台上台下都有人盯着看。",
     "modifiers": [("TEC", "+1d2*5"), ("POW", "-1d2*5")],
     "narrative": "捧角儿的人送来的金条比米还多。你笑着收下,心里清楚这些人爱的是戏服里的影子。"},
    
    {"name": "舞场常客", "rarity": "common", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "上海百乐门、天津利顺德——你都是熟客。",
     "modifiers": [("END", "+1d1*5"), ("APP", "+1d1*5"), ("LOV", "-1d2*5")],
     "narrative": "爵士乐响起的时候,你属于舞池里所有的舞伴。下了场,你又谁都不属于。"},
    
    {"name": "旧式婚约", "rarity": "common", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "父母包办的那门亲事压在你头顶,从未真正实现也从未取消。",
     "modifiers": [("SEN", "+1d2*5"), ("LOV", "-1d2*5")],
     "narrative": "你和那个素未谋面的'未婚配偶'谁都没见过谁,但所有越界的关系都因此带着一层禁忌的滋味。"},

    # ============================================================
    # RARE (2个)
    # ============================================================
    {"name": "上海滩名角", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "你的相片登过《良友》画报。",
     "modifiers": [("APP", "+1d2*5"), ("TEC", "+1d1*5")],
     "narrative": "走在霞飞路上,认得你的人比你认得的多。这种眼光既让你飘飘然,也让你疲惫。"},
    
    {"name": "湘西巫蛊余脉", "rarity": "rare", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "祖母传下来的本事,据说能让人神魂颠倒。",
     "modifiers": [("LIB", "+1d2*5"), ("SEN", "+1d1*5")],
     "narrative": "你不全信那些古老的说法,但每当你看着想要的人时,对方眼神里那种迷离,你也说不清是巧合还是别的。"},

    # ============================================================
    # LEGENDARY (1个)
    # ============================================================
    {"name": "十里洋场交际花", "rarity": "legendary", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "上海滩的舞场、画报、传闻里,都有你的影子。",
     "modifiers": [("APP", "+2d3*5"), ("LIB", "+1d2*5"), ("CRE", "+1d2*5")],
     "narrative": "军阀给你包了别墅,洋行老板给你送了汽车,留学归来的诗人为你写过诗集。你的名字出现在同一份小报的社会版和警察局档案里。每个城里的男人女人都听过你的故事——只是版本各不相同。"},

    # ============================================================
    # WILDCARD (1个)
    # ============================================================
    {"name": "狐仙转世", "rarity": "wildcard", "mode": "HorniIntense", "scenarios": ["distantshore"],
     "desc": "村里的老人在你出生时就说,这孩子来历不一般。",
     "modifiers": [("APP", "+1d3*5"), ("LIB", "+1d3*5"), ("LOV", "-1d3*5")],
     "narrative": "你的眼神能让人发怔,你的笑能让人忘了自己姓什么。但凡是真心爱上你的人,最后都没什么好下场——也许那些老人说的不全是迷信。"},
]

# ------------------------------------------------------------
# [C] 通马桶模拟器模式 (Store Mode) 天赋
# 属性池: STR, CRE, HMR(人脉), INT, APP, END
# ------------------------------------------------------------
TALENT_POOL_STORE = [
    # ============================================================
    # NEGATIVE (10个) - 总属性损失不超过 1d2
    # ============================================================
    {"name": "鸦片瘾", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "应酬场上沾染的烟瘾再也戒不掉了。",
     "modifiers": [("END", "-1d2*5"), ("CRE", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "你和客户能在烟榻上谈成大单子。代价是每天少不了那两口。"},
    
    {"name": "通缉在身", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "某省督军的衙门里挂着你的画像。",
     "modifiers": [("HMR", "-1d2*5"), ("APP", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你不能再回那个省了。但江湖大,机会也大,你换了名字接着干。"},
    
    {"name": "旧伤复发", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "走镖时挨过的那一刀,阴雨天就疼得睡不着。",
     "modifiers": [("END", "-1d2*5"), ("STR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "年轻时不当回事,如今才知道身体记着每一笔账。"},
    
    {"name": "票号倒账", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你存银子的票号倒了,半生积蓄打了水漂。",
     "modifiers": [("CRE", "-1d2*5"), ("HMR", "-1d1*5"), ("END", "+1d1*5")],
     "narrative": "你跑去山西要说法,只看到关着大门的空院子。从那以后你只信现银和黄金。"},
    
    {"name": "脏病暗伤", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "年轻时不知节制,如今身子骨垮了。",
     "modifiers": [("END", "-1d2*5"), ("APP", "-1d1*5"), ("CRE", "+1d1*5")],
     "narrative": "中医西医都看过,药包堆了一柜子。你学会了在客人面前掩饰咳嗽。"},
    
    {"name": "黑社会债务", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你欠了青帮的人情,这种债比银子的更难还。",
     "modifiers": [("CRE", "-1d2*5"), ("END", "-1d1*5"), ("HMR", "+1d1*5")],
     "narrative": "杜先生没派人催过你。但你知道,该还的时候你必须还,而且不会是用钱。"},
    
    {"name": "败家恶名", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你年轻时把祖产挥霍了大半,这事街坊都知道。",
     "modifiers": [("APP", "-1d2*5"), ("HMR", "-1d1*5"), ("INT", "+1d1*5")],
     "narrative": "你后来重新爬起来了,但同行酒桌上还是会拿这事打趣。你只能陪着笑。"},
    
    {"name": "结巴", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "谈、谈生意时,舌头总是跟、跟不上脑子。",
     "modifiers": [("APP", "-1d3*5"), ("INT", "+1d1*5")],
     "narrative": "你学会了少说多写,合同条款比谁都看得仔细。"},
    
    {"name": "兵灾余生", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你的铺子被乱兵烧过一次,你从灰烬里重新爬起来。",
     "modifiers": [("CRE", "-1d2*5"), ("END", "-1d1*5"), ("POW", "+1d1*5")],
     "narrative": "你现在最关心的不是利润,是哪条路能跑得快,哪个码头能上船。"},
    
    {"name": "赌坊常客", "rarity": "negative", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "牌九桌上输掉的银子,够再开一间铺子。",
     "modifiers": [("CRE", "-1d3*5")],
     "narrative": "你每次都发誓是最后一次。每次。"},

    # ============================================================
    # COMMON (15个) - 净值零或大致平衡
    # ============================================================
    {"name": "钱庄学徒出身", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你十二岁就进了钱庄当学徒。",
     "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "你能用算盘打出比钟表还准的数字。代价是再也长不结实的肩膀。"},
    
    {"name": "走镖出身", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你年轻时跟过镖局,押过银两走过官道。",
     "modifiers": [("STR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你认得绿林暗号,挨过土匪的刀。如今火车通了,你也改行了,但身上的疤还在。"},
    
    {"name": "买办经验", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在洋行里给红毛子跑过腿。",
     "modifiers": [("HMR", "+1d2*5"), ("STR", "-1d2*5")],
     "narrative": "你认得几个洋人,会几句洋话。同行说你是'假洋鬼子',但他们做不成的生意要找你。"},
    
    {"name": "茶馆常客", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你每天泡茶馆,消息比官府还灵通。",
     "modifiers": [("HMR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "你没攒下多少钱,但你知道这城里谁家儿子要娶亲,谁家铺子要倒。"},
    
    {"name": "码头帮手", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在天津、上海或汉口的码头上摸爬滚打过。",
     "modifiers": [("STR", "+1d1*5"), ("INT", "-1d1*5")],
     "narrative": "你认得每个码头的把头,知道哪些货色不能见光。"},
    
    {"name": "商会子弟", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "父辈在本地商会里有点位置。",
     "modifiers": [("HMR", "+1d2*5"), ("END", "-1d2*5")],
     "narrative": "你从小见惯了应酬场面。但你也明白,这层关系既是助力,也是绳索。"},
    
    {"name": "走江湖", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你年轻时跑遍了大半个中国。",
     "modifiers": [("INT", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "你能听懂七八种方言,吃过别人想都没想过的东西。"},
    
    {"name": "戏园子常客", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在戏班子的圈子里混得脸熟。",
     "modifiers": [("APP", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "捧角儿花了你不少钱,但也让你结识了一批爱看戏的官员和富商。"},
    
    {"name": "勤俭持家", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你过日子精打细算,一文钱掰成两半花。",
     "modifiers": [("CRE", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你的长衫穿了五年,但银柜里的存货比邻铺多三倍。"},
    
    {"name": "粗通文墨", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你读过几年私塾,能写信看合同。",
     "modifiers": [("INT", "+1d1*5"), ("STR", "-1d1*5")],
     "narrative": "在这个文盲遍地的年代,会写字本身就是一种本钱。"},
    
    {"name": "乡下出身", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你从田埂上走进城里,什么苦都吃过。",
     "modifiers": [("END", "+1d2*5"), ("INT", "-1d2*5")],
     "narrative": "你不识几个字,但你扛得住别人扛不住的活。"},
    
    {"name": "老好人", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你脾气好,街坊邻里都愿意帮衬你。",
     "modifiers": [("HMR", "+1d1*5"), ("CRE", "-1d1*5")],
     "narrative": "你借出去的钱常常收不回来,但需要帮忙时大家也会想到你。"},
    
    {"name": "袍哥兄弟", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在川渝一带的袍哥会里挂过名。",
     "modifiers": [("HMR", "+1d1*5"), ("APP", "-1d1*5")],
     "narrative": "你不是什么大爷,但'仁义礼智信'这五堂的暗语你都懂。"},
    
    {"name": "平凡商户", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "祖辈三代守着一间小铺子。",
     "modifiers": [],
     "narrative": "你既没大起也没大落。在这个乱世,这本身就是一种本事。"},
    
    {"name": "见过世面", "rarity": "common", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在上海或天津的洋场住过几年。",
     "modifiers": [("APP", "+1d1*5"), ("END", "-1d1*5")],
     "narrative": "电灯、电车、咖啡馆——你都习以为常。但回到内地,你也得换上长衫装作什么都没见过。"},

    # ============================================================
    # RARE (8个) - 总属性增益不超过 1d2
    # ============================================================
    {"name": "晋商票号背景", "rarity": "rare", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你曾在山西票号里干过几年。",
     "modifiers": [("CRE", "+1d2*5"), ("INT", "+1d1*5")],
     "narrative": "票号虽然在新银行的冲击下衰落了,但你从大掌柜那里学到的本事——汇兑、风控、识人——在哪个朝代都用得上。"},
    
    {"name": "洋行通译", "rarity": "rare", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你给英商或日商当过翻译。",
     "modifiers": [("INT", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "你是华洋之间唯一的桥梁。两边都需要你,两边也都防着你。"},
    
    {"name": "青帮记名弟子", "rarity": "rare", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在上海拜过码头,递过帖子。",
     "modifiers": [("HMR", "+1d2*5"), ("STR", "+1d1*5")],
     "narrative": "你不是核心人物,但你的名帖能在某些场合换来必要的礼遇。"},
    
    {"name": "走南闯北", "rarity": "rare", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你的脚印从哈尔滨到广州,从上海到兰州。",
     "modifiers": [("INT", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "每个商埠你都认得几个老朋友。这张人脉网比任何银票都值钱。"},
    
    {"name": "海归新派商人", "rarity": "rare", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在日本或南洋待过几年,见识过新式经营。",
     "modifiers": [("INT", "+1d2*5"), ("APP", "+1d1*5")],
     "narrative": "你穿西装,用账本,讲'股份公司'。老一辈说你忘本,年轻人却挤着进你的店。"},
    
    {"name": "军阀供应商", "rarity": "rare", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你给某位督军做过粮草、被服或更敏感的生意。",
     "modifiers": [("CRE", "+1d2*5"), ("HMR", "+1d1*5")],
     "narrative": "钱来得快,风险也大。督军换了,你也得跟着换靠山。"},
    
    {"name": "硬底子身手", "rarity": "rare", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你练过家传的功夫,自卫绰绰有余。",
     "modifiers": [("STR", "+1d2*5"), ("END", "+1d1*5")],
     "narrative": "在这个出门要带枪的年代,一身真功夫比镖师都靠谱。"},
    
    {"name": "古玩眼力", "rarity": "rare", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你过手过的古董成百上千件。",
     "modifiers": [("INT", "+1d2*5"), ("CRE", "+1d1*5")],
     "narrative": "清室散佚的宝贝、洋人收购的瓷器——你看一眼就知道几钱几两。"},

    # ============================================================
    # LEGENDARY (4个) - 总属性增益不超过 3d3
    # ============================================================
    {"name": "南北通吃的掮客", "rarity": "legendary", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在直系、奉系、皖系都有线人。",
     "modifiers": [("HMR", "+2d3*5"), ("INT", "+1d3*5")],
     "narrative": "军阀打仗你做生意。今天给这边送军火,明天给那边卖情报——你的本事是让所有人都觉得你是自己人。"},
    
    {"name": "十里洋场名商", "rarity": "legendary", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你在上海滩有头有脸,租界巡捕房和华界商会都给面子。",
     "modifiers": [("CRE", "+2d3*5"), ("HMR", "+1d2*5"), ("APP", "+1d2*5")],
     "narrative": "你在外滩有写字楼,在霞飞路有公馆。报纸把你和黄金荣、杜月笙的名字放在一起——尽管你做的生意比他们体面得多。"},
    
    {"name": "南洋归侨巨贾", "rarity": "legendary", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你的家族在新加坡或槟城积累了三代财富,你回国主持中国分号。",
     "modifiers": [("CRE", "+2d3*5"), ("INT", "+1d3*5")],
     "narrative": "你的橡胶园在马来亚,洋行在香港,新办的银行在上海。无论哪个军阀上台,他们都得对你客客气气。"},
    
    {"name": "江湖泰斗", "rarity": "legendary", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你年轻时一身武艺名震江湖,如今做生意,老朋友遍及九州。",
     "modifiers": [("STR", "+2d2*5"), ("END", "+1d2*5"), ("HMR", "+1d2*5")],
     "narrative": "提起你的名号,从关外的胡子到江南的青帮,都要给三分薄面。这不是钱能买来的。"},

    # ============================================================
    # WILDCARD (3个)
    # ============================================================
    {"name": "前清遗老的关系户", "rarity": "wildcard", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你和几位住在天津租界里的清朝旧臣有生意往来。",
     "modifiers": [("CRE", "+1d3*5"), ("INT", "+1d3*5"), ("HMR", "-1d3*5")],
     "narrative": "他们手里还有些紫禁城带出来的好东西,你帮他们悄悄变现。但这件事一旦传出去,革命党、新贵、洋人——三方面都会找你的麻烦。"},
    
    {"name": "走私大宗家", "rarity": "wildcard", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你的真正生意从来不在账本上——鸦片、军火、或者更难形容的东西。",
     "modifiers": [("CRE", "+1d3*5"), ("HMR", "+1d3*5"), ("END", "-1d3*5")],
     "narrative": "你睡觉时枕头底下有枪,出门时身边有保镖。你赚的钱十辈子也花不完——前提是你能活到下辈子。"},
    
    {"name": "秘密会党的钱袋子", "rarity": "wildcard", "mode": "Store", "scenarios": ["distantshore"],
     "desc": "你为某个不能明说的组织管理着一部分资金。",
     "modifiers": [("INT", "+1d3*5"), ("HMR", "+1d3*5"), ("APP", "-1d3*5")],
     "narrative": "也许是革命党的军费,也许是哥老会的堂费,也许是某个更古老更隐秘的传承。每月有人来取走他们该取的那份,从不问你的近况——但他们知道你家每个孩子的名字。"},
]