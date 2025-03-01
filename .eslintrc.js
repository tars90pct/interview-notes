module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  extends: ["@vue/eslint-config-standard", "eslint:recommended", "plugin:vue/vue3-recommended", "prettier"],
  parserOptions: {
    parser: "@babel/eslint-parser",
    requireConfigFile: false,
    sourceType: "module",
  },
  plugins: ["prettier"],
  rules: {
    "vue/multi-word-component-names": "off",
  },
};
