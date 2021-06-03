# 语法分析器
from mylexer import Lexer
from mylexer import TokenType
from mylexer import Token
from expnode import ExpNode
import math
import sys


tokenIter = None    #全局变量保存词法分析器结果的迭代器
tokenNow = None		#保存当前Token
showProcess = False  #传参为True


def setDefaultValue(show):
	global showProcess
	showProcess = show


# 从词法分析器的tokens获得token
def FetchToken():
	global tokenNow
	try:
		tokenNow = next(tokenIter)    #获取一个Token
		return tokenNow
	except StopIteration:			#获取完毕，没有next
		sys.exit()					#失败则退出

def MatchToken(tokenType, show=False):	#匹配成功进入下一个Token，失败退出
	if show:
		tokenNow.show()
	if tokenNow.tokenType==tokenType:
		FetchToken()
		return True
	else:
		print("Excepted ", tokenType, "received ", tokenNow.tokenType)
		print("error!")
		return False
		exit(-1)

# level 递归层次
# op=0 进入
# op=1 退出
# showProcess Painter调用不显示信息
def Msg(level, str, op=1):
	global showProcess
	if not showProcess:
		return
	if op==0:
		print("  "*level+ "Enter --> %s" % str)
	else:
		print("  "*level+ "Exit  <-- %s" % str)


##########################################
# 表达式
# ########################################

# 二叉树节点
# + - * / ** T CONST_ID FUNC
# '('  ')' 匹配过程中扔掉
# 叶子节点： T CONST_ID
# 非叶子节点： 非终结符

# 加法运算 
# 左结合
# 新的 + - 为根节点
# Example： 1+2-3
#     -
#    / \
#   +   3
#  / \
# 1   2
# 

def Expression(level):
	Msg(level, "Expression", 0)  #打印 Enter --> Expression
	left = Term(level+1)
	root = None
	while tokenNow.tokenType==TokenType.PLUS or tokenNow.tokenType==TokenType.MINUS:
		root = ExpNode(tokenNow)  #创建root节点
		MatchToken(tokenNow.tokenType)
		right = Term(level+1)
		root.addson(left)
		root.addson(right)
		left = root
		# left.dfs()
	Msg(level, "Expression")     #打印 Exit --> Expression
	return left

# def Expression():
# 	Msg(0, "Expression")
# 	left = Term()
# 	root = None
# 	while tokenNow.tokenType==TokenType.PLUS or tokenNow.tokenType==TokenType.MINUS:
# 		root = ExpNode(tokenNow)
# 		MatchToken(tokenNow.tokenType)
# 		right = Expression()
# 		root.addson(left)
# 		root.addson(right)
# 		left = root
# 	Msg(1, "Expression")
# 	return left

# 乘法运算 
# 左结合
# 新的 * / 为根节点
# Example： 1*2*3
#     *
#    / \
#   *   3
#  / \
# 1   2
def Term(level):
	Msg(level, "Term", 0)
	left = Factor(level)
	root = None
	while tokenNow.tokenType==TokenType.MUL or tokenNow.tokenType==TokenType.DIV:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		right = Factor(level+1)
		root.addson(left)
		root.addson(right)
		left = root

	Msg(level, "Term")
	return left

def Factor(level):
	Msg(level, "Factor", 0)
	if tokenNow.tokenType==TokenType.PLUS or tokenNow.tokenType==TokenType.MINUS:
		root = ExpNode(tokenNow)   #构建一个表达式节点
		MatchToken(tokenNow.tokenType)
		son = Factor(level+1)	
		root.addson(son)
		Msg(level, "Factor")
		return root
	else:
		Msg(level, "Factor")
		return Component(level+1)		

# 乘方运算
# 右结合
# 不支持 CONST_ID ** MINUS CONST_ID, 需要添括号
#匹配  **
def Component(level):
	Msg(level, "Component", 0)
	left = Atom(level)
	if tokenNow.tokenType==TokenType.POWER:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		right = Component(level+1)

		root.addson(left)
		root.addson(right)
		Msg(level, "Component")
		return root
	else:
		Msg(level, "Component")
		return left

