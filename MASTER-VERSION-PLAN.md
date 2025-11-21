# 🚀 Master Version Plan - VetScan Pro Ultimate

**Datum:** 2024-11-21
**Ziel:** Zusammenführung der besten Features aller Versionen zu einer ultimativen Masterversion
**Basis:** React App + Beste Features aus Standalone-Versionen
**Zeitrahmen:** 4-6 Wochen Entwicklung

---

## 🎯 Vision: VetScan Pro Ultimate

**Elevator Pitch:**
> Eine pädagogische Veterinär-Scanner-Simulation, die durch Gamification, Story-Modus und AI-Assistenz Kinder (6-14 Jahre) spielerisch an die Veterinärmedizin heranführt und nachhaltiges Lernen durch wissenschaftlich fundierte Methoden ermöglicht.

**Zielgruppe:**
- 👶 **Primär:** Kinder 6-14 Jahre
- 👨‍👩‍👧 **Sekundär:** Eltern, Lehrkräfte
- 🎓 **Tertiär:** Veterinärmedizin-Interessierte

**USPs:**
1. 🎮 **Gamification** - Level, Achievements, Progression
2. 📖 **Story-Modus** - Narrative Karriere vom Praktikanten zum Cheftierarzt
3. 🤖 **AI-Assistent** - "Dr. Watson" hilft bei Fragen
4. 🔬 **Wissenschaftlich fundiert** - Echte Vitalparameter, echte Diagnosen
5. 🎨 **Moderne UI** - Mobile-First, Touch-optimiert
6. 🧠 **Pädagogisch wertvoll** - Bloom's Taxonomy, Spaced Repetition

---

## 📐 Architektur-Übersicht

```
VetScan Pro Ultimate
│
├── 🏗️ CORE (React App Basis)
│   ├── VetScanMaster.jsx              # Main Component
│   ├── veterinary-medical-data.js     # Medical Database
│   ├── GlobalStateManager.js          # Zustand/Redux
│   └── RouterConfig.jsx               # React Router
│
├── 🎮 GAMIFICATION LAYER
│   ├── LevelSystem/
│   │   ├── LevelManager.js
│   │   ├── ExperienceCalculator.js
│   │   └── ProgressTracker.jsx
│   ├── Achievements/
│   │   ├── AchievementSystem.js
│   │   ├── BadgeCollection.jsx
│   │   └── achievement-definitions.js
│   ├── DailyChallenges/
│   │   ├── ChallengeManager.js
│   │   └── ChallengeUI.jsx
│   └── Rewards/
│       ├── StarRating.jsx
│       └── VeterinaryPoints.js
│
├── 📖 STORY LAYER
│   ├── StoryMode/
│   │   ├── StoryManager.js
│   │   ├── ChapterSystem.js
│   │   └── chapters/
│   │       ├── chapter1-erste-schritte.js
│   │       ├── chapter2-notfall-nacht.js
│   │       ├── chapter3-exotische-patienten.js
│   │       └── chapter4-forscher.js
│   ├── Characters/
│   │   ├── DrWeber.js (Mentor)
│   │   ├── Patients.js
│   │   └── CharacterDialog.jsx
│   └── Narrative/
│       ├── DialogEngine.jsx
│       └── ChoiceSystem.js
│
├── 🤖 AI LAYER
│   ├── DrWatsonAssistant/
│   │   ├── ChatBot.jsx
│   │   ├── NLPProcessor.js
│   │   └── KnowledgeBase.js
│   ├── AutoDiagnosis/
│   │   ├── DiagnosisEngine.js
│   │   └── MLSimulator.js
│   └── SmartRecommendations/
│       ├── RecommendationEngine.js
│       └── ContextAnalyzer.js
│
├── 🏥 PROFESSIONAL TOOLS
│   ├── MedicalRecords/
│   │   ├── PatientHistory.jsx
│   │   └── RecordManager.js
│   ├── TreatmentPlans/
│   │   ├── TreatmentPlanner.jsx
│   │   └── MedicationDatabase.js
│   ├── EmergencyTriage/
│   │   ├── TriageSystem.jsx
│   │   └── PriorityManager.js
│   └── Reports/
│       ├── DiagnosisReport.jsx
│       └── PDFExporter.js
│
├── 🎨 UI COMPONENTS
│   ├── Layout/
│   │   ├── MainLayout.jsx
│   │   ├── Sidebar.jsx
│   │   └── TopBar.jsx
│   ├── Scanning/
│   │   ├── ScannerView.jsx
│   │   ├── VitalMonitor.jsx
│   │   └── ResultsView.jsx
│   ├── Animals/
│   │   ├── AnimalSelector.jsx
│   │   ├── AnimalCard.jsx
│   │   └── Model3DViewer.jsx
│   └── Common/
│       ├── Button.jsx
│       ├── Card.jsx
│       ├── Modal.jsx
│       └── Toast.jsx
│
├── 🧠 PEDAGOGY LAYER
│   ├── Tutorial/
│   │   ├── TutorialSystem.jsx
│   │   ├── InteractiveTour.js
│   │   └── HelpSystem.jsx
│   ├── Learning/
│   │   ├── SpacedRepetition.js
│   │   ├── BloomTaxonomy.js
│   │   └── AdaptiveLearning.js
│   └── Feedback/
│       ├── ImmediateFeedback.jsx
│       ├── ScaffoldingSystem.js
│       └── ProgressReports.jsx
│
└── 💾 DATA & SERVICES
    ├── Storage/
    │   ├── LocalStorageManager.js
    │   ├── IndexedDBHandler.js
    │   └── CloudSync.js (optional)
    ├── Analytics/
    │   ├── AnalyticsTracker.js
    │   └── LearningMetrics.js
    └── API/
        ├── APIClient.js (future)
        └── WebSocketManager.js (future)
```

