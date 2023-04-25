import axios from 'axios';
import { apiUrl } from '@/env';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  RawDivaRun,
  CeleryTask,
  CeleryWorker
} from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      authHeaders(token)
    );
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      data,
      authHeaders(token)
    );
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(
      `${apiUrl}/api/v1/users/`,
      authHeaders(token)
    );
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(
      `${apiUrl}/api/v1/users/${userId}`,
      data,
      authHeaders(token)
    );
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async activateUser(token: string, userId: number) {
    return axios.post(
      `${apiUrl}/api/v1/users/${userId}/activate-and-send-new-account-email`,
      {},
      authHeaders(token)
    );
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token
    });
  },
  async standalone_success_pred(token: string, data: object) {
    return axios.post(`${apiUrl}/api/v1/successpred`, data, {
      responseType: 'blob'
    });
  },
  async analyzeDivaseq(token: string, divaparams: object) {
    return axios.get(`${apiUrl}/api/v1/divaseqscreenshots`, {
      ...{ params: divaparams },
      ...authHeaders(token),
      responseType: 'blob'
    });
  },
  async igvPreview(token: string, igvparams: object) {
    return axios.get(`${apiUrl}/api/v1/igvpreview/`, {
      ...{ params: igvparams },
      ...authHeaders(token)
    });
  },
  async statsSummary(token: string, statsparams: object) {
    return axios.get(`${apiUrl}/api/v1/stats_summary`, {
      ...{ params: statsparams },
      ...authHeaders(token)
    });
  },
  async getScreenshot(token: string, template_name: string) {
    return axios.get(
      `${apiUrl}/api/v1/templates/screenshot/${template_name}`,
      authHeaders(token)
    );
  },
  async updateDb(token: string) {
    return axios.post(`${apiUrl}/api/v1/db/update`, {}, authHeaders(token));
  },
  async updateDbRun(token: string, name: string) {
    return axios.post(
      `${apiUrl}/api/v1/db/update_run/${name}`,
      {},
      authHeaders(token)
    );
  },
  async getRuns(token: string) {
    return axios.get(`${apiUrl}/api/v1/runs`, authHeaders(token));
  },
  async getRun(token: string, run_id: number) {
    return axios.get(`${apiUrl}/api/v1/runs/${run_id}`, authHeaders(token));
  },
  async deleteRun(token: string, run_id: number) {
    return axios.delete(`${apiUrl}/api/v1/runs/${run_id}`, authHeaders(token));
  },
  async getTemplates(token: string, run_id: number) {
    return axios.get(
      `${apiUrl}/api/v1/templates_by_run/${run_id}`,
      authHeaders(token)
    );
  },
  async getSamples(token: string, run_id: number) {
    return axios.get(
      `${apiUrl}/api/v1/samples_by_run_with_igv/${run_id}`,
      authHeaders(token)
    );
  },
  async getSnapshots(token: string, run_id: number) {
    return axios.get(`${apiUrl}/api/v1/snapshots/${run_id}`, {
      ...authHeaders(token),
      responseType: 'blob'
    });
  },
  async getSampleData(token: string, sample_id: number) {
    return axios.get(`${apiUrl}/api/v1/samples/${sample_id}/rawdata`, {
      ...authHeaders(token),
      responseType: 'blob'
    });
  },
  async getSampleCoverage(token: string, sample_id: number) {
    return axios.get(`${apiUrl}/api/v1/samples/${sample_id}/coverage`, {
      ...authHeaders(token)
    });
  },
  async getDivaRuns(token: string) {
    return axios.get<RawDivaRun[]>(
      `${apiUrl}/api/v1/db/raw_diva_runs`,
      authHeaders(token)
    );
  },
  async getCeleryActiveTasks(token: string) {
    return axios.get<CeleryTask[]>(
      `${apiUrl}/api/v1/utils/active-celery-tasks`,
      authHeaders(token)
    );
  },
  async getCeleryReservedTasks(token: string) {
    return axios.get<CeleryTask[]>(
      `${apiUrl}/api/v1/utils/reserved-celery-tasks`,
      authHeaders(token)
    );
  },
  async getCeleryWorkers(token: string) {
    return axios.get<CeleryWorker[]>(
      `${apiUrl}/api/v1/utils/ping-celery-workers`,
      authHeaders(token)
    );
  },
  async purgeCeleryQueue(token: string) {
    return axios.post(
      `${apiUrl}/api/v1/utils/purge-celery-queue`,
      {},
      authHeaders(token)
    );
  }
};