# 函数节点 FUNC <- CONST_ID | T
# 叶子节点 CONST_ID | T
def Atom(level):
	Msg(level, "Atom", 0)
	if tokenNow.tokenType==TokenType.CONST_ID or tokenNow.tokenType==TokenType.T:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		Msg(level, "Atom")
		return root

	elif tokenNow.tokenType==TokenType.FUNC:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		MatchToken(TokenType.L_BRACKET)
		son = Expression(level+1)
		MatchToken(TokenType.R_BRACKET)
		root.addson(son)
		Msg(level, "Atom")
		return root

	elif tokenNow.tokenType==TokenType.L_BRACKET:
		MatchToken(TokenType.L_BRACKET)
		root = Expression(level+1)
		MatchToken(TokenType.R_BRACKET)
		Msg(level, "Atom")
		return root
	else:
		print("Atom Error!")


#进入origin非终结符
def OriginStatement(level):
	Msg(level, "OriginStatement", 0)        #打印进入
	#匹配 origin is (
	MatchToken(TokenType.ORIGIN)
	print("  "*(level+1)+"Define -> "+"ORIGIN")
	MatchToken(TokenType.IS)
	print("  "*(level+1)+ "Define -> "+"IS")
	MatchToken(TokenType.L_BRACKET)
	print("  "*(level+1)+ "Define -> "+"(")
	Origin_x = Expression(level+1)			#再进入一层，匹配数字
	MatchToken(TokenType.COMMA)
	print("  "*(level+1)+ "Define -> "+",")
	Origin_y = Expression(level+1)
	MatchToken(TokenType.R_BRACKET)
	print("  "*(level+1)+ "Define -> "+")")

	Msg(level, "OriginStatement")
	return ["OriginStatement", Origin_x, Origin_y]

def	ScaleStatement(level):
	Msg(level, "ScaleStatement", 0)
	MatchToken(TokenType.SCALE)
	print("  "*(level+1)+"Define -> "+ "SCALE")
	MatchToken(TokenType.IS)
	print("  "*(level+1)+ "Define -> "+"IS")
	MatchToken(TokenType.L_BRACKET)
	print("  "*(level+1)+ "Define -> "+"(")
	Scale_x = Expression(level+1)
	MatchToken(TokenType.COMMA)
	print("  "*(level+1)+ "Define -> "+",")
	Scale_y = Expression(level+1)
	# print(Scale_x)
	# print(Scale_y)
	MatchToken(TokenType.R_BRACKET)
	print("  "*(level+1)+ "Define -> "+")")

	Msg(level, "ScaleStatement")
	return ["ScaleStatement", Scale_x, Scale_y]

def	RotStatement(level):
	Msg(level, "RotStatement", 0)
	MatchToken(TokenType.ROT)
	print("  "*(level+1)+ "Define -> "+"ROT")
	MatchToken(TokenType.IS)
	print("  "*(level+1)+ "Define -> "+"IS")
	Rot_angle = Expression(level+1)

	Msg(level, "RotStatement")
	return ["RotStatement", Rot_angle]

def getColor():
	if tokenNow.tokenType==TokenType.COLOR:
		if tokenNow.lexeme=='RED':
			color = 'r'
		elif tokenNow.lexeme=='GREEN':
			color = 'g'
		elif tokenNow.lexeme=='BLUE':
			color = 'b'
		elif tokenNow.lexeme=='YELLOW':
			color = 'y'
		elif tokenNow.lexeme=='BLACK':
			color = 'k'
		MatchToken(TokenType.COLOR)
		return color
		# else: 
		# 	print("GetColor Error")	
	else:
		print("GetColor Error")

