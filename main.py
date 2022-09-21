from datetime import date, datetime,timedelta
import zhdate
import math
import time
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import configparser,os
import random
import requests
import time
from bs4 import BeautifulSoup
"""
1、从配置文件中获取变量
"""
conf=configparser.ConfigParser()
config_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf.read('config.conf','utf8')
today = datetime.now()+timedelta(hours=8)+timedelta(hours=8)
start_date =conf.get("info", "start_date")#在一起开始日期,格式 ****-**-**
city1 = conf.get("info", "city1")              #所在的城市(请写具体城市，如昆明)，用于匹配天气预报和热点新闻
city2 = conf.get("info", "city2")
birthday_lover = conf.get("info", "birthday_lover")        #生日 格式**-**
birthday_my= conf.get("info", "birthday_my")
app_id = conf.get("info","app_id")   #微信测试号ID（开通以后自动生成）
app_secret = conf.get("info","app_secret")#微信测试号密钥（开通以后自动生成）
template_id =conf.get("info","template_id")
#接收消息的用户ID，让你的女朋友扫微信测试号的二维码，获取微信用户ID
user_id = conf.get("info","user_id") #接收消息的微信号，注意这个不是普通微信号，需要扫微信测试号后台的二维码来获取
user_id1=user_id.split(",")
print(type(user_id1))


"""
2、定义获取数据的函数

"""
#随机依据吃早饭的话
def get_eatmorning_words():
    list=[
            "早上起来吃早餐拥抱太阳，让身体充满，灿烂的阳光",
            "放假就懒，昨天偷懒没有吃早饭，午饭和晚饭也都很迟，胃现在都有点痛。一定还是要按时吃饭，记得吃早餐",
            "炎炎夏日的早晨，你是否没有胃口吃早餐呢？可是早餐很重要。",
            "我们都得经历一段努力、闭嘴、不抱怨的时光，才能熠熠生辉，才能去更酷的地方，成为更酷的人。早安！",
            "人们常说一年之计在于春，一天之计在于晨，可以说早餐的重要。",
            "生活本来就是一场恶战，给止疼药也好，给巴掌也罢，最终都是要单枪匹马练就自身胆量，谁也不例外。早安！",
            "晒晒我家的早餐，15分钟上桌，简单快捷，花钱少，吃得舒服。",
            "美好的一天从早上开始，当然美丽的心情从早餐开始，别忘了吃早餐哦。",
            "别将过去抱的太紧，因为那样你就腾不出手来拥抱此刻了！早上好！",
            "想吃一顿休闲早餐，像城市的女士们一样优雅地喝一杯美国咖啡，安静地坐着，享受秋天的阳光。",
            "充满了精神的青春，是不会那么轻易消失的。早安！",
            "轻轻的问候，道声早安，愿熟睡一晚的你，伴着清晨清香的空气，开始自己最美好的一天！",
            "分钟早餐，早餐要吃好不是只是说说。",
            "早餐是一天中的第一餐，也是最重要的一餐。",
            "清晨醒来的每个早晨，吃到爱心早餐，这是我想要的幸福。",
            "周末的早上一觉睡到自然醒，然后静静的享受一下自己做的早餐。",
            "每天叫醒你的，不是工作，不是阳光，而是一顿可口的早餐，带着满足去做好自己，做好每一件事。",
            "早餐吃的像皇帝，每天7：00准时做好，晒晒我今天的早餐。",
            "才发现生命真的是革命的本钱钱可以少赚点慢慢赚，健康第一位记得吃早餐，多喝水。",
            "日之晨在于早，一日之餐也是早，所以早餐很重要，在忙也要吃早餐！",
            "幸福如甜品，但酸甜苦辣的人生才是正餐。",
            "愿你沉淀又执着，对每件热爱的事物，都全力以赴又满载而归，变成一个美好的人，做美好的事。早安！",
            "是谁来自山川湖海，却囿于昼夜，厨房与爱。",
            "元气早餐秋冬天气，宜多喝汤水，粥类，预防上火。",
            "连起床这么艰难的事你都做到了，接下来的一天还有什么能难倒你！加油！早安哦！",
            "吃食是一种幸福，品味是一种情趣。",
            "早餐吃好了，一上午都有状态。很多人都草草应付早餐，一是早上时间紧，二是食材难备。",
            "为明天做准备的最好方法，就是集中你所有的智慧，所有的热情把今天的事情做得尽善尽美！",
            "天气晴朗，心情好。事情虽然多而且杂，但一件一件去做总能做好。",
            "星光不问赶路人，时光不负有心人。",
            "昨天太累，今天起晚了点早餐就做了一碗简单的牛肉面在忙，也要记得吃早餐。",
            "这样的早餐不仅要享受食物的味道，更重要的是要享受爱的温度。",
            "阳光，带着一丝的温和照在岁月的两岸，悄悄地带走了繁华的时光，留下了岁月的痕迹和回忆。",
            "早餐要吃好，晒晒我今天的早餐，简单省事，天天吃都不腻。",
            "我们单枪匹马闯入这世间，只为活出属于自己的所有可能；愿你这一生既有随处可栖的江湖，也有追风逐梦的骁勇。早安！",
            "有足够的时间做一顿有仪式感的早餐也是一种享受。",
            "心情好时，就算是阴天也会感觉到阳光的存在。",
            "世界那么大，我们去吃吃看？",
            "生活本来就是平凡琐碎的，哪有那么多惊天动地的大事，快乐的秘诀就是不管对大事小事都要保持热情。早安！",
            "世界上最治愈的东西，第一是美食，第二才是文字，记得吃早餐哦。",
            "早上好，愿你有个美好的心情。外面阳光正好，风微醺，这么大好的时光，记得吃早餐噢。",
            "睁开眼睛，给你一个轻轻的祝福，愿它每分每秒都带给你健康、好运和幸福。"
    ]

    return list[random.randint(0,len(list)-1)]


