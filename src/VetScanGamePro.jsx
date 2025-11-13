import React, { useState, useEffect } from 'react';
import {
  Heart, Zap, Trophy, Star, Award, ArrowRight, RefreshCw,
  CheckCircle, XCircle, Clock, Target, BookOpen, Settings, TrendingUp
} from 'lucide-react';

import { getGameEngine } from './game/GameEngine';
import TutorialSystem from './components/TutorialSystem';
import {
  StethoscopeGame,
  XRayGame,
  BloodTestGame,
  PalpationGame
} from './components/DiagnosticMinigames';

import { ANIMAL_SPECIES, generatePatients, getVitalSignsForAnimal } from './veterinary-medical-data';

/**
 * VetScan Game Pro - Professional Veterinary Simulation Game
 * Features: Progression system, minigames, tutorial, achievements, educational content
 */
const VetScanGamePro = () => {
  // Game Engine
  const [gameEngine] = useState(() => getGameEngine());
  const [playerInfo, setPlayerInfo] = useState(gameEngine.getPlayerInfo());
  const [stats, setStats] = useState(gameEngine.getStats());
  const [unlocks, setUnlocks] = useState(gameEngine.getUnlocks());

  // Game State
  const [gameState, setGameState] = useState('menu'); // menu, tutorial, patient_select, examination, diagnosis, feedback
  const [currentPatient, setCurrentPatient] = useState(null);
  const [examinationData, setExaminationData] = useState({});
  const [selectedDiagnosis, setSelectedDiagnosis] = useState(null);
  const [sessionStartTime, setSessionStartTime] = useState(null);

  // UI State
  const [showAchievementPopup, setShowAchievementPopup] = useState(null);
  const [showLevelUpPopup, setShowLevelUpPopup] = useState(null);

  // Available patients
  const [availablePatients, setAvailablePatients] = useState([]);

  useEffect(() => {
    // Check if tutorial should be shown
    if (!gameEngine.state.settings.tutorialCompleted) {
      setGameState('tutorial');
    }

    // Generate available patients
    refreshPatients();
  }, []);

  const refreshPlayerInfo = () => {
    setPlayerInfo(gameEngine.getPlayerInfo());
    setStats(gameEngine.getStats());
    setUnlocks(gameEngine.getUnlocks());
  };

  const refreshPatients = () => {
    const allPatients = generatePatients();
    // Filter by unlocked animals
    const available = allPatients.filter(p =>
      unlocks.animals.includes(p.animalType)
    ).slice(0, 5); // Show 5 patients at a time

    setAvailablePatients(available);
  };

  // Tutorial Complete Handler
  const handleTutorialComplete = (result) => {
    if (!result.skipped) {
      gameEngine.state.inventory.coins += result.coinsGained || 0;
      gameEngine.addXP(result.xpGained || 0, 'Tutorial abgeschlossen');
    }

    gameEngine.state.settings.tutorialCompleted = true;
    gameEngine.saveState();
    refreshPlayerInfo();
    setGameState('menu');
  };

  // Patient Selection
  const handleSelectPatient = (patient) => {
    setCurrentPatient(patient);
    setExaminationData({});
    setSelectedDiagnosis(null);
    setSessionStartTime(Date.now());
    setGameState('examination');
  };

  // Examination Tools Complete Handlers
  const handleToolComplete = (toolData) => {
    setExaminationData({
      ...examinationData,
      [toolData.tool]: toolData
    });
  };

  // Calculate overall thoroughness
  const calculateThoroughness = () => {
    const tools = Object.values(examinationData);
    if (tools.length === 0) return 0;

    const totalThoroughness = tools.reduce((sum, tool) => sum + (tool.thoroughness || 0), 0);
    return totalThoroughness / tools.length;
  };

  // Proceed to Diagnosis
  const handleProceedToDiagnosis = () => {
    if (Object.keys(examinationData).length < 2) {
      alert('Führe mindestens 2 Untersuchungen durch für eine fundierte Diagnose!');
      return;
    }
    setGameState('diagnosis');
  };

  // Submit Diagnosis
  const handleSubmitDiagnosis = () => {
    if (!selectedDiagnosis) {
      alert('Bitte wähle eine Diagnose!');
      return;
    }

    const timeTaken = Math.floor((Date.now() - sessionStartTime) / 1000);
    const thoroughness = calculateThoroughness();

    const result = gameEngine.evaluateDiagnosis(
      currentPatient,
      selectedDiagnosis,
      timeTaken,
      thoroughness
    );

    // Show achievements if any
    if (result.achievements && result.achievements.length > 0) {
      setShowAchievementPopup(result.achievements);
      setTimeout(() => setShowAchievementPopup(null), 5000);
    }

    // Show level up if occurred
    if (result.leveledUp) {
      setShowLevelUpPopup(result.newLevel);
      setTimeout(() => setShowLevelUpPopup(null), 5000);
    }

    refreshPlayerInfo();
    setGameState('feedback');
  };

  // Next Patient
  const handleNextPatient = () => {
    refreshPatients();
    setCurrentPatient(null);
    setExaminationData({});
    setSelectedDiagnosis(null);
    setGameState('patient_select');
  };

  // Return to Menu
  const handleReturnToMenu = () => {
    setGameState('menu');
    refreshPatients();
  };

  // Render Tutorial
  if (gameState === 'tutorial') {
    return <TutorialSystem onComplete={handleTutorialComplete} />;
  }

  // Render Main Menu
  if (gameState === 'menu') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
        {/* Header with Player Info */}
        <div className="border-b border-cyan-800/50 bg-gray-900/80 backdrop-blur-xl">
          <div className="p-4 flex items-center justify-between max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Zap className="w-8 h-8 text-cyan-400" />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                  VetScan Pro
                </h1>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <Trophy className="w-4 h-4 text-yellow-500" />
                <span className="text-gray-400">{playerInfo.career.toUpperCase()}</span>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <div className="text-xs text-gray-400">{playerInfo.name}</div>
                <div className="text-sm font-bold text-cyan-400">Level {playerInfo.level}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Menu Content */}
        <div className="p-8 max-w-6xl mx-auto">
          {/* Player Stats Card */}
          <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* XP Progress */}
              <div className="md:col-span-2">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">Erfahrung</span>
                  <span className="text-sm font-bold text-cyan-400">
                    {playerInfo.xp} / {playerInfo.xpToNextLevel} XP
                  </span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-cyan-600 to-blue-500 transition-all duration-500"
                    style={{ width: `${(playerInfo.xp / playerInfo.xpToNextLevel) * 100}%` }}
                  />
                </div>
              </div>

              {/* Stats */}
              <div className="text-center p-3 bg-gray-800/50 rounded-lg">
                <div className="text-2xl font-bold text-green-400">{stats.diagnosisAccuracy.toFixed(1)}%</div>
                <div className="text-xs text-gray-400">Genauigkeit</div>
              </div>
              <div className="text-center p-3 bg-gray-800/50 rounded-lg">
                <div className="text-2xl font-bold text-blue-400">{playerInfo.totalPatients}</div>
                <div className="text-xs text-gray-400">Patienten</div>
              </div>
            </div>
          </div>

          {/* Game Modes */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {/* Practice Mode */}
            <button
              onClick={() => setGameState('patient_select')}
              className="bg-gradient-to-br from-cyan-900/40 to-blue-900/40 hover:from-cyan-800/50 hover:to-blue-800/50 backdrop-blur-md rounded-xl p-8 border border-cyan-700/30 transition-all text-left group"
            >
              <div className="flex items-center gap-4 mb-4">
                <div className="p-4 bg-cyan-600/20 rounded-lg group-hover:bg-cyan-600/30 transition-colors">
                  <Heart className="w-10 h-10 text-cyan-400" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-cyan-400">Übungsmodus</h3>
                  <p className="text-sm text-gray-400">Lerne ohne Zeitdruck</p>
                </div>
              </div>
              <p className="text-gray-300 mb-4">
                Nimm dir Zeit, um Patienten gründlich zu untersuchen und verschiedene
                diagnostische Tools auszuprobieren.
              </p>
              <div className="flex items-center gap-2 text-cyan-400 font-medium">
                <span>Jetzt spielen</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </div>
            </button>

            {/* Campaign Mode - Locked */}
            <div className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 backdrop-blur-md rounded-xl p-8 border border-purple-700/20 opacity-60 text-left relative overflow-hidden">
              <div className="absolute top-4 right-4 bg-purple-600 text-white text-xs px-3 py-1 rounded-full font-bold">
                Level 5
              </div>
              <div className="flex items-center gap-4 mb-4">
                <div className="p-4 bg-purple-600/20 rounded-lg">
                  <BookOpen className="w-10 h-10 text-purple-400" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-purple-400">Kampagne</h3>
                  <p className="text-sm text-gray-400">Story-basierte Missionen</p>
                </div>
              </div>
              <p className="text-gray-400">
                Folge einer spannenden Geschichte und behandle verschiedene Fälle in
                fortlaufenden Kapiteln. Schalte frei ab Level 5!
              </p>
            </div>

            {/* Emergency Mode - Locked */}
            <div className="bg-gradient-to-br from-red-900/20 to-orange-900/20 backdrop-blur-md rounded-xl p-8 border border-red-700/20 opacity-60 text-left relative overflow-hidden">
              <div className="absolute top-4 right-4 bg-red-600 text-white text-xs px-3 py-1 rounded-full font-bold">
                Level 10
              </div>
              <div className="flex items-center gap-4 mb-4">
                <div className="p-4 bg-red-600/20 rounded-lg">
                  <Clock className="w-10 h-10 text-red-400" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-red-400">Notfall-Modus</h3>
                  <p className="text-sm text-gray-400">Schnelle Entscheidungen</p>
                </div>
              </div>
              <p className="text-gray-400">
                Kritische Fälle mit Zeitdruck - rette Leben unter extremen Bedingungen!
                Schalte frei ab Level 10!
              </p>
            </div>

            {/* Tutorial */}
            <button
              onClick={() => setGameState('tutorial')}
              className="bg-gradient-to-br from-green-900/20 to-emerald-900/20 hover:from-green-800/30 hover:to-emerald-800/30 backdrop-blur-md rounded-xl p-8 border border-green-700/20 transition-all text-left group"
            >
              <div className="flex items-center gap-4 mb-4">
                <div className="p-4 bg-green-600/20 rounded-lg group-hover:bg-green-600/30 transition-colors">
                  <Target className="w-10 h-10 text-green-400" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-green-400">Tutorial</h3>
                  <p className="text-sm text-gray-400">Lerne die Grundlagen</p>
                </div>
              </div>
              <p className="text-gray-300">
                Erfahre wie das Spiel funktioniert und lerne die diagnostischen Tools kennen.
              </p>
            </button>
          </div>

          {/* Achievements Preview */}
          <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-cyan-400 flex items-center gap-2">
                <Award className="w-5 h-5" />
                Erfolge ({gameEngine.state.achievements.length})
              </h3>
              <button className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors">
                Alle ansehen
              </button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {gameEngine.state.achievements.slice(0, 4).map(achId => (
                <div key={achId} className="bg-gray-800/50 p-3 rounded-lg text-center">
                  <div className="text-2xl mb-1">🏆</div>
                  <div className="text-xs text-gray-400">{achId.replace(/_/g, ' ')}</div>
                </div>
              ))}
              {gameEngine.state.achievements.length === 0 && (
                <div className="col-span-4 text-center text-gray-500 py-4">
                  Noch keine Erfolge. Starte deine erste Behandlung!
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Render Patient Selection
  if (gameState === 'patient_select') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
        {/* Header */}
        <div className="border-b border-cyan-800/50 bg-gray-900/80 backdrop-blur-xl">
          <div className="p-4 flex items-center justify-between max-w-7xl mx-auto">
            <h2 className="text-xl font-bold text-cyan-400">Wartezimmer - Wähle einen Patienten</h2>
            <button
              onClick={handleReturnToMenu}
              className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg transition-colors"
            >
              Zurück
            </button>
          </div>
        </div>

        {/* Patient List */}
        <div className="p-8 max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {availablePatients.map(patient => (
              <button
                key={patient.id}
                onClick={() => handleSelectPatient(patient)}
                className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30 hover:border-cyan-600 transition-all text-left group"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="text-6xl">{patient.icon || '🐕'}</div>
                  <div className="flex-1">
                    <div className="text-lg font-bold text-cyan-400">{patient.name}</div>
                    <div className="text-sm text-gray-400">{patient.animalName}</div>
                    <div className="text-xs text-gray-500">{patient.breed}</div>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="text-sm">
                    <span className="text-gray-400">Alter:</span>
                    <span className="text-gray-300 ml-2">{patient.age} Jahre</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-400">Charakter:</span>
                    <span className="text-gray-300 ml-2">{patient.personality}</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-400">Größe:</span>
                    <span className="text-gray-300 ml-2">{patient.size}</span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-gray-700 flex items-center justify-between">
                  <span className="text-xs text-gray-500">Klicken zum Untersuchen</span>
                  <ArrowRight className="w-5 h-5 text-cyan-400 group-hover:translate-x-1 transition-transform" />
                </div>
              </button>
            ))}
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={refreshPatients}
              className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg transition-colors inline-flex items-center gap-2"
            >
              <RefreshCw className="w-5 h-5" />
              Neue Patienten
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Render Examination (Minigames)
  if (gameState === 'examination' && currentPatient) {
    const completedTools = Object.keys(examinationData).length;

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
        {/* Header */}
        <div className="border-b border-cyan-800/50 bg-gray-900/80 backdrop-blur-xl">
          <div className="p-4 max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h2 className="text-2xl font-bold text-cyan-400">Untersuchung: {currentPatient.name}</h2>
                <p className="text-sm text-gray-400">{currentPatient.animalName} • {currentPatient.breed}</p>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-400">Durchgeführte Tests</div>
                <div className="text-2xl font-bold text-cyan-400">{completedTools} / 4</div>
              </div>
            </div>

            {/* Progress */}
            <div className="grid grid-cols-4 gap-2">
              {['stethoscope', 'xray', 'blood_test', 'palpation'].map(tool => (
                <div
                  key={tool}
                  className={`h-2 rounded-full transition-all ${
                    examinationData[tool] ? 'bg-green-500' : 'bg-gray-700'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Examination Tools */}
        <div className="p-8 max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Stethoscope */}
            {!examinationData.stethoscope && (
              <StethoscopeGame patient={currentPatient} onComplete={handleToolComplete} />
            )}

            {/* X-Ray */}
            {!examinationData.xray && completedTools >= 1 && (
              <XRayGame patient={currentPatient} onComplete={handleToolComplete} />
            )}

            {/* Blood Test */}
            {!examinationData.blood_test && completedTools >= 1 && (
              <BloodTestGame patient={currentPatient} onComplete={handleToolComplete} />
            )}

            {/* Palpation */}
            {!examinationData.palpation && completedTools >= 1 && (
              <PalpationGame patient={currentPatient} onComplete={handleToolComplete} />
            )}
          </div>

          {/* Proceed to Diagnosis */}
          {completedTools >= 2 && (
            <div className="bg-green-900/20 backdrop-blur-md rounded-xl p-6 border border-green-700/30">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-green-400 mb-1">Bereit für Diagnose!</h3>
                  <p className="text-sm text-gray-400">
                    Du hast genug Daten gesammelt. Stelle jetzt eine Diagnose!
                  </p>
                </div>
                <button
                  onClick={handleProceedToDiagnosis}
                  className="px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-bold rounded-lg transition-all flex items-center gap-2"
                >
                  Zur Diagnose
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}

          {completedTools < 2 && (
            <div className="bg-amber-900/20 backdrop-blur-md rounded-xl p-4 border border-amber-700/30 text-center">
              <p className="text-sm text-amber-400">
                💡 Tipp: Führe mindestens 2 Untersuchungen durch für eine fundierte Diagnose!
              </p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Render Diagnosis Selection
  if (gameState === 'diagnosis' && currentPatient) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
        {/* Header */}
        <div className="border-b border-cyan-800/50 bg-gray-900/80 backdrop-blur-xl">
          <div className="p-4 max-w-7xl mx-auto">
            <h2 className="text-2xl font-bold text-cyan-400">Diagnose für: {currentPatient.name}</h2>
            <p className="text-sm text-gray-400">Basierend auf deinen Untersuchungsergebnissen</p>
          </div>
        </div>

        {/* Diagnosis Selection */}
        <div className="p-8 max-w-6xl mx-auto">
          {/* Examination Summary */}
          <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30 mb-6">
            <h3 className="text-lg font-bold text-cyan-400 mb-4">Untersuchungsergebnisse</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(examinationData).map(([tool, data]) => (
                <div key={tool} className="bg-gray-800/50 p-4 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-gray-300">{tool.replace(/_/g, ' ').toUpperCase()}</span>
                    {data.correct !== undefined && (
                      data.correct ?
                        <CheckCircle className="w-5 h-5 text-green-400" /> :
                        <XCircle className="w-5 h-5 text-red-400" />
                    )}
                  </div>
                  <div className="text-sm text-gray-400">{data.result}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Diagnosis Options */}
          <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30 mb-6">
            <h3 className="text-lg font-bold text-cyan-400 mb-4">Wähle deine Diagnose</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {currentPatient.symptomSets?.map((symptomSet, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedDiagnosis({ id: symptomSet.id, name: symptomSet.diagnosis })}
                  className={`p-4 rounded-lg border text-left transition-all ${
                    selectedDiagnosis?.id === symptomSet.id
                      ? 'bg-cyan-900/30 border-cyan-500'
                      : 'bg-gray-800/50 border-gray-700 hover:border-cyan-600'
                  }`}
                >
                  <div className="font-medium text-cyan-300">{symptomSet.diagnosis}</div>
                  <div className="text-xs text-gray-400 mt-1">
                    Symptome: {symptomSet.symptoms.join(', ')}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Submit Diagnosis */}
          <button
            onClick={handleSubmitDiagnosis}
            disabled={!selectedDiagnosis}
            className={`w-full py-4 rounded-lg font-bold transition-all ${
              selectedDiagnosis
                ? 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white'
                : 'bg-gray-800 text-gray-500 cursor-not-allowed'
            }`}
          >
            Diagnose bestätigen
          </button>
        </div>
      </div>
    );
  }

  // Render Feedback
  if (gameState === 'feedback' && currentPatient) {
    const result = gameEngine.state.player.correctDiagnoses > 0; // Simplified check
    const feedback = {
      title: result ? '✅ Korrekte Diagnose!' : '❌ Falsche Diagnose',
      message: result ?
        `Ausgezeichnet! ${currentPatient.name} wird sich schnell erholen.` :
        `Die Diagnose war leider nicht korrekt. ${currentPatient.name} leidet an ${currentPatient.correctDiagnosis}.`,
      xpGained: result ? 75 : 15,
      educationalFact: currentPatient.education?.funFacts?.[0] || 'Interessanter Fakt über Tiere!'
    };

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center p-8">
        <div className="max-w-3xl w-full bg-gray-900/80 backdrop-blur-xl rounded-2xl p-8 border border-cyan-800/30">
          {/* Result */}
          <div className="text-center mb-8">
            {result ? (
              <CheckCircle className="w-24 h-24 text-green-400 mx-auto mb-4 animate-bounce" />
            ) : (
              <XCircle className="w-24 h-24 text-red-400 mx-auto mb-4" />
            )}
            <h2 className={`text-3xl font-bold mb-2 ${result ? 'text-green-400' : 'text-red-400'}`}>
              {feedback.title}
            </h2>
            <p className="text-gray-300 text-lg">{feedback.message}</p>
          </div>

          {/* XP Gained */}
          <div className="bg-cyan-900/20 p-6 rounded-lg border border-cyan-700/30 mb-6 text-center">
            <div className="text-sm text-gray-400 mb-2">Erfahrung gewonnen</div>
            <div className="text-4xl font-bold text-cyan-400">+{feedback.xpGained} XP</div>
          </div>

          {/* Educational Fact */}
          <div className="bg-purple-900/20 p-6 rounded-lg border border-purple-700/30 mb-6">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-purple-600/20 rounded-lg">
                <Lightbulb className="w-6 h-6 text-purple-400" />
              </div>
              <div>
                <div className="font-bold text-purple-400 mb-2">Wusstest du?</div>
                <p className="text-gray-300 text-sm">{feedback.educationalFact}</p>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-4">
            <button
              onClick={handleNextPatient}
              className="flex-1 py-4 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-lg transition-all"
            >
              Nächster Patient
            </button>
            <button
              onClick={handleReturnToMenu}
              className="px-6 py-4 bg-gray-800 hover:bg-gray-700 text-gray-300 font-bold rounded-lg transition-all"
            >
              Zum Menü
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default VetScanGamePro;
