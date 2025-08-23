import React, { useState, useEffect } from 'react';
import { 
  Activity, Zap, Brain, Heart, AlertCircle, CheckCircle, 
  Wifi, Search, Filter, ChevronDown, AlertTriangle, Info,
  Thermometer, Wind, Droplet, TrendingUp, Clock, Shield
} from 'lucide-react';

// Umfassende Tierdaten mit 20 Arten
const ANIMAL_SPECIES = {
  haustiere: {
    label: 'Haustiere',
    animals: [
      { id: 'hund', name: 'Hund', icon: '🐕' },
      { id: 'katze', name: 'Katze', icon: '🐈' },
      { id: 'kaninchen', name: 'Kaninchen', icon: '🐰' },
      { id: 'meerschweinchen', name: 'Meerschweinchen', icon: '🐹' },
      { id: 'hamster', name: 'Hamster', icon: '🐹' },
      { id: 'vogel', name: 'Vogel', icon: '🦜' },
      { id: 'fisch', name: 'Fisch', icon: '🐠' }
    ]
  },
  nutztiere: {
    label: 'Nutztiere',
    animals: [
      { id: 'pferd', name: 'Pferd', icon: '🐴' },
      { id: 'kuh', name: 'Kuh', icon: '🐄' },
      { id: 'schwein', name: 'Schwein', icon: '🐷' },
      { id: 'schaf', name: 'Schaf', icon: '🐑' },
      { id: 'ziege', name: 'Ziege', icon: '🐐' },
      { id: 'huhn', name: 'Huhn', icon: '🐔' }
    ]
  },
  exoten: {
    label: 'Exotische Tiere',
    animals: [
      { id: 'frettchen', name: 'Frettchen', icon: '🦦' },
      { id: 'igel', name: 'Igel', icon: '🦔' },
      { id: 'chinchilla', name: 'Chinchilla', icon: '🐭' },
      { id: 'sugar_glider', name: 'Sugar Glider', icon: '🐿️' },
      { id: 'schildkroete', name: 'Schildkröte', icon: '🐢' },
      { id: 'schlange', name: 'Schlange', icon: '🐍' },
      { id: 'echse', name: 'Echse', icon: '🦎' }
    ]
  }
};

