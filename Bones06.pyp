import math
from math import acos, degrees
import os
import c4d
from c4d import plugins, utils, bitmaps
# for a Unique ID go to www.plugincafe.com
PLUGIN_ID = 1026001

BONES06_GLOBAL_SCALE = 10001
BONES06_HINGE_EXTENSION_LEFT = 10002
BONES06_HINGE_EXTENSION_RIGHT = 10003
BONES06_HINGE_THICKNESS = 10004
BONES06_HINGE_WRAP = 10005
BONES06_HINGE_ANCHOR_EXTENSION = 10006


global _r
_r = 20 #! radius segments

class Bones06(plugins.ObjectData):
#
#NullMatrix = Matrix(v1: (1, 0, 0); v2: (0, 1, 0); v3: (0, 0, 1); off: (0, 0, 0))

######################################################
	# def DummyFunction(self, hinge_extension_left,hinge_extension_right,hinge_thickness,hinge_wrap):
	# 	print hinge_extension_left,hinge_extension_right,hinge_thickness,hinge_wrap
	def GenerateMatrix(self, v1, v2, v3, off):
		mtx = c4d.Matrix(v1, v2, v3, off)
		return mtx

	#@staticmethod
	def SetGlobalRotation(self, obj, rot):
		m = obj.GetMg()
		pos = m.off
		scale = c4d.Vector( m.v1.GetLength(),
							m.v2.GetLength(),
							m.v3.GetLength())
							
		m = utils.HPBToMatrix(rot)
		
		m.off = pos
		m.v1 = m.v1.GetNormalized() * scale.x
		m.v2 = m.v2.GetNormalized() * scale.y
		m.v3 = m.v3.GetNormalized() * scale.z
		
		obj.SetMg(m)

	def angle(self, a, b, c):
		return math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))
		#return math.degrees(acos((a * a + b * b - c * c)/(2.0 * b * c)))

