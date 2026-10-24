/**
 * Python Backend Academy — API Client
 * Взаимодействие с сервисом FastAPI по стандарту REST/JSON
 */

export class AcademyApi {
  constructor(baseUrl = '') {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  async _request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json'
    };

    const token = localStorage.getItem('pba_sync_token');
    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...(options.headers || {})
      }
    });

    if (!response.ok && response.status !== 409) {
      throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }

  // --- Content API ---

  async fetchSummary() {
    return await this._request('/api/v1/content/summary');
  }

  async fetchModules() {
    return await this._request('/api/v1/content/modules');
  }

  async fetchNote(noteId) {
    return await this._request(`/api/v1/content/notes/${encodeURIComponent(noteId)}`);
  }

  async fetchDeck(deckId) {
    return await this._request(`/api/v1/content/cards/${encodeURIComponent(deckId)}`);
  }

  async fetchTasks(level = null, topic = null) {
    const params = new URLSearchParams();
    if (level) params.append('level', level);
    if (topic) params.append('topic', topic);
    const query = params.toString() ? `?${params.toString()}` : '';
    return await this._request(`/api/v1/content/tasks${query}`);
  }

  async fetchTask(taskId) {
    return await this._request(`/api/v1/content/tasks/${encodeURIComponent(taskId)}`);
  }

  async searchContent(query) {
    return await this._request(`/api/v1/content/search?q=${encodeURIComponent(query)}`);
  }

  // --- Sync API ---

  async pullProgress() {
    return await this._request('/api/v1/sync');
  }

  async pushProgress(bundle, baseUpdatedAt = 0, device = 'web-client', clientId = null) {
    return await this._request('/api/v1/sync', {
      method: 'POST',
      body: JSON.stringify({
        bundle,
        baseUpdatedAt,
        device,
        clientId: clientId || this.getClientId()
      })
    });
  }

  // --- Feedback API ---

  async submitFeedback(context, message, meta = {}) {
    return await this._request('/api/v1/feedback', {
      method: 'POST',
      body: JSON.stringify({
        context,
        message,
        userAgent: navigator.userAgent,
        meta
      })
    });
  }

  getClientId() {
    let id = localStorage.getItem('pba_client_id');
    if (!id) {
      id = 'client_' + Math.random().toString(36).substring(2, 10);
      localStorage.setItem('pba_client_id', id);
    }
    return id;
  }
}

export const api = new AcademyApi();
