// Enhanced Multi-Species Animal Loader for VetScan Pro 3000
// Professional veterinary simulator supporting 20+ animal species
// Progressive loading with quality levels and medical visualization

import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { MedicalVisualization } from '../shaders/MedicalVisualization.js';

// Species configuration mapping
const SPECIES_CONFIG = {
  // QUADRUPED SMALL
  cat: {
    name: 'Katze',
    template: 'quadruped_small',
    scale: 0.6,
    anatomyScale: 0.8,
    defaultQuality: 'tablet',
    colors: ['orange', 'black', 'white', 'tabby', 'grey']
  },
  rabbit: {
    name: 'Kaninchen', 
    template: 'quadruped_small',
    scale: 0.4,
    anatomyScale: 0.6,
    defaultQuality: 'tablet',
    colors: ['white', 'brown', 'grey', 'black_white']
  },
  guinea_pig: {
    name: 'Meerschweinchen',
    template: 'quadruped_small', 
    scale: 0.3,
    anatomyScale: 0.5,
    defaultQuality: 'tablet',
    colors: ['brown_white', 'black', 'tricolor']
  },
  ferret: {
    name: 'Frettchen',
    template: 'quadruped_small',
    scale: 0.5,
    anatomyScale: 0.7,
    defaultQuality: 'tablet', 
    colors: ['albino', 'sable', 'silver']
  },

  // QUADRUPED MEDIUM
  dog: {
    name: 'Hund',
    template: 'quadruped_medium',
    scale: 1.0,
    anatomyScale: 1.0,
    defaultQuality: 'desktop',
    colors: ['brown', 'black', 'white', 'spotted', 'golden'],
    breeds: ['labrador', 'shepherd', 'beagle', 'retriever', 'mixed']
  },
  sheep: {
    name: 'Schaf',
    template: 'quadruped_medium',
    scale: 1.2,
    anatomyScale: 1.1,
    defaultQuality: 'desktop',
    colors: ['white', 'black', 'brown']
  },
  goat: {
    name: 'Ziege', 
    template: 'quadruped_medium',
    scale: 1.0,
    anatomyScale: 0.9,
    defaultQuality: 'desktop',
    colors: ['white', 'brown', 'black_white']
  },
  pig: {
    name: 'Schwein',
    template: 'quadruped_medium',
    scale: 1.1,
    anatomyScale: 1.0,
    defaultQuality: 'desktop',
    colors: ['pink', 'black', 'spotted']
  },

  // QUADRUPED LARGE
  horse: {
    name: 'Pferd',
    template: 'quadruped_large', 
    scale: 2.5,
    anatomyScale: 2.0,
    defaultQuality: 'desktop',
    colors: ['brown', 'black', 'white', 'chestnut', 'grey']
  },
  cow: {
    name: 'Kuh',
    template: 'quadruped_large',
    scale: 2.2,
    anatomyScale: 1.8,
    defaultQuality: 'desktop',
    colors: ['black_white', 'brown', 'holstein', 'jersey']
  },
  llama: {
    name: 'Lama',
    template: 'quadruped_large',
    scale: 1.8, 
    anatomyScale: 1.5,
    defaultQuality: 'desktop',
    colors: ['white', 'brown', 'grey', 'mixed']
  },

  // BIRDS
  canary: {
    name: 'Kanarienvogel',
    template: 'bird_small',
    scale: 0.15,
    anatomyScale: 0.2,
    defaultQuality: 'tablet',
    colors: ['yellow', 'orange', 'white']
  },
  budgie: {
    name: 'Wellensittich', 
    template: 'bird_small',
    scale: 0.18,
    anatomyScale: 0.2,
    defaultQuality: 'tablet',
    colors: ['green_yellow', 'blue', 'white']
  },
  parrot: {
    name: 'Papagei',
    template: 'bird_medium',
    scale: 0.4,
    anatomyScale: 0.4,
    defaultQuality: 'desktop',
    colors: ['green_red', 'blue_yellow', 'grey']
  },
  chicken: {
    name: 'Huhn',
    template: 'bird_medium', 
    scale: 0.5,
    anatomyScale: 0.5,
    defaultQuality: 'desktop',
    colors: ['brown', 'white', 'black', 'red_brown']
  },

  // REPTILES
  snake: {
    name: 'Schlange',
    template: 'reptile_snake',
    scale: 1.5,
    anatomyScale: 1.0,
    defaultQuality: 'desktop',
    colors: ['green', 'brown', 'patterned']
  },
  lizard: {
    name: 'Echse',
    template: 'reptile_lizard',
    scale: 0.3,
    anatomyScale: 0.4,
    defaultQuality: 'tablet',
    colors: ['green', 'brown', 'blue']
  },
  turtle: {
    name: 'Schildkröte',
    template: 'reptile_turtle',
    scale: 0.6,
    anatomyScale: 0.7,
    defaultQuality: 'desktop', 
    colors: ['green_brown', 'olive', 'dark_green']
  },

  // AQUATIC  
  goldfish: {
    name: 'Goldfisch',
    template: 'fish',
    scale: 0.2,
    anatomyScale: 0.3,
    defaultQuality: 'tablet',
    colors: ['gold', 'orange', 'white', 'calico']
  }
};

