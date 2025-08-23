// Datei: src/game/AnimalLoader.js
// 3D Tierlader für das Veterinärspiel mit progressiver Qualität

import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { MedicalVisualization } from '../shaders/MedicalVisualization.js';

class AnimalLoader {
  constructor() {
    this.loader = new GLTFLoader();
    this.dracoLoader = new DRACOLoader();
    
    // Setup DRACO compression
    this.dracoLoader.setDecoderPath('/draco/');
    this.loader.setDRACOLoader(this.dracoLoader);
    
    this.loadedAnimals = new Map();
    this.loadingPromises = new Map();
  }

  /**
   * Lädt Bello progressiv mit verschiedenen Qualitätsstufen
   * @returns {Promise<THREE.Group>} Das geladene 3D-Modell
   */
  async loadBello() {
    if (this.loadedAnimals.has('bello')) {
      return this.loadedAnimals.get('bello');
    }

    if (this.loadingPromises.has('bello')) {
      return this.loadingPromises.get('bello');
    }

    const loadPromise = this.loadProgressively('bello', [
      './assets/models/animals/bello/bello_low.glb',
      './assets/models/animals/bello/bello_medium.glb',
      './assets/models/animals/bello/bello_high.glb'
    ]);

    this.loadingPromises.set('bello', loadPromise);
    
    try {
      const model = await loadPromise;
      this.loadedAnimals.set('bello', model);
      return model;
    } catch (error) {
      console.error('Failed to load Bello:', error);
      this.loadingPromises.delete('bello');
      throw error;
    }
  }

  /**
   * Progressives Laden mit Qualitätsstufen
   * @param {string} animalName Name des Tieres
   * @param {string[]} modelPaths Pfade in aufsteigender Qualität
   */
  async loadProgressively(animalName, modelPaths) {
    let currentModel = null;
    
    for (let i = 0; i < modelPaths.length; i++) {
      const path = modelPaths[i];
      const quality = ['low', 'medium', 'high'][i];
      
      try {
        console.log(`🐕 Loading ${animalName} - ${quality} quality...`);
        const gltf = await this.loadGLTF(path);
        
        if (currentModel) {
          // Ersetze das vorherige Modell mit besserer Qualität
          this.replaceModel(currentModel, gltf.scene);
        } else {
          currentModel = gltf.scene;
          currentModel.name = animalName;
          
          // Setup initial properties
          this.setupModel(currentModel, animalName);
          
          // Initialisiere Medical Visualizations
          currentModel.medicalViz = new MedicalVisualization(currentModel);
          
          // Setup Interaktionen
          this.setupInteractions(currentModel);
          
          // Gib sofort das erste Modell zurück für schnelles Feedback
          setTimeout(() => this.onModelLoaded?.(currentModel, quality), 0);
        }
        
        console.log(`✅ ${animalName} ${quality} quality loaded`);
        
      } catch (error) {
        console.warn(`⚠️ Failed to load ${quality} quality for ${animalName}:`, error);
        if (i === 0) {
          // Wenn auch das Low-Quality Modell fehlschlägt, verwende Fallback
          return this.createFallbackModel(animalName);
        }
      }
    }
    
    return currentModel;
  }

  /**
   * Lädt eine GLTF-Datei
   * @param {string} path Pfad zur GLTF-Datei
   */
  loadGLTF(path) {
    return new Promise((resolve, reject) => {
      this.loader.load(
        path,
        (gltf) => resolve(gltf),
        (progress) => {
          const percent = (progress.loaded / progress.total * 100).toFixed(1);
          console.log(`📦 Loading progress: ${percent}%`);
        },
        (error) => reject(error)
      );
    });
  }

  /**
   * Ersetzt ein Modell mit höherer Qualität
   */
  replaceModel(oldModel, newModel) {
    // Kopiere Position, Rotation und Scale
    newModel.position.copy(oldModel.position);
    newModel.rotation.copy(oldModel.rotation);
    newModel.scale.copy(oldModel.scale);
    
    // Kopiere Medical Visualization State
    if (oldModel.medicalViz) {
      const currentMode = oldModel.medicalViz.currentMode;
      newModel.medicalViz = new MedicalVisualization(newModel);
      newModel.medicalViz.switchMode(currentMode);
    }
    
    // Ersetze im Parent
    if (oldModel.parent) {
      oldModel.parent.add(newModel);
      oldModel.parent.remove(oldModel);
    }
  }

