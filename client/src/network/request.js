// 封装axios
import axios from 'axios'
function request(config) {
  const instance = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 5000
  })
  return instance(config)
}
export default request