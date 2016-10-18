import AtlasStyle

import ROOT

import BasicConfig
import utils

from datetime import date

if __name__ == '__main__':
    AtlasStyle.SetAtlasStyle()

    mass_list = range(600, 1801, 200)
    tfiles = [utils.open_tfile(BasicConfig.workdir + 'SysUnc_ISR/SysUnc_ISR_{:04d}_weight.root'.format(mass))
              for mass in mass_list]

    c = ROOT.TCanvas('c', 'c', 1000, 800)
    c.SetLogx()
    tf_out = ROOT.TFile(BasicConfig.workdir + 'SysUnc_ISR/SysUnc_ISR_weight.root', 'recreate')
    for ii, (tfile, mass) in enumerate(zip(tfiles, mass_list)):
        tfile.cd()
        c2 = ROOT.gROOT.FindObject('c2')
        hist = c2.GetPrimitive('ggSystem_SysUnc_ISR')
        hist.SetName('ggSystem_SysUnc_ISR_' + str(mass))
        utils.decorate_histogram(hist, BasicConfig.colors[ii])
        c.cd()
        if ii == 0:
            hist.Draw()
        else:
            hist.Draw('same')
        tf_out.cd()
        hist.Write()
    utils.save_as(c, BasicConfig.plotdir + 'SysUnc_ISR_weight' + str(date.today()))
