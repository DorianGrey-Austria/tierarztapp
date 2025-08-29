// Performance Manager for VetScan Pro 3000
// Professional 60 FPS target performance optimization system
// WebGL instancing, memory management, and adaptive quality

import * as THREE from 'three';

class PerformanceManager {
  constructor(renderer, scene, camera) {
    this.renderer = renderer;
    this.scene = scene;
    this.camera = camera;
    
    // Performance monitoring
    this.fpsHistory = [];
    this.frameTimeHistory = [];
    this.memoryHistory = [];
    this.lastFrameTime = performance.now();
    this.frameCount = 0;
    this.currentFPS = 60;
    this.averageFPS = 60;
    this.targetFPS = 60;
    
    // Performance budgets
    this.budgets = {
      drawCalls: 100,
      triangles: 150000,
      textures: 50,
      materials: 25,
      memory: 512 * 1024 * 1024, // 512MB
      geometries: 20
    };
    
    // Adaptive quality settings
    this.qualityLevel = 'high'; // high, medium, low
    this.adaptiveQuality = true;
    this.qualityHistory = [];
    
    // Object pooling
    this.objectPools = new Map();
    this.instancedMeshes = new Map();
    
    // Performance stats
    this.stats = {
      drawCalls: 0,
      triangles: 0,
      textures: 0,
      materials: 0,
      geometries: 0,
      memory: 0,
      shaderSwitches: 0,
      bufferSwitches: 0
    };
    
    // Optimization features
    this.frustumCulling = true;
    this.occlusionCulling = false;
    this.lodSystem = new LODSystem();
    this.textureAtlas = new TextureAtlas();
    this.shaderCache = new Map();
    
    // WebGL state optimization
    this.webglState = {
      lastProgram: null,
      lastTexture: null,
      lastBuffers: new Map(),
      lastUniforms: new Map()
    };
    
    console.log('⚡ Performance Manager initialized');
    console.log(`🎯 Target FPS: ${this.targetFPS}`);
    
    this.detectCapabilities();
    this.setupOptimizations();
    this.startMonitoring();
  }

  /**
   * Detect device capabilities for initial quality setting
   */
  detectCapabilities() {
    const canvas = this.renderer.domElement;
    const gl = this.renderer.getContext();
    
    // GPU detection
    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    const renderer = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : 'Unknown';
    const vendor = debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : 'Unknown';
    
    // Memory estimation
    const memoryInfo = performance.memory;
    const estimatedMemory = memoryInfo ? memoryInfo.usedJSHeapSize : 100 * 1024 * 1024;
    
    // Screen resolution
    const pixelRatio = window.devicePixelRatio || 1;
    const screenArea = window.screen.width * window.screen.height;
    
    // Device classification
    let deviceClass = 'high';
    
    if (renderer.includes('Mali') || renderer.includes('Adreno') || renderer.includes('PowerVR')) {
      deviceClass = 'mobile';
    } else if (renderer.includes('Intel') || screenArea < 1920 * 1080) {
      deviceClass = 'medium';
    }
    
    // Adjust budgets based on device
    if (deviceClass === 'mobile') {
      this.budgets.drawCalls = 50;
      this.budgets.triangles = 50000;
      this.budgets.textures = 20;
      this.budgets.memory = 128 * 1024 * 1024;
      this.qualityLevel = 'low';
    } else if (deviceClass === 'medium') {
      this.budgets.drawCalls = 75;
      this.budgets.triangles = 100000;
      this.budgets.textures = 35;
      this.budgets.memory = 256 * 1024 * 1024;
      this.qualityLevel = 'medium';
    }
    
    console.log(`📱 Device class: ${deviceClass}`);
    console.log(`🎮 GPU: ${renderer}`);
    console.log(`📊 Initial quality: ${this.qualityLevel}`);
  }

