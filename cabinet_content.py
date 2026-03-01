"""
🧪 The Fitzroy Cabinet — Content Data
All bottles, instruments, specimens, personal items, mixing recipes, and lore.
"""

# =============================================================================
# BOTTLES / TINCTURES
# =============================================================================

BOTTLES = [
    {
        "id": "laudanum",
        "name": "Laudanum",
        "subtitle": "Tinctura Opii",
        "shelf": 0,
        "category": "tincture",
        "color": "#b8860b",
        "liquid_color": "#8b4513",
        "shape": "tall_apothecary",
        "description": "An alcoholic solution of opium. The most prescribed medicine of the age.",
        "medical": "10% opium by weight dissolved in alcohol. Dosage: 25 drops for pain, 40 for sleep. "
                   "Prescribed for everything from toothache to tuberculosis.",
        "secret": "The bottle bears Fitzroy's handwriting: 'Batch 7 — modified concentration for Subject C.' "
                  "Subject C is Sebastian Carlisle.",
        "lore": "This is the chain that held Sebastian. Not iron — amber liquid and dependency. "
                "Fitzroy maintained precise logs of every dose.",
        "uv_text": "CARLISLE PROTOCOL — 3x STANDARD",
        "mixing_tags": ["opiate", "sedative", "addictive"],
        "intensity_min": 1,
    },
    {
        "id": "chloroform",
        "name": "Chloroform",
        "subtitle": "Chloroformum",
        "shelf": 0,
        "category": "tincture",
        "color": "#2d5a27",
        "liquid_color": "#1a3a15",
        "shape": "wide_round",
        "description": "A volatile anaesthetic. Sweet-smelling and treacherous.",
        "medical": "Inhaled via soaked cloth for surgical anaesthesia. Discovered 1831. "
                   "Dosage must be precisely controlled — the margin between unconsciousness and death is razor-thin.",
        "secret": "A cloth folded beside the bottle smells faintly sweet. Someone used this recently.",
        "lore": "Queen Victoria herself took chloroform during childbirth. "
                "In less noble hands, it serves darker purposes.",
        "uv_text": "SEE INCIDENT LOG — NOV 12",
        "mixing_tags": ["anaesthetic", "volatile", "dangerous"],
        "intensity_min": 1,
    },
    {
        "id": "mercury",
        "name": "Mercuric Chloride",
        "subtitle": "Hydrargyri Chloridum",
        "shelf": 0,
        "category": "tincture",
        "color": "#1a3a6a",
        "liquid_color": "#c0c0c0",
        "shape": "cobalt_round",
        "description": "A heavy blue bottle sealed with black wax. For the treatment of syphilis.",
        "medical": "Applied topically or ingested in small doses. Side effects include tooth loss, "
                   "neurological damage, kidney failure, and madness. The cure rivals the disease.",
        "secret": "The wax seal has been broken and resealed multiple times. "
                  "Fingerprints in the wax don't match Fitzroy's.",
        "lore": "They called it 'a night with Venus, a lifetime with Mercury.' "
                "Fitzroy kept meticulous records of which patients survived treatment.",
        "uv_text": "BLACKWOOD — PERSONAL USE",
        "mixing_tags": ["heavy_metal", "toxic", "antiseptic"],
        "intensity_min": 1,
    },
    {
        "id": "ether",
        "name": "Diethyl Ether",
        "subtitle": "Aether Sulfuricus",
        "shelf": 0,
        "category": "tincture",
        "color": "#d4d4c8",
        "liquid_color": "#eeeedd",
        "shape": "wide_jar",
        "description": "A wide-mouth jar with a cloth draped over it. The air shimmers above.",
        "medical": "Inhaled anaesthetic predating chloroform. Highly flammable. "
                   "The fumes linger in operating theatres for hours.",
        "secret": "The cloth is stained with something other than ether. Blood, perhaps.",
        "lore": "Ether frolics — parties where young men inhaled the vapour for euphoria — "
                "were common before its medical applications were discovered.",
        "uv_text": "FLAMMABLE — STORE AWAY FROM GAS",
        "mixing_tags": ["anaesthetic", "volatile", "flammable"],
        "intensity_min": 1,
    },
    {
        "id": "strychnine",
        "name": "Strychnine",
        "subtitle": "Nux Vomica",
        "shelf": 1,
        "category": "tincture",
        "color": "#8b0000",
        "liquid_color": "#4a0000",
        "shape": "tiny_vial",
        "description": "A tiny red bottle with a locked cap. Deceptively small.",
        "medical": "Derived from the Strychnos nux-vomica tree. In minute doses, prescribed as a stimulant "
                   "and appetite enhancer. In larger doses: violent convulsions, arched spine, asphyxiation.",
        "secret": "The lock has scratch marks. Someone tried to open it without the key.",
        "lore": "Fitzroy once demonstrated strychnine poisoning on a laboratory dog during a lecture. "
                "Three students fainted. Sebastian walked out.",
        "uv_text": "SCHEDULE I — LOCKED ACCESS ONLY",
        "mixing_tags": ["poison", "stimulant", "convulsant"],
        "intensity_min": 2,
    },
    {
        "id": "arsenic_wafers",
        "name": "Arsenic Complexion Wafers",
        "subtitle": "Dr. Mackenzie's Tablets",
        "shelf": 1,
        "category": "tincture",
        "color": "#f5f0e0",
        "liquid_color": None,
        "shape": "decorative_tin",
        "description": "A small ornate tin. 'For a Pale and Luminous Complexion.' Women ate these willingly.",
        "medical": "Arsenic trioxide in small doses. Sold commercially as beauty products. "
                   "Chronic ingestion causes peripheral neuropathy, organ failure, and slow death.",
        "secret": "The tin was found in Beatrice Whitmore's effects after her death.",
        "lore": "The cruelest irony: women poisoned themselves to meet beauty standards "
                "set by the same men who studied their corpses.",
        "uv_text": "EVIDENCE — PWS CASE FILE #7",
        "mixing_tags": ["poison", "cosmetic", "arsenic"],
        "intensity_min": 2,
    },
    {
        "id": "dovers_powder",
        "name": "Dover's Powder",
        "subtitle": "Pulvis Ipecacuanhae Compositus",
        "shelf": 1,
        "category": "tincture",
        "color": "#654321",
        "liquid_color": "#8b7355",
        "shape": "brown_medicine",
        "description": "A brown bottle with a cork stopper. Standard Victorian pharmacy.",
        "medical": "Opium combined with ipecac. Induces sweating while managing pain. "
                   "Standard prescription for fevers, colds, and rheumatism.",
        "secret": "The label has been altered. The original dosage has been crossed out "
                  "and replaced with a higher number in different handwriting.",
        "lore": "Named after Thomas Dover, a pirate-turned-physician. "
                "Even medicine has its buccaneers.",
        "uv_text": "DOSAGE MODIFIED — WHO?",
        "mixing_tags": ["opiate", "emetic", "febrifuge"],
        "intensity_min": 1,
    },
    {
        "id": "paregoric",
        "name": "Paregoric",
        "subtitle": "Camphorated Tincture of Opium",
        "shelf": 1,
        "category": "tincture",
        "color": "#c49a6c",
        "liquid_color": "#a0724a",
        "shape": "small_amber",
        "description": "A small amber bottle. 'For the quieting of infants.' The label shows a sleeping child.",
        "medical": "Diluted opium with camphor, anise, and benzoic acid. Given to teething babies, "
                   "colicky infants, and restless children. Dosage: 5-10 drops.",
        "secret": "This is one of the tainted bottles from the Red Rose front charity. "
                  "The laudanum concentration is three times the labeled amount.",
        "lore": "How many mothers trusted this bottle? How many infants never woke? "
                "The moral panic blamed Romani wet nurses. The truth was in the chemistry.",
        "uv_text": "RED ROSE SUPPLY CHAIN — LOT 34B",
        "mixing_tags": ["opiate", "pediatric", "tainted"],
        "intensity_min": 2,
    },
    {
        "id": "fitzroy_tonic",
        "name": "Fitzroy's Infant Tonic",
        "subtitle": "Patent Pediatric Formula",
        "shelf": 1,
        "category": "tincture",
        "color": "#2a4a2a",
        "liquid_color": "#3a6a3a",
        "shape": "professional",
        "description": "A professionally labeled bottle. 'Fitzroy Pediatric Compound — Safe for All Ages.'",
        "medical": "The dual-nature Protocol in a bottle. Early pharmacovigilance work designed to trace "
                   "laudanum in contaminated tonics and replace it with safer compounds.",
        "secret": "Two versions exist. One saves lives. The other, distributed through Red Rose fronts, "
                  "contains sterilizing agents. This bottle's batch number determines which.",
        "lore": "Fitzroy's masterwork and his greatest sin share a label. "
                "The line between healer and destroyer was never thinner.",
        "uv_text": "BATCH 12-A — VERIFY DISTRIBUTION",
        "mixing_tags": ["pediatric", "antibiotic", "dual_nature"],
        "intensity_min": 3,
    },
    {
        "id": "distilled_blood",
        "name": "Distilled Blood Serum",
        "subtitle": "Experimental — Restricted",
        "shelf": 3,
        "category": "tincture",
        "color": "#4a0000",
        "liquid_color": "#8b0000",
        "shape": "laboratory",
        "description": "A dark vial in a leather case. The liquid inside is unmistakable.",
        "medical": "An experimental serum developed during unethical experiments at Edinburgh. "
                   "Composition unknown — possibly blood-derived proteins with opiate stabilizers.",
        "secret": "Sebastian's addiction. His chain. The thing that keeps him alive "
                  "and the thing that is killing him.",
        "lore": "Dr. Lucien Warren created this at Edinburgh. Fitzroy perfected it. "
                "Sebastian needs it to survive his blood disorder. They all know this.",
        "uv_text": "WARREN PROTOCOL — EYES ONLY",
        "mixing_tags": ["experimental", "blood", "addictive"],
        "intensity_min": 4,
    },
    {
        "id": "smelling_salts",
        "name": "Smelling Salts",
        "subtitle": "Ammonium Carbonate",
        "shelf": 0,
        "category": "tincture",
        "color": "#e8e4dc",
        "liquid_color": None,
        "shape": "crystal_bottle",
        "description": "A cut-glass bottle with a silver cap. For reviving the faint.",
        "medical": "Ammonium carbonate crystals that release ammonia gas when held under the nose. "
                   "Triggers inhalation reflex and consciousness in the fainted.",
        "secret": "Standard medical supply. But in the anatomy theatre, the question is: "
                  "who needed reviving, and from what?",
        "lore": "Every anatomist kept these close. Not for themselves — "
                "for the students who weren't yet accustomed to the smell.",
        "uv_text": None,
        "mixing_tags": ["stimulant", "ammonia", "revival"],
        "intensity_min": 1,
    },
    {
        "id": "belladonna",
        "name": "Belladonna Extract",
        "subtitle": "Atropa Belladonna",
        "shelf": 0,
        "category": "tincture",
        "color": "#3d1f5a",
        "liquid_color": "#2a0a3a",
        "shape": "elegant_purple",
        "description": "An elegant purple bottle. 'Beautiful Lady' — named for its cosmetic use dilating pupils.",
        "medical": "Contains atropine. Used to dilate pupils for eye examinations, treat asthma, "
                   "and as an antispasmodic. Overdose causes hallucinations, seizures, death.",
        "secret": "Isabella used belladonna drops in her eyes before every ritual. "
                  "The cult believed dilated pupils opened the 'inner sight.'",
        "lore": "Renaissance women dropped it in their eyes for beauty. "
                "Victorian doctors used it for science. Isabella used it for both.",
        "uv_text": "ORDER OF THE CRIMSON VEIL",
        "mixing_tags": ["poison", "cosmetic", "hallucinogen"],
        "intensity_min": 2,
    },
]


