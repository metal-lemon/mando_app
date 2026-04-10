// shared_state.js - Central data management for all Mandarin tools

const STATE_VERSION = "1.0";
const STORAGE_KEYS = {
    KNOWN_CHARS: "mandarin_known_chars",
    TARGET_TEXT: "mandarin_target_text",
    TARGET_CHARS: "mandarin_target_chars",
    LAST_UPDATED: "mandarin_last_updated"
};

class MandarinState {
    constructor() {
        this.listeners = new Set();
        this.knownChars = new Set();
        this.load();
    }

    load() {
        try {
            const saved = localStorage.getItem(STORAGE_KEYS.KNOWN_CHARS);
            if (saved) {
                const data = JSON.parse(saved);
                this.knownChars = new Set(data.characters || []);
                console.log(`Loaded ${this.knownChars.size} characters from localStorage`);
            }
        } catch (e) {
            console.error("Failed to load from localStorage:", e);
        }
    }

    save() {
        try {
            const data = {
                version: STATE_VERSION,
                lastUpdated: new Date().toISOString(),
                characters: Array.from(this.knownChars),
                count: this.knownChars.size
            };
            localStorage.setItem(STORAGE_KEYS.KNOWN_CHARS, JSON.stringify(data));
            this.listeners.forEach(listener => listener(this.knownChars));
        } catch (e) {
            console.error("Failed to save to localStorage:", e);
        }
    }

    addCharacter(char) {
        if (char && char.length === 1 && !this.knownChars.has(char)) {
            this.knownChars.add(char);
            this.save();
            return true;
        }
        return false;
    }

    removeCharacter(char) {
        if (this.knownChars.has(char)) {
            this.knownChars.delete(char);
            this.save();
            return true;
        }
        return false;
    }

    addCharacters(chars) {
        let added = 0;
        for (let ch of chars) {
            if (ch && ch.length === 1 && !this.knownChars.has(ch)) {
                this.knownChars.add(ch);
                added++;
            }
        }
        if (added > 0) this.save();
        return added;
    }

    setCharacters(chars) {
        this.knownChars = new Set(chars.filter(ch => ch && ch.length === 1));
        this.save();
    }

    getCharacters() {
        return Array.from(this.knownChars);
    }

    has(char) {
        return this.knownChars.has(char);
    }

    getCount() {
        return this.knownChars.size;
    }

    getTargetText() {
        try {
            return localStorage.getItem(STORAGE_KEYS.TARGET_TEXT) || '';
        } catch (e) {
            return '';
        }
    }

    setTargetText(text) {
        try {
            localStorage.setItem(STORAGE_KEYS.TARGET_TEXT, text || '');
        } catch (e) {
            console.error('Failed to save target text:', e);
        }
    }

    getTargetChars() {
        try {
            const saved = localStorage.getItem(STORAGE_KEYS.TARGET_CHARS);
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            return [];
        }
    }

    setTargetChars(chars) {
        try {
            localStorage.setItem(STORAGE_KEYS.TARGET_CHARS, JSON.stringify(chars || []));
        } catch (e) {
            console.error('Failed to save target chars:', e);
        }
    }

    subscribe(callback) {
        this.listeners.add(callback);
        return () => this.listeners.delete(callback);
    }

    exportToFile() {
        const charsArray = this.getCharacters();
        if (charsArray.length === 0) {
            alert("No characters to export.");
            return null;
        }
        const exportData = {
            version: STATE_VERSION,
            date: new Date().toISOString(),
            characters: charsArray,
            count: charsArray.length
        };
        const jsonStr = JSON.stringify(exportData, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `mandarin_chars_${new Date().toISOString().slice(0,19).replace(/:/g, '-')}.json`;
        a.click();
        URL.revokeObjectURL(url);
        return exportData;
    }

    importFromFile(file, callback) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                let charsArray;
                if (Array.isArray(data)) charsArray = data;
                else if (data.characters && Array.isArray(data.characters)) charsArray = data.characters;
                else throw new Error("Invalid format");
                const validChars = charsArray.filter(ch => typeof ch === 'string' && ch.length === 1);
                if (validChars.length === 0) throw new Error("No valid characters found");
                this.setCharacters(validChars);
                if (callback) callback(null, validChars);
            } catch (err) {
                if (callback) callback(err);
            }
        };
        reader.onerror = () => callback(new Error("File read error"));
        reader.readAsText(file, 'UTF-8');
    }

    mergeFromFile(file, callback) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                let charsArray;
                if (Array.isArray(data)) charsArray = data;
                else if (data.characters && Array.isArray(data.characters)) charsArray = data.characters;
                else throw new Error("Invalid format");
                const validChars = charsArray.filter(ch => typeof ch === 'string' && ch.length === 1);
                if (validChars.length === 0) throw new Error("No valid characters found");
                const added = this.addCharacters(validChars);
                if (callback) callback(null, { added, total: validChars.length });
            } catch (err) {
                if (callback) callback(err);
            }
        };
        reader.onerror = () => callback(new Error("File read error"));
        reader.readAsText(file, 'UTF-8');
    }

    clear() {
        this.knownChars.clear();
        this.save();
    }
}

window.mandarinState = new MandarinState();
