import React, { useState, useEffect } from 'react';
import { Activity, Zap, Brain, Heart, AlertCircle, CheckCircle, Wifi } from 'lucide-react';

const AnimalScannerPro = () => {
  const [stage, setStage] = useState('input'); // input, scanning, results
  const [suspectedInjury, setSuspectedInjury] = useState('');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [scanProgress, setScanProgress] = useState(0);
  const [pulseAnimation, setPulseAnimation] = useState(0);
  const [selectedAnimalType, setSelectedAnimalType] = useState('hund');
  const [selectedDisease, setSelectedDisease] = useState('');

  const [vitals, setVitals] = useState({
    heartRate: 0,
    temperature: 0,
    bloodPressure: 0,
    oxygenLevel: 0,
    respirationRate: 0,
    bloodGlucose: 0
  });

  const commonDiseases = {
    hund: [
      { value: '', label: '-- Bitte wählen --' },
      { value: 'fraktur_femur', label: 'Fraktur - Femur / Tibia' },
      { value: 'gdv', label: 'GDV - Magendrehung (NOTFALL!)' },
      { value: 'diabetes', label: 'Diabetes mellitus' },
      { value: 'epilepsie', label: 'Idiopathische Epilepsie' },
      { value: 'hd', label: 'HD - Hüftgelenksdysplasie' },
      { value: 'custom', label: 'Andere (selbst eingeben)' }
    ],
    katze: [
      { value: '', label: '-- Bitte wählen --' },
      { value: 'flutd', label: 'FLUTD - Harnwegserkrankung' },
      { value: 'fip', label: 'FIP - Feline Infektiöse Peritonitis' },
      { value: 'diabetes', label: 'Diabetes mellitus' },
      { value: 'cni', label: 'CNI - Chronische Niereninsuffizienz' },
      { value: 'custom', label: 'Andere (selbst eingeben)' }
    ],
    pferd: [
      { value: '', label: '-- Bitte wählen --' },
      { value: 'kolik', label: 'Kolik (NOTFALL!)' },
      { value: 'hufrehe', label: 'Hufrehe / Laminitis' },
      { value: 'lahmheit', label: 'Lahmheit' },
      { value: 'atemweg', label: 'COB/RAO - Atemwegserkrankung' },
      { value: 'custom', label: 'Andere (selbst eingeben)' }
    ],
    kaninchen: [
      { value: '', label: '-- Bitte wählen --' },
      { value: 'gi_stasis', label: 'GI Stasis - Verdauungsstillstand' },
      { value: 'e_cuniculi', label: 'E. cuniculi' },
      { value: 'zahn', label: 'Zahnfehlstellung' },
      { value: 'myxomatose', label: 'Myxomatose' },
      { value: 'custom', label: 'Andere (selbst eingeben)' }
    ]
  };

  const animalNormalValues = {
    hund: {
      heartRate: { min: 70, max: 120, unit: 'BPM' },
      temperature: { min: 37.5, max: 39.0, unit: '°C' },
      bloodPressure: { min: 110, max: 160, unit: 'mmHg' },
      oxygenLevel: { min: 95, max: 100, unit: '%' },
      respirationRate: { min: 10, max: 30, unit: '/min' },
      bloodGlucose: { min: 60, max: 120, unit: 'mg/dl' }
    },
    katze: {
      heartRate: { min: 120, max: 140, unit: 'BPM' },
      temperature: { min: 38.0, max: 39.2, unit: '°C' },
      bloodPressure: { min: 120, max: 170, unit: 'mmHg' },
      oxygenLevel: { min: 95, max: 100, unit: '%' },
      respirationRate: { min: 20, max: 30, unit: '/min' },
      bloodGlucose: { min: 70, max: 150, unit: 'mg/dl' }
    },
    pferd: {
      heartRate: { min: 28, max: 44, unit: 'BPM' },
      temperature: { min: 37.2, max: 38.3, unit: '°C' },
      bloodPressure: { min: 120, max: 180, unit: 'mmHg' },
      oxygenLevel: { min: 95, max: 100, unit: '%' },
      respirationRate: { min: 8, max: 16, unit: '/min' },
      bloodGlucose: { min: 70, max: 135, unit: 'mg/dl' }
    },
    kaninchen: {
      heartRate: { min: 180, max: 250, unit: 'BPM' },
      temperature: { min: 38.5, max: 40.0, unit: '°C' },
      bloodPressure: { min: 90, max: 130, unit: 'mmHg' },
      oxygenLevel: { min: 95, max: 100, unit: '%' },
      respirationRate: { min: 30, max: 60, unit: '/min' },
      bloodGlucose: { min: 75, max: 155, unit: 'mg/dl' }
    }
  };

  const getValueStatus = (value, min, max) => {
    const range = max - min;
    const warningThreshold = range * 0.15;
    
    if (value >= min && value <= max) {
      return { status: 'normal', color: 'text-green-400', bgColor: 'bg-green-900/30', icon: '✓' };
    } else if (value < min - warningThreshold || value > max + warningThreshold) {
      return { status: 'kritisch', color: 'text-red-400', bgColor: 'bg-red-900/30', icon: '⚠' };
    } else {
      return { status: 'warnung', color: 'text-orange-400', bgColor: 'bg-orange-900/30', icon: '!' };
    }
  };

  const getMedicalAlert = (vitalName, value, normalRange, status) => {
    const alerts = {
      heartRate: {
        kritisch_hoch: 'TACHYKARDIE: Sofortige kardiologische Untersuchung erforderlich! Lidocain 2mg/kg IV.',
        kritisch_niedrig: 'BRADYKARDIE: Kritisch niedriger Puls! Atropin 0.04mg/kg IV.',
        warnung_hoch: 'Erhöhte Herzfrequenz: Stress oder beginnende Komplikation möglich.',
        warnung_niedrig: 'Verminderte Herzfrequenz: Überwachung empfohlen.',
        normal: 'Herzfrequenz im Normalbereich.'
      },
      temperature: {
        kritisch_hoch: 'HYPERTHERMIE: Sofortige Kühlung erforderlich! Gefahr eines Hitzschlags.',
        kritisch_niedrig: 'HYPOTHERMIE: Sofortige Wärmezufuhr notwendig! Lebensgefahr.',
        warnung_hoch: 'Fieber festgestellt: Infektion oder Entzündung wahrscheinlich.',
        warnung_niedrig: 'Untertemperatur: Wärmezufuhr und Überwachung empfohlen.',
        normal: 'Körpertemperatur im Normalbereich.'
      },
      bloodPressure: {
        kritisch_hoch: 'HYPERTONIE: Gefahr von Organschäden! Amlodipin 0.2mg/kg PO.',
        kritisch_niedrig: 'HYPOTONIE: Schockgefahr! Volumentherapie + Vasopressoren.',
        warnung_hoch: 'Erhöhter Blutdruck: Weitere Diagnostik empfohlen.',
        warnung_niedrig: 'Niedriger Blutdruck: Flüssigkeitszufuhr erwägen.',
        normal: 'Blutdruck im optimalen Bereich.'
      },
      oxygenLevel: {
        kritisch_niedrig: 'HYPOXIE: Sofortige Sauerstoffgabe! Atemwege überprüfen.',
        warnung_niedrig: 'Verminderte Sauerstoffsättigung: Atemfunktion überwachen.',
        normal: 'Sauerstoffsättigung optimal.'
      },
      respirationRate: {
        kritisch_hoch: 'TACHYPNOE: Schwere Atemnot! O2-Käfig erforderlich.',
        kritisch_niedrig: 'ATEMDEPRESSION: Notfall! Beatmung vorbereiten.',
        warnung_hoch: 'Beschleunigte Atmung: Stress oder Atemwegsproblem möglich.',
        warnung_niedrig: 'Verlangsamte Atmung: Engmaschige Überwachung.',
        normal: 'Atemfrequenz normal.'
      },
      bloodGlucose: {
        kritisch_hoch: 'HYPERGLYKÄMIE: Diabetes-Notfall! Insulin-CRI 0.1 IU/kg/h.',
        kritisch_niedrig: 'HYPOGLYKÄMIE: Sofort 50% Dextrose 1ml/kg IV!',
        warnung_hoch: 'Erhöhter Blutzucker: Diabetes-Screening empfohlen.',
        warnung_niedrig: 'Niedriger Blutzucker: Fütterung und Überwachung.',
        normal: 'Blutzuckerwerte im Normalbereich.'
      }
    };
    
    let alertKey = status.status;
    if (status.status !== 'normal') {
      alertKey += value > normalRange.max ? '_hoch' : '_niedrig';
    }
    
    return alerts[vitalName]?.[alertKey] || 'Wert außerhalb des Normalbereichs.';
  };

  const diagnoseTexts = {
    'fraktur': 'Radiologische Bildgebung zeigt Fraktur mit 15° Achsenabweichung. Sofortige chirurgische Intervention mittels Osteosynthese indiziert.',
    'gdv': 'AKUT-NOTFALL: Gastric Dilatation-Volvulus bestätigt! 270° Magentorsion. Sofortmaßnahmen: IV-Zugänge, kristalloide Infusion 90ml/kg/h.',
    'diabetes': 'Diabetes mellitus diagnostiziert. Glukose 428 mg/dl, Ketonurie positiv. Insulintherapie: Start mit 0.5 IU/kg BID.',
    'kolik': 'NOTFALL: Akute Kolik mit Kreislaufschock! Herzfrequenz erhöht. Sofort: Buscopan 0.3mg/kg IV, Infusionstherapie.',
    'flutd': 'FLUTD mit Harnröhrenobstruktion. Sofortige Katheterisierung unter Sedation. Kristalloide Infusion.',
    'gi_stasis': 'GI Stasis bestätigt. Magenüberladung palpierbar. Therapie: Metoclopramid, Flüssigkeitstherapie, Bauchmassage.',
    'hufrehe': 'Akute Hufrehe Grad III. Rotation des Hufbeins 8°. Sofort: Kühlung, Analgesie, Boxenruhe.',
    'default': 'Pathologische Veränderung im angegebenen Bereich detektiert. Weitere diagnostische Verfahren empfohlen.'
  };

  const getDiagnoseText = () => {
    const key = (selectedDisease || suspectedInjury || '').toLowerCase();
    for (let diagnoseKey in diagnoseTexts) {
      if (key.includes(diagnoseKey)) {
        return diagnoseTexts[diagnoseKey];
      }
    }
    return diagnoseTexts.default;
  };

  useEffect(() => {
    if (stage === 'scanning') {
      const interval = setInterval(() => {
        setScanProgress(prev => {
          if (prev >= 100) {
            setStage('results');
            return 100;
          }
          return prev + 2;
        });
      }, 50);
      return () => clearInterval(interval);
    }
  }, [stage]);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulseAnimation(prev => (prev + 1) % 100);
    }, 20);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (stage === 'results') {
      const normalValues = animalNormalValues[selectedAnimalType];
      const injury = (selectedDisease || suspectedInjury || '').toLowerCase();
      
      const generateValue = (normal, severity = 0) => {
        const range = normal.max - normal.min;
        const baseValue = normal.min + Math.random() * range;
        
        if (severity === 0) return baseValue;
        
        const deviation = range * (0.2 + Math.random() * 0.3);
        if (severity > 0) {
          return baseValue + deviation;
        } else {
          return baseValue - deviation;
        }
      };
      
      let newVitals = {};
      
      if (injury.includes('fraktur') || injury.includes('lahmheit')) {
        newVitals.heartRate = Math.floor(generateValue(normalValues.heartRate, 1));
        newVitals.bloodPressure = Math.floor(generateValue(normalValues.bloodPressure, 1));
        newVitals.temperature = parseFloat(generateValue(normalValues.temperature, 0.5)).toFixed(1);
        newVitals.respirationRate = Math.floor(generateValue(normalValues.respirationRate, 0.5));
      } else if (injury.includes('gdv') || injury.includes('magen') || injury.includes('kolik')) {
        newVitals.heartRate = Math.floor(generateValue(normalValues.heartRate, 1));
        newVitals.temperature = parseFloat(generateValue(normalValues.temperature, 0.7)).toFixed(1);
        newVitals.bloodPressure = Math.floor(generateValue(normalValues.bloodPressure, -0.5));
      } else if (injury.includes('diabetes')) {
        newVitals.bloodGlucose = Math.floor(generateValue(normalValues.bloodGlucose, 2));
      } else {
        newVitals.heartRate = Math.floor(generateValue(normalValues.heartRate, Math.random() > 0.7 ? 0.5 : 0));
        newVitals.temperature = parseFloat(generateValue(normalValues.temperature, Math.random() > 0.8 ? 0.3 : 0)).toFixed(1);
      }
      
      Object.keys(normalValues).forEach(key => {
        if (!newVitals[key]) {
          newVitals[key] = key === 'temperature' 
            ? parseFloat(generateValue(normalValues[key], Math.random() > 0.8 ? (Math.random() - 0.5) : 0)).toFixed(1)
            : Math.floor(generateValue(normalValues[key], Math.random() > 0.9 ? (Math.random() - 0.5) * 0.5 : 0));
        }
      });
      
      setVitals(newVitals);
    }
  }, [stage, selectedAnimalType, suspectedInjury, selectedDisease]);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const startScan = () => {
    if ((suspectedInjury || (selectedDisease && selectedDisease !== 'custom')) && uploadedImage) {
      setStage('scanning');
      setScanProgress(0);
    }
  };

  const resetScan = () => {
    setStage('input');
    setSuspectedInjury('');
    setSelectedDisease('');
    setUploadedImage(null);
    setScanProgress(0);
    setSelectedAnimalType('hund');
  };

  return (
    <div className="min-h-screen bg-gray-950 text-cyan-300 font-mono overflow-hidden relative">
      {/* Animated Background Grid */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `linear-gradient(cyan 1px, transparent 1px), linear-gradient(90deg, cyan 1px, transparent 1px)`,
          backgroundSize: '50px 50px',
          transform: `translateY(${pulseAnimation * 0.5}px)`
        }}></div>
      </div>

      {/* Header */}
      <div className="relative z-10 border-b border-cyan-800 bg-gray-900/80 backdrop-blur-sm">
        <div className="p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Zap className="w-8 h-8 text-cyan-400 animate-pulse" />
              <h1 className="text-2xl font-bold text-cyan-400">VetScan Pro 3000</h1>
            </div>
            <div className="text-xs text-cyan-600">v3.1.0 | Medical Grade</div>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Wifi className="w-4 h-4 text-green-400 animate-pulse" />
              <span className="text-xs text-green-400">ONLINE</span>
            </div>
            <div className="text-xs text-cyan-600">{new Date().toLocaleString('de-DE')}</div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 p-8">
        {stage === 'input' && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-gray-900/60 backdrop-blur-md rounded-lg p-8 border border-cyan-800 shadow-2xl shadow-cyan-900/50">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                <Brain className="w-6 h-6" />
                VETERINÄRMEDIZINISCHE DIAGNOSTIK
              </h2>
              
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm mb-2 text-cyan-400">TIERART:</label>
                    <select
                      value={selectedAnimalType}
                      onChange={(e) => {
                        setSelectedAnimalType(e.target.value);
                        setSelectedDisease('');
                        setSuspectedInjury('');
                      }}
                      className="w-full p-3 bg-gray-800 border border-cyan-700 rounded text-cyan-300"
                    >
                      <option value="hund">Hund</option>
                      <option value="katze">Katze</option>
                      <option value="pferd">Pferd</option>
                      <option value="kaninchen">Kaninchen</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm mb-2 text-cyan-400">VERDACHTSDIAGNOSE:</label>
                    <select
                      value={selectedDisease}
                      onChange={(e) => setSelectedDisease(e.target.value)}
                      className="w-full p-3 bg-gray-800 border border-cyan-700 rounded text-cyan-300"
                    >
                      {commonDiseases[selectedAnimalType].map(disease => (
                        <option key={disease.value} value={disease.value}>{disease.label}</option>
                      ))}
                    </select>
                  </div>
                </div>
                
                {selectedDisease === 'custom' && (
                  <div>
                    <label className="block text-sm mb-2 text-cyan-400">EIGENE DIAGNOSE:</label>
                    <input
                      type="text"
                      value={suspectedInjury}
                      onChange={(e) => setSuspectedInjury(e.target.value)}
                      className="w-full p-3 bg-gray-800 border border-cyan-700 rounded text-cyan-300"
                      placeholder="z.B. Gebrochenes Bein, Bauchschmerzen..."
                    />
                  </div>
                )}

                <div>
                  <label className="block text-sm mb-2 text-cyan-400">PATIENT SCAN-BILD:</label>
                  <div className="border-2 border-dashed border-cyan-700 rounded-lg p-8 text-center hover:border-cyan-400 transition-colors bg-gray-800/50">
                    <input
                      type="file"
                      onChange={handleImageUpload}
                      accept="image/*"
                      className="hidden"
                      id="image-upload"
                    />
                    <label htmlFor="image-upload" className="cursor-pointer">
                      {uploadedImage ? (
                        <div className="space-y-2">
                          <img src={uploadedImage} alt="Patient" className="max-h-48 mx-auto rounded" />
                          <p className="text-green-400 text-sm">✓ BILD ERFOLGREICH GELADEN</p>
                        </div>
                      ) : (
                        <div className="space-y-2">
                          <Activity className="w-16 h-16 mx-auto text-cyan-600" />
                          <p>KLICKEN FÜR BILD-UPLOAD</p>
                        </div>
                      )}
                    </label>
                  </div>
                </div>

                <button
                  onClick={startScan}
                  disabled={!(suspectedInjury || (selectedDisease && selectedDisease !== 'custom')) || !uploadedImage}
                  className={`w-full py-4 rounded font-bold transition-all transform hover:scale-105 ${
                    (suspectedInjury || (selectedDisease && selectedDisease !== 'custom')) && uploadedImage
                      ? 'bg-cyan-600 hover:bg-cyan-500 text-gray-900 shadow-lg shadow-cyan-600/50'
                      : 'bg-gray-700 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  SCAN INITIALISIEREN
                </button>
              </div>
            </div>
          </div>
        )}

        {stage === 'scanning' && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-gray-900/60 backdrop-blur-md rounded-lg p-8 border border-cyan-800 shadow-2xl shadow-cyan-900/50">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                <Activity className="w-6 h-6 animate-spin" />
                SCAN LÄUFT...
              </h2>
              
              <div className="space-y-6">
                {uploadedImage && (
                  <div className="relative overflow-hidden rounded-lg">
                    <img src={uploadedImage} alt="Scanning" className="w-full opacity-50" />
                    <div 
                      className="absolute inset-0 bg-gradient-to-b from-cyan-400/20 to-transparent"
                      style={{
                        transform: `translateY(${100 - scanProgress}%)`,
                        transition: 'transform 0.1s linear'
                      }}
                    ></div>
                  </div>
                )}

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>FORTSCHRITT</span>
                    <span>{scanProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-800 rounded-full h-4 overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-cyan-600 to-cyan-400 transition-all duration-100"
                      style={{ width: `${scanProgress}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {stage === 'results' && (
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Column */}
              <div className="bg-gray-900/60 backdrop-blur-md rounded-lg p-6 border border-cyan-800 shadow-2xl shadow-cyan-900/50">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <CheckCircle className="w-6 h-6 text-green-400" />
                  SCAN ABGESCHLOSSEN
                </h2>
                
                {uploadedImage && (
                  <div className="relative rounded-lg overflow-hidden mb-4">
                    <img src={uploadedImage} alt="Analyzed" className="w-full" />
                  </div>
                )}

                <div className="space-y-3">
                  <div className="bg-gray-800 p-3 rounded border border-cyan-700">
                    <div className="text-xs text-cyan-600 mb-1">TIERART:</div>
                    <div className="text-cyan-400 font-semibold">{selectedAnimalType.toUpperCase()}</div>
                  </div>
                  
                  <div className="bg-gray-800 p-3 rounded border border-cyan-700">
                    <div className="text-xs text-cyan-600 mb-1">VERDACHTSDIAGNOSE:</div>
                    <div className="text-cyan-400 font-semibold">
                      {selectedDisease !== 'custom' && selectedDisease ? 
                        commonDiseases[selectedAnimalType].find(d => d.value === selectedDisease)?.label.toUpperCase() :
                        suspectedInjury.toUpperCase()
                      }
                    </div>
                  </div>
                  
                  <div className="bg-gray-800 p-3 rounded border border-cyan-700">
                    <div className="text-xs text-cyan-600 mb-1">SYSTEM-ANALYSE:</div>
                    <div className="text-green-400">{getDiagnoseText()}</div>
                  </div>
                </div>
              </div>

              {/* Right Column - Vitals */}
              <div className="space-y-4">
                <div className="bg-gray-900/60 backdrop-blur-md rounded-lg p-6 border border-cyan-800 shadow-2xl shadow-cyan-900/50">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <Heart className="w-5 h-5 text-red-400 animate-pulse" />
                    VITALPARAMETER-ANALYSE
                  </h3>
                  
                  <div className="space-y-3">
                    {Object.entries(vitals).map(([key, value]) => {
                      const normalRange = animalNormalValues[selectedAnimalType][key];
                      const status = getValueStatus(value, normalRange.min, normalRange.max);
                      const alert = getMedicalAlert(key, value, normalRange, status);
                      
                      const labels = {
                        heartRate: 'HERZFREQUENZ',
                        temperature: 'KÖRPERTEMPERATUR',
                        bloodPressure: 'BLUTDRUCK',
                        oxygenLevel: 'O₂ SÄTTIGUNG',
                        respirationRate: 'ATEMFREQUENZ',
                        bloodGlucose: 'BLUTZUCKER'
                      };
                      
                      return (
                        <div key={key} className={`bg-gray-800 p-4 rounded border ${
                          status.status === 'normal' ? 'border-green-700' : 
                          status.status === 'warnung' ? 'border-orange-700' : 
                          'border-red-700'
                        } ${status.bgColor}`}>
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <div className="text-xs text-gray-400">{labels[key]}</div>
                              <div className={`text-2xl font-bold ${status.color} flex items-center gap-2`}>
                                <span>{status.icon}</span>
                                <span>{value}</span>
                                <span className="text-sm">{normalRange.unit}</span>
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="text-xs text-gray-500">NORMALBEREICH</div>
                              <div className="text-sm text-gray-400">
                                {normalRange.min} - {normalRange.max} {normalRange.unit}
                              </div>
                            </div>
                          </div>
                          {status.status !== 'normal' && (
                            <div className={`text-xs mt-2 p-2 rounded ${
                              status.status === 'kritisch' ? 'bg-red-900/50' : 'bg-orange-900/50'
                            }`}>
                              <div className={`font-semibold ${status.color} mb-1`}>
                                {status.status === 'kritisch' ? '⚠ KRITISCHER WERT' : '! ABWEICHUNG'}
                              </div>
                              <div className="text-gray-300">{alert}</div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
                
                <button
                  onClick={resetScan}
                  className="w-full py-3 bg-cyan-600 hover:bg-cyan-500 text-gray-900 font-bold rounded transition-all transform hover:scale-105 shadow-lg shadow-cyan-600/50"
                >
                  NEUEN SCAN STARTEN
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Status Bar */}
      <div className="fixed bottom-0 left-0 right-0 bg-gray-900/80 backdrop-blur-sm border-t border-cyan-800 p-2">
        <div className="flex items-center justify-between text-xs text-cyan-600 px-4">
          <div className="flex items-center gap-4">
            <span>SYSTEM: OPERATIONAL</span>
            <span>|</span>
            <span>DATABASE: VETERINARY v2025.1</span>
          </div>
          <div>© 2025 VetScan Technologies</div>
        </div>
      </div>
    </div>
  );
};

export default AnimalScannerPro;