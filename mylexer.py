# 词法分析器

from enum import Enum
import math

class TokenType(Enum):
    ORIGIN = "ORIGIN"
    SCALE = "SCALE"
    ROT = "ROT"
    IS = "IS"
    FOR = "FOR"
    FROM = "FROM"
    TO = "TO"
    STEP = "STEP"
    DRAW = "DRAW"
    T = "T"
    FUNC = "FUNCTION"
    CONST_ID = "CONST_ID"
    SEMICO = ';'
    L_BRACKET = '('
    R_BRACKET = ')'
    COMMA = ','
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    POWER = '**'
    NONTOKEN = "NON"
    ERRTOKEN = "ERR"
    OF = "OF"
    COLOR = "COLOR"

# print(TokenType.FUNC.name)	==> FUNC
# print(TokenType.FUNC.value)	==> FUNCTION
# 定义 Token类型的数据结构
class Token:
	def __init__(self, tokentype, lexeme, value=0.0, funcptr=None):
		self.tokenType = tokentype
		self.lexeme = lexeme
		self.value = value
		self.funcPtr = funcptr

	def show(self):
		print(self.tokenType.name.ljust(15), self.lexeme.ljust(15), str(self.value).ljust(15), self.funcPtr)

# CONST_ID
#初始化记号类型的初始值
TokenTypeDict = dict(PI = Token(TokenType.CONST_ID, "PI", math.pi), 
           E = Token(TokenType.CONST_ID, "E", math.e),      
           T = Token(TokenType.T, "T"),   
           ORIGIN = Token(TokenType.ORIGIN, "ORIGIN"), 
           SCALE = Token(TokenType.SCALE, "SCALE"), 
           ROT = Token(TokenType.ROT, "ROT"), 
           IS = Token(TokenType.IS, "IS"), 
           FOR = Token(TokenType.FOR, "FOR"), 
           FROM = Token(TokenType.FROM, "FROM"), 
           TO = Token(TokenType.TO, "TO"), 
           STEP = Token(TokenType.STEP, "STEP"), 
           DRAW = Token(TokenType.DRAW, "DRAW"),
           SIN = Token(TokenType.FUNC, "SIN", 0.0,  math.sin),    
           COS = Token(TokenType.FUNC, "COS", 0.0,  math.cos), 
           TAN = Token(TokenType.FUNC, "TAN", 0.0,  math.tan), 
           LN = Token(TokenType.FUNC, "LN", 0.0,  math.log), 
           EXP = Token(TokenType.FUNC, "EXP", 0.0,  math.exp), 
           SQRT = Token(TokenType.FUNC, "SQRT", 0.0,  math.sqrt),
           OF = Token(TokenType.OF, "OF"),
           RED = Token(TokenType.COLOR, "RED"),
           GREEN = Token(TokenType.COLOR, "GREEN"),
           BLUE = Token(TokenType.COLOR, "BLUE"),
           YELLOW = Token(TokenType.COLOR, "YELLOW"),
           BLACK = Token(TokenType.COLOR, "BLACK"))



def showTokens(tokens):
	# 定义首行格式内容
	print("Category".ljust(15), "Input".ljust(15), "Value".ljust(15), "FuncPtr")
	for token in tokens:
		token.show()
		
# 没有使用 NONTOKEN
# 利用 i<len(string)
# 


# 已改进
# 防止越界
def getChar(str, pos):
	if pos<len(str):
		return str[pos]
	else:
		return ''

