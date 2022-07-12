import sys
import os
import pytest
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RFEM.enums import PeriodicResponseCombinationRule, DirectionalComponentCombinationRule, CqsDampingRule
from RFEM.initModel import Model, CheckIfMethodOrTypeExists
from RFEM.BasicObjects.material import Material
from RFEM.LoadCasesAndCombinations.spectralAnalysisSettings import SpectralAnalysisSettings

if Model.clientModel is None:
    Model()

def test_spectral_analysis_settings():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    # Create Material
    Material(1, 'S235')

    #Create Spectral Analysis Settings
    SpectralAnalysisSettings(1, 'SpectralSettings_1', PeriodicResponseCombinationRule.SRSS, DirectionalComponentCombinationRule.SRSS)
    SpectralAnalysisSettings(2, 'SpectralSettings_2', PeriodicResponseCombinationRule.SRSS, DirectionalComponentCombinationRule.SCALED_SUM, equivalent_linear_combination=True, save_mode_results=True, signed_dominant_mode_results=True)
    SpectralAnalysisSettings(3, 'SpectralSettings_3', PeriodicResponseCombinationRule.SRSS, DirectionalComponentCombinationRule.SCALED_SUM, directional_component_scale_value=0.4)
    SpectralAnalysisSettings(4, 'SpectralSettings_4', PeriodicResponseCombinationRule.CQC, DirectionalComponentCombinationRule.SCALED_SUM, constant_d_for_each_mode=12)
    SpectralAnalysisSettings(5, 'SpectralSettings_5', PeriodicResponseCombinationRule.CQC, DirectionalComponentCombinationRule.SCALED_SUM, damping_for_cqc_rule=CqsDampingRule.DIFFERENT_FOR_EACH_MODE)
    SpectralAnalysisSettings(6, 'SpectralSettings_6', PeriodicResponseCombinationRule.CQC, DirectionalComponentCombinationRule.ABSOLUTE_SUM)

    Model.clientModel.service.finish_modification()

    assert Model.clientModel.service.get_spectral_analysis_settings(2).combination_rule_for_periodic_responses == 'SRSS'
    assert Model.clientModel.service.get_spectral_analysis_settings(2).combination_rule_for_directional_components == 'SCALED_SUM'
    assert Model.clientModel.service.get_spectral_analysis_settings(2).use_equivalent_linear_combination == True
    assert Model.clientModel.service.get_spectral_analysis_settings(2).signed_results_using_dominant_mode == True
    assert Model.clientModel.service.get_spectral_analysis_settings(2).save_results_of_all_selected_modes == True

    assert Model.clientModel.service.get_spectral_analysis_settings(3).combination_rule_for_directional_components_value == 0.4

    assert Model.clientModel.service.get_spectral_analysis_settings(4).combination_rule_for_periodic_responses == 'CQC'
    assert Model.clientModel.service.get_spectral_analysis_settings(4).constant_d_for_each_mode == 12

    assert Model.clientModel.service.get_spectral_analysis_settings(5).damping_for_cqc_rule == 'DIFFERENT_FOR_EACH_MODE'

    assert Model.clientModel.service.get_spectral_analysis_settings(6).combination_rule_for_directional_components == 'ABSOLUTE_SUM'