// 50+ Medizinische Probleme kategorisiert
const MEDICAL_CONDITIONS = {
  notfaelle: {
    label: 'Notfälle',
    color: 'red',
    conditions: [
      { id: 'magendrehung', name: 'Magendrehung (GDV)', severity: 'kritisch' },
      { id: 'atemstillstand', name: 'Atemstillstand', severity: 'kritisch' },
      { id: 'schock', name: 'Schock', severity: 'kritisch' },
      { id: 'vergiftung', name: 'Vergiftung', severity: 'kritisch' },
      { id: 'hitzschlag', name: 'Hitzschlag', severity: 'kritisch' },
      { id: 'unterkuehlung', name: 'Unterkühlung', severity: 'kritisch' },
      { id: 'anaphylaxie', name: 'Anaphylaktischer Schock', severity: 'kritisch' }
    ]
  },
  infektionen: {
    label: 'Infektionskrankheiten',
    color: 'orange',
    conditions: [
      { id: 'parvovirose', name: 'Parvovirose', severity: 'hoch' },
      { id: 'staupe', name: 'Staupe', severity: 'hoch' },
      { id: 'fiv', name: 'FIV (Katzen-AIDS)', severity: 'hoch' },
      { id: 'fip', name: 'FIP', severity: 'hoch' },
      { id: 'tollwut', name: 'Tollwut', severity: 'kritisch' },
      { id: 'borreliose', name: 'Borreliose', severity: 'mittel' },
      { id: 'leptospirose', name: 'Leptospirose', severity: 'hoch' },
      { id: 'katzenseuche', name: 'Katzenseuche', severity: 'hoch' }
    ]
  },
  chronisch: {
    label: 'Chronische Erkrankungen',
    color: 'yellow',
    conditions: [
      { id: 'diabetes', name: 'Diabetes mellitus', severity: 'mittel' },
      { id: 'niereninsuffizienz', name: 'Niereninsuffizienz', severity: 'hoch' },
      { id: 'arthritis', name: 'Arthritis', severity: 'mittel' },
      { id: 'herzinsuffizienz', name: 'Herzinsuffizienz', severity: 'hoch' },
      { id: 'epilepsie', name: 'Epilepsie', severity: 'mittel' },
      { id: 'cushing', name: 'Cushing-Syndrom', severity: 'mittel' },
      { id: 'addison', name: 'Morbus Addison', severity: 'hoch' },
      { id: 'schilddruese', name: 'Schilddrüsenerkrankung', severity: 'mittel' }
    ]
  },
  orthopaedie: {
    label: 'Orthopädische Probleme',
    color: 'blue',
    conditions: [
      { id: 'fraktur', name: 'Fraktur', severity: 'hoch' },
      { id: 'kreuzbandriss', name: 'Kreuzbandriss', severity: 'hoch' },
      { id: 'hueftdysplasie', name: 'Hüftdysplasie', severity: 'mittel' },
      { id: 'ellbogendysplasie', name: 'Ellbogendysplasie', severity: 'mittel' },
      { id: 'patellaluxation', name: 'Patellaluxation', severity: 'mittel' },
      { id: 'bandscheibenvorfall', name: 'Bandscheibenvorfall', severity: 'hoch' },
      { id: 'osteosarkom', name: 'Osteosarkom', severity: 'kritisch' }
    ]
  },
  parasiten: {
    label: 'Parasitäre Erkrankungen',
    color: 'green',
    conditions: [
      { id: 'floehe', name: 'Flohbefall', severity: 'niedrig' },
      { id: 'zecken', name: 'Zeckenbefall', severity: 'niedrig' },
      { id: 'milben', name: 'Milbenbefall', severity: 'mittel' },
      { id: 'wuermer', name: 'Wurmbefall', severity: 'mittel' },
      { id: 'giardien', name: 'Giardien', severity: 'mittel' },
      { id: 'kokzidien', name: 'Kokzidien', severity: 'mittel' },
      { id: 'herzwuermer', name: 'Herzwürmer', severity: 'hoch' }
    ]
  },
  verdauung: {
    label: 'Verdauungsprobleme',
    color: 'purple',
    conditions: [
      { id: 'gastritis', name: 'Gastritis', severity: 'mittel' },
      { id: 'pankreatitis', name: 'Pankreatitis', severity: 'hoch' },
      { id: 'kolik', name: 'Kolik', severity: 'kritisch' },
      { id: 'obstipation', name: 'Obstipation', severity: 'mittel' },
      { id: 'durchfall', name: 'Durchfall', severity: 'niedrig' },
      { id: 'erbrechen', name: 'Erbrechen', severity: 'mittel' },
      { id: 'fremdkoerper', name: 'Fremdkörper', severity: 'hoch' }
    ]
  },
  haut: {
    label: 'Hauterkrankungen',
    color: 'pink',
    conditions: [
      { id: 'allergie', name: 'Allergie', severity: 'mittel' },
      { id: 'pyodermie', name: 'Pyodermie', severity: 'mittel' },
      { id: 'dermatitis', name: 'Dermatitis', severity: 'mittel' },
      { id: 'pilzinfektion', name: 'Pilzinfektion', severity: 'mittel' },
      { id: 'hotspot', name: 'Hot Spot', severity: 'mittel' },
      { id: 'abszess', name: 'Abszess', severity: 'mittel' }
    ]
  }
};

