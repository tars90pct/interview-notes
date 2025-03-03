module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  extends: ["@nuxtjs/eslint-config-typescript", "prettier", "plugin:prettier/recommended"],
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
