
import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReactConfig from "eslint-plugin-react/configs/recommended.js";
import pluginReactHooks from "eslint-plugin-react-hooks";
import pluginReactRefresh from "eslint-plugin-react-refresh";

export default [
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node }
    }
  },
  pluginJs.configs.recommended,
  {
    ...pluginReactConfig,
    settings: {
      react: {
        version: "detect"
      }
    }
  },
  {
    files: ["src/**/*.{js,jsx}"],
    languageOptions: {
      parserOptions: {
        ecmaFeatures: {
          jsx: true
        }
      }
    },
    plugins: {
      "react-hooks": pluginReactHooks,
      "react-refresh": pluginReactRefresh,
    },
    rules: {
      ...pluginReactHooks.configs.recommended.rules,
      "react-refresh/only-export-components": "warn",
      "react/prop-types": "off",
      "react/react-in-jsx-scope": "off"
    },
  },
  {
    ignores: ["dist", "node_modules", "eslint.config.js"]
  }
];
