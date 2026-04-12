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

    async load() {
        try {
            const Response = await fetch('/api/backup');
            if (Response.ok) {
                const Data = await Response.json();
                if (Data.characters && Data.characters.length > 0) {
                    this.knownChars = new Set(Data.characters);
                    this.save();
                    console.log(`Loaded ${this.knownChars.size} characters from server backup`);
                    return;
                }
            }
        } catch (e) {
            console.log('No server backup found, trying localStorage');
        }
        
        try {
            const Saved = localStorage.getItem(STORAGE_KEYS.KNOWN_CHARS);
            if (Saved) {
                const Data = JSON.parse(Saved);
                this.knownChars = new Set(Data.characters || []);
                console.log(`Loaded ${this.knownChars.size} characters from localStorage`);
            }
        } catch (e) {
            console.error("Failed to load from localStorage:", e);
        }
    }

    async saveToServer() {
        try {
            const Data = {
                version: STATE_VERSION,
                lastUpdated: new Date().toISOString(),
                characters: Array.from(this.knownChars),
                count: this.knownChars.size
            };
            const Response = await fetch('/api/backup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(Data)
            });
            if (Response.ok) {
                console.log(`Saved ${this.knownChars.size} characters to server backup`);
                return true;
            }
        } catch (e) {
            console.error('Failed to save to server:', e);
        }
        return false;
    }

    save() {
        try {
            const Data = {
                version: STATE_VERSION,
                lastUpdated: new Date().toISOString(),
                characters: Array.from(this.knownChars),
                count: this.knownChars.size
            };
            localStorage.setItem(STORAGE_KEYS.KNOWN_CHARS, JSON.stringify(Data));
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
            const Saved = localStorage.getItem(STORAGE_KEYS.TARGET_CHARS);
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
        const CHARS_ARRAY = this.getCharacters();
        if (CHARS_ARRAY.length === 0) {
            alert("No characters to export.");
            return null;
        }
        const EXPORT_DATA = {
            version: STATE_VERSION,
            date: new Date().toISOString(),
            characters: CHARS_ARRAY,
            count: CHARS_ARRAY.length
        };
        const JSON_STR = JSON.stringify(EXPORT_DATA, null, 2);
        const Blob = new Blob([JSON_STR], { type: 'application/json' });
        const Url = URL.createObjectURL(Blob);
        const a = document.createElement('a');
        a.href = Url;
        a.download = `mandarin_chars_${new Date().toISOString().slice(0,19).replace(/:/g, '-')}.json`;
        a.click();
        URL.revokeObjectURL(Url);
        return EXPORT_DATA;
    }

    importFromFile(file, callback) {
        const Reader = new FileReader();
        Reader.onload = (e) => {
            try {
                const Data = JSON.parse(e.target.result);
                let CHARS_ARRAY;
                if (Array.isArray(Data)) CHARS_ARRAY = Data;
                else if (Data.characters && Array.isArray(Data.characters)) CHARS_ARRAY = Data.characters;
                else throw new Error("Invalid format");
                const VALID_CHARS = CHARS_ARRAY.filter(ch => typeof ch === 'string' && ch.length === 1);
                if (VALID_CHARS.length === 0) throw new Error("No valid characters found");
                this.setCharacters(VALID_CHARS);
                if (callback) callback(null, VALID_CHARS);
            } catch (err) {
                if (callback) callback(err);
            }
        };
        Reader.onerror = () => callback(new Error("File read error"));
        Reader.readAsText(file, 'UTF-8');
    }

    mergeFromFile(file, callback) {
        const Reader = new FileReader();
        Reader.onload = (e) => {
            try {
                const Data = JSON.parse(e.target.result);
                let CHARS_ARRAY;
                if (Array.isArray(Data)) CHARS_ARRAY = Data;
                else if (Data.characters && Array.isArray(Data.characters)) CHARS_ARRAY = Data.characters;
                else throw new Error("Invalid format");
                const VALID_CHARS = CHARS_ARRAY.filter(ch => typeof ch === 'string' && ch.length === 1);
                if (VALID_CHARS.length === 0) throw new Error("No valid characters found");
                const Added = this.addCharacters(VALID_CHARS);
                if (callback) callback(null, { added: Added, total: VALID_CHARS.length });
            } catch (err) {
                if (callback) callback(err);
            }
        };
        Reader.onerror = () => callback(new Error("File read error"));
        Reader.readAsText(file, 'UTF-8');
    }

    clear() {
        this.knownChars.clear();
        this.save();
    }
}

window.mandarinState = new MandarinState();
