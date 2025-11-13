/**
 * VetScan Pro - Game Engine
 * Manages game progression, XP, levels, achievements, and player stats
 */

export class GameEngine {
  constructor() {
    this.state = this.loadState() || this.getInitialState();
  }

  getInitialState() {
    return {
      player: {
        name: 'Dr. Neuling',
        level: 1,
        xp: 0,
        xpToNextLevel: 100,
        career: 'praktikant', // praktikant, assistenz, facharzt, oberarzt, chefarzt
        totalPatients: 0,
        correctDiagnoses: 0,
        totalEarnings: 0,
        playTime: 0
      },
      stats: {
        diagnosisAccuracy: 0,
        averageTime: 0,
        fastestDiagnosis: null,
        perfectDiagnoses: 0,
        emergenciesSaved: 0,
        speciesUnlocked: ['dog', 'cat', 'mouse', 'goldfish', 'turtle'] // Start with 5 basic
      },
      unlocks: {
        animals: ['dog', 'cat', 'mouse', 'goldfish', 'turtle'],
        equipment: ['basic_stethoscope', 'basic_thermometer', 'basic_scanner'],
        treatments: ['basic_antibiotics', 'basic_painkillers', 'bandages'],
        modes: ['tutorial', 'practice']
      },
      achievements: [],
      factCards: [],
      inventory: {
        coins: 0,
        gems: 0,
        equipment: ['basic_stethoscope', 'basic_thermometer', 'basic_scanner']
      },
      currentSession: {
        patientsToday: 0,
        xpEarnedToday: 0,
        startTime: Date.now()
      },
      settings: {
        soundEnabled: true,
        musicVolume: 0.5,
        sfxVolume: 0.7,
        difficulty: 'normal', // easy, normal, hard, expert
        tutorialCompleted: false
      }
    };
  }

  // XP and Leveling System
  addXP(amount, reason = '') {
    this.state.player.xp += amount;
    this.state.currentSession.xpEarnedToday += amount;

    const leveledUp = this.checkLevelUp();

    return {
      xpGained: amount,
      leveledUp,
      newLevel: this.state.player.level,
      reason
    };
  }

  checkLevelUp() {
    let leveledUp = false;

    while (this.state.player.xp >= this.state.player.xpToNextLevel) {
      this.state.player.xp -= this.state.player.xpToNextLevel;
      this.state.player.level++;
      leveledUp = true;

      // Increase XP requirement for next level (exponential growth)
      this.state.player.xpToNextLevel = Math.floor(
        100 * Math.pow(1.15, this.state.player.level - 1)
      );

      // Update career based on level
      this.updateCareer();

      // Award level-up rewards
      this.grantLevelRewards(this.state.player.level);
    }

    this.saveState();
    return leveledUp;
  }

  updateCareer() {
    const level = this.state.player.level;

    if (level >= 50) {
      this.state.player.career = 'chefarzt';
      this.state.player.name = 'Chefarzt Dr. ' + this.extractLastName();
    } else if (level >= 30) {
      this.state.player.career = 'oberarzt';
      this.state.player.name = 'Oberarzt Dr. ' + this.extractLastName();
    } else if (level >= 15) {
      this.state.player.career = 'facharzt';
      this.state.player.name = 'Facharzt Dr. ' + this.extractLastName();
    } else if (level >= 5) {
      this.state.player.career = 'assistenz';
      this.state.player.name = 'Dr. ' + this.extractLastName();
    }
  }

  extractLastName() {
    const names = this.state.player.name.split(' ');
    return names[names.length - 1];
  }

  grantLevelRewards(level) {
    const rewards = {
      coins: level * 50,
      gems: Math.floor(level / 5)
    };

    this.state.inventory.coins += rewards.coins;
    this.state.inventory.gems += rewards.gems;

    // Unlock content based on level
    this.checkContentUnlocks(level);

    return rewards;
  }

