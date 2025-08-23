// Datei: src/components/BelloViewer.jsx
// Three.js Viewer für Bello mit medizinischen Visualisierungen

import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { AnimalLoader } from '../game/AnimalLoader.js';

const BelloViewer = ({ className = '' }) => {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const animalLoaderRef = useRef(null);
  const modelRef = useRef(null);
  const animationIdRef = useRef(null);
  
  const [viewMode, setViewMode] = useState('normal');
  const [isLoading, setIsLoading] = useState(true);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [selectedOrgan, setSelectedOrgan] = useState(null);
  const [error, setError] = useState(null);

  // Initialisierung der Three.js Scene
  useEffect(() => {
    if (!mountRef.current) return;

    // Scene Setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    sceneRef.current = scene;

    // Camera Setup
    const camera = new THREE.PerspectiveCamera(
      75,
      mountRef.current.clientWidth / mountRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 0, 5);

    // Renderer Setup
    const renderer = new THREE.WebGLRenderer({ 
      antialias: true, 
      alpha: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    
    mountRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Lights Setup
    setupLights(scene);

    // Controls Setup
    const controls = setupControls(camera, renderer.domElement);

    // Load Bello Model
    loadBelloModel(scene);

    // Animation Loop
    const animate = (time) => {
      animationIdRef.current = requestAnimationFrame(animate);
      
      controls.update();
      
      // Update medical visualization animations
      if (modelRef.current?.medicalViz) {
        modelRef.current.medicalViz.update(time * 0.001);
      }
      
      renderer.render(scene, camera);
    };
    animate();

    // Resize Handler
    const handleResize = () => {
      if (!mountRef.current || !camera || !renderer) return;
      
      const width = mountRef.current.clientWidth;
      const height = mountRef.current.clientHeight;
      
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }
      
      if (animalLoaderRef.current) {
        animalLoaderRef.current.dispose();
      }
      
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      
      renderer.dispose();
      controls.dispose();
    };
  }, []);

  // Licht-Setup
  const setupLights = (scene) => {
    // Ambient Light für grundlegende Beleuchtung
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    // Directional Light für Schatten
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.camera.near = 0.5;
    directionalLight.shadow.camera.far = 100;
    directionalLight.shadow.camera.left = -10;
    directionalLight.shadow.camera.right = 10;
    directionalLight.shadow.camera.top = 10;
    directionalLight.shadow.camera.bottom = -10;
    scene.add(directionalLight);

    // Spot Light für dramatische Beleuchtung
    const spotLight = new THREE.SpotLight(0x0099ff, 0.5);
    spotLight.position.set(-5, 5, 5);
    spotLight.angle = Math.PI / 6;
    spotLight.penumbra = 0.1;
    scene.add(spotLight);
  };

  // Controls Setup (OrbitControls)
  const setupControls = (camera, domElement) => {
    // Dynamischer Import für OrbitControls
    import('three/examples/jsm/controls/OrbitControls.js').then(({ OrbitControls }) => {
      const controls = new OrbitControls(camera, domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.minDistance = 2;
      controls.maxDistance = 20;
      controls.maxPolarAngle = Math.PI / 2;
      return controls;
    });

    // Fallback controls object
    return {
      update: () => {},
      dispose: () => {}
    };
  };

  // Bello Modell laden
  const loadBelloModel = async (scene) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const animalLoader = new AnimalLoader();
      animalLoaderRef.current = animalLoader;
      
      // Progress Callback
      animalLoader.onModelLoaded = (model, quality) => {
        setLoadingProgress(quality === 'low' ? 33 : quality === 'medium' ? 66 : 100);
        
        if (quality === 'high' || !modelRef.current) {
          if (modelRef.current) {
            scene.remove(modelRef.current);
          }
          scene.add(model);
          modelRef.current = model;
          
          if (quality === 'high') {
            setIsLoading(false);
          }
          
          // Setup Click Handler
          setupClickHandler(model);
        }
      };
      
      const model = await animalLoader.loadBello();
      
      if (!modelRef.current) {
        scene.add(model);
        modelRef.current = model;
        setupClickHandler(model);
      }
      
    } catch (err) {
      console.error('Failed to load Bello:', err);
      setError(`Fehler beim Laden: ${err.message}`);
      setIsLoading(false);
      
      // Zeige Fallback-Modell
      const fallback = animalLoaderRef.current?.createFallbackModel('bello');
      if (fallback) {
        scene.add(fallback);
        modelRef.current = fallback;
      }
    }
  };

  // Click Handler für Organerkennung
  const setupClickHandler = (model) => {
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const handleClick = (event) => {
      if (!mountRef.current || !sceneRef.current || !rendererRef.current) return;

      const rect = mountRef.current.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, sceneRef.current.children.find(child => child.isCamera));
      
      const intersects = raycaster.intersectObject(model, true);
      
      if (intersects.length > 0) {
        const clickedPoint = intersects[0].point;
        const organ = detectOrganFromPosition(clickedPoint, model.interactiveZones);
        setSelectedOrgan(organ);
        
        console.log('🖱️ Clicked on:', organ?.name || 'unknown area');
      }
    };

    mountRef.current.addEventListener('click', handleClick);
  };

  // Organ-Erkennung basierend auf Klickposition
  const detectOrganFromPosition = (clickPoint, zones) => {
    if (!zones) return null;
    
    for (const zone of zones) {
      if (zone.sphere.containsPoint(clickPoint)) {
        return {
          name: zone.name,
          organs: zone.organs,
          position: zone.position
        };
      }
    }
    
    return null;
  };

  // Visualisierungsmodus wechseln
  const switchVisualization = (mode) => {
    if (!animalLoaderRef.current || !modelRef.current) return;
    
    animalLoaderRef.current.switchVisualization(modelRef.current, mode);
    setViewMode(mode);
  };

  // Render UI
  if (error) {
    return (
      <div className={`flex items-center justify-center h-96 bg-red-50 border-2 border-red-200 rounded-lg ${className}`}>
        <div className="text-center">
          <div className="text-red-600 mb-2">⚠️ Fehler</div>
          <div className="text-sm text-red-500">{error}</div>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Neu laden
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`relative ${className}`}>
      {/* 3D Viewer */}
      <div ref={mountRef} className="w-full h-96 bg-gray-900 rounded-lg overflow-hidden" />
      
      {/* Loading Overlay */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-lg">
          <div className="text-center text-white">
            <div className="mb-4">🐕 Lade Bello...</div>
            <div className="w-64 bg-gray-700 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${loadingProgress}%` }}
              />
            </div>
            <div className="mt-2 text-sm">{loadingProgress}%</div>
          </div>
        </div>
      )}

      {/* Control Panel */}
      <div className="absolute top-4 left-4 bg-white bg-opacity-90 rounded-lg p-4 shadow-lg">
        <h3 className="font-bold mb-3">🔬 Untersuchungsmodi</h3>
        <div className="grid grid-cols-2 gap-2">
          {[
            { key: 'normal', label: '👁️ Normal', desc: 'Standard' },
            { key: 'xray', label: '🦴 Röntgen', desc: 'Knochen' },
            { key: 'ultrasound', label: '📡 Ultraschall', desc: 'Weichgewebe' },
            { key: 'thermal', label: '🌡️ Thermal', desc: 'Wärme' }
          ].map((mode) => (
            <button
              key={mode.key}
              onClick={() => switchVisualization(mode.key)}
              className={`p-2 rounded text-sm transition-colors ${
                viewMode === mode.key
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
              title={mode.desc}
            >
              {mode.label}
            </button>
          ))}
        </div>
      </div>

      {/* Organ Info Panel */}
      {selectedOrgan && (
        <div className="absolute bottom-4 right-4 bg-white bg-opacity-90 rounded-lg p-4 shadow-lg max-w-xs">
          <h4 className="font-bold mb-2">📍 {selectedOrgan.name}</h4>
          <div className="text-sm">
            <strong>Organe:</strong>
            <ul className="mt-1">
              {selectedOrgan.organs.map((organ, idx) => (
                <li key={idx} className="text-gray-600">• {organ}</li>
              ))}
            </ul>
          </div>
          <button
            onClick={() => setSelectedOrgan(null)}
            className="mt-2 text-xs text-gray-500 hover:text-gray-700"
          >
            Schließen
          </button>
        </div>
      )}

      {/* Help Text */}
      <div className="absolute bottom-4 left-4 text-white text-sm bg-black bg-opacity-50 rounded px-2 py-1">
        🖱️ Klicken zum Untersuchen • 🖱️ Ziehen zum Drehen • 🖱️ Scroll zum Zoomen
      </div>
    </div>
  );
};

export default BelloViewer;