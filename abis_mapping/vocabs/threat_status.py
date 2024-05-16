"""Provides threat status vocabulary for the package"""


# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ACT_CRITICALLY_ENDANGERED = utils.vocabs.Term(
    labels=(
        "ACT/CRITICALLY ENDANGERED",
        "AUSTRALIAN CAPITAL TERRITORY/CRITICALLY ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/ACT/critically-endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
ACT_ENDANGERED = utils.vocabs.Term(
    labels=(
        "ACT/ENDANGERED",
        "AUSTRALIAN CAPITAL TERRITORY/ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/ACT/endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
ACT_EXTINCT = utils.vocabs.Term(
    labels=(
        "ACT/EXTINCT",
        "AUSTRALIAN CAPITAL TERRITORY/EXTINCT",
    ),
    iri=utils.rdf.uri("threatStatus/ACT/extinct", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
ACT_EXTINCT_IN_THE_WILD = utils.vocabs.Term(
    labels=(
        "ACT/EXTINCT IN THE WILD",
        "AUSTRALIAN CAPITAL TERRITORY/EXTINCT IN THE WILD",
    ),
    iri=utils.rdf.uri("threatStatus/ACT/extinct-in-the-wild", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
ACT_REGIONALLY_CONSERVATION_DEPENDENT = utils.vocabs.Term(
    labels=(
        "ACT/REGIONALLY CONSERVATION DEPENDENT",
        "AUSTRALIAN CAPITAL TERRITORY/REGIONALLY CONSERVATION DEPENDENT",
    ),
    iri=utils.rdf.uri("threatStatus/ACT/regionally-conservation-dependent", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
ACT_VULNERABLE = utils.vocabs.Term(
    labels=(
        "ACT/VULNERABLE",
        "AUSTRALIAN CAPITAL TERRITORY/VULNERABLE",
    ),
    iri=utils.rdf.uri("threatStatus/ACT/vulnerable", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_CAMBA = utils.vocabs.Term(
    labels=(
        "EPBC/CAMBA",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CAMBA",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/CAMBA", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_CD = utils.vocabs.Term(
    labels=(
        "EPBC/CD",
        "EPBC/CONSERVATION DEPENDENT",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CD",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CONSERVATION DEPENDENT",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/conservation-dependent", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_CE = utils.vocabs.Term(
    labels=(
        "EPBC/CE",
        "EPBC/CRITICALLY ENDANGERED",
        "EPBC/CR",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CE",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CRITICALLY ENDANGERED",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CR",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/critically-endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_CITES = utils.vocabs.Term(
    labels=(
        "EPBC/CITES",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/CITES",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/CITES", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_E = utils.vocabs.Term(
    labels=(
        "EPBC/E",
        "EPBC/ENDANGERED",
        "EPBC/EN",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/E",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/ENDANGERED",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/EN",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_EX = utils.vocabs.Term(
    labels=(
        "EPBC/EX",
        "EPBC/EXTINCT",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/EX",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/EXTINCT",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/extinct", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_JAMBA = utils.vocabs.Term(
    labels=(
        "EPBC/JAMBA",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/JAMBA",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/JAMBA", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_KAMBA = utils.vocabs.Term(
    labels=(
        "EPBC/KAMBA",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/KAMBA",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/KAMBA", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_V = utils.vocabs.Term(
    labels=(
        "EPBC/V",
        "EPBC/VULNERABLE",
        "EPBC/VU",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/V",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/VULNERABLE",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/VU",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/vulnerable", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
EPBC_XW = utils.vocabs.Term(
    labels=(
        "EPBC/XW",
        "EPBC/EXTINCT IN THE WILD",
        "EPBC/EW",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/XW",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/EXTINCT IN THE WILD",
        "ENVIRONMENT PROTECTION AND BIODIVERSITY CONSERVATION/EW",
    ),
    iri=utils.rdf.uri("threatStatus/EPBC/extinct-in-the-wild", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NSW_CE = utils.vocabs.Term(
    labels=(
        "NSW/CE",
        "NSW/CRITICALLY ENDANGERED",
        "NEW SOUTH WALES/CE",
        "NEW SOUTH WALES/CRITICALLY ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/NSW/Critically-Endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NSW_EX = utils.vocabs.Term(
    labels=(
        "NSW/EX",
        "NSW/EXTINCT",
        "NEW SOUTH WALES/EX",
        "NEW SOUTH WALES/EXTINCT",
    ),
    iri=utils.rdf.uri("threatStatus/NSW/Extinct", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NSW_EN = utils.vocabs.Term(
    labels=(
        "NSW/EN",
        "NSW/ENDANGERED",
        "NEW SOUTH WALES/EN",
        "NEW SOUTH WALES/ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/NSW/Endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NSW_V = utils.vocabs.Term(
    labels=(
        "NSW/V",
        "NSW/VULNERABLE",
        "NEW SOUTH WALES/V",
        "NEW SOUTH WALES/VULNERABLE",
    ),
    iri=utils.rdf.uri("threatStatus/NSW/Vulnerable", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_CE = utils.vocabs.Term(
    labels=(
        "NT/CE",
        "NT/CRITICALLY ENDANGERED",
        "NORTHERN TERRITORY/CE",
        "NORTHERN TERRITORY/CRITICALLY ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Critically-endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_DD = utils.vocabs.Term(
    labels=(
        "NT/DD",
        "NT/DATA DEFICIENT",
        "NORTHERN TERRITORY/DD",
        "NORTHERN TERRITORY/DATA DEFICIENT",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Data-Deficient", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_EN = utils.vocabs.Term(
    labels=(
        "NT/EN",
        "NT/ENDANGERED",
        "NORTHERN TERRITORY/EN",
        "NORTHERN TERRITORY/ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_EN_EXTINCT_IN_NT = utils.vocabs.Term(
    labels=(
        "NT/EN EXTINCT IN NT",
        "NT/ENDANGERED EXTINCT IN NT",
        "NORTHERN TERRITORY/EN EXTINCT IN NT",
        "NORTHERN TERRITORY/ENDANGERED EXTINCT IN NT",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Endangered-extinct-NT", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_EN_EXTINCT_IN_WILD_IN_NT = utils.vocabs.Term(
    labels=(
        "NT/EN EXTINCT IN WILD IN NT",
        "NT/ENDANGERED EXTINCT IN WILD IN NT",
        "NORTHERN TERRITORY/EN EXTINCT IN WILD IN NT",
        "NORTHERN TERRITORY/ENDANGERED EXTINCT IN WILD IN NT",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Endangered-extinct-in-wild-in-NT", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
NT_EW = utils.vocabs.Term(
    labels=(
        "NT/EW",
        "NT/CRITICALLY ENDANGERED POSSIBLY EXTINCT",
        "NORTHERN TERRITORY/EW",
        "NORTHERN TERRITORY/CRITICALLY ENDANGERED POSSIBLY EXTINCT",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Critically-endangered-possibly-extinct", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
NT_EX = utils.vocabs.Term(
    labels=(
        "NT/EX",
        "NT/EXTINCT",
        "NORTHERN TERRITORY/EX",
        "NORTHERN TERRITORY/EXTINCT",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Extinct", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_LC = utils.vocabs.Term(
    labels=(
        "NT/LC",
        "NT/LEAST CONCERN",
        "NORTHERN TERRITORY/LC",
        "NORTHERN TERRITORY/LEAST CONCERN",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Least-concern", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_LC_EXTINCT_IN_NT = utils.vocabs.Term(
    labels=(
        "NT/LC EXTINCT IN NT",
        "NT/LEAST CONCERN EXTINCT IN NT",
        "NORTHERN TERRITORY/LC EXTINCT IN NT",
        "NORTHERN TERRITORY/LEAST CONCERN EXTINCT IN NT",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Least-concern-extinct-in-NT", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_NE = utils.vocabs.Term(
    labels=(
        "NT/NE",
        "NT/NOT EVALUATED",
        "NORTHERN TERRITORY/NE",
        "NORTHERN TERRITORY/NOT EVALUATED",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Not-Evaluated", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_NT = utils.vocabs.Term(
    labels=(
        "NT/NT",
        "NT/NEAR THREATENED",
        "NORTHERN TERRITORY/NT",
        "NORTHERN TERRITORY/NEAR THREATENED",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Near-Threatened", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_VU = utils.vocabs.Term(
    labels=(
        "NT/VU",
        "NT/VULNERABLE",
        "NORTHERN TERRITORY/VU",
        "NORTHERN TERRITORY/VULNERABLE",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Vulnerable", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
NT_VU_EXTINCT_IN_NT = utils.vocabs.Term(
    labels=(
        "NT/VU EXTINCT IN NT",
        "NT/VULNERABLE EXTINCT IN NT",
        "NORTHERN TERRITORY/VU EXTINCT IN NT",
        "NORTHERN TERRITORY/VULNERABLE EXTINCT IN NT",
    ),
    iri=utils.rdf.uri("threatStatus/NT/Vulnerable-extinct-in-NT", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
QLD_C = utils.vocabs.Term(
    labels=(
        "QLD/C",
        "QLD/LEAST CONCERN WILDLIFE",
        "QUEENSLAND/C",
        "QUEENSLAND/LEAST CONCERN WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/Least-concern-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
QLD_CR = utils.vocabs.Term(
    labels=(
        "QLD/CR",
        "QLD/CRITICALLY ENDANGERED WILDLIFE",
        "QUEENSLAND/CR",
        "QUEENSLAND/CRITICALLY ENDANGERED WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/Critically-endangered-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
QLD_E = utils.vocabs.Term(
    labels=(
        "QLD/E",
        "QLD/ENDANGERED WILDLIFE",
        "QUEENSLAND/E",
        "QUEENSLAND/ENDANGERED WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/Endangered-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
QLD_EX = utils.vocabs.Term(
    labels=(
        "QLD/EX",
        "QLD/EXTINCT WILDLIFE",
        "QUEENSLAND/EX",
        "QUEENSLAND/EXTINCT WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/Extinct-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
QLD_I = utils.vocabs.Term(
    labels=(
        "QLD/I",
        "QLD/INTERNATIONAL WILDLIFE",
        "QUEENSLAND/I",
        "QUEENSLAND/INTERNATIONAL WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/International-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
QLD_NT = utils.vocabs.Term(
    labels=(
        "QLD/NT",
        "QLD/NEAR THREATENED WILDLIFE",
        "QUEENSLAND/NT",
        "QUEENSLAND/NEAR THREATENED WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/Near-threatened-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
QLD_PE = utils.vocabs.Term(
    labels=(
        "QLD/PE",
        "QLD/EXTINCT IN THE WILD WILDLIFE",
        "QUEENSLAND/PE",
        "QUEENSLAND/EXTINCT IN THE WILD WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/Extinct-in-the-wild-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
QLD_SL = utils.vocabs.Term(
    labels=(
        "QLD/SL",
        "QLD/SPECIAL LEAST CONCERN WILDLIFE",
        "QUEENSLAND/SL",
        "QUEENSLAND/SPECIAL LEAST CONCERN WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/Special-least-concern-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
QLD_V = utils.vocabs.Term(
    labels=(
        "QLD/V",
        "QLD/VULNERABLE WILDLIFE",
        "QUEENSLAND/V",
        "QUEENSLAND/VULNERABLE WILDLIFE",
    ),
    iri=utils.rdf.uri("threatStatus/QLD/Vulnerable-wildlife", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
SA_E = utils.vocabs.Term(
    labels=(
        "SA/E",
        "SA/ENDANGERED",
        "SOUTH AUSTRALIA/E",
        "SOUTH AUSTRALIA/ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/SA/Endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
SA_R = utils.vocabs.Term(
    labels=(
        "SA/R",
        "SA/RARE",
        "SOUTH AUSTRALIA/R",
        "SOUTH AUSTRALIA/RARE",
    ),
    iri=utils.rdf.uri("threatStatus/SA/Rare", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
SA_V = utils.vocabs.Term(
    labels=(
        "SA/V",
        "SA/VULNERABLE",
        "SOUTH AUSTRALIA/V",
        "SOUTH AUSTRALIA/VULNERABLE",
    ),
    iri=utils.rdf.uri("threatStatus/SA/Vulnerable", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
SA_SP = utils.vocabs.Term(
    labels=(
        "SA/SP",
        "SA/INDICATES THAT A RATING HAS BEEN APPLIED TO THE SPECIES LEVEL THE STATUS HAS NOT BEEN ASSESSED AT THE SUBSPECIES LEVEL",  # noqa: E501
        "SOUTH AUSTRALIA/SP",
        "SOUTH AUSTRALIA/INDICATES THAT A RATING HAS BEEN APPLIED TO THE SPECIES LEVEL THE STATUS HAS NOT BEEN ASSESSED AT THE SUBSPECIES LEVEL",  # noqa: E501
    ),
    iri=utils.rdf.uri("threatStatus/SA/sp", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
SA_SSP = utils.vocabs.Term(
    labels=(
        "SA/SSP",
        "SA/INDICATES THAT AT LEAST ONE SUBSPECIES FOR THIS SPECIES HAS BEEN GIVEN A CONSERVATION RATING",
        "SOUTH AUSTRALIA/SSP",
        "SOUTH AUSTRALIA/INDICATES THAT AT LEAST ONE SUBSPECIES FOR THIS SPECIES HAS BEEN GIVEN A CONSERVATION RATING",
    ),
    iri=utils.rdf.uri("threatStatus/SA/ssp", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
TAS_E = utils.vocabs.Term(
    labels=(
        "TAS/E",
        "TAS/ENDANGERED",
        "TASMANIA/E",
        "TASMANIA/ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/TAS/Endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
TAS_R = utils.vocabs.Term(
    labels=(
        "TAS/R",
        "TAS/RARE",
        "TASMANIA/R",
        "TASMANIA/RARE",
    ),
    iri=utils.rdf.uri("threatStatus/TAS/Rare", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
TAS_V = utils.vocabs.Term(
    labels=(
        "TAS/V",
        "TAS/VULNERABLE",
        "TASMANIA/V",
        "TASMANIA/VULNERABLE",
    ),
    iri=utils.rdf.uri("threatStatus/TAS/Vulnerable", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
TAS_X = utils.vocabs.Term(
    labels=(
        "TAS/X",
        "TAS/EXTINCT",
        "TASMANIA/X",
        "TASMANIA/EXTINCT",
    ),
    iri=utils.rdf.uri("threatStatus/TAS/Extinct", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
VIC_CONSERVATION_DEPENDENT = utils.vocabs.Term(
    labels=(
        "VIC/CONSERVATION DEPENDENT",
        "VICTORIA/CONSERVATION DEPENDENT",
    ),
    iri=utils.rdf.uri("threatStatus/VIC/Conservation-Dependent", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
VIC_CRITICALLY_ENDANGERED = utils.vocabs.Term(
    labels=(
        "VIC/CRITICALLY ENDANGERED",
        "VICTORIA/CRITICALLY ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/VIC/Critically-Endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
VIC_ENDANGERED = utils.vocabs.Term(
    labels=(
        "VIC/ENDANGERED",
        "VICTORIA/ENDANGERED",
    ),
    iri=utils.rdf.uri("threatStatus/VIC/Endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
VIC_ENDANGERED_EXTINCT_IN_VICTORIA = utils.vocabs.Term(
    labels=(
        "VIC/ENDANGERED EXTINCT IN VICTORIA",
        "VICTORIA/ENDANGERED EXTINCT IN VICTORIA",
    ),
    iri=utils.rdf.uri("threatStatus/VIC/Endangered-Extinct-in-Victoria", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
VIC_EXTINCT = utils.vocabs.Term(
    labels=(
        "VIC/EXTINCT",
        "VICTORIA/EXTINCT",
    ),
    iri=utils.rdf.uri("threatStatus/VIC/Extinct", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
VIC_EXTINCT_IN_THE_WILD = utils.vocabs.Term(
    labels=(
        "VIC/EXTINCT IN THE WILD",
        "VICTORIA/EXTINCT IN THE WILD",
    ),
    iri=utils.rdf.uri("threatStatus/VIC/Extinct-in-the-wild", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
VIC_RESTRICTED = utils.vocabs.Term(
    labels=(
        "VIC/RESTRICTED",
        "VICTORIA/RESTRICTED",
    ),
    iri=utils.rdf.uri("threatStatus/VIC/Restricted", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
VIC_VULNERABLE = utils.vocabs.Term(
    labels=(
        "VIC/VULNERABLE",
        "VICTORIA/VULNERABLE",
    ),
    iri=utils.rdf.uri("threatStatus/VIC/Vulnerable", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_CD = utils.vocabs.Term(
    labels=(
        "WA/CD",
        "WA/CONSERVATION DEPENDENT",
        "WA/SPECIES OF SPECIAL CONSERVATION INTEREST CONSERVATION DEPENDENT FAUNA",
        "WESTERN AUSTRALIA/CD",
        "WESTERN AUSTRALIA/CONSERVATION DEPENDENT",
        "WESTERN AUSTRALIA/SPECIES OF SPECIAL CONSERVATION INTEREST CONSERVATION DEPENDENT FAUNA",
    ),
    iri=utils.rdf.uri("threatStatus/WA/species-of-special-conservation-interest-conservation-dependent-fauna", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
WA_CR = utils.vocabs.Term(
    labels=(
        "WA/CR",
        "WA/CRITICALLY ENDANGERED",
        "WA/CRITICALLY ENDANGERED SPECIES",
        "WESTERN AUSTRALIA/CR",
        "WESTERN AUSTRALIA/CRITICALLY ENDANGERED",
        "WESTERN AUSTRALIA/CRITICALLY ENDANGERED SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/critically-endangered", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EN = utils.vocabs.Term(
    labels=(
        "WA/EN",
        "WA/ENDANGERED",
        "WA/ENDANGERED SPECIES",
        "WESTERN AUSTRALIA/EN",
        "WESTERN AUSTRALIA/ENDANGERED",
        "WESTERN AUSTRALIA/ENDANGERED SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/endangered-species", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EW = utils.vocabs.Term(
    labels=(
        "WA/EW",
        "WA/EXTINCT IN THE WILD",
        "WESTERN AUSTRALIA/EW",
        "WESTERN AUSTRALIA/EXTINCT IN THE WILD",
    ),
    iri=utils.rdf.uri("threatStatus/WA/extinct-in-the-wild", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_EX = utils.vocabs.Term(
    labels=(
        "WA/EX",
        "WA/EXTINCT",
        "WA/EXTINCT SPECIES",
        "WESTERN AUSTRALIA/EX",
        "WESTERN AUSTRALIA/EXTINCT",
        "WESTERN AUSTRALIA/EXTINCT SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/extinct-species", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_MI = utils.vocabs.Term(
    labels=(
        "WA/MI",
        "WA/MIGRATORY",
        "WA/MIGRATORY SPECIES",
        "WESTERN AUSTRALIA/MI",
        "WESTERN AUSTRALIA/MIGRATORY",
        "WESTERN AUSTRALIA/MIGRATORY SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/migratory-species", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_OS = utils.vocabs.Term(
    labels=(
        "WA/OS",
        "WA/OTHER SPECIFICALLY PROTECTED FAUNA",
        "WESTERN AUSTRALIA/OS",
        "WESTERN AUSTRALIA/OTHER SPECIFICALLY PROTECTED FAUNA",
    ),
    iri=utils.rdf.uri("threatStatus/WA/other-specifically-protected-fauna", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
WA_P1 = utils.vocabs.Term(
    labels=(
        "WA/P1",
        "WA/PRIORITY 1 POORLY KNOWN",
        "WA/PRIORITY 1 POORLY KNOWN SPECIES",
        "WESTERN AUSTRALIA/P1",
        "WESTERN AUSTRALIA/PRIORITY 1 POORLY KNOWN",
        "WESTERN AUSTRALIA/PRIORITY 1 POORLY KNOWN SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/P1-poorly-known-species", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P2 = utils.vocabs.Term(
    labels=(
        "WA/P2",
        "WA/PRIORITY 2 POORLY KNOWN",
        "WA/PRIORITY 2 POORLY KNOWN SPECIES",
        "WESTERN AUSTRALIA/P2",
        "WESTERN AUSTRALIA/PRIORITY 2 POORLY KNOWN",
        "WESTERN AUSTRALIA/PRIORITY 2 POORLY KNOWN SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/P2-poorly-known-species", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P3 = utils.vocabs.Term(
    labels=(
        "WA/P3",
        "WA/PRIORITY 3 POORLY KNOWN",
        "WA/PRIORITY 3 POORLY KNOWN SPECIES",
        "WESTERN AUSTRALIA/P3",
        "WESTERN AUSTRALIA/PRIORITY 3 POORLY KNOWN",
        "WESTERN AUSTRALIA/PRIORITY 3 POORLY KNOWN SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/P3-poorly-known-species", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_P4 = utils.vocabs.Term(
    labels=(
        "WA/P4",
        "WA/PRIORITY 4 RARE NEAR THREATENED AND OTHER SPECIES IN NEED OF MONITORING",
        "WESTERN AUSTRALIA/P4",
        "WESTERN AUSTRALIA/PRIORITY 4 RARE NEAR THREATENED AND OTHER SPECIES IN NEED OF MONITORING",
    ),
    iri=utils.rdf.uri("threatStatus/WA/P4-rare-near-threatened-and-other-species-in-need-of-monitoring", utils.namespaces.EXAMPLE)  # TODO -> Need real URI  # noqa: E501
)
WA_SPECIALLY_PROTECTED_SPECIES = utils.vocabs.Term(
    labels=(
        "WA/SPECIALLY PROTECTED",
        "WA/SPECIALLY PROTECTED SPECIES",
        "WESTERN AUSTRALIA/SPECIALLY PROTECTED",
        "WESTERN AUSTRALIA/SPECIALLY PROTECTED SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/specially-protected-species", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_T = utils.vocabs.Term(
    labels=(
        "WA/T",
        "WA/THREATENED",
        "WA/THREATENED SPECIES",
        "WESTERN AUSTRALIA/T",
        "WESTERN AUSTRALIA/THREATENED",
        "WESTERN AUSTRALIA/THREATENED SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/threatened", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)
WA_VU = utils.vocabs.Term(
    labels=(
        "WA/VU",
        "WA/VULNERABLE",
        "WA/VULNERABLE SPECIES",
        "WESTERN AUSTRALIA/VU",
        "WESTERN AUSTRALIA/VULNERABLE",
        "WESTERN AUSTRALIA/VULNERABLE SPECIES",
    ),
    iri=utils.rdf.uri("threatStatus/WA/vulnerable-species", utils.namespaces.EXAMPLE)  # TODO -> Need real URI
)

# Vocabulary
THREAT_STATUS = utils.vocabs.FlexibleVocabulary(
    vocab_id="THREAT_STATUS",
    definition=rdflib.Literal("A type of threatStatus."),
    base=utils.rdf.uri("bdr-cv/parameter/threatStatus/"),
    scheme=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/5699eca7-9ef0-47a6-bcfb-9306e0e2b85e"),
    broader=utils.rdf.uri("bdr-cv/parameter/threatStatus", utils.namespaces.EXAMPLE),  # TODO -> Need real URI
    default=None,  # No default, ommitted if not provided
    terms=(
        ACT_CRITICALLY_ENDANGERED,
        ACT_ENDANGERED,
        ACT_EXTINCT_IN_THE_WILD,
        ACT_EXTINCT,
        ACT_REGIONALLY_CONSERVATION_DEPENDENT,
        ACT_VULNERABLE,
        EPBC_CAMBA,
        EPBC_CD,
        EPBC_CE,
        EPBC_CITES,
        EPBC_E,
        EPBC_EX,
        EPBC_JAMBA,
        EPBC_KAMBA,
        EPBC_V,
        EPBC_XW,
        NSW_CE,
        NSW_EN,
        NSW_EX,
        NSW_V,
        NT_CE,
        NT_DD,
        NT_EN_EXTINCT_IN_NT,
        NT_EN_EXTINCT_IN_WILD_IN_NT,
        NT_EN,
        NT_EW,
        NT_EX,
        NT_LC_EXTINCT_IN_NT,
        NT_LC,
        NT_NE,
        NT_NT,
        NT_VU_EXTINCT_IN_NT,
        NT_VU,
        QLD_C,
        QLD_CR,
        QLD_E,
        QLD_EX,
        QLD_I,
        QLD_NT,
        QLD_PE,
        QLD_SL,
        QLD_V,
        SA_E,
        SA_R,
        SA_SP,
        SA_SSP,
        SA_V,
        TAS_E,
        TAS_R,
        TAS_V,
        TAS_X,
        VIC_CONSERVATION_DEPENDENT,
        VIC_CRITICALLY_ENDANGERED,
        VIC_ENDANGERED_EXTINCT_IN_VICTORIA,
        VIC_ENDANGERED,
        VIC_EXTINCT_IN_THE_WILD,
        VIC_EXTINCT,
        VIC_RESTRICTED,
        VIC_VULNERABLE,
        WA_CD,
        WA_CR,
        WA_EN,
        WA_EW,
        WA_EX,
        WA_MI,
        WA_OS,
        WA_P1,
        WA_P2,
        WA_P3,
        WA_P4,
        WA_SPECIALLY_PROTECTED_SPECIES,
        WA_T,
        WA_VU,
    ),
)

# Register
utils.vocabs.Vocabulary.register(THREAT_STATUS)
