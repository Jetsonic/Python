class General:
	def __init__(self, g, ev):
		self.g = g
		self.ev = ev


general = General(g=9.810, ev=(1.51, 2.34, 3.6, 5.09, 5.49, 4.97, 4.14, 4.22, 3.91, 3.41, 2.46, 1.72))


class Reservoir:
	def __init__(self, reservoir, ita, power, rated_discharge, effective_twl=None, Smax=None, Smin=None, Height=None, MDR=None):
		self.name = reservoir
		self.ita = ita
		self.power = power
		self.Smax = Smax
		self.Smin = Smin
		self.effective_twl = effective_twl
		self.rated_discharge = rated_discharge
		self.Height = Height
		self.MDR = MDR


S3 = Reservoir('S3', ita=0.86, power=683, Smax=1769.286774, Smin=769.457152, effective_twl=535, rated_discharge=490)

S2 = Reservoir('S2', ita=0.86, power=1978, Smax=1806.892334, Smin=776.999601, effective_twl=424.6, rated_discharge=1048)

S1 = Reservoir('S1', ita=0.86, power=1357, Smax=1341.308929, Smin=409.5746392, effective_twl=305, rated_discharge=1340.4)

S_MD = Reservoir('S_MD', ita=0.91, power=28.62, Height=47.7, rated_discharge=67)

Dk_sk = Reservoir(reservoir='Dk_sk', ita=600, power=0.934, Smax=1503.37, Smin=238.9, effective_twl=366.4, rated_discharge=242.8, MDR=10)
Dk_dt = Reservoir(reservoir='Dk_dt', ita=0.918, power=35, Smax=1503.37, Smin=238.9, effective_twl=451, rated_discharge=21, MDR=10)
