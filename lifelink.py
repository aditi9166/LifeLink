<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LifeLink Emergency Locator App</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Configure Tailwind for Inter Font -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        'lifelink-red': '#DD1C1A', // Primary Emergency Red
                        'lifelink-blue': '#2A67C9', // Medical Trust Blue
                        'lifelink-dark': '#1F2937',
                        'lifelink-light': '#F9FAFB',
                        'card-red-bg': '#FEE2E2', // Light red for card backgrounds
                        'card-blue-bg': '#EBF8FF', // Light blue for card backgrounds
                        'card-yellow-bg': '#FFFBEB', // Light yellow for card backgrounds
                        'card-green-bg': '#F0FFF4', // Light green for card backgrounds
                    }
                }
            }
        }
    </script>
    <!-- Google Font - Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
    <style>
        /* --- DYNAMIC COLOR VARIABLES (LIGHT/DARK MODE) --- */
        :root {
            /* Light Mode Defaults */
            --color-bg-primary: #F9FAFB; /* Light Gray for main content area */
            --color-bg-secondary: white; /* White for cards, headers, nav */
            --color-text-primary: #1F2937;
            --color-text-secondary: #4B5563;
            --color-border-light: #E5E7EB;
            --color-card-bg: #FFFFFF;
        }

        .dark-mode {
            /* Dark Mode Overrides */
            --color-bg-primary: #1F2937;
            --color-bg-secondary: #374151;
            --color-text-primary: #F9FAFB;
            --color-text-secondary: #D1D5DB;
            --color-border-light: #4B5563;
            --color-card-bg: #4B5563;
        }
        
        /* New styles for Mobile App Simulation */
        body {
            background-color: #E5E7EB;
            display: flex;
            justify-content: center;
            padding: 20px 0;
            min-height: 100vh;
        }
        
        #app-container {
            max-width: 420px; 
            width: 100%;
            background-color: var(--color-bg-secondary);
            color: var(--color-text-primary);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-radius: 2rem; 
            overflow: hidden; 
            margin: auto;
            position: relative;
            display: flex; 
            flex-direction: column;
            min-height: 80vh; 
            transition: background-color 0.3s, color 0.3s;
        }
        
        #app-container header {
            background-color: var(--color-bg-secondary);
            border-bottom: 1px solid var(--color-border-light);
        }

        /* Applying dynamic colors */
        #page-content {
            background-color: var(--color-bg-primary);
            flex-grow: 1; /* Ensure content container fills space */
            padding-bottom: 4rem; /* Space for the fixed nav bar */
        }
        .page-section .bg-white,
        .page-section .bg-lifelink-light,
        #emergency-selection-modal {
            background-color: var(--color-bg-secondary) !important;
        }
        
        /* Dynamic Text Colors */
        .text-lifelink-dark, .text-gray-900 {
            color: var(--color-text-primary) !important;
        }
        .text-gray-500, .text-gray-600, .text-gray-700 {
             color: var(--color-text-secondary) !important;
        }
        
        /* Fixed Bottom Navigation Bar Styling */
        #bottom-nav {
            background-color: var(--color-bg-secondary);
            border-top: 1px solid var(--color-border-light);
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 420px;
            height: 4rem;
            z-index: 30;
            display: flex;
            justify-content: space-around;
            align-items: center;
            box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .nav-item {
            @apply flex flex-col items-center justify-center p-2 transition-colors duration-200 cursor-pointer;
            color: var(--color-text-secondary) !important;
            line-height: 1;
        }
        .nav-item.active-red {
             color: #DD1C1A !important;
        }

        /* --- NEW CARD STYLING (Emergency Modal & First Aid) --- */
        .grid-card {
            @apply p-4 rounded-xl shadow-md cursor-pointer transition transform duration-150;
            border: 1px solid transparent;
            min-height: 120px;
        }
        .grid-card:hover {
            @apply shadow-lg scale-[1.02];
        }

        /* Specific card color overrides for dark mode to maintain contrast */
        .dark-mode .bg-card-red-bg { background-color: #4C0807 !important; color: #FEE2E2 !important; }
        .dark-mode .bg-card-blue-bg { background-color: #123063 !important; color: #EBF8FF !important; }
        .dark-mode .bg-card-yellow-bg { background-color: #4C3C0A !important; color: #FFFBEB !important; }
        .dark-mode .bg-card-green-bg { background-color: #0A3C1A !important; color: #F0FFF4 !important; }

        /* Style for the Hospital List Item */
        .hospital-item {
            @apply p-4 rounded-xl shadow-lg transition duration-150;
            background-color: var(--color-card-bg);
            border-left: 6px solid #2A67C9;
        }
        .hospital-item .specialty-tag {
            @apply text-xs font-semibold px-2 py-0.5 rounded-full mr-1;
            background-color: var(--color-bg-primary);
        }
    </style>
</head>
<body class="font-sans antialiased">

    <!-- Firebase Initialization Script (MANDATORY BOILERPLATE) -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, setDoc, doc, setLogLevel } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
        const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : null;
        const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

        let db = null;
        let auth = null;
        let currentPage = 'Home';
        
        setLogLevel('Debug');

        const initFirebase = async () => {
            if (!firebaseConfig) {
                console.error("Firebase configuration is missing.");
                return;
            }

            try {
                const app = initializeApp(firebaseConfig);
                db = getFirestore(app);
                auth = getAuth(app);
                
                if (initialAuthToken) {
                    await signInWithCustomToken(auth, initialAuthToken);
                } else {
                    await signInAnonymously(auth);
                }
                
                const userId = auth.currentUser?.uid || crypto.randomUUID();
                console.log("Firebase initialized. User ID:", userId);
                
                const userIdEl = document.getElementById('user-id-display');
                if (userIdEl) {
                    userIdEl.textContent = 'User: ' + userId.substring(0, 8) + '...';
                }

            } catch (error) {
                console.error("Firebase initialization failed:", error);
            }
        };
        
        // --- THEME & DARK MODE LOGIC ---
        const applyTheme = () => {
            const savedTheme = localStorage.getItem('theme') || 'light';
            const container = document.getElementById('app-container');
            const toggle = document.getElementById('dark-mode-toggle');
            
            if (container) {
                if (savedTheme === 'dark') {
                    container.classList.add('dark-mode');
                    if (toggle) toggle.checked = true;
                } else {
                    container.classList.remove('dark-mode');
                    if (toggle) toggle.checked = false;
                }
            }
        };

        window.toggleDarkMode = () => {
            const container = document.getElementById('app-container');
            if (container) {
                if (container.classList.contains('dark-mode')) {
                    container.classList.remove('dark-mode');
                    localStorage.setItem('theme', 'light');
                } else {
                    container.classList.add('dark-mode');
                    localStorage.setItem('theme', 'dark');
                }
            }
        };
        
        // --- GEOLOCATION LOGIC ---
        window.getLocation = () => {
            const statusEl = document.getElementById('location-status');
            const displayEl = document.getElementById('location-display');
            
            if (!navigator.geolocation) {
                statusEl.textContent = 'Geolocation is not supported by your browser.';
                statusEl.classList.remove('text-green-600', 'text-lifelink-blue');
                statusEl.classList.add('text-lifelink-red');
                displayEl.innerHTML = '';
                return;
            }

            statusEl.textContent = 'Fetching precise coordinates...';
            statusEl.classList.remove('text-lifelink-red', 'text-green-600');
            statusEl.classList.add('text-lifelink-blue');
            displayEl.innerHTML = '';

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude.toFixed(6);
                    const lon = position.coords.longitude.toFixed(6);
                    
                    statusEl.textContent = 'Location Retrieved Successfully!';
                    statusEl.classList.remove('text-lifelink-blue');
                    statusEl.classList.add('text-green-600');
                    
                    displayEl.innerHTML = `
                        <p><strong>Latitude:</strong> ${lat}</p>
                        <p><strong>Longitude:</strong> ${lon}</p>
                        <p class="text-xs text-gray-500 mt-1">Accuracy: ${position.coords.accuracy.toFixed(0)} meters</p>
                    `;
                    console.log("Location:", {lat, lon});
                },
                (error) => {
                    let message = 'An unknown error occurred.';
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            message = 'Access Denied: Please allow location access in your browser settings.';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            message = 'Location Unavailable: Network or satellite issues.';
                            break;
                        case error.TIMEOUT:
                            message = 'Timeout: Failed to get location within time limit.';
                            break;
                    }
                    statusEl.textContent = `Error: ${message}`;
                    statusEl.classList.remove('text-lifelink-blue');
                    statusEl.classList.add('text-lifelink-red');
                    displayEl.innerHTML = '';
                    console.error("Geolocation Error:", error.message);
                },
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );
        };

        window.onload = () => {
             initFirebase();
             applyTheme();
             navigateTo('Home');
        };
        
        // --- NAVIGATION LOGIC ---
        const updateActiveTab = (activePage) => {
            document.querySelectorAll('.nav-item').forEach(item => {
                const page = item.getAttribute('data-page');
                const label = item.querySelector('.nav-label');
                
                if (page === activePage) {
                    item.classList.add('active-red');
                    label.classList.add('font-bold');
                } else {
                    item.classList.remove('active-red');
                    label.classList.remove('font-bold');
                }
            });
        }
        
        window.navigateTo = (pageName) => {
            const pages = document.querySelectorAll('.page-section');
            pages.forEach(page => page.classList.add('hidden'));

            const newPage = document.getElementById(pageName);
            if (newPage) {
                newPage.classList.remove('hidden');
                currentPage = pageName;
                
                updateActiveTab(pageName);
                document.getElementById('page-content').scrollTo(0, 0);
            }
        };

        // --- FIREBASE & ACTION LOGIC (RETAINED) ---
        window.logEmergency = async (type) => {
            if (db && auth.currentUser) {
                const userId = auth.currentUser.uid;
                const timestamp = new Date().toISOString();
                const emergencyRef = doc(db, `/artifacts/${appId}/users/${userId}/emergencies/${timestamp}`);
                
                await setDoc(emergencyRef, {
                    type: type,
                    timestamp: timestamp,
                    status: 'Initiated'
                });
                console.log(`Emergency logged to Firestore: ${type}`);
            } else {
                console.warn("Database not ready or user not logged in.");
            }
        };

        // Handle Modal Display and interactions
        document.addEventListener('DOMContentLoaded', () => {
            const emergencyModal = document.getElementById('emergency-selection-modal');
            const openEmergencyModalButton = document.getElementById('emergency-modal-open-btn');
            const closeModalButton = document.getElementById('close-modal-btn');
            
            // --- Emergency Modal Logic ---
            if (openEmergencyModalButton) {
                openEmergencyModalButton.onclick = (e) => {
                    e.preventDefault();
                    emergencyModal.classList.remove('hidden');
                    emergencyModal.classList.add('flex');
                };
            }

            if (closeModalButton) {
                closeModalButton.onclick = () => {
                    emergencyModal.classList.add('hidden');
                    emergencyModal.classList.remove('flex');
                };
            }

            // Function to handle card click inside modal
            window.handleEmergencySelect = (type) => {
                window.logEmergency(type);
                
                emergencyModal.classList.add('hidden');
                emergencyModal.classList.remove('flex');

                // Display confirmation message box
                const messageBox = document.getElementById('message-box');
                const messageText = document.getElementById('message-text');

                messageText.textContent = `Alert: Selected ${type}. Dispatching specialized help...`;
                messageBox.classList.remove('hidden');
                
                setTimeout(() => {
                    messageBox.classList.add('hidden');
                }, 4000);
            };
            
            // Function to handle dummy actions (First-Aid Cards)
            window.handleAction = (actionName) => {
                const messageBox = document.getElementById('message-box');
                const messageText = document.getElementById('message-text');
                    
                messageText.textContent = `Alert: Starting ${actionName} tutorial (${actionName})...`;
                messageBox.classList.remove('hidden');

                setTimeout(() => {
                    messageBox.classList.add('hidden');
                }, 3000);
            };
            
            updateActiveTab('Home');
        });
        
        // Dummy Call function for Hospital/Emergency buttons
        window.handleCall = (number) => {
             const messageBox = document.getElementById('message-box');
             const messageText = document.getElementById('message-text');
             messageText.textContent = `Dialing ${number}... (Simulated)`;
             messageBox.classList.remove('hidden');
             
             setTimeout(() => {
                 messageBox.classList.add('hidden');
             }, 3000);
        }
    </script>

    <!-- Global Message Box (Replaces alert()) -->
    <div id="message-box" class="hidden fixed top-0 left-0 right-0 p-4 bg-lifelink-red text-white text-center font-semibold shadow-2xl z-50">
        <p id="message-text"></p>
    </div>

    <!-- START OF MOBILE APP CONTAINER -->
    <div id="app-container">

        <!-- App-style Nav/Status Bar (Always Visible) -->
        <header class="p-6 sticky top-0 z-20">
            <div class="flex justify-between items-center">
                <div class="text-sm">9:41 AM</div>
                <!-- User ID Display (MANDATORY for Firebase multi-user apps) -->
                <div class="text-xs font-mono truncate" id="user-id-display">
                    Loading...
                </div>
                <button class="hover:opacity-75" onclick="navigateTo('Profile')">
                     <!-- Settings Icon -->
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.525.2.981.334 1.345.334zM15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                </button>
            </div>
        </header>


        <!-- MAIN SCROLLABLE PAGE CONTENT CONTAINER -->
        <div id="page-content" class="overflow-y-auto">

            <!-- PAGE 1: HOME -->
            <div id="Home" class="page-section">
                <!-- 1. IMPACTFUL HERO SECTION & CTA (Matches WhatsApp Image 2025-11-06 at 11.32.52 PM.jpeg) -->
                <section class="p-6">
                    <h1 class="text-4xl font-extrabold mb-4 leading-tight text-center">
                        Find Help. <span class="text-lifelink-red">Fast.</span>
                    </h1>
                    <p class="text-lg mb-8 font-light text-center text-gray-600">
                        Instantly locate the nearest hospital, ambulance, and get life-saving guidance in critical moments.
                    </p>
                    
                    <!-- Primary Button: Emergency Access - OPENS MODAL -->
                    <button id="emergency-modal-open-btn" class="inline-block bg-lifelink-red bg-gradient-to-r from-red-600 to-red-800 hover:opacity-90 transition duration-300 text-white font-bold py-4 px-6 rounded-xl shadow-lg transform hover:scale-[1.01] text-lg w-full text-center mb-4">
                        <span class="inline-flex items-center justify-center">
                            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                            Emergency Access
                        </span>
                    </button>
                    
                    <!-- Secondary Button: Find Hospitals -->
                    <button onclick="navigateTo('Hospitals')" class="inline-block bg-white text-lifelink-dark border border-gray-300 font-semibold py-4 px-6 rounded-xl shadow-md hover:bg-gray-100 transition duration-300 text-lg w-full text-center">
                        <span class="inline-flex items-center justify-center">
                             <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.828 0l-4.243-4.243m10.606 0a9 9 0 10-10.606 0z"></path></svg>
                            Find Hospitals
                        </span>
                    </button>
                </section>
                
                <!-- Stats Section -->
                <section class="p-6 pt-0 mt-6 grid grid-cols-3 gap-4 text-center">
                    <div>
                        <p class="text-2xl font-extrabold text-lifelink-red">5000+</p>
                        <p class="text-xs text-gray-500">Hospitals</p>
                    </div>
                    <div>
                        <p class="text-2xl font-extrabold text-lifelink-blue">24/7</p>
                        <p class="text-xs text-gray-500">Support</p>
                    </div>
                    <div>
                        <p class="text-2xl font-extrabold text-green-600">Real-time</p>
                        <p class="text-xs text-gray-500">Updates</p>
                    </div>
                </section>
            </div>

            <!-- PAGE 2: HOSPITALS (Matches WhatsApp Image 2025-11-07 at 12.10.32 AM.jpeg) -->
            <div id="Hospitals" class="page-section hidden">
                <section class="p-6">
                    <h2 class="text-3xl font-bold mb-1">Nearby Hospitals</h2>
                    <p class="mb-6 text-gray-600">Find the closest emergency care</p>
                    
                    <div class="space-y-4">
                        
                        <!-- Hospital Item 1 -->
                        <div class="hospital-item">
                            <div class="flex justify-between items-start mb-2">
                                <h3 class="text-xl font-bold text-lifelink-dark">City General Hospital</h3>
                                <span class="text-sm font-semibold text-gray-500">1.2 km</span>
                            </div>
                            <p class="text-sm text-gray-500 mb-3 flex items-center flex-wrap">
                                <span class="specialty-tag text-lifelink-red">Emergency</span>
                                <span class="specialty-tag text-lifelink-blue">Cardiac</span>
                                <span class="specialty-tag text-lifelink-red">Trauma</span>
                            </p>
                            <div class="flex items-center text-sm font-semibold text-green-600 mb-4">
                                <span class="w-2.5 h-2.5 bg-green-500 rounded-full mr-2"></span>
                                <span>5 beds available</span>
                            </div>

                            <div class="flex space-x-3">
                                <button onclick="handleCall('911 / 112')" class="flex-1 bg-lifelink-red hover:bg-red-700 text-white font-bold py-3 rounded-lg flex items-center justify-center">
                                    <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74A1 1 0 0118 16.847V18a1 1 0 01-1 1h-7A10 10 0 012 9V3z"></path></svg>
                                    Call
                                </button>
                                <button onclick="handleAction('Navigate to City General')" class="flex-1 bg-gray-200 hover:bg-gray-300 text-lifelink-dark font-semibold py-3 rounded-lg flex items-center justify-center">
                                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10l-2 1m0 0l-2-1m2 1v4m-4 10h8a2 2 0 002-2V8a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                                    Navigate
                                </button>
                            </div>
                        </div>
                        
                        <!-- Hospital Item 2 -->
                        <div class="hospital-item" style="border-left-color: #FBBF24;">
                            <div class="flex justify-between items-start mb-2">
                                <h3 class="text-xl font-bold text-lifelink-dark">Metro Medical Center</h3>
                                <span class="text-sm font-semibold text-gray-500">2.5 km</span>
                            </div>
                            <p class="text-sm text-gray-500 mb-3 flex items-center flex-wrap">
                                <span class="specialty-tag text-lifelink-blue">Emergency</span>
                                <span class="specialty-tag text-lifelink-blue">Neuro</span>
                                <span class="specialty-tag text-lifelink-red">ICU</span>
                            </p>
                            <div class="flex items-center text-sm font-semibold text-green-600 mb-4">
                                <span class="w-2.5 h-2.5 bg-green-500 rounded-full mr-2"></span>
                                <span>3 beds available</span>
                            </div>

                            <div class="flex space-x-3">
                                <button onclick="handleCall('911 / 112')" class="flex-1 bg-lifelink-red hover:bg-red-700 text-white font-bold py-3 rounded-lg flex items-center justify-center">
                                    <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74A1 1 0 0118 16.847V18a1 1 0 01-1 1h-7A10 10 0 012 9V3z"></path></svg>
                                    Call
                                </button>
                                <button onclick="handleAction('Navigate to Metro Medical')" class="flex-1 bg-gray-200 hover:bg-gray-300 text-lifelink-dark font-semibold py-3 rounded-lg flex items-center justify-center">
                                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10l-2 1m0 0l-2-1m2 1v4m-4 10h8a2 2 0 002-2V8a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                                    Navigate
                                </button>
                            </div>
                        </div>
                        
                    </div>
                </section>
            </div>
            
            <!-- PAGE 3: FIRST AID HUB (Matches WhatsApp Image 2025-11-07 at 12.10.33 AM.jpeg) -->
            <div id="FirstAid" class="page-section hidden">
                <section class="p-6">
                    <h2 class="text-3xl font-bold mb-1">First-Aid Hub</h2>
                    <p class="mb-6 text-gray-600">Learn life-saving procedures with interactive tutorials and virtual practice simulations</p>

                    <div class="grid grid-cols-2 gap-4">
                        
                        <!-- CPR Card -->
                        <div class="grid-card bg-white" onclick="handleAction('CPR')">
                            <svg class="w-8 h-8 text-lifelink-red mb-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"></path></svg>
                            <h3 class="text-lg font-bold">CPR</h3>
                            <p class="text-xs text-gray-600">Cardiopulmonary resuscitation</p>
                            <p class="text-xs mt-3 flex items-center text-lifelink-blue font-semibold">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                3 min tutorial
                            </p>
                        </div>

                        <!-- Bleeding Control Card -->
                        <div class="grid-card bg-white" onclick="handleAction('Bleeding Control')">
                            <svg class="w-8 h-8 text-lifelink-red mb-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM7 11a1 1 0 001 1h4a1 1 0 100-2H8a1 1 0 00-1 1zM3 7a1 1 0 112 0v6a1 1 0 11-2 0V7zM15 7a1 1 0 112 0v6a1 1 0 11-2 0V7z"></path></svg>
                            <h3 class="text-lg font-bold">Bleeding Control</h3>
                            <p class="text-xs text-gray-600">Stop severe bleeding</p>
                             <p class="text-xs mt-3 flex items-center text-lifelink-blue font-semibold">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                2 min tutorial
                            </p>
                        </div>
                        
                        <!-- Burns & Shock Card -->
                        <div class="grid-card bg-white" onclick="handleAction('Burns & Shock')">
                            <svg class="w-8 h-8 text-lifelink-red mb-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zM5 9a1 1 0 000 2h10a1 1 0 100-2H5z"></path></svg>
                            <h3 class="text-lg font-bold">Burns & Shock</h3>
                            <p class="text-xs text-gray-600">Burn treatment and shock management</p>
                            <p class="text-xs mt-3 flex items-center text-lifelink-blue font-semibold">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                4 min tutorial
                            </p>
                        </div>

                        <!-- Fracture Care Card -->
                        <div class="grid-card bg-white" onclick="handleAction('Fracture Care')">
                            <svg class="w-8 h-8 text-lifelink-red mb-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 110-6 3 3 0 010 6z"></path></svg>
                            <h3 class="text-lg font-bold">Fracture Care</h3>
                            <p class="text-xs text-gray-600">Stabilize broken bones</p>
                            <p class="text-xs mt-3 flex items-center text-lifelink-blue font-semibold">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                3 min tutorial
                            </p>
                        </div>
                    </div>
                </section>
            </div>

            <!-- PAGE 4: EMERGENCY CONTACTS (Matches WhatsApp Image 2025-11-07 at 12.10.33 AM (1).jpeg) -->
            <div id="Emergency" class="page-section hidden">
                <section class="p-6">
                    <h2 class="text-3xl font-bold mb-6">Emergency Direct Call</h2>
                    
                    <div class="grid grid-cols-2 gap-4">
                        
                        <!-- Fire Service -->
                        <div class="p-4 rounded-xl shadow-lg bg-card-red-bg flex flex-col items-center text-center">
                             <svg class="w-8 h-8 text-lifelink-red mb-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-7-9a1 1 0 000 2h14a1 1 0 100-2H3z" clip-rule="evenodd"></path></svg>
                            <h3 class="font-bold">Fire Service</h3>
                            <p class="text-xs text-gray-600 mb-3">Fire emergency</p>
                            <button onclick="handleCall('101')" class="w-full bg-lifelink-red text-white py-2 rounded-lg font-semibold flex items-center justify-center">
                                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74A1 1 0 0118 16.847V18a1 1 0 01-1 1h-7A10 10 0 012 9V3z"></path></svg>
                                Call 101
                            </button>
                        </div>
                        
                        <!-- Women Helpline -->
                        <div class="p-4 rounded-xl shadow-lg bg-card-blue-bg flex flex-col items-center text-center">
                             <svg class="w-8 h-8 text-lifelink-blue mb-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path></svg>
                            <h3 class="font-bold">Women Helpline</h3>
                            <p class="text-xs text-gray-600 mb-3">Women in distress</p>
                            <button onclick="handleCall('1091')" class="w-full bg-lifelink-red text-white py-2 rounded-lg font-semibold flex items-center justify-center">
                                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74A1 1 0 0118 16.847V18a1 1 0 01-1 1h-7A10 10 0 012 9V3z"></path></svg>
                                Call 1091
                            </button>
                        </div>
                        
                        <!-- Child Helpline -->
                        <div class="p-4 rounded-xl shadow-lg bg-card-green-bg flex flex-col items-center text-center">
                            <svg class="w-8 h-8 text-green-600 mb-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                            <h3 class="font-bold">Child Helpline</h3>
                            <p class="text-xs text-gray-600 mb-3">Child in need</p>
                            <button onclick="handleCall('1098')" class="w-full bg-lifelink-red text-white py-2 rounded-lg font-semibold flex items-center justify-center">
                                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74A1 1 0 0118 16.847V18a1 1 0 01-1 1h-7A10 10 0 012 9V3z"></path></svg>
                                Call 1098
                            </button>
                        </div>
                        
                        <!-- National Emergency -->
                        <div class="p-4 rounded-xl shadow-lg bg-card-red-bg flex flex-col items-center text-center">
                             <svg class="w-8 h-8 text-lifelink-red mb-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M12 9V4l3 3h-2v2l-3-3z" clip-rule="evenodd"></path></svg>
                            <h3 class="font-bold">National Emergency</h3>
                            <p class="text-xs text-gray-600 mb-3">All emergencies</p>
                            <button onclick="handleCall('112')" class="w-full bg-lifelink-red text-white py-2 rounded-lg font-semibold flex items-center justify-center">
                                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74A1 1 0 0118 16.847V18a1 1 0 01-1 1h-7A10 10 0 012 9V3z"></path></svg>
                                Call 112
                            </button>
                        </div>
                        
                    </div>
                </section>
            </div>

            <!-- PAGE 5: PROFILE (SETTINGS) - Retained from previous version -->
            <div id="Profile" class="page-section hidden">
                <section class="p-6 border-b">
                    <h2 class="text-3xl font-bold mb-6">My Health Profile</h2>
                    
                    <div class="flex items-center space-x-4 mb-8 p-4 rounded-xl" style="background-color: var(--color-bg-primary);">
                        <img src="https://placehold.co/80x80/2A67C9/FFFFFF?text=User" alt="User Avatar" class="w-16 h-16 rounded-full border-2 border-lifelink-blue object-cover">
                        <div>
                            <p class="text-xl font-bold">John Doe</p>
                            <p class="text-sm">Last updated: Today</p>
                        </div>
                    </div>

                    <h3 class="text-xl font-semibold mb-3 text-lifelink-blue">Vital Information</h3>
                    <div class="space-y-4">
                        <div class="flex justify-between p-3 rounded-lg border" style="background-color: var(--color-bg-secondary); border-color: var(--color-border-light);">
                            <span>Blood Type:</span>
                            <span class="font-bold text-red-600">O+</span>
                        </div>
                        <div class="flex justify-between p-3 rounded-lg border" style="background-color: var(--color-bg-secondary); border-color: var(--color-border-light);">
                            <span>Allergies:</span>
                            <span class="font-bold">Penicillin, Peanuts</span>
                        </div>
                         <div class="flex justify-between p-3 rounded-lg border" style="background-color: var(--color-bg-secondary); border-color: var(--color-border-light);">
                            <span>Medications:</span>
                            <span class="font-bold">Insulin (Daily)</span>
                        </div>
                    </div>
                    
                    <button class="mt-6 bg-gray-200 text-lifelink-dark py-3 px-6 rounded-xl font-bold w-full hover:opacity-75 transition">
                        Edit & Update Vitals
                    </button>
                    
                </section>
                
                <section class="p-6 border-b">
                     <h3 class="text-xl font-semibold mb-4">Location & Privacy Settings</h3>
                     
                     <!-- GEOLOCATION FEATURE -->
                     <div class="space-y-4 mb-6 p-4 rounded-xl border border-dashed border-lifelink-blue" style="background-color: var(--color-bg-primary);">
                         <div class="flex items-center justify-between">
                            <span class="font-semibold">Current GPS Location</span>
                            <button onclick="getLocation()" class="bg-lifelink-blue text-white text-sm py-2 px-4 rounded-lg font-semibold hover:bg-blue-700 transition">
                                Get Location
                            </button>
                         </div>
                         <div class="text-sm">
                             <p id="location-status" class="font-medium text-gray-500 mb-2">Location status: Not requested.</p>
                             <div id="location-display" class="font-mono text-xs space-y-0.5">
                                 <!-- Lat/Lon display here -->
                             </div>
                         </div>
                     </div>
                     
                      <!-- DARK MODE TOGGLE -->
                      <div class="flex justify-between items-center p-3 rounded-lg border" style="background-color: var(--color-bg-secondary); border-color: var(--color-border-light);">
                            <span class="font-semibold">Dark Mode</span>
                            <label class="toggle-switch">
                                <input type="checkbox" id="dark-mode-toggle" onchange="toggleDarkMode()">
                                <span class="slider"></span>
                            </label>
                        </div>
                     
                     <div class="flex justify-between items-center p-3 mt-4 rounded-lg border" style="background-color: var(--color-bg-secondary); border-color: var(--color-border-light);">
                        <span>Emergency Contacts:</span>
                        <span class="text-lifelink-blue font-semibold">3 People</span>
                    </div>

                </section>
                <div class="py-4 text-center text-xs text-gray-500">
                    Version 1.2 | Developed for Safety.
                </div>
            </div>
            
        </div>

        <!-- FIXED BOTTOM NAVIGATION BAR -->
        <nav id="bottom-nav">
            <!-- Home -->
            <div class="nav-item active-red" data-page="Home" onclick="navigateTo('Home')">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-5a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg>
                <span class="text-xs mt-1 nav-label font-bold">Home</span>
            </div>

            <!-- Hospitals -->
            <div class="nav-item" data-page="Hospitals" onclick="navigateTo('Hospitals')">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"></path></svg>
                <span class="text-xs mt-1 nav-label">Hospitals</span>
            </div>
            
            <!-- Emergency -->
            <div class="nav-item" data-page="Emergency" onclick="navigateTo('Emergency')">
                <div class="p-1 bg-lifelink-red rounded-full text-white shadow-lg -mt-3 transform hover:scale-110 transition duration-150">
                     <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                </div>
                <span class="text-xs mt-1 nav-label text-lifelink-red font-semibold">Alert</span>
            </div>
            
            <!-- First Aid -->
            <div class="nav-item" data-page="FirstAid" onclick="navigateTo('FirstAid')">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h2a1 1 0 001-1v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                <span class="text-xs mt-1 nav-label">First Aid</span>
            </div>

            <!-- Profile -->
            <div class="nav-item" data-page="Profile" onclick="navigateTo('Profile')">
                 <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.98 5.98 0 0010 16a5.979 5.979 0 004.546-2.084A5 5 0 0010 11z" clip-rule="evenodd"></path></svg>
                <span class="text-xs mt-1 nav-label">Profile</span>
            </div>
        </nav>
        
        <!-- QUICK EMERGENCY TYPE SELECTION PANEL (MODAL) - (Matches WhatsApp Image 2025-11-06 at 11.37.18 PM.jpeg series) -->
        <div id="emergency-selection-modal" class="hidden fixed inset-0 z-40 flex flex-col items-center justify-start pt-6 px-4 sm:px-6">
            
            <!-- Header -->
            <div class="w-full max-w-sm mb-6 sticky top-0 pb-3" style="background-color: var(--color-bg-secondary);">
                <button id="close-modal-btn" class="absolute top-2 right-0 p-2 rounded-full transition">
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                </button>
                <h2 class="text-3xl font-extrabold text-left">Select Emergency Type</h2>
                <p class="mt-1 text-left text-gray-600">
                    Choose your emergency type to find **specialized facilities** and get **targeted guidance**.
                </p>
            </div>

            <!-- Emergency Cards Grid (Scrollable) -->
            <div class="w-full max-w-sm space-y-3 mb-8 overflow-y-auto" style="max-height: 75vh;">

                <!-- Card 1: Accident -->
                <div class="grid-card bg-card-red-bg flex items-center p-5 hover:border-lifelink-red" onclick="handleEmergencySelect('Accident')">
                    <svg class="w-8 h-8 text-lifelink-red flex-shrink-0 mr-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 110-6 3 3 0 010 6z"></path></svg>
                    <div>
                        <h3 class="text-xl font-bold">Accident</h3>
                        <p class="text-sm text-gray-600">Road or trauma emergency</p>
                    </div>
                </div>

                <!-- Card 2: Heart Attack -->
                <div class="grid-card bg-card-red-bg flex items-center p-5 hover:border-lifelink-red" onclick="handleEmergencySelect('Heart Attack')">
                    <svg class="w-8 h-8 text-lifelink-red flex-shrink-0 mr-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"></path></svg>
                    <div>
                        <h3 class="text-xl font-bold">Heart Attack</h3>
                        <p class="text-sm text-gray-600">Cardiac emergency</p>
                    </div>
                </div>

                <!-- Card 3: Stroke -->
                <div class="grid-card bg-card-blue-bg flex items-center p-5 hover:border-lifelink-blue" onclick="handleEmergencySelect('Stroke')">
                    <svg class="w-8 h-8 text-lifelink-blue flex-shrink-0 mr-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 110-6 3 3 0 010 6z"></path></svg>
                    <div>
                        <h3 class="text-xl font-bold">Stroke</h3>
                        <p class="text-sm text-gray-600">Neurological emergency</p>
                    </div>
                </div>
                
                <!-- Card 4: Asthma Attack -->
                <div class="grid-card bg-card-blue-bg flex items-center p-5 hover:border-lifelink-blue" onclick="handleEmergencySelect('Asthma Attack')">
                    <svg class="w-8 h-8 text-lifelink-blue flex-shrink-0 mr-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM5 9a1 1 0 000 2h10a1 1 0 100-2H5z" clip-rule="evenodd"></path></svg>
                    <div>
                        <h3 class="text-xl font-bold">Asthma Attack</h3>
                        <p class="text-sm text-gray-600">Breathing difficulty</p>
                    </div>
                </div>

                <!-- Card 5: Seizure -->
                <div class="grid-card bg-card-yellow-bg flex items-center p-5 hover:border-yellow-600" onclick="handleEmergencySelect('Seizure')">
                    <svg class="w-8 h-8 text-yellow-600 flex-shrink-0 mr-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-7-9a1 1 0 000 2h14a1 1 0 100-2H3z" clip-rule="evenodd"></path></svg>
                    <div>
                        <h3 class="text-xl font-bold">Seizure</h3>
                        <p class="text-sm text-gray-600">Neurological episode</p>
                    </div>
                </div>
                
                <!-- Card 6: Mental Crisis -->
                <div class="grid-card bg-card-green-bg flex items-center p-5 hover:border-green-600" onclick="handleEmergencySelect('Mental Crisis')">
                    <svg class="w-8 h-8 text-green-600 flex-shrink-0 mr-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 110-6 3 3 0 010 6z"></path></svg>
                    <div>
                        <h3 class="text-xl font-bold">Mental Crisis</h3>
                        <p class="text-sm text-gray-600">Panic or distress</p>
                    </div>
                </div>
                
            </div>

            <!-- Warning Box (Fixed to bottom of modal) -->
            <div class="w-full max-w-sm p-4 bg-lifelink-red text-white font-semibold text-center mt-auto mb-4 rounded-xl shadow-xl">
                <p class="text-sm mb-1">
                    For immediate life-threatening emergencies, call 108 or 112
                </p>
            </div>
        </div>
    </div>
    <!-- END OF MOBILE APP CONTAINER -->

</body>
</html>
