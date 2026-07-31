import photoring as pr
from photoring.geotrans import *
from photoring.photoring import standard_adjust_params
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from scipy.stats import gaussian_kde

class UtilPlot(object):
    """
    This abstract class contains useful methods for the module plot
    """ 
        
    
    def mantisaExp(x):
        """
        Calculate the mantisa and exponent of a number.
        
        Parameters:
            x: number, float.
            
        Return:
            man: mantisa, float
            exp: exponent, float.
            
        Examples:
            m,e=mantisaExp(234.5), returns m=2.345, e=2
            m,e=mantisaExp(-0.000023213), return m=-2.3213, e=-5
        """
        xa=np.abs(x)
        s=np.sign(x)
        try:
            exp=int(np.floor(np.log10(xa)))
            man=s*xa/10**(exp)
        except OverflowError as e:
            man=exp=0
        return man,exp
    
class PlotGrid(object):
    r"""
    Class PlotGrid
    
    Create a grid of plots showing the projection of a N-dimensional
    
    Initialization attributes:
        dproperties: list of properties to be shown, dictionary of dictionaries (N entries)
            keys: label of attribute, ex. "q"
            dictionary: 
                label: label used in axis, string
                range: range for property, tuple (2)
        
    Optional initialization attributes:
        figsize=3 : base size for panels (the size of figure will be M x figsize), integer
        fontsize=10 : base fontsize, int
        direction='out' : direction of ticks in panels.
    
    Other attributes:
        N: number of properties, int
        M: size of grid matrix (M=N-1), int
        fw: figsize
        fs: fontsize
        fig: figure handle, figure
        axs: matrix with subplots, axes handles (MxM)
        axp: matrix with subplots, dictionary of dictionaries
        properties: list of properties labels, list of strings (N)
    
    Methods:
        tightLayout
        setLabels
        setRanges
        setTickParams
        
        plotHist
        scatterPlot

    Example:
        # Read data
        df_neas=pd.read_json(Util.packageFile("data/nea_extended.json.gz"))
        df_neas["q"]=df_neas["a"]*(1-df_neas["e"])

        # Prepare numpy array
        data_neas=np.array(df_neas[["q","e","i","Node","Peri","M"]])
        
        # Describe properties
        properties=dict(
            q=dict(label=r"$q$ [au]",range=[0,1.3]),
            e=dict(label=r"$e$",range=None),
            i=dict(label=r"$i$",range=[0,25]),
            W=dict(label=r"$\Omega$",range=None),
            w=dict(label=r"$\omega$",range=None),
            M=dict(label=r"$M$",range=None),
        )

        # Create PlotGrid
        G=PlotGrid(properties,figsize=2)

        # Plot histogram
        args=dict(alpha=1,bins=50,colorbar=True,cmap="rainbow")
        hist=G.plotHist(data_neas,**args)
        
        # Plot scatter
        args=dict(c='r',marker='.',s=2,edgecolors='none',alpha=0.3)
        G.scatterPlot(data_neas,**args)

        G.fig.suptitle(f"{len(data_neas)} NEAs MPC",x=0.5,y=0.8,ha='left',fontsize=18)
        G.fig.savefig("figs/NEAs-MPC.png")

    Developed by Jorge I. Zuluaga, 2024
    """
    
    def __init__(self,properties,figsize=3,fontsize=10,direction='out'):

        #Basic attributes
        self.dproperties=properties
        self.properties=list(properties.keys())

        #Secondary attributes
        self.N=len(properties)
        self.M=self.N-1
        
        #Optional properties
        self.fw=figsize
        self.fs=fontsize

        #Create figure and axes: it works
        try:
            self.fig,self.axs=plt.subplots(
                self.M,self.M,
                constrained_layout=True,
                figsize=(self.M*self.fw,self.M*self.fw),
                sharex="col",sharey="row"
            )
            self.constrained=True
        except:
            self.fig,self.axs=plt.subplots(
                self.M,self.M,
                figsize=(self.M*self.fw,self.M*self.fw),
                sharex="col",sharey="row"
            )
            self.constrained=False
            
        #Create named axis
        self.axp=dict()
        for j in range(self.N):
            propj=self.properties[j]
            if propj not in self.axp.keys():
                self.axp[propj]=dict()
            for i in range(self.N):
                propi=self.properties[i]
                if i==j:
                    continue
                if propi not in self.axp.keys():
                    self.axp[propi]=dict()
                if i<j:
                    self.axp[propj][propi]=self.axp[propi][propj]
                    continue
                self.axp[propj][propi]=self.axs[i-1][j]
    
        #Deactivate unused panels
        for i in range(self.M):
            for j in range(i+1,self.M):
                self.axs[i][j].axis("off")
        
        #Place ticks
        for i in range(self.M):
            for j in range(i+1):
                self.axs[i,j].tick_params(axis='both',direction=direction)
        for i in range(self.M):
            self.axs[i,0].tick_params(axis='y',direction="out")
            self.axs[self.M-1,i].tick_params(axis='x',direction="out")
        
        #Set properties of panels
        self.setLabels()
        self.setRanges()
        self.setTickParams()
        self.tightLayout()
    
    def tightLayout(self):
        """
        Tight layout if no constrained_layout was used.
        
        Parameters: None
        
        Return: None
        """
        if self.constrained==False:
            self.fig.subplots_adjust(wspace=self.fw/100.,hspace=self.fw/100.)
        self.fig.tight_layout()
        
    def setTickParams(self,**args):
        """
        Set tick parameters.
        
        Parameters: 
            **args: same arguments as tick_params method, dictionary
        
        Return: None
        """
        opts=dict(axis='both',which='major',labelsize=0.8*self.fs)
        opts.update(args)
        for i in range(self.M):
            for j in range(self.M):
                self.axs[i][j].tick_params(**opts)
        
    def setRanges(self):
        """
        Set ranges in panels according to ranges defined in dparameters.
        
        Parameters: None
        
        Return: None
        """
        for i,propi in enumerate(self.properties):
            for j,propj in enumerate(self.properties):
                if j<=i:continue
                if self.dproperties[propi]["range"] is not None:
                    self.axp[propi][propj].set_xlim(self.dproperties[propi]["range"])
                if self.dproperties[propj]["range"] is not None:
                    self.axp[propi][propj].set_ylim(self.dproperties[propj]["range"])
    
    def setLabels(self,**args):
        """
        Set labels parameters.
        
        Parameters: 
            **args: common arguments of set_xlabel, set_ylabel and text, dictionary
        
        Return: None
        """
        opts=dict(fontsize=self.fs)
        opts.update(args)
        for i,prop in enumerate(self.properties[:-1]):
            label=self.dproperties[prop]["label"]
            self.axs[self.M-1][i].set_xlabel(label,**opts)
        for i,prop in enumerate(self.properties[1:]):
            label=self.dproperties[prop]["label"]
            self.axs[i][0].set_ylabel(label,rotation=90,labelpad=10,**opts)
        for i in range(1,self.M):
            label=self.dproperties[self.properties[i]]["label"]
            self.axs[i-1][i].text(0.5,0.0,label,ha='center',
                                  transform=self.axs[i-1][i].transAxes,**opts)
            #270 if you want rotation
            self.axs[i-1][i].text(0.0,0.5,label,rotation=270,va='center',
                                  transform=self.axs[i-1][i].transAxes,**opts)

        label=self.dproperties[self.properties[0]]["label"]
        self.axs[0][1].text(0.0,1.0,label,rotation=0,ha='left',va='top',
                              transform=self.axs[0][1].transAxes,**opts)

        label=self.dproperties[self.properties[-1]]["label"]
        #270 if you want rotation
        self.axs[-1][-1].text(1.05,0.5,label,rotation=270,ha='left',va='center',
                              transform=self.axs[-1][-1].transAxes,**opts)

        self.tightLayout()
        
    def plotHist(self,data,noplot=False,colorbar=False,**args):
        """
        Create a 2d-histograms of data on all panels of the PlotGrid.
        
        Parameters: 
            data: data to be histogramed (n=len(data)), numpy array (nxN)
            
        Optional parameters:
            colorbar=False: include a colorbar?, boolean or int (0/1)
            **args: all arguments of hist2d method, dictionary
        
        Return: 
            hist: list of histogram instances.
        """
        opts=dict()
        opts.update(args)
            
        hist=[]
        for i,propi in enumerate(self.properties):
            if self.dproperties[propi]["range"] is not None:
                xmin,xmax=self.dproperties[propi]["range"]
            else:
                xmin=data[:,i].min()
                xmax=data[:,i].max()
            for j,propj in enumerate(self.properties):
                if j<=i:continue
                    
                if self.dproperties[propj]["range"] is not None:
                    ymin,ymax=self.dproperties[propj]["range"]
                else:
                    ymin=data[:,j].min()
                    ymax=data[:,j].max()                
                
                opts["range"]=[[xmin,xmax],[ymin,ymax]]
                h,xe,ye,im=self.axp[propi][propj].hist2d(data[:,i],data[:,j],**opts)
                
                hist+=[im]
                if colorbar:
                    #Create color bar
                    divider=make_axes_locatable(self.axp[propi][propj])
                    cax=divider.append_axes("top",size="9%",pad=0.1)
                    self.fig.add_axes(cax)
                    cticks=np.linspace(h.min(),h.max(),10)[2:-1]
                    self.fig.colorbar(im,
                                      ax=self.axp[propi][propj],
                                      cax=cax,
                                      orientation="horizontal",
                                      ticks=cticks)
                    cax.xaxis.set_tick_params(labelsize=0.5*self.fs,direction="in",pad=-0.8*self.fs)
                    xt=cax.get_xticks()
                    xm=xt.mean()
                    m,e=UtilPlot.mantisaExp(xm)
                    xtl=[]
                    for x in xt:
                        xtl+=["%.1f"%(x/10**e)]
                    cax.set_xticklabels(xtl)
                    cax.text(0,0.5,r"$\times 10^{%d}$"%e,ha="left",va="center",
                             transform=cax.transAxes,fontsize=6,color='w')

        self.setLabels()
        self.setRanges()
        self.setTickParams()
        self.tightLayout()

        return hist
                    
    def scatterPlot(self,data,**args):
        """
        Scatter plot on all panels of the PlotGrid.
        
        Parameters: 
            data: data to be histogramed (n=len(data)), numpy array (nxN)
            
        Optional parameters:
            **args: all arguments of scatter method, dictionary
        
        Return: 
            scatter: list of scatter instances.
        """
        scatter=[]
        for i,propi in enumerate(self.properties):
            for j,propj in enumerate(self.properties):
                if j<=i:continue
                scatter+=[self.axp[propi][propj].scatter(data[:,i],data[:,j],**args)]

        self.setLabels()
        self.setRanges()
        self.setTickParams()
        self.tightLayout()
        return scatter