# 随机依据吃午饭的话
def get_eatnoon_words():
    list = [
            "人生是自己的，不要活在别人的眼神和口水里。不是所有的言论都需要别人理解，不是所有的选择都需要别人支持。午安。",
            "中午好，最好的祝福送给你！祝你幸福快乐！事事顺利！",
            "友情，在时间的隧道里发酵；情谊，在时光的长河里升华；思念，在彼此的世界里徘徊；问候，则在真挚的呼唤中出炉。朋友，无论何时何地，都愿你天天开心，幸福每时每刻！",
            "培养自己承担责任的勇气和自信心的训练，那么无疑会使一个胆怯懦弱的人以令人惊讶的速度成长为一个坚强勇敢的人。中午好！",
            "我愿为你纺织七色的彩带，让如丝的快乐、轻松、惬意将你紧紧包裹，舞动生活美丽的裙裾。我愿为你架起七色的虹桥，让如火的热情、真纯、祝福将你团团环绕，伴你灿烂生活多情的画卷。中午好！",
            "在一个秋高气爽的下午，躺在树荫下，泡一壶清茶。抱着自己喜欢的书慢慢品味这美好的生活。中午好！",
            "睁开眼睛，给你一个轻轻的祝福，愿它每分每秒都带给你健康好运和幸福。",
            "中午好朋友，醉人甜歌问候送给你，衷心祝福朋友中午开心快乐。",
            "当你收到信息时，那是我的心声；当你感觉温暖时，那是我的欣慰，当你会心一笑时，那是我的期盼；你快乐幸福每一天，是我的心愿。",
            "最好的生活是：时光，浓淡相宜;人心，远近相安。午安。",
            "真切的祝福你，我的朋友，生活虽然平淡，但却天天开心！早上醒来笑一笑，中午睡个美容觉，晚上烦恼都跑掉，明天生活会更好，幸福永远将你怀抱！",
            "永远不要对任何事感到后悔，因为它曾经一度就是你想要的。后悔也没用，要么忘记，要么努力。",
            "不要为了迎合所有人，把自己过得那么累!费尽心思让所有人都开心，你会忘了自己该怎么笑!午安!",
            "把每个睡醒后的早晨当成一件礼物，把每个开心后的微笑当成一个习惯。朋友，中午好，愿你微笑今天，快乐永远！中午好！",
            "如果我的祝愿，能驱除你的烦恼，那么，就让它随这温馨的春风，吹进你的心谷吧！",
            "疲惫的时候我的肩膀是你温馨的港湾，失败的时候我的鼓励是你力量的源泉，伤心的时候我的祝福为你衷心祈愿，朋友，我永远在你的身边，永远祝福你！",
            "激励自我，让斗志昂扬，鼓舞自我，让信心坚挺，完善自我，让能力发挥，努力自我，让梦想实现，拼搏自我，让生活幸福，超越自我，让未来精彩！",
            "夏日养生多喝茶，清心利尿效果佳，解热除烦真不差，止渴消暑好方法，热茶降温笑哈哈，各种冷饮不如它，祝你夏季笑哈哈，注意身边要有茶！中午好！",
            "把每个睡醒后的早晨当成一件礼物，把每个开心后的微笑当成一个习惯。朋友，短信祝早上好，愿你微笑今天，快乐永远！",
            "在男人的世界里，只有更稳定，才出众。只有不走寻常路，张开理想的翅膀飞越无限，才是我们我们正在努力的方向。",
            "换个人爱吧！会真心对你好的人不会只有他一个，如果全世界只余一个人爱你，那你活得也太惨了点。",
            "微笑，可以融化沉重的脸。欣赏，可以鼓舞沮丧心田。帮助，可以减轻人生重担。分享，可以激励奋发潜力。我们每天快乐一点点，生活就会精彩一点点！",
            "生活像一架跷跷板，一头是脾气，一头是福气，脾气越大福气越少，脾气越小福气越大。收得住脾气，才能留得住福气。午安。",
            "朝九晚五双休日，白领工作很得意；西装皮包计算机，小资生活很写意；表面光鲜人人识，背后辛酸无人知；麻木不仁在做事，何时才是出头日！",
            "以前总怕别人不喜欢自己，于是拼命迎合讨好，要是被误会了就恨不得马上能解释能化解。现在越长大心越大，不喜欢就不喜欢呗，大路朝天，各走一边。",
            "没有阳光，学会享受风雨的洗礼;没有鲜花，学会感受泥土的芬芳;没有掌声，学会领悟独处的境界，午安!","有些风景，如果你不站在高处，你永远体会不到它的魅力;有些路，如果你不去启程，你永远不知道它是多么的美丽。午安，各位。","钱不在多，够用就好。衣食无忧，烦恼就跑。房不在大，够住就好。遮风避雨，亲情围绕。友不在多，真心就好。急危救困，心急火燎。人生在世，知足就好。贪欲远离，心情美妙。愿你知足常乐，幸福抱抱！","不要太乖，不想做的事可以拒绝，做不到的事不用勉强，不喜欢的话假装没听见，你的人生不是用来讨好别人，而是善待自己。",
            "两人就这么消磨一下午的时光，相对而言，风平浪静，背后各是一生的波涛诡谲，不可说。中午好！",
            "自己能做的事情，不要去麻烦别人。中午好！","生活处处有困难，个子高的老撞头，个子矮的惹人笑，有钱的招红眼，没钱的招冷眼，我一正常年轻帅小伙，什么挫折不能过。",
            "所谓对自己好一点，就是看得起自己，原谅自己，纵容自己，鼓励自己，爱上自己。岁月会证明，你自己的自己，是唯一一个＂活对了的＂人生。",
            "培养好自己的气质，不要争面子;争来的是假的，养来的才是真的。",
            "晚安!看见夜空中的云了吗?我想你是看不见的，正因如此，我才会在云朵后面偷偷地看着你哦!看你夜里有没有想到我，看你夜里可爱的睡姿，这样我也会有好梦!",
            "大学生活好时机，培养独立好习惯。生活要独立，起居需自理。学习要独立，开拓求新知。思想要独立，明辨是与非。辛苦此一时，赢得是未来。",
            "真情，把距离拉近；真诚，把心灵吸引；真爱，把祝福传达；珍惜，把情意绵延。祝朋友健健康康，平平安安，幸幸福福，快快乐乐！中午好！",
            "中午好，别清闲着，现发放些工作给你，一定要按时完成，把快乐文件整理好，把幸福资料准备全，把欢乐证明做出来，好吧开始工作吧！",
            "送给你一阵轻风，带着我的问候;送给你一缕月光，映着我的影像;送给你一片白云，浸透我的温暖;送给你一条短信，连接你我友谊。",
            "女孩，如果你选择了放弃，就不要抱怨。因为世界是平衡的，每个人都要通过自己的努力去决定生活的样子。没人扶你的时候，自己要站直，路还长，背影要美。中午好！",
            "人生有多残酷，你就该有多坚强，别让挫折带走你的微笑和最初的梦想。",
            "初春时光，乍暖还寒，我的问候温暖不变；初春时节，阴晴不定，我的关怀始终不变；初春时分，万物新生，我的祝福与日俱增！祝好友万事俱备，不欠东风！中午好！",
            "经我反复协商，你的幸福专栏已搞定！你的财富，由财神独家赞助；你的笑容，由蒙娜丽莎代为发布；你的痛苦，引流到壶口瀑布；你的幸福，小心众人嫉妒！中午好！",
            "中午好，一丝思念，平常不失真切；一心惦记，流长不失平淡；一声问候，简约不失温暖；一种感情，恒久不会改变；一道祝福，来自内心的虔诚，祝君幸福安康，万事如意！",
            "人生是海，不为小事而争论，不为流言而费神，无须太计较得失，像海一样，纳百川，人生才能拥有海一般的湛蓝！",
            "生活，忙忙碌碌；身影，急急匆匆；牵挂，点点滴滴；思念，真真切切；问候，甜甜蜜蜜；祝福，真真挚挚。祝你每天快快乐乐，一生幸幸福福。中午好！",
            "天气渐渐变凉，衣衫应该多加，出来晒晒太阳，让我给你温暖，脸上带着微笑，幸福心中荡漾。愿你工作顺利，心情开朗，工资多加！中午好！",
            "中午好，最真诚的祝福送给你，祝你幸福快乐，幸福因为有你。","送你一朵玫瑰，那是我心中惟一一朵。只有戴在你的胸前，它才不会枯萎。",
            "心静者高，高者俯瞰世界;心和者仁，仁者包容万物;心慈者深，深者淡对冷暖;心慧者安，安者笑对人生。午安，各位。",
            "管它蚊子身边闹，管它苍蝇嗡嗡叫，耳朵全当没听到，愉快心情心中绕，炎热烦恼抛云霄，开开心心睡大觉，好梦连连来拥抱。晚安!",
            "最大的敌人莫过于自己，最大的缺点莫过于知错未改，谁都不是生下来就是天才，成功就要战胜自己，跨过坎坷。",
            "有压力，但不要被压垮；有迷茫，但永不要绝望。勇敢地去追求梦想，大胆地去创造奇迹。快乐与幸福只属于拼搏的你。愿成功与你如影相随！",
            "男人和成熟男人对女人的区别就是，前者哄你上床，后者哄你睡觉，各位午安。",
            "人生无限事，少有随心意，不可就此悲人生，就叹前路惘。笑看人生事，乐怀挫折事，人生丰富百媚生，成功指日创。",
            "让我的友情变成你的影子，陪伴你寂寞的光荫。让我的祝福变成雄心，鼓励你走过艰难困境。生活没有一帆风顺，努力就是成功！",
            "这个夏天，真心祝愿：大树庇护你，烈日让着你，微风向着你，暴雨躲着你，爱人由着你，邻居帮着你，朋友记着你，中奖万的只有你。中午好！",
            "想和你一起吃早餐，面对面说早安。",
            "做有用的事，说勇敢的话，想美好的事，睡安稳的觉，把时间用在进步上，而不是抱怨上。愿你遇到这样的人，愿你成为这样的人。午安。",
            "褪去疲劳，忘却烦躁，放眼今天，无限美好。好朋友的祝福总是很早，愿你每天微笑，心情大好，祝你健康幸福，万事顺意，中午好！",
            "把脸迎向微风，就能感受凉爽；把脸迎向阳光，就能感受温暖；把人生面向春天，就会充满动力。即使是冬日，也要像向日葵一样绽放，像夏日一样明媚。",
            "枫叶，证明秋天的存在；金菊，证明秋天的美丽；秋水，证明秋天的多情；秋月，证明秋天的浪漫；短信，证明我的思念；你，证明笨蛋是有的；哈哈！中午好！",
            "一次的想念，两次的失眠，三次的茶饭不思，四次的整夜不眠，五次的天天祝愿，六次的心语心愿，七次幻化成万言归一话，朋友，想你了，祝你好运，中午好！",
            "看着夜空中的月亮圆了一轮有一轮，希望你的梦境也想月亮一样圆满!",
            "早晨推开窗，拥抱阳光，觉得天然的浅笑；夜晚散漫步，聊聊家常，品尝普通的愉悦。中午好！愿你一天愉悦美妙！中午好！",
            "晚上，对着孤灯，我陷入不可名状的思念之中，实在排解不开时，我排徊在我俩散步的海滩、草地，对着星星、月亮，声声呼唤着你!",
            "苦辣酸甜，百味人生。较真起来，谁都难免觉得自己不够富足，但仔细想想，你拥有的其实并不少。学会感恩、知足常乐，方能获得幸福的生活。午安，各位。",
            "耐心点、坚强点，总有一天，你承受过的疼痛会有助于你，生活从来不会刻意亏欠谁，它给了你一块阴影，必会在不远地方撒下阳光。",
            "思念无声无息，弥漫你的心里。当夜深人静的时候，是不是又感到了寂寞，感到了心烦?那就送你一个好梦吧，愿你梦里能回到你媳妇的娘家……高老庄!",
            "天塌下来，有个高的人帮你扛着，可是你能保证，天塌下来的时候，个儿高的人没在弯腰吗?之后，还不是得靠自己!",
            "公驴出差回家，发现母驴怀孕了，公驴怒道：我出差快一年了，你怎么会怀孕，快说是谁干的好事！母驴一脸愧疚地说：是……是看短信的这个小子！",
            "人生道路上的每一个里程碑，都刻着两个字起点。中午好！",
            "天冷了，大树发抖了小草打冷颤了，小白兔穿羽绒服了，蚂蚁买了暧水袋了，小强冬眠了。中午了，你还看什么？多穿一件衣服，午睡别感冒了！",
            "不管忙不忙碌，有牵挂就好，不管联不联系，能想起就好，祝福总是相互的，不管身在何处，照顾好自我就是给对方最大的安慰，愿你的工资天天上升，情绪时时开心，中午好。",
            "没摘到春天的花朵，一样拥有春天。中午好！"
            ]

    return list[random.randint(0, len(list) - 1)]

