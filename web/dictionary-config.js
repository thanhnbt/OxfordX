// Edit this file, then run: python scripts/build_review.py
/* Điền API key Merriam-Webster Intermediate Dictionary tại MW_API_KEY.
   Đăng ký: https://dictionaryapi.com/register — product: Intermediate Dictionary.
   Endpoint: /api/v3/references/sd3/json/{word}
   Key trong JS/HTML sẽ nhìn thấy được khi publish; dùng proxy nếu cần giữ bí mật. */
window.MW_CONFIG = Object.assign({
  MW_API_KEY: '8be396cd-ccca-4b2b-bbc3-884ca4b71e7f',
  REFERENCE: 'sd3'
}, window.MW_CONFIG || {});
window.OXFORD_AUDIO = Object.assign({
  enabled: true,
  provider: 'merriam-webster',
  freeFallback: true,
  endpoint: 'https://api.dictionaryapi.dev/api/v2/entries/en/{word}',
  preferAccent: 'us',
  timeoutMs: 4500,
  // Optional dictionary proxy. It must return [{ phonetics: [{ audio: 'https://...' }] }].
  // Put a public/restricted client token here only if your provider supports it.
  // Secret paid-provider keys belong on your proxy server, never in this file.
  apiKey: '',
  apiKeyHeader: 'X-API-Key'
}, window.OXFORD_AUDIO || {});
