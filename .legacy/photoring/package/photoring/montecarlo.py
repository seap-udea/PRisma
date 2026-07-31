import numpy as np
import pandas as pd
import multiprocess as mp
from photoring.geotrans import *
from photoring.photoring import standard_adjust_params

def mcra_grid_general(S,props,store,samples,
                      adjust=standard_adjust_params,seed=None,verbose=False,default=False):
    """Generate a sample
    """
    
    # Noauto 
    noauto = S.noauto
    S.noauto = True

    # Seed 
    if seed is not None:
        np.random.seed(seed)

    # Arrays to store the values:
    Xs = []

    # Initialize spar
    # Store complimentary information
    spars = dict()
    for sprop,vals in store.items():
        spars[sprop] = getattr(S,vals['prop'])*vals['scale']

    # Maximum value of probabilities
    p_delta_max = 1/((2*np.pi)**0.5*S.delta_std)
    p_rho_obs_max = S.rho_obs_fun.y.max()
    if verbose:print(f"Maximum probabilities: p_delta_max: {p_delta_max}, p_rho_obs_max: {p_rho_obs_max}")

    i=0 # Main counter 
    n=0 # Counter of failed tests
    n_acceptances = [] # Number of tests before acceptance
    while i<samples:

        if verbose:print(f"Testing point: {n} ({i} accepted)")
        n+=1

        # Get a random point
        pars = dict()
        for prop,vals in props.items():
            if default:
                pars[prop] = vals['default']*vals['scale']
            else:
                pars[prop] = np.random.uniform(vals['range'][0], vals['range'][1]) * vals['scale']
        S.__dict__.update(pars)

        # Adjust parameters
        adjust(S)

        msg = ""
        for prop,vals in props.items():
            msg += f"{prop}: {getattr(S,prop)/vals['scale']}, "
        if verbose:print(f"Guess parameters: {msg.strip(', ')}")

        # Update system
        S.updateSystem()
        S.calculate_PR()

        # Store complimentary information
        spars = dict()
        for sprop,vals in store.items():
            spars[sprop] = getattr(S,vals['prop'])*vals['scale']

        # Compute probabilities
        p_rho_obs = float(S.rho_obs_fun(spars['rho_obs']))
        p_delta = float(S.delta_fun(spars['delta']))

        if verbose:print(f"\trho_obs: {spars['rho_obs']}, rho_true: {spars['rho_true']}, PR: {spars['PR']}, delta: {spars['delta']} (target {S.delta_mean})")
        if verbose:print(f"\tProbabilities: p_rho_obs: {p_rho_obs}, p_delta: {p_delta}")

        # Acceptance ratio
        alpha = p_rho_obs*p_delta / (p_rho_obs_max*p_delta_max)
        if verbose:print(f"\tAcceptance ratio: {alpha}")

        # Accept or reject
        u = np.random.rand()
        if verbose:print(f"\tRandom number: {u}")
        if u < alpha:
            # Sample parameters
            values = [pars[prop]/vals['scale'] for prop,vals in props.items()]
            svalues = [spars[prop] for prop in store.keys()]
            Xs.append(values + svalues)
            if verbose:print("\tAccepted")
            i += 1
            n_acceptances += [n]
            n = 0
        else:
            if verbose:print("\t\tRejected")
        
    if verbose:print(f"Acceptance rate: {np.mean(n_acceptances)} test per accepted sample")
    columns = [prop for prop,vals in props.items()]
    scolumns = [prop for prop,vals in spars.items()]
    Xs = pd.DataFrame(Xs,columns=columns + scolumns)

    S.noauto = noauto

    return Xs

def parallel_mcra_grid(S, props, store, samples=100, num_procs=1, adjust=standard_adjust_params):
    
    # Define the number of iterations for each process
    num_iterations = samples // num_procs

    # Function to run the grid
    def run_grid(seed):
        return mcra_grid_general(S, props, store, num_iterations, adjust=adjust, seed=seed)

    # Launch the grids in parallel
    with mp.Pool(processes=num_procs) as pool:
        results = pool.map(run_grid, range(num_procs))

    # Combine the results
    Xs = pd.concat(results, ignore_index=True)

    return Xs