def get_goodnight_words():
   list=[
     "瞌睡来了要睡呢，打扰瞌睡“遭罪孽”；瞌睡来了要睡好，头昏脑胀“伤不起”、祝福你睡眠好好，身体棒棒，工作愉快，快乐逍遥！",
     "当鸟儿倦了的时候，它会选择飞回巢穴，当人儿累的时候，他会选择回到家里，卸去疲惫的伪装，放松自己心情，原来生活是这样的美好，晚安，朋友！",
     "烦恼再多，工作再累，也要休息，安心睡觉，养足精神，充足睡眠，健康生活，活力四射，才能快乐每一天，夜深了，快安心休息吧、",
     "喂！你还没睡啊！我是周公啊！又到了我们约会的时间了啊！你不睡觉我怎么见得着你啊！我见不着你怎么知道你想要什么样的美梦啊！我不知道你想要什么美梦怎么帮你实现啊！快快睡觉吧！我等你好久了！美梦都帮你准备好了，再不来凉了啊！","给你的身子洗洗澡，洗去一身的劳累；给你的肠子洗洗澡，洗去一身的毒素；给你的脑子洗洗澡，洗去一身的烦恼；愿你舒舒服服睡好觉，梦游到桃花源中！晚安！",
     "把酒言欢的时候，你是否还在拼搏，秋风送爽的时候，你是否还在加班，我的关心，才最珍贵，今夜我还在想着你入睡，朋友，晚安！",
     "原来，看不见的伤痕最疼，流不出的眼泪最冷、","人生的路，总有几道沟坎；生活的味，总有几分苦涩、重要的是懂得调解、晚安！",
     "有些事，无能为力，就顺其自然；有些人，不能强求，就一笑了之；有些路，躲避不开，就义无反顾、晚安！",
     "我的梦中夜夜有你。我想，我也一定走进了你的梦里。愿我们在同一星空下编织思念!晚安，祝今晚好梦!",
     "睡着的时候突然打了个喷嚏醒了，我知道是你想我了。我的短信发的晚了，真对不起。如果你已经睡着了，那么，诅咒你打个喷嚏，因为我在想你。如果你还没睡着，那么，晚安啦!","心倦了，身累了，就该歇歇了;天黑了，夜深了，就该睡睡了。结束一天，需要勇气;展望明天，需要锐气。晚安，朋友!",
     "在这个宁静的夜晚，为你褪去疲惫的外衣，让整个世界的喧哗在此时静寂，所有美好的祝福都埋藏在大家的心底，欢乐宁静祥和环绕在你的周围，此时，只因你在享受梦的睡意。",
     "牵挂是月光的.皎洁，照彻浓浓的黑夜，思念是夏夜沁凉的风，吹拂你的额际躁动，惦记是温煦的床第，承托你疲惫的身体，有我的陪伴夏夜里不再暗黑的沉闷，尽情地舒展，祝美梦，晚安。","当夜幕笼罩整个大地，月光布满这一片天际，流星划过这深蓝的宇宙，我轻闭双眼，给你许愿：希望你的生活里阳光一片，精彩无限!晚安!"," 当你还拥有一份美好的缘分时，请一定要好好珍惜，千万别让它悄悄的溜走、当然，若它注定就是不会属于自己，但至少我们真心实意相待过，这样心里也不会有太深的遗憾、",
     " 知识是一种力量，但更有力量的是运用知识的经验、知识学一些忘一些陈旧一些，需要不断学习、如果你了解知识是如何不断转化为经验的，你就有驾驭它的力量，并开始出成就、"," 等到我们迷失了，我们才会开始了解自己、做一个简单的人，踏实而务实、不沉溺幻想、不庸人自扰、要快乐，要开朗，要坚韧，要温暖，对人要真诚、要诚恳，要坦然，要慷慨，要宽容，要有平常心、永远对生活充满希望，对于困境与磨难，微笑面对、多看书，看好书、少吃点，吃好的、"," 人们常因贫穷而产生恶毒之心，那么贫穷的根源究从何来呢？它就是从贪得无厌而不肯布施修福，以致换来贫穷的下场、就像我们虽有很多的钱财，却不懂得拿去投资、储蓄、等到山穷水尽时，我们就成了贫穷的俘虏、所以懂得布施，就是离苦的良方、晚安~",
     " 嘴上说改的人，现实里往往改不了、许多性格和生活习惯，是多少年积累下来的，几乎就是生命、婚姻和爱情最重要的，真的不是感情，而是选人、人选错了，就算感情再深，最后还是会爆发问题，时间越久问题越大、正因如此，所以一定要好好选人、不要着急，人好，一切才会好、",
     " 当遇到合适的人，彼此可以融合生活，不管简单也好，复杂也好，就不要犹豫，犹豫之间，他或她就有可能成为她或他的人、不要贪图物质的享受，也不要贪图精神的高尚，世间没有十全十美的人，也没有十全十美的生活，贫贱富贵，开心就好、",
     " 每一个人，并不是十分完美的、所以，不要评价别人容貌，因为他不靠你吃饭；不要评价别人的德行，因为你未必有他高尚；不要评价别人家庭，因为那和你无关、不要乱花钱，因为明天你可能失业；不要趾高气扬，因为明天你可能失势；不要吹嘘爱情，因为明天你可能失恋……"]

   return list[random.randint(0, len(list) - 1)]