---

## 🎮 Phase 1: Gamification System (Woche 1-2)

### 1.1 Level System

**Datei:** `src/gamification/LevelSystem/LevelManager.js`

```javascript
// Level Configuration
export const LEVEL_CONFIG = {
  maxLevel: 30,
  levelThresholds: {
    beginner: [1, 10],    // Levels 1-10
    intermediate: [11, 20], // Levels 11-20
    expert: [21, 30]       // Levels 21-30
  },
  xpRequirements: {
    // XP needed for each level
    1: 0,
    2: 100,
    3: 250,
    4: 450,
    5: 700,
    // ... exponential growth
    30: 50000
  }
};

export class LevelManager {
  constructor() {
    this.currentLevel = 1;
    this.currentXP = 0;
    this.totalXP = 0;
  }

  addExperience(xp, reason) {
    this.currentXP += xp;
    this.totalXP += xp;

    const leveledUp = this.checkLevelUp();

    return {
      xpGained: xp,
      newXP: this.currentXP,
      leveledUp,
      newLevel: leveledUp ? this.currentLevel : null,
      reason
    };
  }

  checkLevelUp() {
    const nextLevelXP = LEVEL_CONFIG.xpRequirements[this.currentLevel + 1];

    if (this.currentXP >= nextLevelXP && this.currentLevel < 30) {
      this.currentLevel++;
      this.currentXP -= nextLevelXP; // Carry over excess XP
      return true;
    }

    return false;
  }

  getProgress() {
    const currentLevelXP = LEVEL_CONFIG.xpRequirements[this.currentLevel];
    const nextLevelXP = LEVEL_CONFIG.xpRequirements[this.currentLevel + 1];
    const xpForThisLevel = nextLevelXP - currentLevelXP;
    const progress = (this.currentXP / xpForThisLevel) * 100;

    return {
      level: this.currentLevel,
      currentXP: this.currentXP,
      nextLevelXP,
      progress: Math.min(progress, 100),
      tier: this.getTier()
    };
  }

  getTier() {
    if (this.currentLevel <= 10) return 'beginner';
    if (this.currentLevel <= 20) return 'intermediate';
    return 'expert';
  }
}

// XP Rewards
export const XP_REWARDS = {
  correctDiagnosis: {
    easy: 50,
    medium: 100,
    hard: 200,
    expert: 350
  },
  firstTime: 50,           // Bonus for first time diagnosing
  perfectScore: 100,       // All vitals correct
  fastDiagnosis: 75,       // Under 2 minutes
  dailyChallenge: 150,     // Completing daily challenge
  achievement: 200,        // Unlocking achievement
  storylineComplete: 500   // Completing story chapter
};
```

