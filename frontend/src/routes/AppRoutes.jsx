import { BrowserRouter } from "react-router-dom";
import Layout from "../components/layout/Layout";
import Login from "../pages/auth/Login";
import ProtectedRoute from "./ProtectedRoute";
import FollowUp from "../pages/compounder/FollowUp";
import CompounderDashboard from "../pages/compounder/Dashboard";
import RegisterPatient from "../pages/compounder/RegisterPatient";
import ReAppointment from "../pages/compounder/ReAppointment";
import TomorrowAppointments from "../pages/compounder/TomorrowAppointments";
import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";

function AppRoutes() {
  return (
    <BrowserRouter>
    
      <Routes> 
        <Route path="/" element={<Home />} />
        <Route path="/login/:role" element={<Login />} />
        <Route
        path="/compounder"
        element={
            <ProtectedRoute role="compounder">
            <Layout>
                <CompounderDashboard />
            </Layout>
            </ProtectedRoute>
        }
        />
        <Route
        path="/compounder/followup"
        element={
            <ProtectedRoute role="compounder">
            <Layout>
                <FollowUp />
            </Layout>
            </ProtectedRoute>
        }
        />



        <Route
        path="/compounder/register"
        element={
            <ProtectedRoute role="compounder">
            <Layout>
                <RegisterPatient />
            </Layout>
            </ProtectedRoute>
        }
        />
        <Route
        path="/compounder/reappointment"
        element={
            <ProtectedRoute role="compounder">
            <Layout>
                <ReAppointment />
            </Layout>
            </ProtectedRoute>
        }
        />
        <Route
        path="/compounder/tomorrow"
        element={
            <ProtectedRoute role="compounder">
            <Layout>
                <TomorrowAppointments />
            </Layout>
            </ProtectedRoute>
        }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;