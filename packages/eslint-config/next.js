module.exports = {
  extends: ["eslint:recommended", "plugin:react/recommended", "prettier"],
  env: {
    browser: true,
    node: true,
  },
  rules: {
    "react/react-in-jsx-scope": "off",
    "no-unused-vars": "warn",
  },
};