**UI Component:** `src/gamification/LevelSystem/LevelProgressBar.jsx`

```jsx
import React from 'react';
import { Trophy, Star, Zap } from 'lucide-react';

export const LevelProgressBar = ({ level, xp, nextLevelXP, progress }) => {
  return (
    <div className="bg-gradient-to-r from-purple-900/50 to-blue-900/50 rounded-xl p-4 backdrop-blur-md">
      {/* Level Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="bg-yellow-500 text-white rounded-full w-12 h-12 flex items-center justify-center font-bold text-xl">
            {level}
          </div>
          <div>
            <div className="text-white font-bold">Level {level}</div>
            <div className="text-cyan-400 text-sm">
              {getTierName(level)}
            </div>
          </div>
        </div>

        <div className="text-right">
          <div className="text-cyan-400 text-sm">XP</div>
          <div className="text-white font-bold">
            {xp} / {nextLevelXP}
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="relative w-full h-4 bg-gray-800 rounded-full overflow-hidden">
        {/* Background glow */}
        <div
          className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-purple-500 opacity-20"
          style={{ width: `${progress}%` }}
        />

        {/* Actual progress */}
        <div
          className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-purple-500 transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        >
          {/* Animated shine effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30 animate-shine" />
        </div>

        {/* Progress text */}
        <div className="absolute inset-0 flex items-center justify-center text-xs font-bold text-white drop-shadow-lg">
          {progress.toFixed(0)}%
        </div>
      </div>

      {/* Next Milestone */}
      <div className="mt-2 text-xs text-gray-400 text-center">
        {getNextMilestone(level)}
      </div>
    </div>
  );
};

function getTierName(level) {
  if (level <= 10) return '🌱 Junior Veterinarian';
  if (level <= 20) return '⭐ Professional Vet';
  return '🏆 Master Veterinarian';
}

function getNextMilestone(level) {
  const milestones = {
    5: 'Unlock: Nutztiere',
    10: 'Unlock: Story Kapitel 2',
    15: 'Unlock: Exotische Tiere',
    20: 'Unlock: Story Kapitel 3',
    25: 'Unlock: Expertenf\u00e4lle',
    30: 'MAX LEVEL - Du bist ein Meister!'
  };

  const nextMilestone = Object.keys(milestones)
    .map(Number)
    .find(m => m > level);

  return milestones[nextMilestone] || 'Du hast alles freigeschaltet!';
}
```

### 1.2 Achievement System

**Datei:** `src/gamification/Achievements/achievement-definitions.js`