def Lexer(string, show=False):
	# 词法分析
	# 过滤掉无关字符
	# 返回识别出的所有 token
	
	#输入的string为文本的字符串
	string = string.upper()

	tokens = []		# 识别出的token
	lineNum = 1 	# 行号
	# 获取的字母的位置，用于判断是否循环完
	i = 0
	# print("Line %d :" % lineNum)
	flag = True			#如果没有error，则flag为true，否则为false
	error=[]			#保存error信息
	while True:
		char = getChar(string, i)
		if char=='':      						#循环完时添加一个NONTOKEN，表示输入完成
			tokens.append(Token(TokenType.NONTOKEN, ''))
			break

		if char=='\n':							#如过为换行符，则行号加1，跳出继续读取下一个字符
			lineNum = lineNum + 1
			i = i + 1
			continue

		if char==' ' or char=='\t' or char=='\r':		#如果为空格、缩进则直接跳出
			i = i + 1
			continue

		token = None

		if char.isalpha():						#如果为字母
			tmpStr = char						#临时变量保存
			while True:
				i = i + 1
				char = getChar(string, i)
				if char.isalpha() or char.isdigit():    #有争议，不应该有数字
					tmpStr = tmpStr+char		#拼接字母
				else:
					i = i - 1					#下一个不是的话回退一个字符
					break

			# print(tmpStr)
			# 字典中没找到，则为 ERRTOKEN
			# dict.get(key, default=None)
			# 返回指定键的值，如果值不在字典中返回default值
			#token用来保存是否识别成功，结果->Token(,)
			token = TokenTypeDict.get(tmpStr, Token(TokenType.ERRTOKEN, tmpStr))
			if token.tokenType==TokenType.ERRTOKEN:			#有错误，提示编译错误
				flag=False
				error.append((lineNum,tmpStr))

		elif char.isdigit():			#识别数字，包括小数
			tmpNum = char
			while True:
				i = i + 1
				char = getChar(string, i)
				# char = string[i]
				if char.isdigit():
					tmpNum += char
				elif char=='.':
					tmpNum += '.'
					while True:
						i = i + 1
						char = getChar(string, i)
						if char.isdigit():
							tmpNum += char
						else:
							i = i - 1
							break
					break
				else: # 其他符号
					i = i - 1
					break
			token = Token(TokenType.CONST_ID, tmpNum, float(tmpNum))		#保存所识别的数字

		elif char==';':														#特殊单字符直接识别
			token = Token(TokenType.SEMICO, ';')
		elif char=='(':
			token = Token(TokenType.L_BRACKET, '(')
		elif char==')':
			token = Token(TokenType.R_BRACKET, ')')
		elif char==',':
			token = Token(TokenType.COMMA, ',')
		elif char=='+':
			token = Token(TokenType.PLUS, '+')
		elif char=='-':
			i = i + 1
			char = getChar(string, i)
			if char=='-':												# 注释，一致循环，舍弃注释内容，直到换行符
				while string[i+1]!='\n':
					i = i + 1
			else:
				i = i - 1							#如果第二个不是 “ - ”，则回退一个字符
				token = Token(TokenType.MINUS, '-')
		elif char=='*':								#乘和乘方
			i = i + 1
			char = getChar(string, i)
			if char=='*':
				token = Token(TokenType.POWER, '**')
			else:
				i = i - 1
				token = Token(TokenType.MUL, '*')

		elif char=='/':
			i = i + 1
			char = getChar(string, i)
			if char=='/':	# 注释
				while string[i+1]!='\n':
					i = i + 1
			else:
				i = i - 1
				token = Token(TokenType.DIV, '/')

		# 非法字符
		else:
			token = Token(TokenType.ERRTOKEN, char)

		# 调试用
		if token: # and token.tokenType!=TokenType.ERRTOKEN:
			# print(token.lexeme, end=' ')
			tokens.append(token)
		
		i = i + 1

	if show:
		showTokens(tokens)
	if flag==False:
		print("--"*30)
		print("LEXER ERROR: show follow")
		for k in error:
			print(k)
	return tokens


def test():
	# tokens = Lexer("--hello fad\n  //fadfjl\n  hahafds kLL ROT is (  1, 0*2) \n ROT is (sin(t), cos(tt));")
	str = "152+3**(5)+(1-34)*2/2-1*2**5*245-1+2-3*4/5-(6)*7-(((232)))*((2**5)-5)**1.4"
	tokens = Lexer(str)

	showTokens(tokens)

# print('.'.isdigit())
# test()