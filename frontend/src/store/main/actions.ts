import { api } from '@/api';
import router from '@/router';
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import {
  commitAddNotification,
  commitRemoveNotification,
  commitSetLoggedIn,
  commitSetLogInError,
  commitSetToken,
  commitSetUserProfile,
  commitSetRuns,
  commitSetActiveRun,
  commitSetActiveSamples,
  commitSetActiveCeleryTasks,
  commitSetReservedCeleryTasks,
  commitSetCeleryWorkers,
  commitSetDivaRuns
} from './mutations';
import { AppNotification, MainState } from './state';

type MainContext = ActionContext<MainState, State>;

export const actions = {
  async actionLogIn(
    context: MainContext,
    payload: { username: string; password: string }
  ) {
    try {
      const response = await api.logInGetToken(
        payload.username,
        payload.password
      );
      const token = response.data.access_token;
      if (token) {
        saveLocalToken(token);
        commitSetToken(context, token);
        commitSetLoggedIn(context, true);
        commitSetLogInError(context, false);
        await dispatchGetUserProfile(context);
        await dispatchRouteLoggedIn(context);
        commitAddNotification(context, {
          content: 'Logged in',
          color: 'success'
        });
      } else {
        await dispatchLogOut(context);
      }
    } catch (err) {
      commitSetLogInError(context, true);
      await dispatchLogOut(context);
    }
  },
  async actionGetUserProfile(context: MainContext) {
    try {
      const response = await api.getMe(context.state.token);
      if (response.data) {
        commitSetUserProfile(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateUserProfile(context: MainContext, payload) {
    try {
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateMe(context.state.token, payload),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitSetUserProfile(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Profile successfully updated',
        color: 'success'
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionActivateUser(context: MainContext, userId: number) {
    try {
      const loadingNotification = {
        content: 'Activating user',
        showProgress: true
      };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.activateUser(context.state.token, userId),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'User successfully activated',
        color: 'success'
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCheckLoggedIn(context: MainContext) {
    if (!context.state.isLoggedIn) {
      let token = context.state.token;
      if (!token) {
        const localToken = getLocalToken();
        if (localToken) {
          commitSetToken(context, localToken);
          token = localToken;
        }
      }
      if (token) {
        try {
          const response = await api.getMe(token);
          commitSetLoggedIn(context, true);
          commitSetUserProfile(context, response.data);
        } catch (error) {
          await dispatchRemoveLogIn(context);
        }
      } else {
        await dispatchRemoveLogIn(context);
      }
    }
  },
  async actionRemoveLogIn(context: MainContext) {
    removeLocalToken();
    commitSetToken(context, '');
    commitSetLoggedIn(context, false);
  },
  async actionLogOut(context: MainContext) {
    await dispatchRemoveLogIn(context);
    await dispatchRouteLogOut(context);
  },
  async actionUserLogOut(context: MainContext) {
    await dispatchLogOut(context);
    commitAddNotification(context, { content: 'Logged out', color: 'success' });
  },
  actionRouteLogOut(context: MainContext) {
    if (router.currentRoute.path !== '/login') {
      router.push('/login');
    }
  },
  async actionCheckApiError(context: MainContext, payload: AxiosError) {
    if (payload.response!.status === 401) {
      //await dispatchLogOut(context);
    }
  },
  actionRouteLoggedIn(context: MainContext) {
    if (
      router.currentRoute.path === '/login' ||
      router.currentRoute.path === '/'
    ) {
      router.push('/main');
    }
  },
  async removeNotification(
    context: MainContext,
    payload: { notification: AppNotification; timeout: number }
  ) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commitRemoveNotification(context, payload.notification);
        resolve(true);
      }, payload.timeout);
    });
  },
  async passwordRecovery(context: MainContext, payload: { username: string }) {
    const loadingNotification = {
      content: 'Sending password recovery email',
      showProgress: true
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.passwordRecovery(payload.username),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Password recovery email sent',
        color: 'success'
      });
      await dispatchLogOut(context);
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Incorrect username'
      });
    }
  },
  async resetPassword(
    context: MainContext,
    payload: { password: string; token: string }
  ) {
    const loadingNotification = {
      content: 'Resetting password',
      showProgress: true
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.resetPassword(payload.password, payload.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Password successfully reset',
        color: 'success'
      });
      await dispatchLogOut(context);
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Error resetting password'
      });
    }
  },
  async actionStandaloneSuccessPred(context: MainContext, payload: object) {
    const loadingNotification = {
      content: '[something abt loading success predictions]',
      showProgress: true,
      indefinite: true
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.standalone_success_pred(context.state.token, payload),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: '[] successfully created',
        color: 'success'
      });
      return response;
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, { color: 'error', content: 'Error []' });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateDatabase(context: MainContext) {
    const loadingNotification = {
      content: 'Updating Database - this may take a while',
      showProgress: true,
      indefinite: true
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateDb(context.state.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Database update successfully added to queue',
        color: 'success'
      });
      return response;
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Error updating database'
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetRuns(context: MainContext) {
    try {
      const response = (
        await Promise.all([
          api.getRuns(context.state.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitSetRuns(context, response.data);
      return response;
    } catch (error) {
      commitAddNotification(context, {
        color: 'error',
        content: 'Error loading sequencing runs'
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetRun(context: MainContext, run_id: number) {
    try {
      const response = (
        await Promise.all([
          api.getRun(context.state.token, run_id),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitSetActiveRun(context, response.data);
      return response;
    } catch (error) {
      commitAddNotification(context, {
        color: 'error',
        content: 'Error loading active run'
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionDeleteRun(context: MainContext, run_id: number) {
    try {
      const response = (
        await Promise.all([
          api.deleteRun(context.state.token, run_id),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitAddNotification(context, {
        content: 'Runs successfully deleted',
        color: 'success'
      });
      commitSetActiveRun(context, response.data);
      return response;
    } catch (error) {
      commitAddNotification(context, {
        color: 'error',
        content: 'Error deleting run'
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetSamples(context: MainContext, run_id: number) {
    try {
      const response = (
        await Promise.all([
          api.getSamples(context.state.token, run_id),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitSetActiveSamples(context, response.data);
      return response;
    } catch (error) {
      commitAddNotification(context, {
        color: 'error',
        content: 'Error loading Samples'
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetSnapshots(context: MainContext, run_id: number) {
    const loadingNotification = {
      content: 'Retrieving snapshots...',
      showProgress: true,
      indefinite: true
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.getSnapshots(context.state.token, run_id),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Snapshots found.',
        color: 'success'
      });
      return response;
    } catch (error) {
      commitAddNotification(context, {
        color: 'error',
        content: 'Error downloading snapshots'
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetSampleData(context: MainContext, sample_id: number) {
    const loadingNotification = {
      content: 'Retrieving sample data...',
      showProgress: true,
      indefinite: true
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.getSampleData(context.state.token, sample_id),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Sample data found.',
        color: 'success'
      });
      return response;
    } catch (error) {
      commitAddNotification(context, {
        color: 'error',
        content: 'Error downloading sample data'
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetSampleCoverage(context: MainContext, sample_id: number) {
    try {
      const response = (
        await Promise.all([
          api.getSampleCoverage(context.state.token, sample_id),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      return response;
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetActiveCeleryTasks(context: MainContext) {
    try {
      const response = (
        await Promise.all([
          api.getCeleryActiveTasks(context.state.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitSetActiveCeleryTasks(context, response.data);
      return response;
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetReservedCeleryTasks(context: MainContext) {
    try {
      const response = (
        await Promise.all([
          api.getCeleryReservedTasks(context.state.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitSetReservedCeleryTasks(context, response.data);
      return response;
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetCeleryWorkers(context: MainContext) {
    try {
      const response = (
        await Promise.all([
          api.getCeleryWorkers(context.state.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitSetCeleryWorkers(context, response.data);
      return response;
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetDivaRuns(context: MainContext) {
    try {
      const response = (
        await Promise.all([
          api.getDivaRuns(context.state.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitSetDivaRuns(context, response.data);
      return response;
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateDatabaseRun(context: MainContext, name: string) {
    const loadingNotification = {
      content: 'Updating Database Run...',
      showProgress: true,
      indefinite: true
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateDbRun(context.state.token, name),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Run update successfully added to queue',
        color: 'success'
      });
      return response;
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Error adding run update to queue'
      });
      await dispatchCheckApiError(context, error);
    }
  },
  async actionPurgeCeleryQueue(context: MainContext) {
    const loadingNotification = {
      content: 'Purging celery queue...',
      showProgress: true,
      indefinite: true
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.purgeCeleryQueue(context.state.token),
          await new Promise<void>((resolve, reject) =>
            setTimeout(() => resolve(), 500)
          )
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Queue successfully purged',
        color: 'success'
      });
      return response;
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Error purging queue'
      });
      await dispatchCheckApiError(context, error);
    }
  }
};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetUserProfile = dispatch(actions.actionGetUserProfile);
export const dispatchLogIn = dispatch(actions.actionLogIn);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchUpdateUserProfile = dispatch(
  actions.actionUpdateUserProfile
);
export const dispatchActivateUser = dispatch(actions.actionActivateUser);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchPasswordRecovery = dispatch(actions.passwordRecovery);
export const dispatchResetPassword = dispatch(actions.resetPassword);
export const dispatchStandaloneSuccessPred = dispatch(
  actions.actionStandaloneSuccessPred
);
export const dispatchUpdateDatabase = dispatch(actions.actionUpdateDatabase);
export const dispatchGetRuns = dispatch(actions.actionGetRuns);
export const dispatchGetRun = dispatch(actions.actionGetRun);
export const dispatchDeleteRun = dispatch(actions.actionDeleteRun);
export const dispatchGetSamples = dispatch(actions.actionGetSamples);
export const dispatchGetSnapshots = dispatch(actions.actionGetSnapshots);
export const dispatchGetSampleData = dispatch(actions.actionGetSampleData);
export const dispatchGetSampleCoverage = dispatch(
  actions.actionGetSampleCoverage
);
export const dispatchGetActiveCeleryTasks = dispatch(
  actions.actionGetActiveCeleryTasks
);
export const dispatchGetReservedCeleryTasks = dispatch(
  actions.actionGetReservedCeleryTasks
);
export const dispatchGetCeleryWorkers = dispatch(
  actions.actionGetCeleryWorkers
);
export const dispatchPurgeCeleryQueue = dispatch(
  actions.actionPurgeCeleryQueue
);
export const dispatchUpdateDatabaseRun = dispatch(
  actions.actionUpdateDatabaseRun
);
export const dispatchGetDivaRuns = dispatch(actions.actionGetDivaRuns);