const QUALITY_LEVELS = {
  mobile: {
    vertices: 800,
    loadPriority: 1,
    features: ['basic_materials'],
    compression: 'draco_high'
  },
  tablet: {
    vertices: 3000,
    loadPriority: 2,
    features: ['basic_materials', 'simple_shaders'],
    compression: 'draco_medium'
  },
  desktop: {
    vertices: 12000,
    loadPriority: 3,
    features: ['advanced_materials', 'medical_shaders', 'anatomy_zones'],
    compression: 'draco_low'
  },
  pro: {
    vertices: 40000,
    loadPriority: 4,
    features: ['ultra_materials', 'advanced_shaders', 'realtime_simulation'],
    compression: 'none'
  }
};

class MultiSpeciesLoader {
  constructor() {
    this.loader = new GLTFLoader();
    this.dracoLoader = new DRACOLoader();
    
    // Setup DRACO compression
    this.dracoLoader.setDecoderPath('/draco/');
    this.loader.setDRACOLoader(this.dracoLoader);
    
    // Cache management
    this.loadedAnimals = new Map(); // species_id + quality -> model
    this.loadingPromises = new Map(); // track ongoing loads
    this.assetCache = new Map(); // GLB asset cache
    
    // Performance monitoring
    this.loadTimes = new Map();
    this.memoryUsage = 0;
    this.maxMemory = this.detectMemoryLimit();
    
    // Progress tracking
    this.loadingCallbacks = new Set();
    
    console.log('🚀 MultiSpeciesLoader initialized');
    console.log(`📊 Memory limit: ${this.maxMemory}MB`);
    console.log(`📋 Available species: ${Object.keys(SPECIES_CONFIG).length}`);
  }

  /**
   * Detect device memory limits for quality selection
   */
  detectMemoryLimit() {
    // Detect device capabilities
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
    
    if (!gl) return 256; // Fallback for very old devices
    
    // Estimate based on WebGL capabilities
    const renderer = gl.getParameter(gl.RENDERER) || '';
    const vendor = gl.getParameter(gl.VENDOR) || '';
    
    if (renderer.includes('Mali') || renderer.includes('Adreno')) {
      return 512; // Mobile GPU
    } else if (renderer.includes('Intel')) {
      return 1024; // Integrated graphics
    } else {
      return 2048; // Dedicated graphics
    }
  }

  /**
   * Auto-select quality level based on device capabilities
   */
  selectQualityLevel(speciesId, preferredQuality = null) {
    if (preferredQuality && QUALITY_LEVELS[preferredQuality]) {
      return preferredQuality;
    }
    
    const config = SPECIES_CONFIG[speciesId];
    if (!config) return 'tablet';
    
    // Device-based selection
    const devicePixelRatio = window.devicePixelRatio || 1;
    const screenArea = window.screen.width * window.screen.height;
    const isLowEnd = screenArea < 1000000 || devicePixelRatio < 1.5;
    const isHighEnd = screenArea > 2000000 && devicePixelRatio >= 2;
    
    if (isLowEnd) return 'mobile';
    if (isHighEnd && this.maxMemory > 1024) return 'desktop';
    return config.defaultQuality || 'tablet';
  }