# =============================================================================
# INSTRUMENTS
# =============================================================================

INSTRUMENTS = [
    {
        "id": "scarificator",
        "name": "Scarificator",
        "shelf": 2,
        "description": "A spring-loaded brass device with twelve concealed blades. Wind the mechanism, "
                       "press to skin, and the blades release simultaneously.",
        "medical": "Used for bloodletting — creates shallow parallel cuts to 'release bad humours.' "
                   "Spring mechanism made the procedure faster and theoretically more humane.",
        "secret": "This model is engraved with the initials 'E.F.' — Edmund Fitzroy. "
                  "Passed from father to son. A legacy of blood.",
        "lore": "Alistair keeps his father's instruments maintained but never uses them. "
                "He believes in chemical precision, not mechanical brutality.",
        "uv_text": "PROPERTY OF DR. EDMUND FITZROY",
    },
    {
        "id": "leech_jar",
        "name": "Leech Jar",
        "shelf": 2,
        "description": "A tall glass vessel with a perforated ceramic lid. The water inside is murky. "
                       "Something moves.",
        "medical": "Hirudo medicinalis — the medicinal leech. Applied to reduce inflammation, "
                   "treat black eyes, and manage congestion. Still used in microsurgery today.",
        "secret": "The leeches are alive. Someone has been feeding them recently. "
                  "Fresh blood in the water.",
        "lore": "Lizzy Reed knows leech therapy better than any hospital physician. "
                "The Romani tradition predates English medicine by centuries.",
        "uv_text": "ACTIVE — MAINTAIN WEEKLY",
    },
    {
        "id": "trephine",
        "name": "Trephination Drill",
        "shelf": 2,
        "description": "A hand-cranked brass drill with a circular blade. For cutting through skull bone.",
        "medical": "Creates a burr hole in the cranium to relieve intracranial pressure. "
                   "One of the oldest surgical procedures in human history — Stone Age skulls show evidence.",
        "secret": "The blade is sharper than standard. Someone has been maintaining this "
                  "with an unusual level of care.",
        "lore": "Fitzroy demonstrated trephination to prove a point about consciousness. "
                "'Where does the soul reside?' he asked, drilling into a cadaver's skull. "
                "'Not here.'",
        "uv_text": None,
    },
    {
        "id": "amputation_saw",
        "name": "Capital Amputation Saw",
        "subtitle": "By Weiss & Son, London",
        "shelf": 2,
        "description": "A compact bone saw with an ivory handle. The blade has a distinctive curve. "
                       "The handle is stained dark — ivory absorbs what it touches.",
        "medical": "For mid-shaft amputations of long bones. A skilled surgeon could remove a leg "
                   "in under 90 seconds. Speed was mercy before anaesthesia.",
        "secret": "The ivory handle bears teeth marks. Someone gripped this in agony.",
        "lore": "Robert Liston, the fastest surgeon in London, once amputated a leg so quickly "
                "he accidentally cut his assistant's fingers off. Both patients died of infection.",
        "uv_text": "3 OPERATIONS — DATES RECORDED",
    },
    {
        "id": "cupping_set",
        "name": "Cupping Set",
        "shelf": 2,
        "description": "Six brass cups of graduated sizes in a velvet-lined leather case, "
                       "with a spirit lamp and scarification blade.",
        "medical": "Heated cups create suction on the skin, drawing blood to the surface. "
                   "'Wet cupping' involves cutting the skin first. Used for pain, congestion, and fever.",
        "secret": "The velvet lining has a false bottom. Beneath it: a folded letter "
                  "and a wax-sealed envelope.",
        "lore": "The Underground Network of Healers still practices cupping. "
                "When Fitzroy learned this, he called it 'peasant medicine.' "
                "When it worked, he called it 'empirical observation.'",
        "uv_text": "CHECK FALSE BOTTOM",
    },
    {
        "id": "syringe",
        "name": "Hypodermic Syringe",
        "subtitle": "Pravaz Model, c.1853",
        "shelf": 2,
        "description": "An early hypodermic syringe. Glass barrel, silver fittings, "
                       "a needle fine enough to pierce skin without a blade.",
        "medical": "Invented by Alexander Wood and Charles Pravaz in 1853. "
                   "Revolutionized drug delivery — morphine could now be injected directly.",
        "secret": "The barrel has residue. Chemical analysis would reveal "
                  "a compound not found in any pharmacopoeia.",
        "lore": "This is how Fitzroy administered the modified laudanum to Sebastian. "
                "Not by mouth — by vein. Faster. More precise. More control.",
        "uv_text": "CARLISLE DOSING SCHEDULE",
    },
    {
        "id": "scalpel_set",
        "name": "Scalpel Set",
        "subtitle": "Complete Dissection Kit",
        "shelf": 2,
        "description": "Seven scalpels of graduated sizes arranged on a leather roll. "
                       "One slot is empty.",
        "medical": "Standard anatomy demonstrator's kit. Each blade serves a specific purpose — "
                   "skin incision, fascia dissection, nerve isolation, vessel ligation.",
        "secret": "The third scalpel is missing. It has been missing for six weeks. "
                  "No one has reported it.",
        "lore": "Sebastian could identify each blade by touch alone. "
                "'An artist knows his brushes,' he told Evelyn. 'A surgeon knows his steel.'",
        "uv_text": "BLADE #3 — MISSING SINCE OCT 4",
    },
    {
        "id": "obstetric_forceps",
        "name": "Obstetric Forceps",
        "subtitle": "Simpson Pattern",
        "shelf": 2,
        "description": "Curved steel forceps designed to cradle an infant's head during difficult births.",
        "medical": "Used when labour stalls and the infant is in distress. "
                   "Requires immense skill — too much pressure crushes the skull, too little fails to deliver.",
        "secret": "These forceps have never been used. Still wrapped in the original oilcloth. "
                  "Fitzroy doesn't deliver babies. So why does he have them?",
        "lore": "Lizzy Reed refuses to use forceps. 'Hands were here first,' she says. "
                "'And hands know gentleness.'",
        "uv_text": "INFANT PROTOCOL — REFERENCE TOOL",
    },
]


