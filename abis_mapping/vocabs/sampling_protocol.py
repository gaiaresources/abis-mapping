"""Provides sampling protocol vocabulary for the package"""

# Third-Party
import rdflib

# Local
from abis_mapping import utils


# Terms
ACOUSTIC_RECORDING = utils.vocabs.Term(
    labels=("ACOUSTIC RECORDING",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/5f601104-ea57-524d-8a7c-dde7e616f039"),
    description="An acoustic recorder is a device that emits a soundwave at a range of frequencies, and are used to detect and monitor biodiversity in a given area.",
)
ANIMAL_CARCASS_WHOLE = utils.vocabs.Term(
    labels=("ANIMAL CARCASS (WHOLE)",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/71efc83c-2ece-5799-a236-b7e4e9b49b92"),
    description="Refers to the fauna observation method, i.e., any observations made on a carcass (whole), i.e., dead and or decaying animal., Refers to the type of voucher specimen sample, i.e., an animal carcass (full/complete).",
)
ANIMAL_DIGGINGS = utils.vocabs.Term(
    labels=("ANIMAL DIGGINGS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/82e8ae05-1bbe-55b0-addd-78d3e1be62de"),
    description="The type of evidence of a pest animal presence in the form of 'diggings'.",
)
ANIMAL_GUT_WITHIN = utils.vocabs.Term(
    labels=("ANIMAL GUT (WITHIN)",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/a6005006-e7a4-5cd6-b285-c3cb9b6f6c51"),
    description="Animal gut is the portions of the alimentary canal, particularly the stomach and the intestines.",
)
ANIMAL_HAIR_FUR = utils.vocabs.Term(
    labels=("ANIMAL HAIR/FUR",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/fe8cac2d-e965-514a-8138-dadf6f6751fa"),
    description="Animal fur are densely packed hairs on the skin of mammals.",
)
ANIMAL_PELLET = utils.vocabs.Term(
    labels=("ANIMAL PELLET",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/b2086fc8-11ae-53e0-99b2-6e42bd210202"),
    description="Pellets are fecal droppings of animals such as goat, rats, rabbits, wombats, etc., and are often used as a sign/evidence of the presence of the species in the environment.",
)
ANIMAL_SKIN = utils.vocabs.Term(
    labels=("ANIMAL SKIN",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/b28a6ddd-c9c6-5839-9945-028f92707770"),
    description="Skin is the outermost protective layer and the largest organ covering the body of vertebrate animal.",
)
ANIMAL_TRACKING_STATELLITE = utils.vocabs.Term(
    labels=("ANIMAL TRACKING (STATELLITE)",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c21b24dd-4ea9-5c31-af53-8f6a80b40411"),
    description="A method of tracking the movements of fauna species facilitated by the assistance from satellite (i.e., imagery for example).",
)
ANIMAL_TRACKS = utils.vocabs.Term(
    labels=("ANIMAL TRACKS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/8b50e443-c84a-5c85-868c-2fb689524e80"),
    description="Animal tracks are signs in the form of marks or imprints left behind on soil, ground or any related surface indicating the presence of a fauna species., Refers to the fauna observation method, i.e., any signs of a fauna detected from observations of tracks.",
)
BONE_TEETH = utils.vocabs.Term(
    labels=("BONE/TEETH",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/ce300451-6e4f-510b-b95a-14b1cc827bec"),
    description="Bones/teeth are non-perishable remains of mammals that are often divided into skeleton (bones) and dentition (teeth).",
)
BURROW = utils.vocabs.Term(
    labels=("BURROW",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7230bbb8-9f03-5dd0-9ecf-fddfe4bb3c7c"),
    description="A burrow is a hole or tunnel excavated into the ground by an animal to create a space suitable for habitation, temporary refuge, or as a byproduct of locomotion., Burrow is a small tunnel or a hole made by certain ground-dwelling mammals as a place of refuge., Refers to the microhabitat where the targeted fauna was observed. A burrow is a hole or tunnel excavated into the ground by an animal to create a space suitable for habitation, temporary refuge, or as a byproduct of locomotion.",
)
CAGE_TRAP = utils.vocabs.Term(
    labels=("CAGE TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/8f6764de-0f3e-5f6f-b86e-e5e9f6053e24"),
    description="A cage trap is a trap made of metal or galvanised mesh, normally used for trapping mammals., The equipment/method used during a passive, 'targeted fauna survey'. A cage trap is a trap made of metal or galvanised mesh and used in trapping mammals.",
)
DNA = utils.vocabs.Term(
    labels=("DNA",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/6c2cfedc-c95a-5c6f-affb-77a3cc1db64b"),
    description="DNA, or deoxyribonucleic acid, is the hereditary material in almost all living organisms that carries the genetic instructions used in growth, development, functioning, and reproduction. It consists of two long chains of nucleotides twisted into a double helix, with sequences of four types of nitrogen bases (adenine, thymine, cytosine, and guanine) that encode genetic information.",
)
EDNA = utils.vocabs.Term(
    labels=("EDNA",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/4d5d3f71-d98f-5619-9f4d-45330bcb51f3"),
    description="Environment DNA (eDNA) are the DNA that contains genetic information of living organisms representing a specific environmental and is usually sourced from soil, water, etc. , Refers to the method of identification of Vertebrate fauna. Taxon is identified using DNA sequencing techniques from environmental samples (eDNA).",
)
EGGS_EGGSHELL = utils.vocabs.Term(
    labels=("EGGS/EGGSHELL",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9890b2a0-29c0-5122-b592-3ccd445abc70"),
    description="An animal egg, or ovum, is the female reproductive cell (gamete) in many animals and vay in shape, size and structure. Egg shells are outer protctive layer that surrounds the egg of many animals. The animal eggs/egg shells here represent particular life stage of animal and often used as a sign/evidence to detect their presence in its habitat.",
)
ELLIOTT_TRAP = utils.vocabs.Term(
    labels=("ELLIOTT TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d1bdaf17-c484-59c6-84a0-8344a5ce5b5c"),
    description="The equipment/method used during a passive, 'fauna survey'. Elliott trapping is a technique used to trap small to medium sized mammals. The are usually hinged design that allows trapping to be conducted by folding into a compact panel and easy transport to field locations and storage., The equipment/method used during a passive, 'targeted fauna survey'. Elliott trapping is a technique used to trap small to medium sized mammals. The are usually hinged design that allows trapping to be conducted by folding into a compact panel and easy transport to field locations and storage.",
)
EXOSKELETON = utils.vocabs.Term(
    labels=("EXOSKELETON",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/eb3a1100-9028-5562-a12d-b4b3d6e6d92f"),
    description="Exoskeleton is the outer rigid covering of an invertebrate fauna with its structural features generally intact.",
)
FEATHER = utils.vocabs.Term(
    labels=("FEATHER",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/18d4c44d-4c5b-57b2-8eb1-37f3ba0826a0"),
    description="Feathers are light, upright epidermal outgrowths that form the external covering of the body of birds. Feathers include the smaller down feathers and the larger contour and flight feathers., Refers to the type of voucher specimen sample. Feathers are one of the epidermal growths that form the distinctive outer covering, or plumage, on birds.",
)
FOSSIL_SUBFOSSIL = utils.vocabs.Term(
    labels=("FOSSIL/SUBFOSSIL",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/2000e7d5-9851-54e7-8ade-379a07c0cfab"),
    description="Fossils are preserved remains of animal or plant parts, usually of a prehistoric origin. Whereas, a sub-fossil are remains (usually skeletal) of animals that are not ancient enough to qualify as a fossil.",
)
FUNNEL_TRAP = utils.vocabs.Term(
    labels=("FUNNEL TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/970058a7-946d-5a5d-bb5b-c5b801a4def4"),
    description="The equipment/method used in a 'fauna survey'. Funnel trap is a trapping method used in trapping insects/invertebrates. Funnel traps are made of nested black funnels (up to as many as 12). Insects fall through the funnels to a cup that is filled with a preservative., The equipment/method used in a 'targeted fauna survey'. Funnel trap is a trapping method used in trapping insects/invertebrates. Funnel traps are made of nested black funnels (up to as many as 12). Insects fall through the funnels to a cup that is filled with a preservative.",
)
GPS_TRACKING = utils.vocabs.Term(
    labels=("GPS TRACKING",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/cb745f17-e984-5b2b-b8d4-e3d3f784d93f"),
    description="Geospatial tracking devices are portable units designed to monitor and track location. They use satellite navigation to determine movement and establish geographic positions.",
)
HAIR_TUBE = utils.vocabs.Term(
    labels=("HAIR TUBE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/7ed366d3-9c85-5974-863d-127d1ff103ce"),
    description="Hair Tubes are short sections of PVC pipe lined with pieces of double-sided sticky-tape and useful to obtain hair/fur samples of animals., Refers to the targeted fauna observation method, i.e., any observations on a fauna made using 'Hair Tubes', which are short sections of PVC pipe lined with pieces of double-sided sticky-tape.",
)
HARP_TRAP = utils.vocabs.Term(
    labels=("HARP TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/b7a02786-f651-5199-877b-96d5dc4c66c6"),
    description="Refers to the fauna observation method, i.e., any observations made on a fauna captured in a 'Harp trap' (especially designed for bats). They are particularly useful in situations where bats in flight can be channeled through a natural funnel such as above a water course, a cave or mine entrance or a clear area within a forest.",
)
HEARD = utils.vocabs.Term(
    labels=("HEARD",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/ffb1c491-bbb1-5823-ac03-0543f9a9627a"),
    description="The method of bird sighting in the form of calls, or acoustic signals., The method of fauna sighting in the form of calls, or acoustic signals.",
)
HUMAN_OBSERVATION = utils.vocabs.Term(
    labels=("HUMAN OBSERVATION",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/ea1d6342-1901-4f88-8482-3111286ec157"),
    description="An observation performed by a human.",
)
LIGHT_TRAP = utils.vocabs.Term(
    labels=("LIGHT TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/2ee3f6d7-6340-50c6-b9e3-1b115d75100b"),
    description="Light trapping is designed for collecting flying insects attracted to ultra violet light and is useful for sampling insect populations., The equipment/method used during a passive, 'targeted fauna survey'. Light trapping is designed for collecting flying insects attracted to ultra violet light and is useful for sampling insect populations.",
)
MALAISE_TRAP = utils.vocabs.Term(
    labels=("MALAISE TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/8feff6f2-9d17-5bce-8933-d877198ea1ac"),
    description="A Malaise trap is a type of insect trap primarily used to capture invertebrates. They are large, tent-like structure effective in capturing flying insects (e.g., members of Hymenoptera and Diptera)., Refers to the targeted fauna observation method, i.e., any observations on a fauna captured using a malaise trap. A Malaise trap is a type of insect trap primarily used to capture invertebrates. They are large, tent-like structure effective in capturing flying insects (e.g., members of Hymenoptera and Diptera).",
)
MIST_NET = utils.vocabs.Term(
    labels=("MIST NET",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/8ca1c330-b64a-5f97-aab4-9023fddaf009"),
    description="Refers to the fauna observation method, i.e., any observations on a fauna captured using mist nets. The net is made of a very fine diameter cord, which is almost invisible when set up and is often used to capture birds, because they fail to see it, and fly straight into it., Refers to the targeted fauna observation method, i.e., any observations on a fauna captured using mist nets. The net is made of a very fine diameter cord, which is almost invisible when set up and is often used to capture birds, because they fail to see it, and fly straight into it.",
)
NEST = utils.vocabs.Term(
    labels=("NEST",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/b300ac98-8599-5de9-b99b-a2a17055cef8"),
    description="A nest is a place of refuge to hold an animal's eggs or provide a place to live or raise offspring.",
)
NO_STATED_METHOD = utils.vocabs.Term(
    labels=("NO STATED METHOD",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/a8db263e-7a39-5b85-a5d2-8e1af7ce1e39"),
    description="Refers to NO recognised method of observation stated for a target fauna.",
)
NONE = utils.vocabs.Term(
    labels=("NONE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/521214ab-a82f-55e9-910a-72b4de552a6e"),
    description="Refers to No observation method of a target fauna., Refers to the targeted fauna observation method, i.e., 'No' standard observation methods were applied.",
)
OBSERVATION_METHOD_AFTER_CALL_PLAYBACK = utils.vocabs.Term(
    labels=("OBSERVATION METHOD - AFTER CALL PLAYBACK",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c85935df-7a5d-4321-9915-efb7116e9020"),
    description="After call playback, is a method used for fauna observations (usually birds) and involves pre-recorded call playback to detect the presence of a target species in the survey area.",
)
OBSERVATION_METHOD_ANIMAL_DEN = utils.vocabs.Term(
    labels=("OBSERVATION METHOD - ANIMAL DEN",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f338f4ef-5390-4292-b958-1a647a276b63"),
    description="A den is a place of refuge for many mammals and are usually either buried deep underground or built by the animal to create a secret shelter., Refers to the microhabitat where the fauna was observed. A den is a place of refuge for many mammals and are usually either buried deep underground or built by the animal to create a secret shelter.",
)
OBSERVATION_METHOD_ANIMAL_ODOUR = utils.vocabs.Term(
    labels=("OBSERVATION METHOD - ANIMAL ODOUR",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9dc775ac-e68d-4df2-87ea-1b3057c88fdc"),
    description="Animal odour or pheromones are distinct secretions of animals, often used as a sign/evidence of their presence in its habitat., Refers to the type of fauna observation method, which involves detection of a fauna species via its odour or pheromones.",
)
OTHER_SPECIFY = utils.vocabs.Term(
    labels=("OTHER (SPECIFY)",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/565511a8-c50b-53fb-8f59-995e52a01ed2"),
    description="Other types of liquid preservative used to store invertebrate samples., Refers to the any Other type of substrate/s used for fauna signs-based observation., Represents any 'Other' categorical collection NOT listed in the given collection., Represents any 'other' categorical collection NOT listed.",
)
PAN_TRAP = utils.vocabs.Term(
    labels=("PAN TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/9a7c0772-85f7-5f0b-8e6d-73b312137261"),
    description="A pan trap is a type of insect trap primarily used to capture small invertebrates (e.g., members of Hymenoptera) and often used to sample the abundance and diversity of insects., Refers to the targeted fauna observation method, i.e., any observations made from fauna captures in a pan trap. A pan trap is a type of insect trap primarily used to capture small invertebrates (e.g., members of Hymenoptera) and often used to sample the abundance and diversity of insects., The type/method of invertebrate fauna sampling implemented. Pan trapping consists of small, coloured bowls placed on the ground, either filled with water and a small amount of dishwashing liquid for sampling over one day, or propylene glycol for sampling over a longer duration.",
)
PELLET_WITHIN = utils.vocabs.Term(
    labels=("PELLET (WITHIN)",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/488ee615-5c57-5080-b991-04b4bfe05d7a"),
    description="Pellets are fecal droppings of animals such as goat, rats, rabbits, wombats, etc., and are often used as a sign/evidence of the presence of the species in the environment. 'Within pellet' here represents an observation method (tier-2) that involves searching for any signs/evidence of a fauna species within a scat.",
)
PITFALL_TRAP = utils.vocabs.Term(
    labels=("PITFALL TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/aa78fa0e-3bd0-5c87-8ac7-0779f0699a11"),
    description="Refers to the fauna observation method, i.e., any observations made from fauna captures in a pitfall trap. A pitfall trap is a simple device used to catch small animals , particularly insects and other invertebrates , that spend most of their time on the ground., Refers to the targeted fauna observation method, i.e., any observations made from fauna captures in a pitfall trap. A pitfall trap is a simple device used to catch small animals , particularly insects and other invertebrates , that spend most of their time on the ground.",
)
RADIO_TRACKING = utils.vocabs.Term(
    labels=("RADIO TRACKING",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/63199f31-468f-5bb1-bc4e-4e4a873cc261"),
    description="Refers to the fauna observation method, i.e., any signs of a fauna with the assistance of radio tracking device/s.",
)
REMOTE_CAMERA_DEVICE = utils.vocabs.Term(
    labels=("REMOTE CAMERA DEVICE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d9ded7e1-e012-53c0-a612-3f5585281cef"),
    description="Remote camera device are special devices that can be programmed to capture media (picture, videos) in places where humans cannot be physically present, and can be controlled remotely over a wireless network.",
)
SCATS = utils.vocabs.Term(
    labels=("SCATS",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d4d09df7-25db-5f56-8a0f-05c377e18c6b"),
    description="Faeces/faecal pellets/dung/droppings of animals. Often individual or scattered pellets (e.g. rabbit), or clumped pellet groups (e.g. deer). Their deposition will be influenced by diet (wet diet often causes clumping of pellets) and their size can reflect age (adult/juvenile). Scat surveys provide an estimate of relative abundances suitable for both herbivores and predators.",
)
SCATS_WITHIN = utils.vocabs.Term(
    labels=("SCATS (WITHIN)",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/057f361a-8abf-58ed-83fd-c57730076622"),
    description="Scats are fecal droppings of animals and are often represented by most to mark their territory. 'Within scats' here represents an observation method (tier-2) that involves searching for any signs/evidence of a fauna species within a scat.",
)
SCENT_PAD = utils.vocabs.Term(
    labels=("SCENT PAD",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/2ae64fa5-44b2-54a7-a90f-bcf37fb2378c"),
    description="Scent pads are specific pads that are used as lures duing fauna observations.",
)
SCRATCHINGS_ARBOREAL = utils.vocabs.Term(
    labels=("SCRATCHINGS (ARBOREAL)",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/fb1b5882-1e51-503f-874d-b1309df36508"),
    description="Refers to the fauna observation method, i.e., any signs of a fauna detected from observations of scratchings on a tree.",
)
SCRATCHINGS_GROUND = utils.vocabs.Term(
    labels=("SCRATCHINGS (GROUND)",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/c4291c6d-3873-5f01-9a03-40f0e8209f5a"),
    description="Scratchings are common traits of certain mammals leaving scars on trees, rocks etc.",
)
SHELL = utils.vocabs.Term(
    labels=("SHELL",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/ad89e464-2ef1-5342-bdbc-20a71eccd260"),
    description="A shell is a hard, rigid outer layer, which has evolved in a very wide variety of different animals, including molluscs, crustaceans, turtles and tortoises.",
)
SIGHTING = utils.vocabs.Term(
    labels=("SIGHTING",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/1c11410a-2465-56e0-a258-8db9d68da5ae"),
    description="An observation method made by direct sighting of fauna in its habitat.",
)
SPOTLIGHTING = utils.vocabs.Term(
    labels=("SPOTLIGHTING",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/db0cb2f2-e9f8-5679-a566-afce45b28da0"),
    description="Spotlighting technique is a method used for fauna observations during the night and assists surveyors target nocturnal animals, using off-road vehicles and high-powered lights, spotlights, lamps or flashlights.",
)
SWEEP_NET = utils.vocabs.Term(
    labels=("SWEEP NET",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f2b4d479-e3a3-5855-b5bb-24350de1be22"),
    description="Sweep nets are usually used for capturing insects using a number of sweeps. The net is made of fine diameter mesh fitted to a metal handle to trap invertebrates in air., The equipment/method used during a passive, 'targeted fauna survey'. Sweep nets are usually used for capturing insects using a number of sweeps. The net is made of fine diameter mesh fitted to a metal handle to trap invertebrates in air.",
)
TRACKING_PAD = utils.vocabs.Term(
    labels=("TRACKING PAD",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/d6aa5024-ac75-40f3-95bd-12d2f0409088"),
    description="A tracking pad is an artificial pad made of loose material (such as sand for example) that are used to study and observe animal tracks. These pads are often designed to be delpoyed in habitats where animal activity/movements are high., Refers to the type of substrate used for fauna signs-based observation. A tracking pad is an artificial pad made of loose material (such as sand for example) that are used to study animal tracks in a fauna survey.",
)
ULTRASONIC_RECORDING_DEVICE = utils.vocabs.Term(
    labels=("ULTRASONIC RECORDING DEVICE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/e405c9c0-2c1f-5dee-8d63-1edfc6ee5b36"),
    description="Ultrasound recorders are devices that send high-frequency sound waves in the environment to create images or detect objects and movements within various mediums, such as a mammalian body or other environments. They are popular for wildlife monitoring, biodiversity surveys, habitat assessments and echolocation studies (e.g., bats).",
)
UNKNOWN = utils.vocabs.Term(
    labels=("UNKNOWN",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f6b0f6d8-16d8-5dd7-b1b7-66b0c020b96f"),
    description="Refers to the fire history of the plot, unknown., Unknown (unable to be determined)., Unknown capture status., Unknown position., Unknown- unable to be determined., Unknown/unable to be determined.",
)
UNKNOWN_TRAP_TYPE = utils.vocabs.Term(
    labels=("UNKNOWN TRAP TYPE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/f6b0f6d8-16d8-5dd7-b1b7-66b0c020b96f"),
    description="Refers to the fire history of the plot, unknown., Unknown (unable to be determined)., Unknown capture status., Unknown position., Unknown, unable to be determined., Unknown/unable to be determined.",
)
UNSPECIFIED_METHOD = utils.vocabs.Term(
    labels=("UNSPECIFIED",),
    iri=rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/fd083167-3cbf-4f7e-a611-4550a5926a8b"),
    description="The method used was not included in the data.",
)
WALLOW = utils.vocabs.Term(
    labels=("WALLOW",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/950726bd-1334-524b-89d2-3ed65f63b2a1"),
    description="A wallow is a depression containing mud or shallow water, formed by wallowing of large mammals., Wallow is a depression containing mud or shallow water, formed by the wallowing of large mammals such as a buffallo for example.",
)
WATER_SAMPLE = utils.vocabs.Term(
    labels=("WATER SAMPLE",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/bbb5ade2-3f5d-5033-a12d-aa9607fe6d8d"),
    description="Water samples are representative samples of a given habitat that serve as a source to study the chemical composition and detect the presence of fauna species (DNA).",
)
WET_PITFALL_TRAP = utils.vocabs.Term(
    labels=("WET PITFALL TRAP",),
    iri=rdflib.URIRef("https://linked.data.gov.au/def/nrm/4caf0cde-9ffb-56c2-bdc6-17c4c2a7275a"),
    description="Refers to the fauna observation method, i.e., any observations made from fauna captures using a wet pitfall trap.",
)


# Vocabulary
class SamplingProtocol(utils.vocabs.FlexibleVocabulary):
    vocab_id = "SAMPLING_PROTOCOL"
    definition = rdflib.Literal("A type of samplingProtocol.")
    base = "bdr-cv/methods/samplingProtocol/"
    proposed_scheme = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/2fd44aca-168f-4177-b393-0688ce38102c")
    broader = rdflib.URIRef("http://linked.data.gov.au/def/tern-cv/4c489862-0348-4ed8-afae-ed5bb296b034")
    default = "UNSPECIFIED_METHOD"
    terms = (
        ACOUSTIC_RECORDING,
        ANIMAL_CARCASS_WHOLE,
        ANIMAL_DIGGINGS,
        ANIMAL_GUT_WITHIN,
        ANIMAL_HAIR_FUR,
        ANIMAL_PELLET,
        ANIMAL_SKIN,
        ANIMAL_TRACKING_STATELLITE,
        ANIMAL_TRACKS,
        BONE_TEETH,
        BURROW,
        CAGE_TRAP,
        DNA,
        EDNA,
        EGGS_EGGSHELL,
        ELLIOTT_TRAP,
        EXOSKELETON,
        FEATHER,
        FOSSIL_SUBFOSSIL,
        FUNNEL_TRAP,
        GPS_TRACKING,
        HAIR_TUBE,
        HARP_TRAP,
        HEARD,
        HUMAN_OBSERVATION,
        LIGHT_TRAP,
        MALAISE_TRAP,
        MIST_NET,
        NEST,
        NO_STATED_METHOD,
        NONE,
        OBSERVATION_METHOD_AFTER_CALL_PLAYBACK,
        OBSERVATION_METHOD_ANIMAL_DEN,
        OBSERVATION_METHOD_ANIMAL_ODOUR,
        OTHER_SPECIFY,
        PAN_TRAP,
        PELLET_WITHIN,
        PITFALL_TRAP,
        RADIO_TRACKING,
        REMOTE_CAMERA_DEVICE,
        SCATS,
        SCATS_WITHIN,
        SCENT_PAD,
        SCRATCHINGS_ARBOREAL,
        SCRATCHINGS_GROUND,
        SHELL,
        SIGHTING,
        SPOTLIGHTING,
        SWEEP_NET,
        TRACKING_PAD,
        ULTRASONIC_RECORDING_DEVICE,
        UNKNOWN,
        UNKNOWN_TRAP_TYPE,
        UNSPECIFIED_METHOD,
        WALLOW,
        WATER_SAMPLE,
        WET_PITFALL_TRAP,
    )


# Register
utils.vocabs.register(SamplingProtocol)
