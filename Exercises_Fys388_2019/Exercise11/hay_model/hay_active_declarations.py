#!/usr/bin/env python

import neuron
nrn = neuron.h

def make_cell_uniform():
    Vrest = -65
    nrn.t = 0
    nrn.finitialize(Vrest)
    nrn.fcurrent()
    for sec in nrn.allsec():
        for seg in sec:
            seg.e_pas = Vrest
            if nrn.ismembrane("na_ion"):
                seg.e_pas += seg.ina/seg.g_pas
            if nrn.ismembrane("k_ion"):
                seg.e_pas += seg.ik/seg.g_pas
            if nrn.ismembrane("ca_ion"):
                seg.e_pas += seg.ica/seg.g_pas
            if nrn.ismembrane("Ih"):
                seg.e_pas += seg.ihcn_Ih/seg.g_pas


def biophys_passive():
    for sec in neuron.h.allsec():
        sec.insert('pas')
        sec.cm = 1.0
        sec.Ra = 100.
    for sec in neuron.h.soma:
        sec.g_pas = 0.0000338
    for sec in neuron.h.apic:
        sec.cm = 2
        sec.g_pas = 0.0000589
    for sec in neuron.h.dend:
        sec.cm = 2
        sec.g_pas = 0.0000467
    for sec in neuron.h.axon:
        sec.g_pas = 0.0000325
    make_cell_uniform()
    print("Passive dynamics inserted.")


def biophys_passive_uniform():
    for sec in neuron.h.allsec():
        sec.insert('pas')
        sec.cm = 1.0
        sec.Ra = 100.
        sec.g_pas = 0.00003
    make_cell_uniform()
    print("Uniform passive dynamics inserted.")


def biophys_active():

    for sec in neuron.h.allsec():
        sec.insert('pas')
        sec.cm = 1.0
        sec.Ra = 100.
        sec.e_pas = -90.
    for sec in neuron.h.soma:
        sec.insert('Ca_LVAst')
        sec.insert('Ca_HVA')
        sec.insert('SKv3_1')
        sec.insert('SK_E2')
        sec.insert('K_Tst')
        sec.insert('K_Pst')
        sec.insert('Nap_Et2')
        sec.insert('NaTa_t')
        sec.insert('CaDynamics_E2')
        sec.insert('Ih')
        sec.ek = -85
        sec.ena = 50
        sec.gIhbar_Ih = 0.0002
        sec.g_pas = 0.0000338
        sec.decay_CaDynamics_E2 = 460.0
        sec.gamma_CaDynamics_E2 = 0.000501
        sec.gCa_LVAstbar_Ca_LVAst = 0.00343
        sec.gCa_HVAbar_Ca_HVA = 0.000992
        sec.gSKv3_1bar_SKv3_1 = 0.693
        sec.gSK_E2bar_SK_E2 = 0.0441
        sec.gK_Tstbar_K_Tst = 0.0812
        sec.gK_Pstbar_K_Pst = 0.00223
        sec.gNap_Et2bar_Nap_Et2 = 0.00172
        sec.gNaTa_tbar_NaTa_t = 2.04
    for sec in neuron.h.apic:
        sec.cm = 2
        sec.insert('Ih')
        sec.insert('SK_E2')
        sec.insert('Ca_LVAst')
        sec.insert('Ca_HVA')
        sec.insert('SKv3_1')
        sec.insert('NaTa_t')
        sec.insert('Im')
        sec.insert('CaDynamics_E2')
        sec.ek = -85
        sec.ena = 50
        sec.decay_CaDynamics_E2 = 122
        sec.gamma_CaDynamics_E2 = 0.000509
        sec.gSK_E2bar_SK_E2 = 0.0012
        sec.gSKv3_1bar_SKv3_1 = 0.000261
        sec.gNaTa_tbar_NaTa_t = 0.0213
        sec.gImbar_Im = 0.0000675
        sec.g_pas = 0.0000589

    nrn.distribute_channels("apic", "gIhbar_Ih", 2, -0.8696, 3.6161, 0.0, 2.087, 0.0002)
    nrn.distribute_channels("apic", "gCa_LVAstbar_Ca_LVAst", 3, 1.0, 0.010, 685.0, 885.0, 0.0187)
    nrn.distribute_channels("apic", "gCa_HVAbar_Ca_HVA", 3, 1.0, 0.10, 685.00, 885.0, 0.000555)

    for sec in neuron.h.dend:
        sec.cm = 2
        sec.insert('Ih')
        sec.gIhbar_Ih = 0.0002
        sec.g_pas = 0.0000467
    for sec in neuron.h.axon:
        sec.g_pas = 0.0000325
    make_cell_uniform()
    print("active ion-channels inserted.")

def active_declarations(**kwargs):
    ''' set active conductances for Hay model 2011 '''
    nrn.delete_axon()
    nrn.geom_nseg()
    nrn.define_shape()
    exec('biophys_%s()' % kwargs['conductance_type'])