// Vitalparameter für alle Tiere
const VITAL_PARAMETERS = {
  hund: {
    heartRate: { min: 60, max: 180, unit: 'BPM' },
    temperature: { min: 37.5, max: 39.2, unit: '°C' },
    respiratoryRate: { min: 15, max: 30, unit: '/min' },
    bloodPressure: { min: 110, max: 160, unit: 'mmHg' },
    bloodGlucose: { min: 80, max: 120, unit: 'mg/dL' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' }
  },
  katze: {
    heartRate: { min: 100, max: 140, unit: 'BPM' },
    temperature: { min: 37.8, max: 39.4, unit: '°C' },
    respiratoryRate: { min: 20, max: 30, unit: '/min' },
    bloodPressure: { min: 120, max: 170, unit: 'mmHg' },
    bloodGlucose: { min: 80, max: 120, unit: 'mg/dL' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' }
  },
  pferd: {
    heartRate: { min: 28, max: 44, unit: 'BPM' },
    temperature: { min: 37.2, max: 38.3, unit: '°C' },
    respiratoryRate: { min: 8, max: 16, unit: '/min' },
    bloodPressure: { min: 120, max: 180, unit: 'mmHg' },
    bloodGlucose: { min: 70, max: 135, unit: 'mg/dL' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' }
  },
  kaninchen: {
    heartRate: { min: 180, max: 250, unit: 'BPM' },
    temperature: { min: 38.5, max: 40.0, unit: '°C' },
    respiratoryRate: { min: 30, max: 60, unit: '/min' },
    bloodPressure: { min: 90, max: 130, unit: 'mmHg' },
    bloodGlucose: { min: 75, max: 155, unit: 'mg/dL' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' }
  },
  meerschweinchen: {
    heartRate: { min: 230, max: 280, unit: 'BPM' },
    temperature: { min: 37.2, max: 39.5, unit: '°C' },
    respiratoryRate: { min: 40, max: 80, unit: '/min' },
    bloodPressure: { min: 80, max: 120, unit: 'mmHg' },
    bloodGlucose: { min: 60, max: 125, unit: 'mg/dL' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' }
  },
  hamster: {
    heartRate: { min: 250, max: 500, unit: 'BPM' },
    temperature: { min: 36.2, max: 38.0, unit: '°C' },
    respiratoryRate: { min: 35, max: 135, unit: '/min' },
    bloodPressure: { min: 80, max: 110, unit: 'mmHg' },
    bloodGlucose: { min: 50, max: 135, unit: 'mg/dL' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' }
  },
  vogel: {
    heartRate: { min: 200, max: 600, unit: 'BPM' },
    temperature: { min: 40.0, max: 42.0, unit: '°C' },
    respiratoryRate: { min: 15, max: 45, unit: '/min' },
    bloodPressure: { min: 100, max: 180, unit: 'mmHg' },
    bloodGlucose: { min: 200, max: 400, unit: 'mg/dL' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' }
  },
  // Weitere Tiere mit Standardwerten
  default: {
    heartRate: { min: 80, max: 160, unit: 'BPM' },
    temperature: { min: 37.0, max: 39.5, unit: '°C' },
    respiratoryRate: { min: 15, max: 40, unit: '/min' },
    bloodPressure: { min: 100, max: 160, unit: 'mmHg' },
    bloodGlucose: { min: 70, max: 140, unit: 'mg/dL' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' }
  }
};

const VetScanUltraAdvanced = () => {
  const [stage, setStage] = useState('input');
  const [selectedCategory, setSelectedCategory] = useState('haustiere');
  const [selectedAnimal, setSelectedAnimal] = useState('');
  const [selectedConditionCategory, setSelectedConditionCategory] = useState('');
  const [selectedCondition, setSelectedCondition] = useState('');
  const [customDiagnosis, setCustomDiagnosis] = useState('');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [scanProgress, setScanProgress] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(false);
  const [vitals, setVitals] = useState({});
  const [scanResults, setScanResults] = useState(null);

  // Scan Animation Effect
  useEffect(() => {
    if (stage === 'scanning') {
      const interval = setInterval(() => {
        setScanProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            setTimeout(() => {
              generateResults();
              setStage('results');
            }, 500);
            return 100;
          }
          return prev + 2;
        });
      }, 50);
      return () => clearInterval(interval);
    }
  }, [stage]);

  const generateResults = () => {
    const params = VITAL_PARAMETERS[selectedAnimal] || VITAL_PARAMETERS.default;
    const newVitals = {};
    
    // Generate vitals based on condition severity
    const condition = Object.values(MEDICAL_CONDITIONS)
      .flatMap(cat => cat.conditions)
      .find(c => c.id === selectedCondition);
    
    const severity = condition?.severity || 'normal';
    const variationFactor = severity === 'kritisch' ? 0.3 : 
                            severity === 'hoch' ? 0.2 : 
                            severity === 'mittel' ? 0.1 : 0.05;

    Object.entries(params).forEach(([key, range]) => {
      const mid = (range.min + range.max) / 2;
      const variation = (range.max - range.min) * variationFactor;
      let value = mid + (Math.random() - 0.5) * variation;
      
      // Ensure critical conditions show abnormal values
      if (severity === 'kritisch' && Math.random() > 0.5) {
        value = Math.random() > 0.5 ? 
          range.max + (range.max - range.min) * 0.1 : 
          range.min - (range.max - range.min) * 0.1;
      }
      
      newVitals[key] = {
        value: Math.round(value * 10) / 10,
        unit: range.unit,
        normal: { min: range.min, max: range.max },
        isNormal: value >= range.min && value <= range.max
      };
    });

    setVitals(newVitals);
    setScanResults({
      diagnosis: condition?.name || customDiagnosis || 'Unbekannte Erkrankung',
      severity: severity,
      recommendations: generateRecommendations(severity),
      timestamp: new Date().toLocaleString('de-DE')
    });
  };

  const generateRecommendations = (severity) => {
    const recommendations = {
      kritisch: [
        '🚨 SOFORTIGE NOTFALLBEHANDLUNG ERFORDERLICH',
        '📞 Notfall-Tierarzt kontaktieren',
        '🚑 Transport vorbereiten',
        '💊 Notfallmedikation bereithalten'
      ],
      hoch: [
        '⚠️ Dringende tierärztliche Behandlung notwendig',
        '📋 Vollständige Diagnostik empfohlen',
        '💉 Behandlung innerhalb 24 Stunden',
        '📊 Monitoring der Vitalparameter'
      ],
      mittel: [
        '🏥 Tierarztbesuch innerhalb 48-72 Stunden',
        '📝 Symptome dokumentieren',
        '💊 Symptomatische Behandlung möglich',
        '🔍 Weitere Beobachtung empfohlen'
      ],
      niedrig: [
        '✅ Routine-Kontrolle ausreichend',
        '📅 Nächster regulärer Check-up',
        '🏠 Heimbehandlung möglich',
        '📱 Bei Verschlechterung Tierarzt kontaktieren'
      ]
    };
    return recommendations[severity] || recommendations.niedrig;
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setUploadedImage(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const startScan = () => {
    if (selectedAnimal && (selectedCondition || customDiagnosis) && uploadedImage) {
      setStage('scanning');
      setScanProgress(0);
    }
  };

  const resetScan = () => {
    setStage('input');
    setSelectedAnimal('');
    setSelectedCondition('');
    setCustomDiagnosis('');
    setUploadedImage(null);
    setScanProgress(0);
    setVitals({});
    setScanResults(null);
  };

  const getSeverityColor = (severity) => {
    const colors = {
      kritisch: 'text-red-500 border-red-500',
      hoch: 'text-orange-500 border-orange-500',
      mittel: 'text-yellow-500 border-yellow-500',
      niedrig: 'text-green-500 border-green-500'
    };
    return colors[severity] || 'text-gray-500 border-gray-500';
  };

  if (stage === 'input') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
        {/* Header */}
        <div className="border-b border-cyan-800/50 bg-gray-900/80 backdrop-blur-xl sticky top-0 z-50">
          <div className="p-4 flex items-center justify-between max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Zap className="w-8 h-8 text-cyan-400" />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                  VetScan Ultra Pro MAX
                </h1>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <Shield className="w-4 h-4 text-green-500" />
                <span className="text-gray-400">Medical Grade v5.0</span>
              </div>
            </div>
            <div className="text-xs text-cyan-600">{new Date().toLocaleString('de-DE')}</div>
          </div>
        </div>

        {/* Main Content */}
        <div className="p-8 max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Panel - Animal Selection */}
            <div className="lg:col-span-1">
              <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
                <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <Brain className="w-5 h-5 text-cyan-400" />
                  PATIENT AUSWAHL
                </h2>

                {/* Category Tabs */}
                <div className="flex gap-2 mb-4">
                  {Object.entries(ANIMAL_SPECIES).map(([key, category]) => (
                    <button
                      key={key}
                      onClick={() => setSelectedCategory(key)}
                      className={`px-3 py-1 rounded text-xs font-medium transition-all ${
                        selectedCategory === key
                          ? 'bg-cyan-600 text-white'
                          : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                      }`}
                    >
                      {category.label}
                    </button>
                  ))}
                </div>

                {/* Animal Grid */}
                <div className="grid grid-cols-2 gap-2">
                  {ANIMAL_SPECIES[selectedCategory].animals.map(animal => (
                    <button
                      key={animal.id}
                      onClick={() => setSelectedAnimal(animal.id)}
                      className={`p-3 rounded-lg border transition-all ${
                        selectedAnimal === animal.id
                          ? 'bg-cyan-900/30 border-cyan-500 text-cyan-300'
                          : 'bg-gray-800/50 border-gray-700 text-gray-400 hover:border-cyan-600'
                      }`}
                    >
                      <div className="text-2xl mb-1">{animal.icon}</div>
                      <div className="text-xs font-medium">{animal.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Image Upload */}
              <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30 mt-4">
                <h3 className="text-sm font-bold mb-3 text-cyan-400">PATIENT SCAN-BILD</h3>
                <div className="border-2 border-dashed border-cyan-700/50 rounded-lg p-6 text-center hover:border-cyan-500 transition-colors">
                  <input
                    type="file"
                    id="imageUpload"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                  <label htmlFor="imageUpload" className="cursor-pointer">
                    {uploadedImage ? (
                      <div>
                        <img src={uploadedImage} alt="Patient" className="max-h-32 mx-auto rounded mb-2" />
                        <p className="text-xs text-green-400">✓ Bild erfolgreich geladen</p>
                      </div>
                    ) : (
                      <div>
                        <div className="text-4xl mb-2">📷</div>
                        <p className="text-sm text-gray-400">Klicken für Upload</p>
                      </div>
                    )}
                  </label>
                </div>
              </div>
            </div>

            {/* Right Panel - Condition Selection */}
            <div className="lg:col-span-2">
              <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
                <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <Activity className="w-5 h-5 text-cyan-400" />
                  DIAGNOSE AUSWAHL
                </h2>

                {/* Search Bar */}
                <div className="relative mb-4">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" />
                  <input
                    type="text"
                    placeholder="Diagnose suchen..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-cyan-300 placeholder-gray-500 focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                {/* Condition Categories */}
                <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
                  {Object.entries(MEDICAL_CONDITIONS).map(([categoryKey, category]) => {
                    const filteredConditions = category.conditions.filter(c =>
                      c.name.toLowerCase().includes(searchTerm.toLowerCase())
                    );

                    if (filteredConditions.length === 0 && searchTerm) return null;

                    return (
                      <div key={categoryKey} className="border border-gray-700 rounded-lg overflow-hidden">
                        <button
                          onClick={() => setSelectedConditionCategory(
                            selectedConditionCategory === categoryKey ? '' : categoryKey
                          )}
                          className="w-full px-4 py-3 bg-gray-800/50 hover:bg-gray-800 transition-colors flex items-center justify-between"
                        >
                          <div className="flex items-center gap-2">
                            <div className={`w-2 h-2 rounded-full bg-${category.color}-500`}></div>
                            <span className="font-medium text-sm">{category.label}</span>
                            <span className="text-xs text-gray-500">
                              ({filteredConditions.length || category.conditions.length})
                            </span>
                          </div>
                          <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${
                            selectedConditionCategory === categoryKey ? 'rotate-180' : ''
                          }`} />
                        </button>

                        {selectedConditionCategory === categoryKey && (
                          <div className="p-2 bg-gray-900/30">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                              {(searchTerm ? filteredConditions : category.conditions).map(condition => (
                                <button
                                  key={condition.id}
                                  onClick={() => setSelectedCondition(condition.id)}
                                  className={`p-3 rounded-lg border text-left transition-all ${
                                    selectedCondition === condition.id
                                      ? 'bg-cyan-900/30 border-cyan-500'
                                      : 'bg-gray-800/50 border-gray-700 hover:border-cyan-600'
                                  }`}
                                >
                                  <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                      <div className="text-sm font-medium text-cyan-300">
                                        {condition.name}
                                      </div>
                                      <div className={`text-xs mt-1 ${getSeverityColor(condition.severity)}`}>
                                        Schweregrad: {condition.severity.toUpperCase()}
                                      </div>
                                    </div>
                                    {condition.severity === 'kritisch' && (
                                      <AlertTriangle className="w-4 h-4 text-red-500 ml-2" />
                                    )}
                                  </div>
                                </button>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>

                {/* Custom Diagnosis */}
                <div className="mt-4 p-4 bg-gray-800/30 rounded-lg">
                  <label className="block text-sm font-medium mb-2 text-cyan-400">
                    Eigene Diagnose eingeben:
                  </label>
                  <input
                    type="text"
                    value={customDiagnosis}
                    onChange={(e) => {
                      setCustomDiagnosis(e.target.value);
                      if (e.target.value) setSelectedCondition('');
                    }}
                    placeholder="z.B. Verdacht auf..."
                    className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-sm text-cyan-300 placeholder-gray-500 focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                {/* Action Button */}
                <button
                  onClick={startScan}
                  disabled={!selectedAnimal || (!selectedCondition && !customDiagnosis) || !uploadedImage}
                  className={`w-full mt-6 py-4 rounded-lg font-bold transition-all flex items-center justify-center gap-2 ${
                    selectedAnimal && (selectedCondition || customDiagnosis) && uploadedImage
                      ? 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white shadow-lg shadow-cyan-500/25'
                      : 'bg-gray-800 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  <Zap className="w-5 h-5" />
                  SCAN INITIALISIEREN
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (stage === 'scanning') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center">
        <div className="max-w-2xl w-full mx-auto p-8">
          <div className="bg-gray-900/80 backdrop-blur-xl rounded-2xl p-8 border border-cyan-800/30">
            <h2 className="text-2xl font-bold mb-6 text-center flex items-center justify-center gap-3">
              <div className="animate-spin">
                <Wifi className="w-8 h-8 text-cyan-400" />
              </div>
              DEEP SCAN LÄUFT...
            </h2>

            {uploadedImage && (
              <div className="relative mb-6 rounded-xl overflow-hidden">
                <img src={uploadedImage} alt="Scanning" className="w-full opacity-50" />
                <div 
                  className="absolute inset-0 bg-gradient-to-b from-cyan-400/30 to-transparent"
                  style={{
                    transform: `translateY(${100 - scanProgress}%)`,
                    transition: 'transform 0.1s linear'
                  }}
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-6xl font-bold text-cyan-400 drop-shadow-lg">
                    {scanProgress}%
                  </div>
                </div>
              </div>
            )}

            <div className="space-y-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Fortschritt</span>
                <span className="text-cyan-400">{scanProgress}%</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-cyan-600 to-blue-500 transition-all duration-100"
                  style={{ width: `${scanProgress}%` }}
                />
              </div>

              <div className="grid grid-cols-3 gap-2 mt-4">
                <div className="text-center p-2 bg-gray-800/50 rounded">
                  <div className="text-xs text-gray-500">Analyse</div>
                  <div className={`text-sm font-bold ${scanProgress > 33 ? 'text-green-400' : 'text-gray-600'}`}>
                    {scanProgress > 33 ? '✓' : '...'} 
                  </div>
                </div>
                <div className="text-center p-2 bg-gray-800/50 rounded">
                  <div className="text-xs text-gray-500">Diagnose</div>
                  <div className={`text-sm font-bold ${scanProgress > 66 ? 'text-green-400' : 'text-gray-600'}`}>
                    {scanProgress > 66 ? '✓' : '...'}
                  </div>
                </div>
                <div className="text-center p-2 bg-gray-800/50 rounded">
                  <div className="text-xs text-gray-500">Vitaldaten</div>
                  <div className={`text-sm font-bold ${scanProgress === 100 ? 'text-green-400' : 'text-gray-600'}`}>
                    {scanProgress === 100 ? '✓' : '...'}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (stage === 'results') {
    const selectedAnimalData = Object.values(ANIMAL_SPECIES)
      .flatMap(cat => cat.animals)
      .find(a => a.id === selectedAnimal);

    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
        {/* Header */}
        <div className="border-b border-cyan-800/50 bg-gray-900/80 backdrop-blur-xl sticky top-0 z-50">
          <div className="p-4 flex items-center justify-between max-w-7xl mx-auto">
            <div className="flex items-center gap-4">
              <CheckCircle className="w-8 h-8 text-green-500" />
              <h1 className="text-2xl font-bold text-green-400">SCAN ABGESCHLOSSEN</h1>
            </div>
            <div className="text-xs text-cyan-600">{scanResults?.timestamp}</div>
          </div>
        </div>

        {/* Results Content */}
        <div className="p-8 max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Patient Info */}
            <div className="lg:col-span-1">
              <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
                <h2 className="text-lg font-bold mb-4 text-cyan-400">PATIENT INFO</h2>
                
                {uploadedImage && (
                  <img src={uploadedImage} alt="Patient" className="w-full rounded-lg mb-4" />
                )}

                <div className="space-y-3">
                  <div className="bg-gray-800/50 p-3 rounded-lg">
                    <div className="text-xs text-gray-400 mb-1">Tierart</div>
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{selectedAnimalData?.icon}</span>
                      <span className="text-cyan-300 font-medium">{selectedAnimalData?.name}</span>
                    </div>
                  </div>

                  <div className={`p-3 rounded-lg border ${getSeverityColor(scanResults?.severity)}`}>
                    <div className="text-xs text-gray-400 mb-1">Diagnose</div>
                    <div className="font-bold">{scanResults?.diagnosis}</div>
                  </div>

                  <div className="bg-gray-800/50 p-3 rounded-lg">
                    <div className="text-xs text-gray-400 mb-1">Schweregrad</div>
                    <div className={`font-bold uppercase ${getSeverityColor(scanResults?.severity)}`}>
                      {scanResults?.severity}
                    </div>
                  </div>
                </div>
              </div>

              {/* Recommendations */}
              <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30 mt-4">
                <h3 className="text-sm font-bold mb-3 text-cyan-400">EMPFEHLUNGEN</h3>
                <div className="space-y-2">
                  {scanResults?.recommendations.map((rec, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-sm">
                      <span className="text-cyan-500">{rec.split(' ')[0]}</span>
                      <span className="text-gray-300">{rec.substring(rec.indexOf(' ') + 1)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Vital Parameters */}
            <div className="lg:col-span-2">
              <div className="bg-gray-900/60 backdrop-blur-md rounded-xl p-6 border border-cyan-800/30">
                <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <Heart className="w-5 h-5 text-red-500" />
                  VITALPARAMETER ANALYSE
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(vitals).map(([key, data]) => {
                    const labels = {
                      heartRate: { name: 'Herzfrequenz', icon: '❤️' },
                      temperature: { name: 'Körpertemperatur', icon: '🌡️' },
                      respiratoryRate: { name: 'Atemfrequenz', icon: '💨' },
                      bloodPressure: { name: 'Blutdruck', icon: '💉' },
                      bloodGlucose: { name: 'Blutzucker', icon: '🩸' },
                      oxygenSaturation: { name: 'Sauerstoffsättigung', icon: '💧' }
                    };

                    const label = labels[key] || { name: key, icon: '📊' };
                    
                    return (
                      <div 
                        key={key}
                        className={`bg-gray-800/50 p-4 rounded-lg border ${
                          data.isNormal ? 'border-green-700/50' : 'border-red-700/50'
                        }`}
                      >
                        <div className="flex justify-between items-start mb-2">
                          <div className="flex items-center gap-2">
                            <span className="text-xl">{label.icon}</span>
                            <div>
                              <div className="text-xs text-gray-400">{label.name}</div>
                              <div className={`text-2xl font-bold ${
                                data.isNormal ? 'text-green-400' : 'text-red-400'
                              }`}>
                                {data.value} {data.unit}
                              </div>
                            </div>
                          </div>
                          <div className={`text-xs px-2 py-1 rounded ${
                            data.isNormal 
                              ? 'bg-green-900/30 text-green-400' 
                              : 'bg-red-900/30 text-red-400'
                          }`}>
                            {data.isNormal ? 'NORMAL' : 'ABNORMAL'}
                          </div>
                        </div>
                        <div className="mt-2 pt-2 border-t border-gray-700">
                          <div className="flex justify-between text-xs text-gray-500">
                            <span>Normalbereich:</span>
                            <span>{data.normal.min} - {data.normal.max} {data.unit}</span>
                          </div>
                          <div className="mt-1 w-full bg-gray-700 rounded-full h-2 relative overflow-hidden">
                            <div 
                              className="absolute top-0 left-0 h-full bg-green-600/30"
                              style={{
                                left: `${(data.normal.min / (data.normal.max * 1.2)) * 100}%`,
                                width: `${((data.normal.max - data.normal.min) / (data.normal.max * 1.2)) * 100}%`
                              }}
                            />
                            <div 
                              className={`absolute top-0 w-1 h-full ${
                                data.isNormal ? 'bg-green-400' : 'bg-red-400'
                              }`}
                              style={{
                                left: `${Math.min(100, Math.max(0, (data.value / (data.normal.max * 1.2)) * 100))}%`
                              }}
                            />
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 mt-6">
                  <button
                    onClick={resetScan}
                    className="flex-1 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold rounded-lg transition-all"
                  >
                    NEUEN SCAN STARTEN
                  </button>
                  <button
                    onClick={() => window.print()}
                    className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 font-bold rounded-lg transition-all"
                  >
                    📄 DRUCKEN
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default VetScanUltraAdvanced;