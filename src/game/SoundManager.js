/**
 * Sound Manager for VetScan Pro
 * Handles background music and sound effects
 */

export class SoundManager {
  constructor() {
    this.sounds = {};
    this.musicVolume = 0.5;
    this.sfxVolume = 0.7;
    this.enabled = true;
    this.currentMusic = null;
  }

  // Initialize sound effects (Web Audio API)
  init() {
    try {
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      this.loadSounds();
    } catch (error) {
      console.warn('Web Audio API not supported:', error);
    }
  }

  // Load sound definitions
  loadSounds() {
    // Sound effects would be loaded here from audio files
    // For now, we'll use synthesized sounds

    this.soundDefinitions = {
      // UI Sounds
      click: { type: 'beep', frequency: 800, duration: 0.1 },
      success: { type: 'beep', frequency: 1200, duration: 0.2 },
      error: { type: 'beep', frequency: 400, duration: 0.3 },
      levelUp: { type: 'chord', frequencies: [523, 659, 784], duration: 0.5 },
      achievement: { type: 'chord', frequencies: [392, 494, 587], duration: 0.7 },

      // Game Sounds
      heartbeat: { type: 'pulse', frequency: 60, duration: 1.0 },
      scan: { type: 'sweep', startFreq: 200, endFreq: 800, duration: 2.0 },
      diagnose: { type: 'beep', frequency: 600, duration: 0.3 },

      // Animal Sounds (simplified)
      dog: { type: 'bark', frequency: 300, duration: 0.4 },
      cat: { type: 'meow', frequency: 500, duration: 0.3 },

      // Ambient
      clinic: { type: 'ambient', frequencies: [200, 250, 300], duration: 30 }
    };
  }

  // Play a sound effect
  play(soundName, volume = 1.0) {
    if (!this.enabled || !this.audioContext) return;

    const soundDef = this.soundDefinitions[soundName];
    if (!soundDef) {
      console.warn(`Sound '${soundName}' not found`);
      return;
    }

    try {
      const finalVolume = this.sfxVolume * volume;
      this.playSound(soundDef, finalVolume);
    } catch (error) {
      console.warn('Error playing sound:', error);
    }
  }

  // Synthesize and play sound
  playSound(soundDef, volume) {
    const oscillator = this.audioContext.createOscillator();
    const gainNode = this.audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(this.audioContext.destination);

    // Set oscillator type
    oscillator.type = this.getOscillatorType(soundDef.type);

    // Set frequency
    if (soundDef.frequency) {
      oscillator.frequency.value = soundDef.frequency;
    } else if (soundDef.startFreq && soundDef.endFreq) {
      oscillator.frequency.setValueAtTime(soundDef.startFreq, this.audioContext.currentTime);
      oscillator.frequency.exponentialRampToValueAtTime(
        soundDef.endFreq,
        this.audioContext.currentTime + soundDef.duration
      );
    }

    // Set volume envelope
    gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(volume, this.audioContext.currentTime + 0.01);
    gainNode.gain.exponentialRampToValueAtTime(
      0.01,
      this.audioContext.currentTime + soundDef.duration
    );

    // Start and stop
    oscillator.start(this.audioContext.currentTime);
    oscillator.stop(this.audioContext.currentTime + soundDef.duration);
  }

  getOscillatorType(type) {
    const types = {
      beep: 'sine',
      pulse: 'square',
      sweep: 'triangle',
      bark: 'sawtooth',
      meow: 'sine',
      chord: 'sine',
      ambient: 'sine'
    };

    return types[type] || 'sine';
  }

  // Play background music (placeholder)
  playMusic(trackName) {
    if (!this.enabled) return;

    // In a real implementation, this would load and play an audio file
    console.log(`Playing music track: ${trackName}`);
    this.currentMusic = trackName;
  }

  // Stop background music
  stopMusic() {
    if (this.currentMusic) {
      console.log(`Stopping music: ${this.currentMusic}`);
      this.currentMusic = null;
    }
  }

  // Set volumes
  setMusicVolume(volume) {
    this.musicVolume = Math.max(0, Math.min(1, volume));
  }

  setSfxVolume(volume) {
    this.sfxVolume = Math.max(0, Math.min(1, volume));
  }

  // Toggle sound
  toggle() {
    this.enabled = !this.enabled;
    if (!this.enabled) {
      this.stopMusic();
    }
    return this.enabled;
  }

  // Enable/Disable
  enable() {
    this.enabled = true;
  }

  disable() {
    this.enabled = false;
    this.stopMusic();
  }
}

// Singleton instance
let soundManagerInstance = null;

export const getSoundManager = () => {
  if (!soundManagerInstance) {
    soundManagerInstance = new SoundManager();
    soundManagerInstance.init();
  }
  return soundManagerInstance;
};

export default SoundManager;
