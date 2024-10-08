import numpy as np
import xarray as xr


def Γ1_moving_window_function(
        fWin: xr.Dataset,
        n: int,
) -> xr.DataArray:
    """
    This is the implementation of Γ1 function given by equation 9 in L.Graftieaux, M. Michard,
    N. Grosjean, "Combining PIV, POD and vortex identification algorithms for the study of
    unsteady turbulent swirling flows", Meas.Sci.Technol., 12(2001), p.1422-1429.
    Γ1 function is used to identify the locations of the centers of the vortices (which are
    given by the Γ1 peak values within the velocity field).
    IMPORTANT NOTICE: even though this function, theoretically, can be used on its own,  
    it is not supposed to. It is designed to be used with Dask for big
    PIV datasets. The recomendation is not to use this function on its own, but rather use
    Γ1 attribute of piv class of PIVPY package (example of usage in this case would be: ds.piv.Γ1())
    This function accepts a (2*n+1)x(2*n+1) neighborhood of one velocity vector from the
    entire velocity field in the form of Xarray dataset. And for this neighborhood only, 
    it calculates the value of Γ1.
    Also, note this function is designed in a way that assumes point P (see the referenced
    article) to coincide with the center for fWin.
    This function works only for 2D velocity field.

    Args:
        fWin (xarray.Dataset) - a moving window of the dataset (fWin = field rolling window)
        n (int) - the rolling window size (n=1 means a 3x3 rolling window)

    Returns:
        xr.DataArray(Γ1) (xr.DataArray) - an xarray DataArray object with Γ1 caclculated for
                                          for the given rolling window
    """
    # We must convert fWin to numpy, because when this function was originally implemented 
    # with fWin being an xr.Dataset, it was unbelievably slow! Conversion of fWin to numpy 
    # proved to give an incredible boost in speed.
    # To speed up the things even more I put everything in one line, which is unreadable.
    # Thus, to understand, what is going one, I'm giving a break up of the line
    # (the names of the variables are taken from the referenced article):
    # PMx = fWin['xCoordinates'].to_numpy() - float(fWin['xCoordinates'][n,n])
    # PMy = fWin['yCoordinates'].to_numpy() - float(fWin['yCoordinates'][n,n])
    # PM = np.sqrt(np.add(np.square(PMx), np.square(PMy)))
    # u = fWin['u'].to_numpy()
    # v = fWin['v'].to_numpy()
    # U = (u**2 + v**2)**(0.5)
    # The external tensor product (PM ^ U) * z (see the referenced article) can be simplified as a
    # cross product for the case of the 2D velocity field: (PM x U). According to the rules of
    # cross product, for the 2D velocity field, we have (PM x U) = PM_x * v - PM_y * u. In other
    # words, we don't have to compute the sin given in the referenced article. But I am, still,
    # going to use sin down below as the variable to be consistent with the expression given
    # in the referenced article.
    # sinΘM_Γ1 = (PMx*v - PMy*u) / PM / U 
    # Γ1 = np.nansum(sinΘM_Γ1) / (((2*n+1)**2))
    # And now here goes my one-liner. Note, that I didn't put PMx, PMy, u and v calculations
    # into my line. That's because I figured out emperically that would slow down the calculations.
    # n always points to the central interrogation window (just think of it). It gives me point P.
    PMx = np.subtract(fWin['xCoordinates'].to_numpy(), float(fWin['xCoordinates'][n,n]))
    PMy = np.subtract(fWin['yCoordinates'].to_numpy(), float(fWin['yCoordinates'][n,n]))    
    u = fWin['u'].to_numpy()
    v = fWin['v'].to_numpy()  
    # Since for the case when point M coincides with point P we have a 0/0 situation, we'll
    # recive a warning. To temporarily suspend that warning do the following (credit goes to
    # https://stackoverflow.com/a/29950752/10073233):
    with np.errstate(divide='ignore', invalid='ignore'):
        Γ1 = np.nanmean(np.divide(np.subtract(np.multiply(PMx,v), np.multiply(PMy,u)), np.multiply(np.sqrt(np.add(np.square(PMx), np.square(PMy))), np.sqrt(np.add(np.square(u), np.square(v))))))

    return xr.DataArray(Γ1).fillna(0.0) # fillna(0) is necessary for plotting


