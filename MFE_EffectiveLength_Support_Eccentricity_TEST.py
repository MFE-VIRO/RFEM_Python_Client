import sys
sys.path.append("C:/Reken/PYTHON/RFEM_Python_Client")
from RFEM.enums import *
from RFEM.initModel import Model, SetAddonStatus
#from RFEM.dataTypes import inf, nan

if __name__ == '__main__':
    #from RFEM.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
    #from RFEM.baseSettings import BaseSettings
    #from RFEM.BasicObjects.coordinateSystem import CoordinateSystem
    from RFEM.TypesForSteelDesign.steelEffectiveLengths import SteelEffectiveLengths

    Model()
    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()
    SetAddonStatus(Model.clientModel, AddOn.steel_design_active, True)

    #LoadCasesAndCombinations(params={'current_standard_for_combination_wizard': 6207, 'activate_combination_wizard_and_classification': True, 'activate_combination_wizard': False, 'result_combinations_active': False, 'result_combinations_parentheses_active': False, 'result_combinations_consider_sub_results': False, 'combination_name_according_to_action_category': False})
    #BaseSettings(params={'gravitational_acceleration': 10.0, 'global_axes_orientation': 'E_GLOBAL_AXES_ORIENTATION_ZDOWN', 'local_axes_orientation': 'E_LOCAL_AXES_ORIENTATION_ZDOWN', 'tolerance_for_nodes': 0.0005000000237487257, 'tolerance_for_lines': 0.0005000000237487257, 'tolerance_for_surfaces_and_planes': 0.0005000000237487257, 'tolerance_for_directions': 0.0005000000237487257, 'member_representatives_active': False, 'member_set_representatives_active': False})
    #CoordinateSystem(params={'no': 1, 'type': 'TYPE_GLOBAL_XYZ', 'user_defined_name_enabled': False, 'name': 'Global XYZ', 'is_generated': False})
    SteelEffectiveLengths(params={'no': 1, 'user_defined_name_enabled': False, 'name': 'Standard', 'flexural_buckling_about_y': False, 'flexural_buckling_about_z': False, 'torsional_buckling': False, 'lateral_torsional_buckling': True, 'principal_section_axes': True, 'geometric_section_axes': False, 'is_generated': False, 'intermediate_nodes': True, 'different_properties': True, 'factors_definition_absolute': False, 'import_from_stability_analysis_enabled': False, 'determination_mcr_europe': 'DETERMINATION_EUROPE_EIGENVALUE', 'nodal_supports': {'steel_effective_lengths_nodal_supports': [{'no': 1, 'row': {'support_type': 'SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION', 'eccentricity_type': 'ECCENTRICITY_TYPE_NONE', 'support_in_y_type': 'SUPPORT_STATUS_YES', 'restraint_about_x_type': 'SUPPORT_STATUS_YES', 'restraint_about_z_type': 'SUPPORT_STATUS_NO', 'restraint_warping_type': 'SUPPORT_STATUS_NO'}}, {'no': 2, 'row': {'support_type': 'SUPPORT_TYPE_FIXED_IN_Y', 'eccentricity_type': 'ECCENTRICITY_TYPE_AT_UPPER_FLANGE', 'support_in_y_type': 'SUPPORT_STATUS_YES', 'restraint_about_x_type': 'SUPPORT_STATUS_NO', 'restraint_about_z_type': 'SUPPORT_STATUS_NO', 'restraint_warping_type': 'SUPPORT_STATUS_NO'}}, {'no': 3, 'row': {'support_type': 'SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION', 'eccentricity_type': 'ECCENTRICITY_TYPE_NONE', 'support_in_y_type': 'SUPPORT_STATUS_YES', 'restraint_about_x_type': 'SUPPORT_STATUS_YES', 'restraint_about_z_type': 'SUPPORT_STATUS_NO', 'restraint_warping_type': 'SUPPORT_STATUS_NO'}}]}, 'factors': {'steel_effective_lengths_factors': [{'no': 1}, {'no': 2}]}})

    SteelEffectiveLengths(2, "", "", False, False, False, True, True, False, 'SEL2',
        [
            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, \
            0,0,0,0, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Y, False, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_AT_UPPER_FLANGE, \
            1,4,2,3, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_NO, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""],

            [SteelEffectiveLengthsSupportType.SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION, True, 0.0, SteelEffectiveLengthsEccentricityType.ECCENTRICITY_TYPE_NONE, \
            0,0,0,0, SteelEffectiveLengthsSupportTypeInY.SUPPORT_STATUS_YES, SteelEffectiveLengthsRestraintTypeAboutX.SUPPORT_STATUS_YES, \
            SteelEffectiveLengthsRestraintTypeAboutZ.SUPPORT_STATUS_NO, SteelEffectiveLengthsRestraintTypeWarping.SUPPORT_STATUS_NO, ""]
        ],
        intermediate_nodes=True, different_properties=True, determination_of_mcr=SteelEffectiveLengthsDeterminationMcrEurope.DETERMINATION_EUROPE_EIGENVALUE
                        )
    Model.clientModel.service.finish_modification()

