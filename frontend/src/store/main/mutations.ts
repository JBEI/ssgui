import {
  IUserProfile,
  Run,
  Template,
  SamplePlusIGV,
  CeleryTask,
  CeleryWorker,
  RawDivaRun
} from '@/interfaces';
import { MainState, AppNotification } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
  setToken(state: MainState, payload: string) {
    state.token = payload;
  },
  setLoggedIn(state: MainState, payload: boolean) {
    state.isLoggedIn = payload;
  },
  setLogInError(state: MainState, payload: boolean) {
    state.logInError = payload;
  },
  setUserProfile(state: MainState, payload: IUserProfile) {
    state.userProfile = payload;
  },
  setDashboardShowDrawer(state: MainState, payload: boolean) {
    state.dashboardShowDrawer = payload;
  },
  addNotification(state: MainState, payload: AppNotification) {
    state.notifications.push(payload);
  },
  removeNotification(state: MainState, payload: AppNotification) {
    state.notifications = state.notifications.filter(
      notification => notification !== payload
    );
  },
  setRuns(state: MainState, payload: Run[]) {
    state.runs = payload;
  },
  setActiveRun(state: MainState, payload: Run) {
    state.activeRun = payload;
  },
  setActiveSamples(state: MainState, payload: SamplePlusIGV[]) {
    state.activeSamples = payload;
  },
  setActiveCeleryTasks(state: MainState, payload: CeleryTask[]) {
    state.activeCeleryTasks = payload;
  },
  setReservedCeleryTasks(state: MainState, payload: CeleryTask[]) {
    state.reservedCeleryTasks = payload;
  },
  setCeleryWorkers(state: MainState, payload: CeleryWorker[]) {
    state.celeryWorkers = payload;
  },
  setDivaRuns(state: MainState, payload: RawDivaRun[]) {
    state.rawDivaRuns = payload;
  }
};

const { commit } = getStoreAccessors<MainState | any, State>('');

export const commitSetDashboardShowDrawer = commit(
  mutations.setDashboardShowDrawer
);
export const commitSetLoggedIn = commit(mutations.setLoggedIn);
export const commitSetLogInError = commit(mutations.setLogInError);
export const commitSetToken = commit(mutations.setToken);
export const commitSetUserProfile = commit(mutations.setUserProfile);
export const commitAddNotification = commit(mutations.addNotification);
export const commitRemoveNotification = commit(mutations.removeNotification);
export const commitSetRuns = commit(mutations.setRuns);
export const commitSetActiveRun = commit(mutations.setActiveRun);
export const commitSetActiveSamples = commit(mutations.setActiveSamples);
export const commitSetActiveCeleryTasks = commit(
  mutations.setActiveCeleryTasks
);
export const commitSetReservedCeleryTasks = commit(
  mutations.setReservedCeleryTasks
);
export const commitSetCeleryWorkers = commit(mutations.setCeleryWorkers);
export const commitSetDivaRuns = commit(mutations.setDivaRuns);
