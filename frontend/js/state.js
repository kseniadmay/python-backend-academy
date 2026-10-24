/**
 * Python Backend Academy — Reactive State Manager
 * Персистентное локальное состояние + синхронизация
 */

import { api } from './api.js';

const STORAGE_KEY = 'py_backend_academy_v1';

export class StateManager {
  constructor() {
    this.listeners = new Set();
    this.state = this._loadInitialState();
    this.lastSyncedAt = 0;
  }

  _loadInitialState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        return JSON.parse(raw);
      }
    } catch (e) {
      console.error('[State] Ошибка чтения localStorage:', e);
    }

    return {
      xp: 0,
      streak: 1,
      dailyXp: 0,
      lastActiveDate: new Date().toISOString().split('T')[0],
      completedLessons: [],
      completedTasks: [],
      cardsProgress: {},
      readingPositions: {}
    };
  }

  getState() {
    return this.state;
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  _notify() {
    for (const listener of this.listeners) {
      try {
        listener(this.state);
      } catch (e) {
        console.error('[State] Ошибка в слушателе состояния:', e);
      }
    }
  }

  save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
      this._notify();
    } catch (e) {
      console.error('[State] Ошибка сохранения localStorage:', e);
    }
  }

  addXp(amount) {
    if (!amount || amount <= 0) return;
    this.state.xp = (this.state.xp || 0) + amount;
    this.state.dailyXp = (this.state.dailyXp || 0) + amount;
    this.save();
  }

  markLessonCompleted(lessonId) {
    if (!this.state.completedLessons.includes(lessonId)) {
      this.state.completedLessons.push(lessonId);
      this.save();
    }
  }

  markTaskCompleted(taskId) {
    if (!this.state.completedTasks.includes(taskId)) {
      this.state.completedTasks.push(taskId);
      this.save();
    }
  }

  async syncWithServer() {
    try {
      const pullResult = await api.pullProgress();
      if (pullResult && pullResult.bundle && pullResult.updatedAt > this.lastSyncedAt) {
        // Серверное состояние новее — объединяем
        const serverState = pullResult.bundle.academyState || {};
        this.state = {
          ...this.state,
          ...serverState,
          xp: Math.max(this.state.xp || 0, serverState.xp || 0),
          completedLessons: Array.from(new Set([...(this.state.completedLessons || []), ...(serverState.completedLessons || [])])),
          completedTasks: Array.from(new Set([...(this.state.completedTasks || []), ...(serverState.completedTasks || [])]))
        };
        this.lastSyncedAt = pullResult.updatedAt;
        this.save();
      }

      // Отправляем актуальный локальный бандл
      const pushResult = await api.pushProgress(
        {
          academyState: this.state,
          ideStatus: {},
          ideDrafts: {}
        },
        this.lastSyncedAt,
        'web-modular-client'
      );

      if (pushResult && pushResult.ok) {
        this.lastSyncedAt = pushResult.updatedAt;
      }
    } catch (e) {
      console.warn('[State] Ошибка синхронизации с сервером (оффлайн режим):', e);
    }
  }
}

export const stateManager = new StateManager();
