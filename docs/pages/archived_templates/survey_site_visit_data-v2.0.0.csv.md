---
title: Systematic Survey Site Visit Data Template - v2.0.0
 - Archived

summary: A template for systematic survey site visit data
---
<small>
**survey_site_visit_data** v2.0.0
</small>


!!! failure "Template Archived"

    This Template is archived, and is no longer available for use.


# SYSTEMATIC SURVEY SITE VISIT DATA TEMPLATE INSTRUCTIONS

## Intended Usage
This Systematic Survey Site Visit Data template should be used to record data related
to the visit made to the Site area during a systematic survey.

This Systematic Survey Site Visit template **must be used in combination** with the 
Systematic Survey Site Data template.

Templates have been provided to facilitate integration of data into the Biodiversity Data
Repository (BDR) database. Not all types of data have been catered for in the available
templates at this stage - if you are unable to find a suitable template, please
contact <bdr-support@dcceew.gov.au> to make us aware of your data needs.

## Data Validation Requirements:
For data validation, you will need your data file to:
- be the correct **file format**,
- have **fields that match the template downloaded** (do not remove, or change the order of fields),
- have extant values for **mandatory fields** (see Table 1), and
- comply with all **data value constraints**,
- align with existing controlled [vocabularies](#appendix-i-vocabulary-list) wherever possible, but 
new terms may be submitted for consideration and will not cause a validation error.

Additional fields may be added **after the templated fields** (noting that the data type 
is not assumed and values will be encoded as strings).

### FILE FORMAT
- The systematic survey site visit data template is a [UTF-8](#appendix-iii-utf-8) encoded csv (not Microsoft
  Excel Spreadsheets). Be sure to save this file with your data as a .csv (UTF-8) as follows,
  otherwise it will not pass the csv validation step upon upload.
  <br>`[MS Excel: Save As > More options > Tools > Web options > Save this document as >
  Unicode (UTF-8)]`<br>
  otherwise it will not pass the csv validation step upon upload.
- **Do not include empty rows**.

### FILE NAME

When making a manual submission to the Biodiversity Data Repository,
the file name must include the version number
of this biodiversity data template (`v2.0.0`).
The following format is an example of a valid file name:

`data_descripion-v2.0.0-additional_description.csv`

where:

* `data_description`: A short description of the data (e.g. `survey_site_visits`, `test_data`).
* `v2.0.0`: The version number of this template.
* `additional_description`: (Optional) Additional description of the data, if needed (e.g. `test_data`).
* `.csv`: Ensure the file name ends with `.csv`.

For example, `survey_site_visits-v2.0.0-test_data.csv` or `test_data-v2.0.0.csv`

### FILE SIZE
MS Excel imposes a limit of 1,048,576 rows on a spreadsheet, limiting a CSV file to the
header row followed by 1,048,575 occurrences. Furthermore, MS Excel has a 32,767 character
limit on individual cells in a spreadsheet. These limits may be overcome by using or
editing CSV files with other software.

Larger datasets may be more readily ingested using the API interface. Please contact
<bdr-support@dcceew.gov.au> to make us aware of your data needs.

## TEMPLATE FIELDS
The template contains the field names in the top row. Table 1 will assist you in transferring
your data to the template indicating:

- **Field name** in the template (and an external link to the [Data standard](https://linkeddata.tern.org.au/)
  for that field where relevant);
- **Description** of the field;
- **Required** i.e. whether the field is **<font color="Crimson">mandatory</font>,
<font color="DarkGoldenRod">conditionally mandatory</font>, or optional**;
- **Format** (datatype) required for the data values for example text (string), number
  (integer, float), or date;
- **Example** of an entry or entries for that field; and
- **[Vocabulary links](#appendix-i-vocabulary-list)** within this document (for example pick list values) where
  relevant. The fields that have suggested values options for the fields in Table 1 are
  listed in Table 2 in alphabetical order of the field name.

### ADDITIONAL FIELDS
Data that does not match the existing template fields may be added as additional columns in
the CSV files after the templated fields.
For example, `instrumentType`, `instrumentIdentifier`, `weatherConditions`.

<ins>Table 1: Systematic Survey Site Visit data template fields with descriptions, conditions, datatype format, and examples.</ins>

|Field #|Name|Description|Mandatory / Optional|Datatype Format|Examples|
|:---:|:---|:---|:---:|:---:|:---|
|1|<a name="surveyID-field"></a>surveyID|The identifier of the Survey that the Site is related to in this dataset.|Optional|String|AR220-01|
|2|<a name="siteID-field"></a>siteID|A unique within dataset string identifier for the site. Valid values include strings that are used specifically for this survey or URIs from BDR Sites that have been established in previous surveys.|**<font color="Crimson">Mandatory</font>**|String|P1|
|3|<a name="siteIDSource-field"></a>siteIDSource|The organisation that assigned the SiteID to this Site|Optional|String|TERN|
|4|<a name="siteVisitID-field"></a>siteVisitID|The unique key assigned to a visit. A visit is a time distinct assessment conducted within a survey at a designated site.|**<font color="Crimson">Mandatory</font>**|String|CPXEI0000001|
|5|<a name="siteVisitStart-field"></a>siteVisitStart|The temporal start of when the Site was being used to collect data for the survey. Expected values include date, dateTime, dateTimeStamp.|**<font color="Crimson">Mandatory</font>**|Timestamp|2016-02-28|
|6|<a name="siteVisitEnd-field"></a>siteVisitEnd|The temporal end of when the Site was being used to collect data for the survey. Expected values include date, dateTime, dateTimeStamp.|Optional|Timestamp|2016-02-28|
|7|<a name="visitOrgs-field"></a>visitOrgs|The names of the organisations responsible for recording the original Occurrence.|Optional|List|NSW Dept of Planning, Industry and Environment.|
|8|<a name="visitObservers-field"></a>visitObservers|A list (concatenated and separated using \|) of names of people, groups, or organisations responsible for recording the original Occurrence.|Optional|List|Oliver P. Pearson \| Anita K. Pearson|
|9|<a name="condition-field"></a>condition|The state of a patch of vegetation at the time of sampling relative to some specified standard or benchmark (where available).|Optional|String|Burnt|
|10|<a name="targetTaxonomicScope-field"></a>targetTaxonomicScope|The taxonomic group targeted for sampling during the Site Visit|Optional|String|Coleoptera<br>([Vocabulary link](#targetTaxonomicScope-vocabularies))|
|11|<a name="protocolName-field"></a>protocolName|Categorical descriptive name for the method used during the Site Visit.|Optional|String|HARD TRAP<br>([Vocabulary link](#protocolName-vocabularies))|
|12|<a name="protocolDescription-field"></a>protocolDescription|A detailed description of the method used during the Site Visit. The description may include deviations from a protocol referred to in eco:protocolReferences. Recommended good practice is to provide information about instruments used, calibration, etc.|Optional|String|Three conventional harp traps (3.2m ht x 2.2m w) were established in flight path zones for a period of 4 hrs at dawn and dusk for a total of 10 trap nights. Traps were visited on an hourly basis during each deployment period and the trap catch recorded for species, size, weight, sex, age and maternal status.|
|13|<a name="samplingEffortValue-field"></a>samplingEffortValue|Similar to eco:samplingEffortValue. The total sampling effort value. A samplingEffortValue must have a corresponding samplingEffortUnit|**<font color="DarkGoldenRod">Mandatory if samplingEffortUnit is provided.</font>**|String|20 x 12|
|14|<a name="samplingEffortUnit-field"></a>samplingEffortUnit|Similar to eco:samplingEffortUnit. The units associated with samplingEffortValue.|**<font color="DarkGoldenRod">Mandatory if samplingEffortValue is provided.</font>**|String|trapDays<br>([Vocabulary link](#samplingEffortUnit-vocabularies))|


## APPENDICES
### APPENDIX-I: Vocabulary List
Data validation does not require adherence to the vocabularies for the various vocabularied fields.
These vocabularies are merely provided as a means of assistance in developing consistent language
within the database. New terms may be added to more appropriately describe your data that goes 
beyond the current list.

<ins>Table 2: Suggested values for controlled vocabulary fields in the template. Each term has a preferred label with a definition to aid understanding
of its meaning. For some terms, alternative
labels with similar semantics are provided. </ins>

|Template field name|Preferred label|Definition|Alternate label|
|:---|:---|:---|:---|
|<a name="protocolName-vocabularies"></a>protocolName|ACOUSTIC RECORDING|An acoustic recorder is a device that emits a soundwave at a range of frequencies, and are used to detect and monitor biodiversity in a given area.||
|protocolName|ANIMAL PELLET|Pellets are fecal droppings of animals such as goat, rats, rabbits, wombats, etc., and are often used as a sign/evidence of the presence of the species in the environment.||
|protocolName|ANIMAL TRACKING (STATELLITE)|A method of tracking the movements of fauna species facilitated by the assistance from satellite (i.e., imagery for example).||
|protocolName|ANIMAL TRACKS|Animal tracks are signs in the form of marks or imprints left behind on soil, ground or any related surface indicating the presence of a fauna species., Refers to the fauna observation method, i.e., any signs of a fauna detected from observations of tracks.||
|protocolName|BURROW|A burrow is a hole or tunnel excavated into the ground by an animal to create a space suitable for habitation, temporary refuge, or as a byproduct of locomotion., Burrow is a small tunnel or a hole made by certain ground-dwelling mammals as a place of refuge., Refers to the microhabitat where the targeted fauna was observed. A burrow is a hole or tunnel excavated into the ground by an animal to create a space suitable for habitation, temporary refuge, or as a byproduct of locomotion.||
|protocolName|CAGE TRAP|A cage trap is a trap made of metal or galvanised mesh, normally used for trapping mammals., The equipment/method used during a passive, 'targeted fauna survey'. A cage trap is a trap made of metal or galvanised mesh and used in trapping mammals.||
|protocolName|EDNA|Environment DNA (eDNA) are the DNA that contains genetic information of living organisms representing a specific environmental and is usually sourced from soil, water, etc. , Refers to the method of identification of Vertebrate fauna. Taxon is identified using DNA sequencing techniques from environmental samples (eDNA).||
|protocolName|ELLIOTT TRAP|The equipment/method used during a passive, 'fauna survey'. Elliott trapping is a technique used to trap small to medium sized mammals. The are usually hinged design that allows trapping to be conducted by folding into a compact panel and easy transport to field locations and storage., The equipment/method used during a passive, 'targeted fauna survey'. Elliott trapping is a technique used to trap small to medium sized mammals. The are usually hinged design that allows trapping to be conducted by folding into a compact panel and easy transport to field locations and storage.||
|protocolName|FOSSIL/SUBFOSSIL|Fossils are preserved remains of animal or plant parts, usually of a prehistoric origin. Whereas, a sub-fossil are remains (usually skeletal) of animals that are not ancient enough to qualify as a fossil.||
|protocolName|FUNNEL TRAP|The equipment/method used in a 'fauna survey'. Funnel trap is a trapping method used in trapping insects/invertebrates. Funnel traps are made of nested black funnels (up to as many as 12). Insects fall through the funnels to a cup that is filled with a preservative., The equipment/method used in a 'targeted fauna survey'. Funnel trap is a trapping method used in trapping insects/invertebrates. Funnel traps are made of nested black funnels (up to as many as 12). Insects fall through the funnels to a cup that is filled with a preservative.||
|protocolName|GPS TRACKING|Geospatial tracking devices are portable units designed to monitor and track location. They use satellite navigation to determine movement and establish geographic positions.||
|protocolName|HAIR TUBE|Hair Tubes are short sections of PVC pipe lined with pieces of double-sided sticky-tape and useful to obtain hair/fur samples of animals., Refers to the targeted fauna observation method, i.e., any observations on a fauna made using 'Hair Tubes', which are short sections of PVC pipe lined with pieces of double-sided sticky-tape.||
|protocolName|HARP TRAP|Refers to the fauna observation method, i.e., any observations made on a fauna captured in a 'Harp trap' (especially designed for bats). They are particularly useful in situations where bats in flight can be channeled through a natural funnel such as above a water course, a cave or mine entrance or a clear area within a forest.||
|protocolName|HEARD|The method of bird sighting in the form of calls, or acoustic signals., The method of fauna sighting in the form of calls, or acoustic signals.||
|protocolName|HUMAN OBSERVATION|An observation performed by a human.||
|protocolName|LIGHT TRAP|Light trapping is designed for collecting flying insects attracted to ultra violet light and is useful for sampling insect populations., The equipment/method used during a passive, 'targeted fauna survey'. Light trapping is designed for collecting flying insects attracted to ultra violet light and is useful for sampling insect populations.||
|protocolName|MALAISE TRAP|A Malaise trap is a type of insect trap primarily used to capture invertebrates. They are large, tent-like structure effective in capturing flying insects (e.g., members of Hymenoptera and Diptera)., Refers to the targeted fauna observation method, i.e., any observations on a fauna captured using a malaise trap. A Malaise trap is a type of insect trap primarily used to capture invertebrates. They are large, tent-like structure effective in capturing flying insects (e.g., members of Hymenoptera and Diptera).||
|protocolName|MIST NET|Refers to the fauna observation method, i.e., any observations on a fauna captured using mist nets. The net is made of a very fine diameter cord, which is almost invisible when set up and is often used to capture birds, because they fail to see it, and fly straight into it., Refers to the targeted fauna observation method, i.e., any observations on a fauna captured using mist nets. The net is made of a very fine diameter cord, which is almost invisible when set up and is often used to capture birds, because they fail to see it, and fly straight into it.||
|protocolName|NEST|A nest is a place of refuge to hold an animal's eggs or provide a place to live or raise offspring.||
|protocolName|NO STATED METHOD|Refers to NO recognised method of observation stated for a target fauna.|UNSPECIFIED|
|protocolName|NONE|Refers to No observation method of a target fauna., Refers to the targeted fauna observation method, i.e., 'No' standard observation methods were applied.||
|protocolName|OBSERVATION METHOD - AFTER CALL PLAYBACK|After call playback, is a method used for fauna observations (usually birds) and involves pre-recorded call playback to detect the presence of a target species in the survey area.||
|protocolName|OBSERVATION METHOD - ANIMAL DEN|A den is a place of refuge for many mammals and are usually either buried deep underground or built by the animal to create a secret shelter., Refers to the microhabitat where the fauna was observed. A den is a place of refuge for many mammals and are usually either buried deep underground or built by the animal to create a secret shelter.||
|protocolName|OBSERVATION METHOD - ANIMAL ODOUR|Animal odour or pheromones are distinct secretions of animals, often used as a sign/evidence of their presence in its habitat., Refers to the type of fauna observation method, which involves detection of a fauna species via its odour or pheromones.||
|protocolName|PAN TRAP|A pan trap is a type of insect trap primarily used to capture small invertebrates (e.g., members of Hymenoptera) and often used to sample the abundance and diversity of insects., Refers to the targeted fauna observation method, i.e., any observations made from fauna captures in a pan trap. A pan trap is a type of insect trap primarily used to capture small invertebrates (e.g., members of Hymenoptera) and often used to sample the abundance and diversity of insects., The type/method of invertebrate fauna sampling implemented. Pan trapping consists of small, coloured bowls placed on the ground, either filled with water and a small amount of dishwashing liquid for sampling over one day, or propylene glycol for sampling over a longer duration.||
|protocolName|PELLET (WITHIN)|Pellets are fecal droppings of animals such as goat, rats, rabbits, wombats, etc., and are often used as a sign/evidence of the presence of the species in the environment. 'Within pellet' here represents an observation method (tier-2) that involves searching for any signs/evidence of a fauna species within a scat.||
|protocolName|PITFALL TRAP|Refers to the fauna observation method, i.e., any observations made from fauna captures in a pitfall trap. A pitfall trap is a simple device used to catch small animals , particularly insects and other invertebrates , that spend most of their time on the ground., Refers to the targeted fauna observation method, i.e., any observations made from fauna captures in a pitfall trap. A pitfall trap is a simple device used to catch small animals , particularly insects and other invertebrates , that spend most of their time on the ground.||
|protocolName|RADIO TRACKING|Refers to the fauna observation method, i.e., any signs of a fauna with the assistance of radio tracking device/s.||
|protocolName|REMOTE CAMERA DEVICE|Remote camera device are special devices that can be programmed to capture media (picture, videos) in places where humans cannot be physically present, and can be controlled remotely over a wireless network.||
|protocolName|SCATS|Faeces/faecal pellets/dung/droppings of animals. Often individual or scattered pellets (e.g. rabbit), or clumped pellet groups (e.g. deer). Their deposition will be influenced by diet (wet diet often causes clumping of pellets) and their size can reflect age (adult/juvenile). Scat surveys provide an estimate of relative abundances suitable for both herbivores and predators.||
|protocolName|SCATS (WITHIN)|Scats are fecal droppings of animals and are often represented by most to mark their territory. 'Within scats' here represents an observation method (tier-2) that involves searching for any signs/evidence of a fauna species within a scat.||
|protocolName|SCENT PAD|Scent pads are specific pads that are used as lures duing fauna observations.||
|protocolName|SCRATCHINGS (ARBOREAL)|Refers to the fauna observation method, i.e., any signs of a fauna detected from observations of scratchings on a tree.||
|protocolName|SCRATCHINGS (GROUND)|Scratchings are common traits of certain mammals leaving scars on trees, rocks etc.||
|protocolName|SHELL|A shell is a hard, rigid outer layer, which has evolved in a very wide variety of different animals, including molluscs, crustaceans, turtles and tortoises.||
|protocolName|SIGHTING|An observation method made by direct sighting of fauna in its habitat.||
|protocolName|SPOTLIGHTING|Spotlighting technique is a method used for fauna observations during the night and assists surveyors target nocturnal animals, using off-road vehicles and high-powered lights, spotlights, lamps or flashlights.||
|protocolName|SWEEP NET|Sweep nets are usually used for capturing insects using a number of sweeps. The net is made of fine diameter mesh fitted to a metal handle to trap invertebrates in air., The equipment/method used during a passive, 'targeted fauna survey'. Sweep nets are usually used for capturing insects using a number of sweeps. The net is made of fine diameter mesh fitted to a metal handle to trap invertebrates in air.||
|protocolName|TRACKING PAD|A tracking pad is an artificial pad made of loose material (such as sand for example) that are used to study and observe animal tracks. These pads are often designed to be delpoyed in habitats where animal activity/movements are high., Refers to the type of substrate used for fauna signs-based observation. A tracking pad is an artificial pad made of loose material (such as sand for example) that are used to study animal tracks in a fauna survey.||
|protocolName|ULTRASONIC RECORDING DEVICE|Ultrasound recorders are devices that send high-frequency sound waves in the environment to create images or detect objects and movements within various mediums, such as a mammalian body or other environments. They are popular for wildlife monitoring, biodiversity surveys, habitat assessments and echolocation studies (e.g., bats).||
|protocolName|UNKNOWN|Refers to the fire history of the plot, unknown., Unknown (unable to be determined)., Unknown capture status., Unknown position., Unknown- unable to be determined., Unknown/unable to be determined.||
|protocolName|UNKNOWN TRAP TYPE|Refers to the fire history of the plot, unknown., Unknown (unable to be determined)., Unknown capture status., Unknown position., Unknown, unable to be determined., Unknown/unable to be determined.||
|protocolName|WATER SAMPLE|Water samples are representative samples of a given habitat that serve as a source to study the chemical composition and detect the presence of fauna species (DNA).||
|protocolName|WET PITFALL TRAP|Refers to the fauna observation method, i.e., any observations made from fauna captures using a wet pitfall trap.||
|<a name="samplingEffortUnit-vocabularies"></a>samplingEffortUnit|Hectares|The total area surveyed or sampled, measured in hectares.||
|samplingEffortUnit|Hours|The total time spent actively surveying using the specified protocol, expressed in hours.||
|samplingEffortUnit|Metre Hours|The distance (metres) and time (hours) of specific survey activities such as walking or transect surveys (measure of effort across both space and time).||
|samplingEffortUnit|Metres|A measure of linear distance, to describe the length of transects or areas covered.||
|samplingEffortUnit|Minutes|The total time spent actively surveying using the specified protocol, expressed in minutes.||
|samplingEffortUnit|Person Hours|The cumulative amount of time spent by individuals conducting the survey using the specified protocol. For example, if two people survey for 2 hours each, the total would be 4 person-hours.||
|samplingEffortUnit|Trap Nights|The total number of nights traps are left in the field. One trap night refers to one trap set for one night.||
|samplingEffortUnit|kHz|The frequency of sound is measured in kilohertz, for acoustic monitoring.||
|<a name="targetTaxonomicScope-vocabularies"></a>targetTaxonomicScope|AMPHIBIAN|Refers to the target taxa studied in a fauna survey. Amphibians are vertebrates belonging to the class amphibia such as frogs, toads, newts and salamanders that live in a semi-aquatic environment.||
|targetTaxonomicScope|BIRD|Refers to the target taxa studied in a fauna survey.Warm-blooded vertebrates possessing feather and belonging to the class Aves.||
|targetTaxonomicScope|INVERTEBRATE|Refers to the target taxa studied in a fauna survey.Animals that have no spinal column (e.g., insects, molluscs, spiders).||
|targetTaxonomicScope|MAMMALS|Refers to the target taxa studied in a fauna survey. Warm-blooded vertebrate animals belonging to the class Mammalia, including all that possess hair and suckle their young. Warm-blooded vertebrate animals belonging to the class Mammalia, including all that possess hair and suckle their young.||
|targetTaxonomicScope|NON-VASCULAR PLANT|Refers to the target taxa studied in a fauna survey. Non-vascular plants are plants that do not possess a true vascular tissue (such as xylem-water conducting, phloem-sugar transport). Instead, they may possess simpler tissues that have specialized functions for the internal transport of food and water. They are members of bryophytes for example.||
|targetTaxonomicScope|REPTILE|Refers to the target taxa studied in a fauna survey.Cold-blooded, air-breathing Vertebrates belonging to the class Reptilia, usually covered with external scales or bony plates.||
|targetTaxonomicScope|VASCULAR PLANT|Refers to the target taxa studied in a fauna survey. Vascular plants are plants that possess a true vascular tissue (such as xylem-water conducting, phloem-sugar transport). Examples include some members mosses, such as club moss, horsetails, and pteridophytes such as ferns an fern-allies, gymnosperms (including conifers), and angiosperms (flowering plants).||


### APPENDIX-II: Timestamp
Following date and date-time formats are acceptable within the timestamp:

| TYPE | FORMAT                                                                                                                              |
| --- |-------------------------------------------------------------------------------------------------------------------------------------|
| **xsd:dateTimeStamp with timezone** | yyyy-mm-ddThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00) OR <br/> yyyy-mm-ddThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00) OR <br/>  yyyy-mm-ddThh:mmTZD (eg 1997-07-16T19:20+01:00)|
| **xsd:dateTime** | yyyy-mm-ddThh:mm:ss.s (eg 1997-07-16T19:20:30.45) OR<br/> yyyy-mm-ddThh:mm:ss (eg 1997-07-16T19:20:30) OR<br/> yyyy-mm-ddThh:mm (eg 1997-07-16T19:20) |
| **xsd:Date** | dd/mm/yyyy OR<br/> d/m/yyyy OR<br/> yyyy-mm-dd OR<br/> yyyy-m-d |
| **xsd:gYearMonth** | mm/yyyy OR<br/> m/yyyy OR<br/> yyyy-mm |
| **xsd:gYear** | yyyy |

Where:<br/>
&emsp; `yyyy`: four-digit year <br/>
&emsp; `mm`: two-digit month (01=January, etc.) <br/>
&emsp; `dd`: two-digit day of month (01 through 31) <br/>
&emsp; `hh`: two digits of hour (00 through 23) (am/pm NOT allowed) <br/>
&emsp; `mm`: two digits of minute (00 through 59) <br/>
&emsp; `ss`: two digits of second (00 through 59) <br/>
&emsp; `s`: one or more digits representing a decimal fraction of a second
&emsp; `TZD`: time zone designator (Z or +hh:mm or -hh:mm)


### APPENDIX-III: UTF-8
UTF-8 encoding is considered a best practice for handling character encoding, especially in
the context of web development, data exchange, and modern software systems. UTF-8
(Unicode Transformation Format, 8-bit) is a variable-width character encoding capable of
encoding all possible characters (code points) in Unicode.<br/>
Here are some reasons why UTF-8 is recommended:

- **Universal Character Support:** UTF-8 can represent almost all characters from all writing 
  systems in use today. This includes characters from various languages, mathematical symbols, 
  and other special characters.
- **Backward Compatibility:** UTF-8 is backward compatible with ASCII (American
  Standard Code for Information Interchange). The first 128 characters in UTF-8 are
  identical to ASCII, making it easy to work with systems that use ASCII.
- **Efficiency:** UTF-8 is space-efficient for Latin-script characters (common in English
  and many other languages). It uses one byte for ASCII characters and up to four
  bytes for other characters. This variable-length encoding minimises storage and
  bandwidth requirements.
- **Web Standards:** UTF-8 is the dominant character encoding for web content. It is
  widely supported by browsers, servers, and web-related technologies.
- **Globalisation:** As software applications become more globalised, supporting a wide
  range of languages and scripts becomes crucial. UTF-8 is well-suited for
  internationalisation and multilingual support.
- **Compatibility with Modern Systems:** UTF-8 is the default encoding for many
  programming languages, databases, and operating systems. Choosing UTF-8 helps
  ensure compatibility across different platforms and technologies.

When working with text data, UTF-8 encoding is recommended to avoid issues related to character
representation and ensure that a diverse set of characters and languages is supported.

For assistance, please contact: <bdr-support@dcceew.gov.au>

