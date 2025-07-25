import axios from "axios"

export const BASE_URL=import.meta.env.VITE_BASE_PLOT_URL || 'http://localhost:8002'

const apiPlot=axios.create({baseURL:BASE_URL})

export default apiPlot;