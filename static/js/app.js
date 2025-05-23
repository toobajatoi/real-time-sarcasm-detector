// Initialize WebSocket connection
const socket = io();

// Audio recording variables
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let audioContext;
let analyser;
let dataArray;
let animationFrame;
let recordingStartTime;
let recordingDuration = 0;

// DOM elements
const recordButton = document.getElementById('recordButton');
const recordIcon = document.getElementById('recordIcon');
const recordText = document.getElementById('recordText');
const visualizer = document.getElementById('visualizer');
const results = document.getElementById('results');
const loading = document.getElementById('loading');

// Initialize audio context and analyzer
async function initAudio() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);
        
        analyser.fftSize = 512; // Increased for better visualization
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
        
        mediaRecorder = new MediaRecorder(stream);
        setupMediaRecorder();
        
        // Add success message
        showNotification('Microphone access granted! You can start recording.', 'success');
    } catch (err) {
        console.error('Error accessing microphone:', err);
        showNotification('Error accessing microphone. Please ensure you have granted microphone permissions.', 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg transform transition-all duration-500 translate-x-full ${
        type === 'error' ? 'bg-red-500' : 'bg-blue-500'
    } text-white`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(full)';
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// Setup media recorder event handlers
function setupMediaRecorder() {
    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
            socket.emit('audio_data', { audio: reader.result });
        };
        audioChunks = [];
    };
}

// Visualize audio
function visualize() {
    if (!isRecording) return;
    
    analyser.getByteFrequencyData(dataArray);
    const canvas = document.createElement('canvas');
    canvas.width = visualizer.clientWidth;
    canvas.height = visualizer.clientHeight;
    const ctx = canvas.getContext('2d');
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Create gradient background
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, '#3b82f6');
    gradient.addColorStop(1, '#8b5cf6');
    
    const barWidth = (canvas.width / dataArray.length) * 2.5;
    let x = 0;
    
    for (let i = 0; i < dataArray.length; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height;
        
        // Create gradient for each bar
        const barGradient = ctx.createLinearGradient(0, canvas.height - barHeight, 0, canvas.height);
        barGradient.addColorStop(0, `rgba(59, 130, 246, ${dataArray[i] / 255})`);
        barGradient.addColorStop(1, `rgba(139, 92, 246, ${dataArray[i] / 255})`);
        
        ctx.fillStyle = barGradient;
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
        
        // Add glow effect
        ctx.shadowColor = `rgba(59, 130, 246, ${dataArray[i] / 255})`;
        ctx.shadowBlur = 10;
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
        ctx.shadowBlur = 0;
        
        x += barWidth + 1;
    }
    
    // Add recording duration
    const duration = Math.floor((Date.now() - recordingStartTime) / 1000);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.font = '14px Arial';
    ctx.fillText(`Recording: ${duration}s`, 10, 20);
    
    visualizer.innerHTML = '';
    visualizer.appendChild(canvas);
    animationFrame = requestAnimationFrame(visualize);
}

// Toggle recording
function toggleRecording() {
    if (!isRecording) {
        // Start recording
        mediaRecorder.start();
        isRecording = true;
        recordingStartTime = Date.now();
        recordButton.classList.add('recording');
        recordIcon.textContent = '⏹️';
        recordText.textContent = 'Stop Recording';
        results.classList.add('hidden');
        visualize();
        showNotification('Recording started...', 'info');
    } else {
        // Stop recording
        mediaRecorder.stop();
        isRecording = false;
        recordButton.classList.remove('recording');
        recordIcon.textContent = '🎙️';
        recordText.textContent = 'Start Recording';
        cancelAnimationFrame(animationFrame);
        loading.classList.remove('hidden');
        showNotification('Processing audio...', 'info');
    }
}

// Handle WebSocket events
socket.on('analysis_result', (data) => {
    loading.classList.add('hidden');
    results.classList.remove('hidden');
    
    // Update transcription with animation
    const transcription = document.getElementById('transcription');
    transcription.textContent = '';
    const text = data.text;
    let i = 0;
    const typeWriter = () => {
        if (i < text.length) {
            transcription.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 20);
        }
    };
    typeWriter();
    
    // Update sarcasm score with animation
    const sarcasmScore = document.getElementById('sarcasmScore');
    sarcasmScore.textContent = '0%';
    sarcasmScore.className = 'text-4xl font-bold text-center py-6 rounded-xl';
    
    let currentScore = 0;
    const targetScore = data.sarcasm_score;
    const duration = 1000; // 1 second
    const steps = 60;
    const increment = targetScore / steps;
    const stepDuration = duration / steps;
    
    const updateScore = () => {
        currentScore = Math.min(currentScore + increment, targetScore);
        sarcasmScore.textContent = `${Math.round(currentScore)}%`;
        
        if (currentScore < targetScore) {
            setTimeout(updateScore, stepDuration);
        } else {
            if (targetScore > 70) {
                sarcasmScore.classList.add('score-high');
            } else if (targetScore > 30) {
                sarcasmScore.classList.add('score-medium');
            } else {
                sarcasmScore.classList.add('score-low');
            }
        }
    };
    updateScore();
    
    // Update feature values with animation
    const features = ['pitch', 'energy', 'zero_crossing_rate', 'spectral_centroid'];
    features.forEach(feature => {
        const element = document.getElementById(`${feature}Value`);
        const targetValue = data.features[feature];
        let currentValue = 0;
        const steps = 60;
        const increment = targetValue / steps;
        const stepDuration = duration / steps;
        
        const updateFeature = () => {
            currentValue = Math.min(currentValue + increment, targetValue);
            element.textContent = currentValue.toFixed(2);
            
            if (currentValue < targetValue) {
                setTimeout(updateFeature, stepDuration);
            }
        };
        updateFeature();
    });
});

socket.on('error', (data) => {
    loading.classList.add('hidden');
    showNotification(`Error: ${data.message}`, 'error');
});

// Event listeners
recordButton.addEventListener('click', toggleRecording);

// Initialize audio when page loads
initAudio(); 