  checkContentUnlocks(level) {
    const unlockSchedule = {
      2: { animal: 'rabbit', equipment: 'digital_thermometer' },
      3: { equipment: 'advanced_stethoscope' },
      4: { animal: 'guinea_pig', treatment: 'advanced_antibiotics' },
      5: { mode: 'campaign' },
      6: { animal: 'hamster' },
      7: { equipment: 'xray_machine' },
      8: { animal: 'bird' },
      10: { mode: 'emergency', animal: 'horse' },
      12: { animal: 'cow', equipment: 'ultrasound' },
      15: { animal: 'pig', mode: 'expert' },
      18: { animal: 'sheep', equipment: 'blood_analyzer' },
      20: { animal: 'goat', mode: 'timed_challenge' },
      22: { animal: 'chicken' },
      25: { animal: 'ferret', equipment: 'mri_scanner' },
      28: { animal: 'hedgehog' },
      30: { animal: 'chinchilla', mode: 'multi_patient' },
      35: { animal: 'sugar_glider' }
    };

    const unlock = unlockSchedule[level];
    if (unlock) {
      if (unlock.animal && !this.state.unlocks.animals.includes(unlock.animal)) {
        this.state.unlocks.animals.push(unlock.animal);
        this.state.stats.speciesUnlocked.push(unlock.animal);
      }
      if (unlock.equipment && !this.state.unlocks.equipment.includes(unlock.equipment)) {
        this.state.unlocks.equipment.push(unlock.equipment);
        this.state.inventory.equipment.push(unlock.equipment);
      }
      if (unlock.treatment && !this.state.unlocks.treatments.includes(unlock.treatment)) {
        this.state.unlocks.treatments.push(unlock.treatment);
      }
      if (unlock.mode && !this.state.unlocks.modes.includes(unlock.mode)) {
        this.state.unlocks.modes.push(unlock.mode);
      }
    }
  }

  // Diagnosis Evaluation
  evaluateDiagnosis(patientData, playerDiagnosis, timeTaken, thoroughness) {
    const isCorrect = playerDiagnosis.id === patientData.correctDiagnosis.id;

    let baseXP = 50;
    let bonusXP = 0;
    let accuracy = 0;

    if (isCorrect) {
      this.state.player.correctDiagnoses++;
      accuracy = 100;

      // Time bonus (faster = more XP, but with minimum quality check)
      if (timeTaken < 60 && thoroughness >= 0.7) {
        bonusXP += 25; // Speed bonus
      }

      // Thoroughness bonus
      if (thoroughness >= 0.9) {
        bonusXP += 30; // Perfect examination
        this.state.stats.perfectDiagnoses++;
      } else if (thoroughness >= 0.7) {
        bonusXP += 15; // Good examination
      }

      // Emergency bonus
      if (patientData.severity === 'critical' || patientData.severity === 'high') {
        bonusXP += 40;
        this.state.stats.emergenciesSaved++;
      }

      // First time treating this species bonus
      if (!this.state.stats.speciesUnlocked.includes(patientData.animalType)) {
        bonusXP += 50;
      }

    } else {
      // Incorrect diagnosis penalty
      baseXP = 10;
      accuracy = this.calculateSimilarity(playerDiagnosis, patientData.correctDiagnosis);
    }

    const totalXP = baseXP + bonusXP;
    const xpResult = this.addXP(totalXP, isCorrect ? 'Korrekte Diagnose' : 'Diagnose verfehlt');

    // Update stats
    this.state.player.totalPatients++;
    this.state.currentSession.patientsToday++;

    // Update accuracy
    this.state.stats.diagnosisAccuracy =
      (this.state.player.correctDiagnoses / this.state.player.totalPatients) * 100;

    // Update fastest diagnosis
    if (isCorrect && timeTaken < 60) {
      if (!this.state.stats.fastestDiagnosis || timeTaken < this.state.stats.fastestDiagnosis) {
        this.state.stats.fastestDiagnosis = timeTaken;
      }
    }

    // Check achievements
    const newAchievements = this.checkAchievements();

    this.saveState();

    return {
      correct: isCorrect,
      accuracy,
      xpGained: totalXP,
      bonusXP,
      ...xpResult,
      achievements: newAchievements,
      feedback: this.generateFeedback(isCorrect, patientData, playerDiagnosis, thoroughness)
    };
  }

