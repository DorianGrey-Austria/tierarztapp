import React, { useState, useEffect } from 'react';
import { Book, ArrowRight, CheckCircle, Lightbulb, Target, Award } from 'lucide-react';

/**
 * Tutorial System - Guides new players through the game mechanics
 */
export const TutorialSystem = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [completed, setCompleted] = useState(false);

  const tutorialSteps = [
    {
      id: 'welcome',
      title: 'Willkommen bei VetScan Pro! 🎓',
      icon: <Book className="w-12 h-12 text-cyan-400" />,
      content: (
        <div className="space-y-4">
          <p className="text-lg">
            Herzlich willkommen in deiner neuen Tierarztpraxis!
          </p>
          <p>
            Du bist ein frischgebackener Tierarzt und wirst lernen, verschiedene Tiere zu untersuchen,
            Diagnosen zu stellen und Behandlungen durchzuführen.
          </p>
          <div className="bg-cyan-900/20 p-4 rounded-lg border border-cyan-700/30">
            <p className="font-bold text-cyan-400 mb-2">🎯 Deine Ziele:</p>
            <ul className="space-y-1 text-sm text-gray-300">
              <li>• Lerne verschiedene Tierarten kennen</li>
              <li>• Meistere diagnostische Werkzeuge</li>
              <li>• Stelle korrekte Diagnosen</li>
              <li>• Sammle Erfahrungspunkte (XP)</li>
              <li>• Schalte neue Tiere und Ausrüstung frei</li>
            </ul>
          </div>
        </div>
      )
    },
    {
      id: 'patient_intro',
      title: 'Dein erster Patient 🐕',
      icon: <Target className="w-12 h-12 text-cyan-400" />,
      content: (
        <div className="space-y-4">
          <p className="text-lg">
            Lerne, wie du Patienten untersuchst!
          </p>
          <div className="bg-gray-800/50 p-4 rounded-lg">
            <h4 className="font-bold text-cyan-400 mb-2">Der Untersuchungsablauf:</h4>
            <ol className="space-y-2 text-sm">
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">1.</span>
                <span><strong>Anamnese:</strong> Höre dem Besitzer zu und notiere Symptome</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">2.</span>
                <span><strong>Untersuchung:</strong> Nutze verschiedene diagnostische Tools</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">3.</span>
                <span><strong>Diagnose:</strong> Wähle die passende Krankheit aus</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">4.</span>
                <span><strong>Behandlung:</strong> Empfehle die richtige Therapie</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">5.</span>
                <span><strong>Feedback:</strong> Lerne aus deinen Entscheidungen</span>
              </li>
            </ol>
          </div>
          <div className="bg-amber-900/20 p-3 rounded border border-amber-700/30">
            <p className="text-sm"><strong>💡 Tipp:</strong> Je gründlicher deine Untersuchung,
            desto mehr XP erhältst du!</p>
          </div>
        </div>
      )
    },
    {
      id: 'tools_intro',
      title: 'Diagnostische Werkzeuge 🔬',
      icon: <Lightbulb className="w-12 h-12 text-cyan-400" />,
      content: (
        <div className="space-y-4">
          <p className="text-lg">
            Diese Tools helfen dir bei der Diagnose:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="bg-gray-800/50 p-3 rounded-lg border border-cyan-700/30">
              <div className="font-bold text-cyan-400 mb-1">❤️ Stethoskop</div>
              <p className="text-sm text-gray-300">
                Höre Herzgeräusche ab und erkenne Unregelmäßigkeiten
              </p>
            </div>
            <div className="bg-gray-800/50 p-3 rounded-lg border border-cyan-700/30">
              <div className="font-bold text-cyan-400 mb-1">🔍 Röntgen</div>
              <p className="text-sm text-gray-300">
                Finde Knochenbrüche und innere Probleme
              </p>
            </div>
            <div className="bg-gray-800/50 p-3 rounded-lg border border-cyan-700/30">
              <div className="font-bold text-cyan-400 mb-1">💉 Bluttest</div>
              <p className="text-sm text-gray-300">
                Analysiere Blutwerte und erkenne Anomalien
              </p>
            </div>
            <div className="bg-gray-800/50 p-3 rounded-lg border border-cyan-700/30">
              <div className="font-bold text-cyan-400 mb-1">👐 Abtasten</div>
              <p className="text-sm text-gray-300">
                Finde Schmerzpunkte und Schwellungen
              </p>
            </div>
          </div>
          <div className="bg-cyan-900/20 p-3 rounded border border-cyan-700/30">
            <p className="text-sm"><strong>⚡ Wichtig:</strong> Jedes Tool liefert wichtige Informationen.
            Nutze mehrere Tools für eine gründliche Diagnose!</p>
          </div>
        </div>
      )
    },
    {
      id: 'progression',
      title: 'Fortschritt & Belohnungen 🏆',
      icon: <Award className="w-12 h-12 text-cyan-400" />,
      content: (
        <div className="space-y-4">
          <p className="text-lg">
            Entwickle deine Karriere und schalte neue Inhalte frei!
          </p>
          <div className="space-y-3">
            <div className="bg-gradient-to-r from-cyan-900/30 to-blue-900/30 p-4 rounded-lg border border-cyan-700/30">
              <div className="font-bold text-cyan-400 mb-2">📊 Erfahrungspunkte (XP)</div>
              <p className="text-sm text-gray-300">
                Sammle XP durch korrekte Diagnosen, gründliche Untersuchungen und schnelle Behandlungen.
              </p>
            </div>
            <div className="bg-gradient-to-r from-purple-900/30 to-pink-900/30 p-4 rounded-lg border border-purple-700/30">
              <div className="font-bold text-purple-400 mb-2">⬆️ Level-System</div>
              <p className="text-sm text-gray-300">
                Steige von Praktikant zum Chefarzt auf. Jedes Level schaltet neue Tiere und Ausrüstung frei!
              </p>
            </div>
            <div className="bg-gradient-to-r from-green-900/30 to-emerald-900/30 p-4 rounded-lg border border-green-700/30">
              <div className="font-bold text-green-400 mb-2">🏅 Achievements</div>
              <p className="text-sm text-gray-300">
                Erfülle besondere Herausforderungen und sammle Auszeichnungen.
              </p>
            </div>
          </div>
          <div className="bg-amber-900/20 p-3 rounded border border-amber-700/30">
            <p className="text-sm"><strong>💎 Freischaltungen:</strong> Du startest mit 5 grundlegenden
            Tierarten. Schalte durch Levelaufstiege 15 weitere frei!</p>
          </div>
        </div>
      )
    },
    {
      id: 'gameplay_modes',
      title: 'Spielmodi 🎮',
      icon: <Target className="w-12 h-12 text-cyan-400" />,
      content: (
        <div className="space-y-4">
          <p className="text-lg">
            Wähle deinen Spielmodus:
          </p>
          <div className="space-y-3">
            <div className="bg-gray-800/50 p-4 rounded-lg border-l-4 border-cyan-500">
              <div className="font-bold text-cyan-400 mb-1">🎓 Übungsmodus</div>
              <p className="text-sm text-gray-300">
                Nimm dir Zeit, lerne die Werkzeuge kennen und experimentiere ohne Zeitdruck.
              </p>
            </div>
            <div className="bg-gray-800/50 p-4 rounded-lg border-l-4 border-purple-500 opacity-60">
              <div className="font-bold text-purple-400 mb-1">📖 Kampagne (Level 5+)</div>
              <p className="text-sm text-gray-300">
                Folge einer Geschichte, behandle verschiedene Fälle und meistere Herausforderungen.
              </p>
            </div>
            <div className="bg-gray-800/50 p-4 rounded-lg border-l-4 border-red-500 opacity-60">
              <div className="font-bold text-red-400 mb-1">🚨 Notfall-Modus (Level 10+)</div>
              <p className="text-sm text-gray-300">
                Kritische Fälle mit Zeitdruck - teste deine Fähigkeiten unter Stress!
              </p>
            </div>
            <div className="bg-gray-800/50 p-4 rounded-lg border-l-4 border-amber-500 opacity-60">
              <div className="font-bold text-amber-400 mb-1">⏱️ Zeitrennen (Level 20+)</div>
              <p className="text-sm text-gray-300">
                Behandle so viele Patienten wie möglich in begrenzter Zeit.
              </p>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'ready',
      title: 'Bereit für den Start! 🚀',
      icon: <CheckCircle className="w-12 h-12 text-green-400" />,
      content: (
        <div className="space-y-4">
          <p className="text-lg">
            Du bist jetzt bereit, deine Tierarzt-Karriere zu starten!
          </p>
          <div className="bg-green-900/20 p-4 rounded-lg border border-green-700/30">
            <h4 className="font-bold text-green-400 mb-3">📋 Zusammenfassung:</h4>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>✅ Untersuche Patienten gründlich mit allen verfügbaren Tools</li>
              <li>✅ Stelle die richtige Diagnose basierend auf Symptomen und Tests</li>
              <li>✅ Sammle XP und steige in Levels auf</li>
              <li>✅ Schalte neue Tierarten, Ausrüstung und Modi frei</li>
              <li>✅ Lerne aus deinen Fehlern durch detailliertes Feedback</li>
            </ul>
          </div>
          <div className="bg-cyan-900/20 p-4 rounded-lg border border-cyan-700/30 text-center">
            <p className="font-bold text-cyan-400 mb-2">🎁 Tutorial-Bonus</p>
            <p className="text-sm text-gray-300">
              Für das Abschließen des Tutorials erhältst du:
            </p>
            <div className="mt-2 flex items-center justify-center gap-4 text-lg font-bold">
              <span className="text-yellow-400">+100 XP</span>
              <span className="text-gray-400">•</span>
              <span className="text-blue-400">+50 Münzen</span>
            </div>
          </div>
          <div className="bg-amber-900/20 p-3 rounded border border-amber-700/30">
            <p className="text-sm text-center">
              <strong>💡 Tipp:</strong> Du kannst das Tutorial jederzeit in den Einstellungen erneut ansehen!
            </p>
          </div>
        </div>
      )
    }
  ];

  const currentTutorialStep = tutorialSteps[currentStep];

  const handleNext = () => {
    if (currentStep < tutorialSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setCompleted(true);
      setTimeout(() => {
        onComplete({
          xpGained: 100,
          coinsGained: 50,
          tutorialCompleted: true
        });
      }, 500);
    }
  };

  const handleSkip = () => {
    onComplete({
      xpGained: 0,
      coinsGained: 0,
      tutorialCompleted: true,
      skipped: true
    });
  };

  if (completed) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center p-8">
        <div className="max-w-2xl w-full bg-gray-900/80 backdrop-blur-xl rounded-2xl p-8 border border-green-800/30 text-center">
          <div className="mb-6">
            <CheckCircle className="w-24 h-24 text-green-400 mx-auto mb-4 animate-bounce" />
            <h2 className="text-3xl font-bold text-green-400 mb-2">Tutorial abgeschlossen!</h2>
            <p className="text-gray-300">Du erhältst:</p>
          </div>
          <div className="flex items-center justify-center gap-6 text-2xl font-bold mb-8">
            <div className="bg-yellow-900/30 px-6 py-3 rounded-lg border border-yellow-700/30">
              <span className="text-yellow-400">+100 XP</span>
            </div>
            <div className="bg-blue-900/30 px-6 py-3 rounded-lg border border-blue-700/30">
              <span className="text-blue-400">+50 Münzen</span>
            </div>
          </div>
          <div className="animate-pulse text-gray-400">
            Starte deine Karriere...
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full bg-gray-900/80 backdrop-blur-xl rounded-2xl border border-cyan-800/30 overflow-hidden">
        {/* Progress Bar */}
        <div className="h-2 bg-gray-800">
          <div
            className="h-full bg-gradient-to-r from-cyan-600 to-blue-500 transition-all duration-300"
            style={{ width: `${((currentStep + 1) / tutorialSteps.length) * 100}%` }}
          />
        </div>

        {/* Content */}
        <div className="p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-cyan-900/30 rounded-lg">
                {currentTutorialStep.icon}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-cyan-400">
                  {currentTutorialStep.title}
                </h2>
                <p className="text-sm text-gray-400">
                  Schritt {currentStep + 1} von {tutorialSteps.length}
                </p>
              </div>
            </div>
            <button
              onClick={handleSkip}
              className="text-sm text-gray-500 hover:text-gray-300 transition-colors"
            >
              Tutorial überspringen
            </button>
          </div>

          {/* Step Content */}
          <div className="mb-8 text-gray-300">
            {currentTutorialStep.content}
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between">
            <div className="flex gap-2">
              {tutorialSteps.map((_, idx) => (
                <div
                  key={idx}
                  className={`w-3 h-3 rounded-full transition-all ${
                    idx === currentStep
                      ? 'bg-cyan-400 w-8'
                      : idx < currentStep
                      ? 'bg-green-500'
                      : 'bg-gray-700'
                  }`}
                />
              ))}
            </div>

            <button
              onClick={handleNext}
              className="px-6 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-lg transition-all flex items-center gap-2"
            >
              {currentStep === tutorialSteps.length - 1 ? 'Jetzt starten!' : 'Weiter'}
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TutorialSystem;