```javascript
export const ACHIEVEMENTS = {
  // Beginner Achievements
  first_diagnosis: {
    id: 'first_diagnosis',
    name: 'Erste Diagnose',
    description: 'Diagnostiziere dein erstes Tier',
    icon: '🎯',
    tier: 'bronze',
    xpReward: 100,
    condition: (stats) => stats.totalDiagnoses >= 1
  },

  perfect_scan: {
    id: 'perfect_scan',
    name: 'Perfekter Scan',
    description: 'Alle Vitalparameter korrekt identifiziert',
    icon: '💯',
    tier: 'silver',
    xpReward: 150,
    condition: (stats) => stats.perfectScans >= 1
  },

  // Animal-specific
  dog_lover: {
    id: 'dog_lover',
    name: 'Hundefreund',
    description: 'Behandle 10 Hunde',
    icon: '🐕',
    tier: 'bronze',
    xpReward: 200,
    condition: (stats) => stats.animalDiagnoses.dog >= 10
  },

  cat_whispered: {
    id: 'cat_whispered',
    name: 'Katzenflüsterer',
    description: 'Behandle 10 Katzen',
    icon: '🐈',
    tier: 'bronze',
    xpReward: 200,
    condition: (stats) => stats.animalDiagnoses.cat >= 10
  },

  exotic_expert: {
    id: 'exotic_expert',
    name: 'Exoten-Experte',
    description: 'Behandle alle 7 exotischen Tierarten',
    icon: '🦎',
    tier: 'gold',
    xpReward: 500,
    condition: (stats) => {
      const exoticAnimals = ['ferret', 'hedgehog', 'chinchilla', 'sugar_glider', 'turtle', 'snake', 'lizard'];
      return exoticAnimals.every(animal => stats.animalDiagnoses[animal] >= 1);
    }
  },

  // Speed Achievements
  lightning_diagnosis: {
    id: 'lightning_diagnosis',
    name: 'Blitzdiagnose',
    description: 'Diagnose in unter 1 Minute',
    icon: '⚡',
    tier: 'silver',
    xpReward: 250,
    condition: (stats) => stats.fastestDiagnosis <= 60
  },

  // Accuracy Achievements
  hundred_correct: {
    id: 'hundred_correct',
    name: '100 Erfolge',
    description: '100 korrekte Diagnosen',
    icon: '🎊',
    tier: 'gold',
    xpReward: 1000,
    condition: (stats) => stats.correctDiagnoses >= 100
  },

  // Collection Achievements
  disease_encyclopedia: {
    id: 'disease_encyclopedia',
    name: 'Krankheits-Enzyklop\u00e4die',
    description: 'Alle 50 Krankheiten diagnostiziert',
    icon: '📚',
    tier: 'platinum',
    xpReward: 2000,
    condition: (stats) => stats.uniqueDiseasesDiagnosed >= 50
  },

  // Story Achievements
  story_chapter_1: {
    id: 'story_chapter_1',
    name: 'Erste Schritte',
    description: 'Story Kapitel 1 abgeschlossen',
    icon: '📖',
    tier: 'bronze',
    xpReward: 300,
    condition: (stats) => stats.storyProgress.chapter1 === 'completed'
  },

  // Daily/Weekly
  daily_dedication: {
    id: 'daily_dedication',
    name: 'T\u00e4gliche Hingabe',
    description: '7 Tage in Folge gespielt',
    icon: '🔥',
    tier: 'silver',
    xpReward: 500,
    condition: (stats) => stats.consecutiveDays >= 7
  },

  // Special Achievements
  master_veterinarian: {
    id: 'master_veterinarian',
    name: 'Meister-Tierarzt',
    description: 'Erreiche Level 30',
    icon: '🏆',
    tier: 'platinum',
    xpReward: 5000,
    condition: (stats) => stats.level >= 30
  }
};

// Total: 50+ Achievements
// Tiers: Bronze (20), Silver (15), Gold (10), Platinum (5)
```

### 1.3 Daily Challenges

**Datei:** `src/gamification/DailyChallenges/ChallengeManager.js`