  /**
   * Setup initial optimizations
   */
  setupOptimizations() {
    // WebGL optimizations
    const gl = this.renderer.getContext();
    
    // Enable extensions if available
    const extensions = [
      'OES_vertex_array_object',
      'WEBGL_draw_buffers',
      'OES_texture_float',
      'WEBGL_depth_texture',
      'EXT_texture_filter_anisotropic'
    ];
    
    extensions.forEach(ext => {
      const extension = gl.getExtension(ext);
      if (extension) {
        console.log(`✅ Extension enabled: ${ext}`);
      }
    });
    
    // Renderer optimizations
    this.renderer.sortObjects = true;
    this.renderer.powerPreference = 'high-performance';
    
    // Shadow map optimizations
    if (this.renderer.shadowMap) {
      this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      this.renderer.shadowMap.autoUpdate = false;
    }
    
    // Matrix auto-update optimization
    this.scene.matrixAutoUpdate = false;
    this.scene.autoUpdate = false;
  }

  /**
   * Start performance monitoring
   */
  startMonitoring() {
    this.monitoringInterval = setInterval(() => {
      this.updateStats();
      this.checkPerformance();
      this.adaptQuality();
    }, 1000); // Check every second
  }

  /**
   * Update performance statistics
   */
  updateStats() {
    // FPS calculation
    const now = performance.now();
    const deltaTime = now - this.lastFrameTime;
    this.frameTimeHistory.push(deltaTime);
    
    if (this.frameTimeHistory.length > 60) {
      this.frameTimeHistory.shift();
    }
    
    this.currentFPS = 1000 / deltaTime;
    this.fpsHistory.push(this.currentFPS);
    
    if (this.fpsHistory.length > 60) {
      this.fpsHistory.shift();
    }
    
    // Calculate average FPS
    this.averageFPS = this.fpsHistory.reduce((a, b) => a + b, 0) / this.fpsHistory.length;
    
    // WebGL stats
    const info = this.renderer.info;
    this.stats = {
      drawCalls: info.render.calls,
      triangles: info.render.triangles,
      textures: info.memory.textures,
      geometries: info.memory.geometries,
      memory: this.estimateMemoryUsage(),
      shaderSwitches: info.programs ? info.programs.length : 0
    };
    
    this.lastFrameTime = now;
    this.frameCount++;
  }

  /**
   * Estimate memory usage
   */
  estimateMemoryUsage() {
    let memoryUsage = 0;
    
    // Texture memory
    this.scene.traverse(object => {
      if (object.material) {
        const materials = Array.isArray(object.material) ? object.material : [object.material];
        
        materials.forEach(material => {
          Object.keys(material).forEach(key => {
            if (material[key] && material[key].isTexture) {
              const texture = material[key];
              if (texture.image) {
                const size = texture.image.width * texture.image.height * 4; // RGBA
                memoryUsage += size;
              }
            }
          });
        });
      }
      
      // Geometry memory
      if (object.geometry) {
        const attributes = object.geometry.attributes;
        Object.keys(attributes).forEach(key => {
          memoryUsage += attributes[key].array.byteLength;
        });
      }
    });
    
    return memoryUsage;
  }

  /**
   * Check performance against budgets
   */
  checkPerformance() {
    const issues = [];
    
    // FPS check
    if (this.averageFPS < this.targetFPS * 0.9) {
      issues.push(`Low FPS: ${this.averageFPS.toFixed(1)}`);
    }
    
    // Budget checks
    if (this.stats.drawCalls > this.budgets.drawCalls) {
      issues.push(`Draw calls: ${this.stats.drawCalls}/${this.budgets.drawCalls}`);
    }
    
    if (this.stats.triangles > this.budgets.triangles) {
      issues.push(`Triangles: ${this.stats.triangles}/${this.budgets.triangles}`);
    }
    
    if (this.stats.textures > this.budgets.textures) {
      issues.push(`Textures: ${this.stats.textures}/${this.budgets.textures}`);
    }
    
    if (this.stats.memory > this.budgets.memory) {
      issues.push(`Memory: ${(this.stats.memory / 1024 / 1024).toFixed(1)}MB`);
    }
    
    if (issues.length > 0) {
      console.warn('⚠️ Performance issues:', issues);
    }
    
    return issues;
  }

