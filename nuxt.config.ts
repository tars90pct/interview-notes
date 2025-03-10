// https://nuxt.com/docs/api/configuration/nuxt-config
import fs from "fs";

const version = fs.readFileSync("./VERSION").toString();

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  ssr: false,
  devtools: { enabled: true },

  app: {
    baseURL: "/interview-notes/",
    buildAssetsDir: "assets",
  },

  modules: [
    "@nuxtjs/tailwindcss",
    "@nuxt/icon",
    "@nuxtjs/i18n",
    "@nuxtjs/color-mode",
    "@vueuse/nuxt",
    "@pinia/nuxt",
    "@nuxtjs/mdc",
    "@nuxtjs/google-fonts",
  ],

  i18n: {
    langDir: "locales",
    strategy: "no_prefix",
    locales: [
      {
        code: "en",
        iso: "en-US",
        file: "en.json",
      },
      {
        code: "zh-tw",
        iso: "zh-TW",
        file: "zh-tw.json",
      },
    ],
    defaultLocale: "zh-tw",
  },

  googleFonts: {
    families: {
      "Noto Serif TC": [400, 700],
      "Noto Sans TC": [400, 700],
    },
    display: "swap", // Optional: Optimize font loading
  },

  tailwindcss: {
    exposeConfig: true,
    editorSupport: true,
  },

  colorMode: {
    classSuffix: "",
  },

  runtimeConfig: {
    public: {
      version,
    },
  },

  imports: {
    imports: [
      {
        from: "tailwind-variants",
        name: "tv",
      },
      {
        from: "tailwind-variants",
        name: "VariantProps",
        type: true,
      },
    ],
  },
});