# =============================================================================
# SPECIMENS
# =============================================================================

SPECIMENS = [
    {
        "id": "heart_jar",
        "name": "Heart in Formaldehyde",
        "subtitle": "Subject 23",
        "shelf": 3,
        "jar_color": "#aaddaa",
        "liquid_color": "#88bb8844",
        "description": "A human heart suspended in pale green fluid. The label reads 'Subject 23.' "
                       "It rotates slowly in the current.",
        "medical": "Adult male heart, approximately 310 grams. Left ventricle shows mild hypertrophy "
                   "consistent with chronic physical labour. Coronary arteries intact.",
        "secret": "Subject 23 was never a donated cadaver. The Anatomy Club's procurement records "
                  "show payment to grave robbers for this specimen.",
        "lore": "Thomas Blackwood personally oversaw the acquisition. "
                "The Black Book records the cost: twelve shillings and a bottle of gin.",
        "uv_text": "PROCUREMENT: IRREGULAR",
    },
    {
        "id": "brain_section",
        "name": "Brain Cross-Section",
        "subtitle": "Horizontal Plane",
        "shelf": 3,
        "jar_color": "#ccbbaa",
        "liquid_color": "#aa998866",
        "description": "A horizontal slice of brain tissue pressed between glass plates. "
                       "The grey and white matter are clearly distinguishable.",
        "medical": "Horizontal section at the level of the basal ganglia. "
                   "Caudate nucleus, putamen, and internal capsule visible. Teaching specimen.",
        "secret": "A small adhesion near the temporal lobe suggests this individual "
                  "suffered from epilepsy. Fitzroy's notes call it 'the seat of vision.'",
        "lore": "Fitzroy's research into consciousness led him here. "
                "'If I could map every fold,' he wrote, 'I could map the soul itself.'",
        "uv_text": "DEMENTIA STUDY — SEE NOTES",
    },
    {
        "id": "eye_collection",
        "name": "Eyeball Collection",
        "subtitle": "Three Specimens — Progressive Dissection",
        "shelf": 3,
        "jar_color": "#eeeedd",
        "liquid_color": "#ddddcc44",
        "description": "Three glass jars containing human eyeballs in various stages of dissection. "
                       "The first intact, the second halved, the third reduced to lens and retina.",
        "medical": "Demonstrates the layered structure of the eye: sclera, choroid, retina. "
                   "The vitreous humour has been drained from specimens 2 and 3.",
        "secret": "The iris colours don't match. These eyes came from different people. "
                  "Different ages. Different deaths.",
        "lore": "Sebastian sketched these for his anatomy lectures. "
                "His drawings are pinned to the wall beside the cabinet.",
        "uv_text": "THREE DONORS — UNRELATED",
    },
    {
        "id": "hand_bones",
        "name": "Articulated Hand",
        "subtitle": "Right Hand — Female",
        "shelf": 3,
        "jar_color": None,
        "liquid_color": None,
        "description": "A complete hand skeleton, wired together at the joints. "
                       "Positioned as if reaching for something. Or someone.",
        "medical": "27 bones: 8 carpals, 5 metacarpals, 14 phalanges. "
                   "The wiring technique suggests a skilled anatomist's work. "
                   "Bone density indicates a young adult female.",
        "secret": "A ring mark is visible on the fourth metacarpal — "
                  "the bone has a slight groove where a ring sat for years.",
        "lore": "Whose hand was this? The PWS would want to know. "
                "Every bone in this cabinet was once a person.",
        "uv_text": "FEMALE — AGE 20-25 — SOURCE?",
    },
    {
        "id": "blood_rack",
        "name": "Blood Sample Rack",
        "subtitle": "12 Specimens — Various Dates",
        "shelf": 3,
        "jar_color": "#aa0000",
        "liquid_color": "#8b000088",
        "description": "A wooden rack holding twelve small glass vials. The blood inside ranges "
                       "from bright crimson to near-black. Labels show dates spanning two years.",
        "medical": "Serial blood samples showing degradation over time. "
                   "Some have separated into serum and cellular components. "
                   "Three vials show unusual coagulation patterns.",
        "secret": "Seven of these vials are labeled 'S.C.' — Sebastian Carlisle. "
                  "They document his condition over the course of his captivity.",
        "lore": "Fitzroy tracked Sebastian's blood like a sommelier tracks vintages. "
                "'The disease tells a story,' he wrote. 'I am learning to read it.'",
        "uv_text": "S.C. LONGITUDINAL STUDY",
    },
    {
        "id": "wax_moulage",
        "name": "Wax Moulage",
        "subtitle": "Diseased Liver — Teaching Model",
        "shelf": 3,
        "jar_color": None,
        "liquid_color": None,
        "description": "A painted wax model of a cirrhotic liver on a wooden base. "
                       "The detail is disturbingly realistic.",
        "medical": "Demonstrates end-stage alcoholic cirrhosis: nodular surface, "
                   "shrunken right lobe, enlarged left lobe. Jaundiced coloring.",
        "secret": "On the underside of the base, scratched in pencil: "
                  "'Father. 1871.'",
        "lore": "Dr. Edmund Fitzroy died of liver failure. Alistair commissioned this model "
                "and keeps it as a reminder. Of what, exactly, only he knows.",
        "uv_text": "EDMUND FITZROY — d. 1871",
    },
]


