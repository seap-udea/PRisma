from photoring import constants as c
import numpy as np

def standard_adjust_params(S,verbose=False):
    """Adjust the parameters of the system to the given values.

    Args:
        S (System): The system to adjust the parameters of.
        
        verbose (bool, optional): Whether to print the parameters. Defaults to False.

    Returns:
        None
    """
    
    # Given Porb and Mstar calculate ap
    S.ap = ((c.GCONST * S.Mstar * S.Porb_mean**2) / (4 * np.pi**2))**(1/3)
    if verbose:print(f"Semimajor axis: {S.ap/c.AU:.4f} au = {S.ap/S.Rstar:.2f} Rs")

    # Given Borb and ap calculate iorb
    S.iorb = np.arccos(S.borb_mean*S.Rstar/S.ap)
    if verbose:print(f"Orbital inclination: {S.iorb*c.RAD:.2f} degrees")

    S.updateSystem()
