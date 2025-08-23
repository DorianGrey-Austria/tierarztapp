// Comprehensive Veterinary Medical Data for Scanner Simulation Game
// Data compiled from veterinary medical sources with German terminology where appropriate

export const ANIMAL_SPECIES = [
  // Common Pets
  {
    id: 'dog',
    name: 'Hund',
    englishName: 'Dog',
    category: 'pet',
    vitalSigns: {
      heartRate: { min: 60, max: 180, unit: 'BPM' },
      temperature: { min: 37.5, max: 39.2, unit: '°C' }, // 99.5-102.5°F
      respiratoryRate: { min: 15, max: 30, unit: '/min' },
      bloodPressure: { systolic: { min: 110, max: 160 }, diastolic: { min: 60, max: 90 }, unit: 'mmHg' },
      bloodGlucose: { min: 80, max: 120, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Parvovirose',
      'Staupe',
      'Zwingerhusten',
      'Hepatitis contagiosa canis',
      'Magendrehung',
      'Hüftdysplasie',
      'Diabetes mellitus',
      'Epilepsie',
      'Katarakt',
      'Rundwurm-Infektion'
    ]
  },
  {
    id: 'cat',
    name: 'Katze',
    englishName: 'Cat',
    category: 'pet',
    vitalSigns: {
      heartRate: { min: 100, max: 140, unit: 'BPM' },
      temperature: { min: 37.8, max: 39.4, unit: '°C' }, // 100-103.1°F
      respiratoryRate: { min: 20, max: 30, unit: '/min' },
      bloodPressure: { systolic: { min: 120, max: 170 }, diastolic: { min: 70, max: 120 }, unit: 'mmHg' },
      bloodGlucose: { min: 80, max: 120, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Katzenseuche',
      'FIV (Katzen-AIDS)',
      'Katzenleukose',
      'Katzenschnupfen',
      'FIP (Feline Infektiöse Peritonitis)',
      'Niereninsuffizienz',
      'Hyperthyreose',
      'Diabetes mellitus',
      'Arthritis',
      'Zahnstein'
    ]
  },
  {
    id: 'rabbit',
    name: 'Kaninchen',
    englishName: 'Rabbit',
    category: 'pet',
    vitalSigns: {
      heartRate: { min: 120, max: 325, unit: 'BPM' },
      temperature: { min: 38.0, max: 40.6, unit: '°C' }, // 100.4-105°F
      respiratoryRate: { min: 30, max: 60, unit: '/min' },
      bloodPressure: { systolic: { min: 90, max: 130 }, diastolic: { min: 60, max: 90 }, unit: 'mmHg' },
      bloodGlucose: { min: 75, max: 155, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Myxomatose',
      'RHD (Rabbit Hemorrhagic Disease)',
      'Pasteurellose',
      'E. cuniculi',
      'Zahnprobleme',
      'GI-Stasis',
      'Kokzidiose',
      'Milbenbefall',
      'Abszesse',
      'Harnschlamm'
    ]
  },
  {
    id: 'guinea_pig',
    name: 'Meerschweinchen',
    englishName: 'Guinea Pig',
    category: 'pet',
    vitalSigns: {
      heartRate: { min: 230, max: 380, unit: 'BPM' },
      temperature: { min: 37.2, max: 39.5, unit: '°C' },
      respiratoryRate: { min: 42, max: 104, unit: '/min' },
      bloodPressure: { systolic: { min: 80, max: 120 }, diastolic: { min: 50, max: 80 }, unit: 'mmHg' },
      bloodGlucose: { min: 60, max: 125, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Skorbut (Vitamin C-Mangel)',
      'Atemwegsinfektionen',
      'Harnsteine',
      'Pilzinfektionen',
      'Milbenbefall',
      'Zahnprobleme',
      'Trichophyton mentagrophytes',
      'Salmonellose',
      'Verdauungsstörungen',
      'Geburtskomplikationen'
    ]
  },
  {
    id: 'hamster',
    name: 'Hamster',
    englishName: 'Hamster',
    category: 'pet',
    vitalSigns: {
      heartRate: { min: 280, max: 500, unit: 'BPM' },
      temperature: { min: 36.0, max: 38.0, unit: '°C' },
      respiratoryRate: { min: 35, max: 135, unit: '/min' },
      bloodPressure: { systolic: { min: 70, max: 110 }, diastolic: { min: 40, max: 70 }, unit: 'mmHg' },
      bloodGlucose: { min: 60, max: 135, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Wet Tail (Proliferative Ileitis)',
      'Diabetes mellitus',
      'Herzinsuffizienz',
      'Pilzinfektionen',
      'Milbenbefall',
      'Durchfall',
      'Atemwegsinfektionen',
      'Tumore',
      'Augenentzündungen',
      'Salmonellose'
    ]
  },
  {
    id: 'bird',
    name: 'Vogel',
    englishName: 'Bird',
    category: 'pet',
    vitalSigns: {
      heartRate: { min: 150, max: 600, unit: 'BPM' },
      temperature: { min: 40.0, max: 42.0, unit: '°C' },
      respiratoryRate: { min: 15, max: 45, unit: '/min' },
      bloodPressure: { systolic: { min: 120, max: 200 }, diastolic: { min: 80, max: 140 }, unit: 'mmHg' },
      bloodGlucose: { min: 200, max: 400, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Psittakose',
      'PBFD (Psittacine Beak and Feather Disease)',
      'Aspergillose',
      'Atemwegsinfektionen',
      'Federpicken',
      'Salmonellose',
      'Gicht',
      'Legenot',
      'Kropfentzündung',
      'Vitamin A-Mangel'
    ]
  },
  {
    id: 'reptile',
    name: 'Reptil',
    englishName: 'Reptile',
    category: 'pet',
    vitalSigns: {
      heartRate: { min: 20, max: 80, unit: 'BPM' },
      temperature: { min: 20.0, max: 35.0, unit: '°C' }, // Varies greatly by species
      respiratoryRate: { min: 2, max: 20, unit: '/min' },
      bloodPressure: { systolic: { min: 40, max: 80 }, diastolic: { min: 20, max: 50 }, unit: 'mmHg' },
      bloodGlucose: { min: 50, max: 150, unit: 'mg/dL' },
      oxygenSaturation: { min: 85, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Salmonellose',
      'Rachitis (MBD)',
      'Atemwegsinfektionen',
      'Parasiten',
      'Häutungsprobleme',
      'Mundfäule',
      'Legenot',
      'Verstopfung',
      'Pilzinfektionen',
      'Augeninfektionen'
    ]
  },

  // Farm Animals
  {
    id: 'horse',
    name: 'Pferd',
    englishName: 'Horse',
    category: 'farm',
    vitalSigns: {
      heartRate: { min: 28, max: 44, unit: 'BPM' },
      temperature: { min: 37.0, max: 38.5, unit: '°C' },
      respiratoryRate: { min: 8, max: 16, unit: '/min' },
      bloodPressure: { systolic: { min: 110, max: 140 }, diastolic: { min: 70, max: 100 }, unit: 'mmHg' },
      bloodGlucose: { min: 75, max: 115, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Kolik',
      'Lahmheit',
      'Equine Influenza',
      'Strangles (Druse)',
      'Equines Herpesvirus',
      'Hufrehe',
      'Arthritis',
      'Magengeschwüre',
      'Tetanus',
      'Respiratory Disease Complex'
    ]
  },
  {
    id: 'cow',
    name: 'Kuh',
    englishName: 'Cow',
    category: 'farm',
    vitalSigns: {
      heartRate: { min: 60, max: 80, unit: 'BPM' },
      temperature: { min: 38.0, max: 39.5, unit: '°C' },
      respiratoryRate: { min: 12, max: 36, unit: '/min' },
      bloodPressure: { systolic: { min: 140, max: 180 }, diastolic: { min: 90, max: 120 }, unit: 'mmHg' },
      bloodGlucose: { min: 45, max: 75, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Mastitis',
      'Milchfieber',
      'Ketose',
      'Labmagenverlagerung',
      'Klauenerkrankungen',
      'BVD (Bovine Virusdiarrhoe)',
      'IBR (Infektiöse Bovine Rhinotracheitis)',
      'Brucellose',
      'Lungenentzündung',
      'Gebärparese'
    ]
  },
  {
    id: 'pig',
    name: 'Schwein',
    englishName: 'Pig',
    category: 'farm',
    vitalSigns: {
      heartRate: { min: 70, max: 120, unit: 'BPM' },
      temperature: { min: 38.0, max: 39.0, unit: '°C' },
      respiratoryRate: { min: 8, max: 18, unit: '/min' },
      bloodPressure: { systolic: { min: 120, max: 160 }, diastolic: { min: 80, max: 110 }, unit: 'mmHg' },
      bloodGlucose: { min: 65, max: 95, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Schweinepest',
      'PRRS (Porcine Reproductive and Respiratory Syndrome)',
      'Aujeszkysche Krankheit',
      'APP (Actinobacillus pleuropneumoniae)',
      'Dysenterie',
      'Ileitis',
      'Magengeschwüre',
      'Ferkelruß',
      'MMA-Syndrom',
      'Streptokokkose'
    ]
  },
  {
    id: 'sheep',
    name: 'Schaf',
    englishName: 'Sheep',
    category: 'farm',
    vitalSigns: {
      heartRate: { min: 70, max: 90, unit: 'BPM' },
      temperature: { min: 38.5, max: 39.5, unit: '°C' },
      respiratoryRate: { min: 12, max: 20, unit: '/min' },
      bloodPressure: { systolic: { min: 90, max: 130 }, diastolic: { min: 60, max: 90 }, unit: 'mmHg' },
      bloodGlucose: { min: 50, max: 80, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Scrapie',
      'Maedi-Visna',
      'Listeriose',
      'Klauenfäule',
      'Wurmbefall',
      'Gebärparese',
      'Tetanus',
      'Q-Fieber',
      'Blauzungenkrankheit',
      'Lungenentzündung'
    ]
  },
  {
    id: 'goat',
    name: 'Ziege',
    englishName: 'Goat',
    category: 'farm',
    vitalSigns: {
      heartRate: { min: 70, max: 90, unit: 'BPM' },
      temperature: { min: 38.5, max: 39.5, unit: '°C' },
      respiratoryRate: { min: 12, max: 20, unit: '/min' },
      bloodPressure: { systolic: { min: 90, max: 130 }, diastolic: { min: 60, max: 90 }, unit: 'mmHg' },
      bloodGlucose: { min: 50, max: 80, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'CAE (Caprine Arthritis-Encephalitis)',
      'Caseous Lymphadenitis',
      'Listeriose',
      'Wurmbefall',
      'Klauenfäule',
      'Ketose',
      'Pneumonie',
      'Q-Fieber',
      'Enterotoxämie',
      'Mastitis'
    ]
  },
  {
    id: 'chicken',
    name: 'Huhn',
    englishName: 'Chicken',
    category: 'farm',
    vitalSigns: {
      heartRate: { min: 250, max: 300, unit: 'BPM' },
      temperature: { min: 40.5, max: 42.0, unit: '°C' },
      respiratoryRate: { min: 12, max: 37, unit: '/min' },
      bloodPressure: { systolic: { min: 120, max: 180 }, diastolic: { min: 80, max: 120 }, unit: 'mmHg' },
      bloodGlucose: { min: 200, max: 400, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Newcastle Disease',
      'Aviäre Influenza',
      'Infektiöse Bronchitis',
      'Mareksche Krankheit',
      'Kokzidiose',
      'Salmonellose',
      'E. coli-Infektion',
      'Legenot',
      'Kalkbeinmilben',
      'Federpicken'
    ]
  },

  // Exotic Pets
  {
    id: 'ferret',
    name: 'Frettchen',
    englishName: 'Ferret',
    category: 'exotic',
    vitalSigns: {
      heartRate: { min: 180, max: 250, unit: 'BPM' },
      temperature: { min: 37.8, max: 40.0, unit: '°C' },
      respiratoryRate: { min: 33, max: 36, unit: '/min' },
      bloodPressure: { systolic: { min: 90, max: 140 }, diastolic: { min: 60, max: 90 }, unit: 'mmHg' },
      bloodGlucose: { min: 90, max: 125, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Insulinom',
      'Nebennierenerkrankung',
      'Lymphom',
      'Kardiomyopathie',
      'Staupe',
      'Influenza',
      'Helicobacter mustelae',
      'Urolithiasis',
      'Zahnprobleme',
      'Haarballenbildung'
    ]
  },
  {
    id: 'hedgehog',
    name: 'Igel',
    englishName: 'Hedgehog',
    category: 'exotic',
    vitalSigns: {
      heartRate: { min: 190, max: 280, unit: 'BPM' },
      temperature: { min: 35.0, max: 37.0, unit: '°C' },
      respiratoryRate: { min: 25, max: 50, unit: '/min' },
      bloodPressure: { systolic: { min: 80, max: 120 }, diastolic: { min: 50, max: 80 }, unit: 'mmHg' },
      bloodGlucose: { min: 70, max: 140, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Wobbly Hedgehog Syndrome',
      'Hautinfektionen',
      'Milbenbefall',
      'Salmonellose',
      'Fettleber',
      'Herzerkrankungen',
      'Tumore',
      'Zahnprobleme',
      'Verstopfung',
      'Hypothermie'
    ]
  },
  {
    id: 'chinchilla',
    name: 'Chinchilla',
    englishName: 'Chinchilla',
    category: 'exotic',
    vitalSigns: {
      heartRate: { min: 100, max: 150, unit: 'BPM' },
      temperature: { min: 36.0, max: 38.0, unit: '°C' },
      respiratoryRate: { min: 40, max: 65, unit: '/min' },
      bloodPressure: { systolic: { min: 80, max: 120 }, diastolic: { min: 50, max: 80 }, unit: 'mmHg' },
      bloodGlucose: { min: 60, max: 120, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Pilzinfektionen',
      'Hitzschlag',
      'Zahnprobleme',
      'GI-Stasis',
      'Blasensteine',
      'Pelzverlust',
      'Durchfall',
      'Atemwegsinfektionen',
      'Augenentzündungen',
      'Verletzungen'
    ]
  },
  {
    id: 'sugar_glider',
    name: 'Kurzkopfgleitbeutler',
    englishName: 'Sugar Glider',
    category: 'exotic',
    vitalSigns: {
      heartRate: { min: 200, max: 300, unit: 'BPM' },
      temperature: { min: 36.0, max: 37.0, unit: '°C' },
      respiratoryRate: { min: 16, max: 40, unit: '/min' },
      bloodPressure: { systolic: { min: 80, max: 120 }, diastolic: { min: 50, max: 80 }, unit: 'mmHg' },
      bloodGlucose: { min: 80, max: 140, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Calcium-Mangel',
      'Selbstverstümmelung',
      'Salmonellose',
      'Parasiten',
      'Zahnprobleme',
      'Verstopfung',
      'Dehydration',
      'Stress-bedingte Erkrankungen',
      'Verletzungen',
      'Augenprobleme'
    ]
  }
];

export const MEDICAL_CONDITIONS = [
  // Emergency Conditions
  {
    id: 'fracture',
    name: 'Fraktur',
    englishName: 'Fracture',
    category: 'emergency',
    severity: 'high',
    description: 'Knochenbruch durch Trauma oder Sturz',
    symptoms: ['Schmerzen', 'Schwellung', 'Lahmheit', 'sichtbare Deformation'],
    treatment: 'Ruhigstellung, Schmerzmittel, chirurgische Versorgung',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'bird', 'horse', 'cow', 'sheep', 'goat']
  },
  {
    id: 'poisoning',
    name: 'Vergiftung',
    englishName: 'Poisoning',
    category: 'emergency',
    severity: 'critical',
    description: 'Aufnahme giftiger Substanzen',
    symptoms: ['Erbrechen', 'Durchfall', 'Atemnot', 'Krämpfe', 'Bewusstlosigkeit'],
    treatment: 'Dekontamination, Antidot, Intensivbehandlung',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'guinea_pig', 'hamster', 'bird', 'horse']
  },
  {
    id: 'bloat',
    name: 'Magendrehung',
    englishName: 'Gastric Dilatation-Volvulus',
    category: 'emergency',
    severity: 'critical',
    description: 'Lebensbedrohliche Verdrehung und Aufblähung des Magens',
    symptoms: ['Aufgeblähter Bauch', 'Würgereiz ohne Erbrechen', 'Unruhe', 'Schock'],
    treatment: 'Sofortige chirurgische Intervention',
    affectedSpecies: ['dog', 'horse']
  },
  {
    id: 'respiratory_distress',
    name: 'Atemnot',
    englishName: 'Respiratory Distress',
    category: 'emergency',
    severity: 'high',
    description: 'Schwere Atemprobleme mit Sauerstoffmangel',
    symptoms: ['Schnelle Atmung', 'Blaue Schleimhäute', 'Panik', 'Maulatmung'],
    treatment: 'Sauerstoffgabe, Bronchodilatatoren, Notfallbehandlung',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'guinea_pig', 'bird', 'ferret', 'hedgehog']
  },
  {
    id: 'shock',
    name: 'Schock',
    englishName: 'Shock',
    category: 'emergency',
    severity: 'critical',
    description: 'Kreislaufversagen mit Organminderdurchblutung',
    symptoms: ['Schwacher Puls', 'Blasse Schleimhäute', 'Hypothermie', 'Bewusstseinstrübung'],
    treatment: 'Infusionstherapie, Kreislaufstabilisierung',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'horse', 'cow', 'pig', 'sheep', 'goat']
  },

  // Chronic Diseases
  {
    id: 'diabetes',
    name: 'Diabetes mellitus',
    englishName: 'Diabetes mellitus',
    category: 'chronic',
    severity: 'medium',
    description: 'Störung des Zuckerstoffwechsels',
    symptoms: ['Vermehrtes Trinken', 'Häufiges Urinieren', 'Gewichtsverlust', 'Schwäche'],
    treatment: 'Insulin, Diät, regelmäßige Kontrollen',
    affectedSpecies: ['dog', 'cat', 'hamster', 'ferret']
  },
  {
    id: 'kidney_disease',
    name: 'Niereninsuffizienz',
    englishName: 'Kidney Disease',
    category: 'chronic',
    severity: 'high',
    description: 'Fortschreitende Verschlechterung der Nierenfunktion',
    symptoms: ['Vermehrtes Trinken', 'Gewichtsverlust', 'Erbrechen', 'Müdigkeit'],
    treatment: 'Spezialdiät, Medikamente, Flüssigkeitstherapie',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'ferret']
  },
  {
    id: 'arthritis',
    name: 'Arthritis',
    englishName: 'Arthritis',
    category: 'chronic',
    severity: 'medium',
    description: 'Entzündliche Gelenkerkrankung',
    symptoms: ['Lahmheit', 'Steifheit', 'Schmerzen', 'reduzierte Beweglichkeit'],
    treatment: 'Schmerzmittel, Physiotherapie, Gewichtsmanagement',
    affectedSpecies: ['dog', 'cat', 'horse', 'cow', 'sheep', 'goat']
  },
  {
    id: 'heart_disease',
    name: 'Herzerkrankung',
    englishName: 'Heart Disease',
    category: 'chronic',
    severity: 'high',
    description: 'Verschiedene Erkrankungen des Herz-Kreislauf-Systems',
    symptoms: ['Atemnot', 'Husten', 'Schwäche', 'Ödeme'],
    treatment: 'Herzmedikamente, Diuretika, Ruhe',
    affectedSpecies: ['dog', 'cat', 'hamster', 'ferret', 'hedgehog']
  },
  {
    id: 'epilepsy',
    name: 'Epilepsie',
    englishName: 'Epilepsy',
    category: 'chronic',
    severity: 'medium',
    description: 'Neurologische Erkrankung mit wiederkehrenden Anfällen',
    symptoms: ['Krampfanfälle', 'Bewusstseinsverlust', 'Zuckungen', 'Verwirrung'],
    treatment: 'Antiepileptika, Anfallskontrolle',
    affectedSpecies: ['dog', 'cat', 'ferret']
  },

  // Infectious Diseases
  {
    id: 'parvovirus',
    name: 'Parvovirose',
    englishName: 'Parvovirus',
    category: 'infectious',
    severity: 'high',
    description: 'Hochansteckende virale Darmerkrankung',
    symptoms: ['Blutiger Durchfall', 'Erbrechen', 'Fieber', 'Dehydration'],
    treatment: 'Supportive Therapie, Flüssigkeitsersatz, Antibiotika',
    affectedSpecies: ['dog']
  },
  {
    id: 'fiv',
    name: 'FIV (Katzen-AIDS)',
    englishName: 'Feline Immunodeficiency Virus',
    category: 'infectious',
    severity: 'high',
    description: 'Immunschwächevirus bei Katzen',
    symptoms: ['Immunschwäche', 'wiederkehrende Infektionen', 'Gewichtsverlust'],
    treatment: 'Symptomatische Behandlung, Immunsystem stärken',
    affectedSpecies: ['cat']
  },
  {
    id: 'rabies',
    name: 'Tollwut',
    englishName: 'Rabies',
    category: 'infectious',
    severity: 'critical',
    description: 'Tödliche virale Gehirnentzündung',
    symptoms: ['Verhaltensänderungen', 'Aggression', 'Lähmungen', 'Hydrophobie'],
    treatment: 'Keine Behandlung möglich - Prävention durch Impfung',
    affectedSpecies: ['dog', 'cat', 'horse', 'cow', 'pig', 'sheep', 'goat']
  },
  {
    id: 'distemper',
    name: 'Staupe',
    englishName: 'Distemper',
    category: 'infectious',
    severity: 'high',
    description: 'Virale Mehrorganerkrankung',
    symptoms: ['Fieber', 'Nasenausfluss', 'Husten', 'neurologische Symptome'],
    treatment: 'Supportive Therapie, keine spezifische Behandlung',
    affectedSpecies: ['dog', 'ferret']
  },
  {
    id: 'kennel_cough',
    name: 'Zwingerhusten',
    englishName: 'Kennel Cough',
    category: 'infectious',
    severity: 'low',
    description: 'Hochansteckende Atemwegserkrankung',
    symptoms: ['Trockener Husten', 'Würgen', 'leichtes Fieber'],
    treatment: 'Hustenstiller, Antibiotika bei bakterieller Beteiligung',
    affectedSpecies: ['dog']
  },

  // Parasitic Conditions
  {
    id: 'fleas',
    name: 'Flohbefall',
    englishName: 'Flea Infestation',
    category: 'parasitic',
    severity: 'low',
    description: 'Befall mit blutsaugenden Flöhen',
    symptoms: ['Juckreiz', 'Kratzen', 'Hautrötungen', 'kleine braune Insekten'],
    treatment: 'Antiparasitika, Umgebungsbehandlung',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'guinea_pig', 'hamster', 'ferret']
  },
  {
    id: 'ticks',
    name: 'Zeckenbefall',
    englishName: 'Tick Infestation',
    category: 'parasitic',
    severity: 'medium',
    description: 'Befall mit Zecken und mögliche Krankheitsübertragung',
    symptoms: ['Sichtbare Zecken', 'Hautentzündungen', 'mögliche Sekundärerkrankungen'],
    treatment: 'Zeckenentfernung, Antiparasitika, Überwachung auf Folgeerkrankungen',
    affectedSpecies: ['dog', 'cat', 'horse', 'cow', 'sheep', 'goat']
  },
  {
    id: 'roundworms',
    name: 'Rundwurm-Infektion',
    englishName: 'Roundworm Infection',
    category: 'parasitic',
    severity: 'medium',
    description: 'Darmparasiten verschiedener Rundwurmarten',
    symptoms: ['Durchfall', 'Erbrechen', 'aufgeblähter Bauch', 'Gewichtsverlust'],
    treatment: 'Entwurmung mit spezifischen Antiparasitika',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'guinea_pig', 'hamster', 'horse', 'pig']
  },
  {
    id: 'mites',
    name: 'Milbenbefall',
    englishName: 'Mite Infestation',
    category: 'parasitic',
    severity: 'medium',
    description: 'Hautparasiten verschiedener Milbenarten',
    symptoms: ['Starker Juckreiz', 'Haarausfall', 'Hautverdickungen', 'Krusten'],
    treatment: 'Akarizide, medizinische Bäder, Umgebungsbehandlung',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'guinea_pig', 'hamster', 'hedgehog', 'chicken']
  },
  {
    id: 'tapeworms',
    name: 'Bandwurm-Infektion',
    englishName: 'Tapeworm Infection',
    category: 'parasitic',
    severity: 'medium',
    description: 'Darmparasiten der Bandwurmfamilie',
    symptoms: ['Segmente im Kot', 'Juckreiz am After', 'Gewichtsverlust'],
    treatment: 'Spezifische Entwurmung gegen Bandwürmer',
    affectedSpecies: ['dog', 'cat', 'horse', 'cow', 'pig', 'sheep']
  },

  // Breed-specific Conditions
  {
    id: 'hip_dysplasia',
    name: 'Hüftdysplasie',
    englishName: 'Hip Dysplasia',
    category: 'genetic',
    severity: 'medium',
    description: 'Fehlentwicklung des Hüftgelenks',
    symptoms: ['Lahmheit', 'Steifheit', 'Schmerzen beim Aufstehen'],
    treatment: 'Schmerzmittel, Physiotherapie, ggf. Operation',
    affectedSpecies: ['dog', 'cat']
  },
  {
    id: 'cataracts',
    name: 'Katarakt',
    englishName: 'Cataracts',
    category: 'genetic',
    severity: 'medium',
    description: 'Trübung der Augenlinse',
    symptoms: ['Sehstörungen', 'milchige Augen', 'Orientierungslosigkeit'],
    treatment: 'Chirurgische Entfernung bei schweren Fällen',
    affectedSpecies: ['dog', 'cat', 'rabbit']
  },
  {
    id: 'bloat_susceptibility',
    name: 'Magendrehungsneigung',
    englishName: 'Bloat Susceptibility',
    category: 'genetic',
    severity: 'high',
    description: 'Erhöhte Anfälligkeit für Magendrehung bei großen Hunderassen',
    symptoms: ['Präventionsmaßnahmen erforderlich'],
    treatment: 'Fütterungsmanagement, prophylaktische Gastropexie',
    affectedSpecies: ['dog']
  },

  // Age-related Conditions
  {
    id: 'dental_disease',
    name: 'Zahnerkrankungen',
    englishName: 'Dental Disease',
    category: 'age_related',
    severity: 'medium',
    description: 'Zahnstein, Gingivitis und Parodontitis',
    symptoms: ['Mundgeruch', 'Zahnstein', 'Zahnfleischentzündung', 'Schmerzen beim Fressen'],
    treatment: 'Zahnreinigung, Zahnextraktion, regelmäßige Dentalprophylaxe',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'guinea_pig', 'ferret', 'chinchilla']
  },
  {
    id: 'cognitive_dysfunction',
    name: 'Demenz',
    englishName: 'Cognitive Dysfunction',
    category: 'age_related',
    severity: 'medium',
    description: 'Altersbedingter geistiger Abbau',
    symptoms: ['Verwirrung', 'Orientierungslosigkeit', 'Verhaltensänderungen'],
    treatment: 'Medikamente zur Hirnleistungsförderung, Umgebungsanpassung',
    affectedSpecies: ['dog', 'cat']
  },
  {
    id: 'osteoporosis',
    name: 'Osteoporose',
    englishName: 'Osteoporosis',
    category: 'age_related',
    severity: 'medium',
    description: 'Altersbedingter Knochenschwund',
    symptoms: ['Erhöhte Frakturneigung', 'Schmerzen', 'Bewegungseinschränkungen'],
    treatment: 'Calcium- und Vitamin D-Supplementierung, Bewegung',
    affectedSpecies: ['dog', 'cat', 'horse', 'cow']
  },

  // Species-specific conditions
  {
    id: 'myxomatosis',
    name: 'Myxomatose',
    englishName: 'Myxomatosis',
    category: 'infectious',
    severity: 'critical',
    description: 'Tödliche Viruserkrankung bei Kaninchen',
    symptoms: ['Schwellungen', 'Ödeme', 'Fieber', 'Atemnot'],
    treatment: 'Keine spezifische Behandlung - Prävention durch Impfung',
    affectedSpecies: ['rabbit']
  },
  {
    id: 'gi_stasis',
    name: 'GI-Stasis',
    englishName: 'Gastrointestinal Stasis',
    category: 'emergency',
    severity: 'high',
    description: 'Darmträgheit bei Kleinnagern',
    symptoms: ['Appetitlosigkeit', 'kein Kot', 'Aufblähung', 'Lethargie'],
    treatment: 'Motilitätsfördernde Medikamente, Zwangsfütterung, Flüssigkeitstherapie',
    affectedSpecies: ['rabbit', 'guinea_pig', 'chinchilla']
  },
  {
    id: 'wet_tail',
    name: 'Wet Tail',
    englishName: 'Proliferative Ileitis',
    category: 'infectious',
    severity: 'high',
    description: 'Bakterielle Darmentzündung bei Hamstern',
    symptoms: ['Wässriger Durchfall', 'nasser Schwanz', 'Lethargie', 'Dehydration'],
    treatment: 'Antibiotika, Flüssigkeitsersatz, Isolierung',
    affectedSpecies: ['hamster']
  },
  {
    id: 'egg_binding',
    name: 'Legenot',
    englishName: 'Egg Binding',
    category: 'emergency',
    severity: 'high',
    description: 'Ei bleibt im Legetrakt stecken',
    symptoms: ['Anstrengung ohne Eiablage', 'Schwäche', 'aufgeplustertes Gefieder'],
    treatment: 'Manueller Eingriff, Oxytocin, ggf. chirurgische Entfernung',
    affectedSpecies: ['bird', 'chicken', 'reptile']
  },
  {
    id: 'respiratory_infection',
    name: 'Atemwegsinfektion',
    englishName: 'Respiratory Infection',
    category: 'infectious',
    severity: 'medium',
    description: 'Infektion der oberen oder unteren Atemwege',
    symptoms: ['Nasenausfluss', 'Niesen', 'Atemnot', 'reduzierte Aktivität'],
    treatment: 'Antibiotika, Schleimlöser, Inhalationen',
    affectedSpecies: ['dog', 'cat', 'rabbit', 'guinea_pig', 'bird', 'ferret', 'chinchilla']
  },
  {
    id: 'mastitis',
    name: 'Mastitis',
    englishName: 'Mastitis',
    category: 'infectious',
    severity: 'medium',
    description: 'Entzündung der Milchdrüse',
    symptoms: ['Schwellung des Euters', 'Schmerzen', 'Fieber', 'veränderte Milch'],
    treatment: 'Antibiotika, entzündungshemmende Medikamente, Melkhygiene',
    affectedSpecies: ['cow', 'goat', 'sheep', 'pig']
  },
  {
    id: 'colic',
    name: 'Kolik',
    englishName: 'Colic',
    category: 'emergency',
    severity: 'high',
    description: 'Bauchschmerzen verschiedener Ursachen',
    symptoms: ['Unruhe', 'Wälzen', 'Schwitzen', 'fehlende Darmgeräusche'],
    treatment: 'Schmerzmittel, ggf. chirurgische Intervention',
    affectedSpecies: ['horse']
  },
  {
    id: 'laminitis',
    name: 'Hufrehe',
    englishName: 'Laminitis',
    category: 'chronic',
    severity: 'high',
    description: 'Entzündung der Huflederhaut',
    symptoms: ['Lahmheit', 'warme Hufe', 'Pulsation', 'charakteristische Stellung'],
    treatment: 'Schmerztherapie, Hufpflege, Diätmanagement',
    affectedSpecies: ['horse']
  }
];

// Utility functions for the game
export const getAnimalById = (id) => {
  return ANIMAL_SPECIES.find(animal => animal.id === id);
};

export const getConditionById = (id) => {
  return MEDICAL_CONDITIONS.find(condition => condition.id === id);
};

export const getCommonDiseasesForAnimal = (animalId) => {
  const animal = getAnimalById(animalId);
  if (!animal) return [];
  
  return animal.commonDiseases.map(diseaseName => {
    return MEDICAL_CONDITIONS.find(condition => 
      condition.name === diseaseName || condition.englishName === diseaseName
    );
  }).filter(Boolean);
};

export const getConditionsByCategory = (category) => {
  return MEDICAL_CONDITIONS.filter(condition => condition.category === category);
};

export const getConditionsBySeverity = (severity) => {
  return MEDICAL_CONDITIONS.filter(condition => condition.severity === severity);
};

export const getVitalSignsForAnimal = (animalId) => {
  const animal = getAnimalById(animalId);
  return animal ? animal.vitalSigns : null;
};

export const isVitalSignNormal = (animalId, parameter, value) => {
  const vitalSigns = getVitalSignsForAnimal(animalId);
  if (!vitalSigns || !vitalSigns[parameter]) return false;
  
  const range = vitalSigns[parameter];
  return value >= range.min && value <= range.max;
};

// Emergency severity levels for triage
export const SEVERITY_LEVELS = {
  critical: { color: '#FF0000', priority: 1, label: 'Kritisch' },
  high: { color: '#FF6600', priority: 2, label: 'Hoch' },
  medium: { color: '#FFAA00', priority: 3, label: 'Mittel' },
  low: { color: '#00AA00', priority: 4, label: 'Niedrig' }
};

// Categories for organization
export const CONDITION_CATEGORIES = {
  emergency: 'Notfall',
  chronic: 'Chronisch',
  infectious: 'Infektiös',
  parasitic: 'Parasitär',
  genetic: 'Genetisch',
  age_related: 'Altersbedingt'
};

export const ANIMAL_CATEGORIES = {
  pet: 'Haustiere',
  farm: 'Nutztiere',
  exotic: 'Exotische Tiere'
};