  /**
   * Setup grundlegender Modelleigenschaften
   */
  setupModel(model, animalName) {
    // Zentriere das Modell
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    
    // Skaliere für optimale Größe
    const size = box.getSize(new THREE.Vector3());
    const maxDimension = Math.max(size.x, size.y, size.z);
    const targetSize = 2; // Gewünschte Maximalgröße
    model.scale.multiplyScalar(targetSize / maxDimension);
    
    // Aktiviere Schatten
    model.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
        
        // Stelle sicher, dass Materialien korrekt sind
        if (child.material) {
          child.material.needsUpdate = true;
        }
      }
    });
    
    console.log(`🎯 ${animalName} model setup completed`);
  }

  /**
   * Setup von Interaktionen (Klicks, Hover etc.)
   */
  setupInteractions(model) {
    // Füge interaktive Zonen hinzu
    const interactiveZones = this.createInteractiveZones(model);
    model.interactiveZones = interactiveZones;
    
    // Event Handlers werden vom Haupt-Viewer hinzugefügt
    model.userData.interactive = true;
    
    console.log(`🖱️ Interactive zones set up for ${model.name}`);
  }

  /**
   * Erstellt interaktive Bereiche für Untersuchungen
   */
  createInteractiveZones(model) {
    const zones = [
      { name: 'head', position: [0, 1, 0], organs: ['brain', 'eyes', 'ears'] },
      { name: 'chest', position: [0, 0.5, 0], organs: ['heart', 'lungs'] },
      { name: 'abdomen', position: [0, 0, 0], organs: ['stomach', 'liver', 'kidneys'] },
      { name: 'legs', position: [0, -0.5, 0], organs: ['bones', 'joints'] }
    ];
    
    return zones.map(zone => ({
      ...zone,
      position: new THREE.Vector3(...zone.position),
      sphere: new THREE.Sphere(new THREE.Vector3(...zone.position), 0.3)
    }));
  }

  /**
   * Wechselt zwischen Visualisierungsmodi
   * @param {THREE.Group} model Das Tiermodell
   * @param {string} mode 'normal' | 'xray' | 'ultrasound' | 'mri' | 'thermal'
   */
  switchVisualization(model, mode) {
    if (!model.medicalViz) {
      console.warn('Medical visualization not initialized for model');
      return;
    }
    
    model.medicalViz.switchMode(mode);
    console.log(`🔬 Switched to ${mode} visualization mode`);
  }

  /**
   * Erstellt ein Fallback-Modell bei Ladefehlern
   */
  createFallbackModel(animalName) {
    const geometry = new THREE.BoxGeometry(1, 1, 2);
    const material = new THREE.MeshLambertMaterial({ 
      color: 0x8B4513,
      transparent: true,
      opacity: 0.8
    });
    
    const mesh = new THREE.Mesh(geometry, material);
    const group = new THREE.Group();
    group.add(mesh);
    group.name = `${animalName}_fallback`;
    
    // Einfache Medical Visualization für Fallback
    group.medicalViz = {
      switchMode: (mode) => {
        console.log(`Fallback model - switched to ${mode} mode`);
        switch(mode) {
          case 'xray':
            material.opacity = 0.3;
            material.color.setHex(0x404040);
            break;
          default:
            material.opacity = 0.8;
            material.color.setHex(0x8B4513);
        }
      },
      currentMode: 'normal'
    };
    
    console.log(`🔧 Created fallback model for ${animalName}`);
    return group;
  }

  /**
   * Cleanup und Ressourcen freigeben
   */
  dispose() {
    this.loadedAnimals.forEach((model) => {
      model.traverse((child) => {
        if (child.geometry) {
          child.geometry.dispose();
        }
        if (child.material) {
          if (Array.isArray(child.material)) {
            child.material.forEach(material => material.dispose());
          } else {
            child.material.dispose();
          }
        }
      });
    });
    
    this.loadedAnimals.clear();
    this.loadingPromises.clear();
    this.dracoLoader.dispose();
    
    console.log('🧹 AnimalLoader disposed');
  }
}

export { AnimalLoader };