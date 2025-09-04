/**
 * 图片错误处理工具函数
 * 防止图片加载失败时出现重复请求和大量错误日志
 */

// 默认占位图片 SVG (Base64 编码)
const DEFAULT_PLACEHOLDER = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+CiAgPHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleWKoOi9veWbvueJhzwvdGV4dD4KICA8L3N2Zz4K'

/**
 * 处理图片加载错误的通用函数
 * @param {Event} event - 图片错误事件
 * @param {string} placeholder - 可选的占位图片，默认使用内置占位图
 * @param {boolean} enableLogging - 是否启用控制台日志，默认为 false
 */
export function handleImageError(event, placeholder = DEFAULT_PLACEHOLDER, enableLogging = false) {
  // 防止重复触发错误处理
  if (event.target.dataset.errorHandled === 'true') {
    return
  }

  // 标记已处理过错误
  event.target.dataset.errorHandled = 'true'

  // 移除错误事件监听器，防止再次触发
  event.target.removeEventListener('error', handleImageError)

  // 设置占位图片
  event.target.src = placeholder

  // 可选的日志记录
  if (enableLogging) {
    console.warn('图片加载失败，已替换为占位图片:', event.target.getAttribute('data-original-src') || event.target.src)
  }
}

/**
 * 创建一个图片错误处理器，可以预设参数
 * @param {string} placeholder - 占位图片
 * @param {boolean} enableLogging - 是否启用日志
 * @returns {Function} 错误处理函数
 */
export function createImageErrorHandler(placeholder = DEFAULT_PLACEHOLDER, enableLogging = false) {
  return (event) => handleImageError(event, placeholder, enableLogging)
}

/**
 * 为图片元素添加错误处理
 * @param {HTMLImageElement} imgElement - 图片元素
 * @param {string} placeholder - 占位图片
 * @param {boolean} enableLogging - 是否启用日志
 */
export function addImageErrorHandler(imgElement, placeholder = DEFAULT_PLACEHOLDER, enableLogging = false) {
  if (!(imgElement instanceof HTMLImageElement)) {
    console.error('参数必须是 HTMLImageElement')
    return
  }

  // 保存原始 src 用于日志记录
  if (!imgElement.dataset.originalSrc) {
    imgElement.dataset.originalSrc = imgElement.src
  }

  const errorHandler = createImageErrorHandler(placeholder, enableLogging)
  imgElement.addEventListener('error', errorHandler)
}

/**
 * 批量为图片元素添加错误处理
 * @param {NodeList|Array} imgElements - 图片元素数组或 NodeList
 * @param {string} placeholder - 占位图片
 * @param {boolean} enableLogging - 是否启用日志
 */
export function addBatchImageErrorHandler(imgElements, placeholder = DEFAULT_PLACEHOLDER, enableLogging = false) {
  if (!imgElements || !imgElements.length) {
    console.warn('没有找到图片元素')
    return
  }

  Array.from(imgElements).forEach(img => {
    addImageErrorHandler(img, placeholder, enableLogging)
  })
}

export default {
  handleImageError,
  createImageErrorHandler,
  addImageErrorHandler,
  addBatchImageErrorHandler,
  DEFAULT_PLACEHOLDER
}
