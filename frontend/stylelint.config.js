module.exports = {
  extends: [
    "stylelint-config-recess-order", // cssプロパティの自動ソートを設定
    "stylelint-config-prettier", // Prettierとの競合ルールをOFFにする
  ],
  "rules": {
    "at-rule-no-unknown": [true,
      {"ignoreAtRules": ["include","mixin","each"]}],
  }
};