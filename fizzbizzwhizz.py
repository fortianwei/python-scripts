#coding=utf-8
"""
ThoughtWorks面试题:

你是一名体育老师，在某次课距离下课还有五分钟时，你决定搞一个游戏。此时有100名学生在上课。游戏的规则是：
1. 你首先说出三个不同的特殊数，要求必须是个位数，比如3、5、7。
2. 让所有学生拍成一队，然后按顺序报数。
3. 学生报数时，如果所报数字是第一个特殊数（3）的倍数，那么不能说该数字，而要说Fizz；如果所报数字是第二个特殊数（5）的倍数，那么要说Buzz；如果所报数字是第三个特殊数（7）的倍数，那么要说Whizz。
4. 学生报数时，如果所报数字同时是两个特殊数的倍数情况下，也要特殊处理，比如第一个特殊数和第二个特殊数的倍数，那么不能说该数字，而是要说FizzBuzz, 以此类推。如果同时是三个特殊数的倍数，那么要说FizzBuzzWhizz。
5. 学生报数时，如果所报数字包含了第一个特殊数，那么也不能说该数字，而是要说相应的单词，比如本例中第一个特殊数是3，那么要报13的同学应该说Fizz。如果数字中包含了第一个特殊数，那么忽略规则3和规则4，比如要报35的同学只报Fizz，不报BuzzWhizz。

现在，我们需要你完成一个程序来模拟这个游戏，它首先接受3个特殊数，然后输出100名学生应该报数的数或单词


第一反应就是,需要得到三个列表,分别对应某个数在fizz,bizz和whizz方面的分量,最后进行总和相加
假设三个特殊数字是 3 5 7
"""


"""
以下为草稿...
"""
fizz = map(lambda x:(x%3==0 or (str(3) in str(x))) and "Fizz" or "",range(1,101))
bizz = map(lambda x:(x%5==0 and not (str(3) in str(x)))and 'Bizz' or "",range(1,101))
whizz = map(lambda x:(x%7==0 and not (str(3) in str(x)))and "Whizz" or "",range(1,101))
print fizz
print bizz
print whizz
xxx = [fizz[i]+bizz[i]+whizz[i] or i+1 for i in range(100)]
print xxx
f = lambda a,b,c:[map(lambda x:(x%a==0 or (str(a) in str(x))) and "Fizz" or "",range(1,101))[i]+map(lambda x:(x%b==0 and not (str(a) in str(x)))and 'Bizz' or "",range(1,101))[i]+map(lambda x:(x%c==0 and not (str(a) in str(x)))and "Whizz" or "",range(1,101))[i] or i+1 for i in range(100)]
print f(3,5,7)
f = lambda a,b,c:[(str(a) in str(i) and  "Fizz") or ((i%a == 0 and "Fizz" or "")+(i%b == 0 and "Bizz" or "")+(i%c == 0 and "Whizz" or "")) or i for i in xrange(1,101)]
print f(3,5,7)
f = lambda a,b,c :["Fizz"*(str(a) in str(i)) or ("Fizz"*(i%a==0)+"Bizz"*(i%b==0) +"Whizz"*(i%c==0)) or i for i in range(1,101)]
print f(3,5,7)


print "hello" * 0   #结果为""
print "hello" * 1   #结果为"hello"
print "hello"*(not "hi")#结果为'',"hi"具有True含义,然后not之后为False,具有0含义
print "hello"*(not {})#结果为hello,{}具有False含义,然后not之后为True,具有0含义

"""
以下为解释
"""

