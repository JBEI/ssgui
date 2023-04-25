import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { MainState } from './state';

const defaultState: MainState = {
  isLoggedIn: null,
  token: '',
  logInError: false,
  userProfile: null,
  dashboardShowDrawer: true,
  notifications: [],
  runs: [],
  activeRun: null,
  activeSamples: [],
  rawDivaRuns: [],
  activeCeleryTasks: [],
  reservedCeleryTasks: [],
  celeryWorkers: []
};

export const mainModule = {
  state: defaultState,
  mutations,
  actions,
  getters
};
