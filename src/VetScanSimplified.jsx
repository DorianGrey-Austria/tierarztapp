import React, { useState, useEffect } from 'react';
import {
  Heart, Thermometer, Stethoscope, Award, Star, TrendingUp,
  CheckCircle, XCircle, Zap, Sparkles, ArrowRight, Trophy, Book
} from 'lucide-react';
import { getGameEngine } from './game/GameEngine';
import { generatePatients, getVitalSignsForAnimal } from './veterinary-medical-data';

/**
 * VetScan Simplified - Fun-First Game Design
 * Core Principle: Simple to start, progressively complex, always fun!
 */
const VetScanSimplified = () => {
  const [gameEngine] = useState(() => getGameEngine());
  const [playerLevel, setPlayerLevel] = useState(1);
  const [playerXP, setPlayerXP] = useState(0);
  const [xpToNextLevel, setXPToNextLevel] = useState(100);

  // Game state
  const [gamePhase, setGamePhase] = useState('intro'); // intro, examination, diagnosis, feedback, levelup
  const [currentPatient, setCurrentPatient] = useState(null);
  const [currentStep, setCurrentStep] = useState(0); // Which examination step (0 = start, 1 = heart, 2 = temp, etc.)
  const [examinationResults, setExaminationResults] = useState({});
  const [selectedDiagnosis, setSelectedDiagnosis] = useState(null);
  const [streak, setStreak] = useState(0);

  // Animation states
  const [showCelebration, setShowCelebration] = useState(false);
  const [showXPGain, setShowXPGain] = useState(null);
  const [animatingResult, setAnimatingResult] = useState(false);

  // Available patients (simplified)
  const [availablePatients, setAvailablePatients] = useState([]);

  // Tutorial state
  const [tutorialStep, setTutorialStep] = useState(0);
  const [showTutorialHint, setShowTutorialHint] = useState(true);

  useEffect(() => {
    loadNextPatient();
  }, []);

  const loadNextPatient = () => {
    const patients = generatePatients();
    const unlocked = patients.filter(p => ['dog', 'cat', 'mouse'].includes(p.animalType));
    const randomPatient = unlocked[Math.floor(Math.random() * Math.min(5, unlocked.length))];

    setCurrentPatient(randomPatient);
    setCurrentStep(0);
    setExaminationResults({});
    setSelectedDiagnosis(null);
    setGamePhase('intro');
  };

  // Simplified examination - ONE TOOL AT A TIME
  const performExamination = (toolType) => {
    setAnimatingResult(true);
    setShowTutorialHint(false);

    setTimeout(() => {
      const vitalSigns = getVitalSignsForAnimal(currentPatient.animalType);
      let result = {};

      if (toolType === 'heart') {
        const hr = currentPatient.vitalChanges?.heartRate ||
          (vitalSigns.heartRate.min + vitalSigns.heartRate.max) / 2;
        const isNormal = hr >= vitalSigns.heartRate.min && hr <= vitalSigns.heartRate.max;

        result = {
          tool: 'heart',
          value: Math.round(hr),
          unit: 'BPM',
          normalRange: `${vitalSigns.heartRate.min}-${vitalSigns.heartRate.max}`,
          isNormal,
          feedback: isNormal
            ? `✅ Normaler Herzschlag für ${currentPatient.animalName}`
            : `⚠️ Auffälliger Herzschlag für ${currentPatient.animalName}`
        };
      } else if (toolType === 'temperature') {
        const temp = currentPatient.vitalChanges?.temperature ||
          (vitalSigns.temperature.min + vitalSigns.temperature.max) / 2;
        const isNormal = temp >= vitalSigns.temperature.min && temp <= vitalSigns.temperature.max;

        result = {
          tool: 'temperature',
          value: temp.toFixed(1),
          unit: '°C',
          normalRange: `${vitalSigns.temperature.min}-${vitalSigns.temperature.max}`,
          isNormal,
          feedback: isNormal
            ? `✅ Normale Temperatur für ${currentPatient.animalName}`
            : temp > vitalSigns.temperature.max
            ? `🌡️ Fieber! Höher als normal für ${currentPatient.animalName}`
            : `❄️ Unterkühlt! Niedriger als normal`
        };
      }

      setExaminationResults({ ...examinationResults, [toolType]: result });
      setAnimatingResult(false);

      // Auto-advance after showing result
      setTimeout(() => {
        if (playerLevel <= 3) {
          // Early levels: automatically proceed to diagnosis
          setCurrentStep(prev => prev + 1);
          if (Object.keys(examinationResults).length >= 1) {
            proceedToDiagnosis();
          }
        } else {
          setCurrentStep(prev => prev + 1);
        }
      }, 2000);
    }, 1500);
  };

  const proceedToDiagnosis = () => {
    setGamePhase('diagnosis');
  };

  const submitDiagnosis = (diagnosis) => {
    setSelectedDiagnosis(diagnosis);

    // Check if correct
    const isCorrect = diagnosis.toLowerCase().includes(currentPatient.correctDiagnosis?.toLowerCase() ||
      currentPatient.symptoms?.[0]?.toLowerCase() || '');

    // Calculate XP
    const baseXP = 50;
    const streakBonus = streak > 0 ? streak * 10 : 0;
    const totalXP = baseXP + streakBonus;

    // Update streak
    if (isCorrect) {
      setStreak(streak + 1);
    } else {
      setStreak(0);
    }

    // Add XP with animation
    setShowXPGain({ amount: totalXP, isCorrect });
    setTimeout(() => {
      setPlayerXP(prevXP => {
        const newXP = prevXP + totalXP;
        if (newXP >= xpToNextLevel) {
          // Level up!
          setTimeout(() => {
            setGamePhase('levelup');
            setPlayerLevel(prev => prev + 1);
            setPlayerXP(newXP - xpToNextLevel);
            setXPToNextLevel(Math.floor(xpToNextLevel * 1.2));
          }, 1500);
        }
        return newXP;
      });
      setShowXPGain(null);
    }, 1000);

    // Show celebration if correct
    if (isCorrect) {
      setShowCelebration(true);
      setTimeout(() => setShowCelebration(false), 2000);
    }

    setGamePhase('feedback');
  };

  const handleNextPatient = () => {
    loadNextPatient();
    if (tutorialStep < 5) {
      setTutorialStep(prev => prev + 1);
    }
  };

  // INTRO PHASE - Show patient
  if (gamePhase === 'intro' && currentPatient) {
    const tutorialHints = [
      "🎯 Dein erster Patient! Klicke auf das Herz-Symbol um den Herzschlag zu prüfen.",
      "💡 Gut! Jetzt prüfe die Temperatur mit dem Thermometer.",
      "🎓 Super! Du lernst schnell. Untersuche den Patienten.",
      "✨ Du bist schon ein Profi! Weiter so!",
      "🚀 Jetzt kannst du selbst entscheiden, welche Tests du machst!"
    ];

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 p-4">
        {/* Celebration Overlay */}
        {showCelebration && (
          <div className="fixed inset-0 pointer-events-none z-50 flex items-center justify-center">
            <div className="text-9xl animate-bounce">🎉</div>
            <div className="absolute text-6xl animate-ping text-yellow-400">⭐</div>
          </div>
        )}

        {/* XP Gain Animation */}
        {showXPGain && (
          <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 animate-scaleUp">
            <div className={`text-6xl font-bold ${showXPGain.isCorrect ? 'text-green-400' : 'text-yellow-400'}`}>
              +{showXPGain.amount} XP
            </div>
          </div>
        )}

        {/* Top Bar */}
        <div className="max-w-4xl mx-auto mb-6">
          <div className="bg-gray-900/80 backdrop-blur-xl rounded-xl p-4 border border-cyan-800/30">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <Trophy className="w-6 h-6 text-yellow-500" />
                  <span className="text-2xl font-bold text-cyan-400">Level {playerLevel}</span>
                </div>
                {streak > 0 && (
                  <div className="flex items-center gap-1 bg-orange-900/30 px-3 py-1 rounded-full border border-orange-700/50">
                    <Zap className="w-4 h-4 text-orange-400" />
                    <span className="text-sm font-bold text-orange-400">{streak} Streak!</span>
                  </div>
                )}
              </div>
            </div>

            {/* XP Bar */}
            <div className="relative">
              <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-600 to-blue-500 transition-all duration-1000 ease-out"
                  style={{ width: `${(playerXP / xpToNextLevel) * 100}%` }}
                />
              </div>
              <div className="text-right text-xs text-gray-400 mt-1">
                {playerXP} / {xpToNextLevel} XP
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {/* Tutorial Hint */}
          {showTutorialHint && tutorialStep < tutorialHints.length && (
            <div className="bg-purple-900/30 backdrop-blur-md rounded-xl p-4 border border-purple-700/50 mb-6 animate-float">
              <div className="flex items-start gap-3">
                <Sparkles className="w-6 h-6 text-purple-400 flex-shrink-0 mt-1" />
                <p className="text-purple-200">{tutorialHints[tutorialStep]}</p>
              </div>
            </div>
          )}

          {/* Patient Card */}
          <div className="bg-gray-900/80 backdrop-blur-xl rounded-2xl p-8 border border-cyan-800/30 mb-6">
            <div className="text-center mb-6">
              <div className="text-8xl mb-4 animate-float">
                {currentPatient.icon || '🐕'}
              </div>
              <h2 className="text-4xl font-bold text-cyan-400 mb-2">
                {currentPatient.name}
              </h2>
              <p className="text-xl text-gray-400">
                {currentPatient.animalName} • {currentPatient.breed}
              </p>
            </div>

            {/* Symptoms */}
            <div className="bg-red-900/20 backdrop-blur-sm rounded-xl p-6 border border-red-700/30">
              <h3 className="text-lg font-bold text-red-400 mb-3 flex items-center gap-2">
                💬 Was der Besitzer sagt:
              </h3>
              <div className="space-y-2">
                {currentPatient.symptoms?.slice(0, 3).map((symptom, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-gray-200">
                    <div className="w-2 h-2 rounded-full bg-red-500"></div>
                    <span>{symptom}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Examination Tools - SIMPLIFIED */}
          <div className="bg-gray-900/80 backdrop-blur-xl rounded-2xl p-8 border border-cyan-800/30">
            <h3 className="text-2xl font-bold text-cyan-400 mb-6 text-center">
              🔬 Untersuchung
            </h3>

            <div className="grid grid-cols-2 gap-6">
              {/* Heart Examination */}
              <button
                onClick={() => performExamination('heart')}
                disabled={animatingResult || examinationResults.heart}
                className={`relative p-8 rounded-2xl border-2 transition-all transform hover:scale-105 ${
                  examinationResults.heart
                    ? 'bg-green-900/30 border-green-600 cursor-not-allowed'
                    : animatingResult
                    ? 'bg-cyan-900/30 border-cyan-500 cursor-wait'
                    : 'bg-gray-800/50 border-cyan-700 hover:border-cyan-500 hover:bg-cyan-900/20 cursor-pointer'
                }`}
              >
                <div className="text-center">
                  <Heart className={`w-20 h-20 mx-auto mb-4 ${
                    animatingResult ? 'animate-heartbeat text-red-500' : 'text-cyan-400'
                  }`} />
                  <div className="text-2xl font-bold text-white mb-2">Herz</div>
                  {examinationResults.heart ? (
                    <div className="mt-4 animate-scaleUp">
                      <div className="text-3xl font-bold text-green-400 mb-2">
                        {examinationResults.heart.value} {examinationResults.heart.unit}
                      </div>
                      <div className="text-sm text-gray-400">
                        Normal: {examinationResults.heart.normalRange}
                      </div>
                      <div className="mt-2 text-sm font-medium">
                        {examinationResults.heart.feedback}
                      </div>
                    </div>
                  ) : animatingResult ? (
                    <div className="text-cyan-400 animate-pulse">Messe...</div>
                  ) : (
                    <div className="text-gray-400">Klicken zum Prüfen</div>
                  )}
                </div>
              </button>

              {/* Temperature Examination */}
              <button
                onClick={() => performExamination('temperature')}
                disabled={animatingResult || examinationResults.temperature || (playerLevel < 2 && !examinationResults.heart)}
                className={`relative p-8 rounded-2xl border-2 transition-all transform hover:scale-105 ${
                  examinationResults.temperature
                    ? 'bg-green-900/30 border-green-600 cursor-not-allowed'
                    : playerLevel < 2 && !examinationResults.heart
                    ? 'bg-gray-800/20 border-gray-700 opacity-50 cursor-not-allowed'
                    : animatingResult
                    ? 'bg-amber-900/30 border-amber-500 cursor-wait'
                    : 'bg-gray-800/50 border-amber-700 hover:border-amber-500 hover:bg-amber-900/20 cursor-pointer'
                }`}
              >
                {playerLevel < 2 && !examinationResults.heart && (
                  <div className="absolute top-2 right-2 bg-gray-700 text-white text-xs px-2 py-1 rounded-full">
                    Zuerst Herz
                  </div>
                )}
                <div className="text-center">
                  <Thermometer className={`w-20 h-20 mx-auto mb-4 ${
                    animatingResult ? 'animate-pulse text-orange-500' : 'text-amber-400'
                  }`} />
                  <div className="text-2xl font-bold text-white mb-2">Temperatur</div>
                  {examinationResults.temperature ? (
                    <div className="mt-4 animate-scaleUp">
                      <div className="text-3xl font-bold text-green-400 mb-2">
                        {examinationResults.temperature.value} {examinationResults.temperature.unit}
                      </div>
                      <div className="text-sm text-gray-400">
                        Normal: {examinationResults.temperature.normalRange}
                      </div>
                      <div className="mt-2 text-sm font-medium">
                        {examinationResults.temperature.feedback}
                      </div>
                    </div>
                  ) : animatingResult ? (
                    <div className="text-amber-400 animate-pulse">Messe...</div>
                  ) : (
                    <div className="text-gray-400">Klicken zum Prüfen</div>
                  )}
                </div>
              </button>
            </div>

            {/* Proceed to Diagnosis Button */}
            {Object.keys(examinationResults).length > 0 && (
              <div className="mt-8 text-center">
                <button
                  onClick={proceedToDiagnosis}
                  className="px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white text-xl font-bold rounded-xl transition-all transform hover:scale-105 flex items-center gap-3 mx-auto shadow-lg"
                >
                  <span>Diagnose stellen</span>
                  <ArrowRight className="w-6 h-6" />
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // DIAGNOSIS PHASE
  if (gamePhase === 'diagnosis' && currentPatient) {
    // Simplified diagnosis options based on common symptoms
    const diagnosisOptions = [
      { id: 'respiratory', name: 'Atemwegsinfektion', symptoms: ['husten', 'schnupfen', 'atemnot'] },
      { id: 'fever', name: 'Fieber/Infektion', symptoms: ['fieber', 'müde', 'warm'] },
      { id: 'digestive', name: 'Magen-Darm-Problem', symptoms: ['erbrechen', 'durchfall', 'bauch'] },
      { id: 'injury', name: 'Verletzung', symptoms: ['lahmheit', 'schmerz', 'schwellung'] },
      { id: 'healthy', name: 'Gesund / Routine-Check', symptoms: [] }
    ];

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 p-4 flex items-center justify-center">
        <div className="max-w-3xl w-full">
          <div className="bg-gray-900/80 backdrop-blur-xl rounded-2xl p-8 border border-cyan-800/30">
            <h2 className="text-3xl font-bold text-cyan-400 mb-6 text-center">
              🎯 Was ist deine Diagnose?
            </h2>

            {/* Show examination summary */}
            <div className="bg-gray-800/50 rounded-xl p-6 mb-6">
              <h3 className="text-lg font-bold text-gray-300 mb-4">Deine Befunde:</h3>
              <div className="space-y-2">
                {Object.values(examinationResults).map((result, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <span className="text-gray-400">
                      {result.tool === 'heart' ? '❤️ Herzfrequenz' : '🌡️ Temperatur'}:
                    </span>
                    <span className={`font-bold ${result.isNormal ? 'text-green-400' : 'text-yellow-400'}`}>
                      {result.value} {result.unit}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Diagnosis Options */}
            <div className="space-y-3">
              {diagnosisOptions.map((option) => (
                <button
                  key={option.id}
                  onClick={() => submitDiagnosis(option.name)}
                  className="w-full p-6 bg-gray-800/50 hover:bg-cyan-900/30 border-2 border-gray-700 hover:border-cyan-500 rounded-xl transition-all text-left transform hover:scale-102"
                >
                  <div className="text-xl font-bold text-white">{option.name}</div>
                </button>
              ))}
            </div>

            {playerLevel <= 2 && (
              <div className="mt-6 bg-purple-900/20 rounded-xl p-4 border border-purple-700/30">
                <div className="flex items-start gap-2">
                  <Sparkles className="w-5 h-5 text-purple-400 flex-shrink-0 mt-1" />
                  <p className="text-sm text-purple-200">
                    💡 Tipp: Schau dir die Symptome und deine Messwerte an. Was passt am besten zusammen?
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // FEEDBACK PHASE
  if (gamePhase === 'feedback' && currentPatient && selectedDiagnosis) {
    const actualDiagnosis = currentPatient.correctDiagnosis || currentPatient.symptoms?.[0] || 'Unbekannt';
    const isCorrect = selectedDiagnosis.toLowerCase().includes(actualDiagnosis.toLowerCase());

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 p-4 flex items-center justify-center">
        <div className="max-w-3xl w-full">
          <div className={`bg-gray-900/80 backdrop-blur-xl rounded-2xl p-8 border-2 ${
            isCorrect ? 'border-green-600' : 'border-yellow-600'
          }`}>
            {/* Result */}
            <div className="text-center mb-8">
              {isCorrect ? (
                <>
                  <CheckCircle className="w-32 h-32 text-green-400 mx-auto mb-4 animate-bounce" />
                  <h2 className="text-4xl font-bold text-green-400 mb-2">Richtig! 🎉</h2>
                  <p className="text-xl text-gray-300">Toll gemacht!</p>
                </>
              ) : (
                <>
                  <div className="text-8xl mb-4">🤔</div>
                  <h2 className="text-4xl font-bold text-yellow-400 mb-2">Nicht ganz!</h2>
                  <p className="text-xl text-gray-300">Aber gut versucht! Hier ist, was es wirklich war:</p>
                </>
              )}
            </div>

            {/* Explanation */}
            {!isCorrect && (
              <div className="bg-blue-900/20 rounded-xl p-6 border border-blue-700/30 mb-6">
                <h3 className="text-lg font-bold text-blue-400 mb-3">💡 Lerne daraus:</h3>
                <div className="space-y-2 text-gray-300">
                  <p><strong>Deine Diagnose:</strong> {selectedDiagnosis}</p>
                  <p><strong>Richtig wäre:</strong> {actualDiagnosis}</p>
                  <p className="text-sm text-gray-400 mt-4">
                    Tipp: Achte auf die Kombination der Symptome. Beim nächsten Mal klappt's besser!
                  </p>
                </div>
              </div>
            )}

            {/* Fun Fact */}
            <div className="bg-purple-900/20 rounded-xl p-6 border border-purple-700/30 mb-6">
              <h3 className="text-lg font-bold text-purple-400 mb-3">📚 Wusstest du?</h3>
              <p className="text-gray-300">
                {currentPatient.education?.funFacts?.[Math.floor(Math.random() * currentPatient.education.funFacts.length)] ||
                 `${currentPatient.animalName} sind faszinierende Tiere!`}
              </p>
            </div>

            {/* Next Button */}
            <button
              onClick={handleNextPatient}
              className="w-full py-4 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xl font-bold rounded-xl transition-all transform hover:scale-105"
            >
              Nächster Patient →
            </button>
          </div>
        </div>
      </div>
    );
  }

  // LEVEL UP PHASE
  if (gamePhase === 'levelup') {
    return (
      <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div className="max-w-2xl w-full bg-gradient-to-br from-yellow-900/40 to-orange-900/40 backdrop-blur-xl rounded-2xl p-8 border-2 border-yellow-600 animate-scaleUp">
          <div className="text-center">
            <Trophy className="w-32 h-32 text-yellow-400 mx-auto mb-4 animate-bounce" />
            <h2 className="text-6xl font-bold text-yellow-400 mb-4">LEVEL UP!</h2>
            <div className="text-4xl font-bold text-white mb-8">Level {playerLevel}</div>

            {/* Unlocks */}
            <div className="bg-gray-900/50 rounded-xl p-6 mb-6">
              <h3 className="text-xl font-bold text-cyan-400 mb-4">🎉 Neue Freischaltungen:</h3>
              <div className="space-y-2 text-gray-300">
                {playerLevel === 2 && <p>✨ Thermometer freigeschaltet!</p>}
                {playerLevel === 3 && <p>✨ Neue Tierarten verfügbar!</p>}
                {playerLevel === 5 && <p>✨ Röntgengerät freigeschaltet!</p>}
                {playerLevel === 10 && <p>✨ Notfall-Modus freigeschaltet!</p>}
              </div>
            </div>

            <button
              onClick={handleNextPatient}
              className="w-full py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white text-xl font-bold rounded-xl transition-all"
            >
              Weiter spielen! 🚀
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default VetScanSimplified;
