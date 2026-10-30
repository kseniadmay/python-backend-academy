/**
 * Python Backend Academy — Reactive State Manager
 * Персистентное локальное состояние + синхронизация (включая SRS карточек и конспектов 1/3/7/21/30)
 */

import { api } from './api.js';

const STORAGE_KEY = 'py_backend_academy_v1';

function mergeSrsMaps(baseMap, incomingMap, progressKey) {
  const a = (baseMap && typeof baseMap === 'object') ? baseMap : {};
  const b = (incomingMap && typeof incomingMap === 'object') ? incomingMap : {};
  const merged = Object.assign({}, a, b);
  Object.keys(a).concat(Object.keys(b)).forEach(key => {
    const entryA = a[key];
    const entryB = b[key];
    if (entryA && entryB && typeof entryA === 'object' && typeof entryB === 'object') {
      const pickB = String(entryB.lastReview || '') >= String(entryA.lastReview || '') ||
        Number(entryB[progressKey] || 0) > Number(entryA[progressKey] || 0);
      merged[key] = Object.assign({}, entryA, pickB ? entryB : entryA);
    } else if (entryB !== undefined) {
      merged[key] = entryB;
    } else {
      merged[key] = entryA;
    }
  });
  return merged;
}

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
      readNotes: [],
      reviewedDecks: [],
      cardRatings: {},
      cardSrs: {},
      noteSrs: {},
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
        // Серверное состояние новее — объединяем без потери SRS карточек и конспектов
        const serverState = pullResult.bundle.academyState || {};
        const mergedRatings = Object.assign({}, this.state.cardRatings || {}, serverState.cardRatings || {});
        Object.keys(this.state.cardRatings || {}).forEach(ck => {
          if (serverState.cardRatings && serverState.cardRatings[ck] !== undefined) {
            mergedRatings[ck] = Math.max(Number(this.state.cardRatings[ck]) || 0, Number(serverState.cardRatings[ck]) || 0);
          }
        });
        this.state = {
          ...this.state,
          ...serverState,
          xp: Math.max(this.state.xp || 0, serverState.xp || 0),
          completedLessons: Array.from(new Set([...(this.state.completedLessons || []), ...(serverState.completedLessons || [])])),
          completedTasks: Array.from(new Set([...(this.state.completedTasks || []), ...(serverState.completedTasks || [])])),
          readNotes: Array.from(new Set([...(this.state.readNotes || []), ...(serverState.readNotes || [])])),
          reviewedDecks: Array.from(new Set([...(this.state.reviewedDecks || []), ...(serverState.reviewedDecks || [])])),
          cardRatings: mergedRatings,
          cardSrs: mergeSrsMaps(this.state.cardSrs, serverState.cardSrs, 'reps'),
          noteSrs: mergeSrsMaps(this.state.noteSrs, serverState.noteSrs, 'step'),
          readingPositions: Object.assign({}, this.state.readingPositions || {}, serverState.readingPositions || {})
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
