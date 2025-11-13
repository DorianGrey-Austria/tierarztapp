import React, { useState, useEffect } from 'react';
import { Activity, Heart, Lightbulb, Search, Zap, Target, CheckCircle, XCircle, Info, AlertCircle } from 'lucide-react';
import { getVitalSignsForAnimal } from '../veterinary-medical-data';

/**
 * Educational Popup Component
 */
const EducationalPopup = ({ title, content, type = 'info', onClose }) => {
  const colors = {
    info: 'from-blue-900/40 to-cyan-900/40 border-blue-700/30',
    tip: 'from-purple-900/40 to-pink-900/40 border-purple-700/30',
    warning: 'from-amber-900/40 to-orange-900/40 border-amber-700/30',
    success: 'from-green-900/40 to-emerald-900/40 border-green-700/30'
  };

  const icons = {
    info: <Info className="w-6 h-6 text-blue-400" />,
    tip: <Lightbulb className="w-6 h-6 text-purple-400" />,
    warning: <AlertCircle className="w-6 h-6 text-amber-400" />,
    success: <CheckCircle className="w-6 h-6 text-green-400" />
  };

  return (
    <div className={`bg-gradient-to-br ${colors[type]} p-4 rounded-lg border mb-4 animate-float`}>
      <div className="flex items-start gap-3">
        <div className="p-2 bg-gray-900/50 rounded-lg">
          {icons[type]}
        </div>
        <div className="flex-1">
          <div className="font-bold text-white mb-1">{title}</div>
          <div className="text-sm text-gray-300">{content}</div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-300 transition-colors"
          >
            <XCircle className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
};

/**
 * Enhanced Stethoscope Game with Real Data
 */
export const EnhancedStethoscopeGame = ({ patient, onComplete }) => {
  const [listening, setListening] = useState(false);
  const [heartbeat, setHeartbeat] = useState(null);
  const [actualHeartRate, setActualHeartRate] = useState(0);
  const [timeLeft, setTimeLeft] = useState(20);
  const [selectedDiagnosis, setSelectedDiagnosis] = useState(null);
  const [showEducation, setShowEducation] = useState(true);

  // Get real vital signs for this animal
  const vitalSigns = getVitalSignsForAnimal(patient.animalType);
  const normalHeartRate = vitalSigns?.heartRate || { min: 60, max: 120 };

  const heartSounds = {
    normal: { rate: 'normal', rhythm: 'regular', murmur: false, label: 'Normal', bpm: 0 },
    tachycardia: { rate: 'fast', rhythm: 'regular', murmur: false, label: 'Tachykardie (zu schnell)', bpm: 0 },
    bradycardia: { rate: 'slow', rhythm: 'regular', murmur: false, label: 'Bradykardie (zu langsam)', bpm: 0 },
    arrhythmia: { rate: 'normal', rhythm: 'irregular', murmur: false, label: 'Arrhythmie (unregelmäßig)', bpm: 0 },
    murmur: { rate: 'normal', rhythm: 'regular', murmur: true, label: 'Herzgeräusch', bpm: 0 }
  };

  useEffect(() => {
    if (listening && timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [listening, timeLeft]);

  useEffect(() => {
    // Use REAL vital changes from patient
    const vitalChanges = patient.vitalChanges || {};
    const patientHeartRate = vitalChanges.heartRate ||
      (normalHeartRate.min + normalHeartRate.max) / 2;

    setActualHeartRate(Math.round(patientHeartRate));

    // Determine heart sound based on REAL data
    if (patientHeartRate > normalHeartRate.max * 1.2) {
      setHeartbeat({ ...heartSounds.tachycardia, bpm: patientHeartRate });
    } else if (patientHeartRate < normalHeartRate.min * 0.8) {
      setHeartbeat({ ...heartSounds.bradycardia, bpm: patientHeartRate });
    } else if (patient.symptoms?.some(s => s.toLowerCase().includes('herz') || s.toLowerCase().includes('heart'))) {
      setHeartbeat({ ...heartSounds.murmur, bpm: patientHeartRate });
    } else if (patient.symptoms?.some(s => s.toLowerCase().includes('unregelmäßig') || s.toLowerCase().includes('irregular'))) {
      setHeartbeat({ ...heartSounds.arrhythmia, bpm: patientHeartRate });
    } else {
      setHeartbeat({ ...heartSounds.normal, bpm: patientHeartRate });
    }
  }, [patient]);

  const handleListen = () => {
    setListening(true);
    setShowEducation(false);
  };

  const handleSubmit = () => {
    const correct = selectedDiagnosis === heartbeat.label;
    const accuracy = correct ? 100 : 0;

    onComplete({
      tool: 'stethoscope',
      result: `${selectedDiagnosis} (Tatsächlich: ${heartbeat.label})`,
      correct,
      accuracy,
      thoroughness: 0.9,
      data: {
        heartSound: heartbeat.label,
        actualBPM: actualHeartRate,
        normalRange: `${normalHeartRate.min}-${normalHeartRate.max} BPM`,
        animalType: patient.animalName
      },
      educationalContent: {
        fact: `Bei ${patient.animalName} liegt die normale Herzfrequenz zwischen ${normalHeartRate.min} und ${normalHeartRate.max} Schlägen pro Minute.`,
        explanation: correct
          ? `Richtig! Du hast ${heartbeat.label} korrekt identifiziert. Die Herzfrequenz von ${actualHeartRate} BPM ${
              actualHeartRate >= normalHeartRate.min && actualHeartRate <= normalHeartRate.max
                ? 'liegt im Normalbereich'
                : 'liegt außerhalb des Normalbereichs'
            }.`
          : `Das war leider nicht korrekt. Die richtige Diagnose wäre ${heartbeat.label} gewesen. Die Herzfrequenz von ${actualHeartRate} BPM deutet darauf hin.`
      }
    });
  };

  return (
    <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-cyan-400">
        <Heart className="w-6 h-6" />
        Stethoskop - Herzuntersuchung
      </h3>

      {showEducation && (
        <EducationalPopup
          type="info"
          title={`💓 Normale Herzfrequenz für ${patient.animalName}`}
          content={`Die normale Herzfrequenz liegt bei ${normalHeartRate.min}-${normalHeartRate.max} BPM. Kleinere Tiere haben meist schnellere Herzschläge als größere Tiere.`}
          onClose={() => setShowEducation(false)}
        />
      )}

      <div className="space-y-4">
        {/* Animal Info */}
        <div className="bg-cyan-900/20 p-3 rounded-lg border border-cyan-700/30">
          <div className="text-sm text-gray-300">
            <div className="flex justify-between mb-2">
              <span>Patient:</span>
              <span className="font-bold text-cyan-400">{patient.name} ({patient.animalName})</span>
            </div>
            <div className="flex justify-between">
              <span>Normalbereich:</span>
              <span className="font-bold text-cyan-400">{normalHeartRate.min}-{normalHeartRate.max} BPM</span>
            </div>
          </div>
        </div>

        {/* Listening Animation */}
        <div className="relative h-40 bg-gray-800/50 rounded-lg flex items-center justify-center">
          {!listening ? (
            <button
              onClick={handleListen}
              className="px-6 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-lg transition-all flex items-center gap-2"
            >
              <Heart className="w-5 h-5" />
              Herz abhören
            </button>
          ) : (
            <div className="text-center">
              <div className={`w-32 h-32 mx-auto mb-4 rounded-full border-4 border-cyan-400 flex items-center justify-center ${
                heartbeat?.rate === 'fast' ? 'animate-pulse-fast' :
                heartbeat?.rate === 'slow' ? 'animate-pulse-slow' :
                'animate-heartbeat'
              }`}>
                <Heart className={`w-16 h-16 text-red-500 ${
                  heartbeat?.rhythm === 'irregular' ? 'animate-bounce' : ''
                }`} />
              </div>
              <div className="text-cyan-400 font-mono text-lg font-bold mb-2">
                {actualHeartRate} BPM
              </div>
              <div className="text-gray-400 font-mono text-sm">
                {heartbeat?.rate === 'fast' ? 'LUB-DUB-LUB-DUB-LUB-DUB' :
                 heartbeat?.rate === 'slow' ? 'LUB ... DUB ... LUB ... DUB' :
                 heartbeat?.rhythm === 'irregular' ? 'LUB-DUB ... LUB ... DUB-DUB' :
                 heartbeat?.murmur ? 'LUB-WHOOSH-DUB' :
                 'LUB-DUB ... LUB-DUB'}
              </div>
            </div>
          )}
        </div>

        {listening && (
          <>
            {/* Timer */}
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-400">Hörzeit verbleibend:</span>
              <span className={`font-bold ${timeLeft < 5 ? 'text-red-400' : 'text-cyan-400'}`}>
                {timeLeft}s
              </span>
            </div>

            {/* Educational Tip */}
            {timeLeft > 10 && (
              <EducationalPopup
                type="tip"
                title="💡 Diagnose-Tipp"
                content="Achte auf Geschwindigkeit (schnell/langsam), Rhythmus (regelmäßig/unregelmäßig) und zusätzliche Geräusche (Herzgeräusch). Vergleiche mit dem Normalbereich!"
              />
            )}

            {/* Diagnosis Options */}
            <div className="space-y-2">
              <p className="text-sm text-gray-400 font-bold">Was hörst du?</p>
              {Object.values(heartSounds).map((sound) => (
                <button
                  key={sound.label}
                  onClick={() => setSelectedDiagnosis(sound.label)}
                  className={`w-full p-3 rounded-lg border transition-all text-left ${
                    selectedDiagnosis === sound.label
                      ? 'bg-cyan-900/30 border-cyan-500 text-cyan-300'
                      : 'bg-gray-800/50 border-gray-700 text-gray-400 hover:border-cyan-600'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span>{sound.label}</span>
                    {sound.label === 'Normal' && (
                      <span className="text-xs text-gray-500">
                        {normalHeartRate.min}-{normalHeartRate.max} BPM
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmit}
              disabled={!selectedDiagnosis}
              className={`w-full py-3 rounded-lg font-bold transition-all ${
                selectedDiagnosis
                  ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white'
                  : 'bg-gray-800 text-gray-500 cursor-not-allowed'
              }`}
            >
              Diagnose bestätigen
            </button>
          </>
        )}
      </div>
    </div>
  );
};

/**
 * Enhanced Temperature Game - New minigame!
 */
export const TemperatureGame = ({ patient, onComplete }) => {
  const [measuring, setMeasuring] = useState(false);
  const [progress, setProgress] = useState(0);
  const [temperature, setTemperature] = useState(null);
  const [guess, setGuess] = useState('');
  const [showEducation, setShowEducation] = useState(true);

  const vitalSigns = getVitalSignsForAnimal(patient.animalType);
  const normalTemp = vitalSigns?.temperature || { min: 37.5, max: 39.2 };

  useEffect(() => {
    if (measuring && progress < 100) {
      const timer = setTimeout(() => setProgress(progress + 2), 50);
      return () => clearTimeout(timer);
    } else if (progress === 100) {
      // Use real temperature from patient
      const vitalChanges = patient.vitalChanges || {};
      const actualTemp = vitalChanges.temperature ||
        (normalTemp.min + normalTemp.max) / 2 + (Math.random() - 0.5) * 0.5;
      setTemperature(actualTemp.toFixed(1));
      setMeasuring(false);
    }
  }, [measuring, progress]);

  const handleMeasure = () => {
    setMeasuring(true);
    setProgress(0);
    setShowEducation(false);
  };

  const handleSubmit = () => {
    const tempValue = parseFloat(temperature);
    const isNormal = tempValue >= normalTemp.min && tempValue <= normalTemp.max;
    const userGuess = guess.toLowerCase();

    let correct = false;
    if ((isNormal && userGuess === 'normal') ||
        (!isNormal && tempValue > normalTemp.max && userGuess === 'fieber') ||
        (!isNormal && tempValue < normalTemp.min && userGuess === 'unterkühlung')) {
      correct = true;
    }

    onComplete({
      tool: 'thermometer',
      result: `${temperature}°C - ${guess}`,
      correct,
      accuracy: correct ? 100 : 50,
      thoroughness: 0.7,
      data: {
        temperature: tempValue,
        normalRange: `${normalTemp.min}-${normalTemp.max}°C`,
        interpretation: guess,
        isNormal
      },
      educationalContent: {
        fact: `${patient.animalName} haben eine normale Körpertemperatur von ${normalTemp.min}-${normalTemp.max}°C.`,
        explanation: correct
          ? `Richtig! Die Temperatur von ${temperature}°C ist ${isNormal ? 'normal' : 'abnormal'} für ${patient.animalName}.`
          : `Die Temperatur von ${temperature}°C liegt ${tempValue > normalTemp.max ? 'über' : tempValue < normalTemp.min ? 'unter' : 'im'} Normalbereich.`
      }
    });
  };

  return (
    <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-cyan-400">
        <Thermometer className="w-6 h-6" />
        Thermometer - Temperaturmessung
      </h3>

      {showEducation && (
        <EducationalPopup
          type="info"
          title={`🌡️ Normale Temperatur für ${patient.animalName}`}
          content={`Die normale Körpertemperatur liegt bei ${normalTemp.min}-${normalTemp.max}°C. Fieber deutet auf Infektionen hin, niedrige Temperatur auf Schock oder Unterkühlung.`}
          onClose={() => setShowEducation(false)}
        />
      )}

      <div className="space-y-4">
        {/* Animal Info */}
        <div className="bg-amber-900/20 p-3 rounded-lg border border-amber-700/30">
          <div className="text-sm text-gray-300">
            <div className="flex justify-between">
              <span>Normalbereich für {patient.animalName}:</span>
              <span className="font-bold text-amber-400">{normalTemp.min}-{normalTemp.max}°C</span>
            </div>
          </div>
        </div>

        {/* Measuring */}
        {!temperature ? (
          <div className="space-y-4">
            {!measuring ? (
              <button
                onClick={handleMeasure}
                className="w-full py-4 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white font-bold rounded-lg transition-all flex items-center justify-center gap-2"
              >
                <Thermometer className="w-5 h-5" />
                Temperatur messen
              </button>
            ) : (
              <div className="space-y-3">
                <div className="text-center text-amber-400 font-medium">
                  Messung läuft... {progress}%
                </div>
                <div className="w-full bg-gray-800 rounded-full h-4 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-amber-600 to-orange-500 transition-all duration-100"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <div className="text-center">
                  <Thermometer className="w-16 h-16 mx-auto text-amber-500 animate-pulse" />
                </div>
              </div>
            )}
          </div>
        ) : (
          <>
            {/* Temperature Display */}
            <div className="bg-gradient-to-br from-amber-900/30 to-orange-900/30 p-6 rounded-xl border border-amber-700/30 text-center">
              <div className="text-6xl font-bold text-amber-400 mb-2">
                {temperature}°C
              </div>
              <div className="text-sm text-gray-400">Gemessene Temperatur</div>
              <div className="mt-2 text-xs text-gray-500">
                Normal: {normalTemp.min}-{normalTemp.max}°C
              </div>
            </div>

            {/* Interpretation Options */}
            <div className="space-y-2">
              <p className="text-sm text-gray-400 font-bold">Deine Interpretation:</p>
              {['Normal', 'Fieber', 'Unterkühlung'].map((option) => (
                <button
                  key={option}
                  onClick={() => setGuess(option)}
                  className={`w-full p-3 rounded-lg border transition-all text-left ${
                    guess === option
                      ? 'bg-amber-900/30 border-amber-500 text-amber-300'
                      : 'bg-gray-800/50 border-gray-700 text-gray-400 hover:border-amber-600'
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>

            {/* Submit */}
            <button
              onClick={handleSubmit}
              disabled={!guess}
              className={`w-full py-3 rounded-lg font-bold transition-all ${
                guess
                  ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white'
                  : 'bg-gray-800 text-gray-500 cursor-not-allowed'
              }`}
            >
              Interpretation bestätigen
            </button>
          </>
        )}
      </div>
    </div>
  );
};

// Export all enhanced minigames
export const EnhancedDiagnosticMinigames = {
  EnhancedStethoscopeGame,
  TemperatureGame
};

export default EnhancedDiagnosticMinigames;