# =============================================================================
# PERSONAL / SECRET ITEMS (Bottom shelf / Hidden drawer)
# =============================================================================

PERSONAL_ITEMS = [
    {
        "id": "notebook",
        "name": "Fitzroy's Notebook",
        "description": "A leather-bound notebook monogrammed 'A.F.' in gold. "
                       "The pages are dense with formulae and observations.",
        "secret": "Page 47 contains a formula for a compound that doesn't appear "
                  "in any published pharmacopoeia. The margin note reads: 'It works.'",
        "lore": "This is the Rosetta Stone of Fitzroy's research. "
                "Every experiment, every dosage, every subject — all recorded here.",
        "uv_text": "ENCODED PAGES — USE CIPHER KEY",
    },
    {
        "id": "locket",
        "name": "A Woman's Locket",
        "description": "A small gold locket on a broken chain. The clasp is bent "
                       "as though it was torn from someone's neck.",
        "secret": "Inside: a miniature portrait of a woman in her 40s. "
                  "She resembles Alistair around the eyes. His mother.",
        "lore": "Alistair funds an orphanage in her memory. "
                "The locket was hers. How it ended up in the cabinet "
                "rather than around his neck says everything.",
        "uv_text": "ELEANOR FITZROY — 1829-1869",
    },
    {
        "id": "choir_sheets",
        "name": "Choir Sheet Music",
        "description": "Yellowed pages of hymn music. Two sets of handwritten annotations — "
                       "one neat, one wild. Boys' handwriting.",
        "secret": "Alistair and Elijah's childhood. Before medicine, before divinity, "
                  "before everything broke between them. They sang together.",
        "lore": "Elijah still sings these hymns at his Quaker meetings. "
                "Alistair hasn't sung since their mother died.",
        "uv_text": None,
    },
    {
        "id": "red_rose_seal",
        "name": "Red Rose Wax Seal",
        "description": "A heavy brass stamp depicting a crimson rose. "
                       "The handle is worn smooth from use.",
        "secret": "This is how the Society marks its documents. "
                  "The seal pattern contains a hidden cipher — "
                  "each petal encodes a membership tier.",
        "lore": "Whoever holds the seal speaks for the Society. "
                "Fitzroy keeps it in his private cabinet. Not the Society's vault. "
                "That tells you who is really in charge.",
        "uv_text": "TIER III — COUNCIL ACCESS",
    },
    {
        "id": "romani_amulet",
        "name": "A Romani Amulet",
        "description": "A small protective charm on a leather cord. Carved bone and red thread. "
                       "It does not belong here.",
        "secret": "This is a UNH membership token. It guarantees aid from any healer in the network. "
                  "How did Fitzroy acquire it? From whom?",
        "lore": "Lizzy would recognize this instantly. "
                "Someone in the Underground Network trusted the wrong person.",
        "uv_text": "UNH — COMPROMISED AGENT?",
    },
    {
        "id": "unmarked_bottle",
        "name": "Unmarked Bottle",
        "description": "A small bottle with no label. The glass is thick, the stopper sealed with black wax. "
                       "The liquid inside catches light strangely.",
        "secret": "No one knows what this contains. Including, perhaps, Fitzroy himself. "
                  "It was sent to him anonymously with a note: 'For when the time comes.'",
        "lore": "Fitzroy keeps it at the very back of the lowest shelf. "
                "He has never opened it. He has never thrown it away.",
        "uv_text": "???",
    },
    {
        "id": "sealed_letter",
        "name": "A Sealed Letter",
        "description": "A cream envelope, sealed with plain red wax. "
                       "Addressed in elegant script but never sent.",
        "secret": "The address reads: 'Rev. E. Cartwright, Society of Friends Meeting House, Whitechapel.' "
                  "Alistair wrote to his brother. And couldn't send it.",
        "lore": "What does a man say to the brother he destroyed? "
                "Whatever is written here, it has been sealed for three years.",
        "uv_text": "TO ELIJAH — UNSENT",
    },
]