  calculateSimilarity(diagnosis1, diagnosis2) {
    // Simple similarity based on category and severity
    let similarity = 0;

    if (diagnosis1.category === diagnosis2.category) similarity += 30;
    if (diagnosis1.severity === diagnosis2.severity) similarity += 20;

    // Check symptom overlap
    const symptoms1 = new Set(diagnosis1.symptoms || []);
    const symptoms2 = new Set(diagnosis2.symptoms || []);
    const overlap = [...symptoms1].filter(s => symptoms2.has(s)).length;
    const totalSymptoms = Math.max(symptoms1.size, symptoms2.size);

    if (totalSymptoms > 0) {
      similarity += (overlap / totalSymptoms) * 50;
    }

    return Math.round(similarity);
  }

  generateFeedback(isCorrect, patientData, playerDiagnosis, thoroughness) {
    if (isCorrect) {
      const messages = [
        `Ausgezeichnet! ${patientData.name} wird sich schnell erholen.`,
        `Perfekt diagnostiziert! Du hast ${patientData.name} geholfen.`,
        `Sehr gut! Die Behandlung kann sofort beginnen.`,
        `Hervorragend! ${patientData.name}'s Besitzer ist sehr erleichtert.`
      ];

      let feedback = {
        title: '✅ Korrekte Diagnose!',
        message: messages[Math.floor(Math.random() * messages.length)],
        explanation: `Die Symptome ${patientData.symptoms.join(', ')} deuten klar auf ${patientData.correctDiagnosis.name} hin.`,
        tips: thoroughness >= 0.9 ?
          ['Perfekte Untersuchung! Du hast alle Tests durchgeführt.'] :
          ['Gut gemacht! Versuche beim nächsten Mal alle verfügbaren Tests zu nutzen.'],
        educationalFact: this.getEducationalFact(patientData)
      };

      return feedback;
    } else {
      return {
        title: '❌ Falsche Diagnose',
        message: `Die Diagnose war leider nicht korrekt. ${patientData.name} leidet an ${patientData.correctDiagnosis.name}.`,
        explanation: `Obwohl ${playerDiagnosis.name} ähnliche Symptome zeigen kann, weisen die Untersuchungsergebnisse auf ${patientData.correctDiagnosis.name} hin.`,
        tips: [
          'Achte genau auf alle Vitalparameter',
          'Nutze alle verfügbaren Diagnose-Tools',
          'Vergleiche die Symptome mit den Normalwerten'
        ],
        correctDiagnosis: patientData.correctDiagnosis,
        educationalFact: this.getEducationalFact(patientData)
      };
    }
  }

  getEducationalFact(patientData) {
    const facts = patientData.education?.funFacts || [];
    return facts[Math.floor(Math.random() * facts.length)] ||
      'Wusstest du? Jede Tierart hat einzigartige Vitalparameter!';
  }