def	ForStatement(level):
	Msg(level, "ForStatement", 0)
	MatchToken(TokenType.FOR)
	print("  "*(level+1)+ "Define -> "+"FOR")
	MatchToken(TokenType.T)
	print("  "*(level+1)+ "Define -> "+"T")
	MatchToken(TokenType.FROM)
	print("  "*(level+1)+ "Define -> "+"FROM")
	T_start = Expression(level+1)
	MatchToken(TokenType.TO)
	print("  "*(level+1)+ "Define -> "+"TO")
	T_end = Expression(level+1)
	MatchToken(TokenType.STEP)
	print("  "*(level+1)+ "Define -> "+"STEP")
	T_step = Expression(level+1)

	
	MatchToken(TokenType.DRAW)
	print("  "*(level+1)+ "Define -> "+"DRAW")
	MatchToken(TokenType.L_BRACKET)
	print("  "*(level+1)+"Define -> "+ "(")
	Point_x = Expression(level+1)
	# print(Point_x.dfs())
	MatchToken(TokenType.COMMA)
	print("  "*(level+1)+"Define -> "+ ",")
	Point_y = Expression(level+1)
	MatchToken(TokenType.R_BRACKET)
	print("  "*(level+1)+ "Define -> "+")")

	# 自定义颜色
	Draw_color = None
	if tokenNow.tokenType==TokenType.OF:
		MatchToken(TokenType.OF)
		print("  "*(level+1)+ "Define -> "+"OF")
		print("  "*(level+1)+ "Define -> "+"COLOR")
		Draw_color = getColor() 
	# global T_value
	# Painter.set(Origin_x, Origin_y, Scale_x, Scale_y, Rot_angle)
	# Painter.paint(T_start, T_end, T_step, Point_x, Point_y, Draw_color)

	Msg(level, "ForStatement")
	return ["ForStatement", T_start, T_end, T_step, Point_x, Point_y, Draw_color]

#四种类型的语句
# Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement
def Statement(level):
	Msg(level, "Statement", 0)    #打印进入statement
	statement = None
	#判断四种语句然后跳转到对应函数，四种语句都没有则退出
	if tokenNow.tokenType==TokenType.ORIGIN:
		statement = OriginStatement(level+1)
	elif tokenNow.tokenType==TokenType.SCALE:
		statement = ScaleStatement(level+1)
	elif tokenNow.tokenType==TokenType.ROT:
		statement = RotStatement(level+1)
	elif tokenNow.tokenType==TokenType.FOR:
		statement = ForStatement(level+1)
	else:
		print("Statement Error!")
		exit(-1)

	Msg(level, "Statement")
	return statement

#语法树入口函数
def Program(level=0):
	Msg(level, "Program", 0)	#打印进入program
	statements = []
	#进入token的循环
	while tokenNow.tokenType!=TokenType.NONTOKEN:
		tmpstatement = Statement(level+1)
		matched = MatchToken(TokenType.SEMICO)
		if matched:
			statements.append(tmpstatement)
		else:
			print("Program Error")
			exit(-1)
	Msg(level, "Program")
	return statements

#语法分析器主函数
def Parser(string, show=False):
	global tokenIter			# 必须要 global

	# 调用词法分析器 得到记号表
	tokenList = Lexer(string)
	# 生成全局可迭代对象
	tokenIter = iter(tokenList)

	setDefaultValue(show)
	FetchToken()
	return Program()


def test():
	# Parser("--hello fad\n  //fadfjl\n ROT is pi/2   ; SCALE is (  1, 2*2);   \n   ORIGIN is ((2), 242/4);")
	str = "ORigin is (-30, 0); SCALE is (  20, 25); for t from 0 to 2*pi step 0.01 draw (sin(t), cos(t));  SCALE is (  30, 20); for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, t);for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, -t);for t from 0 to 2*pi step 0.01 draw (1+3*sin(t), 3*cos(t)); "

	Parser(str)
	# print("(%f, %f)" % (Origin_x, Origin_y))
	# print("(%f, %f)" % (Scale_x, Scale_y))
	# print("%f" % Rot_angle)


# test()