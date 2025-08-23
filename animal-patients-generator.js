// 20-Animals Patient Generator for VetScan Detective
// Generates 100 individual patients from 20 animal types

const ANIMAL_EMOJIS = {
    dog: '🐕', cat: '🐱', mouse: '🐭', goldfish: '🐠', turtle: '🐢',
    rabbit: '🐰', guinea_pig: '🐹', hamster: '🐹', budgie: '🦜', canary: '🐦',
    ferret: '🦫', hedgehog: '🦔', chinchilla: '🐨', rat: '🐀', degu: '🐿️',
    bearded_dragon: '🦎', snake: '🐍', axolotl: '🦎', parrot: '🦜', iguana: '🦎'
};

// Level 1 Animals (6-10 years) - Simple cases
const LEVEL1_ANIMALS = [
    {
        id: 'dog',
        name: 'Hund',
        emoji: '🐕',
        patients: [
            { name: 'Bello', age: 3, breed: 'Labrador', personality: 'friendly' },
            { name: 'Luna', age: 7, breed: 'Schäferhund', personality: 'nervous' },
            { name: 'Max', age: 1, breed: 'Mischling', personality: 'playful' },
            { name: 'Bella', age: 10, breed: 'Golden Retriever', personality: 'calm' },
            { name: 'Charlie', age: 5, breed: 'Beagle', personality: 'curious' }
        ],
        conditions: [
            {
                condition: 'Atemwegsinfektion',
                timeline: ['Vor 2 Tagen: Husten begonnen', 'Gestern: Nasenausfluss', 'Heute: Schnellere Atmung'],
                symptoms: {
                    head: { finding: 'Nasenausfluss, leichte Schwellung', visual: 'problem' },
                    chest: { finding: 'Schnelle Atmung, leichtes Rasseln', visual: 'problem' },
                    belly: { finding: 'Normal weich', visual: 'normal' },
                    legs: { finding: 'Normale Bewegung', visual: 'normal' }
                },
                measurements: {
                    heartRate: { value: 120, status: 'warning' },
                    temperature: { value: 39.2, status: 'problem' },
                    breathing: { value: 35, status: 'warning' }
                },
                diagnosis: {
                    correct: 'Atemwegsinfektion',
                    options: ['Atemwegsinfektion', 'Herzproblem', 'Allergie', 'Vergiftung']
                },
                hints: ['Achte auf Atmung und Nase', 'Temperatur ist erhöht', 'Häufig bei Welpen und älteren Hunden']
            },
            {
                condition: 'Magen-Darm-Störung',
                timeline: ['Gestern: Erbrechen nach dem Fressen', 'Heute früh: Durchfall', 'Jetzt: Will nicht fressen'],
                symptoms: {
                    head: { finding: 'Trockenes Zahnfleisch, müde Augen', visual: 'warning' },
                    chest: { finding: 'Herzschlag etwas schnell', visual: 'warning' },
                    belly: { finding: 'Gespannt, Schmerzen beim Berühren', visual: 'problem' },
                    legs: { finding: 'Schwächere Bewegungen', visual: 'warning' }
                },
                measurements: {
                    heartRate: { value: 100, status: 'normal' },
                    temperature: { value: 38.5, status: 'normal' },
                    breathing: { value: 25, status: 'normal' }
                },
                diagnosis: {
                    correct: 'Magen-Darm-Störung',
                    options: ['Magen-Darm-Störung', 'Vergiftung', 'Parasitenbefall', 'Futtermittelallergie']
                },
                hints: ['Bauch ist der Schlüssel', 'Dehydration prüfen', 'Was hat der Hund gefressen?']
            },
            {
                condition: 'Ohrenentzündung',
                timeline: ['Vor 3 Tagen: Kopfschütteln', 'Vor 1 Tag: Kratzen am Ohr', 'Heute: Geruch aus dem Ohr'],
                symptoms: {
                    head: { finding: 'Rotes, geschwollenes Ohr mit Geruch', visual: 'problem' },
                    chest: { finding: 'Normal', visual: 'normal' },
                    belly: { finding: 'Normal', visual: 'normal' },
                    legs: { finding: 'Normal, kratzt sich am Ohr', visual: 'normal' }
                },
                measurements: {
                    heartRate: { value: 90, status: 'normal' },
                    temperature: { value: 38.7, status: 'normal' },
                    breathing: { value: 20, status: 'normal' }
                },
                diagnosis: {
                    correct: 'Ohrenentzündung',
                    options: ['Ohrenentzündung', 'Milbenbefall', 'Allergie', 'Fremdkörper im Ohr']
                },
                hints: ['Das Ohr riecht ungewöhnlich', 'Hund schüttelt oft den Kopf', 'Häufig durch Feuchtigkeit']
            }
        ]
    },
    {
        id: 'cat',
        name: 'Katze',
        emoji: '🐱',
        patients: [
            { name: 'Mimi', age: 2, breed: 'Hauskatze', personality: 'shy' },
            { name: 'Felix', age: 6, breed: 'Maine Coon', personality: 'friendly' },
            { name: 'Whiskers', age: 4, breed: 'Perser', personality: 'calm' },
            { name: 'Shadow', age: 8, breed: 'Britisch Kurzhaar', personality: 'independent' },
            { name: 'Mittens', age: 1, breed: 'Siamese', personality: 'playful' }
        ],
        conditions: [
            {
                condition: 'Katzenschnupfen',
                timeline: ['Vor 4 Tagen: Erstes Niesen', 'Vor 2 Tagen: Augenausfluss', 'Heute: Verstopfte Nase'],
                symptoms: {
                    head: { finding: 'Niesen, wässriger Augenausfluss, verstopfte Nase', visual: 'problem' },
                    chest: { finding: 'Leicht beschleunigte Atmung', visual: 'warning' },
                    belly: { finding: 'Normal', visual: 'normal' },
                    legs: { finding: 'Etwas weniger aktiv', visual: 'warning' }
                },
                measurements: {
                    heartRate: { value: 150, status: 'warning' },
                    temperature: { value: 39.5, status: 'problem' },
                    breathing: { value: 35, status: 'warning' }
                },
                diagnosis: {
                    correct: 'Katzenschnupfen',
                    options: ['Katzenschnupfen', 'Allergie', 'Fremdkörper in der Nase', 'Zahnproblem']
                },
                hints: ['Typische Katzenkrankheit', 'Sehr ansteckend für andere Katzen', 'Betrifft Augen und Nase']
            },
            {
                condition: 'Harnwegsinfektion',
                timeline: ['Vor 2 Tagen: Öfter zur Katzentoilette', 'Gestern: Schmerzen beim Urinieren', 'Heute: Blut im Urin bemerkt'],
                symptoms: {
                    head: { finding: 'Normal', visual: 'normal' },
                    chest: { finding: 'Normal', visual: 'normal' },
                    belly: { finding: 'Unterbauch empfindlich, Blase ertastbar', visual: 'problem' },
                    legs: { finding: 'Unruhiges Verhalten', visual: 'warning' }
                },
                measurements: {
                    heartRate: { value: 160, status: 'warning' },
                    temperature: { value: 39.0, status: 'warning' },
                    breathing: { value: 30, status: 'normal' }
                },
                diagnosis: {
                    correct: 'Harnwegsinfektion',
                    options: ['Harnwegsinfektion', 'Blasensteine', 'Nierenprobleme', 'Verstopfung']
                },
                hints: ['Katze geht oft aufs Klo', 'Unterbauch ist schmerzhaft', 'Häufig bei Katzen die wenig trinken']
            }
        ]
    },
    {
        id: 'mouse',
        name: 'Maus',
        emoji: '🐭',
        patients: [
            { name: 'Pip', age: 1, breed: 'Farbmaus', personality: 'curious' },
            { name: 'Squeaky', age: 2, breed: 'Farbmaus', personality: 'shy' },
            { name: 'Nibbles', age: 1, breed: 'Farbmaus', personality: 'playful' },
            { name: 'Whisper', age: 2, breed: 'Farbmaus', personality: 'calm' },
            { name: 'Zippy', age: 1, breed: 'Farbmaus', personality: 'active' }
        ],
        conditions: [
            {
                condition: 'Atemwegsproblem',
                timeline: ['Heute morgen: Schnellere Atmung bemerkt', 'Mittags: Pfeifende Geräusche', 'Jetzt: Weniger aktiv als sonst'],
                symptoms: {
                    head: { finding: 'Schnelle, pfeifende Atmung durch Nase', visual: 'problem' },
                    chest: { finding: 'Sehr schneller Herzschlag, Rasseln', visual: 'problem' },
                    belly: { finding: 'Normal, aber Atmung sichtbar anstrengend', visual: 'warning' },
                    legs: { finding: 'Schwächere Bewegungen, weniger Sprünge', visual: 'warning' }
                },
                measurements: {
                    heartRate: { value: 650, status: 'warning' },
                    temperature: { value: 36.5, status: 'normal' },
                    breathing: { value: 180, status: 'problem' }
                },
                diagnosis: {
                    correct: 'Atemwegsinfektion',
                    options: ['Atemwegsinfektion', 'Stress', 'Herzproblem', 'Allergie gegen Einstreu']
                },
                hints: ['Mäuse atmen normalerweise sehr schnell', 'Pfeifende Geräusche sind nicht normal', 'Kleine Tiere werden schnell schwach']
            }
        ]
    },
    {
        id: 'goldfish',
        name: 'Goldfisch',
        emoji: '🐠',
        patients: [
            { name: 'Goldie', age: 2, breed: 'Gemeiner Goldfisch', personality: 'calm' },
            { name: 'Bubbles', age: 1, breed: 'Fantail', personality: 'active' },
            { name: 'Nemo', age: 3, breed: 'Oranda', personality: 'friendly' },
            { name: 'Shimmer', age: 2, breed: 'Ryukin', personality: 'shy' },
            { name: 'Flash', age: 1, breed: 'Gemeiner Goldfisch', personality: 'energetic' }
        ],
        conditions: [
            {
                condition: 'Schwimmblasenproblem',
                timeline: ['Vor 3 Tagen: Schwimmt schief', 'Vor 1 Tag: Kann nicht richtig tauchen', 'Heute: Treibt an der Oberfläche'],
                symptoms: {
                    head: { finding: 'Augen normal, aber Atmung schneller', visual: 'warning' },
                    chest: { finding: 'Normal, aber Balance gestört', visual: 'problem' },
                    belly: { finding: 'Aufgebläht, schwimmt seitlich', visual: 'problem' },
                    legs: { finding: 'Flossen arbeiten normal', visual: 'normal' }
                },
                measurements: {
                    heartRate: { value: 60, status: 'normal' },
                    temperature: { value: 18.0, status: 'normal' },
                    breathing: { value: 150, status: 'warning' }
                },
                diagnosis: {
                    correct: 'Schwimmblasenproblem',
                    options: ['Schwimmblasenproblem', 'Verstopfung', 'Parasitenbefall', 'Wasserqualitätsproblem']
                },
                hints: ['Fisch kann seine Position im Wasser nicht kontrollieren', 'Oft durch Überfütterung', 'Schwimmblase reguliert Auftrieb']
            }
        ]
    },
    {
        id: 'turtle',
        name: 'Schildkröte',
        emoji: '🐢',
        patients: [
            { name: 'Shelly', age: 5, breed: 'Rotwangen-Schmuckschildkröte', personality: 'calm' },
            { name: 'Speedy', age: 3, breed: 'Russische Landschildkröte', personality: 'active' },
            { name: 'Tank', age: 10, breed: 'Griechische Landschildkröte', personality: 'wise' },
            { name: 'Zippy', age: 2, breed: 'Moschusschildkröte', personality: 'shy' },
            { name: 'Caesar', age: 8, breed: 'Gelbwangen-Schmuckschildkröte', personality: 'proud' }
        ],
        conditions: [
            {
                condition: 'Panzerfäule',
                timeline: ['Vor 1 Woche: Kleine weiche Stelle am Panzer', 'Vor 3 Tagen: Stelle wird größer', 'Heute: Panzer riecht schlecht'],
                symptoms: {
                    head: { finding: 'Normal', visual: 'normal' },
                    chest: { finding: 'Panzer hat weiche, stinkende Stellen', visual: 'problem' },
                    belly: { finding: 'Unterer Panzer auch betroffen', visual: 'problem' },
                    legs: { finding: 'Normale Bewegung, aber weniger aktiv', visual: 'warning' }
                },
                measurements: {
                    heartRate: { value: 15, status: 'normal' },
                    temperature: { value: 25.0, status: 'normal' },
                    breathing: { value: 8, status: 'normal' }
                },
                diagnosis: {
                    correct: 'Panzerfäule',
                    options: ['Panzerfäule', 'Verletzung', 'Pilzinfektion', 'Vitamin-Mangel']
                },
                hints: ['Panzer ist normalerweise hart', 'Schlechter Geruch deutet auf Bakterien hin', 'Oft durch zu viel Feuchtigkeit']
            }
        ]
    }
];

