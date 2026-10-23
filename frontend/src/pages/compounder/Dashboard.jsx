import { useEffect, useState } from "react";
import api from "../../services/api";
import { useNavigate } from "react-router-dom";


function Dashboard() {
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] =useState(false);

  useEffect(() => {
    fetchToday();
  }, []);

  const fetchToday = async () => {
      setLoading(true);
      setError("");

      try {
          const res = await api.get("/appointments/todays");
          setAppointments(res.data);
      } catch (err) {
          console.error(err);

          if (!err.response) {
              setError("Unable to connect to the server.");
          } else if (err.response.status === 401) {
              setError("Session expired. Please login again.");
          } else {
              setError("Unable to load today's appointments.");
          }
      } finally {
          setLoading(false);
      }
  };
  return (
  <div className="min-h-screen bg-gray-100 p-3 sm:p-5 lg:p-6">

    {/* TOP CARDS */}
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 mb-6">

      {/* Register Patient */}
      <div className="bg-white rounded-2xl shadow-md p-4 sm:p-6 lg:p-8">
        <div className="bg-blue-50 rounded-xl p-4 sm:p-6 flex flex-col items-center">

          <div className="bg-blue-200 rounded-full p-4 text-3xl mb-5">
            👤
          </div>

          <button
            onClick={() => navigate("/compounder/register")}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-3 sm:py-4 text-base sm:text-lg font-semibold transition"
          >
            Register New Patient
          </button>

        </div>
      </div>

      {/* View Patients */}
      <div className="bg-white rounded-2xl shadow-md p-4 sm:p-6 lg:p-8">
        <div className="bg-green-50 rounded-xl p-4 sm:p-6 flex flex-col items-center">

          <div className="bg-green-200 rounded-full p-4 text-3xl mb-5">
            👥
          </div>

          <button
            onClick={() => navigate("/compounder/reappointment")}
            className="w-full bg-green-600 hover:bg-green-700 text-white rounded-xl py-3 sm:py-4 text-base sm:text-lg font-semibold transition"
          >
            View Existing Patients
          </button>

        </div>
      </div>

    </div>

    {error && (
    <div className="mb-4 rounded-lg border border-red-300 bg-red-100 px-4 py-3 text-red-700">
        {error}
    </div>
)}
{loading && (
    <div className="mb-4 rounded-lg bg-blue-100 border border-blue-300 px-4 py-3 text-blue-700">
        Loading today's appointments...
    </div>
)}
      {/* 🔷 TABLE SECTION */}
      <div className="bg-white rounded-2xl shadow-md p-6">

        <h2 className="text-lg font-semibold mb-4">
          Today's Appointments
        </h2>
        <div className="overflow-x-auto">

        <table className="w-full text-left">
          <thead>
            <tr className="bg-gray-100 text-gray-600 text-sm">
              <th className="p-2">Patient ID</th>
              <th className="p-2">Name</th>
              <th className="p-2">Phone</th>
              <th className="p-2">Doctor</th>
              <th className="p-2">Time</th>
            </tr>
          </thead>

          {/* <tbody>
            {appointments.map((a) => (
              <tr key={a.id} className="border-b hover:bg-gray-50">
                <td className="p-2">{a.patient_code}</td>
                <td className="p-2">{a.patient_name}</td>
                <td className="p-2">{a.patient_phone}</td>
                <td className="p-2">{a.doctor_name}</td>
                <td className="p-2">{a.time}</td>
              </tr>
            ))}
          </tbody>
          
          */}

<tbody>
  {!loading && !error && appointments.length === 0 ? (
    <tr>
      <td
        colSpan={5}
        className="p-6 text-center text-gray-500"
      >
        No appointments scheduled for today.
      </td>
    </tr>
  ) : (
    appointments.map((a) => (
      <tr key={a.id} className="border-b hover:bg-gray-50">
        <td className="p-2">{a.patient_code}</td>
        <td className="p-2">{a.patient_name}</td>
        <td className="p-2">{a.patient_phone || "-"}</td>
        <td className="p-2">{a.doctor_name}</td>
        <td className="p-2">{a.time}</td>
      </tr>
    ))
  )}
</tbody>


        </table>

      </div>

      {/* Bottom Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-6">

        <button
          onClick={() => navigate("/compounder/tomorrow")}
          className="w-full rounded-xl border-2 border-blue-500 py-3 px-4 font-semibold text-blue-600 hover:bg-blue-50 transition"
        >
          Tomorrow's Appointments
        </button>

        <button
          onClick={() => navigate("/compounder/followUp")}
          className="w-full rounded-xl border-2 border-blue-500 py-3 px-4 font-semibold text-blue-600 hover:bg-blue-50 transition"
        >
          Follow-Up Patients
        </button>

      </div>

    </div>

  </div>
);

}

export default Dashboard;