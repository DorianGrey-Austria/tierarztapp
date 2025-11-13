import React, { useState, useEffect, useRef } from 'react';
import { Activity, Heart, Thermometer, Search, Zap, Target, CheckCircle, XCircle, Clock } from 'lucide-react';

/**
 * Stethoscope Minigame - Listen to heart sounds and identify abnormalities
 */
export const StethoscopeGame = ({ patient, onComplete }) => {
  const [listening, setListening] = useState(false);
  const [heartbeat, setHeartbeat] = useState(null);
  const [timeLeft, setTimeLeft] = useState(15);
  const [selectedDiagnosis, setSelectedDiagnosis] = useState(null);

  const heartSounds = {
    normal: { rate: 'normal', rhythm: 'regular', murmur: false, label: 'Normal' },
    tachycardia: { rate: 'fast', rhythm: 'regular', murmur: false, label: 'Tachykardie (zu schnell)' },
    bradycardia: { rate: 'slow', rhythm: 'regular', murmur: false, label: 'Bradykardie (zu langsam)' },
    arrhythmia: { rate: 'normal', rhythm: 'irregular', murmur: false, label: 'Arrhythmie (unregelmäßig)' },
    murmur: { rate: 'normal', rhythm: 'regular', murmur: true, label: 'Herzgeräusch' }
  };

  useEffect(() => {
    if (listening && timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [listening, timeLeft]);

  useEffect(() => {
    // Determine heart sound based on patient condition
    const vitalChanges = patient.vitalChanges || {};
    const normalRate = patient.vitalSigns?.heartRate || { min: 60, max: 120 };

    if (vitalChanges.heartRate > normalRate.max * 1.2) {
      setHeartbeat(heartSounds.tachycardia);
    } else if (vitalChanges.heartRate < normalRate.min * 0.8) {
      setHeartbeat(heartSounds.bradycardia);
    } else if (patient.diagnosis?.includes('Herz')) {
      setHeartbeat(heartSounds.murmur);
    } else {
      setHeartbeat(heartSounds.normal);
    }
  }, [patient]);

  const handleListen = () => {
    setListening(true);
    // Play heart sound effect here
  };

  const handleSubmit = () => {
    const correct = selectedDiagnosis === heartbeat.label;
    const accuracy = correct ? 100 : 0;

    onComplete({
      tool: 'stethoscope',
      result: selectedDiagnosis,
      correct,
      accuracy,
      thoroughness: 0.8,
      data: { heartSound: heartbeat.label }
    });
  };

  return (
    <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-cyan-400">
        <Heart className="w-6 h-6" />
        Stethoskop - Herzuntersuchung
      </h3>

      <div className="space-y-4">
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
                'animate-pulse'
              }`}>
                <Heart className={`w-16 h-16 text-red-500 ${
                  heartbeat?.rhythm === 'irregular' ? 'animate-bounce' : ''
                }`} />
              </div>
              <div className="text-cyan-400 font-mono text-sm">
                {heartbeat?.rate === 'fast' ? 'LUB-DUB-LUB-DUB-LUB-DUB' :
                 heartbeat?.rate === 'slow' ? 'LUB ... DUB ... LUB ... DUB' :
                 heartbeat?.rhythm === 'irregular' ? 'LUB-DUB ... LUB ... DUB-DUB' :
                 heartbeat?.murmur ? 'LUB-SH-DUB' :
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

            {/* Diagnosis Options */}
            <div className="space-y-2">
              <p className="text-sm text-gray-400">Was hörst du?</p>
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
                  {sound.label}
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
 * X-Ray Minigame - Find fractures and abnormalities
 */
export const XRayGame = ({ patient, onComplete }) => {
  const [imageRevealed, setImageRevealed] = useState(0);
  const [foundAnomalies, setFoundAnomalies] = useState([]);
  const [timeLeft, setTimeLeft] = useState(30);
  const canvasRef = useRef(null);

  const anomalies = [
    { id: 1, x: 45, y: 35, type: 'fracture', label: 'Fraktur' },
    { id: 2, x: 60, y: 50, type: 'inflammation', label: 'Entzündung' },
    { id: 3, x: 30, y: 60, type: 'foreign_object', label: 'Fremdkörper' }
  ];

  // Determine actual anomalies based on patient condition
  const actualAnomalies = anomalies.filter(a =>
    patient.symptoms?.some(s =>
      s.toLowerCase().includes(a.type.split('_')[0]) || s.toLowerCase().includes(a.label.toLowerCase())
    )
  );

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else {
      handleComplete();
    }
  }, [timeLeft]);

  const handleReveal = () => {
    if (imageRevealed < 100) {
      setImageRevealed(Math.min(100, imageRevealed + 10));
    }
  };

  const handleClick = (e) => {
    const rect = e.target.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    // Check if click is near an anomaly
    actualAnomalies.forEach(anomaly => {
      const distance = Math.sqrt(Math.pow(x - anomaly.x, 2) + Math.pow(y - anomaly.y, 2));
      if (distance < 8 && !foundAnomalies.includes(anomaly.id)) {
        setFoundAnomalies([...foundAnomalies, anomaly.id]);
      }
    });
  };

  const handleComplete = () => {
    const foundCount = foundAnomalies.length;
    const totalCount = actualAnomalies.length;
    const accuracy = totalCount > 0 ? (foundCount / totalCount) * 100 : 100;

    onComplete({
      tool: 'xray',
      result: `${foundCount}/${totalCount} Anomalien gefunden`,
      correct: foundCount === totalCount,
      accuracy,
      thoroughness: imageRevealed / 100,
      data: { foundAnomalies, totalAnomalies: actualAnomalies }
    });
  };

  return (
    <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-cyan-400">
        <Search className="w-6 h-6" />
        Röntgen - Bildanalyse
      </h3>

      <div className="space-y-4">
        {/* Timer and Progress */}
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">Zeit: {timeLeft}s</span>
          <span className="text-cyan-400">
            Gefunden: {foundAnomalies.length}/{actualAnomalies.length}
          </span>
        </div>

        {/* X-Ray Image */}
        <div
          ref={canvasRef}
          onClick={handleClick}
          className="relative h-96 bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg cursor-crosshair border-2 border-gray-700 overflow-hidden"
        >
          {/* Simulated X-Ray Image */}
          <div
            className="absolute inset-0 bg-gradient-radial from-gray-600 via-gray-800 to-black opacity-70"
            style={{
              clipPath: `inset(0 ${100 - imageRevealed}% 0 0)`,
              transition: 'clip-path 0.3s'
            }}
          >
            {/* Skeletal structure simulation */}
            <div className="absolute inset-0">
              {actualAnomalies.map((anomaly) => (
                <div
                  key={anomaly.id}
                  className={`absolute w-12 h-12 rounded-full transition-all ${
                    foundAnomalies.includes(anomaly.id)
                      ? 'bg-green-500/50 border-2 border-green-400'
                      : 'bg-red-500/30 border-2 border-red-600 animate-pulse'
                  }`}
                  style={{
                    left: `${anomaly.x}%`,
                    top: `${anomaly.y}%`,
                    transform: 'translate(-50%, -50%)'
                  }}
                >
                  {foundAnomalies.includes(anomaly.id) && (
                    <CheckCircle className="w-full h-full text-green-400" />
                  )}
                </div>
              ))}
            </div>
          </div>

          {imageRevealed < 100 && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/50">
              <button
                onClick={handleReveal}
                className="px-6 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-lg transition-all"
              >
                Bild entwickeln ({imageRevealed}%)
              </button>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="text-xs text-gray-400 space-y-1">
          <p>• Klicke auf verdächtige Bereiche im Röntgenbild</p>
          <p>• Entwickle das Bild weiter für bessere Sicht</p>
          <p>• Finde alle Anomalien bevor die Zeit abläuft</p>
        </div>

        {/* Complete Button */}
        <button
          onClick={handleComplete}
          className="w-full py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-bold rounded-lg transition-all"
        >
          Analyse abschließen
        </button>
      </div>
    </div>
  );
};

/**
 * Blood Test Minigame - Analyze blood values
 */
export const BloodTestGame = ({ patient, onComplete }) => {
  const [testResults, setTestResults] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [interpretation, setInterpretation] = useState({});

  const bloodParameters = [
    { id: 'wbc', name: 'Weiße Blutkörperchen', unit: '×10³/μL', normal: { min: 6, max: 17 } },
    { id: 'rbc', name: 'Rote Blutkörperchen', unit: '×10⁶/μL', normal: { min: 5.5, max: 8.5 } },
    { id: 'glucose', name: 'Glukose', unit: 'mg/dL', normal: { min: 75, max: 120 } },
    { id: 'alt', name: 'ALT (Leber)', unit: 'U/L', normal: { min: 10, max: 100 } },
    { id: 'creatinine', name: 'Kreatinin (Niere)', unit: 'mg/dL', normal: { min: 0.8, max: 1.8 } }
  ];

  useEffect(() => {
    if (analyzing && progress < 100) {
      const timer = setTimeout(() => setProgress(progress + 5), 100);
      return () => clearTimeout(timer);
    } else if (progress === 100) {
      generateResults();
    }
  }, [analyzing, progress]);

  const startAnalysis = () => {
    setAnalyzing(true);
    setProgress(0);
  };

  const generateResults = () => {
    const results = {};
    const vitalChanges = patient.vitalChanges || {};

    bloodParameters.forEach(param => {
      let value;
      const mid = (param.normal.min + param.normal.max) / 2;
      const range = param.normal.max - param.normal.min;

      // Generate abnormal values based on patient condition
      if (patient.symptoms?.some(s => s.toLowerCase().includes('fieber') || s.toLowerCase().includes('infektion'))) {
        if (param.id === 'wbc') {
          value = param.normal.max + Math.random() * 5; // Elevated WBC
        } else {
          value = mid + (Math.random() - 0.5) * range * 0.3;
        }
      } else if (patient.symptoms?.some(s => s.toLowerCase().includes('diabetes'))) {
        if (param.id === 'glucose') {
          value = param.normal.max + Math.random() * 50; // High glucose
        } else {
          value = mid + (Math.random() - 0.5) * range * 0.3;
        }
      } else if (patient.symptoms?.some(s => s.toLowerCase().includes('niere'))) {
        if (param.id === 'creatinine') {
          value = param.normal.max + Math.random() * 2; // High creatinine
        } else {
          value = mid + (Math.random() - 0.5) * range * 0.3;
        }
      } else {
        value = mid + (Math.random() - 0.5) * range * 0.5;
      }

      results[param.id] = {
        value: Math.round(value * 10) / 10,
        normal: param.normal,
        isNormal: value >= param.normal.min && value <= param.normal.max
      };
    });

    setTestResults(results);
    setAnalyzing(false);
  };

  const handleInterpretation = (paramId, isAbnormal) => {
    setInterpretation({ ...interpretation, [paramId]: isAbnormal });
  };

  const handleSubmit = () => {
    let correct = 0;
    let total = 0;

    Object.keys(testResults).forEach(paramId => {
      total++;
      const userSaysAbnormal = interpretation[paramId];
      const actuallyAbnormal = !testResults[paramId].isNormal;

      if (userSaysAbnormal === actuallyAbnormal) {
        correct++;
      }
    });

    const accuracy = (correct / total) * 100;

    onComplete({
      tool: 'blood_test',
      result: `${correct}/${total} korrekt interpretiert`,
      correct: correct === total,
      accuracy,
      thoroughness: 1.0,
      data: { testResults, interpretation }
    });
  };

  return (
    <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-cyan-400">
        <Activity className="w-6 h-6" />
        Bluttest - Laboranalyse
      </h3>

      <div className="space-y-4">
        {!testResults ? (
          <>
            {!analyzing ? (
              <button
                onClick={startAnalysis}
                className="w-full py-4 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-lg transition-all flex items-center justify-center gap-2"
              >
                <Zap className="w-5 h-5" />
                Blutprobe analysieren
              </button>
            ) : (
              <div className="space-y-3">
                <div className="text-center text-cyan-400 font-medium">
                  Analyse läuft... {progress}%
                </div>
                <div className="w-full bg-gray-800 rounded-full h-4 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-cyan-600 to-blue-500 transition-all duration-100"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <div className="grid grid-cols-5 gap-2">
                  {bloodParameters.map((param, idx) => (
                    <div
                      key={param.id}
                      className={`h-12 rounded ${
                        progress > idx * 20 ? 'bg-cyan-600/30 animate-pulse' : 'bg-gray-800'
                      }`}
                    />
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <>
            {/* Blood Test Results */}
            <div className="space-y-3">
              {bloodParameters.map(param => {
                const result = testResults[param.id];
                const interpreted = interpretation[param.id];

                return (
                  <div
                    key={param.id}
                    className={`p-3 rounded-lg border ${
                      result.isNormal ? 'border-green-700/50 bg-gray-800/30' : 'border-red-700/50 bg-red-900/10'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex-1">
                        <div className="text-sm font-medium text-gray-300">{param.name}</div>
                        <div className="text-xs text-gray-500">
                          Normal: {param.normal.min} - {param.normal.max} {param.unit}
                        </div>
                      </div>
                      <div className={`text-2xl font-bold ${
                        result.isNormal ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {result.value} {param.unit}
                      </div>
                    </div>

                    {/* User Interpretation */}
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleInterpretation(param.id, false)}
                        className={`flex-1 py-2 rounded text-sm font-medium transition-all ${
                          interpreted === false
                            ? 'bg-green-600 text-white'
                            : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                        }`}
                      >
                        Normal
                      </button>
                      <button
                        onClick={() => handleInterpretation(param.id, true)}
                        className={`flex-1 py-2 rounded text-sm font-medium transition-all ${
                          interpreted === true
                            ? 'bg-red-600 text-white'
                            : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                        }`}
                      >
                        Abnormal
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmit}
              disabled={Object.keys(interpretation).length !== bloodParameters.length}
              className={`w-full py-3 rounded-lg font-bold transition-all ${
                Object.keys(interpretation).length === bloodParameters.length
                  ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white'
                  : 'bg-gray-800 text-gray-500 cursor-not-allowed'
              }`}
            >
              Interpretation abschließen
            </button>
          </>
        )}
      </div>
    </div>
  );
};

/**
 * Palpation Minigame - Find pain points and swellings
 */
export const PalpationGame = ({ patient, onComplete }) => {
  const [touches, setTouches] = useState([]);
  const [foundPoints, setFoundPoints] = useState([]);
  const [timeLeft, setTimeLeft] = useState(20);

  const painPoints = [
    { id: 1, x: 40, y: 30, severity: 'high', label: 'Starker Schmerz' },
    { id: 2, x: 60, y: 50, severity: 'medium', label: 'Schwellung' },
    { id: 3, x: 25, y: 65, severity: 'low', label: 'Leichter Schmerz' }
  ];

  // Filter pain points based on patient symptoms
  const actualPainPoints = painPoints.filter((point, idx) =>
    patient.symptoms?.some(s =>
      s.toLowerCase().includes('schmerz') ||
      s.toLowerCase().includes('schwellung') ||
      s.toLowerCase().includes('lahm')
    ) || idx === 0 // Always include at least one
  );

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else {
      handleComplete();
    }
  }, [timeLeft]);

  const handleTouch = (e) => {
    const rect = e.target.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    setTouches([...touches, { x, y, timestamp: Date.now() }]);

    // Check if touch is near a pain point
    actualPainPoints.forEach(point => {
      const distance = Math.sqrt(Math.pow(x - point.x, 2) + Math.pow(y - point.y, 2));
      if (distance < 10 && !foundPoints.includes(point.id)) {
        setFoundPoints([...foundPoints, point.id]);
      }
    });
  };

  const handleComplete = () => {
    const foundCount = foundPoints.length;
    const totalCount = actualPainPoints.length;
    const accuracy = totalCount > 0 ? (foundCount / totalCount) * 100 : 100;

    onComplete({
      tool: 'palpation',
      result: `${foundCount}/${totalCount} Schmerzpunkte gefunden`,
      correct: foundCount === totalCount,
      accuracy,
      thoroughness: Math.min(touches.length / 20, 1),
      data: { foundPoints: foundCount, totalPoints: totalCount }
    });
  };

  return (
    <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-cyan-400">
        <Target className="w-6 h-6" />
        Abtasten - Palpation
      </h3>

      <div className="space-y-4">
        {/* Timer and Progress */}
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">Zeit: {timeLeft}s</span>
          <span className="text-cyan-400">
            Gefunden: {foundPoints.length}/{actualPainPoints.length}
          </span>
        </div>

        {/* Animal Body Diagram */}
        <div
          onClick={handleTouch}
          className="relative h-96 bg-gradient-to-br from-amber-900/20 to-amber-800/10 rounded-lg cursor-pointer border-2 border-gray-700 overflow-hidden"
        >
          {/* Animal silhouette */}
          <div className="absolute inset-0 flex items-center justify-center opacity-30">
            <div className="text-9xl">{patient.icon || '🐕'}</div>
          </div>

          {/* Touch points */}
          {touches.map((touch, idx) => (
            <div
              key={idx}
              className="absolute w-4 h-4 bg-cyan-400/30 rounded-full animate-ping"
              style={{
                left: `${touch.x}%`,
                top: `${touch.y}%`,
                transform: 'translate(-50%, -50%)'
              }}
            />
          ))}

          {/* Pain points */}
          {actualPainPoints.map(point => (
            <div
              key={point.id}
              className={`absolute w-16 h-16 rounded-full transition-all ${
                foundPoints.includes(point.id)
                  ? 'bg-green-500/50 border-2 border-green-400'
                  : 'bg-red-500/20 border-2 border-red-600/50'
              }`}
              style={{
                left: `${point.x}%`,
                top: `${point.y}%`,
                transform: 'translate(-50%, -50%)'
              }}
            >
              {foundPoints.includes(point.id) && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <CheckCircle className="w-8 h-8 text-green-400" />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Instructions */}
        <div className="text-xs text-gray-400 space-y-1">
          <p>• Klicke auf den Körper des Tieres zum Abtasten</p>
          <p>• Finde alle Schmerzpunkte und Schwellungen</p>
          <p>• Grüne Bereiche = gefunden, Rote Bereiche = noch zu finden</p>
        </div>

        {/* Complete Button */}
        <button
          onClick={handleComplete}
          className="w-full py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-bold rounded-lg transition-all"
        >
          Untersuchung abschließen
        </button>
      </div>
    </div>
  );
};

// Export all minigames
export const DiagnosticMinigames = {
  StethoscopeGame,
  XRayGame,
  BloodTestGame,
  PalpationGame
};

export default DiagnosticMinigames;
