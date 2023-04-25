// import '@mdi/font/css/materialdesignicons.css'; // Ensure you are using css-loader
import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: 'mdi'
  },
  theme: {
    dark: false,
    themes: {
      light: {
        primary: '#C21659',
        secondary: '#00622B',
        accent: '#03a9f4',
        error: '#f44336',
        warning: '#ffc107',
        info: '#2196f3',
        success: '#4caf50'
      },
      dark: {
        primary: '#cddc39'
      }
    }
  }
});