  /**
   * Adaptive quality adjustment
   */
  adaptQuality() {
    if (!this.adaptiveQuality) return;
    
    const targetFPS = this.targetFPS;
    const currentFPS = this.averageFPS;
    const performanceRatio = currentFPS / targetFPS;
    
    let newQuality = this.qualityLevel;
    
    // Adjust quality based on performance
    if (performanceRatio < 0.8 && this.qualityLevel === 'high') {
      newQuality = 'medium';
    } else if (performanceRatio < 0.6 && this.qualityLevel === 'medium') {
      newQuality = 'low';
    } else if (performanceRatio > 1.1 && this.qualityLevel === 'low') {
      newQuality = 'medium';
    } else if (performanceRatio > 1.3 && this.qualityLevel === 'medium') {
      newQuality = 'high';
    }
    
    if (newQuality !== this.qualityLevel) {
      console.log(`🔄 Quality adjusted: ${this.qualityLevel} → ${newQuality}`);
      this.setQualityLevel(newQuality);
    }
  }

  /**
   * Set quality level and apply optimizations
   */
  setQualityLevel(level) {
    this.qualityLevel = level;
    
    const settings = {
      high: {
        shadowMapSize: 2048,
        antialias: true,
        anisotropy: 16,
        pixelRatio: Math.min(window.devicePixelRatio, 2),
        toneMapping: THREE.ReinhardToneMapping,
        toneMappingExposure: 1.0
      },
      medium: {
        shadowMapSize: 1024,
        antialias: true,
        anisotropy: 8,
        pixelRatio: Math.min(window.devicePixelRatio, 1.5),
        toneMapping: THREE.LinearToneMapping,
        toneMappingExposure: 1.0
      },
      low: {
        shadowMapSize: 512,
        antialias: false,
        anisotropy: 4,
        pixelRatio: 1,
        toneMapping: THREE.NoToneMapping,
        toneMappingExposure: 1.0
      }
    };
    
    const config = settings[level];
    
    // Apply renderer settings
    this.renderer.setPixelRatio(config.pixelRatio);
    this.renderer.toneMapping = config.toneMapping;
    this.renderer.toneMappingExposure = config.toneMappingExposure;
    
    if (this.renderer.shadowMap) {
      this.renderer.shadowMap.mapSize.setScalar(config.shadowMapSize);
    }
    
    // Update materials
    this.scene.traverse(object => {
      if (object.material) {
        const materials = Array.isArray(object.material) ? object.material : [object.material];
        
        materials.forEach(material => {
          // Adjust texture filtering
          Object.keys(material).forEach(key => {
            if (material[key] && material[key].isTexture) {
              material[key].anisotropy = config.anisotropy;
            }
          });
          
          // Disable features for low quality
          if (level === 'low') {
            if (material.normalMap) material.normalScale.setScalar(0.5);
            if (material.roughnessMap) material.roughness = 0.8;
            if (material.envMap) material.envMapIntensity = 0.3;
          }
        });
      }
    });
    
    this.qualityHistory.push({ level, timestamp: Date.now(), fps: this.averageFPS });
  }

  /**
   * GPU Instancing for multiple identical objects
   */
  createInstancedMesh(geometry, material, count, instanceId = 'default') {
    const instancedMesh = new THREE.InstancedMesh(geometry, material, count);
    instancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    
    this.instancedMeshes.set(instanceId, {
      mesh: instancedMesh,
      count: 0,
      maxCount: count
    });
    
    return instancedMesh;
  }

  /**
   * Update instanced mesh positions
   */
  updateInstancedMesh(instanceId, transforms) {
    const instanceData = this.instancedMeshes.get(instanceId);
    if (!instanceData) return;
    
    const { mesh } = instanceData;
    const matrix = new THREE.Matrix4();
    
    transforms.forEach((transform, index) => {
      if (index >= instanceData.maxCount) return;
      
      matrix.compose(transform.position, transform.rotation, transform.scale);
      mesh.setMatrixAt(index, matrix);
    });
    
    mesh.instanceMatrix.needsUpdate = true;
    instanceData.count = Math.min(transforms.length, instanceData.maxCount);
  }