# =============================================================================
# MIXING RECIPES
# =============================================================================

MIXING_RECIPES = [
    {
        "id": "infant_poison",
        "ingredients": ["laudanum", "paregoric"],
        "name": "The Tainted Tonic",
        "result_color": "#8b4513",
        "description": "You've recreated the contaminated infant medicine. "
                       "Laudanum concentrated in a paregoric base — three times the labeled dose.",
        "lore": "This is what killed the babies. Not witchcraft. Not tainted breastmilk. "
                "Chemistry, manufactured by a Red Rose front charity and sold to trusting mothers.",
        "danger": 5,
    },
    {
        "id": "sedation_protocol",
        "ingredients": ["laudanum", "chloroform"],
        "name": "Fitzroy's Sedation Protocol",
        "result_color": "#5a3a1a",
        "description": "Oral laudanum for baseline sedation, chloroform for acute episodes. "
                       "The two-stage protocol used to keep Sebastian compliant.",
        "lore": "Not enough to kill. Just enough to erase resistance. "
                "Fitzroy calibrated this over months of observation.",
        "danger": 4,
    },
    {
        "id": "beauty_death",
        "ingredients": ["arsenic_wafers", "belladonna"],
        "name": "The Beauty Regimen",
        "result_color": "#d4a0d4",
        "description": "Arsenic for pale skin, belladonna for wide dark eyes. "
                       "The fashionable Victorian woman's toilette — and slow suicide.",
        "lore": "Beatrice used both. The Midnight Salon knew. "
                "No one said anything because every woman in the room did the same.",
        "danger": 3,
    },
    {
        "id": "ritual_compound",
        "ingredients": ["belladonna", "distilled_blood"],
        "name": "The Crimson Veil Sacrament",
        "result_color": "#4a0020",
        "description": "Belladonna for 'inner sight,' blood serum for 'communion.' "
                       "Isabella's ritual compound for Order ceremonies.",
        "lore": "The Order believed this mixture allowed communication with the divine. "
                "In reality, it induced hallucinatory euphoria and dependency.",
        "danger": 5,
    },
    {
        "id": "mercurial_treatment",
        "ingredients": ["mercury", "dovers_powder"],
        "name": "Standard Syphilis Treatment",
        "result_color": "#7a8a9a",
        "description": "Mercury for the disease, Dover's Powder for the agony of the cure. "
                       "The patient suffers either way.",
        "lore": "Fitzroy published a paper arguing that mercury treatment "
                "was worse than the disease. The paper was suppressed.",
        "danger": 3,
    },
    {
        "id": "emergency_revival",
        "ingredients": ["smelling_salts", "ether"],
        "name": "Emergency Resuscitation",
        "result_color": "#e8e8d0",
        "description": "Ammonia inhalation with ether vapour. A brutal jolt to consciousness. "
                       "Used when a patient stops breathing during surgery.",
        "lore": "Every surgery carried the risk. The line between sleep and death "
                "was measured in drops and seconds.",
        "danger": 2,
    },
    {
        "id": "murder_cocktail",
        "ingredients": ["strychnine", "chloroform"],
        "name": "The Silent End",
        "result_color": "#1a0a0a",
        "description": "Chloroform to render unconscious, strychnine to stop the heart. "
                       "Virtually undetectable in an era before modern toxicology.",
        "lore": "This combination appears in Thomas Blackwood's notes "
                "beside the names of three women who died 'of natural causes.'",
        "danger": 5,
    },
    {
        "id": "research_serum",
        "ingredients": ["distilled_blood", "fitzroy_tonic"],
        "name": "The Fitzroy Synthesis",
        "result_color": "#6a0a2a",
        "description": "Blood serum stabilized with the pediatric compound. "
                       "Fitzroy's attempt to cure Sebastian's blood disorder.",
        "lore": "It almost worked. Almost. The side effects were... unpredictable. "
                "Fitzroy's notebook records the results with clinical detachment.",
        "danger": 4,
    },
    {
        "id": "romani_remedy",
        "ingredients": ["dovers_powder", "smelling_salts"],
        "name": "Healer's Revival Tonic",
        "result_color": "#8a9a6a",
        "description": "Pain management with respiratory stimulation. "
                       "A combination the Underground Network of Healers uses regularly.",
        "lore": "Lizzy Reed taught this to Elijah. 'Sometimes old medicine and new medicine "
                "agree,' she told him. 'That is how you know it is true.'",
        "danger": 1,
    },
    {
        "id": "poison_ring",
        "ingredients": ["belladonna", "chloroform"],
        "name": "Thomas's Poison Ring Formula",
        "result_color": "#2a1a3a",
        "description": "A concentrated soporific. Small enough dose to fit in a ring compartment. "
                       "Slipped into a drink, it produces confusion, suggestibility, and amnesia.",
        "lore": "This is how Thomas drugged his victims before the phonograph recordings. "
                "Evelyn was dosed with this at the Anatomy Club.",
        "danger": 4,
    },
]