  /**
   * Load animal with progressive quality enhancement
   */
  async loadAnimal(speciesId, patientId = 'default', options = {}) {
    const cacheKey = `${speciesId}_${patientId}`;
    
    // Check cache first
    if (this.loadedAnimals.has(cacheKey)) {
      console.log(`📦 Loaded ${speciesId} from cache`);
      return this.loadedAnimals.get(cacheKey);
    }
    
    // Check if already loading
    if (this.loadingPromises.has(cacheKey)) {
      return this.loadingPromises.get(cacheKey);
    }
    
    const loadPromise = this.loadAnimalProgressive(speciesId, patientId, options);
    this.loadingPromises.set(cacheKey, loadPromise);
    
    try {
      const animal = await loadPromise;
      this.loadedAnimals.set(cacheKey, animal);
      return animal;
    } catch (error) {
      console.error(`❌ Failed to load ${speciesId}:`, error);
      this.loadingPromises.delete(cacheKey);
      throw error;
    }
  }

  /**
   * Progressive loading implementation
   */
  async loadAnimalProgressive(speciesId, patientId, options = {}) {
    const config = SPECIES_CONFIG[speciesId];
    if (!config) {
      throw new Error(`Unknown species: ${speciesId}`);
    }
    
    console.log(`🐕 Loading ${config.name} (${speciesId})...`);
    
    const startTime = Date.now();
    const qualityLevel = this.selectQualityLevel(speciesId, options.quality);
    
    // 1. Immediate: Create fallback model
    let currentModel = this.createFallbackModel(speciesId, config);
    
    // Notify progress
    this.notifyProgress(speciesId, 'fallback', 10);
    
    try {
      // 2. Progressive loading chain
      const qualityChain = this.buildQualityChain(qualityLevel);
      
      for (let i = 0; i < qualityChain.length; i++) {
        const quality = qualityChain[i];
        const progress = 20 + (i / qualityChain.length) * 70;
        
        try {
          console.log(`📊 Loading ${speciesId} - ${quality} quality...`);
          this.notifyProgress(speciesId, quality, progress);
          
          const gltf = await this.loadGLTF(speciesId, quality);
          const newModel = this.processLoadedModel(gltf.scene, speciesId, config, quality);
          
          // Replace current model with higher quality
          if (currentModel && currentModel.parent) {
            this.replaceModel(currentModel, newModel);
          }
          currentModel = newModel;
          
          // Early return for mobile devices after first successful load
          if (quality === 'mobile' && qualityChain.length > 1) {
            this.scheduleQualityUpgrade(currentModel, speciesId, qualityChain.slice(i + 1));
            break;
          }
          
        } catch (error) {
          console.warn(`⚠️ Failed to load ${quality} quality for ${speciesId}:`, error);
          if (i === 0) {
            // If even the lowest quality fails, keep fallback
            console.log(`🔧 Using fallback model for ${speciesId}`);
          }
        }
      }
      
      // Final setup
      this.setupAnimal(currentModel, speciesId, patientId, config);
      
      const loadTime = Date.now() - startTime;
      this.loadTimes.set(speciesId, loadTime);
      console.log(`✅ ${config.name} loaded in ${loadTime}ms`);
      
      this.notifyProgress(speciesId, 'complete', 100);
      return currentModel;
      
    } catch (error) {
      console.error(`❌ Failed to load ${speciesId}:`, error);
      // Return fallback on complete failure
      this.setupAnimal(currentModel, speciesId, patientId, config);
      return currentModel;
    }
  }

  /**
   * Build quality loading chain based on target quality
   */
  buildQualityChain(targetQuality) {
    const qualities = ['mobile', 'tablet', 'desktop', 'pro'];
    const targetIndex = qualities.indexOf(targetQuality);
    
    if (targetIndex === -1) return ['tablet'];
    
    // Progressive chain: start from mobile, go up to target
    return qualities.slice(0, targetIndex + 1);
  }

  /**
   * Load GLB file for specific species and quality
   */
  async loadGLTF(speciesId, quality) {
    const assetPath = `./assets/models/animals/${speciesId}/${speciesId}_${quality}.glb`;
    const cacheKey = `${speciesId}_${quality}`;
    
    // Check asset cache
    if (this.assetCache.has(cacheKey)) {
      return this.assetCache.get(cacheKey);
    }
    
    return new Promise((resolve, reject) => {
      this.loader.load(
        assetPath,
        (gltf) => {
          this.assetCache.set(cacheKey, gltf);
          resolve(gltf);
        },
        (progress) => {
          const percent = (progress.loaded / progress.total * 100).toFixed(1);
          console.log(`📦 Loading ${speciesId}_${quality}: ${percent}%`);
        },
        (error) => {
          console.error(`❌ Failed to load ${assetPath}:`, error);
          reject(error);
        }
      );
    });
  }