  /**
   * Object pooling system
   */
  createObjectPool(poolId, createFn, resetFn, initialSize = 10) {
    const pool = {
      objects: [],
      createFn,
      resetFn,
      activeCount: 0
    };
    
    // Pre-populate pool
    for (let i = 0; i < initialSize; i++) {
      pool.objects.push(createFn());
    }
    
    this.objectPools.set(poolId, pool);
    return pool;
  }

  /**
   * Get object from pool
   */
  getFromPool(poolId) {
    const pool = this.objectPools.get(poolId);
    if (!pool) return null;
    
    let object;
    
    if (pool.objects.length > 0) {
      object = pool.objects.pop();
    } else {
      object = pool.createFn();
    }
    
    pool.activeCount++;
    return object;
  }

  /**
   * Return object to pool
   */
  returnToPool(poolId, object) {
    const pool = this.objectPools.get(poolId);
    if (!pool) return;
    
    pool.resetFn(object);
    pool.objects.push(object);
    pool.activeCount--;
  }

  /**
   * Frustum culling optimization
   */
  updateFrustumCulling() {
    if (!this.frustumCulling) return;
    
    const frustum = new THREE.Frustum();
    const matrix = new THREE.Matrix4().multiplyMatrices(
      this.camera.projectionMatrix,
      this.camera.matrixWorldInverse
    );
    frustum.setFromProjectionMatrix(matrix);
    
    this.scene.traverse(object => {
      if (object.isMesh && object.geometry) {
        if (!object.geometry.boundingSphere) {
          object.geometry.computeBoundingSphere();
        }
        
        const sphere = object.geometry.boundingSphere.clone();
        sphere.applyMatrix4(object.matrixWorld);
        
        object.visible = frustum.intersectsSphere(sphere);
      }
    });
  }

  /**
   * Optimize render order
   */
  optimizeRenderOrder() {
    // Sort transparent objects back to front
    const transparentObjects = [];
    const opaqueObjects = [];
    
    this.scene.traverse(object => {
      if (object.isMesh) {
        if (object.material && object.material.transparent) {
          transparentObjects.push(object);
        } else {
          opaqueObjects.push(object);
        }
      }
    });
    
    // Sort by distance from camera for transparent objects
    const cameraPosition = this.camera.position;
    transparentObjects.sort((a, b) => {
      const distanceA = a.position.distanceTo(cameraPosition);
      const distanceB = b.position.distanceTo(cameraPosition);
      return distanceB - distanceA; // Back to front
    });
    
    // Update render order
    opaqueObjects.forEach((obj, index) => {
      obj.renderOrder = index;
    });
    
    transparentObjects.forEach((obj, index) => {
      obj.renderOrder = opaqueObjects.length + index;
    });
  }

  /**
   * Memory cleanup
   */
  cleanupMemory() {
    // Dispose unused geometries
    const usedGeometries = new Set();
    this.scene.traverse(object => {
      if (object.geometry) {
        usedGeometries.add(object.geometry.uuid);
      }
    });
    
    // Dispose unused textures
    const usedTextures = new Set();
    this.scene.traverse(object => {
      if (object.material) {
        const materials = Array.isArray(object.material) ? object.material : [object.material];
        materials.forEach(material => {
          Object.keys(material).forEach(key => {
            if (material[key] && material[key].isTexture) {
              usedTextures.add(material[key].uuid);
            }
          });
        });
      }
    });
    
    console.log(`🧹 Memory cleanup: ${usedGeometries.size} geometries, ${usedTextures.size} textures`);
  }

  /**
   * Get performance report
   */
  getPerformanceReport() {
    return {
      fps: {
        current: this.currentFPS,
        average: this.averageFPS,
        target: this.targetFPS,
        history: this.fpsHistory.slice(-10)
      },
      stats: this.stats,
      budgets: this.budgets,
      quality: {
        current: this.qualityLevel,
        history: this.qualityHistory.slice(-5)
      },
      memory: {
        estimated: this.stats.memory,
        budget: this.budgets.memory,
        usage: (this.stats.memory / this.budgets.memory * 100).toFixed(1) + '%'
      },
      issues: this.checkPerformance()
    };
  }

