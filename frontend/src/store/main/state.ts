import {
  CeleryTask,
  CeleryWorker,
  IUserProfile,
  RawDivaRun,
  Run,
  SamplePlusIGV
} from '@/interfaces';

export interface AppNotification {
  content: string;
  color?: string;
  showProgress?: boolean;
  indefinite?: boolean;
}

export interface MainState {
  token: string;
  isLoggedIn: boolean | null;
  logInError: boolean;
  userProfile: IUserProfile | null;
  dashboardShowDrawer: boolean;
  notifications: AppNotification[];
  runs: Run[];
  activeRun: Run | null;
  activeSamples: SamplePlusIGV[];
  rawDivaRuns: RawDivaRun[];
  activeCeleryTasks: CeleryTask[];
  reservedCeleryTasks: CeleryTask[];
  celeryWorkers: CeleryWorker[];
}
