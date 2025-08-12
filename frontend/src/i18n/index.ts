import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './en.json';
import hi from './hi.json';
import ta from './ta.json';
import bn from './bn.json';

const resources = {
  en: {
    translation: en
  },
  hi: {
    translation: hi
  },
  ta: {
    translation: ta
  },
  bn: {
    translation: bn
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