  /**
   * Performance frame update (call in render loop)
   */
  update(deltaTime) {
    // Update frustum culling
    if (this.frameCount % 5 === 0) { // Every 5 frames
      this.updateFrustumCulling();
    }
    
    // Update render order
    if (this.frameCount % 10 === 0) { // Every 10 frames
      this.optimizeRenderOrder();
    }
    
    // Memory cleanup
    if (this.frameCount % 300 === 0) { // Every 5 seconds at 60fps
      this.cleanupMemory();
    }
  }

  /**
   * Dispose and cleanup
   */
  dispose() {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
    }
    
    // Dispose object pools
    this.objectPools.forEach(pool => {
      pool.objects.forEach(obj => {
        if (obj.dispose) obj.dispose();
      });
    });
    
    // Dispose instanced meshes
    this.instancedMeshes.forEach(({ mesh }) => {
      if (mesh.dispose) mesh.dispose();
    });
    
    this.objectPools.clear();
    this.instancedMeshes.clear();
    this.shaderCache.clear();
    
    console.log('🧹 Performance Manager disposed');
  }
}

/**
 * LOD (Level of Detail) System
 */
class LODSystem {
  constructor() {
    this.lodObjects = new Map();
    this.lodLevels = [
      { distance: 0, quality: 'high' },
      { distance: 50, quality: 'medium' },
      { distance: 100, quality: 'low' },
      { distance: 200, quality: 'billboard' }
    ];
  }

  addLODObject(object, lodMeshes) {
    this.lodObjects.set(object.uuid, {
      object,
      lodMeshes,
      currentLOD: 0
    });
  }

  updateLOD(cameraPosition) {
    this.lodObjects.forEach(({ object, lodMeshes }) => {
      const distance = object.position.distanceTo(cameraPosition);
      
      let newLOD = 0;
      for (let i = this.lodLevels.length - 1; i >= 0; i--) {
        if (distance >= this.lodLevels[i].distance) {
          newLOD = i;
          break;
        }
      }
      
      // Switch LOD if needed
      if (lodMeshes[newLOD] && object.children[0] !== lodMeshes[newLOD]) {
        object.clear();
        object.add(lodMeshes[newLOD]);
      }
    });
  }
}

/**
 * Texture Atlas System for reducing texture switches
 */
class TextureAtlas {
  constructor(size = 2048) {
    this.size = size;
    this.canvas = document.createElement('canvas');
    this.canvas.width = size;
    this.canvas.height = size;
    this.context = this.canvas.getContext('2d');
    
    this.texture = new THREE.CanvasTexture(this.canvas);
    this.regions = new Map();
    this.currentX = 0;
    this.currentY = 0;
    this.rowHeight = 0;
  }

  addTexture(name, imageData) {
    const img = new Image();
    img.onload = () => {
      // Find space in atlas
      if (this.currentX + img.width > this.size) {
        this.currentX = 0;
        this.currentY += this.rowHeight;
        this.rowHeight = 0;
      }
      
      if (this.currentY + img.height > this.size) {
        console.warn('Texture atlas full');
        return;
      }
      
      // Draw to atlas
      this.context.drawImage(img, this.currentX, this.currentY);
      
      // Store region info
      this.regions.set(name, {
        x: this.currentX / this.size,
        y: this.currentY / this.size,
        width: img.width / this.size,
        height: img.height / this.size
      });
      
      // Update position
      this.currentX += img.width;
      this.rowHeight = Math.max(this.rowHeight, img.height);
      
      this.texture.needsUpdate = true;
    };
    
    img.src = imageData;
  }

  getUVTransform(name) {
    return this.regions.get(name);
  }
}

export { PerformanceManager, LODSystem, TextureAtlas };