import os
import sys

username = os.environ.get('USER')

workdir = '/Users/' + username + '/work/DisplacedVertices/Run2/'
plotdir = workdir + 'plots/'
histodir = workdir + 'histograms/'

rootcoredir = '/Users/' + username + '/ATLAS/sw/projects/DV_xAODAnalysis/'

try:
    import ROOT
    import AtlasStyle
except ImportError:
    # on my laptop
    sys.path.append('/usr/local/root/latest/lib')
    sys.path.append(workdir + 'Macro/')
    import ROOT
    import AtlasStyle

colors = [ROOT.kGray+3, ROOT.kPink-1, ROOT.kViolet+9, ROOT.kViolet-1, ROOT.kAzure+1,
          ROOT.kSpring-1, ROOT.kOrange-3, ROOT.kOrange, ROOT.kPink+1, ROOT.kOrange-8]
