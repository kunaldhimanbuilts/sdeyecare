import { useNavigate } from "react-router-dom";
import logo from "../../assets/logo.png";
import { CLINIC } from "../../constants/clinic";
import logo2 from "../../assets/logo2.png";

function Header() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
    window.location.reload();
  };

  return (

    <div className="flex justify-between items-center px-6 py-1 bg-white shadow-sm border-b">

      <div className="flex items-center gap-3 overflow-hidden">
        <img
          src={logo}
          alt="logo"
          className="h-14 w-auto object-contain"
        />

        <h1 className="text-3xl font-extrabold text-blue-900">{CLINIC.name}</h1>
      </div>

      <button
        onClick={handleLogout}
        className="flex items-center gap-2 bg-blue-900 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
      >
        🔓 Logout
      </button>
    </div>


  );
}

export default Header;