"""
Curated disease information database.

For every PlantVillage class we provide:
  - cause: the pathogen or condition
  - symptoms: visual cues to confirm the diagnosis
  - treatment: an actionable, non-prescriptive recommendation

Sources: extension.umn.edu, apsnet.org, PlantVillage encyclopedia,
Cornell CALS plant pathology fact sheets. Treatment advice is general;
farmers should consult a local agronomist for chemical products
approved in their region.
"""

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "cause": "Fungus Venturia inaequalis; overwinters in fallen leaves.",
        "symptoms": "Olive-green to brown velvety spots on leaves and fruit; deformed fruit.",
        "treatment": "Rake and destroy fallen leaves; apply captan or myclobutanil in spring; plant resistant cultivars (e.g. Liberty, Enterprise).",
    },
    "Apple___Black_rot": {
        "cause": "Fungus Botryosphaeria obtusa.",
        "symptoms": "Circular purple leaf spots; 'frogeye' pattern; rotting fruit with concentric rings.",
        "treatment": "Prune out dead wood and cankers; remove mummified fruit; apply captan or thiophanate-methyl at petal fall.",
    },
    "Apple___Cedar_apple_rust": {
        "cause": "Fungus Gymnosporangium juniperi-virginianae; alternates between apple and juniper hosts.",
        "symptoms": "Bright orange-yellow spots on upper leaf surface; tube-like structures on underside.",
        "treatment": "Remove nearby junipers (0.5–1 mile) if practical; apply myclobutanil at pink bud stage; use resistant varieties.",
    },
    "Apple___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Uniform green colour, no lesions or spots.",
        "treatment": "Continue routine care: balanced NPK fertilization, adequate water, annual pruning.",
    },
    "Blueberry___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Healthy foliage, no discoloration.",
        "treatment": "Maintain acidic soil (pH 4.5–5.5); mulch with pine bark; drip irrigate.",
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "cause": "Fungus Podosphaera clandestina.",
        "symptoms": "White powdery patches on new leaves and shoots; leaves curl and become distorted.",
        "treatment": "Prune for airflow; apply sulfur or potassium bicarbonate at first sign; avoid excess nitrogen.",
    },
    "Cherry_(including_sour)___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Glossy dark-green leaves, no spots.",
        "treatment": "Prune in late winter for airflow; monitor for pests weekly.",
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "cause": "Fungus Cercospora zeae-maydis.",
        "symptoms": "Rectangular grey-tan lesions bounded by leaf veins.",
        "treatment": "Rotate crops (2-year break from corn); till residue; use resistant hybrids; apply strobilurin fungicide at VT stage if severe.",
    },
    "Corn_(maize)___Common_rust_": {
        "cause": "Fungus Puccinia sorghi.",
        "symptoms": "Small cinnamon-brown pustules on both leaf surfaces.",
        "treatment": "Plant resistant hybrids; foliar fungicide (azoxystrobin) only if infection appears before tasseling.",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "cause": "Fungus Exserohilum turcicum.",
        "symptoms": "Long cigar-shaped grey-green lesions on lower leaves that turn tan.",
        "treatment": "Plant resistant hybrids; rotate crops; till residue; apply fungicide (propiconazole) at first symptom if season is wet.",
    },
    "Corn_(maize)___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Uniform green leaves, no lesions.",
        "treatment": "Standard agronomy: side-dress nitrogen at V6, scout weekly for pests.",
    },
    "Grape___Black_rot": {
        "cause": "Fungus Guignardia bidwellii.",
        "symptoms": "Tan circular leaf spots with dark border; berries turn hard, black, shriveled.",
        "treatment": "Remove mummified berries and infected canes; apply mancozeb or myclobutanil from bud break through veraison.",
    },
    "Grape___Esca_(Black_Measles)": {
        "cause": "Complex of wood-inhabiting fungi (Phaeomoniella, Phaeoacremonium).",
        "symptoms": "Interveinal 'tiger-stripe' leaf pattern; dark spots on berries; vine dieback.",
        "treatment": "No cure. Remove severely affected vines; protect pruning wounds with sealant; avoid pruning in wet weather.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "cause": "Fungus Pseudocercospora vitis.",
        "symptoms": "Irregular reddish-brown leaf spots; premature defoliation.",
        "treatment": "Improve canopy airflow via leaf pulling; apply copper-based fungicide; remove fallen leaves after harvest.",
    },
    "Grape___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Bright green leaves, no lesions.",
        "treatment": "Maintain trellis training and canopy management; scout for powdery mildew weekly.",
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "cause": "Bacterium Candidatus Liberibacter asiaticus; vectored by Asian citrus psyllid.",
        "symptoms": "Blotchy mottled leaves; lopsided bitter green fruit; twig dieback.",
        "treatment": "No cure. Remove infected trees to prevent spread; control psyllid vector with imidacloprid; plant certified disease-free stock.",
    },
    "Peach___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas arboricola pv. pruni.",
        "symptoms": "Small angular purple leaf spots that fall out ('shot-hole'); pitted fruit.",
        "treatment": "Plant resistant varieties (Contender, Redhaven); apply copper spray during dormancy; avoid overhead irrigation.",
    },
    "Peach___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Vibrant green leaves, no spots.",
        "treatment": "Annual dormant oil spray; thin fruit for size and airflow.",
    },
    "Pepper,_bell___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas campestris pv. vesicatoria.",
        "symptoms": "Small water-soaked leaf spots turning brown with yellow halo; raised scabs on fruit.",
        "treatment": "Use certified disease-free seed; rotate 2–3 years; apply copper + mancozeb tank mix; avoid working plants when wet.",
    },
    "Pepper,_bell___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Healthy dark-green leaves.",
        "treatment": "Stake plants; mulch to prevent soil splash; consistent watering to prevent blossom-end rot.",
    },
    "Potato___Early_blight": {
        "cause": "Fungus Alternaria solani.",
        "symptoms": "Concentric brown 'bulls-eye' rings on lower leaves; leaves yellow and drop.",
        "treatment": "Rotate crops (3 years); avoid overhead irrigation; apply chlorothalonil or azoxystrobin at first sign.",
    },
    "Potato___Late_blight": {
        "cause": "Oomycete Phytophthora infestans (the Irish famine pathogen).",
        "symptoms": "Large dark water-soaked lesions with white sporulation on leaf undersides; rapid plant collapse.",
        "treatment": "Destroy infected plants immediately; apply chlorothalonil or metalaxyl preventatively; plant certified seed; avoid overhead water.",
    },
    "Potato___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Uniform green foliage.",
        "treatment": "Hill soil around stems; maintain consistent moisture; scout for Colorado potato beetle.",
    },
    "Raspberry___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Healthy green canes and leaves.",
        "treatment": "Prune out floricanes after fruiting; maintain trellis; mulch with straw.",
    },
    "Soybean___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Uniform green trifoliate leaves.",
        "treatment": "Inoculate seed with Bradyrhizobium; scout for aphids and rust.",
    },
    "Squash___Powdery_mildew": {
        "cause": "Fungi Podosphaera xanthii and Erysiphe cichoracearum.",
        "symptoms": "White powdery patches on leaves and stems; leaves eventually turn yellow and die.",
        "treatment": "Spray potassium bicarbonate or milk-water (1:9) weekly; plant resistant varieties; improve airflow with wider spacing.",
    },
    "Strawberry___Leaf_scorch": {
        "cause": "Fungus Diplocarpon earlianum.",
        "symptoms": "Small dark purple leaf spots that coalesce; leaves appear 'scorched'.",
        "treatment": "Remove old leaves after harvest; renovate matted rows; apply captan or myclobutanil in early spring.",
    },
    "Strawberry___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Bright trifoliate green leaves.",
        "treatment": "Mulch with straw to keep berries clean; renew planting every 3 years.",
    },
    "Tomato___Bacterial_spot": {
        "cause": "Bacterium Xanthomonas spp.",
        "symptoms": "Small dark water-soaked leaf spots; scabby fruit lesions.",
        "treatment": "Use certified seed; rotate 2 years; copper + mancozeb spray; remove infected plants at end of season.",
    },
    "Tomato___Early_blight": {
        "cause": "Fungus Alternaria solani.",
        "symptoms": "'Bulls-eye' concentric rings on older leaves; yellowing and defoliation from bottom up.",
        "treatment": "Mulch to prevent soil splash; stake plants; apply chlorothalonil every 7–10 days in wet weather.",
    },
    "Tomato___Late_blight": {
        "cause": "Oomycete Phytophthora infestans.",
        "symptoms": "Large water-soaked lesions turning brown; white fuzzy growth on undersides in humid conditions; fruit rot.",
        "treatment": "Remove infected leaves immediately; apply copper or chlorothalonil preventatively; ensure airflow; avoid overhead irrigation.",
    },
    "Tomato___Leaf_Mold": {
        "cause": "Fungus Passalora fulva (Cladosporium fulvum).",
        "symptoms": "Pale green-yellow spots on upper leaf surface; olive-grey velvety mold on underside.",
        "treatment": "Improve greenhouse ventilation; keep humidity below 85%; apply chlorothalonil or copper; use resistant varieties.",
    },
    "Tomato___Septoria_leaf_spot": {
        "cause": "Fungus Septoria lycopersici.",
        "symptoms": "Small circular spots with dark border and grey center; starts on lower leaves.",
        "treatment": "Remove and destroy infected leaves; mulch; apply chlorothalonil or copper weekly during wet weather.",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "cause": "Arachnid Tetranychus urticae (not a disease — a pest).",
        "symptoms": "Fine stippling on leaves; webbing on undersides; leaves bronze and drop.",
        "treatment": "Blast with water to dislodge; release predatory mites (Phytoseiulus); insecticidal soap or neem oil; avoid pyrethroids (they kill predators).",
    },
    "Tomato___Target_Spot": {
        "cause": "Fungus Corynespora cassiicola.",
        "symptoms": "Small brown spots that enlarge into concentric rings with a light center.",
        "treatment": "Rotate crops; remove crop debris; apply azoxystrobin or chlorothalonil at first sign.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "cause": "Begomovirus vectored by whitefly (Bemisia tabaci).",
        "symptoms": "Upward leaf curling, yellow leaf margins, stunted growth, flower drop.",
        "treatment": "No cure. Control whitefly with imidacloprid or yellow sticky traps; use reflective mulch; plant resistant varieties (TY-labeled cultivars); remove infected plants.",
    },
    "Tomato___Tomato_mosaic_virus": {
        "cause": "Tomato mosaic virus (ToMV); spread mechanically (hands, tools).",
        "symptoms": "Mottled light-and-dark green leaf pattern; leaf distortion; stunted growth.",
        "treatment": "No cure. Remove and destroy infected plants; wash hands and tools with milk or 10% bleach; do not use tobacco near plants; use resistant varieties.",
    },
    "Tomato___healthy": {
        "cause": "No disease detected.",
        "symptoms": "Healthy dark-green foliage.",
        "treatment": "Stake and prune suckers; consistent watering to prevent blossom-end rot; side-dress with calcium.",
    },
}


def get_info(class_name: str) -> dict:
    """Return the info dict for a class name, or a safe fallback."""
    return DISEASE_INFO.get(
        class_name,
        {
            "cause": "Information not available for this class.",
            "symptoms": "—",
            "treatment": "Consult a local agronomist or plant pathologist.",
        },
    )