```javascript
export class DailyChallengeManager {
  constructor() {
    this.challenges = this.generateDailyChallenges();
    this.lastGenerated = new Date().toDateString();
  }

  generateDailyChallenges() {
    const today = new Date();
    const seed = today.getFullYear() * 10000 +
                 (today.getMonth() + 1) * 100 +
                 today.getDate();

    // Pseudo-random based on date
    const random = this.seededRandom(seed);

    return [
      this.generateAnimalChallenge(random),
      this.generateSpeedChallenge(random),
      this.generateAccuracyChallenge(random)
    ];
  }

  generateAnimalChallenge(random) {
    const animals = ['dog', 'cat', 'rabbit', 'horse', 'bird'];
    const animal = animals[Math.floor(random() * animals.length)];
    const count = 3 + Math.floor(random() * 5); // 3-7

    return {
      id: 'daily_animal',
      type: 'animal',
      title: `${count} ${getAnimalName(animal)} behandeln`,
      description: `Diagnostiziere heute ${count} ${getAnimalName(animal)}`,
      icon: getAnimalIcon(animal),
      target: count,
      progress: 0,
      xpReward: count * 50,
      animal
    };
  }

  generateSpeedChallenge(random) {
    const timeLimit = 120 + Math.floor(random() * 120); // 2-4 minutes
    const count = 2 + Math.floor(random() * 3); // 2-4

    return {
      id: 'daily_speed',
      type: 'speed',
      title: `Schnelldiagnosen`,
      description: `${count} Diagnosen unter ${timeLimit}s`,
      icon: '⚡',
      target: count,
      progress: 0,
      xpReward: 200,
      timeLimit
    };
  }

  generateAccuracyChallenge(random) {
    const count = 5 + Math.floor(random() * 5); // 5-9

    return {
      id: 'daily_accuracy',
      type: 'accuracy',
      title: 'Perfekte Serie',
      description: `${count} korrekte Diagnosen in Folge`,
      icon: '🎯',
      target: count,
      progress: 0,
      xpReward: 300,
      streak: 0
    };
  }

  updateProgress(challengeId, progress) {
    const challenge = this.challenges.find(c => c.id === challengeId);
    if (challenge) {
      challenge.progress = Math.min(progress, challenge.target);

      if (challenge.progress >= challenge.target) {
        return this.completeChallenge(challengeId);
      }
    }
    return null;
  }

  completeChallenge(challengeId) {
    const challenge = this.challenges.find(c => c.id === challengeId);
    if (challenge && !challenge.completed) {
      challenge.completed = true;
      challenge.completedAt = new Date();

      return {
        challenge,
        xpReward: challenge.xpReward,
        message: `Challenge abgeschlossen: ${challenge.title}!`
      };
    }
    return null;
  }

  seededRandom(seed) {
    return function() {
      seed = (seed * 9301 + 49297) % 233280;
      return seed / 233280;
    };
  }
}
```

---

## 📖 Phase 2: Story Mode System (Woche 3-4)

### 2.1 Story Structure

**Datei:** `src/story/chapters/chapter-structure.js`

