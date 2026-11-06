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


  // --- SRS & FSRS Spaced Repetition API ---

  async fetchSrsDue(echelon = null, deckId = null, limit = 50) {
    const params = new URLSearchParams();
    if (echelon) params.append('echelon', echelon);
    if (deckId) params.append('deck_id', deckId);
    if (limit) params.append('limit', limit);
    const query = params.toString() ? `?${params.toString()}` : '';
    return await this._request(`/api/v1/srs/due${query}`);
  }

  async rateSrsCard(cardId, deckId, rating, durationMs = null) {
    return await this._request('/api/v1/srs/rate', {
      method: 'POST',
      body: JSON.stringify({
        card_id: cardId,
        deck_id: deckId,
        rating: Number(rating),
        duration_ms: durationMs
      })
    });
  }

  async fetchSrsStats() {
    return await this._request('/api/v1/srs/stats');
  }

  async fetchSrsCardState(cardId) {
    return await this._request(`/api/v1/srs/card/${encodeURIComponent(cardId)}`);
  }


  // --- Navigation & App Shell API ---

  async fetchNavigationMeta() {
    return await this._request('/api/v1/navigation/meta');
  }


  // --- Practice & Task Execution API ---

  async runTaskCode(taskId, code) {
    return await this._request('/api/v1/practice/run', {
      method: 'POST',
      body: JSON.stringify({
        task_id: Number(taskId),
        code
      })
    });
  }

  async fetchTaskHints(taskId, level = 1) {
    return await this._request(`/api/v1/practice/hint/${encodeURIComponent(taskId)}?level=${level}`);
  }

  async saveTaskDraft(taskId, draftCode) {
    return await this._request('/api/v1/practice/draft', {
      method: 'POST',
      body: JSON.stringify({
        task_id: Number(taskId),
        draft_code: draftCode
      })
    });
  }

  async fetchTaskDraft(taskId) {
    return await this._request(`/api/v1/practice/draft/${encodeURIComponent(taskId)}`);
  }


  // --- Path & Trail Progression API ---

  async fetchPathOverview() {
    return await this._request('/api/v1/path/overview');
  }

  async fetchEchelonPath(echelonId) {
    return await this._request(`/api/v1/path/echelon/${encodeURIComponent(echelonId)}`);
  }


  // --- Atomic Notes & Reader API ---

  async fetchNoteDetail(noteId) {
    return await this._request(`/api/v1/notes/${encodeURIComponent(noteId)}`);
  }

  async saveNoteProgress(noteId, stepIndex, isCompleted = false) {
    return await this._request('/api/v1/notes/progress', {
      method: 'POST',
      body: JSON.stringify({
        note_id: noteId,
        step_index: Number(stepIndex),
        is_completed: Boolean(isCompleted)
      })
    });
  }

  async fetchDueNotes() {
    return await this._request('/api/v1/notes/due');
  }


  // --- Mock Technical Interview API ---

  async fetchMockSession(echelon = 1, taskId = null) {
    const params = new URLSearchParams({ echelon });
    if (taskId) params.append('task_id', taskId);
    return await this._request(`/api/v1/mock/session?${params.toString()}`);
  }

  async evaluateMockTask(sessionId, taskId, code, hintsUsed = 0) {
    return await this._request('/api/v1/mock/evaluate', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        task_id: Number(taskId),
        code,
        hints_used: Number(hintsUsed)
      })
    });
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
