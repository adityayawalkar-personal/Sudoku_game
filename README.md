<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Sudoku Pro - Complete Edition</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;line-height:1.5;color:#111;background:#fff;margin:20px;padding:0}
    .container{max-width:980px;margin:0 auto;padding:20px}
    h1{font-size:1.8rem;margin:0 0 8px}
    h2{font-size:1.2rem;margin-top:22px}
    h3{margin-top:16px}
    pre{background:#f5f5f5;padding:12px;border-radius:6px;overflow:auto}
    table{border-collapse:collapse;width:100%;margin:12px 0}
    table th, table td{border:1px solid #ddd;padding:8px;text-align:left}
    ul,ol{margin:8px 0 8px 20px}
    hr{border:none;border-top:1px solid #eee;margin:18px 0}
    .badge-img{height:20px;margin-right:8px;vertical-align:middle}
    .note{color:#555;font-size:0.95rem}
    .screenshot{max-width:100%;height:auto;border:1px solid #eee;padding:6px;border-radius:6px;margin:8px 0}
  </style>
</head>
<body>
  <div class="container">

    <h1>🎮 Sudoku Pro - Complete Edition</h1>
    <p>A professional Sudoku game with two versions: a classic simple interface (v1) and a modern Sudoku.com-inspired design (v2). Choose the experience that suits you best!</p>

    <p>
      <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python" class="badge-img"></a>
      <a href="https://api.arcade.academy/"><img src="https://img.shields.io/badge/arcade-2.6+-green.svg" alt="Arcade" class="badge-img"></a>
      <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" class="badge-img"></a>
      <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-2.0.0-blue.svg" alt="Version" class="badge-img"></a>
    </p>

    <h2>📋 Table of Contents</h2>
    <ul>
      <li><a href="#choose-your-version">Choose Your Version</a></li>
      <li><a href="#quick-start">Quick Start</a></li>
      <li><a href="#version-comparison">Version Comparison</a></li>
      <li><a href="#features-by-version">Features by Version</a></li>
      <li><a href="#installation">Installation</a></li>
      <li><a href="#how-to-play">How to Play</a></li>
      <li><a href="#controls">Controls</a></li>
      <li><a href="#screenshots">Screenshots</a></li>
      <li><a href="#technical-details">Technical Details</a></li>
      <li><a href="#changelog">Changelog</a></li>
      <li><a href="#contributing">Contributing</a></li>
      <li><a href="#license">License</a></li>
    </ul>

    <hr>

    <h2 id="choose-your-version">🎯 Choose Your Version</h2>
    <p>This repository contains <strong>two complete versions</strong> of Sudoku Pro, each with its own strengths.</p>

    <h3>Version 1.0 - Classic &amp; Simple</h3>
    <p><strong>Perfect for</strong>: Quick games, minimalist design lovers, lower-end systems</p>
    <pre><code>python sudoku_game_v1.py</code></pre>
    <p><strong>Highlights:</strong></p>
    <ul>
      <li>✅ Clean, straightforward interface</li>
      <li>✅ Fast and lightweight</li>
      <li>✅ All core Sudoku features</li>
      <li>✅ Easy to learn</li>
      <li>✅ 700×850 window</li>
    </ul>
    <p class="note"><strong>Best for:</strong> Players who want pure Sudoku without extras</p>

    <hr>

    <h3>Version 2.0 - Professional &amp; Feature-Rich</h3>
    <p><strong>Perfect for</strong>: Serious players, modern UI enthusiasts, advanced features</p>
    <pre><code>python sudoku_pro_v2.py</code></pre>
    <p><strong>Highlights:</strong></p>
    <ul>
      <li>✨ Sudoku.com-style modern interface</li>
      <li>✨ Undo/Redo system (200 moves)</li>
      <li>✨ Pause/Resume with timer freeze</li>
      <li>✨ Clickable number pad</li>
      <li>✨ Auto-updating notes</li>
      <li>✨ Enhanced highlighting</li>
      <li>✨ Score tracking</li>
    </ul>
    <p class="note"><strong>Best for:</strong> Players who want the complete Sudoku experience</p>

    <hr>

    <h2 id="quick-start">⚡ Quick Start</h2>

    <h3>Install Dependencies</h3>
    <pre><code>pip install arcade</code></pre>

    <h3>Run Version 1 (Classic)</h3>
    <pre><code>python sudoku_game_v1.py</code></pre>

    <h3>Run Version 2 (Professional)</h3>
    <pre><code>python sudoku_pro_v2.py</code></pre>

    <p class="note">Both versions work independently - no conflicts!</p>

    <hr>

    <h2 id="version-comparison">📊 Version Comparison</h2>

    <table>
      <thead>
        <tr>
          <th>Feature</th>
          <th>v1.0 Classic</th>
          <th>v2.0 Professional</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><strong>Window Size</strong></td><td>700×850</td><td>600×900</td></tr>
        <tr><td><strong>Grid Sizes</strong></td><td>9×9, 16×16</td><td>9×9, 16×16</td></tr>
        <tr><td><strong>Difficulty Levels</strong></td><td>5 (Easy to Extreme)</td><td>5 (Easy to Extreme)</td></tr>
        <tr><td><strong>Note-Taking</strong></td><td>✅ Basic</td><td>✅ Auto-update</td></tr>
        <tr><td><strong>Hints</strong></td><td>✅ 3 per game</td><td>✅ 3 with flash effect</td></tr>
        <tr><td><strong>Undo/Redo</strong></td><td>❌</td><td>✅ Full history (200 moves)</td></tr>
        <tr><td><strong>Pause/Resume</strong></td><td>❌</td><td>✅ With timer freeze</td></tr>
        <tr><td><strong>Number Pad</strong></td><td>Keyboard only</td><td>✅ Clickable buttons</td></tr>
        <tr><td><strong>Highlighting</strong></td><td>Basic (3 levels)</td><td>Advanced (4 levels)</td></tr>
        <tr><td><strong>Conflict Detection</strong></td><td>❌</td><td>✅ Real-time</td></tr>
        <tr><td><strong>Score System</strong></td><td>❌</td><td>✅ Point tracking</td></tr>
        <tr><td><strong>Timer</strong></td><td>✅ MM:SS</td><td>✅ MM:SS with pause</td></tr>
        <tr><td><strong>Mistake Tracking</strong></td><td>✅ 3 max</td><td>✅ 3 max</td></tr>
        <tr><td><strong>Color Coding</strong></td><td>2 colors</td><td>3 colors</td></tr>
        <tr><td><strong>Button Styling</strong></td><td>Simple</td><td>Shadows + hover</td></tr>
        <tr><td><strong>UI Style</strong></td><td>Functional</td><td>Sudoku.com-inspired</td></tr>
        <tr><td><strong>Performance</strong></td><td>Very fast</td><td>Fast</td></tr>
        <tr><td><strong>File Size</strong></td><td>~15 KB</td><td>~25 KB</td></tr>
      </tbody>
    </table>

    <h3>Which Should You Choose?</h3>
    <p><strong>Choose v1.0 if you want:</strong></p>
    <ul>
      <li>Simple, no-frills Sudoku</li>
      <li>Lightweight performance</li>
      <li>Quick load times</li>
      <li>Classic game feel</li>
    </ul>

    <p><strong>Choose v2.0 if you want:</strong></p>
    <ul>
      <li>Modern, polished interface</li>
      <li>Advanced features (undo/pause)</li>
      <li>Better visual feedback</li>
      <li>Professional experience</li>
    </ul>

    <hr>

    <h2 id="features-by-version">✨ Features by Version</h2>

    <h3>Common Features (Both Versions)</h3>
    <ul>
      <li>✅ <strong>Multiple Grid Sizes</strong>: 9×9 and 16×16</li>
      <li>✅ <strong>5 Difficulty Levels</strong> (Easy → Extreme)</li>
      <li>✅ <strong>Smart Puzzle Generation</strong>: Backtracking, unique solution</li>
      <li>✅ <strong>Note-Taking System</strong> (toggle with 'N')</li>
      <li>✅ <strong>Hint System</strong>: 3 hints per game</li>
      <li>✅ <strong>Mistake Tracking</strong>: Max 3 mistakes</li>
      <li>✅ <strong>Timer</strong> (MM:SS)</li>
      <li>✅ <strong>Keyboard &amp; Mouse Controls</strong></li>
      <li>✅ <strong>Visual Highlights</strong></li>
      <li>✅ <strong>Victory/Game Over Screens</strong></li>
    </ul>

    <h3>Version 1.0 Exclusive Features</h3>
    <ul>
      <li>Horizontal layout, minimalist design</li>
      <li>Simple menu and compact tools</li>
      <li>Faster startup and lower resource usage</li>
    </ul>

    <h3>Version 2.0 Exclusive Features</h3>
    <ul>
      <li>Undo/Redo (200 moves) – <code>Ctrl+Z</code> / <code>Ctrl+Y</code></li>
      <li>Pause/Resume with timer freeze (keyboard: <code>P</code> or <code>Space</code>)</li>
      <li>Clickable number pad, auto-update notes</li>
      <li>4-level enhanced highlighting &amp; real-time conflict detection</li>
      <li>Score system (+10 per correct placement, +5 per hint)</li>
      <li>Flash effects, professional UI, color-coded numbers</li>
      <li>Hexadecimal support for 16×16 (A–G for 10–16)</li>
    </ul>

    <hr>

    <h2 id="installation">📥 Installation</h2>

    <h3>Prerequisites</h3>
    <ul>
      <li>Python 3.7 or higher</li>
      <li>pip</li>
    </ul>

    <h3>Step 1: Clone Repository</h3>
    <pre><code>git clone https://github.com/yourusername/sudoku-pro.git
cd sudoku-pro</code></pre>

    <h3>Step 2: Install Dependencies</h3>
    <pre><code>pip install -r requirements.txt</code></pre>
    <p>Or install Arcade directly:</p>
    <pre><code>pip install arcade</code></pre>

    <h3>Step 3: Run Your Preferred Version</h3>
    <pre><code># Version 1 (Classic)
python sudoku_game_v1.py

# Version 2 (Professional)
python sudoku_pro_v2.py</code></pre>

    <hr>

    <h2 id="how-to-play">🎮 How to Play</h2>

    <h3>Objective</h3>
    <p>Fill the grid so each row, column, and box contains all numbers (1–9 for 9×9, 1–16 for 16×16).</p>

    <h3>Game Flow</h3>
    <ol>
      <li>Select difficulty</li>
      <li>Select a cell (click or arrow keys)</li>
      <li>Enter number (keyboard or number pad in v2)</li>
      <li>Use notes (toggle with 'N')</li>
      <li>Use hints (3 per game)</li>
      <li>Win by completing puzzle with ≤3 mistakes</li>
    </ol>

    <h3>Tips for Success</h3>
    <ul>
      <li>Start with easy cells and use notes</li>
      <li>Find naked/hidden singles and patterns</li>
      <li>In v2, use undo and watch conflict highlights</li>
    </ul>

    <hr>

    <h2 id="controls">🎹 Controls</h2>

    <h3>Version 1.0 Controls — Keyboard</h3>
    <table>
      <thead><tr><th>Key</th><th>Action</th></tr></thead>
      <tbody>
        <tr><td>Arrow Keys</td><td>Navigate cells</td></tr>
        <tr><td>1–9</td><td>Enter number (9×9)</td></tr>
        <tr><td>1–9, A–G</td><td>Enter number (16×16)</td></tr>
        <tr><td>0 / Backspace</td><td>Delete number</td></tr>
        <tr><td>Delete</td><td>Clear cell</td></tr>
        <tr><td>N</td><td>Toggle note mode</td></tr>
      </tbody>
    </table>

    <h3>Version 2.0 Controls — Keyboard &amp; Mouse</h3>
    <table>
      <thead><tr><th>Key / Action</th><th>Effect</th></tr></thead>
      <tbody>
        <tr><td>1–9</td><td>Enter number (9×9)</td></tr>
        <tr><td>1–9, A–G</td><td>Enter number (16×16)</td></tr>
        <tr><td>0 / Backspace</td><td>Erase</td></tr>
        <tr><td>Arrow Keys</td><td>Move selection</td></tr>
        <tr><td>N</td><td>Toggle note mode</td></tr>
        <tr><td>P or Space</td><td>Pause/Resume</td></tr>
        <tr><td>Ctrl+Z</td><td>Undo</td></tr>
        <tr><td>Ctrl+Y</td><td>Redo</td></tr>
        <tr><td>ESC</td><td>Return to menu</td></tr>
      </tbody>
    </table>

    <p class="note">Mouse: Click cells, click number pad (v2), click action bar buttons.</p>

    <hr>

    <h2 id="screenshots">📸 Screenshots</h2>

    <h3>Version 1.0 - Classic Interface</h3>
    <p><img src="screenshots/v1_menu.png" alt="v1 Menu" class="screenshot"></p>
    <p><img src="screenshots/v1_gameplay_9x9.png" alt="v1 Gameplay 9x9" class="screenshot"></p>
    <p><img src="screenshots/v1_gameplay_16x16.png" alt="v1 Gameplay 16x16" class="screenshot"></p>

    <h3>Version 2.0 - Professional Interface</h3>
    <p><img src="screenshots/v2_interface.png" alt="v2 Interface" class="screenshot"></p>
    <p><img src="screenshots/v2_highlighting.png" alt="v2 Highlighting" class="screenshot"></p>
    <p><img src="screenshots/v2_undo.png" alt="v2 Undo" class="screenshot"></p>
    <p><img src="screenshots/v2_pause.png" alt="v2 Pause" class="screenshot"></p>

    <hr>

    <h2 id="technical-details">🔧 Technical Details</h2>

    <h3>System Requirements</h3>
    <p><strong>Minimum:</strong></p>
    <ul>
      <li>Python 3.7+</li>
      <li>512 MB RAM</li>
      <li>50 MB disk space</li>
      <li>1024×768 screen</li>
    </ul>
    <p><strong>Recommended:</strong></p>
    <ul>
      <li>Python 3.10+</li>
      <li>1 GB RAM</li>
      <li>100 MB disk</li>
      <li>1920×1080 screen</li>
    </ul>

    <h3>Performance</h3>
    <table>
      <thead><tr><th>Metric</th><th>v1.0</th><th>v2.0</th></tr></thead>
      <tbody>
        <tr><td>Startup Time</td><td>&lt;1s</td><td>&lt;1s</td></tr>
        <tr><td>Frame Rate</td><td>60 FPS</td><td>60 FPS</td></tr>
        <tr><td>Memory Usage</td><td>~40 MB</td><td>~50 MB</td></tr>
        <tr><td>Code Lines</td><td>~500</td><td>~900</td></tr>
      </tbody>
    </table>

    <h3>Architecture</h3>
    <p>Both versions share backtracking puzzle generation, an arcade game loop, and object-oriented design. Version 2 adds a history stack, state machine for pause, conflict computation, and auto-note logic.</p>

    <h3>File Structure</h3>
    <pre><code>sudoku-pro/
├── sudoku_game_v1.py
├── sudoku_pro_v2.py
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── screenshots/
└── docs/</code></pre>

    <hr>

    <h2 id="changelog">📝 Changelog</h2>

    <h3>[2.0.0] - 2024-12-18 ⭐ LATEST</h3>
    <p><strong>Major Release - Complete UI Overhaul</strong></p>
    <p><strong>Added (v2)</strong>: Undo/Redo, Pause/Resume, Clickable number pad, Auto-notes, Enhanced highlighting, Real-time conflict detection, Score tracking, Flash effects, Sudoku.com-style UI.</p>

    <h3>[1.0.0] - 2024-12-17</h3>
    <p><strong>Initial Release</strong>: 9×9 &amp; 16×16 grids, 5 difficulty levels, note-taking, hints, mistake tracking, timer, basic highlighting.</p>

    <p><a href="CHANGELOG.md">See full changelog →</a></p>

    <hr>

    <h2 id="which-version">🎯 Which Version for Which Use Case?</h2>

    <h3>Use Version 1.0 if:</h3>
    <ul>
      <li>You prefer simplicity and lightweight performance</li>
      <li>You want quick games and a classic feel</li>
      <li>You're teaching beginners</li>
    </ul>

    <h3>Use Version 2.0 if:</h3>
    <ul>
      <li>You want modern features (undo, pause, score)</li>
      <li>You prefer a polished professional UI</li>
      <li>You play seriously and want better visual feedback</li>
    </ul>

    <hr>

    <h2 id="roadmap">🚀 Future Roadmap</h2>
    <h3>Version 1.x (Classic)</h3>
    <ul>
      <li>v1.1: Bug fixes</li>
      <li>v1.2: Minor UI improvements</li>
    </ul>

    <h3>Version 2.x (Professional)</h3>
    <ul>
      <li>v2.1 (Q1 2025): Save/Load</li>
      <li>v2.2 (Q2 2025): Daily challenge</li>
      <li>v2.3 (Q2 2025): Achievements</li>
    </ul>

    <hr>

    <h2 id="contributing">🤝 Contributing</h2>
    <p>Contributions are welcome. Please specify which version your changes target (v1 or v2).</p>
    <ol>
      <li>Fork the repo</li>
      <li>Create a feature branch</li>
      <li>Test thoroughly</li>
      <li>Open a Pull Request</li>
    </ol>
    <p>Follow PEP 8, add docstrings, and include tests where applicable.</p>

    <hr>

    <h2 id="documentation">📖 Documentation</h2>
    <ul>
      <li><strong>README.md</strong> (this file)</li>
      <li><strong>CHANGELOG.md</strong></li>
      <li><strong>docs/algorithm.md</strong> - puzzle generation</li>
    </ul>

    <hr>

    <h2 id="known-issues">🐛 Known Issues</h2>
    <h4>Version 1.0</h4>
    <ul>
      <li>16×16 note display could be improved</li>
      <li>No undo</li>
    </ul>

    <h4>Version 2.0</h4>
    <ul>
      <li>Flash effect may lag on old systems</li>
      <li>Undo history cleared on new game</li>
    </ul>

    <hr>

    <h2 id="tips">💡 Tips &amp; Tricks</h2>
    <h4>For v1 Players</h4>
    <ul>
      <li>Use note mode early</li>
      <li>Keyboard navigation is faster</li>
    </ul>
    <h4>For v2 Players</h4>
    <ul>
      <li>Use undo (<code>Ctrl+Z</code>) to experiment</li>
      <li>Watch conflict highlights</li>
    </ul>

    <hr>

    <h2 id="support">📞 Support</h2>
    <p>Issues: <a href="https://github.com/yourusername/sudoku-pro/issues">GitHub Issues</a></p>
    <p>Discussions: <a href="https://github.com/yourusername/sudoku-pro/discussions">GitHub Discussions</a></p>
    <p>Email: your.email@example.com</p>

    <hr>

    <h2 id="license">📜 License</h2>
    <p>This project is licensed under the MIT License - see <a href="LICENSE">LICENSE</a> for details.</p>

    <h3>MIT License Summary</h3>
    <ul>
      <li>✅ Commercial use</li>
      <li>✅ Modification &amp; distribution</li>
      <li>⚠️ No warranty provided</li>
    </ul>

    <hr>

    <h2 id="author">👨‍💻 Author</h2>
    <p><strong>Your Name</strong><br>
      GitHub: <a href="https://github.com/yourusername">@yourusername</a><br>
      Email: your.email@example.com</p>

    <hr>

    <h2 id="acknowledgments">🙏 Acknowledgments</h2>
    <ul>
      <li>Python Arcade framework</li>
      <li>Sudoku.com – UI inspiration</li>
      <li>Backtracking algorithm references</li>
      <li>Beta testers and community contributors</li>
    </ul>

    <hr>

    <h2 id="education">🎓 Educational Use</h2>
    <p>Great for learning Python game dev, backtracking algorithms, and UI/UX design. Feel free to use it in classes and tutorials.</p>

    <hr>

    <h2 id="stats">📊 Project Stats</h2>
    <table>
      <thead><tr><th>Metric</th><th>v1.0</th><th>v2.0</th></tr></thead>
      <tbody>
        <tr><td>Lines of Code</td><td>~500</td><td>~900</td></tr>
        <tr><td>Development Time</td><td>2 days</td><td>3 days</td></tr>
        <tr><td>File Size</td><td>15 KB</td><td>25 KB</td></tr>
      </tbody>
    </table>

    <hr>

    <h2 id="star-history">🌟 Star History</h2>
    <p>If you enjoy either version, please give it a star! ⭐</p>

    <hr>

    <h2 id="closing">🎮 Happy Sudoku Solving!</h2>
    <p><strong>Choose your experience:</strong> v1.0 for simplicity, v2.0 for features, or both for variety.</p>
    <p><em>Made with ❤️ and lots of ☕</em></p>
    <p class="note"><strong>Version 1.0</strong> - December 2024 &nbsp; | &nbsp; <strong>Version 2.0</strong> - December 2024</p>

  </div>
</body>
</html>