```javascript
export const STORY_CHAPTERS = {
  chapter1: {
    id: 'chapter1',
    title: 'Erste Schritte',
    subtitle: 'Dein erster Tag in der Tierklinik',
    difficulty: 'beginner',
    requiredLevel: 1,
    estimatedDuration: 30, // minutes
    scenes: [
      {
        id: 'intro',
        type: 'dialog',
        character: 'dr_weber',
        background: 'clinic_entrance',
        dialog: [
          {
            speaker: 'dr_weber',
            text: 'Willkommen! Ich bin Dr. Weber. Sch\u00f6n, dass du heute bei uns anfängst!',
            emotion: 'happy'
          },
          {
            speaker: 'player',
            text: 'Danke! Ich bin schon sehr aufgeregt.',
            choices: [
              { text: 'Ich freue mich sehr!', next: 'tour', emotion: 'excited' },
              { text: 'Etwas nervös...', next: 'reassurance', emotion: 'nervous' }
            ]
          }
        ]
      },
      {
        id: 'first_patient',
        type: 'diagnosis',
        patient: {
          animal: 'dog',
          name: 'Bello',
          age: 3,
          breed: 'Labrador',
          condition: 'respiratory',
          difficulty: 'easy'
        },
        guidance: {
          hints: [
            'Achte auf die Atemfrequenz',
            'Die Körpertemperatur ist erhöht',
            'Höre auf die Lungen-Geräusche'
          ],
          autoReveal: false,
          dr_weber_comments: [
            'Guter Start! Weiter so.',
            'Schau dir die Vitalparameter genau an.'
          ]
        },
        success: {
          nextScene: 'congratulations',
          xpReward: 150,
          unlocks: ['basic_scanner']
        },
        failure: {
          nextScene: 'try_again',
          allowRetry: true
        }
      }
    ],
    completion: {
      xpReward: 500,
      unlocks: ['chapter2', 'achievement_first_steps'],
      certificate: true
    }
  },

  chapter2: {
    id: 'chapter2',
    title: 'Die Notfall-Nacht',
    subtitle: 'Mehrere Notfälle gleichzeitig',
    difficulty: 'intermediate',
    requiredLevel: 5,
    estimatedDuration: 45,
    scenes: [
      // Triage-System
      {
        id: 'emergency_arrival',
        type: 'triage',
        patients: [
          {
            name: 'Max',
            animal: 'dog',
            condition: 'fracture',
            severity: 'high',
            timeLimit: 600 // 10 minutes
          },
          {
            name: 'Luna',
            animal: 'cat',
            condition: 'poisoning',
            severity: 'critical',
            timeLimit: 300 // 5 minutes
          },
          {
            name: 'Hoppel',
            animal: 'rabbit',
            condition: 'gi_stasis',
            severity: 'medium',
            timeLimit: 900 // 15 minutes
          }
        ],
        objective: 'Priorisiere die Patienten nach Dringlichkeit',
        correctOrder: ['Luna', 'Max', 'Hoppel']
      }
    ]
  },

  chapter3: {
    id: 'chapter3',
    title: 'Exotische Patienten',
    subtitle: 'Ungewöhnliche Tiere brauchen deine Hilfe',
    difficulty: 'advanced',
    requiredLevel: 10,
    estimatedDuration: 60
  },

  chapter4: {
    id: 'chapter4',
    title: 'Veterinär-Forscher',
    subtitle: 'Eine mysteriöse Krankheit',
    difficulty: 'expert',
    requiredLevel: 20,
    estimatedDuration: 90
  }
};
```

### 2.2 Dialog System

**Component:** `src/story/DialogSystem.jsx`