######################################### Merge Product

	def mergeObjects(self, objs, name):

		for o in objs:
			doc.InsertObject(o)
			o.ToggleBit(c4d.BIT_ACTIVE)
			o.GetBit(c4d.BIT_ACTIVE)

		c4d.CallCommand(16768)
		
		group = doc.GetActiveObject()
		group.SetName(name)

		result = group
		c4d.CallCommand(100004767)

		return result
		
	def Colorize(self, color):
		if color == 'red':
			return c4d.Vector(1,0,0)
		elif color == 'green':
			return c4d.Vector(0,1,0)
		elif color == 'blue':
			return c4d.Vector(0,0,1)

	def Vectorize(self, vector):
		return c4d.Vector(vector[0], vector[1], vector[2])

	def GenerateSpline(self, name, color, position, d_points):
		i = 0
		if not isinstance(position, c4d.Vector): 
			#raise TypeError("Expected vector, got %s" % type(position))
			position = self.Vectorize(position)

		spline_product = c4d.SplineObject(len(d_points), 0)
		spline_product.SetName(name)
		spline_product[c4d.ID_BASEOBJECT_USECOLOR] = 2
		spline_product[c4d.ID_BASEOBJECT_COLOR] = self.Colorize(color)

		for coords in d_points:
			try:
				spline_vec = c4d.Vector(coords[0],coords[1],coords[2]) - position
				spline_product.SetPoint(i, spline_vec)
			except IndexError:
				pass
			i = i + 1

		return spline_product

	def MakeCircle(self, start, end, points, radius, plane):
		res = []
		##
		i = start
		plot = end
		##
		slice = 2 * math.pi / points;

		while i <= plot:
			angle = slice * i

			if plane == 'x':
				newX = radius * math.cos(angle)
				newY = radius * math.sin(angle)
				p = (newX, newY, 0)
			elif plane == 'y':
				newY = radius * math.cos(angle)
				newZ = radius * math.sin(angle)
				p = (0, newY, newZ)
			else:
				newZ = radius * math.cos(angle)
				newX = radius * math.sin(angle)
				p = (newZ, 0, newX)
			res.append(p)
			i = i + 1

		return res
	#def BuildHinge(radius, wrap_radius, ext_a, ext_b, plane, position):

	def InsertHinge(self, name, radius, color, ext_a, ext_b, thk, wrp):
		
		item = doc.SearchObject(name)

		if item != None:
			position = item.GetMg()
		else:
			plugin = doc.SearchObject('Bones06')
			position = plugin.GetMg()

		doc.SetActiveObject(item)
		c4d.CallCommand(12109)

		#thk = 0
		# ext_a = ext
		# ext_b = ext
		#wrp = dat
		oy = 0
		oz = _s
		
		s_1 = [(-_s-wrp,-oy,-thk),(-_s-wrp,ext_a,-thk)]
		c_1 = c_3 = self.MakeCircle((_r/2),_r,_r, radius+wrp, 'x')
		c_2 = c_4 = self.MakeCircle(-(_r/4),(_r/4),_r, radius+thk, 'y')
		s_2 = [(-_s-wrp,ext_a,(_s*2)+thk),(-_s-wrp,-oy,(_s*2)+thk)]
		s_3 = [(_s+wrp,ext_b+oy,-thk),(_s+wrp,0,-thk)]
		s_4 = [(_s+wrp,ext_b+oy,(_s*2)+thk),(_s+wrp,0,(_s*2)+thk)]
		c_5 = self.MakeCircle(0,_r,_r, radius, 'z')
		#
		# c_1 = c_3 = self.MakeCircle(_r/2,_r,_r, radius+wrp, 'x')
		# c_2 = c_4 = self.MakeCircle(-5,5,20, radius+thk, 'y')
		# c_5 = self.MakeCircle(0,20,20, radius, 'z')
		#c_6 = MakeCircle(0,(_s*2),(_s*2), radius, 'z')

		a_0 = self.GenerateSpline(name, color, (0,0,oz), s_1)
		a_1 = self.GenerateSpline(name, color, (0,oy,thk+oz), c_1)
		a_2 = self.GenerateSpline(name, color, (_s+wrp,-ext_a,-_s+oz), c_2)
		a_3 = self.GenerateSpline(name, color, (0,0,oz), s_2)
		a_4 = self.GenerateSpline(name, color, (0,oy,-(_s*2)-thk+oz), c_3)
		a_5 = self.GenerateSpline(name, color, (-_s-wrp,-ext_b,-_s+oz), c_4)
		#a_7 = GenerateSpline(name, color, (0,40,-_s), c_6)
		a_8 = self.GenerateSpline(name, color, (0,oy,oz), s_3)
		a_9 = self.GenerateSpline(name, color, (0,oy,oz), s_4)
		a_6 = self.GenerateSpline(name, color, (0,((_s*2)+_s)+wrp+oy,-_s+oz), c_5)

		list=[a_0, a_1, a_2, a_3, a_4, a_5, a_6, a_8, a_9]

		wireframe_circle = self.mergeObjects(list, name)

		plugin_item = doc.SearchObject('Bones06')

		wireframe_circle.InsertUnder(plugin_item)
		wireframe_circle.SetMg(position)
		doc.SetActiveObject(plugin_item)

	def InsertHingeAnchor(self, name, hinge_thk, hinge_wrap, hinge_anchor_ext):
		
		rad = hinge_wrap + _s

		item = doc.SearchObject(name)

		if item != None:
			position = item.GetMg()
		else:
			plugin = doc.SearchObject('Bones06')
			position = plugin.GetMg()

		doc.SetActiveObject(item)
		c4d.CallCommand(12109)

		s_1 = self.MakeCircle(0,(_r*2),_r, rad, 'x')
		s_2 = self.MakeCircle(0,(_r*2),_r, rad, 'x')
		s_3 = [(0,0,0),(0,0,(-hinge_thk-_s)*2)]
		s_4 = [(0,hinge_wrap+_s*2+hinge_anchor_ext,0),(0,hinge_wrap+_s*2+hinge_anchor_ext,(-hinge_thk-_s)*2)]
		s_5 = [(0,hinge_wrap+_s*2+hinge_anchor_ext,(-hinge_thk-_s)*2),(0,hinge_wrap+_s,(-hinge_thk-_s)*2)]
		s_6 = [(0,hinge_wrap+_s*2+hinge_anchor_ext,0),(0,hinge_wrap+_s,0)]

		a_0 = self.GenerateSpline(name, 'blue', (0,0,hinge_thk+_s), s_1)
		a_1 = self.GenerateSpline(name, 'blue', (0,0,-hinge_thk-_s), s_2)
		a_2 = self.GenerateSpline(name, 'blue', (0,-hinge_wrap-_s,-hinge_thk-_s), s_3)
		a_3 = self.GenerateSpline(name, 'blue', (0,0,-hinge_thk-_s), s_4)
		a_4 = self.GenerateSpline(name, 'blue', (0,0,-hinge_thk-_s), s_5)
		a_5 = self.GenerateSpline(name, 'blue', (0,0,-hinge_thk-_s), s_6)

		list=[a_0, a_1, a_2, a_3, a_4, a_5]
		wireframe_circle = self.mergeObjects(list, name)
		plugin_item = doc.SearchObject('Bones06')

		wireframe_circle.InsertUnder(plugin_item)
		wireframe_circle.SetMg(position)
		doc.SetActiveObject(plugin_item)

		#print name
	def RotationConstraint(self, name, wrp, ext_a, ext_b, thk, ext_anchor):

		# first = int(raw_input("First side: "))
		# second = int(raw_input("Second side: "))

		item = doc.SearchObject(name)
		is_rot = item.GetAbsRot()[2]
		is_deg = is_rot * 180 / math.pi
		#
		print is_deg
		#
		if is_deg > 0:
			print 'right'

			#if ext_a+_s >= ext_anchor+wrp:
			a = ext_a+_s+thk
			b = wrp+_s
			c = math.hypot(a, b)
			print 'r_calc'

			if is_deg >= self.angle(c, a, b):
				#rot = op.GetAbsRot()
				#HPB = rot * 180 / math.pi
				hpb = c4d.Vector(0, 0, c4d.utils.Rad( self.angle(c, a, b) ))
				self.SetGlobalRotation(item, hpb)

				#print str(33)+'_'+str(is_rot * 180 / math.pi)
				return

		if is_deg < 0:
			print 'left'
			
			#if ext_b+_s >= ext_anchor+wrp:
			a = ext_b+_s+thk
			b = wrp+_s
			c = math.hypot(a, b)
			print 'l_calc'

			if is_deg <= -self.angle(c, a, b):
				#rot = op.GetAbsRot()
				#HPB = rot * 180 / math.pi
				hpb = c4d.Vector(0, 0, c4d.utils.Rad( -self.angle(c, a, b) ))
				self.SetGlobalRotation(item, hpb)

				#print str(33)+'_'+str(is_rot * 180 / math.pi)
				return
		