def Γ2_moving_window_function(
        fWin: xr.Dataset,
        n: int,
) -> xr.DataArray:
    """
    This is the implementation of Γ2 function given by equation 11 in L.Graftieaux, M. Michard,
    N. Grosjean, "Combining PIV, POD and vortex identification algorithms for the study of
    unsteady turbulent swirling flows", Meas.Sci.Technol., 12(2001), p.1422-1429.
    Γ2 function is used to identify the boundaries of the vortices in a velocity field.
    IMPORTANT NOTICE: even though this function, theoretically, can be used on its own, 
    it is not supposed to. It is designed to be used with Dask for big
    PIV datasets. The recomendation is not to use this function on its own, but rather use
    Γ2 attribute of piv class of PIVPY package (example of usage in this case would be: ds.piv.Γ2())
    This function accepts a (2*n+1)x(2*n+1) neighborhood of one velocity vector from the
    entire velocity field in the form of Xarray dataset. And for this neighborhood only, 
    it calculates the value of Γ2.
    Also, note this function is designed in a way that assumes point P (see the referenced
    article) to coincide with the center for fWin.
    And finally, the choice of convective velocity (see the referenced article) is made in the
    article: it is the average velocity within fWin.
    This function works only for 2D velocity field.

    Args:
        fWin (xarray.Dataset) - a moving window of the dataset (fWin = field rolling window)
        n (int) - the rolling window size (n=1 means a 3x3 rolling window)

    Returns:
        xr.DataArray(Γ2) (xr.DataArray) - an xarray DataArray object with Γ2 caclculated for
                                          for the given rolling window
    """
    # We must convert fWin to numpy, because when this function was originally implemented 
    # with fWin being an xr.Dataset, it was unbelievably slow! Conversion of fWin to numpy 
    # proved to give an incredible boost in speed.
    # To speed up the things even more I put everything in one line, which is unreadable.
    # Thus, to understand, what is going one, I'm giving a break up of the line
    # (the names of the variables are taken from the referenced article):
    # PMx = fWin['xCoordinates'].to_numpy() - float(fWin['xCoordinates'][n,n])
    # PMy = fWin['yCoordinates'].to_numpy() - float(fWin['yCoordinates'][n,n])
    # PM = np.sqrt(np.add(np.square(PMx), np.square(PMy)))
    # u = fWin['u'].to_numpy()
    # v = fWin['v'].to_numpy()
    # We are going to include point P into the calculations of velocity UP_tilde
    # uP_tilde = np.nanmean(u)
    # vP_tilde = np.nanmean(v)
    # uDif = u - uP_tilde
    # vDif = v - vP_tilde
    # UDif = (uDif**2 + vDif**2)**(0.5)
    # The external tensor product (PM ^ UDif) * z (see the referenced article) can be simplified as a
    # cross product for the case of the 2D velocity field: (PM x UDif). According to the rules of
    # cross product, for the 2D velocity field, we have (PM x UDif) = PM_x * vDif - PM_y * uDif. 
    # I am going to use sin down below as the variable to be consistent with the expression given
    # for Γ1 function.
    # sinΘM_Γ2 = (PMx*vDif - PMy*uDif) / PM / UDif 
    # Γ2 = np.nansum(sinΘM_Γ2) / (((2*n+1)**2))
    # And now here goes my one-liner. Note, that I didn't put PMx, PMy, u and v calculations
    # into my line. That's because I figured out emperically that would slow down the calculations.
    # n always points to the central interrogation window (just think of it). It gives me point P.
    PMx = np.subtract(fWin['xCoordinates'].to_numpy(), float(fWin['xCoordinates'][n,n]))
    PMy = np.subtract(fWin['yCoordinates'].to_numpy(), float(fWin['yCoordinates'][n,n]))    
    u = fWin['u'].to_numpy()
    v = fWin['v'].to_numpy()  
    uDif = u - np.nanmean(u)
    vDif = v - np.nanmean(v)
    # Since for the case when point M coincides with point P, we have a 0/0 situation and we'll
    # recive a warning. To temporarily suspend that warning do the following (credit goes to
    # https://stackoverflow.com/a/29950752/10073233):
    with np.errstate(divide='ignore', invalid='ignore'):
        Γ2 = np.nanmean(np.divide(np.subtract(np.multiply(PMx,vDif), np.multiply(PMy,uDif)), np.multiply(np.sqrt(np.add(np.square(PMx), np.square(PMy))), np.sqrt(np.add(np.square(uDif), np.square(vDif))))))

    return xr.DataArray(Γ2).fillna(0.0) # fillna(0) is necessary for plotting