```jsx
import React, { useState } from 'react';
import { MessageCircle, User } from 'lucide-react';

export const DialogSystem = ({ scene, onChoiceMade, onComplete }) => {
  const [currentDialogIndex, setCurrentDialogIndex] = useState(0);
  const [selectedChoice, setSelectedChoice] = useState(null);

  const currentDialog = scene.dialog[currentDialogIndex];

  const handleChoice = (choice) => {
    setSelectedChoice(choice);
    onChoiceMade(choice);

    setTimeout(() => {
      if (choice.next) {
        // Navigate to next scene
        onComplete(choice.next);
      } else {
        // Next dialog in current scene
        setCurrentDialogIndex(prev => prev + 1);
        setSelectedChoice(null);
      }
    }, 500);
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-blue-900 via-purple-900 to-indigo-900">
      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center opacity-40"
        style={{ backgroundImage: `url(/backgrounds/${scene.background}.jpg)` }}
      />

      {/* Character Portrait */}
      <div className="absolute left-10 bottom-32 w-64 h-96">
        <img
          src={`/characters/${currentDialog.speaker}.png`}
          alt={currentDialog.speaker}
          className="w-full h-full object-contain animate-fade-in"
        />
      </div>

      {/* Dialog Box */}
      <div className="absolute bottom-0 left-0 right-0 p-8">
        <div className="bg-gray-900/95 rounded-2xl p-6 backdrop-blur-md border-2 border-cyan-500/50 shadow-2xl">
          {/* Speaker Name */}
          <div className="flex items-center gap-2 mb-4">
            {currentDialog.speaker === 'player' ? (
              <User className="w-5 h-5 text-cyan-400" />
            ) : (
              <MessageCircle className="w-5 h-5 text-purple-400" />
            )}
            <span className="font-bold text-lg text-white">
              {getSpeakerName(currentDialog.speaker)}
            </span>
          </div>

          {/* Dialog Text */}
          <div className="text-white text-lg mb-6 leading-relaxed">
            <TypewriterText text={currentDialog.text} speed={30} />
          </div>

          {/* Choices */}
          {currentDialog.choices && (
            <div className="space-y-3">
              {currentDialog.choices.map((choice, index) => (
                <button
                  key={index}
                  onClick={() => handleChoice(choice)}
                  disabled={selectedChoice !== null}
                  className={`w-full p-4 rounded-lg text-left transition-all ${
                    selectedChoice === choice
                      ? 'bg-cyan-600 text-white'
                      : 'bg-gray-800 hover:bg-gray-700 text-cyan-300'
                  }`}
                >
                  <span className="font-medium">{choice.text}</span>
                </button>
              ))}
            </div>
          )}

          {/* Continue Button (if no choices) */}
          {!currentDialog.choices && currentDialogIndex < scene.dialog.length - 1 && (
            <button
              onClick={() => setCurrentDialogIndex(prev => prev + 1)}
              className="mt-4 px-6 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition-colors"
            >
              Weiter →
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

function getSpeakerName(speaker) {
  const names = {
    dr_weber: 'Dr. Weber',
    player: 'Du',
    assistant: 'Assistentin Maria',
    receptionist: 'Empfang'
  };
  return names[speaker] || speaker;
}

const TypewriterText = ({ text, speed = 30 }) => {
  const [displayedText, setDisplayedText] = useState('');

  React.useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      if (index < text.length) {
        setDisplayedText(text.substring(0, index + 1));
        index++;
      } else {
        clearInterval(interval);
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text, speed]);

  return <span>{displayedText}</span>;
};
```

---

## 🤖 Phase 3: AI Assistant (Woche 5)

**Datei:** `src/ai/DrWatsonAssistant.jsx`

```jsx
import React, { useState } from 'react';
import { Bot, Send, HelpCircle } from 'lucide-react';

export const DrWatsonAssistant = ({ context }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hallo! Ich bin Dr. Watson, dein AI-Assistent. Frag mich alles über Tiermedizin!'
    }
  ]);
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  const knowledgeBase = {
    // Simplified knowledge base
    'parvovirose': {
      answer: 'Parvovirose ist eine hochansteckende Viruserkrankung bei Hunden. Typische Symptome sind:\n• Blutiger Durchfall 💩\n• Erbrechen 🤮\n• Fieber 🌡️\n• Dehydration 💧\n\nBehandlung: Intensive Flüssigkeitstherapie und supportive care.',
      relatedTopics: ['dehydration', 'viruserkrankungen', 'welpenerkrankungen']
    },
    // ... 50+ topics
  };

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);

    // Simple keyword matching (replace with actual AI later)
    const response = generateResponse(input, knowledgeBase, context);

    setTimeout(() => {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response
      }]);
    }, 500);

    setInput('');
  };

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-8 right-8 w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full shadow-2xl flex items-center justify-center hover:scale-110 transition-transform z-50"
      >
        <Bot className="w-8 h-8 text-white" />
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-28 right-8 w-96 h-[500px] bg-gray-900 rounded-2xl shadow-2xl border-2 border-cyan-500/50 flex flex-col z-50">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-4 rounded-t-2xl">
            <div className="flex items-center gap-3">
              <Bot className="w-6 h-6 text-white" />
              <div>
                <h3 className="font-bold text-white">Dr. Watson</h3>
                <p className="text-xs text-cyan-100">AI Veterinär-Assistent</p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-cyan-600 text-white'
                      : 'bg-gray-800 text-gray-100'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-800">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Frag mich etwas..."
                className="flex-1 bg-gray-800 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"
              />
              <button
                onClick={handleSend}
                className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-lg transition-colors"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

function generateResponse(input, knowledgeBase, context) {
  input = input.toLowerCase();

  // Check knowledge base
  for (const [topic, data] of Object.entries(knowledgeBase)) {
    if (input.includes(topic)) {
      return data.answer;
    }
  }

  // Context-aware responses
  if (context.currentAnimal) {
    return `Du untersuchst gerade einen ${context.currentAnimal}. Möchtest du mehr über typische Krankheiten bei dieser Tierart erfahren?`;
  }

  // Default
  return 'Das ist eine interessante Frage! Kannst du genauer beschreiben, was du wissen möchtest?';
}
```

