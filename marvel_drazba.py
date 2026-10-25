from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="sk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Marvel Bidding War - Alternating Turns</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #0f172a;
                --card-bg: rgba(30, 41, 59, 0.7);
                --accent-blue: #38bdf8;
                --accent-purple: #c084fc;
                --accent-green: #4ade80;
                --accent-red: #f87171;
                --accent-gold: #facc15;
                --text: #f8fafc;
            }

            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Poppins', sans-serif; }
            body { background: var(--bg); color: var(--text); display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }

            .game-container {
                background: var(--card-bg);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                width: 100%;
                max-width: 650px;
                padding: 30px;
                box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                text-align: center;
            }

            h1 { font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #ef4444, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px; }

            .prize-banner {
                background: rgba(250, 204, 21, 0.1);
                border: 1px solid rgba(250, 204, 21, 0.3);
                color: var(--accent-gold);
                padding: 8px 16px;
                border-radius: 20px;
                display: inline-block;
                font-size: 0.9rem;
                font-weight: 600;
                margin-bottom: 20px;
            }

            #menu-screen { display: block; }
            #game-screen { display: none; }

            .menu-btns { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
            .btn-menu {
                background: linear-gradient(135deg, #0284c7, #38bdf8);
                color: white;
                padding: 16px;
                font-size: 1.1rem;
                font-weight: 700;
                border: none;
                border-radius: 14px;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
            }
            .btn-menu:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5); }
            .btn-menu.pvp { background: linear-gradient(135deg, #9333ea, #c084fc); box-shadow: 0 4px 15px rgba(192, 132, 252, 0.3); }
            .btn-menu.pvp:hover { box-shadow: 0 6px 20px rgba(192, 132, 252, 0.5); }

            .auction-box {
                background: rgba(15, 23, 42, 0.6);
                border-radius: 16px;
                padding: 20px;
                margin-bottom: 25px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }

            .player-avatar { font-size: 3.5rem; margin-bottom: 5px; }
            .player-name { font-size: 1.8rem; font-weight: 600; color: #fff; text-transform: uppercase; letter-spacing: 2px; }
            .hero-power-tag { font-size: 0.9rem; color: var(--accent-gold); margin-top: 3px; font-weight: 600; }
            .turn-indicator { font-size: 1rem; color: var(--accent-purple); font-weight: 600; margin-top: 5px; }
            .bid-display { font-size: 1.2rem; color: #94a3b8; margin-top: 10px; }
            .bid-amount { font-size: 2rem; font-weight: 800; color: var(--accent-blue); }

            .controls { display: flex; gap: 15px; justify-content: center; margin-bottom: 25px; }
            .btn {
                flex: 1;
                padding: 14px 20px;
                font-size: 1rem;
                font-weight: 600;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .btn-bid { background: linear-gradient(135deg, #0284c7, #38bdf8); color: white; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3); }
            .btn-bid:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5); }
            .btn-pass { background: rgba(255, 255, 255, 0.1); color: #cbd5e1; }
            .btn-pass:hover:not(:disabled) { background: rgba(255, 255, 255, 0.2); color: #fff; }
            .btn-restart { background: linear-gradient(135deg, #475569, #64748b); color: #fff; font-weight: 700; margin-top: 10px; width: 100%; display: none; }

            .btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none !important; }

            .teams-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
            .team-card {
                background: rgba(15, 23, 42, 0.4);
                padding: 15px;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.05);
                text-align: left;
            }
            .team-title { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
            .team-money { font-size: 1.2rem; font-weight: 800; color: var(--accent-green); margin-bottom: 5px; }
            .team-power-score { font-size: 0.85rem; color: var(--accent-gold); margin-bottom: 10px; font-weight: 600; }
            .slots { display: flex; flex-wrap: wrap; gap: 6px; }
            .badge {
                background: rgba(56, 189, 248, 0.15);
                color: var(--accent-blue);
                border: 1px solid rgba(56, 189, 248, 0.3);
                padding: 4px 10px;
                border-radius: 8px;
                font-size: 0.85rem;
                font-weight: 600;
            }
            .badge-p2 {
                background: rgba(192, 132, 252, 0.15);
                color: var(--accent-purple);
                border-color: rgba(192, 132, 252, 0.3);
            }

            .log-container {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 12px;
                padding: 12px;
                height: 100px;
                overflow-y: auto;
                text-align: left;
                font-size: 0.85rem;
                color: #94a3b8;
            }
        </style>
    </head>
    <body>

    <div class="game-container">
        <h1>MARVEL BIDDING WAR</h1>
        <div class="prize-banner"></div>

        <div id="menu-screen">
            <p style="color: #94a3b8; margin-bottom: 20px;">Vyber si herný režim:</p>
            <div class="menu-btns">
                <button class="btn-menu" onclick="startGame('ai')">🤖 Hráč vs AI</button>
                <button class="btn-menu pvp" onclick="startGame('pvp')">👥 Multiplayer (2 Hráči na 1 PC)</button>
            </div>
        </div>

        <div id="game-screen">
            <div class="auction-box">
                <div class="player-avatar" id="hero-avatar">🦸</div>
                <div class="player-name" id="current-player">---</div>
                <div class="hero-power-tag" id="hero-power">Sila: 0</div>
                <div class="turn-indicator" id="turn-indicator"></div>
                <div class="bid-display">Aktuálna ponuka: <span class="bid-amount" id="bid-price">0 €</span></div>
            </div>

            <div class="controls">
                <button class="btn btn-bid" id="btn-bid" onclick="makeBid()">Prihodiť +1€</button>
                <button class="btn btn-pass" id="btn-pass" onclick="makePass()">Vzdať sa</button>
            </div>

            <div class="teams-grid">
                <div class="team-card">
                    <div class="team-title" id="p1-title">Tvoj Tím</div>
                    <div class="team-money" id="p1-money">20 €</div>
                    <div class="team-power-score" id="p1-power">Celková sila: 0</div>
                    <div class="slots" id="p1-team"></div>
                </div>
                <div class="team-card">
                    <div class="team-title" id="p2-title">AI Tím</div>
                    <div class="team-money" id="p2-money" style="color: var(--accent-purple)">20 €</div>
                    <div class="team-power-score" id="p2-power">Celková sila: 0</div>
                    <div class="slots" id="p2-team"></div>
                </div>
            </div>

            <div class="log-container" id="log"></div>
            <button class="btn btn-restart" id="btn-restart" onclick="returnToMenu()">Späť do Menu 🔄</button>
        </div>
    </div>

    <script>
        const marvelPool = [
            { name: "Thanos", icon: "💎", power: 10 },
            { name: "Thor", icon: "⚡", power: 9 },
            { name: "Scarlet Witch", icon: "✨", power: 9 },
            { name: "Doctor Strange", icon: "🔮", power: 9 },
            { name: "Hulk", icon: "🟢", power: 9 },
            { name: "Iron Man", icon: "🤖", power: 7 },
            { name: "Wolverine", icon: "🐺", power: 9 },
            { name: "Captain America", icon: "🛡️", power: 7 },
            { name: "Black Panther", icon: "🐾", power: 6 },
            { name: "Spider-Man", icon: "🕷️", power: 6 },
            { name: "Deadpool", icon: "⚔️", power: 8 },
            { name: "Black Widow", icon: "🕷️", power: 3 },
            { name: "Loki", icon: "👑", power: 6 },
            { name: "Groot", icon: "🌳", power: 5 },
            { name: "Rocket", icon: "🦝", power: 4 },
            { name: "Hawkeye", icon: "🏹", power: 4 },
            { name: "Dr Doom", icon: "🧪", power: 9 }
        ];

        let gameMode = 'ai';
        let activeHeroes = [];
        let heroIndex = 0;
        let p1Money = 20, p2Money = 20;
        let p1Team = [], p2Team = [];
        let currentBid = 0, highBidder = null;
        let currentTurn = 'P1';
        let startingPlayer = 'P1'; // Určuje, kto začína aktuálne kolo (bude sa striedať)
        let biddingActive = false;

        function log(msg) {
            const logBox = document.getElementById("log");
            logBox.innerHTML += msg + "<br>";
            logBox.scrollTop = logBox.scrollHeight;
        }

        function startGame(mode) {
            gameMode = mode;
            activeHeroes = marvelPool.sort(() => Math.random() - 0.5).slice(0, 8);
            heroIndex = 0;
            p1Money = 20;
            p2Money = 20;
            p1Team = [];
            p2Team = [];
            startingPlayer = 'P1';

            document.getElementById("menu-screen").style.display = "none";
            document.getElementById("game-screen").style.display = "block";
            document.getElementById("btn-bid").disabled = false;
            document.getElementById("btn-pass").disabled = false;
            document.getElementById("btn-restart").style.display = "none";
            document.getElementById("log").innerHTML = "";

            if (gameMode === 'pvp') {
                document.getElementById("p1-title").innerText = "Hráč 1 Tím";
                document.getElementById("p2-title").innerText = "Hráč 2 Tím";
            } else {
                document.getElementById("p1-title").innerText = "Tvoj Tím";
                document.getElementById("p2-title").innerText = "AI Tím";
            }

            nextTurn();
        }

        function returnToMenu() {
            document.getElementById("menu-screen").style.display = "block";
            document.getElementById("game-screen").style.display = "none";
        }

        function calculatePower(team) {
            return team.reduce((total, hero) => total + hero.power, 0);
        }

        function updateUI() {
            document.getElementById("p1-money").innerText = p1Money + " €";
            document.getElementById("p2-money").innerText = p2Money + " €";
            
            let p1Power = calculatePower(p1Team);
            let p2Power = calculatePower(p2Team);
            document.getElementById("p1-power").innerText = "Celková sila: " + p1Power;
            document.getElementById("p2-power").innerText = "Celková sila: " + p2Power;

            document.getElementById("bid-price").innerText = currentBid + " €";

            document.getElementById("p1-team").innerHTML = p1Team.map(h => `<span class="badge" title="Sila: ${h.power}">${h.icon} ${h.name} (${h.power})</span>`).join('');
            document.getElementById("p2-team").innerHTML = p2Team.map(h => `<span class="badge badge-p2" title="Sila: ${h.power}">${h.icon} ${h.name} (${h.power})</span>`).join('');

            if (biddingActive) {
                if (gameMode === 'pvp') {
                    let nameP1 = "Hráč 1";
                    let nameP2 = "Hráč 2";
                    document.getElementById("turn-indicator").innerText = "Na ťahu: " + (currentTurn === 'P1' ? nameP1 : nameP2);
                } else {
                    document.getElementById("turn-indicator").innerText = currentTurn === 'P1' ? "Tvoj ťah" : "Ťah AI...";
                }
            } else {
                document.getElementById("turn-indicator").innerText = "";
            }
        }

        function nextTurn() {
            if (heroIndex >= activeHeroes.length || (p1Team.length === 4 && p2Team.length === 4)) {
                endGame();
                return;
            }

            currentBid = 0;
            highBidder = null;
            
            // Striedame začínajúceho hráča v každom novom kole dražby
            currentTurn = startingPlayer;
            biddingActive = true;
            
            const currentHero = activeHeroes[heroIndex];
            document.getElementById("current-player").innerText = currentHero.name;
            document.getElementById("hero-avatar").innerText = currentHero.icon;
            document.getElementById("hero-power").innerText = "⭐ Sila hrdinu: " + currentHero.power;

            log("--------------------------------");
            let starterName = (currentTurn === 'P1') ? (gameMode === 'pvp' ? "Hráč 1" : "Ty") : (gameMode === 'pvp' ? "Hráč 2" : "AI");
            log("👉 Dražba o: <b>" + currentHero.icon + " " + currentHero.name.toUpperCase() + "</b> (Sila: " + currentHero.power + ") | Začína: <b>" + starterName + "</b>");

            // Ak má začiatočník plné sloty, prepneme na druhého
            if (currentTurn === 'P1' && p1Team.length >= 4) {
                log("⚠️ Hráč 1 má plné sloty (4/4), začína druhý hráč.");
                currentTurn = 'P2';
            } else if (currentTurn === 'P2' && p2Team.length >= 4) {
                log("⚠️ Hráč 2/AI má plné sloty (4/4), začína Hráč 1.");
                currentTurn = 'P1';
            }

            if (gameMode === 'ai' && currentTurn === 'AI') {
                updateUI();
                setTimeout(aiTurn, 600);
            } else {
                updateUI();
            }
        }

        function makeBid() {
            if (!biddingActive) return;

            if (currentTurn === 'P1' && p1Team.length >= 4) return;
            if (currentTurn === 'P2' && p2Team.length >= 4) return;

            let nextBid = currentBid + 1;
            let moneyAvailable = currentTurn === 'P1' ? p1Money : p2Money;

            if (nextBid > moneyAvailable) {
                log("❌ " + (currentTurn === 'P1' ? "Hráč 1" : (gameMode === 'pvp' ? "Hráč 2" : "Ty")) + " nemá dostatok peňazí!");
                return;
            }

            currentBid = nextBid;
            highBidder = currentTurn;

            let displayName = currentTurn === 'P1' ? "Hráč 1" : (gameMode === 'pvp' ? "Hráč 2" : "Ty");
            log("👤 " + displayName + " prihodil na " + currentBid + "€");

            if (gameMode === 'pvp') {
                let nextPlayer = currentTurn === 'P1' ? 'P2' : 'P1';
                if ((nextPlayer === 'P1' && p1Team.length >= 4) || (nextPlayer === 'P2' && p2Team.length >= 4)) {
                    log("⚠️ Druhý hráč má plné sloty, kolo končí víťazstvom pre: " + (highBidder === 'P1' ? "Hráč 1" : "Hráč 2"));
                    finishRound(highBidder);
                    return;
                }
                currentTurn = nextPlayer;
                updateUI();
            } else {
                currentTurn = 'AI';
                updateUI();
                setTimeout(aiTurn, 600);
            }
        }

        function makePass() {
            if (!biddingActive) return;

            let displayName = currentTurn === 'P1' ? "Hráč 1" : (gameMode === 'pvp' ? "Hráč 2" : "Ty");
            log("🏳️ " + displayName + " sa vzdáva.");

            if (gameMode === 'pvp') {
                if (highBidder === null) {
                    finishRound(null);
                } else {
                    let winner = highBidder;
                    finishRound(winner);
                }
            } else {
                if (highBidder === 'AI') {
                    finishRound('AI');
                } else {
                    biddingActive = false;
                    setTimeout(aiTurn, 600);
                }
            }
        }

        function aiTurn() {
            if (p2Team.length >= 4) {
                log("🤖 AI má už plný tím (4/4).");
                finishRound(highBidder);
                return;
            }

            let aiNextBid = currentBid + 1;
            let canBid = aiNextBid <= p2Money && (aiNextBid <= 7 || Math.random() < 0.3);

            if (canBid) {
                currentBid = aiNextBid;
                highBidder = 'AI';
                log("🤖 AI prihadzuje na " + currentBid + "€");
                currentTurn = 'P1';
                
                if (p1Team.length >= 4) {
                    log("⚠️ Hráč 1 má plný tím, AI automaticky vyhráva dražbu.");
                    finishRound('AI');
                    return;
                }

                biddingActive = true;
                updateUI();
            } else {
                log("🤖 AI sa vzdáva.");
                if (highBidder === 'P1') {
                    finishRound('P1');
                } else {
                    finishRound(null);
                }
            }
        }

        function finishRound(winner) {
            biddingActive = false;
            const hero = activeHeroes[heroIndex];

            if (winner === 'P1') {
                p1Money -= currentBid;
                p1Team.push(hero);
                let name = gameMode === 'pvp' ? "Hráč 1 získal" : "Získal si";
                log("<span style='color:var(--accent-green)'>🎉 " + name + " " + hero.name + " (Sila: " + hero.power + ")!</span>");
            } else if (winner === 'P2' || winner === 'AI') {
                p2Money -= currentBid;
                p2Team.push(hero);
                let name = gameMode === 'pvp' ? "Hráč 2 získal" : "AI získalo";
                log("<span style='color:var(--accent-red)'>🤖 " + name + " " + hero.name + " (Sila: " + hero.power + ")!</span>");
            } else {
                log("⚪ Hrdinu " + hero.name + " nikto nezískal.");
            }

            // Prepni začiatočníka pre nasledujúce kolo (raz začína P1, nabudúce P2/AI)
            startingPlayer = (startingPlayer === 'P1') ? 'P2' : 'P1';

            heroIndex++;
            updateUI();
            setTimeout(nextTurn, 1500);
        }

        function endGame() {
            log("--------------------------------");
            log("<b>🎮 DRAŽBA SKONČILA! VYHODNOTENIE SILY TÍMOV:</b>");

            let p1Power = calculatePower(p1Team);
            let p2Power = calculatePower(p2Team);

            log("📊 Celková sila Hráč 1 / Ty: <b>" + p1Power + "</b>");
            log("📊 Celková sila Hráč 2 / AI: <b>" + p2Power + "</b>");

            let resultMsg = "";
            let avatar = "🏆";
            let p1Name = gameMode === 'pvp' ? "Hráč 1" : "Ty";
            let p2Name = gameMode === 'pvp' ? "Hráč 2" : "AI";

            if (p1Power > p2Power) {
                resultMsg = p1Name.toUpperCase() + " MÁ SILNEJŠÍ TÍM A VYHRÁVA! 🎉";
                avatar = "👑";
            } else if (p2Power > p1Power) {
                resultMsg = p2Name.toUpperCase() + " MÁ SILNEJŠÍ TÍM A VYHRÁVA! 🤖";
                avatar = "💀";
            } else {
                resultMsg = "ZODPOVEDÁ ROVNAKEJ SILE - ABSOLÚTNA REMÍZA!";
                avatar = "🤝";
            }

            document.getElementById("current-player").innerText = resultMsg;
            document.getElementById("hero-avatar").innerText = avatar;
            document.getElementById("hero-power").innerText = "Súboje tímov skončili";
            document.getElementById("turn-indicator").innerText = "";

            document.getElementById("btn-bid").style.display = "none";
            document.getElementById("btn-pass").style.display = "none";
            document.getElementById("btn-restart").style.display = "block";
        }
    </script>
    </body>
    </html>
    """