  // Achievements System
  checkAchievements() {
    const newAchievements = [];
    const achievements = [
      {
        id: 'first_patient',
        name: 'Erster Patient',
        description: 'Behandle deinen ersten Patienten',
        condition: () => this.state.player.totalPatients >= 1,
        icon: '🎯',
        xp: 50
      },
      {
        id: 'perfect_ten',
        name: 'Perfekte 10',
        description: '10 Patienten korrekt diagnostiziert',
        condition: () => this.state.player.correctDiagnoses >= 10,
        icon: '🌟',
        xp: 100
      },
      {
        id: 'speed_demon',
        name: 'Blitzdiagnose',
        description: 'Diagnose in unter 30 Sekunden',
        condition: () => this.state.stats.fastestDiagnosis && this.state.stats.fastestDiagnosis < 30,
        icon: '⚡',
        xp: 150
      },
      {
        id: 'perfectionist',
        name: 'Perfektionist',
        description: '5 perfekte Diagnosen (100% Gründlichkeit)',
        condition: () => this.state.stats.perfectDiagnoses >= 5,
        icon: '💯',
        xp: 200
      },
      {
        id: 'lifesaver',
        name: 'Lebensretter',
        description: '10 Notfälle erfolgreich behandelt',
        condition: () => this.state.stats.emergenciesSaved >= 10,
        icon: '🚑',
        xp: 250
      },
      {
        id: 'accuracy_master',
        name: 'Diagnose-Meister',
        description: '90% Genauigkeit erreicht',
        condition: () => this.state.stats.diagnosisAccuracy >= 90,
        icon: '🎓',
        xp: 300
      },
      {
        id: 'species_expert',
        name: 'Arten-Experte',
        description: '10 verschiedene Tierarten behandelt',
        condition: () => this.state.stats.speciesUnlocked.length >= 10,
        icon: '🦁',
        xp: 400
      },
      {
        id: 'century_club',
        name: 'Century Club',
        description: '100 Patienten behandelt',
        condition: () => this.state.player.totalPatients >= 100,
        icon: '💯',
        xp: 500
      }
    ];

    achievements.forEach(achievement => {
      if (!this.state.achievements.includes(achievement.id) && achievement.condition()) {
        this.state.achievements.push(achievement.id);
        newAchievements.push(achievement);
        this.addXP(achievement.xp, `Achievement: ${achievement.name}`);
      }
    });

    if (newAchievements.length > 0) {
      this.saveState();
    }

    return newAchievements;
  }

  // Fact Cards Collection
  collectFactCard(card) {
    if (!this.state.factCards.find(c => c.id === card.id)) {
      this.state.factCards.push(card);
      this.addXP(25, 'Fact Card gesammelt');
      this.saveState();
      return true;
    }
    return false;
  }

  // Save/Load State
  saveState() {
    try {
      localStorage.setItem('vetScanGameState', JSON.stringify(this.state));
      return true;
    } catch (error) {
      console.error('Failed to save game state:', error);
      return false;
    }
  }

  loadState() {
    try {
      const saved = localStorage.getItem('vetScanGameState');
      return saved ? JSON.parse(saved) : null;
    } catch (error) {
      console.error('Failed to load game state:', error);
      return null;
    }
  }

  resetProgress() {
    this.state = this.getInitialState();
    this.saveState();
  }

  // Getters
  getPlayerInfo() {
    return this.state.player;
  }

  getStats() {
    return this.state.stats;
  }

  getUnlocks() {
    return this.state.unlocks;
  }

  getAchievements() {
    return this.state.achievements;
  }

  getInventory() {
    return this.state.inventory;
  }

  isAnimalUnlocked(animalId) {
    return this.state.unlocks.animals.includes(animalId);
  }

  isModeUnlocked(mode) {
    return this.state.unlocks.modes.includes(mode);
  }

  // Shop System
  purchaseItem(item, cost) {
    if (this.state.inventory.coins >= cost) {
      this.state.inventory.coins -= cost;

      if (item.type === 'equipment' && !this.state.inventory.equipment.includes(item.id)) {
        this.state.inventory.equipment.push(item.id);
        this.state.unlocks.equipment.push(item.id);
      }

      this.saveState();
      return { success: true, item };
    }

    return { success: false, reason: 'Nicht genug Münzen' };
  }
}

// Singleton instance
let gameEngineInstance = null;

export const getGameEngine = () => {
  if (!gameEngineInstance) {
    gameEngineInstance = new GameEngine();
  }
  return gameEngineInstance;
};

export default GameEngine;
