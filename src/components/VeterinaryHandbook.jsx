import React, { useState } from 'react';
import { Book, Search, X, Heart, Stethoscope, Activity, AlertCircle, TrendingUp, Info } from 'lucide-react';
import { ANIMAL_SPECIES, getAnimalById, getVitalSignsForAnimal } from '../veterinary-medical-data';

/**
 * Veterinary Handbook - Educational Reference System
 * Provides detailed information about animals, diseases, and medical knowledge
 */
export const VeterinaryHandbook = ({ isOpen, onClose, currentAnimal = null }) => {
  const [activeTab, setActiveTab] = useState('species'); // species, diseases, symptoms, vitals
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSpecies, setSelectedSpecies] = useState(currentAnimal);

  if (!isOpen) return null;

  const allAnimals = ANIMAL_SPECIES.slice(0, 10); // First 10 for now

  // Get selected animal data
  const animalData = selectedSpecies ? getAnimalById(selectedSpecies) : null;
  const vitalSigns = selectedSpecies ? getVitalSignsForAnimal(selectedSpecies) : null;

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden border border-cyan-800/30 shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-cyan-900/40 to-blue-900/40 p-6 border-b border-cyan-800/30">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-cyan-600/20 rounded-lg">
                <Book className="w-8 h-8 text-cyan-400" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-cyan-400">Tierärztliches Handbuch</h2>
                <p className="text-sm text-gray-400">Umfassendes medizinisches Nachschlagewerk</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <X className="w-6 h-6 text-gray-400" />
            </button>
          </div>

          {/* Search Bar */}
          <div className="mt-4 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Suche nach Tierarten, Krankheiten, Symptomen..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-cyan-300 placeholder-gray-500 focus:border-cyan-500 focus:outline-none"
            />
          </div>

          {/* Tabs */}
          <div className="mt-4 flex gap-2 overflow-x-auto">
            {[
              { id: 'species', label: '🐕 Tierarten', icon: Heart },
              { id: 'vitals', label: '💓 Vitalwerte', icon: Activity },
              { id: 'diseases', label: '🏥 Krankheiten', icon: AlertCircle },
              { id: 'comparison', label: '📊 Vergleich', icon: TrendingUp }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-lg font-medium text-sm whitespace-nowrap transition-all ${
                  activeTab === tab.id
                    ? 'bg-cyan-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-280px)] custom-scrollbar">
          {/* Species Tab */}
          {activeTab === 'species' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Species List */}
              <div>
                <h3 className="text-lg font-bold text-cyan-400 mb-4">Wähle eine Tierart</h3>
                <div className="space-y-2">
                  {allAnimals.filter(animal =>
                    !searchTerm || animal.name.toLowerCase().includes(searchTerm.toLowerCase())
                  ).map(animal => (
                    <button
                      key={animal.id}
                      onClick={() => setSelectedSpecies(animal.id)}
                      className={`w-full p-4 rounded-lg border text-left transition-all ${
                        selectedSpecies === animal.id
                          ? 'bg-cyan-900/30 border-cyan-500'
                          : 'bg-gray-800/50 border-gray-700 hover:border-cyan-600'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-4xl">{animal.model3D?.colorVariations?.[0] ? '🐕' : '🐾'}</span>
                        <div className="flex-1">
                          <div className="font-bold text-cyan-300">{animal.name}</div>
                          <div className="text-xs text-gray-400">{animal.englishName}</div>
                          <div className="text-xs text-gray-500 mt-1">
                            {animal.category === 'pet' ? '🏠 Haustier' :
                             animal.category === 'farm' ? '🚜 Nutztier' :
                             '🌴 Exotisch'}
                          </div>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Species Details */}
              {animalData && (
                <div className="space-y-4">
                  <div className="bg-gradient-to-br from-cyan-900/20 to-blue-900/20 p-6 rounded-xl border border-cyan-700/30">
                    <h3 className="text-2xl font-bold text-cyan-400 mb-2">{animalData.name}</h3>
                    <p className="text-gray-400 text-sm mb-4">{animalData.englishName}</p>

                    {/* Fun Facts */}
                    {animalData.education?.funFacts && (
                      <div className="bg-purple-900/20 p-4 rounded-lg border border-purple-700/30 mb-4">
                        <div className="font-bold text-purple-400 mb-2 flex items-center gap-2">
                          <Info className="w-5 h-5" />
                          Wusstest du?
                        </div>
                        <ul className="space-y-2">
                          {animalData.education.funFacts.slice(0, 3).map((fact, idx) => (
                            <li key={idx} className="text-sm text-gray-300">• {fact}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Common Diseases */}
                    {animalData.commonDiseases && (
                      <div className="bg-red-900/20 p-4 rounded-lg border border-red-700/30">
                        <div className="font-bold text-red-400 mb-2 flex items-center gap-2">
                          <AlertCircle className="w-5 h-5" />
                          Häufige Erkrankungen
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {animalData.commonDiseases.slice(0, 6).map((disease, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-red-900/30 text-red-300 text-xs rounded"
                            >
                              {disease}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Vital Signs Tab */}
          {activeTab === 'vitals' && (
            <div>
              <h3 className="text-lg font-bold text-cyan-400 mb-4">Vitalparameter nach Tierart</h3>

              {/* Species Selector */}
              <div className="mb-6 flex flex-wrap gap-2">
                {allAnimals.slice(0, 8).map(animal => (
                  <button
                    key={animal.id}
                    onClick={() => setSelectedSpecies(animal.id)}
                    className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
                      selectedSpecies === animal.id
                        ? 'bg-cyan-600 text-white'
                        : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                    }`}
                  >
                    {animal.name}
                  </button>
                ))}
              </div>

              {/* Vital Signs Display */}
              {vitalSigns && animalData && (
                <div className="space-y-4">
                  <div className="bg-cyan-900/20 p-4 rounded-lg border border-cyan-700/30">
                    <h4 className="font-bold text-cyan-400 mb-3 text-lg">
                      Normalwerte für {animalData.name}
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {Object.entries(vitalSigns).map(([key, value]) => {
                        const labels = {
                          heartRate: { name: '❤️ Herzfrequenz', icon: '💓' },
                          temperature: { name: '🌡️ Körpertemperatur', icon: '🌡️' },
                          respiratoryRate: { name: '💨 Atemfrequenz', icon: '💨' },
                          bloodPressure: { name: '💉 Blutdruck', icon: '💉' },
                          bloodGlucose: { name: '🩸 Blutzucker', icon: '🩸' },
                          oxygenSaturation: { name: '💧 Sauerstoffsättigung', icon: '💧' }
                        };

                        const label = labels[key];
                        if (!label) return null;

                        return (
                          <div key={key} className="bg-gray-800/50 p-4 rounded-lg">
                            <div className="text-sm font-medium text-gray-300 mb-2">{label.name}</div>
                            <div className="text-2xl font-bold text-cyan-400 mb-1">
                              {value.min} - {value.max} {value.unit}
                            </div>
                            <div className="text-xs text-gray-500">Normalbereich</div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Educational Content */}
                  <div className="bg-green-900/20 p-4 rounded-lg border border-green-700/30">
                    <div className="font-bold text-green-400 mb-2 flex items-center gap-2">
                      <Info className="w-5 h-5" />
                      Warum sind diese Werte wichtig?
                    </div>
                    <div className="space-y-2 text-sm text-gray-300">
                      <p>
                        • <strong>Herzfrequenz:</strong> Zeigt die Herzgesundheit und kann auf Stress,
                        Schmerzen oder Herzerkrankungen hinweisen.
                      </p>
                      <p>
                        • <strong>Körpertemperatur:</strong> Fieber kann auf Infektionen hindeuten,
                        niedrige Temperatur auf Schock oder Unterkühlung.
                      </p>
                      <p>
                        • <strong>Atemfrequenz:</strong> Schnelle Atmung kann auf Atemnot, Schmerzen
                        oder Stress hinweisen.
                      </p>
                      <p>
                        • <strong>Blutzucker:</strong> Wichtig für Diabetes-Diagnose und
                        Stoffwechselüberwachung.
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Diseases Tab */}
          {activeTab === 'diseases' && (
            <div>
              <h3 className="text-lg font-bold text-cyan-400 mb-4">Krankheitslexikon</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Emergency Diseases */}
                <div className="bg-red-900/20 p-4 rounded-lg border border-red-700/30">
                  <h4 className="font-bold text-red-400 mb-3 flex items-center gap-2">
                    🚨 Notfälle (kritisch)
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-red-300">Magendrehung (GDV)</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Lebensbedrohliche Verdrehung des Magens. Sofortige OP erforderlich!
                        Symptome: Aufgeblähter Bauch, Würgereiz, Unruhe.
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-red-300">Anaphylaktischer Schock</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Schwere allergische Reaktion. Symptome: Atemnot, Schwellungen, Kreislaufkollaps.
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-red-300">Hitzschlag</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Überhitzung des Körpers. Symptome: Hecheln, Speicheln, Bewusstlosigkeit.
                      </div>
                    </div>
                  </div>
                </div>

                {/* Chronic Diseases */}
                <div className="bg-yellow-900/20 p-4 rounded-lg border border-yellow-700/30">
                  <h4 className="font-bold text-yellow-400 mb-3 flex items-center gap-2">
                    📋 Chronische Erkrankungen
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-yellow-300">Diabetes mellitus</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Zuckerstoffwechselstörung. Symptome: Vermehrtes Trinken, Urinieren, Gewichtsverlust.
                        Behandlung: Insulin, Diät.
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-yellow-300">Niereninsuffizienz</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Verschlechterung der Nierenfunktion. Symptome: Erbrechen, Müdigkeit, Gewichtsverlust.
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-yellow-300">Arthritis</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Gelenkentzündung. Symptome: Lahmheit, Steifheit, Schmerzen beim Bewegen.
                      </div>
                    </div>
                  </div>
                </div>

                {/* Infectious Diseases */}
                <div className="bg-orange-900/20 p-4 rounded-lg border border-orange-700/30">
                  <h4 className="font-bold text-orange-400 mb-3 flex items-center gap-2">
                    🦠 Infektionskrankheiten
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-orange-300">Parvovirose</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Hochansteckende Viruserkrankung bei Hunden. Symptome: Blutiger Durchfall, Erbrechen.
                        Prävention: Impfung!
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-orange-300">FIV (Katzen-AIDS)</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Immunschwächevirus bei Katzen. Symptome: Wiederkehrende Infektionen, Gewichtsverlust.
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-orange-300">Tollwut</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Tödliche Viruserkrankung. Symptome: Verhaltensänderungen, Aggression, Lähmungen.
                        Impfung ist Pflicht!
                      </div>
                    </div>
                  </div>
                </div>

                {/* Parasitic Diseases */}
                <div className="bg-green-900/20 p-4 rounded-lg border border-green-700/30">
                  <h4 className="font-bold text-green-400 mb-3 flex items-center gap-2">
                    🐛 Parasitäre Erkrankungen
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-green-300">Flohbefall</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Häufigster Parasit. Symptome: Juckreiz, Kratzen, kleine braune Insekten im Fell.
                        Behandlung: Spot-on, Tabletten.
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-green-300">Zecken</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Können Krankheiten übertragen (Borreliose, Anaplasmose). Regelmäßig kontrollieren!
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-3 rounded">
                      <div className="font-bold text-green-300">Wurmbefall</div>
                      <div className="text-gray-400 text-xs mt-1">
                        Darmparasiten. Symptome: Durchfall, Gewichtsverlust, Wurmsegmente im Kot.
                        Regelmäßige Entwurmung!
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Comparison Tab */}
          {activeTab === 'comparison' && (
            <div>
              <h3 className="text-lg font-bold text-cyan-400 mb-4">Tierarten im Vergleich</h3>

              <div className="bg-cyan-900/20 p-6 rounded-lg border border-cyan-700/30 mb-4">
                <h4 className="font-bold text-cyan-400 mb-3">Herzfrequenz im Vergleich</h4>
                <div className="space-y-3">
                  {allAnimals.slice(0, 6).map(animal => {
                    const vitals = getVitalSignsForAnimal(animal.id);
                    if (!vitals?.heartRate) return null;

                    const avgRate = (vitals.heartRate.min + vitals.heartRate.max) / 2;
                    const maxPossible = 700; // Hamster max
                    const percentage = (avgRate / maxPossible) * 100;

                    return (
                      <div key={animal.id}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm text-gray-300">{animal.name}</span>
                          <span className="text-sm font-bold text-cyan-400">
                            {vitals.heartRate.min}-{vitals.heartRate.max} BPM
                          </span>
                        </div>
                        <div className="w-full bg-gray-800 rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-cyan-600 to-blue-500 h-2 rounded-full"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-purple-900/20 p-4 rounded-lg border border-purple-700/30">
                  <h4 className="font-bold text-purple-400 mb-3">🌡️ Körpertemperatur</h4>
                  <div className="space-y-2 text-sm text-gray-300">
                    <p>• <strong>Vögel:</strong> Höchste Temperatur (40-42°C)</p>
                    <p>• <strong>Säugetiere:</strong> 37-39°C durchschnittlich</p>
                    <p>• <strong>Reptilien:</strong> Wechselwarm (20-35°C)</p>
                    <p className="text-xs text-gray-500 mt-3">
                      Vögel brauchen höhere Temperaturen für ihren schnellen Stoffwechsel!
                    </p>
                  </div>
                </div>

                <div className="bg-amber-900/20 p-4 rounded-lg border border-amber-700/30">
                  <h4 className="font-bold text-amber-400 mb-3">💨 Atemfrequenz</h4>
                  <div className="space-y-2 text-sm text-gray-300">
                    <p>• <strong>Mäuse:</strong> 100-200/min (sehr schnell!)</p>
                    <p>• <strong>Hunde/Katzen:</strong> 15-30/min</p>
                    <p>• <strong>Pferde:</strong> 8-16/min (langsam)</p>
                    <p className="text-xs text-gray-500 mt-3">
                      Kleinere Tiere atmen schneller, um ihren höheren Stoffwechsel zu unterstützen.
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-blue-900/20 p-6 rounded-lg border border-blue-700/30 mt-4">
                <h4 className="font-bold text-blue-400 mb-3 flex items-center gap-2">
                  <Info className="w-5 h-5" />
                  Warum sind kleine Tiere anders?
                </h4>
                <div className="space-y-2 text-sm text-gray-300">
                  <p>
                    <strong>🐭 Kleine Tiere (Mäuse, Hamster):</strong>
                  </p>
                  <ul className="ml-4 space-y-1 text-gray-400">
                    <li>• Höherer Stoffwechsel → Schnellerer Herzschlag</li>
                    <li>• Größere Oberfläche pro Körpergewicht → Schnellerer Wärmeverlust</li>
                    <li>• Kürzere Lebenserwartung (1-3 Jahre)</li>
                    <li>• Schnellere Atmung zur Sauerstoffversorgung</li>
                  </ul>
                  <p className="mt-3">
                    <strong>🐴 Große Tiere (Pferde, Kühe):</strong>
                  </p>
                  <ul className="ml-4 space-y-1 text-gray-400">
                    <li>• Langsamerer Stoffwechsel → Langsamerer Herzschlag</li>
                    <li>• Bessere Wärmespeicherung</li>
                    <li>• Längere Lebenserwartung (20-30+ Jahre)</li>
                    <li>• Effizientere Atmung</li>
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-cyan-800/30 p-4 bg-gray-900/80">
          <div className="text-center text-sm text-gray-400">
            💡 Tipp: Nutze das Handbuch während des Spiels, um mehr über Tiere zu lernen!
          </div>
        </div>
      </div>
    </div>
  );
};

export default VeterinaryHandbook;