######################################### Merge Product
	def Message(self, node, type, data):
		if type==c4d.MSG_MENUPREPARE:
			doc = data
		return True

	def Init(self, node):
		data = node.GetDataInstance()
		global doc
		doc = c4d.documents.GetActiveDocument()

		self.InitAttr(node, float, [c4d.BONES06_GLOBAL_SCALE])
		self.InitAttr(node, float, [c4d.BONES06_HINGE_EXTENSION_LEFT])
		self.InitAttr(node, float, [c4d.BONES06_HINGE_EXTENSION_RIGHT])
		self.InitAttr(node, float, [c4d.BONES06_HINGE_THICKNESS])
		self.InitAttr(node, float, [c4d.BONES06_HINGE_WRAP])
		self.InitAttr(node, float, [c4d.BONES06_HINGE_ANCHOR_EXTENSION])

		data.SetReal(c4d.BONES06_GLOBAL_SCALE,1.0)
		data.SetReal(c4d.BONES06_HINGE_EXTENSION_LEFT,0.0)
		data.SetReal(c4d.BONES06_HINGE_EXTENSION_RIGHT,0.0)
		data.SetReal(c4d.BONES06_HINGE_THICKNESS,0.0)
		data.SetReal(c4d.BONES06_HINGE_WRAP,0.0)
		data.SetReal(c4d.BONES06_HINGE_ANCHOR_EXTENSION,0.0)

		#node[c4d.BONES06_GLOBAL_SCALE] = 10.0)
		#node[c4d.BONES06_HINGE_EXTENSION_LEFT] = 20.0)
		#node[c4d.BONES06_HINGE_EXTENSION_RIGHT] = 30.0)
		#node[c4d.BONES06_HINGE_THICKNESS] = 40.0)
		#node[c4d.BONES06_HINGE_WRAP] = 50.0)
		#node[c4d.BONES06_HINGE_ANCHOR_EXTENSION] = 60.0)

		return True
	def Draw(self, op, drawpass, bd, bh):
		self.RotationConstraint('Anchor', op[c4d.BONES06_HINGE_WRAP], op[c4d.BONES06_HINGE_EXTENSION_RIGHT], op[c4d.BONES06_HINGE_EXTENSION_LEFT], op[c4d.BONES06_HINGE_THICKNESS], op[c4d.BONES06_HINGE_ANCHOR_EXTENSION])

		return c4d.DRAWRESULT_OK
	
	def GetContour(self, op, doc, lod, bt):
		data = op.GetDataInstance()
		global _s
		_s = data.GetReal(c4d.BONES06_GLOBAL_SCALE) #1 #global scale

		ba = op.GetDataInstance()
		#bb = self.DummyFunction(ba.GetReal(c4d.BONES06_HINGE_EXTENSION_LEFT), ba.GetReal(c4d.BONES06_HINGE_EXTENSION_RIGHT), ba.GetReal(c4d.BONES06_HINGE_THICKNESS), ba.GetReal(c4d.BONES06_HINGE_WRAP) )

		bb = self.InsertHinge('Hinge', _s, 'green', ba.GetReal(c4d.BONES06_HINGE_EXTENSION_LEFT), ba.GetReal(c4d.BONES06_HINGE_EXTENSION_RIGHT), ba.GetReal(c4d.BONES06_HINGE_THICKNESS), ba.GetReal(c4d.BONES06_HINGE_WRAP))
		bs = self.InsertHingeAnchor('Anchor', ba.GetReal(c4d.BONES06_HINGE_THICKNESS), ba.GetReal(c4d.BONES06_HINGE_WRAP), ba.GetReal(c4d.BONES06_HINGE_ANCHOR_EXTENSION))
		#if not bb: return None
		
		#return bb
if __name__ == "__main__":
	path, file = os.path.split(__file__)
	bmp = bitmaps.BaseBitmap()
	bmp.InitWith(os.path.join(path, "res", "Bones06.tif"))
	plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Bones06",
								g=Bones06,
								description="Bones06", icon=bmp,
								info=c4d.OBJECT_GENERATOR|c4d.OBJECT_ISSPLINE)