---

## 💾 Phase 4: Data Persistence (Woche 6)

**Datei:** `src/storage/GameStateManager.js`

```javascript
import { openDB } from 'idb';

export class GameStateManager {
  constructor() {
    this.dbPromise = this.initDB();
  }

  async initDB() {
    return openDB('VetScanProDB', 1, {
      upgrade(db) {
        // Player Profile
        db.createObjectStore('profile', { keyPath: 'id' });

        // Game Progress
        db.createObjectStore('progress', { keyPath: 'id' });

        // Achievements
        db.createObjectStore('achievements', { keyPath: 'id' });

        // Diagnosis History
        db.createObjectStore('history', { keyPath: 'id', autoIncrement: true });
      }
    });
  }

  async saveProgress(data) {
    const db = await this.dbPromise;
    await db.put('progress', {
      id: 'current',
      level: data.level,
      xp: data.xp,
      totalXP: data.totalXP,
      unlockedAnimals: data.unlockedAnimals,
      unlockedConditions: data.unlockedConditions,
      storyProgress: data.storyProgress,
      lastPlayed: new Date().toISOString()
    });
  }

  async loadProgress() {
    const db = await this.dbPromise;
    return await db.get('progress', 'current');
  }

  async saveAchievement(achievement) {
    const db = await this.dbPromise;
    await db.put('achievements', {
      ...achievement,
      unlockedAt: new Date().toISOString()
    });
  }

  async saveDiagnosis(diagnosisData) {
    const db = await this.dbPromise;
    await db.add('history', {
      ...diagnosisData,
      timestamp: new Date().toISOString()
    });
  }

  async getStats() {
    const db = await this.dbPromise;
    const history = await db.getAll('history');

    return {
      totalDiagnoses: history.length,
      correctDiagnoses: history.filter(d => d.correct).length,
      accuracy: (history.filter(d => d.correct).length / history.length) * 100,
      favoriteAnimal: this.getMostFrequent(history.map(d => d.animal)),
      averageTime: history.reduce((sum, d) => sum + d.timeSpent, 0) / history.length
    };
  }
}
```

---

## 📱 Phase 5: Polish & Testing (Woche 7-8)

### 5.1 Tutorial System
### 5.2 Accessibility
### 5.3 Performance Optimization
### 5.4 Testing (Unit, Integration, E2E)
### 5.5 Documentation

---

## ✅ Zusammenfassung

**Masterversion enthält:**
1. ✅ React App (Core)
2. ✅ Gamification (Level, Achievements, Challenges)
3. ✅ Story Mode (4 Kapitel)
4. ✅ AI Assistant (Dr. Watson)
5. ✅ Professional Tools
6. ✅ Data Persistence
7. ✅ Tutorial System

**Zeitplan:** 6-8 Wochen
**Tech Stack:** React + Vite + Tailwind + IndexedDB
**Deployment:** vibecoding.company via GitHub Actions

---

**Erstellt:** 2024-11-21
**Status:** ✅ Bereit zur Implementierung
**Nächster Schritt:** Phase 1 Gamification starten