"""
知识点:
python中的逻辑运算符并不仅仅适用于True/False,而是适用于全部python里面存在的东西
python中true的含义比如数字非0,string/tuple/list/dict等非空或者是function/class等等的时候,结果为yy
python中具有false含义的比如0,'',(),{},[]之类的时候,结果为zz
理论上,布局有false含义的东西,在python中就具有true的含义
例如

print True and "hello" or "world" #结果为 hello
print 1 and "hello" or "world"  #结果为 hello
print 5 and "hello" or "world"  #结果为 hello
print 'haha' and "hello" or "world"  #结果为 hello
print (4,7) and "hello" or "world"  #结果为 hello
f = lambda  x:x+1
print f and "hello" or "world"   #结果为 hello


print False and "hello" or "world" #结果为 world
print 0 and "hello" or "world" #结果为 world
print '' and "hello" or "world" #结果为 world
print [] and "hello" or "world" #结果为 world
print {} and "hello" or "world" #结果为 world


fizz = map(lambda x:(x%3==0 or (str(3) in str(x))) and "Fizz" or "",range(1,101))
bizz = map(lambda x:(x%5==0 and not (str(3) in str(x)))and 'Bizz' or "",range(1,101))
whizz = map(lambda x:(x%7==0 and not (str(3) in str(x)))and "Whizz" or "",range(1,101))
print fizz
print bizz
print whizz
['', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', 'Fizz', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', 'Fizz', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', '', '', 'Fizz', 'Fizz', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', 'Fizz', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', 'Fizz', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', 'Fizz', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '', '', 'Fizz', '']
['', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz', '', '', '', '', 'Bizz']
['', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '', '', '', '', '', 'Whizz', '', '']
很显然,把它们相加就得到对应值
print [fizz[i]+bizz[i]+whizz[i] if fizz[i]+bizz[i]+whizz[i] != '' else i+1 for i in range(100)]

结果:[1, 2, 'Fizz', 4, 'Bizz', 'Fizz', 'Whizz', 8, 'Fizz', 'Bizz', 11, 'Fizz', 'Fizz', 'Whizz', 'FizzBizz', 16, 17, 'Fizz', 19, 'Bizz', 'FizzWhizz', 22, 'Fizz', 'Fizz', 'Bizz', 26, 'Fizz', 'Whizz', 29, 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Fizz', 'Bizz', 41, 'FizzWhizz', 'Fizz', 44, 'FizzBizz', 46, 47, 'Fizz', 'Whizz', 'Bizz', 'Fizz', 52, 'Fizz', 'Fizz', 'Bizz', 'Whizz', 'Fizz', 58, 59, 'FizzBizz', 61, 62, 'Fizz', 64, 'Bizz', 'Fizz', 67, 68, 'Fizz', 'BizzWhizz', 71, 'Fizz', 'Fizz', 74, 'FizzBizz', 76, 'Whizz', 'Fizz', 79, 'Bizz', 'Fizz', 82, 'Fizz', 'FizzWhizz', 'Bizz', 86, 'Fizz', 88, 89, 'FizzBizz', 'Whizz', 92, 'Fizz', 94, 'Bizz', 'Fizz', 97, 'Whizz', 'Fizz', 'Bizz']

上面的方法很直观,而且可以简化
当然也可以一句话表示这个函数为:[fizz[i]+bizz[i]+whizz[i] or i+1 for i in range(100)]
然后一句话函数
f = lambda a,b,c:[map(lambda x:(x%a==0 or (str(a) in str(x))) and "Fizz" or "",range(1,101))[i]+map(lambda x:(x%b==0 and not (str(a) in str(x)))and 'Bizz' or "",range(1,101))[i]+map(lambda x:(x%c==0 and not (str(a) in str(x)))and "Whizz" or "",range(1,101))[i] or i+1 for i in range(100)]
print f(3,5,7)

很显然,这个一句话有点太长太罗嗦,其实还有很多可以有很多优化空间,不需要用到map,直接用and or来拼接字符串
利用空字符串的false特性,其实可以做更多事情:
f = lambda a,b,c:[(str(a) in str(i) and  "Fizz") or ((i%a == 0 and "Fizz" or "")+(i%b == 0 and "Bizz" or "")+(i%c == 0 and "Whizz" or "")) or i for i in xrange(1,101)]

其实上面是我想到的方法,然而据说别人写的更短,代码大致如下:
f = lambda a,b,c :["Fizz"*(str(a) in str(i)) or ("Fizz"*(i%a==0)+"Bizz"*(i%b==0) +"Whizz"*(i%c==0)) or i for i in range(1,101)]

恍然大悟,没错,思路没有反过来想
既然那么多有True含义的东西,那么True本身含义是什么?是数字1
既然那么多有False含义的东西,那么False本身含义是什么?是数字0

print "hello" * 0   #结果为""
print "hello" * 1   #结果为"hello"
print "hello"*(not "hi")#结果为'',"hi"具有True含义,然后not之后为False,具有0含义
print "hello"*(not {})#结果为hello,{}具有False含义,然后not之后为True,具有0含义

既然有0和1的表达,那么可以直接利用字符串乘以数字的方式来表达空字符串

也就是"fizz" * False 为 ''  而这个''同时又具有False含义,可以继续做逻辑操作(and/or/not)

"""