def plotSample(Xs,S,props,rho_range=(500,4000),chargs=dict(),csargs=dict(),prefix="noprefix"):
    # ################################################
    # TARGET DISTRIBUTIONS
    # ################################################
    fig1, axs = plt.subplots(1, 3, figsize=(12, 6))

    # First subplot
    axs[0].hist(Xs['rho_obs'], bins=30, density=True, alpha=0.5, label='MCMC Samples')
    x = np.linspace(500,4000,400)
    y = S.rho_obs_fun(x)
    axs[0].plot(x, y, 'r--', label='Interpolated Observed Density')
    y_true = S.rho_true_fun(x)
    axs[0].plot(x, y_true, 'b--', label='Interpolated True Density')
    axs[0].set_xlim(*rho_range)
    axs[0].set_xlabel(r'Observed Density [kg/m$^3$]')
    axs[0].set_ylabel('Frequency')
    axs[0].legend()

    # Second subplot
    axs[1].hist(Xs['delta'], bins=30, density=True, alpha=0.5, label='MCMC Samples')
    delta_values = np.linspace(Xs['delta'].min(), Xs['delta'].max(), 400)
    gaussian = S.delta_fun(delta_values)
    axs[1].plot(delta_values, gaussian, 'r--', label='Gaussian Distribution')
    axs[1].set_xlabel('Delta')
    axs[1].set_ylabel('Frequency')
    axs[1].legend()

    # Third subplot
    axs[2].hist(Xs['rho_true'], bins=4, density=True, alpha=0.5, label='MCMC Samples')
    x = np.linspace(500,4000,400)
    y = S.rho_true_fun(x)
    axs[2].plot(x, y, 'r--', label='Interpolated True Density')
    axs[2].set_xlim(*rho_range)
    axs[2].set_xlabel(r'True Density [kg/m$^3$]')
    axs[2].set_ylabel('Frequency')
    axs[2].legend()

    plt.tight_layout()
    plt.savefig(f"{pr.PRFIG_DIR}/target_distributions-{prefix}.png")
    
    # ################################################
    # PARAMETER'S CONTOURS
    # ################################################
    columns = [prop for prop,vals in props.items()]
    data = np.array(Xs[columns])

    G=PlotGrid(props,figsize=3)

    hargs=dict(alpha=1,bins=10,density=False,colorbar=1,cmap="rainbow")
    hargs.update(chargs)
    G.plotHist(data,**hargs)

    sargs=dict(c='r',marker='.',s=2,edgecolors='none',alpha=0.3)
    sargs.update(csargs)
    G.scatterPlot(data,**sargs)
    G.fig.savefig(f"{pr.PRFIG_DIR}/corner_posteriors-{prefix}.png")

    # ################################################
    # PARAMETER'S POSTERIORS
    # ################################################
    fig2, axs = plt.subplots(1, len(props), figsize=(18, 6))

    for i, (prop, vals) in enumerate(props.items()):
        axs[i].hist(Xs[prop], bins=30, density=True, alpha=0.5, label=prop)
        axs[i].set_xlabel(prop)
        axs[i].set_ylabel('Frequency')
        axs[i].set_title(f'Histogram of {prop}')
        axs[i].legend()

    plt.tight_layout()
    plt.savefig(f"{pr.PRFIG_DIR}/parameters_posteriors-{prefix}.png")
    return G, fig1, fig2 