# =============================================================================
# SECRETS (unlockable based on interactions)
# =============================================================================

CABINET_SECRETS = [
    {
        "id": "fitzroy_legacy",
        "title": "The Fitzroy Legacy",
        "condition": "examine_5_items",
        "content": "You've examined enough to see the pattern. Every item in this cabinet "
                   "tells the same story: a brilliant man who believed knowledge justified anything. "
                   "The instruments, the specimens, the drugs — they are his autobiography in objects.",
    },
    {
        "id": "sebastian_trail",
        "title": "Sebastian's Trail",
        "condition": "examine_laudanum_and_syringe_and_blood",
        "content": "Laudanum. Syringe. Blood samples. You've traced the path of Sebastian's captivity "
                   "through the objects that maintained it. The cabinet is a prison disguised as a pharmacy.",
    },
    {
        "id": "infant_truth",
        "title": "The Truth About the Babies",
        "condition": "mix_infant_poison",
        "content": "You've recreated the contaminated tonic. The moral panic blamed Romani wet nurses "
                   "and 'fallen women.' The truth was always in the chemistry — manufactured by men "
                   "who called themselves healers and distributed through charities they controlled.",
    },
    {
        "id": "brothers_divided",
        "title": "Brothers Divided",
        "condition": "examine_choir_and_letter",
        "content": "The choir sheets and the unsent letter. Two brothers who once sang in harmony. "
                   "One chose science without mercy. One chose mercy without science. "
                   "The cabinet holds one brother's regret. The meeting house holds the other's.",
    },
    {
        "id": "hidden_drawer",
        "title": "The Hidden Drawer",
        "condition": "examine_all_personal",
        "content": "Behind the false back of the lowest shelf, your fingers find a catch. "
                   "A drawer slides out. Inside: a single page torn from the Black Book, "
                   "listing seven names. Three are crossed out. The ink is fresh.",
    },
]


