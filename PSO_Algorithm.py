import random
import numpy as np


def pso(func, lb, ub, ieqcons=[], f_ieqcons=None, args=(), kwargs={},
		swarmsize=1000, pem=0.2, wmax=1.2, wmin=0.5, c1=2, c2=2, X=0.73, maxiter=1000,
		minstep=1e-8, minfunc=1e-8, debug=True):
	"""
    Perform a particle swarm optimization (PSO)

    Parameters
    ==========
    func : function
        The function to be minimized
    lb : array
        The lower bounds of the design variable(s)
    ub : array
        The upper bounds of the design variable(s)

    Optional
    ========
    ieqcons : list
        A list of functions of length n such that ieqcons[j](x,*args) >= 0.0 in
        a successfully optimized problem (Default: [])
    f_ieqcons : function
        Returns a 1-D array in which each element must be greater or equal
        to 0.0 in a successfully optimized problem. If f_ieqcons is specified,
        ieqcons is ignored (Default: None)
    args : tuple
        Additional arguments passed to objective and constraint functions
        (Default: empty tuple)
    kwargs : dict
        Additional keyword arguments passed to objective and constraint
        functions (Default: empty dict)
    swarmsize : int
        The number of particles in the swarm (Default: 100)
    Chi(X) : constriction factor which is used to control and constrict
        velocities (Default: 1)
    omega(w) : scalar
        Particle velocity scaling factor (Default: 0.5)
    phip(c1) : scalar
        Scaling factor to search away from the particle's best known position
        (Default: 0.5)
    phig(c2) : scalar
        Scaling factor to search away from the swarm's best known position
        (Default: 0.5)
    maxiter : int
        The maximum number of iterations for the swarm to search (Default: 100)
    minstep : scalar
        The minimum stepsize of swarm's best position before the search
        terminates (Default: 1e-8)
    minfunc : scalar
        The minimum change of swarm's best objective value before the search
        terminates (Default: 1e-8)
    debug : boolean
        If True, progress statements will be displayed every iteration
        (Default: False)

    Returns
    =======
    g : array
        The swarm's best known position (optimal design)
    f : scalar
        The objective value at ``g``

    """

	assert len(lb) == len(ub), 'Lower- and upper-bounds must be the same length'
	assert hasattr(func, '__call__'), 'Invalid function handle'
	lb = np.array(lb)
	ub = np.array(ub)
	assert np.all(ub > lb), 'All upper-bound values must be greater than lower-bound values'

	vhigh = np.abs(ub - lb)
	vlow = -vhigh

	# Check for constraint function(s) #########################################
	obj = lambda x: func(x, *args, **kwargs)
	if f_ieqcons is None:
		if not len(ieqcons):
			if debug:
				print('No constraints given.')
			cons = lambda x: np.array([0])
		else:
			if debug:
				print('Converting ieqcons to a single constraint function')
			cons = lambda x: np.array([y(x, *args, **kwargs) for y in ieqcons])
	else:
		if debug:
			print('Single constraint function given in f_ieqcons')
		cons = lambda x: np.array(f_ieqcons(x, *args, **kwargs))

	def is_feasible(x):
		check = np.all(cons(x) >= 0)
		return check

	# Initialize the particle swarm ############################################
	S = swarmsize
	D = len(lb)  # the number of dimensions each particle has
	x = np.random.rand(S, D)  # particle positions
	v = np.zeros_like(x)  # particle velocities
	p = np.zeros_like(x)  # best particle positions
	fp = np.zeros(S)  # best particle function values
	ft = np.zeros(S)  # fitness function values
	g = []  # best swarm position
	fg = 1e100  # artificial best swarm position starting value
	iter_vs_swamp_vs_fitness = []
	iter_vs_globalbest = []
	for i in range(S):
		# Initialize the particle's position
		x[i, :] = lb + x[i, :] * (ub - lb)

		# Initialize the particle's best known position
		p[i, :] = x[i, :]

		# Calculate the objective's value at the current particle's
		fp[i] = obj(p[i, :])


		# At the start, there may not be any feasible starting point, so just
		# give it a temporary "best" point since it's likely to change
		if i == 0:
			g = p[0, :].copy()

		# If the current particle's position is better than the swarm's,
		# update the best swarm position
		if fp[i] < fg and is_feasible(p[i, :]):
			fg = fp[i]
			g = p[i, :].copy()
			print('Initial best fitness value:', fg)

		# Initialize the particle's velocity
		v[i, :] = vlow + np.random.rand(D) * (vhigh - vlow)

	# Iterate until termination criterion met ##################################
	it = 1
	while it <= maxiter:
		print("Iteration Number:", it)
		rp = np.random.uniform(size=(S, D))
		rg = np.random.uniform(size=(S, D))
		for i in range(S):

			# Update the particle's velocity
			v[i, :] = X * ((wmax - it * (wmax - wmin) / maxiter) * v[i, :] + c1 * rp[i, :] * (p[i, :] - x[i, :]) + c2 * rg[i, :] * (g - x[i, :]))

			# Update the particle's position, correcting lower and upper bound
			# violations, then update the objective function value
			x[i, :] = x[i, :] + v[i, :]

			mark1 = x[i, :] < lb
			mark2 = x[i, :] > ub
			x[i, mark1] = lb[mark1]
			x[i, mark2] = ub[mark2]
			fx = obj(x[i, :])
			ft[i] = fx

			# Compare particle's best position (if constraints are satisfied)
			if fx < fp[i] and is_feasible(x[i, :]):
				p[i, :] = x[i, :].copy()
				fp[i] = fx
				print("current swarm best fitness value:", fp[i])
				iter_vs_swamp_vs_fitness.append([it, i, fp[i]])

				# Compare swarm's best position to current particle's position
				# (Can only get here if constraints are satisfied)
				if fx < fg:
					if debug:
						print('New best for swarm at iteration {:}: {:} {:}'.format(it, x[i, :], fx))
					iter_vs_globalbest.append([it, fx])

					tmp = x[i, :].copy()
					stepsize = np.sqrt(np.sum((g - tmp) ** 2))
					if np.abs(fg - fx) <= minfunc:
						print('Stopping search: Swarm best objective change less than {:}'.format(minfunc))
						return tmp, fx, iter_vs_swamp_vs_fitness, iter_vs_globalbest
					elif stepsize <= minstep:
						print('Stopping search: Swarm best position change less than {:}'.format(minstep))
						return tmp, fx, iter_vs_swamp_vs_fitness, iter_vs_globalbest
					else:
						g = tmp.copy()
						fg = fx
		# Algorithm for EMPSO
		if it > 0.1 * maxiter:
			sort_index = np.argsort(ft)
			sort_index = np.flip(sort_index)
			for k in range(int(3 * S ** (1. / 3))):  # No of mutation swarms can be taken as 3 times cube root of swarm size.
				l = sort_index[k]
				for d in range(len(ub)):
					if np.random.rand() < pem:
						x[l][d] = g[d] + 0.1 * (ub[d] - lb[d]) * np.random.randn()
					else:
						x[l][d] = g[d]
			for i in range(S):
				mark1 = x[i, :] < lb
				mark2 = x[i, :] > ub
				x[i, mark1] = lb[mark1]
				x[i, mark2] = ub[mark2]
				fx = obj(x[i, :])

				# Compare particle's best position (if constraints are satisfied)
				if fx < fp[i] and is_feasible(x[i, :]):
					p[i, :] = x[i, :].copy()
					fp[i] = fx
					print("current swarm best fitness value:", fp[i])
					iter_vs_swamp_vs_fitness.append([it, i, fp[i]])

					# Compare swarm's best position to current particle's position
					# (Can only get here if constraints are satisfied)
					if fx < fg:
						if debug:
							print('New best for swarm at iteration {:}: {:} {:}'.format(it, x[i, :], fx))
						iter_vs_globalbest.append([it, fx])

						tmp = x[i, :].copy()
						stepsize = np.sqrt(np.sum((g - tmp) ** 2))
						if np.abs(fg - fx) <= minfunc:
							print('Stopping search: Swarm best objective change less than {:}'.format(minfunc))
							return tmp, fx, iter_vs_swamp_vs_fitness, iter_vs_globalbest
						elif stepsize <= minstep:
							print('Stopping search: Swarm best position change less than {:}'.format(minstep))
							return tmp, fx, iter_vs_swamp_vs_fitness, iter_vs_globalbest
						else:
							g = tmp.copy()
							fg = fx

		print('Current global best after iteration {:}: {:}'.format(it, fg))

		if debug:
			print('Best after iteration {:}: {:}'.format(it, fg))
		it += 1

	print('Stopping search: maximum iterations reached --> {:}'.format(maxiter))

	if not is_feasible(g):
		print("However, the optimization couldn't find a feasible design. Sorry")
	return g, fg, iter_vs_swamp_vs_fitness, iter_vs_globalbest