def plotPlanet(Xs,S,props,adjust=standard_adjust_params,scale=0.03,prefix="noprefix"):

    # Adjust parameters
    adjust(S)
    S.calculate_PR()
    S.updateSystem()

    # Plot Grid
    columns = [prop for prop,vals in props.items()]
    data = np.array(Xs[columns])

    G=PlotGrid(props,figsize=3)

    hargs=dict(alpha=1,bins=20,density=False,colorbar=1,cmap="rainbow")
    G.plotHist(data,**hargs)

    # Select
    values = np.array([getattr(S, prop) / props[prop]['scale'] for prop in props.keys()])
    sargs=dict(c='k',marker='x',s=100,edgecolors='none')
    data = np.array([values])
    G.scatterPlot(data,**sargs)

    # Probability
    delta=S.Ar/np.pi
    p_delta_max = 1/((2*np.pi)**0.5*S.delta_std)
    p_rho_obs_max = S.rho_obs_fun.y.max()

    p_rho_obs = float(S.rho_obs_fun(S.rho_obs))
    p_delta = float(S.delta_fun(delta))

    print(f"rho_obs: {S.rho_obs}, p(rho_obs_fun): {p_rho_obs}")
    print(f"delta: {delta}, p(delta_fun): {p_delta}")

    alpha = p_rho_obs*p_delta / (p_rho_obs_max*p_delta_max)
    print(f"Acceptance ratio: {alpha}")

    # Draw planet
    axs = G.fig.axes
    ax = axs[1]
    
    # Plot planet
    fh=0.2/(S.fe*S.Rp)
    fv=fh

    C=AR(0.5,0.5)
    Planet=Figure(C,fh*S.Rp,fv*S.Rp,1.0,0.0,'Planet')
    Ringe=Figure(C,fh*S.Re,fv*S.Re*cos(S.ieff),cos(S.teff),sin(S.teff),'Ringext')
    Ringi=Figure(C,fh*S.Ri,fv*S.Ri*cos(S.ieff),cos(S.teff),sin(S.teff),'Ringint')
    plotEllipse(ax,Planet,patch=True,zorder=10,color='k',transform=ax.transAxes)
    plotEllipse(ax,Ringe,zorder=10,color='b',alpha=0.2,transform=ax.transAxes)
    plotEllipse(ax,Ringi,zorder=10,color='r',alpha=0.2,transform=ax.transAxes)

    # Label 
    label = ""
    for prop in props.keys():
        value = getattr(S, prop) / props[prop]['scale']
        label += f"{prop}: {value:.1f}, "
    label = label.strip(", ")
    ax.set_title(f"Planet Configuration\n{label}",fontsize=10)

    G.fig.tight_layout()
    G.fig.savefig(f"{pr.PRFIG_DIR}/planet_configuration-{prefix}.png")
    
    return G

def get_maximum_kde(Xs,props):
    cols=props.keys()
    data_kde = Xs[cols].values.T
    kde = gaussian_kde(data_kde, bw_method=0.1)
    Xs['kde'] = kde(Xs[cols].T)
    max_kde_index = Xs['kde'].idxmax()
    max_kde_values = np.array(Xs.loc[max_kde_index, cols])
    peak_point = dict()
    for i,col in enumerate(cols):
        peak_point[col] = float(max_kde_values[i])
    return peak_point

