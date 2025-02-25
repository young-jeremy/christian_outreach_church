class PodcastPlayer {
    constructor(audioElement, options = {}) {
        this.audio = audioElement;
        this.episodeId = options.episodeId;
        this.progressBar = options.progressBar;
        this.playButton = options.playButton;
        this.timeDisplay = options.timeDisplay;
        this.speedControl = options.speedControl;
        this.volumeControl = options.volumeControl;

        this.setupEventListeners();
        this.initializeControls();
    }

    setupEventListeners() {
        // Playback controls
        this.playButton.addEventListener('click', () => this.togglePlay());

        // Progress tracking
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.progressBar.addEventListener('click', (e) => this.seek(e));

        // Analytics
        this.audio.addEventListener('play', () => this.trackAnalytics('play'));
        this.audio.addEventListener('ended', () => this.trackAnalytics('complete'));

        // Speed control
        this.speedControl.addEventListener('change', (e) => {
            this.audio.playbackRate = e.target.value;
        });

        // Volume control
        this.volumeControl.addEventListener('input', (e) => {
            this.audio.volume = e.target.value;
        });
    }

    togglePlay() {
        if (this.audio.paused) {
            this.audio.play();
            this.playButton.innerHTML = '<i class="fas fa-pause"></i>';
        } else {
            this.audio.pause();
            this.playButton.innerHTML = '<i class="fas fa-play"></i>';
        }
    }

    updateProgress() {
        const progress = (this.audio.currentTime / this.audio.duration) * 100;
        this.progressBar.value = progress;

        // Update time display
        const currentTime = this.formatTime(this.audio.currentTime);
        const duration = this.formatTime(this.audio.duration);
        this.timeDisplay.textContent = `${currentTime} / ${duration}`;
    }

    seek(event) {
        const percent = event.offsetX / this.progressBar.offsetWidth;
        this.audio.currentTime = percent * this.audio.duration;
    }

    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        seconds = Math.floor(seconds % 60);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }

    trackAnalytics(action) {
        fetch('/podcasts/analytics/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                episode_id: this.episodeId,
                action: action
            })
        });
    }

    initializeControls() {
        // Set initial volume
        this.audio.volume = this.volumeControl.value;

        // Enable speed presets
        this.speedControl.value = '1';

        // Initialize progress bar
        this.progressBar.value = 0;
    }
}