// Generate medical cases from animal data
function generate20AnimalCases() {
    const cases = [];
    
    LEVEL1_ANIMALS.forEach(animal => {
        // Generate 6 cases per animal (60 total for level 1)
        for (let i = 0; i < 6; i++) {
            const patient = animal.patients[i % 5]; // Cycle through patients
            const condition = animal.conditions[i % animal.conditions.length]; // Cycle through conditions
            
            const caseData = {
                id: `${animal.id}_patient${i}_condition${i % animal.conditions.length}`,
                animal: {
                    type: animal.name,
                    name: patient.name,
                    age: patient.age,
                    breed: patient.breed,
                    personality: patient.personality,
                    emoji: animal.emoji
                },
                condition: condition.condition,
                timeline: condition.timeline,
                symptoms: condition.symptoms,
                measurements: condition.measurements,
                diagnosis: condition.diagnosis,
                hints: condition.hints,
                difficulty: 'easy',
                animalId: animal.id,
                patientNumber: i + 1
            };
            
            cases.push(caseData);
        }
    });
    
    return cases;
}

// Educational facts about each animal
const ANIMAL_EDUCATION = {
    dog: {
        funFacts: [
            'Hunde können 10.000 mal besser riechen als Menschen',
            'Ein Hundeherz schlägt 70-120 mal pro Minute',
            'Hunde schwitzen nur über ihre Pfoten',
            'Sie haben 42 Zähne (Menschen haben 32)',
            'Hunde träumen genauso wie Menschen'
        ],
        memoryTricks: [
            'H.U.N.D = Herz, Urin, Nase, Darm prüfen',
            'WUFF = Wärme, Urin, Fell, Fresslust checken'
        ]
    },
    cat: {
        funFacts: [
            'Katzen können 32 Muskeln in jedem Ohr bewegen',
            'Ein Katzenherz schlägt doppelt so schnell wie ein Menschenherz',
            'Katzen haben einen Geruchssinn der 14x stärker ist als bei Menschen',
            'Sie können bis zu 20 Stunden am Tag schlafen',
            'Katzen haben 230 Knochen (Menschen haben 206)'
        ],
        memoryTricks: [
            'K.A.T.Z.E = Kopf, Augen, Temperatur, Zähne, Energie prüfen',
            'MIAU = Mund, Innenohr, Augen, Urin checken'
        ]
    },
    mouse: {
        funFacts: [
            'Mäuseherzen schlagen bis zu 700 mal pro Minute',
            'Mäuse haben eine Körpertemperatur von 36-37°C',
            'Sie können durch Löcher kriechen, die nur halb so groß sind wie sie',
            'Mäuse haben einen ausgezeichneten Tastsinn durch ihre Schnurrhaare',
            'Sie leben nur 1-3 Jahre'
        ],
        memoryTricks: [
            'M.A.U.S = Mini, Aktiv, Unruhig, Schnell prüfen',
            'PIEP = Puls, Innenohr, Energie, Pfoten checken'
        ]
    },
    goldfish: {
        funFacts: [
            'Goldfische können über 20 Jahre alt werden',
            'Sie haben ein Gedächtnis von mehreren Monaten, nicht nur 3 Sekunden',
            'Goldfische können Farben unterscheiden',
            'Sie haben keine Mägen - das Futter geht direkt in den Darm',
            'Goldfische können ohne Sauerstoffpumpe überleben'
        ],
        memoryTricks: [
            'F.I.S.C.H = Flossen, Ich-Krankheit, Schwimmblase, Chilodonella, Hautprobleme',
            'GLUB = Gills (Kiemen), Licht, Unterwasser, Bakterien prüfen'
        ]
    },
    turtle: {
        funFacts: [
            'Schildkröten können über 100 Jahre alt werden',
            'Ihr Herz schlägt nur 10-25 mal pro Minute',
            'Sie können ihren Kopf in den Panzer zurückziehen',
            'Schildkröten gibt es seit 200 Millionen Jahren',
            'Sie haben keinen Zahnersatz, aber scharfe Kieferränder'
        ],
        memoryTricks: [
            'S.C.H.I.L.D = Sonne, Calcium, Hitze, Infektion, Licht, Darm prüfen',
            'TURTLE = Temperatur, UV-Licht, Ruhe, Trichomonaden, Leber, Eier'
        ]
    }
};

// Get random educational fact
function getRandomEducationalFact() {
    const allFacts = [];
    Object.values(ANIMAL_EDUCATION).forEach(animal => {
        allFacts.push(...animal.funFacts);
    });
    return allFacts[Math.floor(Math.random() * allFacts.length)];
}

// Get educational info for specific animal
function getAnimalEducation(animalId) {
    return ANIMAL_EDUCATION[animalId] || null;
}

// Export for use in HTML files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        generate20AnimalCases,
        getRandomEducationalFact,
        getAnimalEducation,
        ANIMAL_EMOJIS,
        LEVEL1_ANIMALS
    };
}