# =============================================================================
# SHELF LABELS
# =============================================================================

SHELF_LABELS = {
    0: "Tinctures & Tonics",
    1: "Compounds & Preparations",
    2: "Surgical Instruments",
    3: "Specimens & Evidence",
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_items():
    """Return all cabinet items organized by shelf."""
    items = {}
    for shelf_num in range(4):
        items[shelf_num] = {
            "bottles": [b for b in BOTTLES if b.get("shelf") == shelf_num],
            "instruments": [i for i in INSTRUMENTS if i.get("shelf") == shelf_num],
            "specimens": [s for s in SPECIMENS if s.get("shelf") == shelf_num],
        }
    return items


def get_item_by_id(item_id: str):
    """Find any item by its ID across all categories."""
    for item in BOTTLES + INSTRUMENTS + SPECIMENS + PERSONAL_ITEMS:
        if item["id"] == item_id:
            return item
    return None


def get_mixing_result(id1: str, id2: str):
    """Check if two bottle IDs produce a known mixing result."""
    for recipe in MIXING_RECIPES:
        ingredients = set(recipe["ingredients"])
        if ingredients == {id1, id2}:
            return recipe
    return None


def get_bottles_for_mixing():
    """Return only bottles that have mixing_tags (can be mixed)."""
    return [b for b in BOTTLES if b.get("mixing_tags")]


def check_cabinet_secret(secret, examined_items, examined_specimens, mixed_recipes):
    """Check if a cabinet secret condition has been met."""
    condition = secret["condition"]

    if condition == "examine_5_items":
        return len(examined_items) + len(examined_specimens) >= 5

    if condition == "examine_laudanum_and_syringe_and_blood":
        needed = {"laudanum", "syringe", "blood_rack"}
        return needed.issubset(set(examined_items) | set(examined_specimens))

    if condition == "mix_infant_poison":
        return "infant_poison" in mixed_recipes

    if condition == "examine_choir_and_letter":
        needed = {"choir_sheets", "sealed_letter"}
        return needed.issubset(set(examined_items))

    if condition == "examine_all_personal":
        all_personal = {p["id"] for p in PERSONAL_ITEMS}
        return all_personal.issubset(set(examined_items))

    return False
