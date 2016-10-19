import os
import sys

username = os.environ.get('USER')
hostname = str(os.environ.get('HOSTNAME'))
#if type(hostname) == NoneType:
#    hostname = 'unknown'
print(type(hostname))

# my laptop
workdir = '/Users/' + username + '/work/DisplacedVertices/Run2/'
rootcoredir = '/Users/' + username + '/ATLAS/sw/projects/DV_xAODAnalysis/'

if 'icepp.jp' in hostname:
    workdir = '/home/' + username +'/DV/DV_analysisScriptsRun2/'
    rootcoredir = '/home/' + username + '/DV/DV_xAODAnalysis/'
elif 'lxplus' in hostname:
    pass

plotdir = workdir + 'plots/'
histodir = workdir + 'histograms/'

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
