import axios from "axios";

const api = axios.create({
 
  baseURL: import.meta.env.VITE_API_URL,
});

// Attach token automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});
// ============================================================
// UPDATE PATIENT PERSONAL DETAILS
// ============================================================

export const updatePatient = async (patientId, patientData) => {
  try {
    const response = await api.patch(
      `/patients/${patientId}`,
      patientData
    );

    return response.data;
  } catch (error) {
    console.error("Error updating patient:", error);

    throw error;
  }
};

export default api;



