import { MainState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
  hasAdminAccess: (state: MainState) => {
    return (
      state.userProfile &&
      state.userProfile.is_superuser &&
      state.userProfile.is_active
    );
  },
  loginError: (state: MainState) => state.logInError,
  dashboardShowDrawer: (state: MainState) => state.dashboardShowDrawer,
  userProfile: (state: MainState) => state.userProfile,
  token: (state: MainState) => state.token,
  isLoggedIn: (state: MainState) => state.isLoggedIn,
  firstNotification: (state: MainState) =>
    state.notifications.length > 0 && state.notifications[0],
  runs: (state: MainState) => state.runs,
  activeRun: (state: MainState) => state.activeRun,
  activeSamples: (state: MainState) => state.activeSamples,
  activeCeleryTasks: (state: MainState) => state.activeCeleryTasks,
  reservedCeleryTasks: (state: MainState) => state.reservedCeleryTasks,
  celeryWorkers: (state: MainState) => state.celeryWorkers,
  rawDivaRuns: (state: MainState) => state.rawDivaRuns
};

const { read } = getStoreAccessors<MainState, State>('');

export const readDashboardShowDrawer = read(getters.dashboardShowDrawer);
export const readHasAdminAccess = read(getters.hasAdminAccess);
export const readIsLoggedIn = read(getters.isLoggedIn);
export const readLoginError = read(getters.loginError);
export const readToken = read(getters.token);
export const readUserProfile = read(getters.userProfile);
export const readFirstNotification = read(getters.firstNotification);
export const readRuns = read(getters.runs);
export const readActiveRun = read(getters.activeRun);
export const readActiveSamples = read(getters.activeSamples);
export const readActiveCeleryTasks = read(getters.activeCeleryTasks);
export const readReservedCeleryTasks = read(getters.reservedCeleryTasks);
export const readCeleryWorkers = read(getters.celeryWorkers);
export const readRawDivaRuns = read(getters.rawDivaRuns);
