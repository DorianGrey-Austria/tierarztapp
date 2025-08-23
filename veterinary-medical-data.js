// Comprehensive Veterinary Medical Data for Scanner Simulation Game
// Data compiled from veterinary medical sources with German terminology where appropriate
// 20 Animals System: 100 Patients (60 Level 1, 40 Level 2)

export const ANIMAL_SPECIES = [
  // LEVEL 1 (6-10 Years) - 10 Basic Pets
  {
    id: 'dog',
    name: 'Hund',
    englishName: 'Dog',
    category: 'pet',
    difficulty: 'beginner',
    ageGroup: '6-10',
    model3D: {
      baseTemplate: 'quadruped_medium.blend',
      anatomyPoints: {
        heart: { x: 0.3, y: 0.6, z: 0.5 },
        lungs: { x: 0.35, y: 0.65, z: 0.5 },
        stomach: { x: 0.5, y: 0.4, z: 0.5 },
        liver: { x: 0.45, y: 0.45, z: 0.5 }
      },
      colorVariations: ['brown', 'black', 'white', 'spotted', 'golden'],
      sizeVariations: ['small', 'medium', 'large']
    },
    patientProfiles: [
      { name: 'Bello', age: 3, breed: 'Labrador', personality: 'friendly', size: 'large' },
      { name: 'Luna', age: 7, breed: 'Schäferhund', personality: 'nervous', size: 'large' },
      { name: 'Max', age: 1, breed: 'Mischling', personality: 'playful', size: 'medium' },
      { name: 'Bella', age: 10, breed: 'Golden Retriever', personality: 'calm', size: 'large' },
      { name: 'Charlie', age: 5, breed: 'Beagle', personality: 'curious', size: 'medium' }
    ],
    symptomSets: [
      {
        id: 'respiratory',
        symptoms: ['Husten', 'Schnelle Atmung', 'Nasenausfluss'],
        vitalChanges: { heartRate: 120, temperature: 39.0, respiratoryRate: 35 },
        diagnosis: 'Atemwegsinfektion',
        treatment: 'Antibiotika und Ruhe'
      },
      {
        id: 'digestive',
        symptoms: ['Erbrechen', 'Durchfall', 'Appetitlosigkeit'],
        vitalChanges: { heartRate: 90, temperature: 38.5, bloodGlucose: 70 },
        diagnosis: 'Magen-Darm-Störung',
        treatment: 'Schonkost und Flüssigkeitsersatz'
      },
      {
        id: 'trauma',
        symptoms: ['Lahmheit', 'Schwellung', 'Schmerzen beim Berühren'],
        vitalChanges: { heartRate: 130, temperature: 38.8 },
        diagnosis: 'Verletzung am Bein',
        treatment: 'Röntgen und Schmerzmittel'
      },
      {
        id: 'skin_condition',
        symptoms: ['Juckreiz', 'Hautrötung', 'Haarausfall'],
        vitalChanges: { heartRate: 80, temperature: 38.2 },
        diagnosis: 'Hautentzündung',
        treatment: 'Medizinisches Shampoo'
      },
      {
        id: 'ear_infection',
        symptoms: ['Kopfschütteln', 'Ohrengeruch', 'Kratzen am Ohr'],
        vitalChanges: { heartRate: 95, temperature: 38.7 },
        diagnosis: 'Ohrenentzündung',
        treatment: 'Ohrentropfen und Reinigung'
      }
    ],
    education: {
      funFacts: [
        'Hunde können 10.000 mal besser riechen als Menschen',
        'Ein Hundeherz schlägt 70-120 mal pro Minute',
        'Hunde schwitzen nur über ihre Pfoten',
        'Sie haben 42 Zähne (Menschen haben 32)',
        'Hunde träumen genauso wie Menschen'
      ],
      comparisons: [
        'Hundenase ist wie ein Super-Detektor',
        'Herzschlag so schnell wie Joggen beim Menschen',
        'Körpertemperatur wie leichtes Fieber'
      ],
      memoryTricks: [
        'H.U.N.D = Herz, Urin, Nase, Darm prüfen',
        'WUFF = Wärme, Urin, Fell, Fresslust checken'
      ]
    },
    vitalSigns: {
      heartRate: { min: 60, max: 180, unit: 'BPM' },
      temperature: { min: 37.5, max: 39.2, unit: '°C' },
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
    difficulty: 'beginner',
    ageGroup: '6-10',
    model3D: {
      baseTemplate: 'quadruped_medium.blend',
      anatomyPoints: {
        heart: { x: 0.32, y: 0.62, z: 0.5 },
        lungs: { x: 0.37, y: 0.67, z: 0.5 },
        stomach: { x: 0.52, y: 0.42, z: 0.5 },
        liver: { x: 0.47, y: 0.47, z: 0.5 }
      },
      colorVariations: ['orange', 'black', 'white', 'tabby', 'grey'],
      sizeVariations: ['small', 'medium']
    },
    patientProfiles: [
      { name: 'Mimi', age: 2, breed: 'Hauskatze', personality: 'shy', size: 'small' },
      { name: 'Felix', age: 6, breed: 'Maine Coon', personality: 'friendly', size: 'medium' },
      { name: 'Whiskers', age: 4, breed: 'Perser', personality: 'calm', size: 'medium' },
      { name: 'Shadow', age: 8, breed: 'Britisch Kurzhaar', personality: 'independent', size: 'medium' },
      { name: 'Mittens', age: 1, breed: 'Siamese', personality: 'playful', size: 'small' }
    ],
    symptomSets: [
      {
        id: 'respiratory',
        symptoms: ['Niesen', 'Verstopfte Nase', 'Augenausfluss'],
        vitalChanges: { heartRate: 130, temperature: 39.2, respiratoryRate: 35 },
        diagnosis: 'Katzenschnupfen',
        treatment: 'Antibiotika und Dampfbad'
      },
      {
        id: 'urinary',
        symptoms: ['Häufiges Urinieren', 'Schmerzen beim Wasserlassen', 'Blut im Urin'],
        vitalChanges: { heartRate: 140, temperature: 38.9 },
        diagnosis: 'Harnwegsinfektion',
        treatment: 'Antibiotika und viel Wasser'
      },
      {
        id: 'dental',
        symptoms: ['Mundgeruch', 'Zahnfleischentzündung', 'Schwierigkeiten beim Fressen'],
        vitalChanges: { heartRate: 110, temperature: 38.5 },
        diagnosis: 'Zahnprobleme',
        treatment: 'Zahnreinigung beim Tierarzt'
      },
      {
        id: 'digestive',
        symptoms: ['Erbrechen', 'Haarballen', 'Verstopfung'],
        vitalChanges: { heartRate: 95, temperature: 38.0 },
        diagnosis: 'Verdauungsstörung',
        treatment: 'Malzpaste und Ballaststoffe'
      },
      {
        id: 'skin_parasite',
        symptoms: ['Kratzen', 'Kleine schwarze Punkte im Fell', 'Unruhe'],
        vitalChanges: { heartRate: 125, temperature: 38.3 },
        diagnosis: 'Flohbefall',
        treatment: 'Antiparasitikum und Umgebungsbehandlung'
      }
    ],
    education: {
      funFacts: [
        'Katzen können 32 Muskeln in jedem Ohr bewegen',
        'Ein Katzenherz schlägt doppelt so schnell wie ein Menschenherz',
        'Katzen haben einen Geruchssinn der 14x stärker ist als bei Menschen',
        'Sie können bis zu 20 Stunden am Tag schlafen',
        'Katzen haben 230 Knochen (Menschen haben 206)'
      ],
      comparisons: [
        'Katzenaugen leuchten wie kleine Scheinwerfer',
        'Herzschlag wie ein schnelles Trommeln',
        'Körpertemperatur etwas wärmer als Menschen'
      ],
      memoryTricks: [
        'K.A.T.Z.E = Kopf, Augen, Temperatur, Zähne, Energie prüfen',
        'MIAU = Mund, Innenohr, Augen, Urin checken'
      ]
    },
    vitalSigns: {
      heartRate: { min: 100, max: 140, unit: 'BPM' },
      temperature: { min: 37.8, max: 39.4, unit: '°C' },
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
    id: 'mouse',
    name: 'Maus',
    englishName: 'Mouse',
    category: 'pet',
    difficulty: 'beginner',
    ageGroup: '6-10',
    model3D: {
      baseTemplate: 'quadruped_small.blend',
      anatomyPoints: {
        heart: { x: 0.35, y: 0.65, z: 0.5 },
        lungs: { x: 0.4, y: 0.7, z: 0.5 },
        stomach: { x: 0.55, y: 0.45, z: 0.5 },
        liver: { x: 0.5, y: 0.5, z: 0.5 }
      },
      colorVariations: ['white', 'brown', 'black', 'spotted', 'grey'],
      sizeVariations: ['tiny']
    },
    patientProfiles: [
      { name: 'Pip', age: 1, breed: 'Farbmaus', personality: 'curious', size: 'tiny' },
      { name: 'Squeaky', age: 2, breed: 'Farbmaus', personality: 'shy', size: 'tiny' },
      { name: 'Nibbles', age: 1, breed: 'Farbmaus', personality: 'playful', size: 'tiny' },
      { name: 'Whisper', age: 2, breed: 'Farbmaus', personality: 'calm', size: 'tiny' },
      { name: 'Zippy', age: 1, breed: 'Farbmaus', personality: 'active', size: 'tiny' }
    ],
    symptomSets: [
      {
        id: 'respiratory',
        symptoms: ['Schnelle Atmung', 'Pfeifende Geräusche', 'Weniger aktiv'],
        vitalChanges: { heartRate: 650, temperature: 36.5, respiratoryRate: 180 },
        diagnosis: 'Atemwegsproblem',
        treatment: 'Warme, feuchte Luft und Ruhe'
      },
      {
        id: 'digestive',
        symptoms: ['Weicher Kot', 'Weniger Fressen', 'Aufgeblähter Bauch'],
        vitalChanges: { heartRate: 550, temperature: 35.5 },
        diagnosis: 'Verdauungsstörung',
        treatment: 'Schonkost und probiotische Mittel'
      },
      {
        id: 'skin_condition',
        symptoms: ['Kratzen', 'Rötliche Haut', 'Haarausfall'],
        vitalChanges: { heartRate: 600, temperature: 36.2 },
        diagnosis: 'Hautentzündung',
        treatment: 'Spezialshampoo und Salbe'
      },
      {
        id: 'trauma',
        symptoms: ['Lahmes Bein', 'Schmerzen beim Berühren', 'Weniger bewegen'],
        vitalChanges: { heartRate: 700, temperature: 36.8 },
        diagnosis: 'Verletzung',
        treatment: 'Schmerzmittel und Käfigrest'
      },
      {
        id: 'parasites',
        symptoms: ['Juckreiz', 'Kleine bewegende Punkte', 'Unruhe'],
        vitalChanges: { heartRate: 650, temperature: 36.0 },
        diagnosis: 'Milbenbefall',
        treatment: 'Antiparasitikum'
      }
    ],
    education: {
      funFacts: [
        'Mäuseherzen schlagen bis zu 700 mal pro Minute',
        'Mäuse haben eine Körpertemperatur von 36-37°C',
        'Sie können durch Löcher kriechen, die nur halb so groß sind wie sie',
        'Mäuse haben einen ausgezeichneten Tastsinn durch ihre Schnurrhaare',
        'Sie leben nur 1-3 Jahre'
      ],
      comparisons: [
        'Mäuseherz schlägt so schnell wie ein Kolibri',
        'Körpertemperatur etwas kühler als Menschen',
        'So klein wie ein Daumen'
      ],
      memoryTricks: [
        'M.A.U.S = Mini, Aktiv, Unruhig, Schnell prüfen',
        'PIEP = Puls, Innenohr, Energie, Pfoten checken'
      ]
    },
    vitalSigns: {
      heartRate: { min: 500, max: 700, unit: 'BPM' },
      temperature: { min: 36.0, max: 37.0, unit: '°C' },
      respiratoryRate: { min: 100, max: 200, unit: '/min' },
      bloodPressure: { systolic: { min: 70, max: 110 }, diastolic: { min: 40, max: 70 }, unit: 'mmHg' },
      bloodGlucose: { min: 60, max: 140, unit: 'mg/dL' },
      oxygenSaturation: { min: 95, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Atemwegsinfektionen',
      'Milbenbefall',
      'Durchfall',
      'Tumore',
      'Augenentzündungen',
      'Verletzungen',
      'Salmonellose',
      'Hautprobleme',
      'Verdauungsstörungen',
      'Parasitenbefall'
    ]
  },
  {
    id: 'goldfish',
    name: 'Goldfisch',
    englishName: 'Goldfish',
    category: 'pet',
    difficulty: 'beginner',
    ageGroup: '6-10',
    model3D: {
      baseTemplate: 'aquatic_base.blend',
      anatomyPoints: {
        gills: { x: 0.25, y: 0.7, z: 0.5 },
        swim_bladder: { x: 0.5, y: 0.6, z: 0.5 },
        fins: { x: 0.7, y: 0.5, z: 0.5 },
        scales: { x: 0.5, y: 0.5, z: 0.5 }
      },
      colorVariations: ['orange', 'gold', 'white', 'red', 'calico'],
      sizeVariations: ['small', 'medium', 'large']
    },
    patientProfiles: [
      { name: 'Goldie', age: 2, breed: 'Gemeiner Goldfisch', personality: 'calm', size: 'medium' },
      { name: 'Bubbles', age: 1, breed: 'Fantail', personality: 'active', size: 'small' },
      { name: 'Nemo', age: 3, breed: 'Oranda', personality: 'friendly', size: 'large' },
      { name: 'Shimmer', age: 2, breed: 'Ryukin', personality: 'shy', size: 'medium' },
      { name: 'Flash', age: 1, breed: 'Gemeiner Goldfisch', personality: 'energetic', size: 'small' }
    ],
    symptomSets: [
      {
        id: 'swim_bladder',
        symptoms: ['Schwimmt seitlich', 'Kann nicht tauchen', 'Treibt an Oberfläche'],
        vitalChanges: { heartRate: 60, temperature: 15.0 },
        diagnosis: 'Schwimmblasenproblem',
        treatment: 'Fasten und warmes Wasser'
      },
      {
        id: 'fin_rot',
        symptoms: ['Ausgefranste Flossen', 'Rötliche Ränder', 'Träge Bewegungen'],
        vitalChanges: { heartRate: 45, temperature: 16.5 },
        diagnosis: 'Flossenfäule',
        treatment: 'Wasserwechsel und Medikamente'
      },
      {
        id: 'ich',
        symptoms: ['Weiße Punkte auf Körper', 'Scheuert sich an Gegenständen', 'Schnelle Atmung'],
        vitalChanges: { heartRate: 70, temperature: 17.0 },
        diagnosis: 'Pünktchenkrankheit',
        treatment: 'Temperatur erhöhen und Salzbad'
      },
      {
        id: 'fungus',
        symptoms: ['Weiße watteartige Beläge', 'Trübe Augen', 'Appetitlosigkeit'],
        vitalChanges: { heartRate: 40, temperature: 15.5 },
        diagnosis: 'Pilzinfektion',
        treatment: 'Antimykotische Behandlung'
      },
      {
        id: 'poor_water',
        symptoms: ['Schnelle Atmung', 'Hängt an Oberfläche', 'Blasse Kiemen'],
        vitalChanges: { heartRate: 80, temperature: 18.0 },
        diagnosis: 'Schlechte Wasserqualität',
        treatment: 'Sofortiger Wasserwechsel'
      }
    ],
    education: {
      funFacts: [
        'Goldfische können über 20 Jahre alt werden',
        'Sie haben ein Gedächtnis von mehreren Monaten, nicht nur 3 Sekunden',
        'Goldfische können Farben unterscheiden',
        'Sie haben keine Mägen - das Futter geht direkt in den Darm',
        'Goldfische können ohne Sauerstoffpumpe überleben'
      ],
      comparisons: [
        'Herzschlag so langsam wie ein ruhender Mensch',
        'Körpertemperatur passt sich der Wassertemperatur an',
        'Atmung durch Kiemen wie ein U-Boot mit Schnorchel'
      ],
      memoryTricks: [
        'F.I.S.C.H = Flossen, Ich-Krankheit, Schwimmblase, Chilodonella, Hautprobleme',
        'GLUB = Gills (Kiemen), Licht, Unterwasser, Bakterien prüfen'
      ]
    },
    vitalSigns: {
      heartRate: { min: 40, max: 80, unit: 'BPM' },
      temperature: { min: 15.0, max: 25.0, unit: '°C' },
      respiratoryRate: { min: 120, max: 180, unit: 'Kiemenbewegungen/min' },
      bloodPressure: { systolic: { min: 30, max: 60 }, diastolic: { min: 15, max: 35 }, unit: 'mmHg' },
      waterOxygen: { min: 5, max: 8, unit: 'ppm' },
      phLevel: { min: 6.5, max: 7.5, unit: 'pH' }
    },
    commonDiseases: [
      'Pünktchenkrankheit (Ich)',
      'Flossenfäule',
      'Schwimmblasenstörung',
      'Pilzinfektionen',
      'Bakterielle Infektionen',
      'Parasiten',
      'Sauerstoffmangel',
      'Vergiftung durch Wasserschadstoffe',
      'Verstopfung',
      'Augentrübung'
    ]
  },
  {
    id: 'turtle',
    name: 'Schildkröte',
    englishName: 'Turtle',
    category: 'pet',
    difficulty: 'beginner',
    ageGroup: '6-10',
    model3D: {
      baseTemplate: 'reptile_base.blend',
      anatomyPoints: {
        shell: { x: 0.5, y: 0.6, z: 0.5 },
        head: { x: 0.2, y: 0.7, z: 0.5 },
        legs: { x: 0.7, y: 0.3, z: 0.5 },
        tail: { x: 0.8, y: 0.5, z: 0.5 }
      },
      colorVariations: ['green', 'brown', 'yellow', 'olive', 'dark_green'],
      sizeVariations: ['small', 'medium', 'large']
    },
    patientProfiles: [
      { name: 'Shelly', age: 5, breed: 'Rotwangen-Schmuckschildkröte', personality: 'calm', size: 'medium' },
      { name: 'Speedy', age: 3, breed: 'Russische Landschildkröte', personality: 'active', size: 'small' },
      { name: 'Tank', age: 10, breed: 'Griechische Landschildkröte', personality: 'wise', size: 'large' },
      { name: 'Zippy', age: 2, breed: 'Moschusschildkröte', personality: 'shy', size: 'small' },
      { name: 'Caesar', age: 8, breed: 'Gelbwangen-Schmuckschildkröte', personality: 'proud', size: 'large' }
    ],
    symptomSets: [
      {
        id: 'shell_rot',
        symptoms: ['Weiche Stellen am Panzer', 'Übel riechender Panzer', 'Verfärbungen'],
        vitalChanges: { heartRate: 15, temperature: 22.0 },
        diagnosis: 'Panzerfäule',
        treatment: 'Desinfektion und Trockenlegung'
      },
      {
        id: 'respiratory',
        symptoms: ['Maulatmung', 'Pfeifende Geräusche', 'Schleimige Nase'],
        vitalChanges: { heartRate: 25, temperature: 24.0 },
        diagnosis: 'Atemwegsinfektion',
        treatment: 'Wärme und Antibiotika'
      },
      {
        id: 'vitamin_deficiency',
        symptoms: ['Weicher Panzer', 'Schwache Beine', 'Appetitlosigkeit'],
        vitalChanges: { heartRate: 12, temperature: 20.0 },
        diagnosis: 'Vitamin D3-Mangel',
        treatment: 'UV-Licht und Vitamine'
      },
      {
        id: 'parasites',
        symptoms: ['Dünner Kot', 'Gewichtsverlust', 'Lethargie'],
        vitalChanges: { heartRate: 18, temperature: 21.5 },
        diagnosis: 'Parasitenbefall',
        treatment: 'Antiparasitäre Medikamente'
      },
      {
        id: 'eye_infection',
        symptoms: ['Geschwollene Augen', 'Augen zu', 'Weiße Beläge'],
        vitalChanges: { heartRate: 20, temperature: 23.0 },
        diagnosis: 'Augenentzündung',
        treatment: 'Augentropfen und Wärme'
      }
    ],
    education: {
      funFacts: [
        'Schildkröten können über 100 Jahre alt werden',
        'Ihr Herz schlägt nur 10-25 mal pro Minute',
        'Sie können ihren Kopf in den Panzer zurückziehen',
        'Schildkröten gibt es seit 200 Millionen Jahren',
        'Sie haben keinen Zahnersatz, aber scharfe Kieferränder'
      ],
      comparisons: [
        'Herzschlag so langsam wie ein schlafender Mensch',
        'Panzer härter als Fingernägel',
        'Lebensdauer wie ein alter Baum'
      ],
      memoryTricks: [
        'S.C.H.I.L.D = Sonne, Calcium, Hitze, Infektion, Licht, Darm prüfen',
        'TURTLE = Temperatur, UV-Licht, Ruhe, Trichomonaden, Leber, Eier'
      ]
    },
    vitalSigns: {
      heartRate: { min: 10, max: 25, unit: 'BPM' },
      temperature: { min: 20.0, max: 30.0, unit: '°C' },
      respiratoryRate: { min: 3, max: 15, unit: '/min' },
      bloodPressure: { systolic: { min: 40, max: 80 }, diastolic: { min: 20, max: 50 }, unit: 'mmHg' },
      bloodGlucose: { min: 50, max: 150, unit: 'mg/dL' },
      oxygenSaturation: { min: 85, max: 100, unit: '%' }
    },
    commonDiseases: [
      'Panzerfäule',
      'Atemwegsinfektionen',
      'Vitamin A-Mangel',
      'Vitamin D3-Mangel',
      'Parasiten',
      'Augenentzündungen',
      'Legenot',
      'Verstopfung',
      'Nierenprobleme',
      'Salmonellose'
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

// 20-Animals System: Patient Generator
export const PATIENT_DISTRIBUTION = {
  level1: 60, // 60 patients from easy animals (6 per animal)
  level2: 40  // 40 patients from complex animals (4 per animal)
};

// Generate 100 individual patients from 20 animal types
export const generatePatients = () => {
  const patients = [];
  const level1Animals = ANIMAL_SPECIES.filter(a => a.ageGroup === '6-10');
  const level2Animals = ANIMAL_SPECIES.filter(a => a.ageGroup === '10-14');
  
  // Generate 60 patients from Level 1 animals (6 per animal type)
  level1Animals.slice(0, 10).forEach((animal, animalIndex) => {
    for (let i = 0; i < 6; i++) {
      const profile = animal.patientProfiles[i % 5];
      const symptomSet = animal.symptomSets[i % 5];
      
      patients.push({
        id: `level1_${animalIndex}_${i}`,
        patientNumber: patients.length + 1,
        animalType: animal.id,
        animalName: animal.name,
        difficulty: 'beginner',
        ageGroup: '6-10',
        ...profile,
        symptoms: symptomSet.symptoms,
        vitalChanges: symptomSet.vitalChanges,
        correctDiagnosis: symptomSet.diagnosis,
        treatment: symptomSet.treatment,
        model3D: animal.model3D,
        education: animal.education,
        level: 1
      });
    }
  });
  
  // Generate 40 patients from Level 2 animals (4 per animal type)
  level2Animals.slice(0, 10).forEach((animal, animalIndex) => {
    for (let i = 0; i < 4; i++) {
      const profile = animal.patientProfiles[i % 5];
      const symptomSet = animal.symptomSets[i % 5];
      
      patients.push({
        id: `level2_${animalIndex}_${i}`,
        patientNumber: patients.length + 1,
        animalType: animal.id,
        animalName: animal.name,
        difficulty: 'advanced',
        ageGroup: '10-14',
        ...profile,
        symptoms: symptomSet.symptoms,
        vitalChanges: symptomSet.vitalChanges,
        correctDiagnosis: symptomSet.diagnosis,
        treatment: symptomSet.treatment,
        model3D: animal.model3D,
        education: animal.education,
        level: 2
      });
    }
  });
  
  // Shuffle patients for random order
  return patients.sort(() => Math.random() - 0.5);
};

// Get patient by ID
export const getPatientById = (id) => {
  const allPatients = generatePatients();
  return allPatients.find(patient => patient.id === id);
};

// Get patients by difficulty level
export const getPatientsByLevel = (level) => {
  const allPatients = generatePatients();
  return allPatients.filter(patient => patient.level === level);
};

// Get random patient by age group
export const getRandomPatientByAgeGroup = (ageGroup) => {
  const allPatients = generatePatients();
  const filteredPatients = allPatients.filter(patient => patient.ageGroup === ageGroup);
  const randomIndex = Math.floor(Math.random() * filteredPatients.length);
  return filteredPatients[randomIndex];
};

// Get patients by animal type
export const getPatientsByAnimal = (animalId) => {
  const allPatients = generatePatients();
  return allPatients.filter(patient => patient.animalType === animalId);
};

// Statistics for the 20-animals system
export const getSystemStats = () => {
  const allPatients = generatePatients();
  const level1Count = allPatients.filter(p => p.level === 1).length;
  const level2Count = allPatients.filter(p => p.level === 2).length;
  
  const animalTypes = [...new Set(allPatients.map(p => p.animalType))];
  const animalCounts = {};
  animalTypes.forEach(type => {
    animalCounts[type] = allPatients.filter(p => p.animalType === type).length;
  });
  
  return {
    totalPatients: allPatients.length,
    level1Patients: level1Count,
    level2Patients: level2Count,
    animalTypes: animalTypes.length,
    animalDistribution: animalCounts,
    averagePatientsPerAnimal: Math.round(allPatients.length / animalTypes.length)
  };
};