from ROOT import gDirectory
from ROOT import TFile
from ROOT import TTree
from ROOT import TH1F
from ROOT import TGraphErrors
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import kBlack, kGray

import AtlasStyle
import BasicConfig
import utils
import mc


def draw_cross_section_limit(tree, mass_g, flavor_of_sample='MET_TLJets'):
    AtlasStyle.SetAtlasStyle()
    entries = tree.GetEntries()
    current_delta_mass = 0
    upper_limits = []
    dM = []
    index = -1
    for entry in range(entries):
        tree.GetEntry(entry)
        if tree.mGluino == mass_g:
            if current_delta_mass != tree.deltaM:
                print('*** {0}, {1}'.format(tree.mGluino, tree.deltaM))
                upper_limits.append(TGraphErrors())
                dM.append(int(tree.deltaM))
                index += 1
                point = 0
            current_delta_mass = tree.deltaM
            #if current_delta_mass < 100:
            #    continue
            upper_limits[index].SetPoint(point, tree.ctau * 1e3, tree.xsUL)
            upper_limits[index].SetPointError(point, 0, tree.xsUL*tree.effRelStatErr+tree.xsUL*tree.effRelSystErr)
            point += 1
            print(tree.ctau, tree.xsUL)
    canvas = TCanvas('c', 'c', 1000, 800)
    canvas.SetLogx()
    canvas.SetLogy()
    #upper_limits[0].SetMinimum(0.8)
    #upper_limits[0].SetMinimum(0.05)
    #upper_limits[0].SetMaximum(30000)
    #upper_limits[0].GetXaxis().SetRangeUser(0.9, 310)
    #upper_limits[0].GetXaxis().SetTitle('c#tau [mm]')
    #upper_limits[0].GetYaxis().SetTitle('Cross Section [fb]')
    #upper_limits[0].Draw('A3')
    #if mass_g == 1400:
    #    upper_limits[1].RemovePoint(0)
    #upper_limits[0].RemovePoint(2)
    #upper_limits[1].RemovePoint(0)
    h_xs = TH1F('xs', ';c#tau [mm]; Cross Section [fb]', 1000, 0.9, 310)
    h_xs_line = TH1F('xs_line', ';c#tau [mm]; Cross Section [fb]', 1000, 0.9, 310)
    print(mc.mass_xs_err[mass_g]['xs'] * 1e3)
    for bin in range(1, 1000+1):
        h_xs.SetBinContent(bin, mc.mass_xs_err[mass_g]['xs'] * 1e3)
        h_xs_line.SetBinContent(bin, mc.mass_xs_err[mass_g]['xs'] * 1e3)
        h_xs.SetBinError(bin, mc.mass_xs_err[mass_g]['xs'] * 1e3 * mc.mass_xs_err[mass_g]['xs_err'] * 0.01)
    h_xs.SetMarkerSize(0)
    h_xs.SetFillStyle(3001)
    h_xs.SetFillColor(kGray+2)
    #h_xs.SetMinimum(0.8)
    h_xs.SetMinimum(0.05)
    h_xs.SetMaximum(30000)
    #h_xs.Draw('same,e2')
    h_xs.Draw('e2')
    h_xs_line.SetLineColor(kGray+3)
    h_xs_line.SetLineStyle(2)
    h_xs_line.Draw('same')
    legend = TLegend(0.60, 0.75, 0.83, 0.90)
    for ii, upper_limit in enumerate(upper_limits):
        #upper_limit.RemovePoint(0)
        upper_limit.SetMarkerSize(0)
        upper_limit.SetFillStyle(3001)
        index = ii
        if dM[ii] == 130:
            index = 1
        elif dM[ii] == 80:
            index = 2
            continue
        elif dM[ii] == 50:
            index = 3
        elif dM[ii] == 30:
            index = 4
        upper_limit.SetFillColor(BasicConfig.colors[index+1])
        upper_limit.SetLineColor(BasicConfig.colors[index+1])
        upper_limit.Draw('3,same')
        #upper_limit.Draw('c,same')
        #if dM[ii] > 100:
        #    #legend.AddEntry(upper_limit, 'M_{#tilde{g}} = '+str(mass_g)+' GeV, #DeltaM = '+str(dM[ii])+' GeV', 'lf')
        #    legend.AddEntry(upper_limit, '#DeltaM = '+str(dM[ii])+' GeV', 'lf')
        legend.AddEntry(upper_limit, '#DeltaM = '+str(dM[ii])+' GeV', 'lf')
    utils.decorate_legend(legend)
    legend.Draw()
    AtlasStyle.ATLASLabel(0.19, 0.87, 'Work in Progress')
    AtlasStyle.myText(0.20, 0.79, kBlack, '#sqrt{s} = 13 TeV, #int L dt = 30 fb^{-1}', 0.035)
    AtlasStyle.myText(0.20, 0.73, kBlack, 'Split-SUSY Model, M_{#tilde{g}} = '+str(mass_g)+' GeV', 0.032)
    #AtlasStyle.myText(0.20, 0.67, kBlack, 'M_{#tilde{g}} = '+str(mass_g)+' GeV', 0.035)
    utils.save_as(canvas, BasicConfig.plotdir + 'xs_limit_mGluino' + str(mass_g) + flavor_of_sample)


if __name__ == '__main__':
    input_tfile = TFile(BasicConfig.workdir + 'dv-multitrack-postprocessus/limits/rhadron_v00-02.root-out.root')
    flavor = 'MET_TLJets'
    input_tfile = TFile(BasicConfig.workdir + 'dv-multitrack-postprocessus/limits/rhadron_SimpleMETFilter.root-out.root')
    flavor = 'SimpleMET'
    tree = TTree()
    tree = input_tfile.Get('outTree')
    #tree = gDirectory.FindObject('outTree')

    draw_cross_section_limit(tree, mass_g=600, flavor_of_sample=flavor)
    draw_cross_section_limit(tree, mass_g=800, flavor_of_sample=flavor)
    draw_cross_section_limit(tree, mass_g=1000, flavor_of_sample=flavor)
    draw_cross_section_limit(tree, mass_g=1200, flavor_of_sample=flavor)
    draw_cross_section_limit(tree, mass_g=1400, flavor_of_sample=flavor)
    draw_cross_section_limit(tree, mass_g=1600, flavor_of_sample=flavor)
    draw_cross_section_limit(tree, mass_g=1800, flavor_of_sample=flavor)
    draw_cross_section_limit(tree, mass_g=2000, flavor_of_sample=flavor)
