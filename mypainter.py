from expnode import *
from myparser import Parser
import matplotlib.pyplot as plt 
import math

class Painter:
	def __init__(self, string):
		self.orx = 0.0				#原点位置
		self.ory = 0.0
		self.scx = 1.0				#x轴放大倍数
		self.scy = 1.0				#y轴放大倍数
		self.ang = 0.0				#旋转角度
		self.Draw_color = 'k'		#默认颜色为黑色
		statements = Parser(string)
		# print(len(statements))

		self.analyse(statements)	#调用analyse函数
		self.showPic()				#展示图片

	# 语义分析
	def analyse(self, statements):
		for statement in statements:
			if statement[0]=="RotStatement":
				self.ang = statement[1].getValue()		#计算角度
			elif statement[0]=="ScaleStatement":		#放大倍数
				self.scx, self.scy = statement[1].getValue(), statement[2].getValue()
			elif statement[0]=="OriginStatement":		
				self.orx, self.ory = statement[1].getValue(), statement[2].getValue()
			elif statement[0]=="ForStatement":
				T_start, T_end = statement[1].getValue(), statement[2].getValue()
				T_step = statement[3].getValue()

				Point_x, Point_y = statement[4], statement[5]
				# print(statement[4].token.lexeme, statement[5].token.lexeme)
				if statement[6]:		#颜色
					# print(statement[6])
					self.Draw_color = statement[6]
				self.paint(T_start, T_end, T_step, Point_x, Point_y)
			else:
				print("analyse Error")

	def paint(self, T_start, T_end, T_step, Point_x, Point_y):
		# for T_value in range(T_start, T_end, T_step):
		T_value = T_start
		# 绘制的点坐标
		Points = dict(X=[], Y=[]) 
		while T_value<=T_end:
			ExpNode.T_value = T_value	#修改类的静态变量，来得到T的值
			x = Point_x.getValue()
			y = Point_y.getValue()
			# print(Point_x,Point_y)
			# print("(%f, %f)" % (x, y))

			# 坐标变换
			# 比例变换
			x, y = x*self.scx, y*self.scy
			# 旋转变换
			x, y = x*math.cos(self.ang) + y*math.sin(self.ang), y*math.cos(self.ang) - x*math.sin(self.ang)
			# 平移变换
			x, y = x+self.orx, y+self.ory

			# points.append((x, y))
			Points['X'].append(x)
			Points['Y'].append(y)

			# print("(%f, %f)" % (x, y))
			T_value += T_step

		# plt.plot(x,y,format_string,**kwargs) 
		# 第三个参数 https://blog.csdn.net/qiurisiyu2016/article/details/80187177
		# 'r', 'g', 'b', 'k'(Black),'y'(Yellow) 
		# '.' 点标记  ',' 像素点
		plt.plot(Points['X'], Points['Y'], ','+self.Draw_color)
		self.Draw_color='k'

	def showPic(self):
		# plt.xlim(xmax=100, xmin=-100)
		# plt.ylim(ymax=100, ymin=-100)
		# 保持纵横比例

		plt.axis('off')
		
		plt.show()
