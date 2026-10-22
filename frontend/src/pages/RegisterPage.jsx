import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Sparkles, Lock, Mail, User, Phone, Hash, Building2, ArrowRight, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { departmentService } from '../services/api';

export const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    role: 'student',
    phone: '',
    identifier: '',
    department_id: '',
    password: '',
    password_confirm: '',
  });
  const [departments, setDepartments] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  // Academic Departments / Engineering Branches for Students
  const defaultAcademicList = [
    { id: 'CSE', code: 'CSE', name: 'Computer Science & Engineering' },
    { id: 'ISE', code: 'ISE', name: 'Information Science & Engineering' },
    { id: 'ECE', code: 'ECE', name: 'Electronics & Communication Engineering' },
    { id: 'EEE', code: 'EEE', name: 'Electrical & Electronics Engineering' },
    { id: 'AIML', code: 'AIML', name: 'Artificial Intelligence & Machine Learning (AI/ML)' },
    { id: 'CSBS', code: 'CSBS', name: 'Computer Science & Business Systems (CSBS)' },
    { id: 'MECH', code: 'MECH', name: 'Mechanical Engineering' },
    { id: 'CIVIL_ENG', code: 'CIVIL_ENG', name: 'Civil Engineering' },
  ];

  // Maintenance & Facility Divisions for Technicians / Staff
  const defaultFacilityList = [
    { id: 'ELEC', code: 'ELEC', name: 'Electrical & Power Systems' },
    { id: 'PLUMB', code: 'PLUMB', name: 'Plumbing & Water Facilities' },
    { id: 'ITNET', code: 'ITNET', name: 'IT & Campus Network' },
    { id: 'CIVIL', code: 'CIVIL', name: 'Civil & Furniture Works' },
    { id: 'CLEAN', code: 'CLEAN', name: 'Housekeeping & Sanitation' },
    { id: 'LAB', code: 'LAB', name: 'Laboratory Safety & Equipment' },
  ];

  const academicDepartments = departments.filter((d) => d.category === 'academic');
  const facilityDepartments = departments.filter((d) => d.category === 'facility' || !d.category);

  const currentDeptOptions = formData.role === 'student'
    ? (academicDepartments.length > 0 ? academicDepartments : defaultAcademicList)
    : (facilityDepartments.length > 0 ? facilityDepartments : defaultFacilityList);

  useEffect(() => {
    const fetchDepts = async () => {
      try {
        const data = await departmentService.getDepartments();
        setDepartments(data);
      } catch (err) {
        console.error('Failed to load departments', err);
      }
    };
    fetchDepts();
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (formData.password !== formData.password_confirm) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        ...formData,
        department_id: formData.department_id ? Number(formData.department_id) : null,
      };
      await register(payload);
      navigate('/login?registered=true');
    } catch (err) {
      const errorMsg =
        err.response?.data?.email?.[0] ||
        err.response?.data?.password?.[0] ||
        err.response?.data?.error ||
        'Registration failed. Please check the form and try again.';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-lg space-y-6"
      >
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-blue-600 text-white flex items-center justify-center mx-auto shadow-md shadow-blue-500/20">
            <Sparkles className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">
            Join CampusFix
          </h2>
          <p className="text-xs text-slate-500">
            Sign up to report issues or manage campus maintenance requests
          </p>
        </div>

        <div className="bg-white p-7 rounded-3xl border border-slate-200/80 shadow-xl space-y-6">
          {error && (
            <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Role Switcher */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">
                Registering As
              </label>
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={() => setFormData((prev) => ({ ...prev, role: 'student', department_id: '' }))}
                  className={`py-2 px-3 rounded-xl text-xs font-semibold border transition-all ${
                    formData.role === 'student'
                      ? 'border-blue-600 bg-blue-50 text-blue-700 ring-2 ring-blue-500/20'
                      : 'border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  Student
                </button>
                <button
                  type="button"
                  onClick={() => setFormData((prev) => ({ ...prev, role: 'staff', department_id: '' }))}
                  className={`py-2 px-3 rounded-xl text-xs font-semibold border transition-all ${
                    formData.role === 'staff'
                      ? 'border-blue-600 bg-blue-50 text-blue-700 ring-2 ring-blue-500/20'
                      : 'border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  Technician / Staff
                </button>
              </div>
            </div>

            {/* Name Fields */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  First Name
                </label>
                <input
                  type="text"
                  name="first_name"
                  required
                  placeholder="Aarav"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  Last Name
                </label>
                <input
                  type="text"
                  name="last_name"
                  required
                  placeholder="Gupta"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                Campus Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                <input
                  type="email"
                  name="email"
                  required
                  placeholder="student@campusfix.edu"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full pl-10 pr-3.5 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Department & Identifier */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  {formData.role === 'student' ? 'Academic Branch / Dept' : 'Maintenance Division'}
                </label>
                <select
                  name="department_id"
                  value={formData.department_id}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                >
                  <option value="">
                    {formData.role === 'student' ? 'Select Branch (e.g. CSE, AI/ML)' : 'Select Facility Division'}
                  </option>
                  {currentDeptOptions.map((d) => (
                    <option key={d.id || d.code} value={d.id}>
                      {d.name} {d.code ? `(${d.code})` : ''}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  {formData.role === 'student' ? 'Roll Number' : 'Employee ID'}
                </label>
                <input
                  type="text"
                  name="identifier"
                  placeholder={formData.role === 'student' ? 'CS-2024-001' : 'STF-101'}
                  value={formData.identifier}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Passwords */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  required
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  Confirm
                </label>
                <input
                  type="password"
                  name="password_confirm"
                  required
                  placeholder="••••••••"
                  value={formData.password_confirm}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-xl text-sm font-semibold shadow-md shadow-blue-500/20 transition-all flex items-center justify-center gap-2 pt-2"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  <span>Create Account</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>

        <p className="text-center text-xs text-slate-500">
          Already registered?{' '}
          <Link to="/login" className="font-semibold text-blue-600 hover:text-blue-700">
            Sign In here
          </Link>
        </p>
      </motion.div>
    </div>
  );
};
export default RegisterPage;
