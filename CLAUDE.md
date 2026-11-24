# PROJEKT-MASTERFILE – FEUERRAUM
Gilt zusätzlich zur globalen Masterfile (~/.claude/CLAUDE.md).

## 1. Ziel und Endprodukt
Interaktive Demo-Webseite für einen erfundenen Betrieb (Kamin- und Ofenstudio mit eigenen Ofenbauern) „FEUERRAUM“. Musterbeispiel für Akquise (PROJEKT EX), Niveau wie WARMHERZ, FARBKANTE, LICHTBOGEN.
Probleme, die die Seite löst: Aufwendige Beratung vor Ort (Foto schicken, passt er rein?), Leistung nach Raumgröße, Holz/Pellet/Gas-Vergleich, Herbst-Ansturm (früher planen), Wartung, Ofenbauer-Nachwuchs.

## 2. Qualitätsanspruch & Referenzen
- Aufbau wie FLUTLICHT27/FARBKANTE: Film-Kapitel (Scrollen spult das Video) im Wechsel mit Motion-Design-Kapiteln, Übergänge Film ↔ Grafik.
- Fotolook 4K, cinematic, dunkle Farbwelt mit EINER Akzentfarbe (Glut-Orange).
- Leitmotiv eindeutig zum Gewerk: Erste Flamme, Ofenbauer beim Einbau (Aufmaß → Anschluss → Verkleidung → Abnahme Schornsteinfeger), Ausstellung mit brennenden Öfen.

## 3. Regeln für dieses Projekt
- Keine echten Firmen/Personen, keine Preise/Euro, kein Wort „KI“, keine Rechtsaussagen. Demo-Hinweis, Formulare senden nichts, `?firma=Name`.
- Bewertungen nur als markierte Beispiele, bis echte Daten vorliegen.
- Mobil-Prüfung 390×844, 360×740, 430×932, 844×390 + Kopfzeile 1081–1600 px.
- Recruiting-Kapitel (Film + Bewerbung in 60 s) Pflicht.

## 4. Skills, Plugins, Agenten, MCP
claude-in-chrome (sjinn.ai Unlimited). Sonst nichts.

## 5. Zugänge
gh (Engelstraenen), sjinn in Chrome eingeloggt.

## 6. Workflow & Freigabepunkte
3 Storyboards (konzepte/) → Eugens Wahl → First Frames 4K → Video-Drafts gratis → Seite bauen → Storyboard-Abgleich → GitHub Pages.

## 7. Befehle
- Vorschau: `python3 tools/serve.py 4460` → http://localhost:4460 (Port 4460 = FEUERRAUM)
- Bilder: im sjinn-Tab `JSON.stringify(SB.harvest2())` → `tools/urls.json`, dann `python3 tools/assets.py tools/urls.json` (Namen-Zuordnung FRA-xx → Dateiname in assets.py)
- Videos: `python3 tools/video.py assets-roh/vid/<roh>.mp4 <section-id> <datei>` (flamme→flamme, oefen→showroom, karriere→karriere), danach `python3 tools/assets.py`
- Handy-Prüfung: `python3 tools/mobil_check.py http://localhost:4460/`

## 8. Offene Fragen
- keine

## 9. Entschieden
- 24.11.2026: Video-Drafts auf Dreamina Seedance 2.5 720P Unlimited (Wächter `FRW` im Dreamina-Tab, klickt nur bei Schalter an + Preis 0). Download über Hover → „Download“ → ~/Downloads (Eugens OK 24.11.). Drafts: FRV1 Flamme (Dreamina), FRV2 Showroom (Wan 480p), FRV3 Karriere (MiniMax 768p).
- 24.11.2026: Dateien aus dem side-session-notes-Ordner kamen bei Eugen NICHT an (Videos/Bilder „nichts geschickt“). Vorschauen nach `vorschau/` im Projektordner (= Arbeitsordner der Sitzung) legen und von dort schicken, dazu direkte Links.
- 23.11.2026 (Eugen „top“): Mix-Storyboard FR4 (konzepte/4-mix.png) bestätigt = verbindliche Vorlage, Frame für Frame bauen.
- 23.11.2026 (Eugen): Mix aus Storyboard 1 (Erste Flamme) und 3 (Showroom). Kapitel: Film Erste Flamme (kalt → Streichholz → warm) · Showroom-Fahrt 5 Feuerarten · Rechner (Wohnsituation, m², kW, Holz/Pellet/Gas) · Passt er rein? (Foto + Ofen ziehen) · Ofen-Check · Früh planen (Monatsleiste) · Karriere-Film + Kinetik · Bewerbung 60 s · Bewertungen (Beispiel) · Ausstellung + Termin.
- 23.11.2026: Sitzung von der Fahrschul-Sitzung gelöst (eigenständig). Bilder an Eugen aus lokalem Ordner außerhalb Dropbox schicken, Dropbox-Pfade kamen nicht an.
- 23.11.2026: Name FEUERRAUM (Annahme). 3 Storyboards auf sjinn (Nano Banana 2.1, 2K, Unlimited), Prompts im sjinn-Verlauf, Alt-Text beginnt mit FR1/FR2/FR3.
- 23.11.2026: Alle 3 Storyboards fertig (2752×1536). Annahme eines sjinn-Auftrags nur per `SB.details()` prüfen (Zähler zählt fremde Aufträge mit).

## 10. Ablage
Code + Konzepte: Dropbox/CLAUDE/Projekte/FEUERRAUM