  /**
   * Process loaded GLTF model
   */
  processLoadedModel(scene, speciesId, config, quality) {
    const model = scene.clone();
    model.name = `${speciesId}_${quality}`;
    
    // Scale according to species config
    model.scale.setScalar(config.scale);
    
    // Center the model
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    
    // Setup materials and shadows
    this.setupModelMaterials(model, quality);
    this.setupModelShadows(model);
    
    return model;
  }

  /**
   * Setup model materials based on quality level
   */
  setupModelMaterials(model, quality) {
    const qualityConfig = QUALITY_LEVELS[quality];
    
    model.traverse((child) => {
      if (child.isMesh && child.material) {
        // Enable features based on quality level
        if (qualityConfig.features.includes('advanced_materials')) {
          child.material.roughness = 0.8;
          child.material.metalness = 0.1;
          child.material.envMapIntensity = 0.5;
        }
        
        // Optimize for performance
        if (quality === 'mobile') {
          child.material.flatShading = true;
          child.material.envMapIntensity = 0;
        }
        
        child.material.needsUpdate = true;
      }
    });
  }

  /**
   * Setup model shadows
   */
  setupModelShadows(model) {
    model.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true;
        child.receiveShadow = true;
      }
    });
  }

  /**
   * Replace model with higher quality version
   */
  replaceModel(oldModel, newModel) {
    if (!oldModel.parent) return;
    
    // Copy transform
    newModel.position.copy(oldModel.position);
    newModel.rotation.copy(oldModel.rotation);
    newModel.scale.copy(oldModel.scale);
    
    // Copy medical visualization state
    if (oldModel.medicalViz && newModel) {
      const currentMode = oldModel.medicalViz.currentMode;
      newModel.medicalViz = new MedicalVisualization(newModel);
      newModel.medicalViz.switchMode(currentMode);
    }
    
    // Copy user data
    newModel.userData = { ...oldModel.userData };
    
    // Replace in scene
    oldModel.parent.add(newModel);
    oldModel.parent.remove(oldModel);
    
    // Dispose old model
    this.disposeModel(oldModel);
    
    console.log(`🔄 Replaced ${oldModel.name} with ${newModel.name}`);
  }

  /**
   * Schedule quality upgrade for later
   */
  scheduleQualityUpgrade(model, speciesId, remainingQualities) {
    if (remainingQualities.length === 0) return;
    
    // Upgrade after 2 seconds to not block UI
    setTimeout(async () => {
      try {
        const nextQuality = remainingQualities[0];
        const gltf = await this.loadGLTF(speciesId, nextQuality);
        const config = SPECIES_CONFIG[speciesId];
        const newModel = this.processLoadedModel(gltf.scene, speciesId, config, nextQuality);
        
        this.replaceModel(model, newModel);
        
        // Continue with remaining qualities
        if (remainingQualities.length > 1) {
          this.scheduleQualityUpgrade(newModel, speciesId, remainingQualities.slice(1));
        }
      } catch (error) {
        console.warn(`⚠️ Background quality upgrade failed for ${speciesId}:`, error);
      }
    }, 2000);
  }

  /**
   * Create fallback procedural model
   */
  createFallbackModel(speciesId, config) {
    console.log(`🔧 Creating fallback model for ${speciesId}`);
    
    // Basic geometry based on template
    let geometry, material;
    
    if (config.template.includes('quadruped')) {
      geometry = new THREE.BoxGeometry(1.5, 0.8, 0.6);
      material = new THREE.MeshLambertMaterial({ color: 0x8B4513 });
    } else if (config.template.includes('bird')) {
      geometry = new THREE.SphereGeometry(0.3, 8, 6);
      material = new THREE.MeshLambertMaterial({ color: 0x4169E1 });
    } else if (config.template.includes('fish')) {
      geometry = new THREE.CylinderGeometry(0.1, 0.2, 0.8, 8);
      material = new THREE.MeshLambertMaterial({ color: 0xFFD700 });
    } else {
      geometry = new THREE.BoxGeometry(1, 1, 1);
      material = new THREE.MeshLambertMaterial({ color: 0x808080 });
    }
    
    const mesh = new THREE.Mesh(geometry, material);
    const group = new THREE.Group();
    group.add(mesh);
    group.name = `${speciesId}_fallback`;
    group.scale.setScalar(config.scale);
    
    return group;
  }

  /**
   * Final animal setup with medical systems
   */
  setupAnimal(model, speciesId, patientId, config) {
    // Add medical visualization
    if (!model.medicalViz) {
      model.medicalViz = new MedicalVisualization(model);
    }
    
    // Add anatomy markers
    this.createAnatomyMarkers(model, speciesId, config);
    
    // Add species metadata
    model.userData = {
      speciesId: speciesId,
      patientId: patientId,
      speciesName: config.name,
      template: config.template,
      interactive: true,
      loadTime: this.loadTimes.get(speciesId) || 0
    };
    
    console.log(`🎯 ${config.name} setup completed`);
  }

  /**
   * Create anatomy interaction markers
   */
  createAnatomyMarkers(model, speciesId, config) {
    const anatomyScale = config.anatomyScale || 1.0;
    
    const markers = [
      { name: 'heart', position: [0.3, 0.6, 0.0], radius: 0.1 * anatomyScale },
      { name: 'lungs', position: [0.35, 0.65, 0.0], radius: 0.12 * anatomyScale },
      { name: 'stomach', position: [0.0, 0.4, 0.0], radius: 0.15 * anatomyScale },
      { name: 'liver', position: [-0.2, 0.45, 0.15], radius: 0.1 * anatomyScale },
      { name: 'brain', position: [0.6, 0.8, 0.0], radius: 0.08 * anatomyScale }
    ];
    
    model.anatomyMarkers = markers.map(marker => ({
      ...marker,
      position: new THREE.Vector3(...marker.position).multiplyScalar(config.scale),
      sphere: new THREE.Sphere(
        new THREE.Vector3(...marker.position).multiplyScalar(config.scale),
        marker.radius
      )
    }));
    
    console.log(`🫀 Created ${markers.length} anatomy markers for ${speciesId}`);
  }

  /**
   * Progress notification system
   */
  notifyProgress(speciesId, stage, progress) {
    const event = {
      speciesId,
      stage,
      progress,
      timestamp: Date.now()
    };
    
    this.loadingCallbacks.forEach(callback => {
      try {
        callback(event);
      } catch (error) {
        console.error('❌ Progress callback error:', error);
      }
    });
  }

  /**
   * Add progress callback
   */
  onProgress(callback) {
    this.loadingCallbacks.add(callback);
    return () => this.loadingCallbacks.delete(callback);
  }

  /**
   * Get available species list
   */
  getAvailableSpecies() {
    return Object.keys(SPECIES_CONFIG).map(id => ({
      id,
      name: SPECIES_CONFIG[id].name,
      template: SPECIES_CONFIG[id].template,
      scale: SPECIES_CONFIG[id].scale
    }));
  }

  /**
   * Get species configuration
   */
  getSpeciesConfig(speciesId) {
    return SPECIES_CONFIG[speciesId] || null;
  }

  /**
   * Memory and performance management
   */
  getMemoryUsage() {
    return {
      loadedAnimals: this.loadedAnimals.size,
      cachedAssets: this.assetCache.size,
      estimatedMemory: this.memoryUsage,
      maxMemory: this.maxMemory
    };
  }

  /**
   * Dispose model and free memory
   */
  disposeModel(model) {
    if (!model) return;
    
    model.traverse((child) => {
      if (child.geometry) {
        child.geometry.dispose();
      }
      if (child.material) {
        if (Array.isArray(child.material)) {
          child.material.forEach(mat => mat.dispose());
        } else {
          child.material.dispose();
        }
      }
    });
    
    if (model.medicalViz) {
      model.medicalViz.dispose();
    }
  }

  /**
   * Clear cache and free memory
   */
  clearCache() {
    // Dispose loaded animals
    this.loadedAnimals.forEach(model => this.disposeModel(model));
    this.loadedAnimals.clear();
    
    // Clear asset cache
    this.assetCache.clear();
    
    // Clear loading promises
    this.loadingPromises.clear();
    
    this.memoryUsage = 0;
    console.log('🧹 MultiSpeciesLoader cache cleared');
  }

  /**
   * Cleanup and disposal
   */
  dispose() {
    this.clearCache();
    this.dracoLoader.dispose();
    this.loadingCallbacks.clear();
    console.log('🧹 MultiSpeciesLoader disposed');
  }
}

export { MultiSpeciesLoader, SPECIES_CONFIG, QUALITY_LEVELS };