#获取当前时间
def get_weekday():
    #日期时间
    date=(datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d %X")
    #农历日期
    nongli_date=zhdate.ZhDate.from_datetime(datetime.now()+timedelta(hours=8))
    #星期
    dayOfWeek = (datetime.now()+timedelta(hours=8)).weekday()
    if dayOfWeek==0:
        weekd=date+"  星期一\n"+str(nongli_date)
    if dayOfWeek==1:
        weekd=date+"  星期二\n"+str(nongli_date)
    if dayOfWeek==2:
        weekd=date+"  星期三\n"+str(nongli_date)
    if dayOfWeek==3:
        weekd=date+"  星期四\n"+str(nongli_date)
    if dayOfWeek==4:
        weekd=date+"  星期五\n"+str(nongli_date)
    if dayOfWeek==5:
        weekd=date+"  星期六\n"+str(nongli_date)
    if dayOfWeek==6:
        weekd=date+"  星期日\n"+str(nongli_date)
    return weekd



#获取天气
def get_weather(city):
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

#计算在一起的日期
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#计算距离下一次生日多少天
def get_birthday(birthday):
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now()+timedelta(hours=8):
    next = next.replace(year=next.year + 1)
  return (next - today).days

#计算到元旦、春节的日期
def get_spr(yd,sp):
  next1 = datetime.strptime(str(date.today().year) + "-" + yd, "%Y-%m-%d")
  if next1 < datetime.now()+timedelta(hours=8):
    next1 = next1.replace(year=next1.year + 1)
    j_yd=(next1 - today).days

  next2 = datetime.strptime(str(date.today().year) + "-" + sp, "%Y-%m-%d")
  if next2 < datetime.now()+timedelta(hours=8):
      next2 = next2.replace(year=next2.year + 1)
      j_cj = (next2 - today).days

  return j_yd,j_cj

#每日金句
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

#字体颜色，随机 每次不一样
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

#电影
def top_mv():
    # 1 爬取源
    url = "https://movie.douban.com/chart"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    # 2 发起http请求
    spond = requests.get(url, headers=header)
    res_text = spond.text
    # 3 内容解析
    soup = BeautifulSoup(res_text, "html.parser")
    soup1 = soup.find_all(width="75")  # 解析出电影名称
    # print(soup1[0]['alt'])
    soup2 = soup.find_all('span', class_="rating_nums")  # 解析出评分
    # print(soup2[0].text)
    # 4数据的处理

    """简单处理1，输入数值N，返回排第N的电影名及评分"""

    """处理2，将电影名和评分组成[{电影名：评分},{:}]的形式"""
    list_name = []  # 将电影名做成一个列表
    for i in range(10):
        list_name.append(soup1[i]['alt'])

    list_value = []  # 将评分值做成一个列表
    for i in range(10):
        list_value.append(soup2[i].text)

    dict_name_value = dict(zip(list_name, list_value))  # 将两个list转化为字典dict

    mv_top = sorted(dict_name_value.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)  # 字典排序,type==list


    for i in range(0,1):
        mv_top_name = mv_top[i][0]  # 取出电影名,后期直接使用
        mv_top_value = mv_top[i][1]  # 取出评分，后期直接使用
        show=str(mv_top_name) + ":" + str(mv_top_value) + "分"

    return show




"""
3、调用函数，获取数据，保存为字典格式数据
"""
#获取天气和温度
wea1, temperature1 = get_weather(city1)
wea2, temperature2 = get_weather(city1)

#计算到春节的天数
j_yd, j_cj = get_spr("01-01","01-12")
#如果温度过高，提示语
sid=""
if temperature1>=23:
  sid="[室外温度较高，注意喝水哦]"
elif temperature1<=17:
  sid="[室外温度过低，记得多穿点衣服保暖]"
else:
  sid="[温度不高不低，但也要注意及时补水哦]"

#提醒吃饭
now_time=int(time.localtime().tm_hour)
# print(now_time)
if now_time<4 and now_time>0:
    eat=get_eatmorning_words()
    m_n_a="[ 早安！宝 ]"
if now_time<11 and now_time>=4:
    eat = get_eatnoon_words()
    m_n_a = "[ 下午好吖！ ]"
if now_time<=24 and now_time>=11:
    eat = get_goodnight_words()
    m_n_a = "[ 记得晚上早点睡觉哈，然后做个好梦！]"

#数据整理
data = {"m_n_a":{"value":m_n_a,"color":get_random_color()},
        "eat":{"value":eat,"color":get_random_color()},
        "daytime":{"value":get_weekday(),"color":get_random_color()},
        "city1":{"value":city1,"color":get_random_color()},
        "city2":{"value":city2,"color":get_random_color()},
        "weather1":{"value":wea1,"color":get_random_color()},
        "weather2":{"value":wea2,"color":get_random_color()},
        "temperature1":{"value":str(temperature1)+"℃","color":get_random_color()},
        "sid":{"value":sid,"color":get_random_color()},
        "love_days":{"value":get_count(),"color":get_random_color()},
        "yd":{"value":j_yd,"color":get_random_color()},
        "cj":{"value":j_cj,"color":get_random_color()},
        "birthday_lover":{"value":get_birthday(birthday_lover),"color":get_random_color()},
        "birthday_my":{"value":get_birthday(birthday_my),"color":get_random_color()},
        "words":{"value":"\n"+get_words(),"color":get_random_color()},
        "mv":{"value":top_mv(),"color":get_random_color()},
         "start_date":{"value":get_count(),"vlaue":get_random_color()}
        }


"""
4、实例化微信客户端
"""
#模拟登录微信客户端
client = WeChatClient(app_id, app_secret)
#实例化微信客户端
wm = WeChatMessage(client)

"""
5、发送消息
"""
#参数 接收对象、消息模板ID、数据（消息模板里面的的变量与字典数据做匹配）

for i in range(0,len(user_id1)):
    print(user_id1[i])
    res = wm.send_template(user_id1[i], template_id, data)
    #打印消息发送情况
    print(res)



'''
[{{m_n_a.DATA}}] 
{{eat.DATA}} 
所在城市：{{city1.DATA}} 
当前时间：{{daytime.DATA}} 
今日天气：{{weather1.DATA}} 
当前温度：{{temperature1.DATA}} 
{{sid.DATA}} 
今天是我们在一起的第{{start_date.DATA}}天
距离领导的生日还有{{birthday_lover.DATA}}天 
距离秘书的生日还有{{birthday_my.DATA}}天 
距离元旦还有{{yd.DATA}}天 
距离春节还有{{cj.DATA}}天 
===家乡:{{city2.DATA}} 天气:{{weather2.DATA}}=== 
每日一句：{{words.DATA}}






'''
